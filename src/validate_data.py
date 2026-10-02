"""Load and validate scripts, labelled datasets, and model-safe inputs."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List

ALLOWED_VERDICTS = {"PASS", "FLAG", "HUMAN_REVIEW"}
REQUIRED_TOP_LEVEL = {"case_id", "language", "format", "multiple_brands", "caption", "scenes", "ground_truth"}
REQUIRED_SCRIPT_INPUT = {"case_id", "language", "format", "multiple_brands", "caption", "scenes"}
FORBIDDEN_SCRIPT_INPUT = {"ground_truth", "annotator_notes", "dataset_split"}
MODEL_INPUT_FIELDS = (
    "case_id", "language", "format", "multiple_brands", "caption", "scenes",
    "creator_used_product", "claim_reference_sources",
)


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


def validate_script_input(case: Dict[str, Any]) -> List[str]:
    """Validate one user-submitted script without requiring or accepting gold labels."""
    errors: List[str] = []
    if not isinstance(case, dict):
        return ["script input must be a JSON object"]
    forbidden = FORBIDDEN_SCRIPT_INPUT & set(case)
    if forbidden:
        errors.append("remove evaluation-only fields: " + ", ".join(sorted(forbidden)))
    missing = REQUIRED_SCRIPT_INPUT - set(case)
    if missing:
        errors.append("missing required fields: " + ", ".join(sorted(missing)))
        return errors
    if not isinstance(case["case_id"], str) or not case["case_id"].strip():
        errors.append("case_id must be a non-empty string")
    if case["language"] != "en":
        errors.append("this prototype currently accepts English only (language='en')")
    if case["format"] != "short_video":
        errors.append("format must be short_video")
    if not isinstance(case["multiple_brands"], bool):
        errors.append("multiple_brands must be a boolean")
    if not isinstance(case["caption"], list) or any(not isinstance(line, str) for line in case["caption"]):
        errors.append("caption must be a list of strings, one per line")
    if not isinstance(case["scenes"], list):
        errors.append("scenes must be a list")
    else:
        for index, scene in enumerate(case["scenes"]):
            if not isinstance(scene, dict):
                errors.append(f"scenes[{index}] must be an object")
                continue
            for field in ("verbal_endorsement", "visual_endorsement"):
                if not isinstance(scene.get(field), bool):
                    errors.append(f"scenes[{index}].{field} must be a boolean")
            for field in ("spoken_text", "on_screen_text"):
                value = scene.get(field)
                if not isinstance(value, list) or any(not isinstance(line, str) for line in value):
                    errors.append(f"scenes[{index}].{field} must be a list of strings")
    if "creator_used_product" in case and not isinstance(case["creator_used_product"], (bool, type(None))):
        errors.append("creator_used_product must be true, false, or null")
    if "claim_reference_sources" in case and not isinstance(case["claim_reference_sources"], list):
        errors.append("claim_reference_sources must be a list")
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
    """Allowlist review inputs so present and future label fields stay private."""
    return {key: case[key] for key in MODEL_INPUT_FIELDS if key in case}
