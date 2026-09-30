# CHANEL Sponsored-Script Brand-Rule Checker

**PE6201 project report — working draft**  
**Student:** Liu Weiqi  
**Evidence date:** 30 September 2026

## 1. Problem statement

Brand and creator-partnership reviewers must check sponsored short-form video scripts against creator-facing brand rules. A keyword search can find literal phrases, but it can miss meaning expressed through slang, metaphor, or context. An AI reviewer may interpret context, but it can also over-escalate acceptable content or miss a violation. This project builds and evaluates a human-in-the-loop prototype that compares a deterministic keyword-search baseline with an AI-assisted reviewer on the same small, controlled set of scripts.

The prototype is designed to help a reviewer find evidence and decide what needs attention. A single-script command accepts a label-free JSON input and returns a structured review; the batch evaluator runs the same reviewer over frozen cases. It does not make final approval decisions.

**Dataset note:** The repository contains a 60-case dataset: the original 30-case development set and a separately blind-reviewed, frozen 30-case extension. Both systems have now been evaluated on the extension. Because the prompt was revised after earlier outputs were inspected, the extension result is reported as a prompt-locked development check, not a final independent benchmark.

## 2. User, scope, and source

The primary user is a brand partnerships/content-policy reviewer at a luxury beauty company, checking a creator's proposed English caption and spoken script before publication. This is a hypothesis about the user, not a persona validated through interviews. The reviewer already has the brand rules but needs to locate relevant wording and decide what needs checking. The project is an independent academic prototype and is not affiliated with or approved by CHANEL. Its source is CHANEL's publicly available [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), accessed on 29 September 2026.

