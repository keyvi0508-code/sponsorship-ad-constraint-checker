# CHANEL Sponsored-Script Brand-Rule Checker

**PE6201 project report — working draft**  
**Student:** Liu Weiqi  
**Evidence date:** 30 September 2026

## 1. Problem statement

Brand and creator-partnership reviewers must check sponsored short-form video scripts against creator-facing brand rules. A keyword search can find literal phrases, but it can miss meaning expressed through slang, metaphor, or context. An AI reviewer may interpret context, but it can also over-escalate acceptable content or miss a violation. This project builds and evaluates a human-in-the-loop prototype that compares a deterministic keyword-search baseline with an AI-assisted reviewer on the same small, controlled set of scripts.

The prototype is designed to help a reviewer find evidence and decide what needs attention. It does not make final approval decisions.

**Dataset note:** The repository now contains a 60-case dataset: the original 30-case development set and a separate, blind-reviewed 30-case holdout extension. The results below are the original development-set scores only; the new holdout has not yet been run through either system.

## 2. User, scope, and source

The intended user is a reviewer checking an English sponsored-video script before publication. The selected source is CHANEL's publicly available [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), accessed on 29 September 2026. The project is an independent academic prototype and is not affiliated with or approved by CHANEL.

The prototype checks disclosure wording and sponsor identity, disclosure placement represented in structured text fields, and whether criticism of a competitor could be presented as impartial. It can route unsupported factual or first-hand product claims to human review. It cannot inspect finished video or audio, verify on-screen visibility or spoken audibility, access private campaign briefs, or confirm unpublished selling points. The official guide may change after the recorded access date.

## 3. Design and business/technical trade-offs

The workflow separates deterministic evidence checks from policy judgement. Level 1 checks the structured input and gathers candidate evidence. Level 2 applies the source-grounded rubric and returns `PASS`, `FLAG`, or `HUMAN_REVIEW`, with a rule ID, quoted evidence, and rationale. The AI output is constrained to a structured schema. Ambiguous cases remain with a person.

The keyword baseline is cheap, reproducible, and easy to explain, but depends on patterns chosen in advance and is weak on paraphrase and context. The AI reviewer can interpret more varied wording, but introduces API cost, latency, nondeterminism, and the risk of unsupported interpretation. Human review reduces the risk of treating uncertain cases as automatic approvals, but consumes reviewer time. The selected design therefore uses AI as decision support and escalation, not as an autonomous gate.

The AI experiment used OpenRouter with `openai/gpt-6-sol`. The revised run processed 30 cases with 36,590 input tokens and 14,058 output tokens. At the recorded rates, estimated usage cost was US$0.213760 total, or about US$0.00713 per case. The provider dashboard should be checked for actual billed cost; an interrupted request may not appear in the saved token totals. This figure excludes human-review labor and production overhead.

## 4. Evaluation method

The original frozen v2 development set contains 30 synthetic English cases: 10 labelled `PASS`, 10 `FLAG`, and 10 `HUMAN_REVIEW`. A new 30-case extension has since been blind-reviewed and frozen as a holdout, preserving 10 examples in each class. The extension labels and original development labels are combined in a versioned 60-case file, with the split recorded per case. The keyword baseline has been run on both sets; the AI reviewer has been run only on the original 30 cases so far. The reported revised AI run used prompt version `rubric-clarification-2026-09-30-v1`; it produced 30 valid structured outputs.

The revised prompt was created after inspecting the initial AI run. Therefore the 90.0% result is development evidence, not an independent estimate of generalization. The cases are synthetic, the sample is small, and several cases probe judgment boundaries. A fresh held-out set is needed for an independent performance claim.

## 5. Results

