"""Validate and summarize saved real-caption method outputs without gold labels."""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_public_captions import check_prompt_manifest, load_locked_rows, prompt_digest
from src.ai_reviewer import DEFAULT_MODEL
from src.evaluate_ai import calculate_cost
from src.public_caption_reviewer import PROMPT_VERSION
from src.validate_data import load_jsonl

DATA = ROOT / "data" / "real_public_reels_caption_development_v1.jsonl"
MANIFEST = ROOT / "data" / "real_public_reels_caption_development_v1_manifest.json"
KEYWORD = ROOT / "reports" / "public_caption_keyword_v1.jsonl"
AI = ROOT / "reports" / "public_caption_ai_v1.jsonl"
OUTPUT = ROOT / "reports" / "public_caption_pilot_analysis_v1.json"
ORDER = ("PASS", "FLAG", "HUMAN_REVIEW", "UNKNOWN")


def analyze() -> dict:
    rows = load_locked_rows(DATA, MANIFEST)
    check_prompt_manifest(ROOT / "data" / "public_caption_prompt_manifest_v1.json")
    keyword = load_jsonl(KEYWORD)
    ai = load_jsonl(AI)
    saved_summary = json.loads((ROOT / "reports" / "public_caption_ai_v1_summary.json").read_text(encoding="utf-8"))
    ids = [row["id"] for row in rows]
    if [item.get("id") for item in keyword] != ids or [item.get("id") for item in ai] != ids:
        raise ValueError("Saved results differ from the locked source order")
    if any(item.get("error") or item.get("scope") != "captured_caption_only" or item.get("full_review_status") != "UNKNOWN" for item in ai + keyword):
        raise ValueError("A method output is incomplete or exceeds caption-only scope")
    if any(item.get("prompt_version") != PROMPT_VERSION or item.get("model") != DEFAULT_MODEL or item.get("provider") != "openrouter" for item in ai):
        raise ValueError("AI rows differ from the locked model or prompt version")
    if saved_summary.get("prompt_sha256") != prompt_digest() or saved_summary.get("source_manifest_sha256") != hashlib.sha256(DATA.read_bytes()).hexdigest():
        raise ValueError("Saved AI summary differs from locked prompt or source")
    for item in ai:
        expected_cost = calculate_cost(DEFAULT_MODEL, item["usage"])
        if abs(item.get("estimated_cost_usd", -1) - expected_cost) > 1e-8:
            raise ValueError(f"{item['id']}: saved cost differs from reported token usage")
    for source, result in zip(rows, ai):
        caption = source["caption_text"]
        for quote in [signal["quote"] for signal in result["signals"]] + [finding["quote"] for finding in result["findings"]]:
            if quote and quote not in caption:
                raise ValueError(f"{source['id']}: saved evidence is not an exact caption quote")
    matrix = {left: {right: 0 for right in ORDER} for left in ORDER}
    for left, right in zip(keyword, ai):
        matrix[left["suggestion"]][right["suggestion"]] += 1
    keyword_counts = Counter(item["suggestion"] for item in keyword)
    ai_counts = Counter(item["suggestion"] for item in ai)
    if saved_summary.get("caption_suggestion_distribution") != {label: ai_counts[label] for label in ORDER}:
        raise ValueError("Saved AI summary distribution differs from case-level results")
    relationship_matrix = {name: {label: 0 for label in ORDER} for name in sorted({row["relationship_signal"] for row in rows})}
    for source, result in zip(rows, ai):
        relationship_matrix[source["relationship_signal"]][result["suggestion"]] += 1
    latencies = [item["latency_seconds"] for item in ai]
    return {
        "status": "SAVED_CAPTION_RUN_VALIDATED",
        "n_posts": len(rows),
        "source_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "keyword_distribution": {label: keyword_counts[label] for label in ORDER},
        "ai_distribution": {label: ai_counts[label] for label in ORDER},
        "keyword_to_ai_matrix": matrix,
        "disagreements": sum(left["suggestion"] != right["suggestion"] for left, right in zip(keyword, ai)),
        "ai_by_creator_authored_relationship_signal": relationship_matrix,
        "ai_finding_rule_counts": dict(sorted(Counter(finding["rule_id"] for item in ai for finding in item["findings"]).items())),
        "saved_evidence_quotes_outside_caption": 0,
        "full_review_status_distribution": {"UNKNOWN": len(rows)},
        "latency_median_seconds": round(statistics.median(latencies), 3),
        "estimated_total_cost_usd": round(sum(item["estimated_cost_usd"] for item in ai), 6),
        "estimated_cost_per_post_usd": round(sum(item["estimated_cost_usd"] for item in ai) / len(rows), 6),
        "reference_labels_available": False,
        "accuracy_calculated": False,
        "interpretation": "Descriptive method behavior on a purposively selected caption-only sample; no full-video compliance or accuracy claim.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Save the audit summary without overwriting an existing file")
    args = parser.parse_args()
    result = analyze()
    if args.write:
        with OUTPUT.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
