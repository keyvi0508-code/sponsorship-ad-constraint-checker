"""Recheck the saved one-stage ablation against frozen cases and two-stage rows."""
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_single_stage_ablation import check_prompt_lock, load_inputs, prompt_digest
from src.ai_reviewer import DEFAULT_MODEL
from src.evaluate_ai import calculate_cost, score_predictions
from src.single_stage_reviewer import PROMPT_VERSION
from src.validate_data import load_jsonl

SINGLE = ROOT / "reports" / "single_stage_ablation_extension_v2.jsonl"
TWO = ROOT / "reports" / "ai_evaluation_extension_v2.jsonl"
SUMMARY = ROOT / "reports" / "single_stage_ablation_extension_v2_summary.json"


def analyze() -> dict:
    cases = load_inputs()
    check_prompt_lock()
    one = load_jsonl(SINGLE)
    two = load_jsonl(TWO)
    saved = json.loads(SUMMARY.read_text(encoding="utf-8"))
    ids = [case["case_id"] for case in cases]
    if [item.get("case_id") for item in one] != ids or [item.get("case_id") for item in two] != ids:
        raise ValueError("Saved ablation rows differ from frozen case order")
    if saved.get("prompt_sha256") != prompt_digest() or saved.get("dataset_sha256") != hashlib.sha256((ROOT / "data" / "extension_cases_v2.jsonl").read_bytes()).hexdigest():
        raise ValueError("Saved ablation summary differs from frozen prompt or data")
    if any(item.get("prompt_version") != PROMPT_VERSION or item.get("model") != DEFAULT_MODEL or item.get("error") for item in one):
        raise ValueError("One-stage output has an error or incompatible prompt/model")
    if any(abs(item["estimated_cost_usd"] - calculate_cost(DEFAULT_MODEL, item["usage"])) > 1e-8 for item in one + two):
        raise ValueError("A saved case cost does not match token usage")
    one_pred = {item["case_id"]: item["verdict"] for item in one}
    two_pred = {item["case_id"]: item["verdict"] for item in two}
    one_metrics = score_predictions(cases, one_pred)
    two_metrics = score_predictions(cases, two_pred)
    if saved.get("single_stage_metrics") != one_metrics or saved.get("saved_two_stage_metrics") != two_metrics:
        raise ValueError("Saved summary metrics do not match case-level predictions")
    differences = [
        {"case_id": case["case_id"], "reference_verdict": case["ground_truth"]["verdict"],
         "reference_rule_ids": case["ground_truth"]["rule_ids"],
         "single_stage_verdict": one_item["verdict"], "two_stage_verdict": two_item["verdict"],
         "single_stage_rule_ids": [f["rule_id"] for f in one_item["findings"]],
         "two_stage_rule_ids": [f["rule_id"] for f in two_item["findings"]]}
        for case, one_item, two_item in zip(cases, one, two)
        if one_item["verdict"] != two_item["verdict"]
    ]
    one_cost = sum(item["estimated_cost_usd"] for item in one)
    two_cost = sum(item["estimated_cost_usd"] for item in two)
    return {
        "status": "SAVED_ABLATION_VERIFIED",
        "n_cases": len(cases), "verdict_disagreements": differences,
        "single_stage_correct": sum(one_pred[c["case_id"]] == c["ground_truth"]["verdict"] for c in cases),
        "two_stage_correct": sum(two_pred[c["case_id"]] == c["ground_truth"]["verdict"] for c in cases),
        "single_stage_false_negatives_marked_safe": one_metrics["false_negatives_marked_safe"],
        "two_stage_false_negatives_marked_safe": two_metrics["false_negatives_marked_safe"],
        "single_stage_estimated_cost_usd": round(one_cost, 6),
        "two_stage_estimated_cost_usd": round(two_cost, 6),
        "single_stage_cost_as_fraction_of_two_stage": round(one_cost / two_cost, 4),
        "single_stage_median_latency_seconds": round(statistics.median(item["latency_seconds"] for item in one), 3),
        "two_stage_median_latency_seconds": round(statistics.median(item["latency_seconds"] for item in two), 3),
        "independent_validation": False,
        "interpretation": "Exploratory comparison on constructed cases after prior output inspection; no causal or real-world superiority claim.",
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
