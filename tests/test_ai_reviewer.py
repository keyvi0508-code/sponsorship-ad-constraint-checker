import json
import unittest
import urllib.error
from io import BytesIO
from unittest.mock import patch

from src.ai_reviewer import review_case


class AiReviewerTests(unittest.TestCase):
    def test_default_model_cost_uses_standard_rates(self):
        from src.evaluate_ai import calculate_cost
        self.assertEqual(calculate_cost("openai/gpt-6-sol", {"input_tokens": 1_000_000, "output_tokens": 1_000_000}), 12.0)

    def test_openrouter_endpoint_and_structured_output_routing(self):
        from src.ai_reviewer import API_URL, DEFAULT_MODEL, build_request, ASSERTION_SCHEMA
        request = build_request(DEFAULT_MODEL, "instructions", {"caption": []}, "evidence", ASSERTION_SCHEMA)
        self.assertEqual(API_URL, "https://openrouter.ai/api/v1/responses")
        self.assertEqual(DEFAULT_MODEL, "openai/gpt-6-sol")
        self.assertTrue(request["provider"]["require_parameters"])

    def test_rubric_prompt_separates_context_and_product_use(self):
        from src.ai_reviewer import decision_instructions, PROMPT_VERSION
        instructions = decision_instructions()
        self.assertIn("broad brand-level preference", instructions)
        self.assertIn("if use is unknown, use HUMAN_REVIEW", instructions)
        self.assertIn("Evaluate both rules independently", instructions)
        self.assertEqual(PROMPT_VERSION, "rubric-clarification-2026-09-30-v1")

    def test_two_stage_calls_never_receive_gold_labels(self):
        case = {
            "case_id": "TEST-01",
            "language": "en",
            "format": "short_video",
            "multiple_brands": False,
            "caption": ["#ad"],
            "scenes": [],
            "ground_truth": {"verdict": "PASS", "rule_ids": [], "rationale": "private gold label"},
        }
        extraction = {"output": [{"type": "message", "content": [{
            "type": "output_text", "text": json.dumps({"signals": []})
        }]}], "usage": {"input_tokens": 80, "output_tokens": 10}}
        decision = {"output": [{"type": "message", "content": [{
            "type": "output_text", "text": json.dumps({"verdict": "PASS", "findings": []})
        }]}], "usage": {"input_tokens": 120, "output_tokens": 20}}

        with patch("src.ai_reviewer._post_response", side_effect=[extraction, decision]) as post:
            result = review_case(case, api_key="test-only", model="gpt-6-sol")

        self.assertEqual(post.call_count, 2)
        for call in post.call_args_list:
            request_body = call.args[0]
            self.assertNotIn("ground_truth", request_body["input"])
            self.assertNotIn("private gold label", request_body["input"])
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["usage"]["input_tokens"], 200)
        self.assertEqual(result["usage"]["output_tokens"], 30)

    def test_response_reader_rejects_an_empty_output(self):
        from src.ai_reviewer import _read_output
        with self.assertRaises(ValueError):
            _read_output({"output": []})

    def test_unverifiable_level1_quotes_are_rejected(self):
        from src.ai_reviewer import _validate_assertion_quotes
        case = {"caption": ["#ad"], "scenes": []}
        assertions = {"signals": [{"signal_type": "disclosure_phrase", "quote": "#sponsored", "location": "caption line 1"}]}
        with self.assertRaises(ValueError):
            _validate_assertion_quotes(assertions, case)

    def test_api_error_does_not_persist_masked_key_text(self):
        from src.ai_reviewer import ApiAuthenticationError, _post_response
        body = b'{"error":{"message":"Incorrect API key provided: secret-mask","code":"invalid_api_key"}}'
        error = urllib.error.HTTPError("https://openrouter.ai/api/v1/responses", 401, "Unauthorized", {}, BytesIO(body))
        with patch("src.ai_reviewer.urllib.request.urlopen", side_effect=error):
            with self.assertRaises(ApiAuthenticationError) as raised:
                _post_response({}, "test-only")
        self.assertIn("401", str(raised.exception))
        self.assertIn("invalid_api_key", str(raised.exception))
        self.assertNotIn("secret-mask", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
