# Supplementary extension: keyword baseline and AI reviewer

**Dataset:** `extension_cases_v2.jsonl` (frozen v2)  
**Runs:** deterministic keyword baseline (no API calls) and two-stage AI reviewer via OpenRouter  
**Date:** 2026-09-30

The deterministic keyword baseline scored **20/30 (66.7%)**. The AI reviewer scored **23/30 (76.7%)**, three more correct cases on this 30-case set. The AI's estimated token cost was **US$0.237478 total** (about **US$0.00792 per case**) at the recorded rates; check the provider dashboard for actual billing. Both systems were evaluated against the same frozen labels. This is supplementary development evidence; the primary course result is reported separately on the original 30-case set.

The AI returned valid structured output for all 30 cases. Gold labels are rows and system predictions are columns.

### AI reviewer confusion matrix

| Gold \\ Prediction | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 10 | 0 | 0 |
| HUMAN_REVIEW | 4 | 5 | 1 |
| PASS | 0 | 2 | 8 |

It flagged all 10 clear violations and marked none of them `PASS`. It also issued no `FLAG` on clean cases; two clean cases were conservatively sent to human review. It sent 5/10 borderline cases to human review. Its seven disagreements were HOLDOUT-06, 07, 09, 22, 26, 27, and 30; the most consequential errors were marking HOLDOUT-26 `PASS` when its gold label is `HUMAN_REVIEW`, and escalating four borderline cases to `FLAG`.

### Per-class precision and recall

Precision and recall are calculated one class at a time against the other two classes.

| System | Class | Precision | Recall |
|---|---|---:|---:|
| AI reviewer | FLAG | 71.4% | 100.0% |
| AI reviewer | HUMAN_REVIEW | 71.4% | 50.0% |
| AI reviewer | PASS | 88.9% | 80.0% |
| Keyword baseline | FLAG | 69.2% | 90.0% |
| Keyword baseline | HUMAN_REVIEW | 100.0% | 30.0% |
| Keyword baseline | PASS | 57.1% | 80.0% |

### Keyword baseline confusion matrix

The deterministic keyword baseline scored **20/30 (66.7%)** on the balanced extension. Gold labels are rows; baseline predictions are columns.

| Gold \ Prediction | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 9 | 0 | 1 |
| HUMAN_REVIEW | 2 | 3 | 5 |
| PASS | 2 | 0 | 8 |

It flagged 9/10 clear violations and marked one violation `PASS`. It incorrectly flagged 2/10 clean cases. It escalated 3/10 borderline cases to a person; on the other 7, it chose a definitive verdict. The model was correct on 8/10 clean cases.

This is an actually measured baseline on the supplementary extension, not a result inferred from the primary 30 cases. Keep this split separate from the primary course result. The saved per-case results are in [baseline_keyword_holdout_extension_v2.json](baseline_keyword_holdout_extension_v2.json); AI per-case outputs and summary are [ai_evaluation_extension_v2.jsonl](ai_evaluation_extension_v2.jsonl) and [ai_evaluation_extension_v2_summary.json](ai_evaluation_extension_v2_summary.json).

### Case-by-case comparison

Both systems were correct on 15 cases; the AI alone was correct on 8, the keyword baseline alone on 5, and both were wrong on 2. This gives the AI a net advantage of three correct cases here, but the sample is too small to support a broad claim of superiority.

## Interpretation and limitations

The run summary labels this `DRAFT_DATASET_DEVELOPMENT_RUN` and notes that the prompt had been revised after inspecting the primary-set outputs. The extension labels were frozen before this AI run, and the prompt was not changed during it. This is a useful prompt-locked check on additional fictional cases, but it remains supplementary development evidence rather than a representative real-world benchmark. The labels also depend on one reviewer return whose identity and experience were not provided. Do not tune the prompt or keyword patterns against these results. Stronger real-world claims would require a permissioned, independently labeled set under the same CHANEL rule scope.

The run made 60 model-stage requests for 30 cases, produced 30/30 structured outputs, and recorded 38,229 input and 16,102 output tokens. Estimated cost at the recorded prices was US$0.237478; this is not a provider invoice. The raw output and summary are preserved for auditability.
