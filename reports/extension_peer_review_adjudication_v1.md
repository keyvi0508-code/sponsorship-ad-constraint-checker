# Additional 30-case blind review and adjudication

**Date received:** 2026-09-30  
**Cases reviewed:** 30/30 unique blind IDs  
**Reviewer identity:** Not provided  
**Reviewer-reported relevant experience:** Not applicable

## Initial agreement

The reviewer matched the original draft label on 21 of 30 cases (70.0%). Rows below use the original author labels; columns are the blind reviewer's verdicts.

| Draft label \ Reviewer | PASS | FLAG | HUMAN_REVIEW |
|---|---:|---:|---:|
| PASS | 7 | 0 | 3 |
| FLAG | 0 | 9 | 1 |
| HUMAN_REVIEW | 0 | 5 | 5 |

The review surfaced two recurring interpretation issues. First, five unsupported objective claims were marked `FLAG`; under the project rubric, absent substantiation means the reviewer cannot establish truth or falsity, so the script should go to `HUMAN_REVIEW`. Second, some cases were escalated solely because creator product use was unknown even though the script only showed a product and made no first-hand opinion or usage claim. Unknown use matters when the script implies a review, opinion, or hands-on application.

## Case-by-case adjudication

| Case | Draft | Reviewer | Proposed adjudication | Reason |
|---|---|---|---|---|
| `HOLDOUT-03` | HUMAN_REVIEW | FLAG | Retain HUMAN_REVIEW | “Side-by-side wear test” suggests a comparative method, but the supplied wording does not make the impartiality claim explicit. The project rubric reserves `FLAG` for clear claims of impartiality and routes genuinely ambiguous implications to review. |
| `HOLDOUT-11` | FLAG | HUMAN_REVIEW | Retain FLAG | A visual product endorsement has no on-screen disclosure. This is a clear `CH-DISC-02` issue. Unknown product use does not override that direct disclosure violation, and the script makes no first-hand product opinion. |
| `HOLDOUT-26` | PASS | HUMAN_REVIEW | Change to HUMAN_REVIEW | The script presents a guide to applying the product, which reasonably implies hands-on use; supplied use metadata is unknown. The safer source-grounded disposition is human review under `CH-CLAIM-01`. |
| `HOLDOUT-07` | PASS | HUMAN_REVIEW | Retain PASS | The script describes packaging differences without criticizing the competitor. `CH-CONTEXT-01` applies to competitor criticism presented as impartial; a neutral mention without criticism is not a breach. |
| `HOLDOUT-27` | HUMAN_REVIEW | FLAG | Retain HUMAN_REVIEW | “Lasts 24 hours on everyone” is an objective claim with no supporting evidence. Missing support does not prove the statement false; the reviewer should verify it. |
| `HOLDOUT-16` | PASS | HUMAN_REVIEW | Retain PASS | The script shows a compact and contains clear disclosure, but makes no product opinion, review, or claim of actual use. Unknown use alone is not enough to invoke `CH-CLAIM-01`. |
| `HOLDOUT-30` | HUMAN_REVIEW | FLAG | Change to PASS | The statement is explicitly bounded to the creator's own week of use, and metadata confirms actual use. The guide permits truthful opinions grounded in actual experience; no evidence is supplied that the creator's personal experience is false or represented as a universal guarantee. |
| `HOLDOUT-09` | HUMAN_REVIEW | FLAG | Retain HUMAN_REVIEW | The efficacy statement is objective and unsupported in the packet. It needs substantiation; it is not established as false from the script alone. |
| `HOLDOUT-22` | HUMAN_REVIEW | FLAG | Retain HUMAN_REVIEW | A named product page without a supporting passage does not substantiate the universal suitability and guarantee claims. A human must verify the exact claims. |

## Proposed label revision

Two labels change in the adjudicated draft: `HOLDOUT-26` moves from `PASS` to `HUMAN_REVIEW`, and `HOLDOUT-30` moves from `HUMAN_REVIEW` to `PASS`. This preserves a balanced 10/10/10 class distribution while grounding the changes in the rule wording and supplied metadata. The resulting agreement with the reviewer's original labels would be 22/30 (73.3%); the primary peer-review result remains the unedited initial agreement of 21/30 (70.0%).

The revised labels are stored separately in [the adjudicated draft dataset](../data/extension_cases_v2_adjudicated_draft.jsonl), with checksum and pending status in [its draft manifest](../data/extension_manifest_v2_draft.json). The original draft set, blind packet, and raw mapping remain unchanged. No AI or keyword evaluation has been run on this extension. Do not call the revised file frozen until the project owner signs off.

## What this review does and does not show

The return is useful evidence that several rubric boundaries need to be explicit, especially `FLAG` versus `HUMAN_REVIEW` for unsupported factual claims and the conditions under which unknown product use matters. It is a single reviewer round; the reviewer's identity was not supplied, so this is recorded as a reviewer return, not verified inter-annotator reliability. The 70.0% figure is raw agreement on this purpose-built set, not a claim about general reviewer performance.
