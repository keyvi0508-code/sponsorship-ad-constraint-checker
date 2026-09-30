# Blind-review return 2 comparison (draft)

## Summary

- All 30 cases have verdicts.
- This return: `PASS` 16, `FLAG` 10, `HUMAN_REVIEW` 4.
- Agreement with the current draft labels: **19/30 (63.3%)**; 11 cases still differ.
- Compared with the prior returned packet, only R14 changed (`FLAG` → `PASS`), correctly recognizing `#GiftFromChanel` as an acceptable example. The other 29 verdicts are unchanged. The file alone cannot establish whether this was the same annotator or a new reviewer.
- No gold labels have been changed. This is annotator comparison, not model performance.

## Remaining disagreements

| Blind ID | Case | Draft label | New reviewer label | Note |
|---|---|---:|---:|---|
| R06 | REVIEW-08 | HUMAN_REVIEW | FLAG | REVIEW-08: “feels cheap to me” is subjective. Sponsorship plus criticism alone does not establish an impartiality implication; consider PASS or HUMAN_REVIEW, not an automatic FLAG. |
| R07 | REVIEW-10 | HUMAN_REVIEW | FLAG | REVIEW-10: the script discloses its CHANEL connection and frames the comparison as “cheaper to me.” The rationale does not identify an impartiality claim; adjudicate PASS vs HUMAN_REVIEW. |
| R09 | FLAG-09 | FLAG | PASS | FLAG-09: on-screen text is only “New favourite lipstick,” not a relationship disclosure; a visual endorsement still needs on-screen disclosure. |
| R12 | REVIEW-02 | HUMAN_REVIEW | FLAG | REVIEW-02: “worse for my routine” is framed as personal experience. FLAG is not supported solely by having a CHANEL relationship; adjudicate PASS vs HUMAN_REVIEW. |
| R13 | FLAG-06 | FLAG | PASS | FLAG-06: the spoken endorsement has no spoken relationship disclosure. Caption `#ad` does not substitute for the spoken medium. |
| R18 | REVIEW-01 | HUMAN_REVIEW | FLAG | REVIEW-01: “overpriced for what you get” is competitor criticism, but whether it implies impartiality is context-sensitive; HUMAN_REVIEW fits better than a certain FLAG. |
| R20 | FLAG-05 | FLAG | PASS | FLAG-05: the caption disclosure is on line 2, but the verbal endorsement scene itself lacks a spoken sponsorship disclosure. |
| R24 | FLAG-07 | FLAG | PASS | FLAG-07: “CHANEL Rouge Allure” names the product but does not disclose the sponsorship in the visual endorsement. |
| R28 | FLAG-04 | FLAG | PASS | FLAG-04: with multiple brands, generic `#ad` does not identify CHANEL as sponsor; mentioning a CHANEL product is not a partnership disclosure. |
| R29 | REVIEW-07 | HUMAN_REVIEW | PASS | REVIEW-07: “lasts all day” is an objective duration claim without a supplied source; route to HUMAN_REVIEW. |
| R30 | REVIEW-03 | HUMAN_REVIEW | FLAG | REVIEW-03: “My own test” may suggest comparative testing, but the wording does not clearly claim impartiality; HUMAN_REVIEW is more appropriate than a certain FLAG. |

## Interpretation

- The correction on R14 resolves one direct reading error: the official guide lists `#GiftFromChanel` among acceptable disclosure examples.
- Several remaining `PASS` labels overlook that caption disclosure does not replace disclosure in spoken or on-screen video content, and that a product name is not itself a sponsorship disclosure.
- Five competitor-criticism cases remain marked `FLAG` by the reviewer. CHANEL’s rule concerns representing or implying impartiality in competitor criticism; it does not make every negative competitor comment an automatic violation. Some of these draft `HUMAN_REVIEW` labels also merit adjudication because personal wording may support `PASS`.
- The `lasts all day` claim is not supported by the supplied evidence and should remain `HUMAN_REVIEW`.

## Next step

Adjudicate the 11 remaining cases against the source-mapped rubric. If any draft case is relabelled, keep an audit note and preserve 10 cases in each gold class by replacing/relabeling cases only with documented reasons. Do not freeze the data until that reconciliation is complete.

> Historical snapshot: this report compares the earlier pre-adjudication dataset and its blind packet. It does not represent the revised 30-case dataset.
