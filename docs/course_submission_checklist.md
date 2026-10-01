# PE6201 Course Project readiness checklist

This checklist maps the project to the four rubric weights cited in the instructor's Project Proposal Watchouts and to the **1 October 2026 NTU Learn announcement** clarifying final deliverables. It is a preparation map; check the final upload controls in NTU Learn before submitting.

| Course criterion | Weight in Watchouts | Evidence in this project | Remaining check |
|---|---:|---|---|
| Problem Statement & Significance | 15% | Final report's user and scope; [`product_overview.md`](product_overview.md) persona and input/output | Real reviewer volume, review time, and business pain remain unmeasured; state that plainly |
| Business & Technical Trade-offs | 25% | Measured keyword baseline; saved token cost and wait; two-call choice; human final decision | Explain that a one-call alternative and reviewer labour cost were not measured |
| Implementation — code & repository | 35% | `src/`, `tests/`, balanced primary and extension data, frozen manifests, saved results, [`data/README.md`](../data/README.md), [`reports/README.md`](../reports/README.md), and README run instructions | Check a fresh run and make the source accessible to the marker |
| Demonstration & Communication | 25% | Final report; [`demo_script.md`](../reports/demo_script.md); saved no-call example and reviewer export | Record and upload the face-plus-screen demo; speak to limits and uncertainty |

## Current evidence and caveats

- The primary course evaluation uses 30 fictional English script cases, balanced across 10 `PASS`, 10 `FLAG`, and 10 `HUMAN_REVIEW`. A separate blind-reviewed extension adds another 30 cases.
- On the primary set, the revised AI scored 27/30 (90.0%) and the measured keyword baseline scored 24/30 (80.0%) against the original frozen labels. The prompt was revised after an earlier run. A later [rule-by-rule adjudication](../reports/boundary_case_adjudication_v1.md) proposes label changes; the original scores have not been recalculated. Report them as historical development evidence on synthetic cases.
- The extension scored 23/30 (76.7%) for AI and 20/30 (66.7%) for the keyword baseline. Report it as supplementary development evidence, not as a combined headline score or real-world benchmark. The reviewer did not provide identity or experience, so raw agreement is not verified inter-rater reliability.
- Keep the submission focused on CHANEL's public guidelines. A real-world dataset under another policy, such as a regulator's rulings, is future work and is not part of the current product or reported evaluation.
- The prototype's single-script command has a no-call default and requires explicit flags before a paid request. The saved results can be used for a demo without spending more API credit.
- Estimated usage cost is not an invoice. The creator-guild source page may change, and the prototype cannot inspect finished video or audio.
- The blind-review return is documented, but reviewer identity and relevant experience were not supplied; do not call the agreement score verified inter-rater reliability.

## Finalization sequence

1. Deliver a well-structured report near **1,200 words** (about 1,020–1,380 allowed), including outcome, reasoning, performance and eval critique, difficulties, tuning, and rough edges. Submission copies are available as [Word](PE6201_Creator_Content_Review_Workbench_Report.docx) and [PDF](PE6201_Creator_Content_Review_Workbench_Report.pdf); also upload the requested format directly in NTU Learn.
2. Record and upload a **2–8 minute video**, aiming near five minutes, with the presenter’s face and computer/mobile screen visible together. Content after eight minutes may not be watched.
3. Keep case files, evaluation code, saved outputs, data and evaluation explainers, persona, input/output, architecture box diagram, and observed-versus-prospective metrics in the repository.
4. Re-run `python -m unittest discover -s tests -v` and `python -m src.review_one examples/review_case.json`; both are no-call checks. Verify that the marker can access the repository or include a source archive.
5. Check the final NTU Learn upload controls and ensure the report, video, data/evals, and code are actually checked in before **4 October 2026, 23:59 Singapore time**.
6. Before changing repository visibility, scan complete history and working files for keys, blind-ID mappings, and materials the reviewer did not consent to publish. The repository is intentionally private until this review is complete.

The 1 October announcement does not itself specify whether final files must be uploaded separately, linked, or zipped. Confirm this in the Course Project submission UI.
