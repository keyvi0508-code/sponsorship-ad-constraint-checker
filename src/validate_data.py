"""Loading and validation for the ground-truth primary dataset."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List

ALLOWED_VERDICTS = {"PASS", "FLAG", "HUMAN_REVIEW"}
REQUIRED_TOP_LEVEL = {"case_id", "language", "format", "multiple_brands", "caption", "scenes", "ground_truth"}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc.msg}") from exc
            if not isinstance(case, dict):
                raise ValueError(f"Line {line_number} must contain a JSON object")
            cases.append(case)
    return cases


def validate_case(case: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    missing = REQUIRED_TOP_LEVEL - set(case)
    if missing:
        errors.append("missing required fields: " + ", ".join(sorted(missing)))
        return errors
    if case["language"] != "en":
        errors.append("primary set must be English-only (language='en')")
    if case["format"] != "short_video":
        errors.append("format must be short_video")
    if not isinstance(case["multiple_brands"], bool):
        errors.append("multiple_brands must be a boolean")
    if not isinstance(case["caption"], list):
        errors.append("caption must be an ordered list of lines")
    if not isinstance(case["scenes"], list):
        errors.append("scenes must be an ordered list")
    truth = case["ground_truth"]
    if not isinstance(truth, dict):
        errors.append("ground_truth must be an object")
    else:
        if truth.get("verdict") not in ALLOWED_VERDICTS:
            errors.append("ground_truth.verdict must be PASS, FLAG, or HUMAN_REVIEW")
        if not isinstance(truth.get("rule_ids"), list):
            errors.append("ground_truth.rule_ids must be a list")
        if not isinstance(truth.get("rationale"), str) or not truth.get("rationale", "").strip():
            errors.append("ground_truth.rationale must be a non-empty string")
    return errors


def validate_primary_set(cases: Iterable[Dict[str, Any]], expected_per_class: int = 10) -> None:
    cases = list(cases)
    if len(cases) != expected_per_class * 3:
        raise ValueError(f"Expected {expected_per_class * 3} cases, got {len(cases)}")
    ids = [case.get("case_id") for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("case_id values must be unique")
    counts = Counter(case.get("ground_truth", {}).get("verdict") for case in cases)
    expected = {"PASS": expected_per_class, "FLAG": expected_per_class, "HUMAN_REVIEW": expected_per_class}
    if counts != Counter(expected):
        raise ValueError(f"Expected balanced verdict counts {expected}, got {dict(counts)}")
    for index, case in enumerate(cases, start=1):
        errors = validate_case(case)
        if errors:
            raise ValueError(f"Case {case.get('case_id', index)}: " + "; ".join(errors))


def case_for_model(case: Dict[str, Any]) -> Dict[str, Any]:
    """Return only review inputs; gold labels and rationales cannot leak to a model."""
    return {
        key: value for key, value in case.items()
        if key not in {"ground_truth", "annotator_notes", "dataset_split"}
    }