| Method | Correct | Accuracy | Clear violations flagged | Clean cases incorrectly flagged | Clean cases sent to human review | Borderline cases sent to human review |
|---|---:|---:|---:|---:|---:|---:|
| Keyword / Ctrl+F baseline | 24/30 | 80.0% | 10/10 | 0 | 1 | 5/10 |
| Initial AI prompt | 26/30 | 86.7% | 10/10 | 0 | 3 | 9/10 |
| Revised AI prompt v1 | 27/30 | 90.0% | 10/10 | 0 | 2 | 9/10 |

For the revised AI run, the confusion matrix below uses the human-adjudicated frozen labels as rows and system predictions as columns.

| Gold label \ Prediction | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 10 | 0 | 0 |
| HUMAN_REVIEW | 0 | 9 | 1 |
| PASS | 0 | 2 | 8 |

The revised AI did not mark any of the 10 clear violations safe (`FLAG` recall 10/10 on this set), and it did not issue a `FLAG` on any clean case. It sent 2 of 10 clean cases to human review, which is a conservative escalation rather than a false `FLAG`. It escalated 9 of 10 borderline cases. The keyword baseline also flagged all 10 clear violations, but had lower overall accuracy because of errors on other classes.

On the new frozen holdout, the keyword baseline scored 20/30 (66.7%): it flagged 9/10 clear violations, incorrectly flagged 2/10 clean cases, and escalated 3/10 borderline cases. The revised AI prompt has not yet been run on the holdout, so there is no AI-versus-baseline holdout comparison. See [the holdout baseline analysis](holdout_keyword_baseline_results.md).

On a case-by-case comparison, the revised AI was correct where the keyword baseline was wrong on 5 cases; the baseline was correct where the AI was wrong on 2; both were wrong on 1; and both were correct on 22. The net difference is three additional correct cases for the revised AI on this dataset. With only 30 synthetic cases, this should be treated descriptively, not as statistically reliable evidence that AI is generally superior.

## 6. Error analysis and label uncertainty

The revised AI's remaining disagreements were `REVIEW-03`, `REVIEW-08`, and `REVIEW-10`. The blind targeted reviewer agreed with `HUMAN_REVIEW` for `REVIEW-03`, where both systems had predicted `PASS`. For `REVIEW-08` and `REVIEW-10`, the reviewer and revised AI both chose `HUMAN_REVIEW`, while frozen v2 says `PASS`. Both cases concern an identifiable competitor formula whose actual use is unknown. This reveals a possible inconsistency in how the first-hand-use rule was applied in the gold labels.

The frozen v2 dataset and reported scores have not been changed. The targeted reviewer’s identity/provenance was not supplied, so this response is recorded as reviewer input but is not claimed as verified independent peer review. Any new label version requires documented project-owner adjudication; scores must then be recomputed and shown separately rather than silently replacing the frozen result.

## 7. Limitations and next evaluation

The evaluation uses only 30 synthetic English cases from a narrow interpretation of one public guide. It does not show performance on real creator submissions, other brands, languages, visual content, or audio. The prompt was revised after seeing initial errors, so prompt-v1 is not held out. The labels for two cases may need formal adjudication. Estimated token cost is not a substitute for checking the provider invoice, and no latency distribution was captured.

The next evaluation is to run the frozen 30-case holdout with the prompt locked as-is. Since the current prompt has already seen the original 30, report the fresh extension as the holdout result and the combined 60 only as a supplementary descriptive result. Also report per-class precision/recall and reviewer workload, and record actual API billing and latency. The interface should continue to show evidence and uncertainty so the human reviewer can challenge the model.

## 8. Current submission status

The prototype, source-grounded rule notes, original 30-case development evaluation, a separately frozen 30-case holdout, and the combined 60-case dataset are present in the project folder. Remaining course-facing work is to evaluate the holdout without prompt changes, update this report with those results, record a short demo, verify any cover-page or self-appraisal requirements in NTU Learn, rerun checks, and complete private GitHub synchronization and pre-publication review. The repository should not be made public until secrets, history, attribution, and user-approved readiness have been checked.
