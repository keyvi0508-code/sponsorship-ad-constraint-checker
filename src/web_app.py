"""Local-only review workbench. No API call is made on page load or baseline use."""
from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from statistics import median
from typing import Any, Dict
from urllib.parse import urlparse

from src.ai_reviewer import DEFAULT_MODEL, review_case
from src.baseline import review_with_keyword_baseline
from src.evaluate_ai import calculate_cost, estimate_run_upper_bound
from src.validate_data import load_jsonl, validate_script_input

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
CASE_PATH = ROOT / "data" / "extension_cases_v2.jsonl"
AI_RESULTS_PATH = ROOT / "reports" / "ai_evaluation_extension_v2.jsonl"
AI_SUMMARY_PATH = ROOT / "reports" / "ai_evaluation_extension_v2_summary.json"
SINGLE_REVIEW_COST_CEILING_USD = 0.10
MAX_BODY_BYTES = 32_000


def sample_payload() -> Dict[str, Any]:
    cases = load_jsonl(CASE_PATH)
    labeled_case = next(case for case in cases if case["case_id"] == "HOLDOUT-03")
    reference_verdict = labeled_case["ground_truth"]["verdict"]
    case = {key: value for key, value in labeled_case.items() if key not in {"ground_truth", "annotator_notes", "dataset_split"}}
    baseline = review_with_keyword_baseline(case)
    ai_results = [json.loads(line) for line in AI_RESULTS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    ai_result = next(result for result in ai_results if result.get("case_id") == case["case_id"])
    summary = json.loads(AI_SUMMARY_PATH.read_text(encoding="utf-8"))
    return {
        "case": case,
        "baseline": baseline,
        "ai": ai_result,
        "reference_verdict": reference_verdict,
        "metrics": {
            "ai_accuracy": summary["metrics"]["accuracy"],
            "baseline_accuracy": 20 / 30,
            "ai_human_review": 7,
            "cases": summary["n_cases"],
            "estimated_cost_per_case_usd": summary["estimated_cost_per_case_usd"],
            "median_ai_latency_seconds": round(median(result["latency_seconds"] for result in ai_results), 2),
        },
        "mode": "saved_demo_no_api_call",
    }


def validate_request_case(case: Any) -> Dict[str, Any]:
    errors = validate_script_input(case)
    if errors:
        raise ValueError("; ".join(errors))
    return case


class ReviewHandler(SimpleHTTPRequestHandler):
    """Serve static assets and local JSON endpoints without logging script text."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        # Request logs omit user-supplied content; keep local demo output quiet.
        return

    def _json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> Any:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid request size") from exc
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ValueError(f"Request must be between 1 and {MAX_BODY_BYTES} bytes")
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Request body must be valid UTF-8 JSON") from exc

    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/sample":
            try:
                self._json(sample_payload())
            except Exception as exc:
                self._json({"error": f"Could not load saved demo data: {type(exc).__name__}"}, 500)
            return
        if route.startswith("/api/"):
            self._json({"error": "Not found"}, 404)
            return
        if route == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        try:
            payload = self._read_json()
            case = validate_request_case(payload.get("case") if isinstance(payload, dict) else None)
            if route == "/api/baseline":
                self._json({"baseline": review_with_keyword_baseline(case)})
                return
            if route == "/api/preflight":
                upper_bound = estimate_run_upper_bound([case], DEFAULT_MODEL)
                if upper_bound is None or upper_bound > SINGLE_REVIEW_COST_CEILING_USD:
                    self._json({"error": "The request exceeds the configured one-review cost ceiling."}, 402)
                    return
                self._json({
                    "model": DEFAULT_MODEL,
                    "api_calls": 2,
                    "conservative_cost_upper_bound_usd": round(upper_bound, 8),
                    "ceiling_usd": SINGLE_REVIEW_COST_CEILING_USD,
                })
                return
            if route == "/api/review":
                if payload.get("confirm_paid_run") is not True:
                    self._json({"error": "Paid review requires explicit confirmation."}, 403)
                    return
                upper_bound = estimate_run_upper_bound([case], DEFAULT_MODEL)
                if upper_bound is None or upper_bound > SINGLE_REVIEW_COST_CEILING_USD:
                    self._json({"error": "The request exceeds the configured one-review cost ceiling."}, 402)
                    return
                result = review_case(case, model=DEFAULT_MODEL)
                result["estimated_cost_usd"] = calculate_cost(DEFAULT_MODEL, result["usage"])
                result["conservative_cost_upper_bound_usd"] = round(upper_bound, 8)
                self._json({"ai": result})
                return
            self._json({"error": "Not found"}, 404)
        except ValueError as exc:
            self._json({"error": str(exc)}, 400)
        except Exception as exc:
            self._json({"error": f"Review failed: {type(exc).__name__}. Check the local server output."}, 502)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), ReviewHandler)
    print("Local review workbench: http://127.0.0.1:8765")
    print("This local demo does not save scripts. API reviews require a separate confirmation.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWorkbench stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
