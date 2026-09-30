# AI disagreement adjudication proposal

Status: proposed rule clarification only. The frozen v2 dataset, run output, and reported scores have not been changed.

## Proposed decisions for the four disagreements

| Case | Frozen v2 label | AI result | Proposed interpretation | Reason |
|---|---|---|---|---|
| `REVIEW-01` | `HUMAN_REVIEW` | `PASS` | Retain `HUMAN_REVIEW`; model miss | “Overpriced for what you get” is a broad comparative/value judgment. The supplied wording does not clearly claim impartiality, but it is less clearly personal than the rubric's explicit preference examples. Route to a person instead of silently passing it. |
| `REVIEW-02` | `PASS` | `HUMAN_REVIEW` | Retain `PASS`; AI likely over-applied `CH-CLAIM-01` | “Worse for my routine” is framed as personal preference and does not identify a particular product, service, or factual product claim. The product-use field being unknown alone should not turn every brand-level personal comparison into a review case. |
| `REVIEW-08` | `PASS` | `HUMAN_REVIEW` | Mark for blinded human re-adjudication; `HUMAN_REVIEW` is supported by the written rules | “Formula feels cheap to me” is an opinion about a product, while `creator_used_product` is unknown. The source rule and project rulebook require actual experience for product opinions; the evaluator is told to route unresolved first-hand use to a person. The existing `PASS` rationale covers impartiality but does not resolve this separate rule. |
| `REVIEW-10` | `PASS` | `HUMAN_REVIEW` | Mark for blinded human re-adjudication; `HUMAN_REVIEW` is supported by the written rules | The script compares product formulas, but the supplied metadata does not establish first-hand use. The same unresolved `CH-CLAIM-01` issue applies. |

## Recommended rubric clarification

1. Apply `CH-CONTEXT-01` to whether a competitor criticism is presented as impartial. A clearly personal brand-level preference, without an identifiable product claim or impartiality cue, may `PASS`. A value judgment that could reasonably read as a neutral comparison but is not explicit should go to `HUMAN_REVIEW`.
2. Apply `CH-CLAIM-01` separately when the script gives an opinion about an identifiable product or service. If actual use is explicitly false, `FLAG`; if use is unknown, `HUMAN_REVIEW`; if use is confirmed, do not flag solely for missing first-hand use. Do not extend this check to a vague brand-level preference unless the script identifies a product/service or makes a factual claim.
3. Do not let `PASS` under the competitor-impartiality rule erase an independent first-hand-use issue. Record every applicable rule before assigning the overall verdict.

This interpretation follows CHANEL's published distinction between impartiality about competitor criticism (section 1) and actual experience for product opinions (section 3), along with this project's `CH-CLAIM-01` rulebook summary. See [CHANEL Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/).

## Evaluation-integrity decision

Do not replace the frozen labels in place or recalculate the original score from these proposals. The AI outputs have already been seen, so changing labels now and re-scoring the same run would risk tuning the answer key to the model. The next defensible evaluation should version the rubric, have a human adjudicator label the affected cases without seeing the AI outputs, rebalance the set only through a documented process, freeze a new manifest, and use fresh cases as a holdout if the prompt is changed.

The present result remains 26/30 for AI and 24/30 for the measured keyword baseline on frozen v2. Under this proposal, `REVIEW-01` remains an AI miss; `REVIEW-02` remains an AI over-escalation; `REVIEW-08` and `REVIEW-10` are unresolved label questions rather than confirmed AI errors.
