# OpenRouter AI evaluation analysis

Historical note: this file records the initial run and its error analysis. The complete revised-prompt run is documented in [ai_evaluation_prompt_v1_results.md](ai_evaluation_prompt_v1_results.md); that report supersedes the earlier partial-run note below.

Run date: 2026-09-30  
Dataset: frozen 30-case synthetic set (`data/primary_cases.jsonl`)  
Provider/model: OpenRouter / `openai/gpt-6-sol`  
Protocol: two API stages per case; 30/30 structured outputs; 0 request or parsing errors. This run predates prompt version `rubric-clarification-2026-09-30-v1`.

## Results

Accuracy was 26/30 (86.7%). The confusion matrix uses gold labels as rows and model predictions as columns.

| Gold \ Predicted | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 10 | 0 | 0 |
| HUMAN_REVIEW | 0 | 9 | 1 |
| PASS | 0 | 3 | 7 |

On this set, the model flagged all 10 clear violations and did not mark any clear violation safe. It raised no `FLAG` on the 10 clean cases, but escalated 3 clean cases to `HUMAN_REVIEW`. It escalated 9/10 borderline cases; `REVIEW-01` was incorrectly passed.

## Comparison with measured Ctrl+F baseline

The keyword baseline scored 24/30 (80.0%), compared with 26/30 (86.7%) for AI, a net gain of 2 cases on this set. Paired by case, AI was correct when the baseline was wrong on 5 cases (`REVIEW-03`, `REVIEW-07`, `REVIEW-11`, `REVIEW-12`, `REVIEW-13`); the baseline was correct when AI was wrong on 3 (`REVIEW-01`, `REVIEW-08`, `REVIEW-10`); both were wrong on 1 (`REVIEW-02`); both were correct on 21. This is a small descriptive comparison, not evidence of a statistically reliable or generalizable improvement.

Both methods flagged all 10 clear violations and produced zero `FLAG` decisions on clean cases. The AI escalated 9/10 borderline cases versus 5/10 for the keyword baseline, while escalating 3 clean cases to a human versus 1 for the baseline. The observed AI advantage is therefore mainly better escalation of borderline examples, with a modest increase in human-review workload.

## Disagreements and rubric alignment

- `REVIEW-01`: gold `HUMAN_REVIEW`, model `PASS` with no findings. The case was intentionally ambiguous about whether “overpriced for what you get” reads as impartial competitor criticism. The current prompt may need a clearer escalation boundary for ambiguous comparisons.
- `REVIEW-02`, `REVIEW-08`, and `REVIEW-10`: gold `PASS`, model `HUMAN_REVIEW` under `CH-CLAIM-01`, because the script did not establish first-hand use. This is not automatically an AI mistake. `REVIEW-08` and `REVIEW-10` explicitly discuss a competitor product formula; CHANEL's public guideline section 3 says product opinions should come from an actual user, and the project rulebook says opinions require first-hand use. Their `creator_used_product` field is unknown, so routing them to a person is defensible; the gold rationales address impartiality but do not resolve the separate first-hand-use rule. `REVIEW-02` refers broadly to a rival brand and does not identify a particular product, so applying a product-use rule there may be overbroad. Together these cases expose an unresolved scope boundary in the rubric.

Do not change gold labels solely to improve the score. First decide whether subjective negative comparisons about competitor products are in scope for `CH-CLAIM-01`, whether brand-level comparisons are in scope, and what an unknown product-use field means. Keep the current run and frozen labels intact as the recorded result. If labels or prompts change, version the rubric and use a new holdout set for the next evaluation.

## Cost and limitations

Reported usage was 31,059 input tokens and 14,026 output tokens. Estimated cost was US$0.202378 total (US$0.00674593 per script), against a preflight estimate of US$1.081488 and an authorized ceiling of US$1.50. Cost is an estimate calculated from the dated rate snapshot; check OpenRouter's usage page for the billed amount.

These results describe one model, one prompt/rubric version, and a small synthetic set authored for this project. The 86.7% figure is not evidence of performance on real creator content or on CHANEL's private campaign rules. Report the per-class outcomes and limitations alongside accuracy. The prior direct-OpenAI authentication failure is documented separately in `ai_evaluation_auth_failure.md` and is not part of this evaluation. The relevant primary-source wording is in CHANEL's [Social Media Guidelines, sections 1 and 3](https://www.chanel.com/us/makeup/social-media-guidelines/).

## Revised development prompt results

The following partial-run figures describe the interruption before resume only; they are superseded by the complete 30-case results in [ai_evaluation_prompt_v1_results.md](ai_evaluation_prompt_v1_results.md).

The Level 2 prompt now has a versioned clarification, `rubric-clarification-2026-09-30-v1`. It treats ambiguous impartiality wording as `HUMAN_REVIEW`, limits first-hand-use checks to identifiable products/services, routes unknown use for those items to a person, and evaluates context and claim rules independently. After a pause during case 26 and a successful resume, all 30 cases have outputs with no API or parsing errors. The revised prompt achieved 27/30 (90.0%), compared with 26/30 (86.7%) for the initial prompt and 24/30 (80.0%) for the measured keyword baseline.

The 25 completed rows record an estimated US$0.175676. The remaining five cases have a preflight estimate of US$0.190476. The interrupted `REVIEW-09` stage-2 request may have generated billable usage that was not recorded; resuming will retry that case because no complete result row exists for it. Use the provider usage page for the billed total.

Since this prompt was drafted after inspecting the original v2 outputs, even a completed same-set rerun remains development evidence rather than an independent test. A fresh holdout is needed for a clean evaluation of the revised prompt.
