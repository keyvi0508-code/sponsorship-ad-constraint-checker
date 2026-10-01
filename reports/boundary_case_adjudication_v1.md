# Boundary-case adjudication v1

**Date:** 2026-10-01  
**Basis:** project annotation guide v3, project rulebook, the supplied case facts, and CHANEL's public Social Media Guidelines. Prepared at the user's request after the first blind peer return.  
**Data handling:** this is a separate adjudication record. The original primary/extension labels, manifests, and previously reported evaluation scores remain unchanged. Any later incorporation requires a new dataset version and fresh metric calculation.

## Decisions

Rule-level statuses are `PASS`, `FLAG`, `HUMAN_REVIEW`, or `N/A`. The overall result is `FLAG` if any applicable rule is `FLAG`; otherwise `HUMAN_REVIEW` if any is `HUMAN_REVIEW`; otherwise `PASS`.

| Blind case | Source case | Disclosure rules | Context | Claim/use | Adjudicated overall | Change from current label |
|---|---|---|---|---|---|---|
| CAL-01 | REVIEW-01 | DISC-01 PASS; DISC-02 PASS | CONTEXT HUMAN_REVIEW | CLAIM N/A | HUMAN_REVIEW | Keep |
| CAL-02 | REVIEW-02 | DISC-01 PASS; DISC-02 PASS | CONTEXT PASS | CLAIM N/A | PASS | Keep |
| CAL-03 | REVIEW-03 | DISC-01 PASS; DISC-02 PASS | CONTEXT PASS | CLAIM N/A | PASS | Change from HUMAN_REVIEW |
| CAL-04 | REVIEW-08 | DISC-01 PASS; DISC-02 PASS | CONTEXT PASS | CLAIM HUMAN_REVIEW | HUMAN_REVIEW | Change from PASS |
| CAL-05 | REVIEW-10 | DISC-01 PASS; DISC-02 PASS | CONTEXT PASS | CLAIM HUMAN_REVIEW | HUMAN_REVIEW | Change from PASS |
| CAL-06 | REVIEW-11 | DISC-01 PASS; DISC-02 PASS | CONTEXT HUMAN_REVIEW | CLAIM PASS | HUMAN_REVIEW | Keep |
| CAL-07 | REVIEW-12 | DISC-01 PASS; DISC-02 PASS | CONTEXT N/A | CLAIM HUMAN_REVIEW | HUMAN_REVIEW | Keep |
| CAL-08 | HOLDOUT-06 | DISC-01 PASS; DISC-02 FLAG | CONTEXT N/A | CLAIM HUMAN_REVIEW | FLAG | Change from HUMAN_REVIEW |
| CAL-09 | HOLDOUT-12 | DISC-01 PASS; DISC-02 PASS | CONTEXT HUMAN_REVIEW | CLAIM HUMAN_REVIEW | HUMAN_REVIEW | Keep |
| CAL-10 | HOLDOUT-15 | DISC-01 PASS; DISC-02 PASS | CONTEXT HUMAN_REVIEW | CLAIM PASS | HUMAN_REVIEW | Keep |
| CAL-11 | HOLDOUT-17 | DISC-01 PASS; DISC-02 FLAG | CONTEXT N/A | CLAIM FLAG | FLAG | Overall verdict kept; add DISC-02 |

## Rationale by case

### CAL-01 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** `#ad` is at the start of the caption and the spoken script identifies CHANEL sponsorship. There is no visual endorsement.
- **CH-CONTEXT-01: HUMAN_REVIEW.** “Another luxury house is overpriced for what you get” criticizes a competitor in broad value-judgment language. It does not explicitly claim impartiality, so it is not a clear FLAG; unlike a clearly personal routine or sensory statement, it leaves unresolved whether the judgment is presented as an objective assessment.
- **CH-CLAIM-01: N/A.** No particular product or product feature is identified.

### CAL-02 — PASS

- **CH-DISC-01 / CH-DISC-02: PASS.** The caption and spoken script clearly disclose the CHANEL connection near the endorsement.
- **CH-CONTEXT-01: PASS.** “Worse for my routine” is explicitly framed as the creator's personal preference, with no claim of neutrality or impartiality.
- **CH-CLAIM-01: N/A.** This is a general routine preference; no product or feature is identified.

### CAL-03 — PASS

- **CH-DISC-01 / CH-DISC-02: PASS.** The caption and spoken script disclose sponsorship.
- **CH-CONTEXT-01: PASS.** Although the caption says “My own test,” its conclusion is “feels less suited to me.” Taken together, this is a personal suitability judgment, not a claim that the criticism is independent or impartial. The word “test” alone does not trigger HUMAN_REVIEW.
- **CH-CLAIM-01: N/A.** No identifiable product or feature is named.

### CAL-04 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** `#ad` and “Sponsored by CHANEL” identify the connection in their respective supplied fields.
- **CH-CONTEXT-01: PASS.** “Feels cheap to me” clearly marks a personal impression; the negative tone alone is not an impartiality breach.
- **CH-CLAIM-01: HUMAN_REVIEW.** “Another luxury house's formula” could refer to a product or product feature, but the case does not identify which one. Creator use is `unknown`. The missing product/use context determines whether the first-hand-use rule applies.

