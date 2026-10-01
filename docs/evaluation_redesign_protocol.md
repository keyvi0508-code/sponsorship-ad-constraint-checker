# Submission evaluation plan

## Keep one clear project scope

The submission evaluates one product: a human-in-the-loop workbench for checking English sponsored creator scripts against a narrow interpretation of CHANEL's public Social Media Guidelines. Do not add ASA/CAP, another brand, a second jurisdiction, or a new real-world dataset to this submission. Those would require a separate rulebook, labels, and product explanation, and would distract from the question already being evaluated.

## Put the existing evidence in the right order

1. **Primary course evaluation:** the original frozen 30 synthetic cases in `data/primary_cases.jsonl`, balanced as 10 `PASS`, 10 `FLAG`, and 10 `HUMAN_REVIEW`. Report measured Ctrl+F/keyword results (24/30, 80.0%) beside the revised AI result (27/30, 90.0%). State that the AI prompt was revised after inspecting an earlier run, the cases were project-authored, and later rule-by-rule adjudication proposed changes to three primary labels. These scores remain tied to the original frozen labels. Treat this as descriptive development evidence on a small synthetic set, not real-world proof.
2. **Supplementary extension:** the additional frozen 30 synthetic cases in `data/extension_cases_v2.jsonl`, with their own results (keyword 20/30, 66.7%; AI 23/30, 76.7%). Label this as a supplementary, prompt-locked development check. Do not merge its score into the primary result or call it a representative real-world holdout.
3. **Combined 60-case file:** retain it for reproducibility, regression checks, and broader coverage. Do not present a single combined accuracy as the headline result; keep the two splits and their histories visible.

## Report both error directions

For each split, show the confusion matrix and class counts. Explicitly distinguish:

- a clean case incorrectly given `FLAG` (false positive);
- a clear violation incorrectly given `PASS` (false negative);
- a clean case sent to `HUMAN_REVIEW` (a conservative escalation, not a false flag);
- a borderline case sent to review versus forced into `PASS` or `FLAG`.

Keep keyword baseline and AI results tied to the same cases. The keyword baseline is measured, deterministic, and costs US$0 per script. For the AI, report provider/model, token usage, pricing date and source, estimated cost per script, structured-output rate, and the fact that estimated usage is not an invoice. Do not invent latency or reviewer-time savings.

## Preserve the audit trail

- Do not edit frozen case labels, manifests, prompt-run outputs, or past scores to improve reported performance.
- Link the [later 11-case adjudication](../reports/boundary_case_adjudication_v1.md), which proposes three primary and one extension overall label changes plus an added rule ID. Any incorporation needs a separately versioned dataset, a new checksum, and separately recomputed results.
- Keep the [retrospective sensitivity analysis](../reports/label_adjudication_sensitivity_v1.md) separate from the headline results. All four proposed overall changes match predictions already observed from the AI, and the hypothetical labels break the balanced splits. Do not present the resulting 30/30 as independent accuracy.
- Describe the extension peer review as one reviewer return with unknown identity/experience; 70% raw agreement is not verified inter-rater reliability.
- Keep fictional examples clearly labeled as synthetic. They are not creator submissions or confidential campaign scripts.
- Run code checks and the no-call demo before submission; never expose API credentials.

## Future work, outside this submission

After the course submission, a permissioned set of real creator drafts could test whether the synthetic examples resemble actual reviewer work. That would require appropriate consent, data handling, independent annotation, adjudication, and a new untouched test set. Public advertising-regulator decisions could be a separate study under their own jurisdiction-specific rules; they must not be relabeled as CHANEL cases. Neither effort is required for the current submission or should be mixed into its reported scores.
