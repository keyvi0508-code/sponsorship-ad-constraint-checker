"""Run a cost-recorded AI evaluation. No paid call occurs without --run-api."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

from src.ai_reviewer import (
    ASSERTION_SCHEMA, DECISION_SCHEMA, EXTRACTION_INSTRUCTIONS, MAX_OUTPUT_TOKENS, PROMPT_VERSION,
    ApiAuthenticationError, build_request, decision_instructions, review_case,
)
from src.validate_data import ALLOWED_VERDICTS, load_jsonl, validate_primary_set

PRICE_DATE = "2026-09-30"
AUTHORIZED_COST_CEILING_USD = 1.50
USD_PER_MILLION_TOKENS = {
    # Standard processing rates. Do not use the lower Batch/Flex rates unless
    # the request is explicitly submitted under one of those processing modes.
    "openai/gpt-6-luna": {"input": 0.10, "output": 0.50},
    "openai/gpt-6-sol": {"input": 2.00, "output": 10.00},
    "openai/gpt-6-astra": {"input": 10.00, "output": 50.00},
}


def calculate_cost(model: str, usage: Dict[str, int]) -> float | None:
    price = USD_PER_MILLION_TOKENS.get(model)
    if price is None:
        return None
    return (usage["input_tokens"] * price["input"] + usage["output_tokens"] * price["output"]) / 1_000_000


def estimate_run_upper_bound(cases: List[Dict[str, Any]], model: str) -> float | None:
    """Conservatively preflight max output plus UTF-8 request bytes as input tokens."""
    price = USD_PER_MILLION_TOKENS.get(model)
    if price is None:
        return None
    input_bytes = 0
    for case in cases:
        # case_for_model strips labels/notes before constructing either API input.
        from src.validate_data import case_for_model
        review_input = case_for_model(case)
        stage1 = build_request(model, EXTRACTION_INSTRUCTIONS, review_input, "script_evidence", ASSERTION_SCHEMA)
        stage2 = build_request(
            model, decision_instructions(), {"script": review_input, "level1_evidence": {"signals": []}},
            "script_verdict", DECISION_SCHEMA,
        )
        input_bytes += len(json.dumps(stage1, ensure_ascii=False).encode("utf-8"))
        input_bytes += len(json.dumps(stage2, ensure_ascii=False).encode("utf-8"))
    # JSON schema/input bytes are a deliberately conservative proxy for input
    # tokens; output is capped per request in the API request itself.
    output_tokens = len(cases) * 2 * MAX_OUTPUT_TOKENS
    # The Level 1 JSON is also included in Level 2 input; reserve its full
    # output cap as additional input for a conservative ceiling.
    input_bytes += len(cases) * MAX_OUTPUT_TOKENS
    return (input_bytes * price["input"] + output_tokens * price["output"]) / 1_000_000


def score_predictions(cases: List[Dict[str, Any]], predictions: Dict[str, str]) -> Dict[str, Any]:
    classes = sorted(ALLOWED_VERDICTS)
    matrix = {gold: {pred: 0 for pred in classes} for gold in classes}
    for case in cases:
        if case["case_id"] in predictions:
            matrix[case["ground_truth"]["verdict"]][predictions[case["case_id"]]] += 1
    correct = sum(predictions.get(c["case_id"]) == c["ground_truth"]["verdict"] for c in cases)
    clean = [c for c in cases if c["ground_truth"]["verdict"] == "PASS"]
    violations = [c for c in cases if c["ground_truth"]["verdict"] == "FLAG"]
    borderline = [c for c in cases if c["ground_truth"]["verdict"] == "HUMAN_REVIEW"]
    return {
        "n": len(cases),
        "accuracy": correct / len(cases) if cases else None,
        "confusion_matrix": matrix,
        "false_positives_on_clean": sum(predictions.get(c["case_id"]) == "FLAG" for c in clean),
        "human_escalations_on_clean": sum(predictions.get(c["case_id"]) == "HUMAN_REVIEW" for c in clean),
        "false_negatives_marked_safe": sum(predictions.get(c["case_id"]) == "PASS" for c in violations),
        "violations_escalated_instead_of_flagged": sum(predictions.get(c["case_id"]) == "HUMAN_REVIEW" for c in violations),
        "borderline_escalations": sum(predictions.get(c["case_id"]) == "HUMAN_REVIEW" for c in borderline),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", nargs="?", type=Path, default=Path("data/primary_cases.jsonl"))
    parser.add_argument("--output", type=Path, default=Path(f"reports/ai_evaluation_{PROMPT_VERSION}.jsonl"))
    parser.add_argument("--summary", type=Path, default=Path(f"reports/ai_evaluation_{PROMPT_VERSION}_summary.json"))
    parser.add_argument("--manifest", type=Path, default=Path("data/frozen_manifest.json"))
    parser.add_argument("--model", default=os.environ.get("OPENROUTER_MODEL", "openai/gpt-6-sol"))
    parser.add_argument("--expected-per-class", type=int, default=10, help="Expected cases in each verdict class (10 for 30 cases, 20 for 60).")
    parser.add_argument("--run-api", action="store_true", help="Make billable API calls; without this flag the command is a no-call dry run.")
    parser.add_argument("--confirm-paid-run", action="store_true", help="Confirm that the user has approved API spending for this run.")
    parser.add_argument("--resume", action="store_true", help="Continue an existing partial result file; only missing cases are sent.")
    args = parser.parse_args()

    cases = load_jsonl(args.cases)
    validate_primary_set(cases, expected_per_class=args.expected_per_class)
    if not args.run_api:
        print(json.dumps({
            "mode": "dry_run_no_api_calls",
            "cases_validated": len(cases),
            "model_selected": args.model,
            "calls_that_would_be_made": len(cases) * 2,
            "next_step": "Set OPENROUTER_API_KEY locally, then rerun with --run-api --confirm-paid-run after explicit spending approval.",
        }, indent=2))
        return

    if not args.confirm_paid_run:
        raise SystemExit("Billable run blocked. Obtain the user's explicit spending approval, then pass --confirm-paid-run.")

    if not args.manifest.exists():
        raise SystemExit("Billable run blocked: no frozen dataset manifest. Finish blind review, reconcile labels, then run src.freeze_dataset.")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    digest = hashlib.sha256(args.cases.read_bytes()).hexdigest()
    if manifest.get("status") != "FROZEN" or manifest.get("sha256") != digest:
        raise SystemExit("Billable run blocked: the dataset is not frozen or its hash no longer matches the freeze manifest.")

    if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")):
        raise SystemExit("OPENROUTER_API_KEY is not set. Configure it locally; never put the key in project files.")

    existing_results: List[Dict[str, Any]] = []
    completed_ids = set()
    if args.output.exists():
        if not args.resume:
            raise SystemExit(
                f"Output file already exists: {args.output}. Use --resume to continue it, "
                "or choose a new --output path; existing results will not be overwritten."
            )
        for line_number, line in enumerate(args.output.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                result = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Cannot resume: invalid JSON on output line {line_number}.") from exc
            case_id = result.get("case_id")
            if case_id not in {case["case_id"] for case in cases} or case_id in completed_ids:
                raise SystemExit(f"Cannot resume: unexpected or duplicate case ID {case_id!r}.")
            if result.get("prompt_version") != PROMPT_VERSION or result.get("model") != args.model:
                raise SystemExit("Cannot resume: existing rows use a different prompt version or model.")
            if result.get("error"):
                raise SystemExit(f"Cannot resume: {case_id} has an error row; inspect it before retrying.")
            completed_ids.add(case_id)
            existing_results.append(result)
    elif args.resume:
        raise SystemExit(f"Cannot resume: output file does not exist: {args.output}")

    pending_cases = [case for case in cases if case["case_id"] not in completed_ids]

    pending_cost_upper_bound = estimate_run_upper_bound(pending_cases, args.model) if pending_cases else 0.0
    completed_costs = [calculate_cost(args.model, result["usage"]) for result in existing_results]
    if pending_cost_upper_bound is None or any(cost is None for cost in completed_costs):
        raise SystemExit(f"No verified pricing snapshot for model {args.model}; paid run blocked.")
    completed_cost = sum(completed_costs)
    # If resuming after an interruption, the in-flight case may have been billed
    # without producing a saved row. Reserve one extra case to cover its retry.
    interrupted_case_reserve = (
        estimate_run_upper_bound([pending_cases[0]], args.model)
        if args.resume and pending_cases else 0.0
    )
    cost_upper_bound = completed_cost + pending_cost_upper_bound + (interrupted_case_reserve or 0.0)
    if cost_upper_bound > AUTHORIZED_COST_CEILING_USD:
        raise SystemExit(
            f"Paid run blocked: conservative estimated ceiling ${cost_upper_bound:.4f} exceeds "
            f"the authorized ${AUTHORIZED_COST_CEILING_USD:.2f} limit."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, Any]] = list(existing_results)
    file_mode = "a" if args.resume else "x"
    with args.output.open(file_mode, encoding="utf-8", newline="\n") as handle:
        print(
            f"Starting {len(pending_cases)} remaining case(s) with prompt {PROMPT_VERSION}; "
            f"{len(existing_results)} completed result(s) will be kept."
        )
        for index, case in enumerate(pending_cases, start=1):
            print(f"Reviewing {index}/{len(pending_cases)}: {case['case_id']} (two API stages)", flush=True)
            try:
                result = review_case(case, model=args.model)
                result["estimated_cost_usd"] = calculate_cost(args.model, result["usage"])
            except ApiAuthenticationError as exc:
                result = {"case_id": case["case_id"], "model": args.model, "error": str(exc)}
                results.append(result)
                handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                handle.flush()
                raise SystemExit(
                    "Evaluation stopped at the first authentication error. Check the API provider/key; "
                    "no further cases were sent."
                ) from exc
            except Exception as exc:  # Keep failures visible and include them in structured-output rate.
                result = {"case_id": case["case_id"], "model": args.model, "error": f"{type(exc).__name__}: {exc}"}
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            handle.flush()
            if result.get("verdict") in ALLOWED_VERDICTS:
                print(f"Completed {case['case_id']}: {result['verdict']}", flush=True)
            else:
                print(f"Recorded an error for {case['case_id']}; check the output file.", flush=True)

    predictions = {r["case_id"]: r["verdict"] for r in results if r.get("verdict") in ALLOWED_VERDICTS}
    usage_totals = Counter()
    total_cost = 0.0
    cost_complete = True
    for result in results:
        if "usage" in result:
            usage_totals.update(result["usage"])
        if result.get("estimated_cost_usd") is None:
            cost_complete = False
        else:
            total_cost += result["estimated_cost_usd"]

    summary = {
        "evaluation_status": "DRAFT_DATASET_DEVELOPMENT_RUN",
        "provider": "openrouter",
        "prompt_version": PROMPT_VERSION,
        "resumed_partial_run": args.resume,
        "cases_completed_before_this_run": len(existing_results),
        "cases_sent_this_run": len(pending_cases),
        "prompt_version": PROMPT_VERSION,
        "date": date.today().isoformat(),
        "price_verified_on": PRICE_DATE,
        "model": args.model,
        "pricing_usd_per_million_tokens": USD_PER_MILLION_TOKENS.get(args.model),
        "n_cases": len(cases),
        "successful_structured_outputs": len(predictions),
        "structured_output_rate": len(predictions) / len(cases),
        "usage": dict(usage_totals),
        "total_estimated_cost_usd": round(total_cost, 8) if cost_complete else None,
        "preflight_cost_upper_bound_usd": round(cost_upper_bound, 8),
        "authorized_cost_ceiling_usd": AUTHORIZED_COST_CEILING_USD,
        "estimated_cost_per_case_usd": round(total_cost / len(cases), 8) if cost_complete else None,
        "metrics": score_predictions(cases, predictions),
        "results_path": str(args.output),
        "note": "A prompt revised after inspecting prior outputs is development evidence; use a fresh holdout for an independent evaluation.",
    }
    args.summary.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
