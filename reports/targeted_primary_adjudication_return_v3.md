# Targeted primary-set adjudication return v3

**Return received:** 2026-09-30  
**Reviewer background/provenance:** Not provided  
**Cases:** same five targeted cases as the earlier calibration packets  
**Current frozen primary labels:** unchanged

## Verdict comparison

| Blind case | Primary case | Frozen label | Latest verdict | Review |
|---|---|---|---|---|
| CAL-A | `REVIEW-08` | `PASS` | `PASS` | Correctly treats the personal competitor criticism as not violating CH-CONTEXT-01. However, the reviewer marked product identifiability `unclear` while use is `unknown`, and did not discuss CH-CLAIM-01. Overall disposition remains unresolved under the current project guide. |
| CAL-B | `REVIEW-12` | `HUMAN_REVIEW` | `HUMAN_REVIEW` | Consistent: the script claims first-hand product experience while supplied use is unknown. |
| CAL-C | `REVIEW-02` | `PASS` | `PASS` | Consistent: a brand-level personal preference is not an impartiality claim and no specific product is identified. |
| CAL-D | `REVIEW-10` | `PASS` | `PASS` | Correctly treats the disclosed, subjective competitor criticism as not violating CH-CONTEXT-01. As in CAL-A, the reviewer marked product identifiability `unclear` but did not discuss CH-CLAIM-01 despite unknown use. Overall disposition remains unresolved under the current project guide. |
| CAL-E | `REVIEW-04` | `HUMAN_REVIEW` | `HUMAN_REVIEW` | Consistent: the text asserts a first-hand experience and the input does not confirm use. |

All five latest verdicts match the current frozen labels. Because these are selected boundary cases, the reviewer background was not supplied, and the rationales for CAL-A/CAL-D omit a potentially applicable rule, this is not a verified reliability result and does not by itself resolve the gold-label question.

## Rule-by-rule adjudication

For **CH-CONTEXT-01**, the latest return is consistent with the written rule: CAL-A, CAL-C, and CAL-D do not clearly present their personal competitor opinions as impartial. The earlier `FLAG` decisions for CAL-A/CAL-C/CAL-D should not be accepted on the rationale “negative competitor comment plus CHANEL sponsorship” alone.

For **CH-CLAIM-01**, CAL-A and CAL-D are product/formula opinions with creator use marked `unknown`. The latest reviewer marked the discussed product's identifiability `unclear` and gave no CH-CLAIM rationale. The draft v3 annotation guide says to use `HUMAN_REVIEW` when product identifiability is unclear and that uncertainty determines whether the first-hand-use rule applies. Under that guide, the complete multi-rule verdict for CAL-A and CAL-D is provisionally `HUMAN_REVIEW` under CH-CLAIM-01, while `PASS` under CH-CONTEXT-01. This is a project-level adjudication recommendation, not an official CHANEL determination.

CAL-C remains `PASS`: it is a general preference about a rival brand, not a first-hand opinion about an identifiable product or feature. CAL-B and CAL-E remain `HUMAN_REVIEW` under CH-CLAIM-01.

## Data action

- Do not overwrite `primary_cases.jsonl`, its frozen manifest, or historical scores.
- Keep this return as evidence that CH-CONTEXT-01 is better understood with explicit examples, while CH-CLAIM-01 product-identifiability is still a label boundary.
- Before a v3 gold release, the project owner should decide whether “another luxury house's formula” is an identifiable product/feature for this task. If the v3 draft guide is adopted, CAL-A and CAL-D should be re-labeled `HUMAN_REVIEW` for CH-CLAIM-01, moving the primary set from 10/10/10 to 8 PASS / 10 FLAG / 12 HUMAN_REVIEW. Do not add replacement cases solely to restore class balance without blinded labeling and a new evaluation run.
- Any approved label change requires a separately versioned dataset, new manifest/checksum, and separately recomputed baseline and AI metrics. Report the old and revised result separately because the revised labels were considered after model outputs had been inspected.

## Source

CHANEL, [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), sections 1 and 3. `CH-*` identifiers and the stated mapping are project interpretations, not official CHANEL wording or identifiers.
