# Targeted primary-set adjudication return v2

**Return date:** 2026-09-30  
**Reviewer background:** Not provided  
**Cases:** 5 targeted cases from the primary 30-case set  
**Purpose:** inspect the boundary between personal competitor opinion, impartiality claims, and first-hand product-use uncertainty.

## Comparison with frozen labels

| Blind case | Primary case | Frozen label | Reviewer verdict | Initial assessment |
|---|---|---|---|---|
| CAL-A | `REVIEW-08` | `PASS` | `FLAG` | Personal wording (“feels cheap to me”) is treated as an impartiality breach without a quoted claim of neutrality or independence. Keep the frozen label pending adjudication. The reviewer also said no specific product was identifiable, so the first-hand-use rule was not raised. |
| CAL-B | `REVIEW-12` | `HUMAN_REVIEW` | `HUMAN_REVIEW` | Consistent with the supplied unknown-use metadata and explicit first-hand experience wording. |
| CAL-C | `REVIEW-02` | `PASS` | `FLAG` | “Worse for my routine” is expressly framed around the creator's routine. The rationale does not show that the script presents the opinion as impartial. Keep the frozen label pending adjudication. |
| CAL-D | `REVIEW-10` | `PASS` | `FLAG` | The caption discloses a CHANEL connection and frames the opinion as “feels cheaper to me.” No evidence of an impartiality claim is cited. Keep the frozen label pending adjudication. |
| CAL-E | `REVIEW-04` | `HUMAN_REVIEW` | `HUMAN_REVIEW` | Consistent with the first-hand opinion wording and unknown use metadata. The product referent remains underspecified. |

The raw agreement with the existing labels is **2/5**. This is a deliberately selected, small calibration sample, and reviewer background was not provided. It is not an estimate of inter-rater reliability.

## Rule-based assessment

CHANEL's public guide says creators should not represent or imply that they are impartial when criticizing competitors. The project's operational rubric further says negative personal opinion alone is not enough for `FLAG`, and reserves `HUMAN_REVIEW` for genuinely unclear implications. The three `FLAG` rationales rely on sponsorship plus negative sentiment or describe the comment as non-objective; they do not identify wording that claims or implies impartiality. The supplied phrases “feels cheap to me,” “worse for my routine,” and “feels cheaper to me” are framed as personal opinions. Under the written project rubric, these rationales do not support changing the three frozen `PASS` labels to `FLAG`.

The two first-hand-use decisions are consistent with the project rule: a claimed personal experience combined with unknown use warrants `HUMAN_REVIEW`. The return does not resolve whether the vague “another luxury house's formula” wording identifies a specific product for CH-CLAIM-01; that boundary remains open and should not be silently settled from this return.

## Dataset action

- No frozen label, manifest, or previous score changes based on this response.
- Preserve the return as a disagreement record; do not discard it or describe it as an independent reliability result.
- The data-quality issue now includes reviewer interpretation drift on CH-CONTEXT-01, in addition to the existing question of whether “formula” identifies a product under CH-CLAIM-01.
- I drafted a clearer operational guide that defines product identifiability and gives balanced decision examples: [annotation decision guide v3 draft](../data/annotation_decision_guide_v3_draft.md). This draft does not retroactively change prior review instructions.
- If another reviewer is available, use a fresh copy of the same label-hidden cases with the v3 draft. Otherwise retain the frozen labels and report the disagreement. Any revised dataset needs a new version and checksum.

## Source

CHANEL, [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), section 1. The paraphrase and `CH-*` identifiers used in this project are operational interpretations, not official CHANEL wording or identifiers.
