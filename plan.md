# Implementation and evaluation plan

## Stage 1 — scope and evidence

- [x] User selected CHANEL and its public creator rules.
- [x] Use English-only scripts to match the official source and avoid translation as an evaluation confound.
- [x] Capture instructor feedback as implementation and evaluation checks.
- [x] Identify the official CHANEL Social Media Guidelines page and document limitations.
- [x] Freeze a narrow rule matrix with source passages and operational interpretations.

## Stage 2 — test design before model runs

- [ ] Define a JSONL schema with case ID, language, structured script fields, ground-truth class, rule tags, and rationale.
- [ ] Author and review all 30 primary instances before running either method: 10 compliant, 10 violating, 10 borderline.
- [ ] Record why each label follows the cited guide; freeze the primary file and its checksum.
- [ ] Separate prompt-tuning/development cases from the primary set.

## Stage 3 — prototype

- [ ] Implement deterministic keyword search with a documented pattern list and rule-to-pattern mapping.
- [ ] Implement an AI reviewer that receives the same source-grounded rules and structured script; require schema-validated JSON.
- [ ] Keep Level 1 JSON assertions separate from Level 2 policy judgement.
- [ ] Use PASS, FLAG, and HUMAN_REVIEW; require a quoted evidence span and rule ID for each finding.
- [ ] Keep API keys outside GitHub; capture provider/model, token use, latency, and actual pricing assumptions.

## Stage 4 — evaluation and reporting

- [ ] Run both systems on the same frozen 30 instances with settings recorded.
- [ ] Report a 3-by-3 confusion matrix, per-class results, false-positive rate on clean cases, false-negative rate on violating cases, and borderline escalation rate.
- [ ] Report invalid-output rate, average/median cost per script, total evaluation cost, and representative failures.
- [ ] Report limitations, source access date, and that public guidelines may change.

## Stage 5 — course submission and portfolio

- [ ] Complete the problem statement and business/technical trade-off analysis.
- [ ] Prepare clear setup/run instructions and meaningful tests.
- [ ] Record a concise demo showing the workflow and a contextual case where keyword search and AI differ.
- [ ] Verify the course cover/self-appraisal requirement against NTU Learn before submission.
- [ ] Review the repository for secrets, private material, source attribution, and polished README before asking the user to make it public.
