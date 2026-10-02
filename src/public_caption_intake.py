"""Gate partial public-post evidence before any script or model review.

This module reports what a captured caption literally shows. It never turns an
uninspected video into an empty scene or a full-policy PASS/FLAG decision.
"""
from __future__ import annotations

from typing import Any, Dict, List
from urllib.parse import urlparse

from src.baseline import ACCEPTABLE, INSUFFICIENT


CAPTURE_STATES = {"complete", "partial", "not_captured"}


def _matches(text: str, patterns: list) -> List[str]:
    """Return exact marker substrings found in the captured caption."""
    return [match.group(0) for pattern in patterns for match in pattern.finditer(text)]


def inspect_public_caption(row: Dict[str, Any]) -> Dict[str, Any]:
    """Assess intake readiness without calling an API or issuing a policy verdict.

    `caption_text` must be copied from the original post, not reconstructed from
    a summary, search snippet, or the older `caption_marker_text` inventory field.
    """
    if not isinstance(row, dict):
        raise ValueError("public observation must be a JSON object")
    post_id = row.get("id")
    source_url = row.get("source_url")
    accessed_on = row.get("accessed_on")
    if not isinstance(post_id, str) or not post_id.strip():
        raise ValueError("id must be a non-empty string")
    parsed = urlparse(source_url) if isinstance(source_url, str) else None
    if not parsed or parsed.scheme != "https" or parsed.hostname != "www.instagram.com" or not parsed.path.startswith("/reel/"):
        raise ValueError(f"{post_id}: source_url must point to an original Instagram Reel")
    if not isinstance(accessed_on, str) or not accessed_on.strip():
        raise ValueError(f"{post_id}: accessed_on must be recorded")

    capture = row.get("caption_capture", "not_captured")
    if capture not in CAPTURE_STATES:
        raise ValueError(f"{post_id}: caption_capture must be complete, partial, or not_captured")
    caption_text = row.get("caption_text")
    if capture == "not_captured":
        if caption_text is not None:
            raise ValueError(f"{post_id}: caption_text cannot be supplied when not_captured")
        caption_review_status = "NEEDS_CAPTION_CAPTURE"
        marker_status = "UNKNOWN"
        acceptable: List[str] = []
        insufficient: List[str] = []
    else:
        if not isinstance(caption_text, str) or not caption_text.strip():
            raise ValueError(f"{post_id}: {capture} caption capture requires non-empty original caption_text")
        acceptable = _matches(caption_text, ACCEPTABLE)
        insufficient = _matches(caption_text, INSUFFICIENT)
        if acceptable:
            marker_status = "ACCEPTABLE_EXAMPLE_OBSERVED"
        elif insufficient:
            marker_status = "INSUFFICIENT_EXAMPLE_OBSERVED"
        elif capture == "complete":
            marker_status = "NO_LISTED_MARKER_IN_CAPTURED_CAPTION"
        else:
            marker_status = "UNKNOWN"
        caption_review_status = "READY_FOR_CAPTION_REVIEW" if capture == "complete" else "PARTIAL_CAPTION_ONLY"

    return {
        "id": post_id,
        "source_url": source_url,
        "accessed_on": accessed_on,
        "caption_capture": capture,
        "caption_review_status": caption_review_status,
        "caption_observation": {
            "marker_status": marker_status,
            "acceptable_examples_seen": acceptable,
            "insufficient_examples_seen": insufficient,
            "scope": "captured_caption_only",
        },
        "full_review_status": "UNKNOWN",
        "full_review_reason": "Published-video speech, overlays, visibility, product use, and private relationship facts were not established by caption intake.",
        "methods_run": [],
    }
