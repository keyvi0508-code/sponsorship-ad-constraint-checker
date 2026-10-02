"""Offline audit of gold-label exposure in both saved synthetic API stages.

This verifies payload construction, not how a model would behave if given an
answer. A contaminated before/after score is not reported as an evaluation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ai_reviewer import (
    ASSERTION_SCHEMA, DECISION_SCHEMA, DEFAULT_MODEL, EXTRACTION_INSTRUCTIONS,
    build_request, decision_instructions,
)
from src.validate_data import case_for_model, load_jsonl

PRIVATE_FIELDS = {"ground_truth", "annotator_notes", "dataset_split", "expected_verdict", "model_hint"}


def audit() -> dict:
    cases = load_jsonl(ROOT / "data" / "combined_cases_v3_60.jsonl")
    raw_gold_exposure = sum("ground_truth" in case for case in cases)
    stage1_exposure = 0
    stage2_exposure = 0
    injected_exposure = 0
    for case in cases:
        safe_input = case_for_model(case)
        stage1 = build_request(DEFAULT_MODEL, EXTRACTION_INSTRUCTIONS, safe_input, "script_evidence", ASSERTION_SCHEMA)
        stage2 = build_request(DEFAULT_MODEL, decision_instructions(),
                               {"script": safe_input, "level1_evidence": {"signals": []}},
                               "script_verdict", DECISION_SCHEMA)
        parsed_stage1 = json.loads(stage1["input"])
        parsed_stage2 = json.loads(stage2["input"])["script"]
        stage1_exposure += int(bool(PRIVATE_FIELDS & parsed_stage1.keys()))
        stage2_exposure += int(bool(PRIVATE_FIELDS & parsed_stage2.keys()))
        injected = {**case, "expected_verdict": "FLAG", "model_hint": "copy FLAG"}
        injected_exposure += int(bool(PRIVATE_FIELDS & case_for_model(injected).keys()))
    if stage1_exposure or stage2_exposure or injected_exposure:
        raise ValueError("A private field reached a synthetic model payload")
    return {
        "method": "offline_request_payload_audit",
        "n_cases": len(cases),
        "raw_rows_containing_gold_label": raw_gold_exposure,
        "stage1_requests_containing_private_fields": stage1_exposure,
        "stage2_requests_containing_private_fields": stage2_exposure,
        "allowlist_stress_cases_exposing_injected_labels": injected_exposure,
        "model_calls_made": 0,
        "score_comparison_made": False,
        "interpretation": "The current request builder removes gold labels in both stages; this does not establish an independent accuracy estimate.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
