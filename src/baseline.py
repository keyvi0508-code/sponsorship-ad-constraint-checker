"""Rule-based keyword baseline and Level 1 assertion extraction."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = json.loads((ROOT / "data" / "rulebook.json").read_text(encoding="utf-8-sig"))

ACCEPTABLE = [re.compile(re.escape(x), re.IGNORECASE) for x in RULEBOOK["rules"][0]["acceptable_disclosure_patterns"]]
INSUFFICIENT = [re.compile(re.escape(x), re.IGNORECASE) for x in RULEBOOK["rules"][0]["insufficient_disclosure_patterns"]]
BRAND_SPECIFIC = [re.compile(x, re.IGNORECASE) for x in (r"#chanelpartner", r"#giftfromchanel", r"sponsored\s+by\s+chanel", r"paid\s+partnership\s+with\s+chanel")]
COMPETITOR_CUES = re.compile(r"\b(competitor|rival brand|another luxury house|other luxury brand)\b", re.IGNORECASE)
CRITICISM_CUES = re.compile(r"\b(overpriced|poor quality|inferior|worse|cheaply made|not as good)\b", re.IGNORECASE)
IMPARTIALITY_CUES = re.compile(r"\b(unbiased|independent review|completely objective|no connection to any brand|impartial)\b", re.IGNORECASE)


def _script_texts(case: Dict[str, Any]) -> Iterable[Tuple[str, str]]:
    for index, line in enumerate(case.get("caption", [])):
        yield f"caption[{index}]", str(line)
    for scene_index, scene in enumerate(case.get("scenes", [])):
        for field in ("spoken_text", "on_screen_text"):
            for text_index, text in enumerate(scene.get(field, [])):
                yield f"scenes[{scene_index}].{field}[{text_index}]", str(text)


def _matches(patterns: List[re.Pattern[str]], text: str) -> List[str]:
    return [match.group(0) for pattern in patterns for match in pattern.finditer(text)]


def extract_level1_assertions(case: Dict[str, Any]) -> Dict[str, Any]:
    """Extract literal evidence only; do not make the policy decision here."""
    texts = list(_script_texts(case))
    disclosure_mentions: List[Dict[str, str]] = []
    for location, text in texts:
        for match in _matches(ACCEPTABLE + INSUFFICIENT, text):
            disclosure_mentions.append({"text": match, "location": location})

    caption = [str(x) for x in case.get("caption", [])]
    early_caption_text = "\n".join(caption[:2])
    scenes = case.get("scenes", [])
    first_endorsement_index = next(
        (i for i, scene in enumerate(scenes) if scene.get("verbal_endorsement") or scene.get("visual_endorsement")),
        None,
    )
    first_scene = scenes[first_endorsement_index] if first_endorsement_index is not None else {}
    spoken = "\n".join(str(x) for x in first_scene.get("spoken_text", []))
    on_screen = "\n".join(str(x) for x in first_scene.get("on_screen_text", []))
    all_text = "\n".join(text for _, text in texts)

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
    }


def review_with_keyword_baseline(case: Dict[str, Any]) -> Dict[str, Any]:
    """Level 2 rule decisions from Level 1 literal assertions."""
    assertions = extract_level1_assertions(case)
    issues: List[Dict[str, str]] = []
    all_text = "\n".join(text for _, text in _script_texts(case))
    has_acceptable = bool(_matches(ACCEPTABLE, all_text))
    has_insufficient = bool(_matches(INSUFFICIENT, all_text))
    multiple_brands = bool(case.get("multiple_brands"))

    if not has_acceptable or (multiple_brands and not assertions["brand_specific_disclosure_anywhere"]):
        evidence = _matches(INSUFFICIENT, all_text)
        issues.append({
            "rule_id": "CH-DISC-01",
            "evidence": evidence[0] if evidence else "No clear disclosure phrase found",
            "rationale": "Keyword baseline did not find a sufficient disclosure for the sponsorship context.",
        })
    elif has_insufficient and not has_acceptable:
        issues.append({
            "rule_id": "CH-DISC-01",
            "evidence": _matches(INSUFFICIENT, all_text)[0],
            "rationale": "The only disclosure-like wording matches an example the guide identifies as insufficient.",
        })

    if has_acceptable and not assertions["acceptable_disclosure_in_first_two_caption_lines"]:
        issues.append({
            "rule_id": "CH-DISC-02",
            "evidence": "Disclosure not found in the first two caption lines",
            "rationale": "The baseline checks caption placement literally and did not find an acceptable disclosure above the fold.",
        })

    scene_index = assertions["first_endorsement_scene_index"]
    if scene_index is not None:
        scene = case["scenes"][scene_index]
        if scene.get("verbal_endorsement") and not assertions["spoken_disclosure_in_first_endorsement_scene"]:
            issues.append({
                "rule_id": "CH-DISC-02",
                "evidence": "Spoken disclosure not found in the first endorsement scene",
                "rationale": "The baseline checks for a literal disclosure phrase in the spoken script.",
            })
        if scene.get("visual_endorsement") and not assertions["on_screen_disclosure_in_first_endorsement_scene"]:
            issues.append({
                "rule_id": "CH-DISC-02",
                "evidence": "On-screen disclosure not found in the first endorsement scene",
                "rationale": "The baseline checks for a literal disclosure phrase in planned on-screen text.",
            })

    if assertions["competitor_cues"] and assertions["criticism_cues"] and assertions["impartiality_cues"]:
        issues.append({
            "rule_id": "CH-CONTEXT-01",
            "evidence": "; ".join(assertions["competitor_cues"] + assertions["criticism_cues"] + assertions["impartiality_cues"]),
            "rationale": "The keyword baseline found competitor criticism alongside language claiming impartiality.",
        })

    return {
        "case_id": case["case_id"],
        "verdict": "FLAG" if issues else "PASS",
        "assertions": assertions,
        "findings": issues,
        "method": "keyword_baseline",
    }
