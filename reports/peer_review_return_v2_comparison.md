# Revised dataset v2: blind-review comparison

Status: comparison only; no labels changed in this report.

## Summary

- All 30 revised cases received a reviewer verdict.
- Agreement with the current draft labels: **20/30 (66.7%)**.
- Exploratory Cohen's kappa: **0.50**. Interpret cautiously because this is a small, constructed set and reviewer identity/provenance is not encoded in the returned text.
- Draft labels: 10 PASS, 10 FLAG, 10 HUMAN_REVIEW.
- Reviewer labels counted from the 30 individual entries: 11 PASS, 11 FLAG, 8 HUMAN_REVIEW. The packet's own summary says 12 PASS, 11 FLAG, 7 HUMAN_REVIEW, so its summary tally is off by one in two classes; case-level entries were used for all metrics.
- The earlier comparison reports concern the old packet and are not interchangeable with this v2 result.

## Disagreements

| Blind ID | Case | Draft | Reviewer | Adjudication note |
|---|---|---:|---:|---|
| R01 | FLAG-09 | FLAG | PASS | The on-screen line is only “New favourite lipstick.” It is an opinion, but it is not a relationship disclosure for the visual endorsement. Caption/spoken disclosure does not supply the on-screen disclosure. Draft FLAG is supported. |
| R03 | REVIEW-01 | HUMAN_REVIEW | FLAG | “Overpriced for what you get” is negative competitor criticism, but the rationale does not show an impartiality claim. The narrow rule does not make all competitor criticism an automatic FLAG; retain HUMAN_REVIEW for context. |
| R05 | REVIEW-10 | PASS | FLAG | The creator discloses a CHANEL connection and uses “cheaper to me,” a personal comparison. No impartiality claim is apparent in the supplied wording; draft PASS is supported. |
| R09 | FLAG-07 | FLAG | PASS | “CHANEL Rouge Allure” is a product name, not a sponsorship disclosure. The visual endorsement lacks an on-screen relationship disclosure; draft FLAG is supported. |
| R10 | REVIEW-02 | PASS | FLAG | “Worse for my routine” is framed as personal preference and does not claim impartiality. Draft PASS is supported by the narrow rule. |
| R11 | FLAG-06 | FLAG | PASS | The spoken endorsement lacks spoken relationship disclosure. Caption `#ad` does not replace it; draft FLAG is supported. |
| R12 | REVIEW-08 | PASS | FLAG | “Feels cheap to me” is subjective wording, with no explicit or clear implied impartiality. Draft PASS is supported; sponsorship plus criticism alone is insufficient. |
| R15 | REVIEW-13 | HUMAN_REVIEW | PASS | A generic CHANEL product-information page is named, but the packet supplies no study details to establish that it supports the exact “9 out of 10” statistic. Draft HUMAN_REVIEW is supported. |
| R18 | FLAG-05 | FLAG | HUMAN_REVIEW | The reviewer is right that a disclosure on caption line 2 is within the stated first two lines, so the draft rationale based only on caption placement is weak. However, the spoken endorsement has no clear spoken paid-relationship disclosure. Keep FLAG provisionally under CH-DISC-02 and revise the rationale to name this medium mismatch. |
| R21 | REVIEW-03 | HUMAN_REVIEW | FLAG | “My own test” may suggest a comparative test, but “feels less suited to me” is personal and does not clearly claim impartiality. HUMAN_REVIEW remains the more calibrated outcome. |

## Pattern and next step

The reviewer correctly identifies several claim-evidence and disclosure cases, but overlooks matching-medium disclosure in R01, R09, and R11. Five competitor-criticism cases are treated as automatic violations even where the wording is expressly personal; the rulebook should continue to distinguish criticism from an implied claim of impartiality. R18 exposes a rationale defect: the caption's second line is within the defined first-two-lines window, while the stronger basis for FLAG is the missing spoken disclosure.

See [the adjudication report](peer_review_return_v2_adjudication.md) and [rubric clarification](../data/peer_review_rubric_v2.md) for the case decisions and protocol. Do not present the 66.7% agreement as model accuracy.
