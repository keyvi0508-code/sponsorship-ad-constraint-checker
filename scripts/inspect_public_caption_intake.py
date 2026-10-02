"""Print public-caption intake readiness; no keyword verdict or API call is made."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.public_caption_intake import inspect_public_caption


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "real_public_reels_pilot_v1.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    results = [inspect_public_caption(row) for row in rows]
    print(json.dumps({
        "status": "INTAKE_ONLY_NO_MODEL_OR_POLICY_VERDICT",
        "posts": len(results),
        "caption_review_status_counts": dict(sorted(Counter(row["caption_review_status"] for row in results).items())),
        "caption_marker_status_counts": dict(sorted(Counter(row["caption_observation"]["marker_status"] for row in results).items())),
        "full_review_status_counts": dict(sorted(Counter(row["full_review_status"] for row in results).items())),
        "results": results,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
