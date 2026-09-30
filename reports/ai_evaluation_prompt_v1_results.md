# Revised AI prompt: full development-run results

Run date: 2026-09-30  
Provider/model: OpenRouter / `openai/gpt-6-sol`  
Prompt: `rubric-clarification-2026-09-30-v1`  
Dataset: frozen v2 synthetic set, 30 cases  
Completion: 30/30 structured outputs; no API or JSON parsing errors.

## Results

Accuracy was 27/30 (90.0%). Gold labels are rows; AI predictions are columns.

| Gold \ Predicted | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 10 | 0 | 0 |
| HUMAN_REVIEW | 0 | 9 | 1 |
| PASS | 0 | 2 | 8 |

The model flagged all 10 clear violations and produced no `FLAG` for clean cases. It escalated 9/10 borderline cases and escalated 2 clean cases to a person. The remaining disagreements are `REVIEW-03` (gold `HUMAN_REVIEW`, AI `PASS`), `REVIEW-08` and `REVIEW-10` (gold `PASS`, AI `HUMAN_REVIEW`). The latter two involve opinions about a specific competitor formula with actual use unknown; the AI applied the project's first-hand-use rule. Their gold rationales address impartiality but do not resolve this separate rule, so treat these as rubric/label questions pending blinded adjudication.

## Comparison on the same 30 cases

| Method | Correct | Accuracy | Borderline escalations | Clean cases escalated to a person | Clear violations flagged |
|---|---:|---:|---:|---:|---:|
| Keyword / Ctrl+F baseline | 24/30 | 80.0% | 5/10 | 1 | 10/10 |
| Initial AI prompt | 26/30 | 86.7% | 9/10 | 3 | 10/10 |
| Revised AI prompt v1 | 27/30 | 90.0% | 9/10 | 2 | 10/10 |

Paired by case, revised AI was correct when Ctrl+F was wrong on 5 (`REVIEW-02`, `REVIEW-07`, `REVIEW-11`, `REVIEW-12`, `REVIEW-13`); Ctrl+F was correct when revised AI was wrong on 2 (`REVIEW-08`, `REVIEW-10`); both were wrong on 1 (`REVIEW-03`); both were correct on 22. This is a descriptive result on one small dataset, not a statistically reliable improvement estimate.

The prompt clarification corrected `REVIEW-01` and `REVIEW-02` from the initial run. The persistent `REVIEW-08` and `REVIEW-10` disagreement requires policy adjudication; do not change labels only to raise model accuracy.

## Cost and evidence limits

The saved run reports 36,590 input tokens and 14,058 output tokens, estimated at US$0.213760 total (US$0.00712533 per case). The resumed-run preflight upper bound was US$0.404064. Because the `REVIEW-09` stage-2 response was interrupted before a result row was saved, the provider may have billed that request without its usage being included in the summary. Check the OpenRouter usage page for the actual total.

This prompt was revised after inspecting the first run's outputs, so this is development evidence, not an independent test. The cases are synthetic and the gold labels may have unresolved scope issues. Before claiming broad performance, adjudicate `REVIEW-08`/`REVIEW-10` without showing the model verdicts, version the rubric if needed, and test the final prompt on fresh held-out cases. The archived initial summary is `ai_evaluation_initial_summary.json`; its original per-case output was overwritten by the interrupted prompt-v1 run, and the earlier error analysis is in `ai_evaluation_openrouter_analysis.md`.
