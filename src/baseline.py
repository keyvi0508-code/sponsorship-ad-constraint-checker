"""Rule-based keyword baseline and Level 1 assertion extraction."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Pattern, Tuple

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = json.loads((ROOT / "data" / "rulebook.json").read_text(encoding="utf-8-sig"))
RULES = {rule["id"]: rule for rule in RULEBOOK["rules"]}


def _literal_pattern(value: str) -> Pattern[str]:
    if value.startswith("#"):
        return re.compile(r"(?<![\w])" + re.escape(value) + r"(?![\w])", re.IGNORECASE)
    escaped = re.escape(value).replace(r"\ ", r"\s+")
    return re.compile(r"(?<!\w)" + escaped + r"(?!\w)", re.IGNORECASE)


ACCEPTABLE = [_literal_pattern(x) for x in RULES["CH-DISC-01"]["acceptable_disclosure_patterns"]]
INSUFFICIENT = [_literal_pattern(x) for x in RULES["CH-DISC-01"]["insufficient_disclosure_patterns"]]
BRAND_SPECIFIC = [_literal_pattern(x) for x in ("#chanelpartner", "#giftfromchanel", "sponsored by chanel", "paid partnership with chanel")]
COMPETITOR_CUES = re.compile(r"\b(competitor|rival brand|another luxury house|other luxury brand)\b", re.IGNORECASE)
CRITICISM_CUES = re.compile(r"\b(overpriced|poor quality|inferior|worse|cheaply made|not as good)\b", re.IGNORECASE)
IMPARTIALITY_CUES = re.compile(r"\b(unbiased|independent review|completely objective|no connection to any brand|impartial)\b", re.IGNORECASE)


def _script_texts(case: Dict[str, Any]) -> Iterable[Tuple[str, str]]:
    caption = case.get("caption", [])
    if isinstance(caption, str):
        caption = caption.splitlines()
    for index, line in enumerate(caption):
        yield f"caption[{index}]", str(line)
    for scene_index, scene in enumerate(case.get("scenes", [])):
        for field in ("spoken_text", "on_screen_text"):
            values = scene.get(field, [])
            if isinstance(values, str):
                values = [values]
            for text_index, text in enumerate(values):
                yield f"scenes[{scene_index}].{field}[{text_index}]", str(text)


def _matches(patterns: List[Pattern[str]], text: str) -> List[str]:
    return [match.group(0) for pattern in patterns for match in pattern.finditer(text)]


def _has_cue(cues: List[str], text: str) -> List[str]:
    return _matches([_literal_pattern(cue) for cue in cues], text)


def extract_level1_assertions(case: Dict[str, Any]) -> Dict[str, Any]:
    """Extract literal evidence only; do not make the policy decision here."""
    texts = list(_script_texts(case))
    disclosure_mentions: List[Dict[str, str]] = []
    for location, text in texts:
        for pattern_type, patterns in (("acceptable_example", ACCEPTABLE), ("insufficient_example", INSUFFICIENT)):
            for match in _matches(patterns, text):
                disclosure_mentions.append({"text": match, "location": location, "pattern_type": pattern_type})

    caption = case.get("caption", [])
    if isinstance(caption, str):
        caption = caption.splitlines()
    early_caption_text = "\n".join(str(x) for x in caption[:2])
    scenes = case.get("scenes", [])
    first_endorsement_index = next(
        (i for i, scene in enumerate(scenes) if scene.get("verbal_endorsement") or scene.get("visual_endorsement")),
        None,
    )
    first_scene = scenes[first_endorsement_index] if first_endorsement_index is not None else {}
    spoken = "\n".join(str(x) for x in first_scene.get("spoken_text", []))
    on_screen = "\n".join(str(x) for x in first_scene.get("on_screen_text", []))
    all_text = "\n".join(text for _, text in texts)
    claim_rule = RULES["CH-CLAIM-01"]

    return {
        "disclosure_mentions": disclosure_mentions,
        "acceptable_disclosure_in_first_two_caption_lines": bool(_matches(ACCEPTABLE, early_caption_text)),
        "brand_specific_disclosure_anywhere": bool(_matches(BRAND_SPECIFIC, all_text)),
        "first_endorsement_scene_index": first_endorsement_index,
        "spoken_disclosure_in_first_endorsement_scene": bool(_matches(ACCEPTABLE, spoken)),
        "on_screen_disclosure_in_first_endorsement_scene": bool(_matches(ACCEPTABLE, on_screen)),
        "competitor_cues": _matches([COMPETITOR_CUES], all_text),
        "criticism_cues": _matches([CRITICISM_CUES], all_text),
        "impartiality_cues": _matches([IMPARTIALITY_CUES], all_text),
        "experience_claim_cues": _has_cue(claim_rule["experience_cues"], all_text),
        "objective_claim_cues": _has_cue(claim_rule["objective_claim_cues"], all_text),
    }


def review_with_keyword_baseline(case: Dict[str, Any]) -> Dict[str, Any]:
    """Level 2 rule decisions from the literal Level 1 assertions."""
    assertions = extract_level1_assertions(case)
    findings: List[Dict[str, str]] = []
    all_text = "\n".join(text for _, text in _script_texts(case))
    has_acceptable = bool(_matches(ACCEPTABLE, all_text))
    has_insufficient = bool(_matches(INSUFFICIENT, all_text))
    multiple_brands = bool(case.get("multiple_brands"))

    if not has_acceptable or (multiple_brands and not assertions["brand_specific_disclosure_anywhere"]):
        weak = _matches(INSUFFICIENT, all_text)
        findings.append({
            "rule_id": "CH-DISC-01",
            "evidence": weak[0] if weak else "No clear disclosure phrase found",
            "rationale": "The keyword baseline did not find a sufficient disclosure for the sponsorship context.",
        })

    if has_acceptable and not assertions["acceptable_disclosure_in_first_two_caption_lines"]:
        findings.append({
            "rule_id": "CH-DISC-02",
            "evidence": "Disclosure not found in the first two caption lines",
            "rationale": "The baseline did not find an acceptable disclosure above the fold in the caption.",
        })

    scene_index = assertions["first_endorsement_scene_index"]
    if scene_index is not None:
        scene = case["scenes"][scene_index]
        if scene.get("verbal_endorsement") and not assertions["spoken_disclosure_in_first_endorsement_scene"]:
            findings.append({
                "rule_id": "CH-DISC-02",
                "evidence": "Spoken disclosure not found in the first endorsement scene",
                "rationale": "The baseline checks for a literal disclosure phrase in the spoken script.",
            })
        if scene.get("visual_endorsement") and not assertions["on_screen_disclosure_in_first_endorsement_scene"]:
            findings.append({
                "rule_id": "CH-DISC-02",
                "evidence": "On-screen disclosure not found in the first endorsement scene",
                "rationale": "The baseline checks for a literal disclosure phrase in planned on-screen text.",
            })

    if assertions["competitor_cues"] and assertions["criticism_cues"]:
        if assertions["impartiality_cues"]:
            findings.append({
                "rule_id": "CH-CONTEXT-01",
                "evidence": "; ".join(assertions["competitor_cues"] + assertions["criticism_cues"] + assertions["impartiality_cues"]),
                "rationale": "The keyword baseline found competitor criticism alongside language claiming impartiality.",
            })
        else:
            findings.append({
                "rule_id": "CH-CONTEXT-01",
                "evidence": "; ".join(assertions["competitor_cues"] + assertions["criticism_cues"]),
                "rationale": "The keyword baseline cannot tell whether this competitor criticism implies impartiality; a human should review the context.",
                "action": "HUMAN_REVIEW",
            })

    if assertions["experience_claim_cues"]:
        used = case.get("creator_used_product")
        if used is None:
            findings.append({
                "rule_id": "CH-CLAIM-01",
                "evidence": "; ".join(assertions["experience_claim_cues"]),
                "rationale": "The script makes a first-hand opinion claim, but product use is not confirmed in the review inputs.",
                "action": "HUMAN_REVIEW",
            })
        elif used is False:
            findings.append({
                "rule_id": "CH-CLAIM-01",
                "evidence": "; ".join(assertions["experience_claim_cues"]),
                "rationale": "The review inputs say the creator has not used the product but the script claims first-hand experience.",
            })

    if assertions["objective_claim_cues"] and not case.get("claim_reference_sources"):
        findings.append({
            "rule_id": "CH-CLAIM-01",
            "evidence": "; ".join(assertions["objective_claim_cues"]),
            "rationale": "An objective product claim needs an authoritative reference; none was supplied to the reviewer.",
            "action": "HUMAN_REVIEW",
        })

    if any(item.get("action") == "HUMAN_REVIEW" for item in findings):
        verdict = "HUMAN_REVIEW"
    elif findings:
        verdict = "FLAG"
    else:
        verdict = "PASS"

    return {
        "case_id": case["case_id"],
        "verdict": verdict,
        "assertions": assertions,
        "findings": findings,
        "method": "keyword_baseline",
    }
