"""Compare one API stage with the saved two-stage synthetic extension run.

No API call occurs without --run-api --confirm-paid-run. This retrospective
design comparison is development evidence, not an independent benchmark.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai_reviewer import DECISION_SCHEMA, DEFAULT_MODEL, MAX_OUTPUT_TOKENS, build_request
from src.evaluate_ai import USD_PER_MILLION_TOKENS, calculate_cost, score_predictions
from src.single_stage_reviewer import PROMPT_VERSION, review_case_single_stage, single_stage_instructions
from src.validate_data import case_for_model, load_jsonl, validate_primary_set

DATA = ROOT / "data" / "extension_cases_v2.jsonl"
DATA_MANIFEST = ROOT / "data" / "extension_frozen_manifest_v2.json"
PROMPT_MANIFEST = ROOT / "data" / "single_stage_prompt_manifest_v1.json"
TWO_STAGE = ROOT / "reports" / "ai_evaluation_extension_v2.jsonl"
OUTPUT = ROOT / "reports" / "single_stage_ablation_extension_v2.jsonl"
COST_CEILING_USD = 1.50


def prompt_digest() -> str:
    spec = {"prompt_version": PROMPT_VERSION, "model": DEFAULT_MODEL,
            "instructions": single_stage_instructions(), "decision_schema": DECISION_SCHEMA,
            "rulebook_sha256": hashlib.sha256((ROOT / "data" / "rulebook.json").read_bytes()).hexdigest()}
    return hashlib.sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def load_inputs() -> list[dict]:
    manifest = json.loads(DATA_MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "FROZEN" or hashlib.sha256(DATA.read_bytes()).hexdigest() != manifest.get("sha256"):
        raise ValueError("Extension data differs from its frozen manifest")
    cases = load_jsonl(DATA)
    validate_primary_set(cases, expected_per_class=10)
    return cases


def check_prompt_lock() -> None:
    manifest = json.loads(PROMPT_MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "PROMPT_LOCKED_BEFORE_ABLATION_RUN" or manifest.get("prompt_version") != PROMPT_VERSION or manifest.get("sha256") != prompt_digest():
        raise ValueError("One-stage prompt differs from its pre-run manifest")


def cost_upper_bound(cases: list[dict]) -> float:
    rates = USD_PER_MILLION_TOKENS[DEFAULT_MODEL]
    request_bytes = sum(len(json.dumps(build_request(
        DEFAULT_MODEL, single_stage_instructions(), case_for_model(case),
        "single_stage_script_verdict", DECISION_SCHEMA
    ), ensure_ascii=False).encode("utf-8")) for case in cases)
    return (request_bytes * rates["input"] + len(cases) * MAX_OUTPUT_TOKENS * rates["output"]) / 1_000_000


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-api", action="store_true")
    parser.add_argument("--confirm-paid-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    cases = load_inputs()
    check_prompt_lock()
    prior = load_jsonl(TWO_STAGE)
    if len(prior) != len(cases) or [x["case_id"] for x in prior] != [x["case_id"] for x in cases]:
        raise ValueError("Saved two-stage comparison does not align with frozen extension cases")
    bound = cost_upper_bound(cases)
    if not args.run_api:
        print(json.dumps({"mode": "dry_run_no_api_calls", "cases": len(cases),
                          "one_stage_calls_if_run": len(cases), "two_stage_saved_calls": len(cases) * 2,
                          "conservative_cost_upper_bound_usd": round(bound, 6),
                          "prompt_sha256": prompt_digest(),
                          "design_limit": "Exploratory retrospective ablation on synthetic cases already inspected"}, indent=2))
        return
    if not args.confirm_paid_run:
        raise SystemExit("Billable ablation blocked: --confirm-paid-run required")
    if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")):
        raise SystemExit("Billable ablation blocked: no API key in this process environment")

    summary_path = args.output.with_name(args.output.stem + "_summary.json")
    if summary_path.exists():
        raise SystemExit("Ablation summary already exists; choose a new output path")
    existing = []
    if args.output.exists():
        if not args.resume:
            raise SystemExit("Ablation output already exists; use --resume")
        existing = load_jsonl(args.output)
        if [item.get("case_id") for item in existing] != [case["case_id"] for case in cases[:len(existing)]]:
            raise SystemExit("Cannot resume: saved rows do not match frozen order")
        if any(item.get("error") or item.get("prompt_version") != PROMPT_VERSION or item.get("model") != DEFAULT_MODEL for item in existing):
            raise SystemExit("Cannot resume: incompatible or error row")
    elif args.resume:
        raise SystemExit("Cannot resume: ablation output does not exist")
    pending = cases[len(existing):]
    prior_cost = sum(calculate_cost(DEFAULT_MODEL, item["usage"]) for item in existing)
    # Reserve an interrupted request for a resume, because it may have been billed.
    cost_limit_estimate = prior_cost + cost_upper_bound(pending) + (cost_upper_bound(pending[:1]) if args.resume and pending else 0)
    if cost_limit_estimate > COST_CEILING_USD:
        raise SystemExit(f"Billable ablation blocked: ${cost_limit_estimate:.4f} exceeds ${COST_CEILING_USD:.2f} ceiling")
    print(f"Starting {len(pending)} single-stage cases; dated-rate cost ceiling ${cost_limit_estimate:.4f}.", flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    results = list(existing)
    with args.output.open("a" if args.resume else "x", encoding="utf-8", newline="\n") as handle:
        for index, case in enumerate(pending, start=1):
            print(f"Reviewing {index}/{len(pending)}: {case['case_id']}", flush=True)
            try:
                result = review_case_single_stage(case, model=DEFAULT_MODEL)
                result["estimated_cost_usd"] = calculate_cost(DEFAULT_MODEL, result["usage"])
            except Exception as exc:
                error = {"case_id": case["case_id"], "prompt_version": PROMPT_VERSION,
                         "model": DEFAULT_MODEL, "error": f"{type(exc).__name__}: {exc}"}
                handle.write(json.dumps(error, ensure_ascii=False) + "\n")
                handle.flush()
                raise SystemExit(f"Ablation stopped on {case['case_id']}; inspect error row") from exc
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            handle.flush()
            print(f"Completed {case['case_id']}: {result['verdict']}", flush=True)

    new_predictions = {item["case_id"]: item["verdict"] for item in results}
    prior_predictions = {item["case_id"]: item["verdict"] for item in prior}
    usage = Counter()
    for item in results:
        usage.update(item["usage"])
    summary = {
        "status": "EXPLORATORY_SYNTHETIC_DEVELOPMENT_ABLATION",
        "date": date.today().isoformat(), "n_cases": len(cases),
        "model": DEFAULT_MODEL, "prompt_version": PROMPT_VERSION,
        "prompt_sha256": prompt_digest(), "dataset_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "single_stage_metrics": score_predictions(cases, new_predictions),
        "saved_two_stage_metrics": score_predictions(cases, prior_predictions),
        "one_vs_two_stage_verdict_disagreements": sum(new_predictions[c["case_id"]] != prior_predictions[c["case_id"]] for c in cases),
        "single_stage_usage": dict(usage),
        "single_stage_estimated_cost_usd": round(sum(item["estimated_cost_usd"] for item in results), 8),
        "saved_two_stage_estimated_cost_usd": round(sum(item["estimated_cost_usd"] for item in prior), 8),
        "gold_labels_available": True,
        "limitation": "Prompt designed after two-stage outputs were inspected; no independent generalization claim.",
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
