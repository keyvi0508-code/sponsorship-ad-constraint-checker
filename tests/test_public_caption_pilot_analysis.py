"""Saved real-post analysis must match the locked sources and case outputs."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.analyze_public_caption_pilot import analyze


class PublicCaptionPilotAnalysisTests(unittest.TestCase):
    def test_saved_run_is_descriptive_and_full_status_stays_unknown(self):
        result = analyze()
        self.assertEqual(result["n_posts"], 23)
        self.assertEqual(result["ai_distribution"], {
            "PASS": 5, "FLAG": 0, "HUMAN_REVIEW": 14, "UNKNOWN": 4,
        })
        self.assertEqual(result["disagreements"], 14)
        self.assertEqual(result["full_review_status_distribution"], {"UNKNOWN": 23})
        self.assertFalse(result["accuracy_calculated"])
        self.assertEqual(result["saved_evidence_quotes_outside_caption"], 0)


if __name__ == "__main__":
    unittest.main()
