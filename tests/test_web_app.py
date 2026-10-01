import json
import sys
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.web_app import ReviewHandler, ThreadingHTTPServer


class WebWorkbenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), ReviewHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = "http://127.0.0.1:{}".format(cls.server.server_address[1])

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)
        cls.server.server_close()

    def post_json(self, route, payload):
        request = Request(
            self.base_url + route,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=2) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def test_saved_demo_omits_gold_label_from_submitted_case(self):
        with urlopen(self.base_url + "/api/sample", timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["case"]["case_id"], "HOLDOUT-03")
        self.assertNotIn("ground_truth", payload["case"])
        self.assertEqual(payload["baseline"]["verdict"], "PASS")
        self.assertEqual(payload["ai"]["verdict"], "HUMAN_REVIEW")
        self.assertEqual(payload["reference_verdict"], "HUMAN_REVIEW")

    def test_workbench_is_served_locally_without_remote_font_dependencies(self):
        with urlopen(self.base_url + "/", timeout=2) as response:
            page = response.read().decode("utf-8")
        self.assertIn("Creator content review", page)
        self.assertIn("/styles.css", page)
        self.assertNotIn("fonts.googleapis.com", page)
        self.assertIn("Policy scope: CHANEL only", page)
        self.assertIn("Do not use it for another sponsor brand", page)
        self.assertIn("not an independent or real-world estimate", page)
        self.assertIn("not independently verified", page)

    def test_findings_link_to_the_source_guideline(self):
        with urlopen(self.base_url + "/app.js", timeout=2) as response:
            app = response.read().decode("utf-8")
        self.assertIn("CHANEL guide §", app)
        self.assertIn("CH-CONTEXT-01", app)
        self.assertIn("https://www.chanel.com/us/makeup/social-media-guidelines/", app)

    def test_ai_preflight_returns_estimate_without_calling_model(self):
        from src.web_app import sample_payload
        case = sample_payload()["case"]
        with patch("src.web_app.review_case") as paid_review:
            status, result = self.post_json("/api/preflight", {"case": case})
        self.assertEqual(status, 200)
        self.assertEqual(result["api_calls"], 2)
        self.assertLessEqual(result["conservative_cost_upper_bound_usd"], result["ceiling_usd"])
        paid_review.assert_not_called()

    def test_free_baseline_endpoint_returns_keyword_verdict(self):
        from src.web_app import sample_payload
        case = sample_payload()["case"]
        status, result = self.post_json("/api/baseline", {"case": case})
        self.assertEqual(status, 200)
        self.assertEqual(result["baseline"]["verdict"], "PASS")

    def test_live_review_endpoint_requires_confirmation_before_call(self):
        from src.web_app import sample_payload
        case = sample_payload()["case"]
        with patch("src.web_app.review_case") as paid_review:
            status, result = self.post_json("/api/review", {"case": case, "confirm_paid_run": False})
        self.assertEqual(status, 403)
        self.assertIn("explicit confirmation", result["error"])
        paid_review.assert_not_called()

    def test_live_review_rejects_gold_labels(self):
        from src.web_app import sample_payload
        case = sample_payload()["case"]
        case["ground_truth"] = {"verdict": "PASS"}
        status, result = self.post_json("/api/baseline", {"case": case})
        self.assertEqual(status, 400)
        self.assertIn("evaluation-only", result["error"])


if __name__ == "__main__":
    unittest.main()
