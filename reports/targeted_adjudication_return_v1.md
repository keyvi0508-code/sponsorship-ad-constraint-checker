# Targeted adjudication return v1

Date: 2026-09-30  
Input: user-provided completed `targeted_adjudication_packet_v1.md`  
Reviewer identity/provenance: not supplied. The return is therefore recorded as a targeted reviewer response, not verified as independent classmate review.

## Mapping and adjudication

| Blind ID | Case ID | Frozen v2 label | Reviewer | Revised AI v1 | Keyword baseline | Adjudication recommendation |
|---|---|---|---|---|---|---|
| T-17 | `REVIEW-03` | `HUMAN_REVIEW` (`CH-CONTEXT-01`) | `HUMAN_REVIEW` (`CH-CONTEXT-01`, `CH-CLAIM-01`) | `PASS` | `PASS` | Retain `HUMAN_REVIEW`, primarily under `CH-CONTEXT-01`: “My own test” may imply a more evidence-based comparison, but the implication is unresolved. The wording does not identify a specific product, so `CH-CLAIM-01` is not needed under the project's clarified scope. This remains a revised-AI miss and a baseline miss. |
| T-04 | `REVIEW-08` | `PASS` | `HUMAN_REVIEW` (`CH-CONTEXT-01`, `CH-CLAIM-01`) | `HUMAN_REVIEW` | `PASS` | For a future label version, change to `HUMAN_REVIEW` under `CH-CLAIM-01`: “formula” identifies a product, while actual use is unknown. Do not retain `CH-CONTEXT-01` as a basis: “feels cheap to me” is personal wording and sponsorship plus negative tone alone is insufficient. |
| T-29 | `REVIEW-10` | `PASS` | `HUMAN_REVIEW` (`CH-CONTEXT-01`, `CH-CLAIM-01`) | `HUMAN_REVIEW` | `PASS` | For a future label version, change to `HUMAN_REVIEW` under `CH-CLAIM-01`: the creator compares a specific product formula and actual use is unknown. The personal wording and explicit relationship disclosure do not clearly imply impartiality, so `CH-CONTEXT-01` is not needed for this verdict. |

## Consistency check across the frozen cases

The cases with unknown product-use metadata and a product-opinion issue already route to `HUMAN_REVIEW` in `REVIEW-04` and `REVIEW-12`. `REVIEW-05` is also `HUMAN_REVIEW` for an unsupported objective claim. `REVIEW-02` is a broad personal preference about a rival brand without an identifiable product or factual claim, so its `PASS` remains consistent with the clarified rule scope. The two formula cases (`REVIEW-08` and `REVIEW-10`) are the apparent frozen-label inconsistencies.

If only those two labels changed in a future data version, counts would move from 10 PASS / 10 FLAG / 10 HUMAN_REVIEW to 8 PASS / 10 FLAG / 12 HUMAN_REVIEW. The v2 dataset remains frozen and balanced; no labels or reported scores have been changed by this note. Do not substitute or add cases merely to restore balance without a documented, blinded method.

## Effect on reported AI result

The v1 prompt scored 27/30 (90.0%) against the frozen v2 labels. If a future adjudication changes only `REVIEW-08` and `REVIEW-10` to `HUMAN_REVIEW`, the v1 prompt would match those two additional labels, while `REVIEW-03` would remain incorrect. That counterfactual is not a revised benchmark score; it is only an illustration of why the labeling decision matters. The current 27/30 and Ctrl+F 24/30 figures remain the reported v2 results.

The reviewer and model agreeing on `REVIEW-08` and `REVIEW-10` is useful evidence for reopening the label decision, but not proof by itself. The targeted packet included the project rule interpretation about unknown product use. Record reviewer provenance and project-owner sign-off before producing a new gold dataset. Because the revised prompt was tuned after the initial AI run, use fresh held-out cases for any independent performance claim.
