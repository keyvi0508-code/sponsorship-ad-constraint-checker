"""Verify the exact synthetic evaluation artifacts without regenerating history.

This checks the frozen case bytes, labels, split order and combined-file
derivation. It does not claim to recreate the original human-authored wording.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validate_data import load_jsonl, validate_primary_set


SPLITS = (
    ("development_v2", "primary_cases.jsonl", "frozen_manifest.json"),
    ("holdout_extension_v2", "extension_cases_v2.jsonl", "extension_frozen_manifest_v2.json"),
)


def verify() -> dict:
    split_rows = []
    verified_splits = []
    for name, filename, manifest_filename in SPLITS:
        path = ROOT / "data" / filename
        manifest_path = ROOT / "data" / manifest_filename
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != manifest["sha256"]:
            raise ValueError(f"{filename}: checksum mismatch")
        rows = load_jsonl(path)
        validate_primary_set(rows, expected_per_class=10)
        if len(rows) != manifest["n_cases"]:
            raise ValueError(f"{filename}: case count mismatch")
        counts = dict(Counter(row["ground_truth"]["verdict"] for row in rows))
        if counts != manifest["class_counts"]:
            raise ValueError(f"{filename}: class counts differ from manifest")
        split_rows.extend((name, row) for row in rows)
        verified_splits.append({"split": name, "file": f"data/{filename}", "sha256": digest,
                                "n": len(rows), "class_counts": counts})

    combined_path = ROOT / "data" / "combined_cases_v3_60.jsonl"
    combined_manifest = json.loads((ROOT / "data" / "combined_manifest_v3_60.json").read_text(encoding="utf-8"))
    combined_digest = hashlib.sha256(combined_path.read_bytes()).hexdigest()
    if combined_digest != combined_manifest["sha256"]:
        raise ValueError("Combined file checksum mismatch")
    combined = load_jsonl(combined_path)
    if len(combined) != combined_manifest["n_cases"] or len(combined) != len(split_rows):
        raise ValueError("Combined file count mismatch")
    for index, ((split_name, original), merged) in enumerate(zip(split_rows, combined), start=1):
        if merged.get("dataset_split") != split_name:
            raise ValueError(f"Combined row {index}: split marker mismatch")
        if {key: value for key, value in merged.items() if key != "dataset_split"} != original:
            raise ValueError(f"Combined row {index}: original case content changed")
    combined_counts = dict(Counter(row["ground_truth"]["verdict"] for row in combined))
    if combined_counts != combined_manifest["class_counts"]:
        raise ValueError("Combined file class counts mismatch")
    if len({row["case_id"] for row in combined}) != len(combined):
        raise ValueError("Duplicate case IDs across splits")
    return {
        "status": "EXACT_SAVED_ARTIFACTS_VERIFIED",
        "splits": verified_splits,
        "combined": {"file": "data/combined_cases_v3_60.jsonl", "sha256": combined_digest,
                     "n": len(combined), "class_counts": combined_counts,
                     "matches_ordered_source_splits": True},
        "generation_provenance": "ORIGINAL_WORDING_GENERATOR_NOT_RECORDED",
        "interpretation": "This reproduces the evaluated input files, not the original act of authoring them.",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
