# Sensitivity to the later boundary-case adjudication

**Date:** 2026-10-01  
**Status:** retrospective sensitivity analysis, not a new benchmark or revised reported result.

The original primary and extension datasets each contain 30 synthetic cases balanced 10/10/10 across `PASS`, `FLAG`, and `HUMAN_REVIEW`. The [later 11-case rule-by-rule adjudication](boundary_case_adjudication_v1.md) proposes four overall label changes: `REVIEW-03` from `HUMAN_REVIEW` to `PASS`, `REVIEW-08` and `REVIEW-10` from `PASS` to `HUMAN_REVIEW`, and `HOLDOUT-06` from `HUMAN_REVIEW` to `FLAG`. It also proposes an additional `CH-DISC-02` rule ID for `HOLDOUT-17`, without changing that case's overall `FLAG`.

The table below re-scores the **already saved** keyword and AI predictions under those four hypothetical label changes. No new model call or prompt change was made, and the original files were not overwritten.

| Split | Reference labels | PASS / FLAG / HUMAN_REVIEW | AI correct | Keyword correct |
|---|---|---:|---:|---:|
| Primary 30 | Original frozen | 10 / 10 / 10 | 27/30 | 24/30 |
| Primary 30 | Hypothetical adjudicated | 9 / 10 / 11 | 30/30 | 23/30 |
| Extension 30 | Original frozen | 10 / 10 / 10 | 23/30 | 20/30 |
| Extension 30 | Hypothetical adjudicated | 10 / 11 / 9 | 24/30 | 19/30 |

Every proposed overall label change matches the saved AI prediction on that case. This is precisely why the hypothetical 30/30 primary score **must not** be presented as independent accuracy evidence: the adjudication happened after AI outputs had been inspected, and the selected boundary cases were already known to be contested. A plausible rule-level rationale does not remove this selection and hindsight risk. The hypothetical labels also break the instructor-requested 10/10/10 balance in each 30-case split.

The valid presentation for the current submission is therefore to keep the original frozen-label scores as historical development results, disclose the later disagreements and rule omissions, and describe this table only as a sensitivity check. The project should not replace the old scores or claim that the AI has become perfect. A future performance claim would need a new, pre-labeled set evaluated after the policy and rubric are fixed, without using its results to revise its labels.

**Reproduction:** from the project root, run `python scripts/label_sensitivity.py`. The script reads `data/primary_cases.jsonl`, `data/extension_cases_v2.jsonl`, the saved AI JSONL outputs, and the saved keyword prediction reports, then applies only the four adjudicated overall label overrides. It makes no API calls.
