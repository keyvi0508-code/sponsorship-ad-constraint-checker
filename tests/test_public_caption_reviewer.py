"""Safety checks for the real-post caption path and its limited suggestions."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_public_captions import check_prompt_manifest, cost_upper_bound, load_locked_rows
from src.public_caption_reviewer import ai_review, keyword_review


def row(caption: str, capture: str = "complete") -> dict:
    return {
        "id": "REAL-TEST", "source_url": "https://www.instagram.com/reel/example/",
        "accessed_on": "2026-10-02", "caption_capture": capture,
        "caption_text": caption, "full_policy_verdict": "FLAG",
        "discovery_route": "INTERNAL_LABEL_HINT", "creator_handle": "should_not_be_sent",
    }


def response(body: dict) -> dict:
    return {"output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps(body)}]}],
            "usage": {"input_tokens": 12, "output_tokens": 8}}


class PublicCaptionReviewerTests(unittest.TestCase):
    def test_keyword_marker_is_not_full_video_pass(self):
        result = keyword_review(row("#CHANELpartner I love this look"))
        self.assertEqual(result["suggestion"], "PASS")
        self.assertEqual(result["full_review_status"], "UNKNOWN")
        self.assertEqual(result["scope"], "captured_caption_only")

    def test_keyword_weak_or_missing_marker_does_not_accuse(self):
        self.assertEqual(keyword_review(row("#gifted A beautiful look"))["suggestion"], "HUMAN_REVIEW")
        self.assertEqual(keyword_review(row("A beautiful look"))["suggestion"], "UNKNOWN")

    def test_partial_caption_cannot_enter_either_method(self):
        with self.assertRaises(ValueError):
            keyword_review(row("#CHANELpartner", "partial"))
        with self.assertRaises(ValueError):
            ai_review(row("#CHANELpartner", "partial"), api_key="not-real")

    def test_two_stage_api_sees_only_caption_and_never_promotes_to_full_pass(self):
        captured = []
        outputs = [
            response({"signals": [{"type": "disclosure", "quote": "#CHANELpartner"}]}),
            response({"suggestion": "PASS", "findings": [], "uncertainties": ["Video audio and overlay not checked"]}),
        ]

        def fake_post(request_body, api_key):
            self.assertEqual(api_key, "not-real")
            captured.append(request_body)
            return outputs.pop(0)

        with patch("src.public_caption_reviewer._post_response", side_effect=fake_post):
            result = ai_review(row("#CHANELpartner I love this look"), api_key="not-real")
        self.assertEqual(result["suggestion"], "PASS")
        self.assertEqual(result["full_review_status"], "UNKNOWN")
        self.assertEqual(result["usage"]["input_tokens"], 24)
        self.assertEqual(len(captured), 2)
        for request in captured:
            model_input = request["input"]
            self.assertIn("caption_text", model_input)
            for forbidden in ("full_policy_verdict", "discovery_route", "creator_handle", "INTERNAL_LABEL_HINT", "should_not_be_sent"):
                self.assertNotIn(forbidden, model_input)

    def test_hallucinated_quote_rejected(self):
        with patch("src.public_caption_reviewer._post_response", return_value=response({
            "signals": [{"type": "disclosure", "quote": "not in caption"}]
        })):
            with self.assertRaises(ValueError):
                ai_review(row("#CHANELpartner"), api_key="not-real")

    def test_pass_cannot_hide_adverse_finding(self):
        outputs = [
            response({"signals": []}),
            response({"suggestion": "PASS", "findings": [{"rule_id": "CH-DISC-01", "quote": "#gifted", "rationale": "weak marker", "action": "HUMAN_REVIEW"}], "uncertainties": []}),
        ]
        with patch("src.public_caption_reviewer._post_response", side_effect=outputs):
            with self.assertRaises(ValueError):
                ai_review(row("#gifted"), api_key="not-real")

    def test_locked_rows_and_dated_preflight(self):
        rows = load_locked_rows(
            ROOT / "data" / "real_public_reels_caption_development_v1.jsonl",
            ROOT / "data" / "real_public_reels_caption_development_v1_manifest.json",
        )
        self.assertEqual(len(rows), 23)
        self.assertGreater(cost_upper_bound(rows, "openai/gpt-6-sol"), 0)
        self.assertLess(cost_upper_bound(rows, "openai/gpt-6-sol"), 1.5)
        check_prompt_manifest(ROOT / "data" / "public_caption_prompt_manifest_v1.json")


if __name__ == "__main__":
    unittest.main()
