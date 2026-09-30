"""Review one script. The default mode validates and estimates without an API call."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from src.ai_reviewer import DEFAULT_MODEL, review_case
from src.evaluate_ai import calculate_cost, estimate_run_upper_bound
from src.validate_data import validate_script_input


def load_script(path: Path) -> Dict[str, Any]:
    try:
        case = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read a valid JSON script from {path}: {exc}") from exc
    errors = validate_script_input(case)
    if errors:
        raise SystemExit("Invalid script input: " + "; ".join(errors))
    return case


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path, help="Path to one label-free JSON script")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-cost-usd", type=float, default=0.10,
                        help="Maximum conservative cost estimate allowed for this one review")
    parser.add_argument("--run-api", action="store_true", help="Make two billable API calls")
    parser.add_argument("--confirm-paid-run", action="store_true",
                        help="Confirm this one-script API review may incur a charge")
    parser.add_argument("--output", type=Path, help="Optional JSON output path; existing files are never overwritten")
    args = parser.parse_args()

    case = load_script(args.script)
    if args.output and args.output.exists():
        raise SystemExit(f"Output already exists; choose a new path before starting: {args.output}")
    if args.max_cost_usd <= 0:
        raise SystemExit("--max-cost-usd must be greater than zero")
    upper_bound = estimate_run_upper_bound([case], args.model)
    if upper_bound is None:
        raise SystemExit(f"No verified price snapshot is available for {args.model}; request blocked.")
    if upper_bound > args.max_cost_usd:
        raise SystemExit(
            f"Request blocked: conservative one-script estimate ${upper_bound:.4f} exceeds "
            f"the configured ${args.max_cost_usd:.2f} limit."
        )

    if not args.run_api:
        print(json.dumps({
            "mode": "dry_run_no_api_calls",
            "case_id": case["case_id"],
            "model": args.model,
            "api_calls_that_would_be_made": 2,
            "conservative_cost_upper_bound_usd": round(upper_bound, 8),
            "next_step": "Only if you approve this charge, rerun with --run-api --confirm-paid-run.",
        }, indent=2, ensure_ascii=False))
        return

    if not args.confirm_paid_run:
        raise SystemExit("Billable review blocked. Add --confirm-paid-run only after approving the charge.")

    result = review_case(case, model=args.model)
    result["estimated_cost_usd"] = calculate_cost(args.model, result["usage"])
    result["conservative_cost_upper_bound_usd"] = round(upper_bound, 8)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        try:
            with args.output.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(rendered)
        except FileExistsError as exc:
            raise SystemExit(f"Output already exists; choose a new path: {args.output}") from exc
    print(rendered, end="")


if __name__ == "__main__":
    main()