An existing workflow product is [Aspire's creator-content approval feature](https://www.aspire.io/content-creation): its vendor documentation describes content approval, reviewer comments, change requests, and approval before creators post ([review workflow](https://help.aspireiq.com/en/articles/10370759-reviewing-content-in-group-review-as-a-content-approver)). This is a broader campaign workflow, not evidence that Aspire lacks rule analysis. My prototype is narrower: it checks submitted text against a small rule map and returns quoted evidence and a proposed disposition. It does not manage creator campaigns, review full video/audio, or communicate revisions to creators. The measured Ctrl+F-style keyword baseline is the non-AI comparator. I have not measured how many scripts a real team handles or its current review time, so I make no claim about industry-wide time savings.

The prototype checks disclosure wording and sponsor identity, disclosure placement represented in structured text fields, and whether criticism of a competitor could be presented as impartial. It can route unsupported factual or first-hand product claims to human review. It cannot inspect finished video or audio, verify on-screen visibility or spoken audibility, access private campaign briefs, or confirm unpublished selling points. The official guide may change after the recorded access date.

## 3. Design and business/technical trade-offs

The workflow separates deterministic evidence checks from policy judgement. Level 1 checks the structured input and gathers candidate evidence. Level 2 applies the source-grounded rubric and returns `PASS`, `FLAG`, or `HUMAN_REVIEW`, with a rule ID, quoted evidence, and rationale. The AI output is constrained to a structured schema. Ambiguous cases remain with a person.

The keyword baseline is cheap, reproducible, and easy to explain, but depends on patterns chosen in advance and is weak on paraphrase and context. The AI reviewer can interpret more varied wording, but introduces API cost, latency, nondeterminism, and the risk of unsupported interpretation. Human review reduces the risk of treating uncertain cases as automatic approvals, but consumes reviewer time. The selected design therefore uses AI as decision support and escalation, not as an autonomous gate.

The build-versus-buy choice is deliberately hybrid: I own the command-line interface, Python orchestration, rule mapping, synthetic cases, and evaluation code; I rent the `openai/gpt-6-sol` foundation model through OpenRouter. I do not use RAG because the selected rule set is short enough to pass directly in the prompt, and I do not fine-tune because 60 synthetic cases are not a suitable training corpus. I went directly to code rather than trialling a low-code builder because this experiment needs repeatable dataset validation, hiding gold labels, schema checks, and controlled cost accounting; I did not test a low-code tool. The API estimate is US$0.00792 per case on the new 30-case extension. Development time-to-deploy and current reviewer labor are not measured, so a business ROI cannot yet be calculated.

The current smallest working path accepts one structured script, makes two sequential model calls (evidence extraction, then rule-based decision), and returns one structured review. This separation supports evidence traceability, but it does not meet the Watchouts document's literal one-model-call version of the smallest first slice. It also doubles call count relative to a one-call design. I retain it in this evaluation because the instructor's interim feedback endorsed keeping evidence assertions separate from policy judgement; the extra call and its cost remain a design trade-off to discuss.

The AI experiment used OpenRouter with `openai/gpt-6-sol`. The revised run processed 30 cases with 36,590 input tokens and 14,058 output tokens. At the recorded rates, estimated usage cost was US$0.213760 total, or about US$0.00713 per case. The provider dashboard should be checked for actual billed cost; an interrupted request may not appear in the saved token totals. This figure excludes human-review labor and production overhead.

The holdout AI run used the same provider and model and processed 30 cases with 38,229 input tokens and 16,102 output tokens. Estimated usage cost was US$0.237478 total, or about US$0.00792 per case. The evaluator returned valid structured output for all 30 cases. The provider dashboard should be checked for actual billed cost; this estimate excludes human-review labor and production overhead.

## 4. Evaluation method

The dataset contains 60 synthetic English cases: 30 development cases and a separately blind-reviewed, frozen 30-case extension, each balanced across `PASS`, `FLAG`, and `HUMAN_REVIEW`. These are constructed examples, not collected creator submissions; the case set is project-authored, and no personal data is included. I did not implement a deterministic case-generation script, so the dataset is not claimed to be reproducible from a generator. The original labels and extension adjudications are preserved with versioned files and manifests. A reviewer supplied 30 extension labels, but did not provide identity or relevant experience; the reported 70% initial agreement is therefore not verified inter-annotator reliability. The extension was built after the original evaluation, so it is a useful separate set but not independent evidence about real-world generalisation. `ground_truth` and dataset-split fields are removed from the model payload; automated tests verify both exclusions. I did not run a deliberately leaked-label score because the production path is designed to prevent that leak.

The public guideline page is the source for the rule map; the scripts themselves are synthetic. The prototype does not collect from people or use private campaign materials. Because I did not collect actual creator data, this evaluation does not establish performance on real submissions. A small number of real, permissioned cases would be needed to validate whether the synthetic examples reflect actual reviewer language.

The revised prompt was created after inspecting the initial AI run. Therefore the 90.0% result is development evidence, not an independent estimate of generalization. The cases are synthetic, the sample is small, and several cases probe judgment boundaries. A fresh held-out set is needed for an independent performance claim.

## 5. Results

| Method | Correct | Accuracy | Clear violations flagged | Clean cases incorrectly flagged | Clean cases sent to human review | Borderline cases sent to human review |
|---|---:|---:|---:|---:|---:|---:|
| Original development — keyword baseline | 24/30 | 80.0% | 10/10 | 0 | 1 | 5/10 |
| Original development — initial AI prompt | 26/30 | 86.7% | 10/10 | 0 | 3 | 9/10 |
| Original development — revised AI prompt v1 | 27/30 | 90.0% | 10/10 | 0 | 2 | 9/10 |
| New extension — keyword baseline | 20/30 | 66.7% | 9/10 | 2 | 0 | 3/10 |
| New extension — AI reviewer v1 | 23/30 | 76.7% | 10/10 | 0 | 2 | 5/10 |

For the revised AI run, the confusion matrix below uses the human-adjudicated frozen labels as rows and system predictions as columns.

| Gold label \ Prediction | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 10 | 0 | 0 |
| HUMAN_REVIEW | 0 | 9 | 1 |
| PASS | 0 | 2 | 8 |

The revised AI did not mark any of the 10 clear violations safe (`FLAG` recall 10/10 on this set), and it did not issue a `FLAG` on any clean case. It sent 2 of 10 clean cases to human review, which is a conservative escalation rather than a false `FLAG`. It escalated 9 of 10 borderline cases. The keyword baseline also flagged all 10 clear violations, but had lower overall accuracy because of errors on other classes.

On the new frozen extension, the keyword baseline scored 20/30 (66.7%): it flagged 9/10 clear violations, incorrectly flagged 2/10 clean cases, and escalated 3/10 borderline cases. The AI reviewer scored 23/30 (76.7%): it flagged all 10 clear violations, marked no clean case `FLAG`, sent 2/10 clean cases and 5/10 borderline cases to human review, and produced valid structured output in all 30 cases. Both systems were correct on 15 cases; AI alone was correct on 8, the baseline alone on 5, and both were wrong on 2. The net difference is three additional correct cases for AI on this set. See [the holdout evaluation](holdout_keyword_baseline_results.md) and the raw [AI summary](ai_evaluation_extension_v2_summary.json).

The AI run summary is explicitly marked `DRAFT_DATASET_DEVELOPMENT_RUN`: the prompt was revised after inspecting the earlier development outputs. The extension was held out from those model calls and the prompt was not changed during this run, so these are useful results on new cases, but the small synthetic set and prompt/data development history mean they are not a final independent estimate of real-world performance.

For the AI, `HUMAN_REVIEW` is the abstention outcome: it occurred on 7/30 scripts (23.3%). Of the 10 gold borderline cases, 5 were escalated; 2 clean scripts were also escalated. The other five borderline cases received a definitive verdict, including four `FLAG` outcomes and one `PASS`. These counts show both how often the system abstains and which gold classes it abstains on; they do not reveal the counterfactual answer the model would have given without the abstention. No success threshold was registered before this run. For a future, newly sourced and independently labeled set, I propose setting guardrails in advance: at least 9/10 clear violations flagged, no more than 1/10 clean cases falsely flagged, and at least 7/10 borderline cases routed to human review. These are prospective targets, not targets this run was designed to meet.

On the original development set, the revised AI was correct where the keyword baseline was wrong on 5 cases; the baseline was correct where the AI was wrong on 2; both were wrong on 1; and both were correct on 22. The net difference is three additional correct cases for the revised AI on that set. On the new extension, the case-by-case comparison is reported above. With only 30 synthetic cases in either set, these results are descriptive, not statistically reliable evidence that AI is generally superior.

## 6. Error analysis and label uncertainty

The revised AI's remaining disagreements were `REVIEW-03`, `REVIEW-08`, and `REVIEW-10`. The blind targeted reviewer agreed with `HUMAN_REVIEW` for `REVIEW-03`, where both systems had predicted `PASS`. For `REVIEW-08` and `REVIEW-10`, the reviewer and revised AI both chose `HUMAN_REVIEW`, while frozen v2 says `PASS`. Both cases concern an identifiable competitor formula whose actual use is unknown. This reveals a possible inconsistency in how the first-hand-use rule was applied in the gold labels.

The frozen v2 dataset and reported scores have not been changed. The targeted reviewer’s identity/provenance was not supplied, so this response is recorded as reviewer input but is not claimed as verified independent peer review. Any new label version requires documented project-owner adjudication; scores must then be recomputed and shown separately rather than silently replacing the frozen result.

## 7. Limitations and next evaluation

The evaluation uses only 30 synthetic English cases from a narrow interpretation of one public guide. It does not show performance on real creator submissions, other brands, languages, visual content, or audio. The prompt was revised after seeing initial errors, so the extension run is development evidence, not a final independent benchmark. The labels for two original-set cases may need formal adjudication. Estimated token cost is not a substitute for checking the provider invoice, and no latency distribution was captured.

| Risk or failure mode | Current mitigation | Residual limitation |
|---|---|---|
| A clear rule violation is silently marked safe | Human-adjudicated cases, per-class confusion matrices, and a `HUMAN_REVIEW` outcome; tests ensure labels are withheld from model input | A small synthetic set cannot establish production miss rates; HOLDOUT-26 shows a borderline case can still be passed |
| A borderline or clean script is unnecessarily flagged or escalated | Keep `FLAG` distinct from `HUMAN_REVIEW`; report clean escalations and borderline routing separately | On this extension, four borderline cases were flagged and two clean cases escalated |
| The script looks compliant but the finished video's disclosure is inaudible or unreadable | State that the tool only reviews structured text; require a human to inspect final video and audio | The prototype cannot evaluate timing, legibility, or audibility |
| Unsupported product claims are treated as proven facts | Ask for evidence and route unsubstantiated claims to human review rather than asserting that they are false | The tool cannot independently verify a claim without authoritative source material |
| Users over-trust a confident model verdict | Show quoted evidence and rule IDs, preserve human approval, and expose false-negative and escalation metrics | There is no production monitoring or real-world reviewer study |

The human-review design is consistent with the human-involvement and operations-management themes in Singapore's [Model AI Governance Framework, second edition](https://www.pdpc.gov.sg/-/media/files/pdpc/pdf-files/resource-for-organisation/ai/sgmodelaigovframework2.pdf). This is a governance reference for the design, not a claim of certification or legal compliance.

The extension evaluation is complete and the prompt should stay locked while these results are reported. Stronger future evidence requires a newly sourced and independently labeled test set. Also record actual API billing and latency, and report per-class precision/recall and reviewer workload where the dataset supports them. The interface should continue to show evidence and uncertainty so the human reviewer can challenge the model.

## 8. Current submission status

The prototype, source-grounded rule notes, original 30-case development evaluation, separately frozen 30-case extension evaluation, and combined 60-case dataset are present in the project folder and private GitHub repository. The new single-script command provides a user-facing entry point with a no-call default; a paid review requires explicit flags and a conservative cost ceiling. The NTU Learn Course Project page shows a 4 October 2026, 23:59 SGT deadline, 100 points, unlimited attempts, and one earlier attempt submitted on 23 August containing `PE6201_Project_Problem_Statement_LWQ.docx`; its assignment instructions currently say “No instructions added.” The separate A1 assignment folder contains `PE6201_A1_Self_Appraisal.docx`, but the Course Project page does not say that it is required for the final submission. The final file format and exact submission bundle therefore remain unconfirmed. Remaining work is to finalize this report, record the demo, check actual API billing, confirm the final upload format, rerun checks, and complete a final repository review. The repository should not be made public until secrets, history, attribution, and user-approved readiness have been checked. See the [submission-readiness checklist](../docs/course_submission_checklist.md).