### CAL-05 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** The caption states a CHANEL connection and the spoken script explicitly says the video is sponsored by CHANEL.
- **CH-CONTEXT-01: PASS.** “Feels cheaper to me” is a subjective impression; explicitly mentioning the CHANEL connection does not by itself make the criticism impartial.
- **CH-CLAIM-01: HUMAN_REVIEW.** As in CAL-04, “another luxury house's formula” is not specific enough to resolve whether an identifiable product/feature is being reviewed. Use is marked `unknown`.

### CAL-06 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** The caption and spoken script disclose the CHANEL relationship; no visual endorsement is supplied.
- **CH-CONTEXT-01: HUMAN_REVIEW.** “A side-by-side wear test” and a timed, comparative result (“looked patchier by hour six”) can sound like an evidence-based competitor comparison. The wording does not explicitly claim impartiality, so human review is more appropriate than FLAG.
- **CH-CLAIM-01: PASS.** The supplied metadata confirms product use and the statement is framed as the creator's own observed wear-test experience. No separate unsupported general product claim is established by the supplied facts.

### CAL-07 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** The caption and spoken script disclose the CHANEL relationship.
- **CH-CONTEXT-01: N/A.** No competitor criticism appears.
- **CH-CLAIM-01: HUMAN_REVIEW.** The script claims a first-hand experience with “this foundation,” but actual use is `unknown`. The claim in the script is not independent verification that the experience occurred.

### CAL-08 — FLAG

- **CH-DISC-01: PASS.** The caption says `#ad` and identifies CHANEL.
- **CH-DISC-02: FLAG.** The spoken endorsement (“I love how this foundation feels on my skin”) has no spoken sponsorship disclosure. The visible endorsement identifies “CHANEL foundation” but does not disclose the sponsorship on screen. A caption disclosure does not replace disclosures in the spoken and visible video surfaces.
- **CH-CONTEXT-01: N/A.** No competitor criticism appears.
- **CH-CLAIM-01: HUMAN_REVIEW.** The script makes a first-hand opinion about the identified CHANEL foundation, while actual use is `unknown`.
- **Overall:** FLAG takes precedence over the unresolved use question.

### CAL-09 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** `#ad` appears in the caption and the spoken script begins with a CHANEL sponsorship disclosure. No visual endorsement is supplied.
- **CH-CONTEXT-01: HUMAN_REVIEW.** “My own test suggests” identifies a claimed test, but “lasts longer” is a comparative performance conclusion about a competitor. The text does not clearly claim impartiality, yet the evidence-based implication is unresolved.
- **CH-CLAIM-01: HUMAN_REVIEW.** The fragrance-duration conclusion is a factual/comparative product claim with no source supplied, and actual use is `unknown`. The missing test/use evidence prevents PASS; it does not establish that the claim is false.

### CAL-10 — HUMAN_REVIEW

- **CH-DISC-01 / CH-DISC-02: PASS.** The caption identifies `#ad · CHANEL` and the spoken script says “Sponsored by CHANEL.”
- **CH-CONTEXT-01: HUMAN_REVIEW.** “Short wear test” and “the other lipstick transferred more” present a comparative test result. Use is confirmed, but that fact does not resolve whether the competitor criticism is framed as impartial or evidence-based. No explicit impartiality claim is present, so do not FLAG.
- **CH-CLAIM-01: PASS.** The supplied metadata confirms use and the claim is presented as the creator's own wear-test observation; no separate unsupported general claim is established here.

### CAL-11 — FLAG

- **CH-DISC-01: PASS.** `#ad` appears at the start of the caption.
- **CH-DISC-02: FLAG.** The spoken product endorsement contains no spoken CHANEL sponsorship disclosure. No visual endorsement is supplied.
- **CH-CONTEXT-01: N/A.** No competitor criticism appears.
- **CH-CLAIM-01: FLAG.** The caption claims “I tried this serum,” while the spoken script says “I have never tried this serum,” and the metadata says `not used`. The first-hand-use conflict is explicit.
- **Overall:** FLAG under both disclosure placement and first-hand-use rules.

## What changes and what remains separate

The adjudicated decisions change CAL-03 from `HUMAN_REVIEW` to `PASS`, CAL-04 and CAL-05 from `PASS` to `HUMAN_REVIEW`, and CAL-08 from `HUMAN_REVIEW` to `FLAG`. CAL-11 keeps its overall `FLAG` but gains `CH-DISC-02`. All other overall labels remain as stored. These decisions explain the appropriate next dataset version; they have **not** been written over the original case files or used to recalculate AI/baseline metrics.

## Source

CHANEL's current [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/) say not to imply impartiality when criticizing competitors, require clear and conspicuous disclosures matched to spoken/visual endorsement surfaces, require real product use for product opinions, and require factual claims to be supportable and verifiable. `CH-*` are project identifiers, not official CHANEL rule IDs. Accessed 2026-10-01.
