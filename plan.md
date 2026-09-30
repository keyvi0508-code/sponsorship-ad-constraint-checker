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
- [x] Blind-review the additional 30-case extension, adjudicate differences, and publish a versioned combined 60-case dataset without replacing the original frozen v2 file. Treat only the fresh extension as holdout evidence for the already-revised prompt.
- [x] Review/sign off the two-label adjudication in `reports/extension_peer_review_adjudication_v1.md`; the original and adjudicated versions remain separately recorded.

## Stage 3 — prototype

- [x] Implement deterministic keyword search with documented patterns and rule mapping.
- [x] Implement an AI reviewer using the same source-grounded rules and structured script; require schema-validated JSON.
- [x] Keep Level 1 JSON assertions separate from Level 2 policy judgement.
- [x] Add a single-script JSON entry point with schema validation, cost preflight, no-call default, explicit paid-run confirmation, and non-overwriting output.
- [x] Use PASS, FLAG, and HUMAN_REVIEW with evidence and rule IDs.
- [x] Keep API keys out of project files; capture provider/model, token usage, estimated cost, and pricing assumptions. Verify repository history and ignore rules again before public release.

## Stage 4 — evaluation and reporting

- [x] Run both systems on the same frozen 30 instances with settings recorded.
- [x] Report confusion matrices, class results, both error directions, and borderline escalation.
- [x] Report structured-output validity and estimated API cost per script and overall. Actual provider billing still needs a dashboard check; latency/median were not captured and must not be invented.
- [x] Document representative disagreements, source access date, synthetic-data limits, prompt-tuning leakage, and the unresolved gold-label question.
- [x] Measure the keyword baseline on the new holdout without tuning its patterns; it scored 20/30 (66.7%).
- [x] Run the locked revised prompt on the frozen 30-case extension and report its result separately: AI 23/30 (76.7%) versus keyword baseline 20/30 (66.7%); do not tune on these outputs and continue calling this set a holdout.

## Stage 5 — course submission and portfolio

- [ ] Finalize the problem statement and business/technical trade-off analysis using the report draft.
- [x] Prepare setup/run instructions and meaningful tests (19 tests pass in the current implementation checkpoint; rerun before final submission).
- [x] Draft a concise English demo script showing HOLDOUT-03 and the workflow; recording the video remains open.
- [x] Inspect NTU Learn's Course Project submission page: it has no written instructions; the separate A1 section lists a self-appraisal form, but the Course Project page does not state that it is required.
- [x] Map current artifacts and open items to the four criteria in `docs/course_submission_checklist.md`.
- [ ] Confirm the final upload format/bundle because the Course Project submission page has no written instructions.
- [ ] Review the repository for secrets, private material, source attribution, and polished README; confirm private GitHub sync, then make it public only after the user is ready.
