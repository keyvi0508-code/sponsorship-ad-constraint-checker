# Boundary-case audit v1

**Status:** development audit, 30 September 2026. This report identifies cases to review for consistency; it does not change frozen labels or evaluation scores.

## Why this audit exists

The targeted peer review agreed with all five frozen overall labels, but its CAL-A and CAL-D rationales assessed competitor impartiality without resolving whether the competitor-formula opinions also invoke the first-hand-use rule. Similar patterns occur elsewhere in the two synthetic datasets. This is a policy-definition and annotation-consistency issue, not a reason by itself to increase dataset size.

## Related cases

| Case | Existing label | Relevant wording or fact | What it tests |
|---|---|---|---|
| `REVIEW-01` | `HUMAN_REVIEW` | “Another luxury house is overpriced for what you get.” | Contrast with personal “feels cheap to me” wording; rationale should say why this implies a more objective value judgment or why context is unresolved. |
| `REVIEW-02` | `PASS` | “This rival brand is worse for my routine.” | Personal routine framing; useful negative-opinion control. |
| `REVIEW-03` | `HUMAN_REVIEW` | “My own test: this rival brand feels less suited to me.” | Whether “my own test” implies an evidence-based comparison despite subjective wording. |
| `REVIEW-08` | `PASS` | “Another luxury house's formula feels cheap to me.”; use is `unknown` | Personal competitor criticism under CH-CONTEXT-01; product/formula identifiability under CH-CLAIM-01. |
| `REVIEW-10` | `PASS` | “...another luxury house's formula feels cheaper to me.”; use is `unknown` | Same dual-rule issue as REVIEW-08, with an explicit CHANEL connection. |
| `REVIEW-11` | `HUMAN_REVIEW` | “A side-by-side wear test...” | Whether test language implies an impartial/evidence-based comparison. |
| `REVIEW-12` | `HUMAN_REVIEW` | First-person foundation experience; use metadata is `unknown` | Unknown use is not proof of non-use; the script's own claim is not independent verification. |
| `HOLDOUT-06` | `HUMAN_REVIEW` | First-person foundation opinion; use is `unknown`; verbal and visual endorsement are marked true | Parallel unknown-use case, but it may also have a disclosure-placement issue: the spoken copy and on-screen text do not state the sponsorship. Review all applicable rules; do not assume it isolates product use. |
| `HOLDOUT-12` | `HUMAN_REVIEW` | “My own test suggests the rival fragrance lasts longer”; use is `unknown` | Two unresolved dimensions: impartiality implication and actual use. |
| `HOLDOUT-15` | `HUMAN_REVIEW` | Competitor lipstick wear-test comparison; use is `true` | Isolates context ambiguity even when product use is supplied. |
| `HOLDOUT-17` | `FLAG` | The creator says they have never tried the serum but reviews it; use is `false` | Clear contrast to unknown-use cases. Also check whether the spoken endorsement lacks the corresponding spoken disclosure under CH-DISC-02; the overall verdict may be right while the recorded rule IDs are incomplete. |

## Interpretation to settle

1. Keep rule-level findings distinct. A case may pass CH-CONTEXT-01 but still need HUMAN_REVIEW under CH-CLAIM-01.
2. State when competitor formula/feature opinions count as product opinions for CH-CLAIM-01. Do not apply the use rule to a general brand preference with no product or feature reference.
3. Distinguish personal sensory language from a test or comparison that may imply evidence-based impartiality. The words “test” or “comparison” should trigger review only when the broader wording leaves that implication unresolved; they are not automatic violations.
4. Treat `creator_used_product: unknown` as missing evidence, not as `false`. A first-person assertion is evidence of what the script claims, not external verification that the use occurred.
5. Review `REVIEW-01` against the same written standard as REVIEW-02/08/10 and document the reason for any different result.
6. Check for omitted co-occurring rules. In particular, HOLDOUT-06 and HOLDOUT-17 contain spoken endorsements without a spoken CHANEL disclosure, and HOLDOUT-06 also has a visual endorsement with no visible sponsorship disclosure. Confirm the project rule interpretation, then assess whether the frozen labels/rule IDs capture all applicable issues.

## Proposed next action

Use the draft annotation guide to do a blinded, rule-by-rule adjudication of the listed cases. Preserve every original label and reviewer response. If the project owner approves changes, create a new dataset version and manifest, then recompute baseline and AI metrics separately. Until then, report current scores against the frozen labels and describe these cases as unresolved boundary analysis.
