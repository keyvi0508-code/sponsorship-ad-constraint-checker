"""Build a separate, reproducible synthetic fixture for future review tests.

Each scenario declares its intended verdict and rule before the wording template.
This script did not produce the historical 60 scored cases. The generated labels
are construction targets, not independently adjudicated reference answers.
There is no RNG: scenario order and the two product variants define every byte.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.validate_data import validate_primary_set

OUTPUT = ROOT / "data" / "prospective_synthetic_fixture_v1.jsonl"
MANIFEST = ROOT / "data" / "prospective_synthetic_fixture_v1_manifest.json"
PRODUCTS = (("lipstick", "shade"), ("foundation", "formula"))

# The matrix is the generator specification. Verdicts/rules precede text fields.
# Every scenario is rendered once with each of the two product variants.
SCENARIOS = (
    ("PASS", (), "upfront_connection", "#ad · Paid partnership with CHANEL. I tried this {product} this week.",
     "This video is sponsored by CHANEL. I like how this {product} feels on me.", "#ad · CHANEL", True,
     "Clear connection in all endorsement surfaces; first-hand opinion with known use."),
    ("PASS", (), "screen_disclosure", "#ad · A look at a CHANEL {product}.",
     "Here is the {product} in daylight.", "Paid partnership with CHANEL", None,
     "Upfront caption and visible disclosure; no personal product-performance claim."),
    ("PASS", (), "neutral_rival", "#sponsored · CHANEL {product} alongside another brand's {product}.",
     "Sponsored by CHANEL. These are two products on my desk.", "#ad · CHANEL", None,
     "A rival is mentioned neutrally; sponsorship is clear in the scripted surfaces."),
    ("PASS", (), "known_personal_preference", "Paid partnership with CHANEL. This {product} is my preferred look today.",
     "Sponsored by CHANEL. I have used this {product} and prefer it for today's look.", "#ad · CHANEL", True,
     "Preference is subjective, use is known, and the connection is disclosed."),
    ("PASS", (), "plain_description", "#ad · A CHANEL {product} close-up in morning light.",
     "This video is sponsored by CHANEL. Here is the packaging.", "#ad · CHANEL", None,
     "Descriptive copy with clear disclosure and no unsupported claim."),
    ("FLAG", ("CH-DISC-01", "CH-DISC-02"), "weak_marker_only", "#partner · My CHANEL {product} pick.",
     "I recommend this {product}.", "CHANEL {product}", True,
     "Only an insufficient relationship marker appears; spoken and visual endorsement lack clear disclosure."),
    ("FLAG", ("CH-DISC-01",), "missing_sponsor_identity", "#ad · Two beauty houses sent me {product} samples.",
     "I recommend the CHANEL {product}.", "#ad", True,
     "Multiple brands are involved, but the script does not identify CHANEL as the sponsor."),
    ("FLAG", ("CH-DISC-01", "CH-DISC-02"), "no_disclosure", "My favorite CHANEL {product} this month.",
     "I recommend this {product}.", "CHANEL {product}", True,
     "A sponsored endorsement contains no material-connection disclosure in any scripted surface."),
    ("FLAG", ("CH-CLAIM-01",), "known_no_use", "#ad · CHANEL {product}. I tested this personally and love it.",
     "Sponsored by CHANEL. I wore this {product} all week.", "#ad · CHANEL", False,
     "The script asserts first-hand experience although the supplied use fact is false."),
    ("FLAG", ("CH-CONTEXT-01",), "false_impartiality", "#ad · My independent, unbiased comparison: the rival {product} is worse.",
     "Sponsored by CHANEL. This is my neutral verdict on the rival {product}.", "#ad · CHANEL", True,
     "Competitor criticism is presented as impartial despite the disclosed sponsor connection."),
    ("HUMAN_REVIEW", ("CH-CLAIM-01",), "unknown_use", "#ad · CHANEL {product}. I love how this feels on me.",
     "Sponsored by CHANEL. This {product} feels comfortable to me.", "#ad · CHANEL", None,
     "First-hand product opinion is present, but actual use has not been established."),
    ("HUMAN_REVIEW", ("CH-CLAIM-01",), "unverified_claim", "#ad · This CHANEL {product} lasts 24 hours.",
     "Sponsored by CHANEL. It lasts 24 hours.", "#ad · CHANEL", None,
     "A factual duration claim needs support; no reference source is supplied."),
    ("HUMAN_REVIEW", ("CH-CONTEXT-01",), "ambiguous_comparison", "#ad · My own test: the rival {product} feels less suited to me.",
     "Sponsored by CHANEL. That is my personal impression.", "#ad · CHANEL", True,
     "The comparison is subjective but 'my own test' could imply independent evidence; impartiality is uncertain."),
    ("HUMAN_REVIEW", ("CH-DISC-02",), "placement_uncertain", "I reach for this CHANEL {product} most mornings.\n#CHANELpartner",
     "Sponsored by CHANEL. I reach for this {product} often.", "#ad · CHANEL", True,
     "Caption endorsement precedes the marker; actual prominence and fold require human review."),
    ("HUMAN_REVIEW", ("CH-CLAIM-01",), "ambiguous_opinion", "#ad · This CHANEL {product} looks like a dream on skin.",
     "Sponsored by CHANEL. It looks lovely.", "#ad · CHANEL", None,
     "It is unclear whether the wording is an observed first-hand effect or a visual description."),
)


def build_cases() -> list[dict]:
    """Render the predeclared target matrix into 30 labelled script fixtures."""
    rows = []
    counters = Counter()
    for verdict, rules, family, caption, spoken, screen, used, rationale in SCENARIOS:
        for product, part in PRODUCTS:
            counters[verdict] += 1
            values = {"product": product, "part": part}
            rows.append({
                "case_id": f"PROSP-{verdict[:2]}-{counters[verdict]:02d}",
                "scenario_family": family,
                "language": "en", "format": "short_video",
                "multiple_brands": family in {"neutral_rival", "missing_sponsor_identity", "false_impartiality", "ambiguous_comparison"},
                "caption": caption.format(**values).split("\n"),
                "scenes": [{
                    "verbal_endorsement": True,
                    "visual_endorsement": True,
                    "spoken_text": [spoken.format(**values)],
                    "on_screen_text": [screen.format(**values)],
                }],
                "creator_used_product": used,
                "claim_reference_sources": [],
                "ground_truth": {"verdict": verdict, "rule_ids": list(rules), "rationale": rationale},
            })
    validate_primary_set(rows, expected_per_class=10)
    return rows


def artifacts() -> tuple[bytes, bytes]:
    rows = build_cases()
    data = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows).encode("utf-8")
    manifest = {
        "status": "PROSPECTIVE_UNREVIEWED_FIXTURE_NOT_SCORED",
        "source_script": "scripts/generate_prospective_cases.py",
        "source_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "output": "data/prospective_synthetic_fixture_v1.jsonl",
        "output_sha256": hashlib.sha256(data).hexdigest(),
        "n_cases": 30,
        "class_counts": {"PASS": 10, "FLAG": 10, "HUMAN_REVIEW": 10},
        "scenario_families": 15,
        "variants_per_family": 2,
        "randomness": "none",
        "interpretation": "Construction targets await independent annotation; do not pool with the historical 60 scored cases.",
    }
    return data, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Create the new fixture and manifest once")
    mode.add_argument("--check", action="store_true", help="Regenerate in memory and compare exact bytes")
    args = parser.parse_args()
    data, manifest = artifacts()
    if args.write:
        for path in (OUTPUT, MANIFEST):
            if path.exists():
                raise FileExistsError(f"Refusing to replace frozen artifact: {path}")
        OUTPUT.write_bytes(data)
        MANIFEST.write_bytes(manifest)
    else:
        if OUTPUT.read_bytes() != data or MANIFEST.read_bytes() != manifest:
            raise ValueError("Prospective fixture or generator changed; exact reproduction failed")
    print(json.dumps({"status": "CREATED" if args.write else "EXACT_REGENERATION_VERIFIED",
                      "n_cases": 30, "sha256": hashlib.sha256(data).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
