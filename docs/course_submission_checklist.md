# PE6201 Course Project readiness checklist

This checklist maps the current project artifacts to the four criteria in the instructor's Project Proposal Watchouts. The Course Project page in NTU Learn currently has no written submission instructions, so this is a preparation map, not a claim about the required upload format.

| Course criterion | Weight in Watchouts | Evidence in this project | Remaining check |
|---|---:|---|---|
| Problem Statement & Significance | 15% | `reports/course_report_draft.md` sections 1–2; `scope.md`; problem-statement template was previously submitted as a milestone | Confirm whether the final portal expects an updated problem statement as a separate file |
| Business & Technical Trade-offs | 25% | Report section 3; measured Ctrl+F-style keyword baseline; estimated API cost; build-versus-rent choice; human-review workflow | Check actual provider billing and keep the two-call versus one-call trade-off explicit |
| Implementation — code & repository | 35% | `src/`, `tests/`, 60 balanced synthetic cases, frozen manifests, saved AI and baseline results, README run instructions | Run tests on a clean environment; inspect secrets, ignored files, and repository history before any public release |
| Demonstration & Communication | 25% | `reports/demo_script.md`; saved `HOLDOUT-03` AI and baseline results; README quick start | Record the demo; show both methods and limitations without exposing credentials or making an unapproved API call |

## Current evidence and caveats

- The dataset has 60 fictional English script cases: 30 original development cases and a separately frozen, blind-reviewed 30-case extension.
- On the extension, the AI reviewer scored 23/30 (76.7%) and the deterministic keyword baseline scored 20/30 (66.7%). The prompt had been revised after earlier results, so this is a prompt-locked development check, not a final independent benchmark.
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
