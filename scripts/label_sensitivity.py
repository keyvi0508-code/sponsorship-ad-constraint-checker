"""Compare historical scores with proposed label changes without altering frozen data."""

import json
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
OVERRIDES = {
    "REVIEW-03": "PASS",
    "REVIEW-08": "HUMAN_REVIEW",
    "REVIEW-10": "HUMAN_REVIEW",
    "HOLDOUT-06": "FLAG",
}
SPLITS = [
    (
        "primary",
        "data/primary_cases.jsonl",
        "reports/ai_evaluation_rubric-clarification-2026-09-30-v1.jsonl",
        "reports/baseline_keyword_frozen.json",
    ),
    (
        "extension",
        "data/extension_cases_v2.jsonl",
        "reports/ai_evaluation_extension_v2.jsonl",
        "reports/baseline_keyword_holdout_extension_v2.json",
    ),
]


def read_jsonl(relative_path):
    return [json.loads(line) for line in (PROJECT / relative_path).read_text(encoding="utf-8-sig").splitlines() if line]


def score(labels, predictions):
    ids = set(labels)
    assert ids == set(predictions), (len(ids), len(predictions), ids ^ set(predictions))
    matrix = {
        gold: {pred: sum(labels[cid] == gold and predictions[cid] == pred for cid in ids)
               for pred in ("PASS", "FLAG", "HUMAN_REVIEW")}
        for gold in ("PASS", "FLAG", "HUMAN_REVIEW")
    }
    return {
        "correct": sum(labels[cid] == predictions[cid] for cid in ids),
        "n": len(ids),
        "class_counts": dict(Counter(labels.values())),
        "matrix": matrix,
        "clean_flagged": matrix["PASS"]["FLAG"],
        "clean_escalated": matrix["PASS"]["HUMAN_REVIEW"],
        "violations_passed": matrix["FLAG"]["PASS"],
        "violations_escalated": matrix["FLAG"]["HUMAN_REVIEW"],
        "borderline_escalated": matrix["HUMAN_REVIEW"]["HUMAN_REVIEW"],
    }


for split, cases_file, ai_file, baseline_file in SPLITS:
    cases = read_jsonl(cases_file)
    before = {case["case_id"]: case["ground_truth"]["verdict"] for case in cases}
    after = {cid: OVERRIDES.get(cid, label) for cid, label in before.items()}
    ai = {row["case_id"]: row["verdict"] for row in read_jsonl(ai_file)}
    baseline = json.loads((PROJECT / baseline_file).read_text(encoding="utf-8"))["predictions"]
    print(json.dumps({
        "split": split,
        "changed_cases": {cid: {"before": before[cid], "after": after[cid], "ai": ai[cid], "keyword": baseline[cid]}
                          for cid in before if before[cid] != after[cid]},
        "ai_before": score(before, ai),
        "ai_after": score(after, ai),
        "keyword_before": score(before, baseline),
        "keyword_after": score(after, baseline),
    }, indent=2))

