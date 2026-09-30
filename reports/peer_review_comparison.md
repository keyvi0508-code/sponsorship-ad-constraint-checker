# Blind peer-review comparison (draft)

## Summary

- All 30 blinded cases were returned with a verdict.
- Peer verdict counts: `PASS` 15, `FLAG` 11, `HUMAN_REVIEW` 4.
- Agreement with the current draft labels: **18/30 (60%)**; 12 cases differ.
- Exploratory Cohen’s kappa: **0.40** (small, deliberately balanced set; interpret cautiously).
- These are annotator-comparison results, not AI performance. No gold labels have been changed by this report.

## Cases requiring adjudication

| Blind ID | Original case | Draft label | Peer label | Review note |
|---|---|---:|---:|---|
| R06 | REVIEW-08 | HUMAN_REVIEW | FLAG | Peer treated “feels cheap to me” plus CHANEL sponsorship as an automatic breach. The rule concerns implying impartiality; this personal wording does not clearly make that implication. Discuss PASS vs HUMAN_REVIEW; FLAG is not established by the stated rationale. |
| R07 | REVIEW-10 | HUMAN_REVIEW | FLAG | “Cheaper to me” is framed as personal judgment and the connection is disclosed. The peer rationale does not identify an impartiality claim. Reassess PASS vs HUMAN_REVIEW; FLAG is not established. |
| R09 | FLAG-09 | FLAG | PASS | Visual endorsement is present, but the on-screen text is “New favourite lipstick,” not a disclosure. Caption and spoken disclosure do not replace the required visual disclosure. FLAG remains supported under CH-DISC-02. |
| R12 | REVIEW-02 | HUMAN_REVIEW | FLAG | “Worse for my routine” is personal criticism, not an explicit impartiality claim. Peer applies a broader rule than the source-mapped standard. Discuss PASS vs HUMAN_REVIEW; do not treat all competitor criticism as an automatic FLAG. |
| R13 | FLAG-06 | FLAG | PASS | The spoken endorsement has no spoken disclosure. `#ad` in the caption does not substitute for disclosure in the spoken medium. FLAG remains supported under CH-DISC-02. |
| R14 | PASS-09 | PASS | FLAG | The guide lists `#GiftFromChanel` as an acceptable example, and the spoken line also says “paid partnership with CHANEL.” The peer appears to reverse the instructions. PASS remains supported. |
| R18 | REVIEW-01 | HUMAN_REVIEW | FLAG | “Overpriced for what you get” is a competitor criticism alongside a disclosed CHANEL connection. Whether this implies impartiality is context-sensitive, so HUMAN_REVIEW is consistent with the rubric; the rationale does not establish a clear FLAG. |
| R20 | FLAG-05 | FLAG | PASS | Although the caption disclosure occurs on line 2, the verbal endorsement scene lacks a spoken disclosure: “Here is the look I created with CHANEL” does not disclose sponsorship. FLAG remains supported under CH-DISC-02. |
| R24 | FLAG-07 | FLAG | PASS | The visual endorsement has only a product name on screen, not a sponsorship disclosure. Caption disclosure does not replace on-screen disclosure. FLAG remains supported under CH-DISC-02. |
| R28 | FLAG-04 | FLAG | PASS | With multiple brands, generic `#ad` does not identify CHANEL as sponsor. Naming a CHANEL foundation in the spoken text is not itself a sponsorship disclosure. FLAG remains supported under CH-DISC-01. |
| R29 | REVIEW-07 | HUMAN_REVIEW | PASS | “This finish lasts all day” is an objective duration claim, but no source is supplied. It should go to HUMAN_REVIEW under CH-CLAIM-01 rather than be treated as an established personal opinion. |
| R30 | REVIEW-03 | HUMAN_REVIEW | FLAG | “My own test” and “feels less suited to me” are mixed signals; they may imply a comparative independent test but do not clearly claim impartiality. HUMAN_REVIEW fits the stated ambiguity; FLAG is not established. |

## Patterns to resolve before freezing labels

- **Competitor criticism:** CHANEL section 1 focuses on representing or implying impartiality when criticizing competitors; it does not say every negative competitor opinion is automatically a violation. Resolve whether each ambiguous case is personal opinion, an implied impartial comparison, or needs HUMAN_REVIEW. [CHANEL Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/).
- **Disclosure by medium:** A caption label does not replace spoken disclosure for verbal endorsements or on-screen disclosure for visible endorsements. Product/brand naming is also not the same as disclosing a sponsorship.
- **Specific accepted wording:** `#GiftFromChanel` is listed as acceptable in section 2; it should not be labelled insufficient.
- **Claims:** A factual duration/performance claim without evidence should be escalated to HUMAN_REVIEW, not assumed to be a subjective opinion.

## Recommended next action

Review the 12 cases with the peer, explain the above source-mapped distinctions, and ask whether the peer would revise any decisions. Separately, adjudicate the two subjective competitor-criticism draft labels (REVIEW-08 and REVIEW-10), which may be better labelled PASS under a strict reading. Then replace any genuinely confounded cases while preserving 10 cases per class, update rationales, rerun the baseline as a development check, and freeze only after labels are settled.

> Historical snapshot: this report compares the earlier pre-adjudication dataset and its blind packet. It does not represent the revised 30-case dataset.
