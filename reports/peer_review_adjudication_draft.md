# Blind-review adjudication draft (historical v1)

Status: historical first-return adjudication. The current revised dataset and final v2 decisions are documented in `peer_review_return_v2_adjudication.md`.

## Recommendation

Adjudicate the five disclosure cases and the unsupported factual-claim case as in the table below. For the competitor-criticism cases, do not automatically mark every criticism as a violation. The project owner accepted changing R06, R07, and R12 from `HUMAN_REVIEW` to `PASS`, because each is framed as personal opinion and does not clearly imply impartiality. Retain `HUMAN_REVIEW` for R18 and R30 because their wording leaves a more meaningful contextual question. These are provisional adjudications against the project's source-mapped rubric, not a claim that the brand guide itself defines every example.

## Case-by-case decisions

| Blind ID | Draft label | Reviewer label | Proposed label | Adjudication |
|---|---:|---:|---:|---|
| R06 / REVIEW-08 | HUMAN_REVIEW | FLAG | PASS | “Feels cheap to me” is explicitly framed as subjective perception. The supplied text does not imply an impartial or neutral comparison, so there is no clear breach of the narrow impartiality rule. |
| R07 / REVIEW-10 | HUMAN_REVIEW | FLAG | PASS | The creator discloses the CHANEL connection and says the other formula feels “cheaper to me.” This is a disclosed, personal comparison, not a clear claim of impartiality. |
| R09 / FLAG-09 | FLAG | PASS | FLAG | The scene has a visual endorsement and the on-screen text is only “New favourite lipstick.” The caption and spoken sponsorship disclosure do not replace an on-screen disclosure in the visual endorsement. |
| R12 / REVIEW-02 | HUMAN_REVIEW | FLAG | PASS | “Worse for my routine” is framed as personal preference, with no supplied wording suggesting an impartiality claim. The narrow rule does not make all negative competitor opinions violations. |
| R13 / FLAG-06 | FLAG | PASS | FLAG | The spoken line endorses the fragrance, but there is no spoken relationship disclosure. Caption `#ad` does not substitute for disclosure in the spoken medium. |
| R18 / REVIEW-01 | HUMAN_REVIEW | FLAG | HUMAN_REVIEW | “Overpriced for what you get” criticizes a competitor but does not explicitly claim impartiality. Whether the wider context implies impartiality is interpretive, so HUMAN_REVIEW is appropriate. |
| R20 / FLAG-05 | FLAG | PASS | FLAG | The caption's disclosure is on line 2, and the spoken line “Here is the look I created with CHANEL” does not clearly disclose a paid relationship. Keep FLAG under the matching-medium/placement rule; update the original rationale to identify both issues. |
| R24 / FLAG-07 | FLAG | PASS | FLAG | The on-screen text names “CHANEL Rouge Allure,” which identifies a product but does not disclose a material connection. The visual endorsement needs an on-screen relationship disclosure. |
| R28 / FLAG-04 | FLAG | PASS | FLAG | Multiple brands appear. Generic `#ad` does not identify CHANEL as sponsor, and naming the CHANEL foundation in speech is not a sponsorship disclosure. |
| R29 / REVIEW-07 | HUMAN_REVIEW | PASS | HUMAN_REVIEW | “Lasts all day” is an objective duration claim and no supporting source is supplied. Route it for evidence review rather than treating it as established. |
| R30 / REVIEW-03 | HUMAN_REVIEW | FLAG | HUMAN_REVIEW | “My own test” may suggest comparison, but “feels less suited to me” is personal wording and does not clearly claim impartiality. Preserve HUMAN_REVIEW for contextual judgment. |

## Dataset and evaluation implications

- The revised primary set now has 10 PASS / 10 FLAG / 10 HUMAN_REVIEW. Three redundant clean examples (PASS-04, PASS-07, PASS-10) are retained in `data/archived_cases_pre_adjudication.jsonl`; they are not part of the revised evaluation set. Three new borderline cases (REVIEW-11 through REVIEW-13) replaced them and have draft HUMAN_REVIEW labels. Those three cases still require blind review before freezing.
- Do not count this reviewer comparison as model performance. It measures agreement with draft annotations.
- The file alone does not establish whether this packet is a revision from the first annotator or an independent second annotator. Record that provenance before making any claim about inter-annotator agreement.
- After the replacement cases are reviewed, adjudicate any remaining differences, document the final labels, then freeze the dataset and run the measured Ctrl+F baseline and AI evaluation.

## Replacement-case notes

- REVIEW-11 tests whether a disclosed, subjective side-by-side wear-test comparison could imply impartiality.
- REVIEW-12 tests a first-hand experience claim when the supplied usage metadata is unknown.
- REVIEW-13 tests a numerical consumer-study claim when a source is named but the supporting study evidence is not supplied.
