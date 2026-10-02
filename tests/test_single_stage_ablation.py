"""The optional ablation must be reproducible, label-safe, and no-call by default."""
import json
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluate_single_stage_ablation import check_prompt_lock, cost_upper_bound, load_inputs, main
from src.single_stage_reviewer import review_case_single_stage, single_stage_instructions


class SingleStageAblationTests(unittest.TestCase):
    def test_prompt_lock_and_dated_preflight(self):
        check_prompt_lock()
        cases = load_inputs()
        self.assertEqual(len(cases), 30)
        self.assertGreater(cost_upper_bound(cases), 0)
        self.assertLess(cost_upper_bound(cases), 1.5)
        self.assertNotIn("Use Level 1 signals", single_stage_instructions())

    def test_dry_run_makes_no_api_call(self):
        output = StringIO()
        with patch.object(sys, "argv", ["evaluate_single_stage_ablation"]):
            with patch("scripts.evaluate_single_stage_ablation.review_case_single_stage") as reviewer:
                with redirect_stdout(output):
                    main()
        reviewer.assert_not_called()
        summary = json.loads(output.getvalue())
        self.assertEqual(summary["mode"], "dry_run_no_api_calls")
        self.assertEqual(summary["one_stage_calls_if_run"], 30)

    def test_one_stage_request_excludes_gold_label(self):
        case = {"case_id": "T-01", "caption": ["#ad"],
                "ground_truth": {"verdict": "FLAG", "rationale": "private label"},
                "expected_verdict": "FLAG"}
        fake = {"output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps({
            "verdict": "PASS", "findings": []})}]}],
            "usage": {"input_tokens": 10, "output_tokens": 3}}
        with patch("src.single_stage_reviewer._post_response", return_value=fake) as post:
            result = review_case_single_stage(case, api_key="not-real")
        self.assertEqual(result["verdict"], "PASS")
        payload = post.call_args.args[0]["input"]
        self.assertNotIn("ground_truth", payload)
        self.assertNotIn("private label", payload)
        self.assertNotIn("expected_verdict", payload)


if __name__ == "__main__":
    unittest.main()
