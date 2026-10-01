# Blind peer review: initial observations

**Status:** historical first-pass analysis. The completed rule-by-rule decisions are in [boundary-case adjudication v1](boundary_case_adjudication_v1.md). Original labels and evaluation data remain unchanged.
**Review packet:** `data/boundary_case_blind_review_packet_v1.md`
**Review date/background:** not supplied in the returned response.

## What the response shows

The reviewer returned verdicts and rationales for all 11 cases. Against the labels currently stored for the corresponding cases, the raw overall-verdict agreement is **7/11 (63.6%)**. This is a descriptive agreement count on a small, deliberately boundary-focused sample. It is not a reliability estimate and should not be presented as benchmark performance.

| Blind case | Project case | Current project label | Reviewer label | Initial reading |
|---|---|---|---|---|
| CAL-01 | REVIEW-01 | HUMAN_REVIEW | PASS | Disagreement: “overpriced for what you get” is broader than an explicitly personal preference; keep the impartiality ambiguity visible and adjudicate against the guide. |
| CAL-02 | REVIEW-02 | PASS | PASS | Agreement; “worse for my routine” is clearly personal preference under the current context rule. |
| CAL-03 | REVIEW-03 | HUMAN_REVIEW | PASS | Disagreement: reviewer treats “my own test” as settling the issue. The current guide treats an unresolved evidence-based/impartial implication as HUMAN_REVIEW; confidence should not be high without explaining that boundary. |
| CAL-04 | REVIEW-08 | PASS | PASS | Agreement on context. Keep the separate open question about whether “another luxury house’s formula” identifies a product/feature for CH-CLAIM-01. |
| CAL-05 | REVIEW-10 | PASS | PASS | Agreement on context. Same product-identifiability/use question as CAL-04 remains separate. |
| CAL-06 | REVIEW-11 | HUMAN_REVIEW | PASS | Disagreement: a side-by-side wear test and timed comparative result can imply an evidence-based comparison even when described as the creator’s own test. The guide’s calibration standard supports HUMAN_REVIEW pending adjudication. |
| CAL-07 | REVIEW-12 | HUMAN_REVIEW | HUMAN_REVIEW | Agreement; first-person foundation experience with use marked unknown needs review. |
| CAL-08 | HOLDOUT-06 | HUMAN_REVIEW | HUMAN_REVIEW | Overall agreement on product use, but likely omitted CH-DISC-02: the caption has `#ad`, while spoken endorsement has no spoken sponsorship disclosure and the visible endorsement has no visible sponsorship disclosure. Check rule-by-rule; under the current precedence, a confirmed disclosure FLAG would make the overall verdict FLAG. |
| CAL-09 | HOLDOUT-12 | HUMAN_REVIEW | HUMAN_REVIEW | Agreement on the overall escalation. The reviewer identifies both context and claim/use questions; retain exact claim language and the missing test/use fact. |
| CAL-10 | HOLDOUT-15 | HUMAN_REVIEW | PASS | Disagreement: confirmed use does not settle whether “wear test” and the comparative transfer result imply an evidence-based competitor assessment. The current guide’s calibration example supports HUMAN_REVIEW. |
| CAL-11 | HOLDOUT-17 | FLAG | FLAG | Agreement on the clear first-hand-use conflict. Likely omitted CH-DISC-02 as well: the spoken product review has no spoken CHANEL disclosure. The overall FLAG remains, but the rule list may be incomplete. |

## Quality of the peer response

The reviewer applied the central principle correctly in several cases: a negative personal preference is not automatically a violation, unknown use is not the same as confirmed non-use, and an explicit “never tried” statement can support a clear first-hand-use FLAG. They also supplied exact evidence and missing facts for most cases.

The main weakness is **rule coverage and calibration**, not effort. The response frequently jumps from one plausible rule to the overall verdict instead of documenting each applicable rule separately. In CAL-08 and CAL-11 it treats a caption `#ad` as sufficient even though CHANEL’s guide says video disclosures should match the medium: verbal disclosure when the endorsement is verbal, and on-screen disclosure when the endorsement is visible. The project’s CH-DISC-02 operationalizes those surfaces. In CAL-06 and CAL-10, the reviewer uses “my own test” or confirmed use to resolve competitor-impartiality concerns, although actual use and whether the comparison sounds impartial are distinct questions.

The response also marks several genuinely contested cases `high` confidence. For CAL-01, CAL-03, CAL-06, and CAL-10, `medium` would better reflect the unresolved interpretation, even if the overall verdict remains unchanged after adjudication. The response omits the requested review date and reviewer-experience field; record these as “not provided,” rather than inferring them.

## Recommended next step

Keep the peer’s answer unchanged as the raw blind-review record. Do not overwrite the current labels or recalculate the 60-case model/baseline scores from this one review. The project owner should adjudicate the four overall disagreements (CAL-01, CAL-03, CAL-06, CAL-10), then perform an all-rule disclosure check on CAL-08 and CAL-11, and resolve whether CAL-04/CAL-05 trigger CH-CLAIM-01 under the product-identifiability rule. If any label or rule IDs change, create a new adjudicated dataset version and manifest, preserve the existing versions, and rerun metrics only on that new version.

## Source check

The current CHANEL Social Media Guidelines say not to imply impartiality when criticizing a competitor, require disclosures close to the endorsement and at the beginning of a post, and say verbal/visual disclosures should match endorsements in those media. They also require product opinions to reflect actual experience. The project’s `CH-*` IDs are local operational labels, not official CHANEL identifiers. Source: <https://www.chanel.com/us/makeup/social-media-guidelines/> (accessed 2026-09-30).
