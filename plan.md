# Implementation and evaluation plan

## Stage 1 — scope and evidence

- [x] User selected CHANEL and its public creator rules.
- [x] Use English-only scripts to match the language of the official source and avoid translation as an evaluation confound.
- [x] Capture instructor feedback as implementation and evaluation checks.
- [x] Identify the official CHANEL creator social-media-guidelines page and document limitations.
- [x] Freeze a narrow rule matrix with source passages and operational interpretations.

## Stage 2 — test design before model runs

- [x] Define a JSONL schema with case ID, language, structured script fields, ground-truth class, rule tags, and rationale.
- [x] Prepare 30 primary instances: 10 compliant, 10 violating, 10 borderline.
- [x] Record label rationales and freeze the primary file with a checksum.
- [x] Preserve the initial prompt run and revised prompt as separate development evidence. The revised prompt was informed by initial errors, so neither result is an independent held-out test.
- [ ] Resolve the two targeted reviewer disagreements in a documented new label version only if the project owner approves; keep frozen v2 and its scores intact until then.
- [x] Receive and document a targeted label-hidden review of five primary-set boundary cases in `reports/targeted_primary_adjudication_return_v2.md`; no frozen labels or scores changed because the return conflicts with the written CH-CONTEXT-01 boundary.
- [ ] If time permits, have a second reviewer independently assess a fresh copy of the five-case packet using `data/annotation_decision_guide_v3_draft.md`. Record reviewer provenance privately with permission. Do not change labels or recalculate headline metrics until the response is adjudicated; if no second review is available before submission, retain the frozen labels and report the uncertainty.
- [x] Blind-review the additional 30-case extension, adjudicate differences, and preserve a versioned combined 60-case file without replacing the original frozen v2 file. Keep the primary 30 cases and supplementary extension separate in the submission.
- [x] Review/sign off the two-label adjudication in `reports/extension_peer_review_adjudication_v1.md`; the original and adjudicated versions remain separately recorded.

## Stage 3 — prototype

- [x] Implement deterministic keyword search with documented patterns and rule mapping.
- [x] Implement an AI reviewer using the same source-grounded rules and structured script; require schema-validated JSON.
- [x] Keep Level 1 JSON assertions separate from Level 2 policy judgement.
- [x] Add a single-script JSON entry point with schema validation, cost preflight, no-call default, explicit paid-run confirmation, and non-overwriting output.
- [x] Add a local-only browser workbench with a saved no-call demo, keyword review, optional cost-confirmed AI review, and a non-persistent reviewer disposition control.
- [x] Use PASS, FLAG, and HUMAN_REVIEW with evidence and rule IDs.
- [x] Keep API keys out of project files; capture provider/model, token usage, estimated cost, and pricing assumptions. Verify repository history and ignore rules again before public release.

## Stage 4 — evaluation and reporting

- [x] Run both systems on the same frozen 30 instances with settings recorded.
- [x] Report confusion matrices, class results, both error directions, and borderline escalation.
- [x] Report structured-output validity and estimated API cost per script and overall. Actual provider billing still needs a dashboard check; latency/median were not captured and must not be invented.
- [x] Document representative disagreements, source access date, synthetic-data limits, prompt-tuning leakage, and the unresolved gold-label question.
- [x] Measure the keyword baseline on the supplementary extension without tuning its patterns; it scored 20/30 (66.7%).
- [x] Run the revised prompt on the frozen 30-case extension and report it separately: AI 23/30 (76.7%) versus keyword baseline 20/30 (66.7%). Describe it as supplementary development evidence, not as a real-world or representative benchmark.
- [x] Keep this submission focused on the single CHANEL public-guideline ruleset. Place permissioned creator drafts or regulator cases only under future work; do not add another policy/data track to the current evaluation.

## Stage 5 — course submission and portfolio

- [ ] Finalize the problem statement and business/technical trade-off analysis using the report draft.
- [x] Prepare setup/run instructions and meaningful tests (30 tests passed on 2026-09-30; rerun before final submission).
- [x] Draft a concise English demo script showing HOLDOUT-03 and the workflow; recording the video remains open.
- [x] Inspect NTU Learn's Course Project submission page: it has no written instructions; the separate A1 section lists a self-appraisal form, but the Course Project page does not state that it is required.
- [x] Map current artifacts and open items to the four criteria in `docs/course_submission_checklist.md`.
- [ ] Confirm the final upload format/bundle because the Course Project submission page has no written instructions.
- [ ] Review the repository for secrets, private material, source attribution, and polished README; confirm private GitHub sync, then make it public only after the user is ready.
