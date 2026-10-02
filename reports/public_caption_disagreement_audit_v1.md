# Audit of the 14 keyword–AI disagreements

This is a qualitative review of the [23 saved real-caption outputs](public_caption_ai_pilot_v1.md). The table records **why the methods differed**, not which suggestion is correct. `PASS` in the keyword column means a listed acceptable disclosure marker was found, not full caption or video compliance. The original post URL and captured caption are in the [locked source file](../data/real_public_reels_caption_development_v1.jsonl); case-level model rationales are in the [AI JSONL](public_caption_ai_v1.jsonl). The [case-level coding sheet](public_caption_disagreement_codes_v1.jsonl) and `python scripts/summarize_public_caption_disagreements.py` make the categories and counts inspectable. No private relationship, finished video, product use, or independent compliance label was verified.

| Case | Keyword → AI | What AI raised | Audit interpretation |
|---|---|---|---|
| `REAL-02` | `PASS` → `HUMAN_REVIEW` | Partnership marker follows endorsement wording. | Useful placement question; actual mobile prominence and video remain unknown. |
| `REAL-05` | `PASS` → `HUMAN_REVIEW` | Partnership marker follows product copy. | Possible placement issue, not an established breach. |
| `REAL-08` | `PASS` → `HUMAN_REVIEW` | Marker position plus “my absolute favorite essentials.” | Checks a product-opinion/use question that literal search cannot; use unverified. |
| `REAL-09` | `PASS` → `HUMAN_REVIEW` | “Ideal scent” as product opinion. | First-hand experience question is plausible, but the caption cannot verify use. |
| `REAL-10` | `PASS` → `HUMAN_REVIEW` | Five-year collaboration claim and “all of my faves.” | The product-use question is plausible; routing collaboration duration to the product-claim rule appears outside that rule’s stated scope. |
| `REAL-11` | `UNKNOWN` → `HUMAN_REVIEW` | Plain “Gifted” wording. | Shows a listed-keyword vocabulary gap. Underlying gift terms are not independently established. |
| `REAL-12` | `HUMAN_REVIEW` → `UNKNOWN` | `#gifted` with relationship unverified. | AI uses missing prerequisite rather than judging disclosure adequacy; keyword simply reacts to the listed weak marker. |
| `REAL-13` | `HUMAN_REVIEW` → `UNKNOWN` | Same prerequisite issue for `#gifted`. | A rule-boundary difference, not a measured error. |
| `REAL-15` | `UNKNOWN` → `HUMAN_REVIEW` | Plain “gifted” wording. | Another literal vocabulary gap; relationship and video context remain unknown. |
| `REAL-16` | `UNKNOWN` → `HUMAN_REVIEW` | “Favorites” as first-hand product opinion. | May warrant use verification if the creator relationship is in scope; it is not a proven false claim. |
| `REAL-17` | `UNKNOWN` → `HUMAN_REVIEW` | Product-description opinion. | No material CHANEL connection is established; applying the sponsored-creator claim rule may over-escalate an organic post. |
| `REAL-20` | `PASS` → `HUMAN_REVIEW` | Late marker and “bestsellers.” | Demonstrates a possible silent failure of marker-only `PASS`; placement and claim support still require verification. |
| `REAL-22` | `UNKNOWN` → `HUMAN_REVIEW` | “asia viral ones” as a factual claim. | Materiality and rule scope are debatable, and no material connection is established. Candidate over-escalation. |
| `REAL-23` | `UNKNOWN` → `HUMAN_REVIEW` | `$72` price statement. | A price can be checked, but may be time- or market-specific; no material connection is established. Candidate over-escalation. |

The six keyword `PASS` → AI `HUMAN_REVIEW` cases show how an acceptable hashtag can coexist with other unresolved questions. The six keyword `UNKNOWN` → AI `HUMAN_REVIEW` cases show both semantic coverage and potential reviewer burden. The two `HUMAN_REVIEW` → `UNKNOWN` cases show that the methods apply uncertainty differently. None of these patterns yields a false-positive or false-negative count without independently adjudicated reference labels.

Across these 14 disagreements, the saved AI findings cite a placement question in **4** cases (`REAL-02/05/08/20`) and a product-opinion or product-claim question in **8** (`REAL-08/09/10/16/17/20/22/23`). Plain `gifted` wording appears in **2** literal-marker gaps (`REAL-11/15`); the opposite `#gifted` prerequisite difference appears in **2** (`REAL-12/13`). AI escalated **3** captions whose source file does not establish a material CHANEL connection (`REAL-17/22/23`). The analyst marked **4** possible rule-scope overreaches (`REAL-10/17/22/23`). Categories overlap and the latter category is an interpretation, not a verified error. The coding script cross-checks the observable tags against the saved findings and source metadata; it cannot validate the policy interpretation without independent reviewers.
