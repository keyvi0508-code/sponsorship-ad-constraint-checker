"""Validate and summarize the source-linked public-Reel feasibility pilot.

This is an observability check, not a compliance evaluator. It deliberately
does not turn partial captions into PASS/FLAG ground truth or pool real posts
with the synthetic development cases.
"""

import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


DATA = Path(__file__).resolve().parents[1] / "data" / "real_public_reels_pilot_v1.jsonl"


def main():
    rows = [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = [row["id"] for row in rows]
    urls = [row["source_url"] for row in rows]
    if len(ids) != len(set(ids)) or len(urls) != len(set(urls)):
        raise ValueError("Pilot IDs and source URLs must be unique")
    for row in rows:
        if urlparse(row["source_url"]).hostname != "www.instagram.com":
            raise ValueError(f"Unexpected source domain: {row['id']}")
        if row["full_policy_verdict"] is not None:
            raise ValueError(f"Partial observation must not have a full verdict: {row['id']}")
        if any(row[field] for field in ("video_speech_checked", "video_overlay_checked", "creator_use_verified")):
            raise ValueError(f"Unverified modality or product use marked verified: {row['id']}")
    summary = {
        "pilot_status": "CAPTION_ONLY_FEASIBILITY_NOT_MODEL_EVALUATION",
        "posts": len(rows),
        "unique_creators": len(set(row["creator_handle"] for row in rows)),
        "caption_marker_counts": dict(sorted(Counter(row["caption_marker"] for row in rows).items())),
        "full_policy_verdicts": sum(row["full_policy_verdict"] is not None for row in rows),
        "video_speech_checked": sum(row["video_speech_checked"] for row in rows),
        "video_overlay_checked": sum(row["video_overlay_checked"] for row in rows),
        "creator_use_verified": sum(row["creator_use_verified"] for row in rows),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
