# PE6201 Course Project readiness checklist

This checklist maps the current project artifacts to the four criteria in the instructor's Project Proposal Watchouts. The Course Project page in NTU Learn currently has no written submission instructions, so this is a preparation map, not a claim about the required upload format.

| Course criterion | Weight in Watchouts | Evidence in this project | Remaining check |
|---|---:|---|---|
| Problem Statement & Significance | 15% | `reports/course_report_draft.md` sections 1–2; `scope.md`; problem-statement template was previously submitted as a milestone | Confirm whether the final portal expects an updated problem statement as a separate file |
| Business & Technical Trade-offs | 25% | Report section 3; measured Ctrl+F-style keyword baseline; estimated API cost; build-versus-rent choice; human-review workflow | Check actual provider billing and keep the two-call versus one-call trade-off explicit |
| Implementation — code & repository | 35% | `src/`, `tests/`, a primary balanced 30-case set plus a separately reported 30-case extension, frozen manifests, saved AI and baseline results, README run instructions | Run tests on a clean environment; inspect secrets, ignored files, and repository history before any public release |
| Demonstration & Communication | 25% | `reports/demo_script.md`; saved `HOLDOUT-03` AI and baseline results; README quick start | Record the demo; show both methods and limitations without exposing credentials or making an unapproved API call |

## Current evidence and caveats

- The primary course evaluation uses 30 fictional English script cases, balanced across 10 `PASS`, 10 `FLAG`, and 10 `HUMAN_REVIEW`. A separate blind-reviewed extension adds another 30 cases.
- On the primary set, the revised AI scored 27/30 (90.0%) and the measured keyword baseline scored 24/30 (80.0%) against the original frozen labels. The prompt was revised after an earlier run. A later [rule-by-rule adjudication](../reports/boundary_case_adjudication_v1.md) proposes label changes; the original scores have not been recalculated. Report them as historical development evidence on synthetic cases.
- The extension scored 23/30 (76.7%) for AI and 20/30 (66.7%) for the keyword baseline. Report it as supplementary development evidence, not as a combined headline score or real-world benchmark. The reviewer did not provide identity or experience, so raw agreement is not verified inter-rater reliability.
- Keep the submission focused on CHANEL's public guidelines. A real-world dataset under another policy, such as a regulator's rulings, is future work and is not part of the current product or reported evaluation.
- The prototype's single-script command has a no-call default and requires explicit flags before a paid request. The saved results can be used for a demo without spending more API credit.
- Estimated usage cost is not an invoice. The creator-guild source page may change, and the prototype cannot inspect finished video or audio.
- The blind-review return is documented, but reviewer identity and relevant experience were not supplied; do not call the agreement score verified inter-rater reliability.

## Finalization sequence

1. Re-run `python -m unittest discover -s tests -v` and the no-call command `python -m src.review_one examples/review_case.json`.
2. Record the demo from the saved outputs and follow `reports/demo_script.md`.
3. Check the OpenRouter usage dashboard and replace estimates only if an actual billed amount is visible.
4. Ask the instructor or check a later NTU Learn update for the final upload format and whether the self-appraisal form is required. The current Course Project page does not answer either question.
5. Before changing the repository visibility, scan the complete Git history and working files for keys, private blind-ID mappings, and materials the reviewer did not consent to publish.

The repository is intentionally still private while those checks remain open.
