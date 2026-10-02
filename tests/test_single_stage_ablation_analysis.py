"""The saved one-stage comparison must stay tied to the frozen evidence."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.analyze_single_stage_ablation import analyze


class SingleStageAblationAnalysisTests(unittest.TestCase):
    def test_one_disagreement_is_a_safe_miss(self):
        result = analyze()
        self.assertEqual(result["n_cases"], 30)
        self.assertEqual(result["single_stage_correct"], 22)
        self.assertEqual(result["two_stage_correct"], 23)
        self.assertEqual(result["single_stage_false_negatives_marked_safe"], 1)
        self.assertEqual(result["two_stage_false_negatives_marked_safe"], 0)
        self.assertEqual([item["case_id"] for item in result["verdict_disagreements"]], ["HOLDOUT-19"])
        self.assertFalse(result["independent_validation"])


if __name__ == "__main__":
    unittest.main()
