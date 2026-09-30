# Revised dataset v2: peer-review adjudication

Status: labels frozen for reproducible evaluation after adjudication. Reviewer identity/provenance was not included in the return; record it before claiming independent peer-review reliability.

## Decision

The v2 reviewer returned labels for all 30 cases. Agreement with current labels is 20/30 (66.7%), with exploratory Cohen's kappa 0.50. These statistics measure agreement between annotations only; they are not model-performance metrics. No verdict changed as a result of this review. The returned packet's summary tally (12 PASS, 11 FLAG, 7 HUMAN_REVIEW) conflicts with its 30 individual verdicts; we counted 11 PASS, 11 FLAG, and 8 HUMAN_REVIEW from those entries. The rationale for FLAG-05 was corrected because its caption disclosure is on line 2 (within the project's first-two-lines window); the remaining basis for FLAG is the missing clear spoken paid-relationship disclosure.

The reviewer over-applies CH-CONTEXT-01 to five negative competitor comments. Under the public rule, criticism is not automatically a violation; the question is whether the creator represents or implies that the criticism is impartial. The case-by-case decisions are:

| Blind ID | Case | Draft label retained | Reviewer label | Final rationale |
|---|---|---:|---:|---|
| R01 | FLAG-09 | FLAG | PASS | “New favourite lipstick” is an opinion, not an on-screen relationship disclosure. Visual endorsement still needs a matching on-screen disclosure. |
| R03 | REVIEW-01 | HUMAN_REVIEW | FLAG | “Overpriced for what you get” is negative competitor criticism, but does not clearly claim impartiality. Keep HUMAN_REVIEW for context. |
| R05 | REVIEW-10 | PASS | FLAG | CHANEL connection is disclosed; “cheaper to me” is a personal comparison, not a clear impartiality claim. |
| R09 | FLAG-07 | FLAG | PASS | “CHANEL Rouge Allure” names a product; it does not disclose the sponsorship in the visual endorsement. |
| R10 | REVIEW-02 | PASS | FLAG | “Worse for my routine” is personal preference, with no clear impartiality claim. |
| R11 | FLAG-06 | FLAG | PASS | The spoken endorsement has no spoken relationship disclosure. Caption `#ad` does not replace it. |
| R12 | REVIEW-08 | PASS | FLAG | “Feels cheap to me” is subjective; the supplied wording does not imply impartiality. |
| R15 | REVIEW-13 | HUMAN_REVIEW | PASS | A generic CHANEL product-information page is named, but no study details establish that it supports the exact 9-out-of-10 statistic. |
| R18 | FLAG-05 | FLAG | HUMAN_REVIEW | Caption line 2 is within the stated first-two-lines window. The spoken line does not clearly disclose the paid relationship, which supports FLAG under the matching-medium rule. The case rationale was updated accordingly. |
| R21 | REVIEW-03 | HUMAN_REVIEW | FLAG | “My own test” may imply a comparative assessment, but “feels less suited to me” is personal. The implication remains contextual, so HUMAN_REVIEW is better calibrated. |

## Label counts and remaining status

The adjudicated set remains balanced at 10 PASS, 10 FLAG, and 10 HUMAN_REVIEW. A machine-readable comparison, including the confusion matrix, is in `peer_review_return_v2_comparison.json`. The reviewer-return text does not establish the reviewer's identity or whether this was an independent classmate review; record that provenance before reporting inter-annotator agreement. The dataset is frozen for the keyword-baseline run; the AI evaluation has not yet been run.
