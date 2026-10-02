"""One-call alternative to the saved two-stage synthetic script reviewer.

It keeps the same model, rule rubric and decision schema, but asks the model to
find its own evidence in one request. Results are exploratory development data.
"""
from __future__ import annotations

import os
import time
from typing import Any, Dict

from src.ai_reviewer import (
    DECISION_SCHEMA, DEFAULT_MODEL, _post_response, _read_output, _usage,
    build_request, decision_instructions,
)
from src.validate_data import case_for_model

PROMPT_VERSION = "single-stage-ablation-2026-10-02-v1"
_TWO_STAGE_SENTENCE = "Use Level 1 signals as evidence pointers, but verify evidence against the original supplied script. "


def single_stage_instructions() -> str:
    original = decision_instructions()
    if original.count(_TWO_STAGE_SENTENCE) != 1:
        raise ValueError("Base rubric changed; review the single-stage prompt before running")
    return original.replace(
        _TWO_STAGE_SENTENCE,
        "Find and verify evidence directly in the original supplied script. ",
    )


def review_case_single_stage(case: Dict[str, Any], api_key: str | None = None, model: str | None = None) -> Dict[str, Any]:
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENROUTER_API_KEY locally; never put it in project files")
    model = model or os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)
    review_input = case_for_model(case)
    started = time.perf_counter()
    response = _post_response(build_request(
        model, single_stage_instructions(), review_input, "single_stage_script_verdict", DECISION_SCHEMA
    ), api_key)
    decision = _read_output(response)
    if decision.get("verdict") not in {"PASS", "FLAG", "HUMAN_REVIEW"} or not isinstance(decision.get("findings"), list):
        raise ValueError("Single-stage reviewer returned an invalid decision")
    return {
        "case_id": case["case_id"], "verdict": decision["verdict"],
        "findings": decision["findings"], "provider": "openrouter",
        "method": "openrouter_responses_single_stage", "prompt_version": PROMPT_VERSION,
        "model": model, "usage": _usage(response),
        "latency_seconds": round(time.perf_counter() - started, 3),
    }
