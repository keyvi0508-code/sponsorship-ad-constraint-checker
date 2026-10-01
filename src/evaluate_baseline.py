"""Score the keyword baseline on a balanced, frozen 30-case dataset."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

from src.baseline import review_with_keyword_baseline
from src.validate_data import ALLOWED_VERDICTS, load_jsonl, validate_primary_set


def confusion_matrix(cases: List[Dict[str, Any]], predictions: Dict[str, str]) -> Dict[str, Dict[str, int]]:
    matrix = {gold: {pred: 0 for pred in sorted(ALLOWED_VERDICTS)} for gold in sorted(ALLOWED_VERDICTS)}
    for case in cases:
        gold = case["ground_truth"]["verdict"]
        matrix[gold][predictions[case["case_id"]]] += 1
    return matrix


def score_baseline(cases: List[Dict[str, Any]], expected_per_class: int = 10) -> Dict[str, Any]:
    validate_primary_set(cases, expected_per_class=expected_per_class)
    predictions = {case["case_id"]: review_with_keyword_baseline(case)["verdict"] for case in cases}
    correct = sum(predictions[case["case_id"]] == case["ground_truth"]["verdict"] for case in cases)
    matrix = confusion_matrix(cases, predictions)
    clean = [case for case in cases if case["ground_truth"]["verdict"] == "PASS"]
    violating = [case for case in cases if case["ground_truth"]["verdict"] == "FLAG"]
    borderline = [case for case in cases if case["ground_truth"]["verdict"] == "HUMAN_REVIEW"]
    return {
        "n": len(cases),
        "accuracy": correct / len(cases),
        "confusion_matrix": matrix,
        "false_positives_on_clean": sum(predictions[c["case_id"]] == "FLAG" for c in clean),
        "false_negatives_on_violations": sum(predictions[c["case_id"]] == "PASS" for c in violating),
        "borderline_escalations": sum(predictions[c["case_id"]] == "HUMAN_REVIEW" for c in borderline),
        "predictions": predictions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path, help="Path to the frozen JSONL primary set")
    parser.add_argument("--expected-per-class", type=int, default=10)
    args = parser.parse_args()
    report = score_baseline(load_jsonl(args.cases), expected_per_class=args.expected_per_class)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
