import sys
import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.review_one import main as review_one_main
from src.validate_data import case_for_model, load_jsonl, validate_primary_set, validate_script_input


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

    def test_single_script_input_rejects_gold_labels(self):
        script = {
            "case_id": "T1", "language": "en", "format": "short_video",
            "multiple_brands": False, "caption": ["#ad"], "scenes": [],
            "ground_truth": {"verdict": "PASS"},
        }
        self.assertTrue(any("evaluation-only" in error for error in validate_script_input(script)))

    def test_single_script_dry_run_makes_no_api_call(self):
        input_path = ROOT / "examples" / "review_case.json"
        with patch.object(sys, "argv", ["review_one", str(input_path)]):
            with patch("src.review_one.review_case") as api_review:
                output = StringIO()
                with redirect_stdout(output):
                    review_one_main()
        self.assertEqual(__import__("json").loads(output.getvalue())["mode"], "dry_run_no_api_calls")
        api_review.assert_not_called()

    def test_single_script_requires_paid_run_confirmation(self):
        input_path = ROOT / "examples" / "review_case.json"
        with patch.object(sys, "argv", ["review_one", str(input_path), "--run-api"]):
            with patch("src.review_one.review_case") as api_review:
                with self.assertRaises(SystemExit):
                    review_one_main()
        api_review.assert_not_called()

    def test_single_script_refuses_existing_output_before_api_call(self):
        input_path = ROOT / "examples" / "review_case.json"
        output_path = ROOT / "tests" / "existing_review_output_test.json"
        output_path.write_text("{}", encoding="utf-8")
        try:
            with patch.object(sys, "argv", ["review_one", str(input_path), "--run-api",
                                             "--confirm-paid-run", "--output", str(output_path)]):
                with patch("src.review_one.review_case") as api_review:
                    with self.assertRaises(SystemExit):
                        review_one_main()
            api_review.assert_not_called()
        finally:
            output_path.unlink(missing_ok=True)

    def test_single_script_dry_run_reports_one_case_cost_preflight(self):
        input_path = ROOT / "examples" / "review_case.json"
        with patch.object(sys, "argv", ["review_one", str(input_path)]):
            output = StringIO()
            with redirect_stdout(output):
                review_one_main()
        summary = json.loads(output.getvalue())
        self.assertEqual(summary["api_calls_that_would_be_made"], 2)
        self.assertGreater(summary["conservative_cost_upper_bound_usd"], 0)


if __name__ == "__main__":
    unittest.main()
