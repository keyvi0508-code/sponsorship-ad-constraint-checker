"""Run the locked real-caption pilot without claiming full-video compliance or accuracy.

The default mode is a free, deterministic keyword run. --run-api adds a
separate billable two-stage AI run, retaining per-case output for resumption.
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

from src.ai_reviewer import DEFAULT_MODEL, MAX_OUTPUT_TOKENS, build_request
from src.evaluate_ai import USD_PER_MILLION_TOKENS, calculate_cost
from src.public_caption_intake import inspect_public_caption
from src.public_caption_reviewer import (
    EXTRACTION_INSTRUCTIONS, PROMPT_VERSION, SIGNAL_SCHEMA, SUGGESTION_SCHEMA,
    ai_review, decision_instructions, keyword_review,
)
from src.validate_data import load_jsonl

DEFAULT_DATA = ROOT / "data" / "real_public_reels_caption_development_v1.jsonl"
DEFAULT_MANIFEST = ROOT / "data" / "real_public_reels_caption_development_v1_manifest.json"
DEFAULT_PROMPT_MANIFEST = ROOT / "data" / "public_caption_prompt_manifest_v1.json"
DEFAULT_KEYWORD = ROOT / "reports" / "public_caption_keyword_v1.jsonl"
DEFAULT_AI = ROOT / "reports" / "public_caption_ai_v1.jsonl"
COST_CEILING_USD = 1.50
PRICE_VERIFIED_ON = "2026-10-02"
PRICE_SOURCE = "https://openrouter.ai/openai/gpt-6-sol"


def prompt_digest() -> str:
    """Fingerprint the actual two-stage instructions, schemas and rule source."""
    spec = {
        "prompt_version": PROMPT_VERSION, "model": DEFAULT_MODEL,
        "extraction_instructions": EXTRACTION_INSTRUCTIONS,
        "decision_instructions": decision_instructions(),
        "signal_schema": SIGNAL_SCHEMA, "suggestion_schema": SUGGESTION_SCHEMA,
        "rulebook_sha256": hashlib.sha256((ROOT / "data" / "rulebook.json").read_bytes()).hexdigest(),
    }
    return hashlib.sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def check_prompt_manifest(path: Path) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("status") != "PROMPT_LOCKED_BEFORE_MODEL_RUN" or manifest.get("prompt_version") != PROMPT_VERSION or manifest.get("sha256") != prompt_digest():
        raise ValueError("Caption AI prompt or rulebook differs from the pre-run lock")


def load_locked_rows(data: Path, manifest_path: Path) -> list[dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "SOURCE_SELECTION_LOCKED_BEFORE_MODEL_RUN":
        raise ValueError("Source selection has not been locked")
    if hashlib.sha256(data.read_bytes()).hexdigest() != manifest.get("sha256"):
        raise ValueError("Caption data checksum differs from the locked source manifest")
    rows = load_jsonl(data)
    if len(rows) != manifest.get("n_posts") or [row["id"] for row in rows] != manifest.get("selection_order"):
        raise ValueError("Caption rows differ from the locked selection order")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate source IDs")
    if any(inspect_public_caption(row)["caption_review_status"] != "READY_FOR_CAPTION_REVIEW" for row in rows):
        raise ValueError("A row lacks a complete original caption")
    return rows


def cost_upper_bound(rows: list[dict], model: str) -> float:
    """Use request UTF-8 bytes as a conservative input-token proxy."""
    price = USD_PER_MILLION_TOKENS.get(model)
    if price is None:
        raise ValueError(f"No dated cost snapshot for {model}")
    input_bytes = 0
    for row in rows:
        payload = {"caption_text": row["caption_text"]}
        requests = [
            build_request(model, EXTRACTION_INSTRUCTIONS, payload, "caption_signals", SIGNAL_SCHEMA),
            build_request(model, decision_instructions(), {**payload, "level1_signals": {"signals": []}}, "caption_suggestion", SUGGESTION_SCHEMA),
        ]
        input_bytes += sum(len(json.dumps(request, ensure_ascii=False).encode("utf-8")) for request in requests)
    # Reserve full Stage 1 output in the second request input as well.
    input_bytes += len(rows) * MAX_OUTPUT_TOKENS
    output_tokens = len(rows) * 2 * MAX_OUTPUT_TOKENS
    return (input_bytes * price["input"] + output_tokens * price["output"]) / 1_000_000


def distribution(results: list[dict]) -> dict[str, int]:
    counts = Counter(row["suggestion"] for row in results)
    return {key: counts[key] for key in ("PASS", "FLAG", "HUMAN_REVIEW", "UNKNOWN")}


def write_jsonl_exclusive(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--prompt-manifest", type=Path, default=DEFAULT_PROMPT_MANIFEST)
    parser.add_argument("--keyword-output", type=Path, default=DEFAULT_KEYWORD)
    parser.add_argument("--ai-output", type=Path, default=DEFAULT_AI)
    parser.add_argument("--model", default=os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL))
    parser.add_argument("--run-api", action="store_true", help="Send billable caption-only AI calls")
    parser.add_argument("--confirm-paid-run", action="store_true", help="Acknowledge authorized paid use")
    parser.add_argument("--resume", action="store_true", help="Keep completed AI rows and send only missing IDs")
    args = parser.parse_args()

    rows = load_locked_rows(args.data, args.manifest)
    baseline = [keyword_review(row) for row in rows]
    if args.keyword_output.exists():
        saved = load_jsonl(args.keyword_output)
        if saved != baseline:
            raise SystemExit("Existing keyword output differs; choose a new path instead of overwriting it")
    else:
        write_jsonl_exclusive(args.keyword_output, baseline)
    baseline_summary = {
        "evaluation_layer": "public_caption_development_pilot",
        "source_manifest_sha256": json.loads(args.manifest.read_text(encoding="utf-8"))["sha256"],
        "n_posts": len(rows), "method": "caption_literal_keyword_screen",
        "caption_suggestion_distribution": distribution(baseline),
        "full_review_status_distribution": {"UNKNOWN": len(rows)},
        "gold_labels_available": False, "accuracy_calculated": False,
        "note": "Keyword suggestions concern listed literal disclosure markers only. They are not video compliance judgements.",
    }
    baseline_summary_path = args.keyword_output.with_name(args.keyword_output.stem + "_summary.json")
    if baseline_summary_path.exists() and json.loads(baseline_summary_path.read_text(encoding="utf-8")) != baseline_summary:
        raise SystemExit("Existing keyword summary differs; choose a new path instead of overwriting it")
    if not baseline_summary_path.exists():
        baseline_summary_path.write_text(json.dumps(baseline_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"keyword_summary": baseline_summary, "keyword_output": str(args.keyword_output)}, ensure_ascii=False, indent=2))

    if not args.run_api:
        print(json.dumps({"api_status": "NOT_RUN", "reason": "--run-api was not supplied", "potential_calls": len(rows) * 2}, indent=2))
        return
    if not args.confirm_paid_run:
        raise SystemExit("Billable run blocked: --confirm-paid-run is required")
    check_prompt_manifest(args.prompt_manifest)
    if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")):
        raise SystemExit("Billable run blocked: no API key in this process environment. Do not paste it into chat or project files.")

    summary_path = args.ai_output.with_name(args.ai_output.stem + "_summary.json")
    if summary_path.exists():
        raise SystemExit("AI summary already exists; choose a new output path rather than overwriting it")
    if args.model not in USD_PER_MILLION_TOKENS:
        raise SystemExit(f"No dated cost snapshot for {args.model}; paid run blocked")
    if args.model != DEFAULT_MODEL:
        raise SystemExit(f"This public pilot has verified pricing only for {DEFAULT_MODEL}; paid run blocked for another model")
    existing = []
    if args.ai_output.exists():
        if not args.resume:
            raise SystemExit("AI output already exists; use --resume to retain completed rows")
        existing = load_jsonl(args.ai_output)
        ids = {row["id"] for row in rows}
        if len({item.get("id") for item in existing}) != len(existing) or any(item.get("id") not in ids for item in existing):
            raise SystemExit("Cannot resume: unexpected or duplicate AI row")
        if any(item.get("error") or item.get("prompt_version") != PROMPT_VERSION or item.get("model") != args.model for item in existing):
            raise SystemExit("Cannot resume: inspect error rows or incompatible prompt/model")
        if [item["id"] for item in existing] != [row["id"] for row in rows[:len(existing)]]:
            raise SystemExit("Cannot resume: completed AI rows do not match locked source order")
    elif args.resume:
        raise SystemExit("Cannot resume: AI output does not exist")
    completed_ids = {item["id"] for item in existing}
    pending = [row for row in rows if row["id"] not in completed_ids]
    prior_cost = sum(calculate_cost(args.model, item["usage"]) for item in existing)
    reserve = cost_upper_bound(pending[:1], args.model) if args.resume and pending else 0
    bound = prior_cost + cost_upper_bound(pending, args.model) + reserve
    if bound > COST_CEILING_USD:
        raise SystemExit(f"Billable run blocked: conservative ${bound:.4f} estimate exceeds ${COST_CEILING_USD:.2f} ceiling")
    print(f"Dated-rate conservative preflight: ${bound:.4f} for {len(pending)} pending posts; ceiling ${COST_CEILING_USD:.2f}.", flush=True)

    args.ai_output.parent.mkdir(parents=True, exist_ok=True)
    results = list(existing)
    with args.ai_output.open("a" if args.resume else "x", encoding="utf-8", newline="\n") as handle:
        for index, row in enumerate(pending, start=1):
            print(f"Reviewing {index}/{len(pending)}: {row['id']} (two caption-only API stages)", flush=True)
            try:
                result = ai_review(row, model=args.model)
                result["estimated_cost_usd"] = calculate_cost(args.model, result["usage"])
            except Exception as exc:
                # Stop immediately: a failed second stage may already have been billed.
                # Record no opaque provider body and no credential in the output.
                result = {"id": row["id"], "prompt_version": PROMPT_VERSION, "model": args.model,
                          "error": f"{type(exc).__name__}: {exc}"}
                handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                handle.flush()
                raise SystemExit(f"AI run stopped on {row['id']}; inspect the saved error row before a new run") from exc
            results.append(result)
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            handle.flush()
            print(f"Completed {row['id']}: {result['suggestion']}", flush=True)

    usage = Counter()
    for result in results:
        usage.update(result["usage"])
    summary = {
        "evaluation_layer": "public_caption_development_pilot",
        "date": date.today().isoformat(), "n_posts": len(rows), "n_ai_completed": len(results),
        "source_manifest_sha256": baseline_summary["source_manifest_sha256"],
        "prompt_sha256": prompt_digest(),
        "provider": "openrouter", "model": args.model, "prompt_version": PROMPT_VERSION,
        "caption_suggestion_distribution": distribution(results),
        "full_review_status_distribution": {"UNKNOWN": len(rows)},
        "keyword_ai_disagreements": sum(a["suggestion"] != b["suggestion"] for a, b in zip(baseline, results)),
        "usage": dict(usage),
        "estimated_total_cost_usd": round(sum(item["estimated_cost_usd"] for item in results), 8),
        "conservative_preflight_ceiling_usd": round(bound, 8),
        "cost_rate_snapshot": PRICE_VERIFIED_ON, "cost_rate_source": PRICE_SOURCE,
        "gold_labels_available": False, "accuracy_calculated": False,
        "note": "Caption suggestions are descriptive. No full-video or real-world accuracy result is claimed.",
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"ai_summary": summary, "ai_output": str(args.ai_output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
