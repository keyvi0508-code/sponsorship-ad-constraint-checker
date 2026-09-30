"""Freeze a peer-reviewed dataset by recording its SHA-256 and class counts."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Dict

from src.validate_data import load_jsonl, validate_primary_set


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", nargs="?", type=Path, default=Path("data/primary_cases.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("data/frozen_manifest.json"))
    parser.add_argument("--human-review-complete", action="store_true", help="Confirm an independent review has been completed.")
    parser.add_argument("--disagreements-resolved", action="store_true", help="Confirm disagreements have been resolved and labels are frozen.")
    parser.add_argument("--expected-per-class", type=int, default=10, help="Expected cases in each verdict class (10 for 30 cases, 20 for 60).")
    args = parser.parse_args()
    if not args.human_review_complete or not args.disagreements_resolved:
        raise SystemExit("Dataset not frozen. Complete the blind human review and resolve disagreements before using both confirmation flags.")

    cases = load_jsonl(args.cases)
    validate_primary_set(cases, expected_per_class=args.expected_per_class)
    counts = Counter(case["ground_truth"]["verdict"] for case in cases)
    manifest: Dict[str, Any] = {
        "status": "FROZEN",
        "frozen_on": date.today().isoformat(),
        "cases_file": args.cases.as_posix(),
        "sha256": hashlib.sha256(args.cases.read_bytes()).hexdigest(),
        "n_cases": len(cases),
        "class_counts": dict(counts),
        "human_review_completed": True,
        "disagreements_resolved": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
