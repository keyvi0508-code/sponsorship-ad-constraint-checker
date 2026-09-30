import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.validate_data import case_for_model, load_jsonl, validate_primary_set


class ValidationTests(unittest.TestCase):
    def test_model_payload_never_contains_ground_truth(self):
        case = {"case_id": "T1", "caption": ["#ad"], "ground_truth": {"verdict": "PASS"}, "annotator_notes": "private note"}
        payload = case_for_model(case)
        self.assertNotIn("ground_truth", payload)
        self.assertNotIn("annotator_notes", payload)
        self.assertIn("caption", payload)

    def test_model_payload_hides_dataset_split(self):
        case = {"case_id": "T2", "caption": ["#ad"], "dataset_split": "holdout_extension_v2"}
        self.assertNotIn("dataset_split", case_for_model(case))

    def test_combined_60_case_set_is_balanced_and_split_metadata_is_private(self):
        cases = load_jsonl(ROOT / "data" / "combined_cases_v3_60.jsonl")
        validate_primary_set(cases, expected_per_class=20)
        self.assertEqual({case["dataset_split"] for case in cases}, {"development_v2", "holdout_extension_v2"})
        self.assertTrue(all("dataset_split" not in case_for_model(case) for case in cases))

    def test_primary_set_rejects_an_unbalanced_dataset(self):
        cases = [{"case_id": "T1", "ground_truth": {"verdict": "PASS"}}]
        with self.assertRaises(ValueError):
            validate_primary_set(cases)


if __name__ == "__main__":
    unittest.main()
