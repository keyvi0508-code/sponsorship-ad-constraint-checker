"""Check that public-caption intake cannot turn absent evidence into PASS."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.public_caption_intake import inspect_public_caption
from src.validate_data import load_jsonl


class PublicCaptionIntakeTests(unittest.TestCase):
    def base_row(self):
        return {
            "id": "REAL-TEST",
            "source_url": "https://www.instagram.com/reel/example/",
            "accessed_on": "2026-10-02",
        }

    def test_existing_inventory_is_not_semantic_review_input(self):
        rows = load_jsonl(ROOT / "data" / "real_public_reels_pilot_v1.jsonl")
        results = [inspect_public_caption(row) for row in rows]
        self.assertEqual(len(results), 10)
        self.assertTrue(all(row["caption_review_status"] == "NEEDS_CAPTION_CAPTURE" for row in results))
        self.assertTrue(all(row["full_review_status"] == "UNKNOWN" for row in results))
        self.assertTrue(all(row["methods_run"] == [] for row in results))

    def test_locked_caption_set_is_ready_but_not_full_video_labelled(self):
        path = ROOT / "data" / "real_public_reels_caption_development_v1.jsonl"
        manifest = json.loads((ROOT / "data" / "real_public_reels_caption_development_v1_manifest.json").read_text(encoding="utf-8"))
        rows = load_jsonl(path)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), manifest["sha256"])
        self.assertEqual(len(rows), manifest["n_posts"])
        self.assertEqual([row["id"] for row in rows], manifest["selection_order"])
        results = [inspect_public_caption(row) for row in rows]
        self.assertTrue(all(row["caption_review_status"] == "READY_FOR_CAPTION_REVIEW" for row in results))
        self.assertTrue(all(row["full_review_status"] == "UNKNOWN" for row in results))
        self.assertTrue(all(row["full_policy_verdict"] is None for row in rows))

    def test_complete_caption_marker_does_not_become_full_pass(self):
        row = {**self.base_row(), "caption_capture": "complete", "caption_text": "#CHANELpartner\nMy new look."}
        result = inspect_public_caption(row)
        self.assertEqual(result["caption_review_status"], "READY_FOR_CAPTION_REVIEW")
        self.assertEqual(result["caption_observation"]["marker_status"], "ACCEPTABLE_EXAMPLE_OBSERVED")
        self.assertEqual(result["full_review_status"], "UNKNOWN")
        self.assertNotIn("verdict", result)

    def test_partial_caption_without_marker_cannot_confirm_absence(self):
        row = {**self.base_row(), "caption_capture": "partial", "caption_text": "A new look."}
        result = inspect_public_caption(row)
        self.assertEqual(result["caption_observation"]["marker_status"], "UNKNOWN")
        self.assertEqual(result["caption_review_status"], "PARTIAL_CAPTION_ONLY")

    def test_complete_caption_without_marker_is_only_an_observation(self):
        row = {**self.base_row(), "caption_capture": "complete", "caption_text": "A new look."}
        result = inspect_public_caption(row)
        self.assertEqual(result["caption_observation"]["marker_status"], "NO_LISTED_MARKER_IN_CAPTURED_CAPTION")
        self.assertEqual(result["full_review_status"], "UNKNOWN")

    def test_cannot_claim_complete_capture_from_inventory_marker(self):
        row = {**self.base_row(), "caption_capture": "complete", "caption_marker_text": "#CHANELpartner"}
        with self.assertRaises(ValueError):
            inspect_public_caption(row)


if __name__ == "__main__":
    unittest.main()
