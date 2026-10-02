"""Validate manual disagreement codes against locked caption outputs and print counts.

The codebook records observable method behavior plus a clearly marked analyst
interpretation. Its tags are not independent compliance labels. This script
checks every coded case against the saved keyword/AI runs and source signals;
it never calls an API or calculates accuracy.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEBOOK = ROOT / "reports" / "public_caption_disagreement_codes_v1.jsonl"
TAGS = {
    "PLACEMENT_QUESTION": "AI cites CH-DISC-02 for caption marker position; actual prominence unverified.",
    "PRODUCT_CLAIM_QUESTION": "AI cites CH-CLAIM-01; product use or claim support unverified.",
    "PLAIN_GIFT_WORDING_GAP": "Plain gifted wording appears without the exact #gifted token the literal screen recognizes.",
    "RELATIONSHIP_PREREQUISITE_DIFFERENCE": "Keyword asks for review on #gifted while AI withholds judgement pending relationship facts.",
    "NO_ESTABLISHED_CONNECTION_ESCALATION": "AI escalates although the source file marks the relationship signal NOT_ESTABLISHED.",
    "POSSIBLE_RULE_SCOPE_OVERREACH": "Analyst flags a debatable application of the project rule; not a measured error.",
}


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def summarize() -> dict:
    source = {row["id"]: row for row in read_jsonl(ROOT / "data" / "real_public_reels_caption_development_v1.jsonl")}
    keyword = {row["id"]: row for row in read_jsonl(ROOT / "reports" / "public_caption_keyword_v1.jsonl")}
    ai = {row["id"]: row for row in read_jsonl(ROOT / "reports" / "public_caption_ai_v1.jsonl")}
    codes = read_jsonl(CODEBOOK)
    if set(source) != set(keyword) or set(source) != set(ai) or len(source) != 23:
        raise ValueError("Source and saved run IDs do not match the 23-post pilot")
    disagreement_ids = {id_ for id_ in source if keyword[id_]["suggestion"] != ai[id_]["suggestion"]}
    if len(disagreement_ids) != 14 or {row["id"] for row in codes} != disagreement_ids or len(codes) != 14:
        raise ValueError("The codebook must contain each saved disagreement exactly once")
    directions, tag_cases = Counter(), defaultdict(list)
    for row in codes:
        id_ = row["id"]
        direction = keyword[id_]["suggestion"] + " -> " + ai[id_]["suggestion"]
        directions[direction] += 1
        tags = row["tags"]
        if not tags or len(tags) != len(set(tags)) or any(tag not in TAGS for tag in tags):
            raise ValueError(f"{id_}: invalid or duplicate tag")
        if not row.get("audit_note", "").strip():
            raise ValueError(f"{id_}: missing audit note")
        rule_ids = {finding["rule_id"] for finding in ai[id_].get("findings", [])}
        if "PLACEMENT_QUESTION" in tags and "CH-DISC-02" not in rule_ids:
            raise ValueError(f"{id_}: placement tag lacks model finding")
        if "PRODUCT_CLAIM_QUESTION" in tags and "CH-CLAIM-01" not in rule_ids:
            raise ValueError(f"{id_}: product claim tag lacks model finding")
        if "PLAIN_GIFT_WORDING_GAP" in tags:
            caption = source[id_]["caption_text"].lower()
            if "gifted" not in caption or "#gifted" in caption or keyword[id_]["suggestion"] != "UNKNOWN":
                raise ValueError(f"{id_}: plain gift wording tag lacks source support")
        if "RELATIONSHIP_PREREQUISITE_DIFFERENCE" in tags:
            if direction != "HUMAN_REVIEW -> UNKNOWN" or "#gifted" not in source[id_]["caption_text"].lower():
                raise ValueError(f"{id_}: prerequisite tag lacks source support")
        if "NO_ESTABLISHED_CONNECTION_ESCALATION" in tags:
            if source[id_]["relationship_signal"] != "NOT_ESTABLISHED" or ai[id_]["suggestion"] != "HUMAN_REVIEW":
                raise ValueError(f"{id_}: connection tag lacks source support")
        for tag in tags:
            tag_cases[tag].append(id_)
    return {
        "status": "SAVED_OUTPUTS_AND_MANUAL_CODES_VALIDATED",
        "n_posts": len(source), "n_disagreements": len(disagreement_ids),
        "direction_counts": dict(sorted(directions.items())),
        "tag_counts": {tag: {"n": len(tag_cases[tag]), "case_ids": tag_cases[tag], "definition": definition}
                       for tag, definition in TAGS.items()},
        "coding_note": "Tags may overlap. They explain observed method behavior or analyst concerns, not actual compliance or model accuracy.",
    }


if __name__ == "__main__":
    print(json.dumps(summarize(), ensure_ascii=False, indent=2))
