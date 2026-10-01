# Annotation decision guide v3 — draft

**Status:** clarification draft created after the targeted reviewer disagreement on 30 September 2026. It is not retroactively attributed to earlier reviewers. Do not use this draft to silently change frozen labels or past scores.

This is a project annotation aid for the narrow rules selected from CHANEL's public [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/). The `CH-*` identifiers are project IDs, not official CHANEL rule IDs. Apply only the supplied script and metadata; do not infer a creator's intent, audience reaction, product use, video visibility, or substantiation from missing information.

## Verdict standard

- **`PASS`** — no in-scope issue is apparent in the supplied text and metadata.
- **`FLAG`** — the supplied information clearly contradicts an in-scope rule. A possible concern or missing fact alone is not enough.
- **`HUMAN_REVIEW`** — a fact or meaning needed to apply a rule cannot be resolved. Do not use it merely because content is negative or sounds unfavorable.

For every non-`PASS` decision, quote the evidence, name the rule, and explain why that wording meets the rule threshold. If evidence is missing, state what information is needed.

### Evaluate each rule before assigning the overall verdict

Record a separate result for every applicable rule. If one rule is `FLAG`, the overall case is `FLAG`; otherwise, if one rule is `HUMAN_REVIEW`, the overall case is `HUMAN_REVIEW`; use overall `PASS` only when all applicable rules pass or no in-scope rule applies. This prevents a `PASS` under competitor impartiality from hiding an unresolved first-hand-use question. A first-person sentence is evidence that the script makes an experience claim; it is not independent proof that the creator actually used the product. Apply the supplied use metadata consistently: `false` can establish a conflict, `unknown` cannot establish either use or non-use.

## CH-CONTEXT-01 — competitor criticism and impartiality

The source rule is about a CHANEL-connected creator representing or implying that criticism of a CHANEL competitor is impartial. The project does not treat all negative competitor statements as violations.

1. If there is no criticism of a competitor, this rule does not apply.
2. If the criticism is clearly framed as an individual preference or experience, the negative tone alone is not a breach. For example, a statement limited to what suits the creator's own routine or how something feels to them is not, by itself, a claim of impartiality.
3. `FLAG` only when the script clearly claims or strongly presents the criticism as neutral, independent, unbiased, or objectively established despite the CHANEL connection.
4. Use `HUMAN_REVIEW` when wording could reasonably be an evidence-based or impartial comparison but the implication cannot be resolved from the supplied text. Do not turn a hypothetical audience interpretation into a clear breach.
5. The mere fact that the creator has a CHANEL connection does not make a personal criticism an impartiality violation. Disclosure informs the audience of the relationship; it does not by itself settle whether the separate impartiality rule is breached.

## CH-CLAIM-01 — first-hand opinion and factual-claim support

### Is a specific product identifiable?

- **Yes:** the text or supplied metadata names the product/feature or clearly links a reference such as “this foundation” to a specific item.
- **No:** the wording is only a general brand-level preference or criticism and no product or feature is identified.
- **Unclear:** a category or vague reference such as “another house's formula” appears, but the supplied context does not show which product or feature is meant.

### Apply the first-hand-use rule

- An opinion or review about an identifiable product/feature with use marked `true` does not trigger a use concern on that fact alone.
- If an identifiable product/feature is being reviewed and use is `false`, `FLAG` the clear conflict with the first-hand-use rule.
- If an identifiable product/feature is being reviewed and use is `unknown`, use `HUMAN_REVIEW`; unknown does not prove either use or non-use.
- If no product/feature is identifiable, do not trigger CH-CLAIM-01 solely because the use field is unknown.
- If identifiability is unclear and that determines whether the rule applies, use `HUMAN_REVIEW` and name the missing context.

### Apply the factual-claim rule

Objective product claims need support that addresses the exact claim. A source title or general product page does not automatically substantiate a statistic or guarantee. If support is absent or does not clearly cover the wording, use `HUMAN_REVIEW`; do not call the statement false without evidence.

## Reviewer procedure

Review cases without seeing current labels, prior reviewer responses, model outputs, or baseline predictions. Record a verdict, rule ID(s), verbatim evidence, rationale, confidence, and missing information. Keep the original response. The project owner adjudicates disagreements against the source and this guide, records the reason, and versions any label change with a new checksum. Report raw agreement only with its denominator; do not call it reliability when there is only one reviewer or the review process/provenance is not established.

## Calibration examples (not evaluation cases)

- “That shade is more comfortable for my everyday routine” is personal wording; it is not automatically an impartiality violation.
- “An independent, controlled comparison proves the rival product performs worse” clearly presents an impartial/evidence-based competitor criticism; assess it under CH-CONTEXT-01.
- “I tested this named serum for a week” with use marked `unknown` needs `HUMAN_REVIEW` under CH-CLAIM-01.
- “Another luxury house's formula feels cheap to me” can be `PASS` under CH-CONTEXT-01 while remaining `HUMAN_REVIEW` overall if the reviewer cannot tell whether the formula is an identifiable product/feature and actual use is unknown.
- “I have never tried this serum, but it works beautifully” with a product review and use marked `false` is `FLAG` under CH-CLAIM-01.
- “I prefer that brand's overall style” without reference to a product or feature does not trigger CH-CLAIM-01 solely because use is unknown.
