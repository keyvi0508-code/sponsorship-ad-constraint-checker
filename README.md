# CHANEL Sponsorship Script Brand-Rule Checker

An English-only course-project prototype that helps a human reviewer check a proposed sponsored-video script against CHANEL's publicly available creator guidelines. It compares an actually measured keyword-search baseline with an AI-assisted reviewer and routes ambiguous cases to a person.

## Scope

The MVP focuses on disclosure wording and sponsor identity, placement represented in structured script fields, and contextual competitor criticism. It does not claim to know CHANEL's private campaign brief or required selling points. See [scope](scope.md), [decisions](decisions.md), [evaluation plan](plan.md), and [brand-source assessment](docs/brand_source_research.md).

## Run the prototype

The project uses Python's standard library; no package installation is required. Python 3.9 or later is sufficient for the included commands.

Run the automated checks and a deterministic baseline without making network or API calls:

```powershell
python -m unittest discover -s tests -v
python -m src.evaluate_baseline data/extension_cases_v2.jsonl
```

Review one fictional script. By default, this validates the input and prints a conservative cost estimate; it does **not** call an API:

```powershell
python -m src.review_one examples/review_case.json
```

An actual single-script review sends two model requests and can incur a charge. Configure an OpenRouter API key in your local environment, review the preflight estimate, and run the following only after approving the spend:

```powershell
python -m src.review_one examples/review_case.json --run-api --confirm-paid-run
```

To save the result, add a new output path such as `--output reports/my_review.json`; existing files are never overwritten. The one-script command has a conservative default ceiling of US$0.10. See [the input schema and API design](docs/ai_api_design.md) before using a different script. Never put an API key in a project file or commit it.

## Evaluation

The project dataset has 60 English-language instances: 20 `PASS`, 20 `FLAG`, and 20 `HUMAN_REVIEW`, split into the original 30-case development set and a blind-reviewed 30-case extension. The original frozen v2 scores remain unchanged: keyword baseline 24/30 (80.0%), initial AI prompt 26/30 (86.7%), and revised development prompt 27/30 (90.0%) at an estimated US$0.213760. On the new extension, the keyword baseline scored 20/30 (66.7%) and the AI reviewer scored 23/30 (76.7%), with estimated AI token cost US$0.237478. See [the original-run analysis](reports/ai_evaluation_prompt_v1_results.md), [extension evaluation](reports/holdout_keyword_baseline_results.md), [combined data](data/combined_cases_v3_60.jsonl), and [extension adjudication report](reports/extension_peer_review_adjudication_v1.md). The revised prompt was shaped after reviewing initial errors, so report the extension as a prompt-locked development check, not a final independent benchmark. Reviewer identity was not provided, and two original-set label questions remain documented; all cases are synthetic and results are limited to this prototype.

A separate, balanced 30-case extension was blind-reviewed and adjudicated. Initial reviewer agreement with draft labels was 21/30 (70.0%); after two documented label changes, agreement with the reviewer is 22/30 (73.3%). The extension is frozen as a new version. The keyword baseline scored 20/30 (66.7%) and AI scored 23/30 (76.7%); keep these results separate from the original development-set scores. See the [blind review and adjudication report](reports/extension_peer_review_adjudication_v1.md), [extension evaluation](reports/holdout_keyword_baseline_results.md), [frozen extension data](data/extension_cases_v2.jsonl), and [60-case combined data](data/combined_cases_v3_60.jsonl). The private blind-ID mapping is not included.

## Blind review and AI-run safety

The latest blind-label round used [review instructions](data/peer_review_instructions.md) and [blind packet v2](data/peer_review_packet_v2.md). Historical packets and comparisons remain in the repository for audit context. Reviewer identity/provenance was not supplied, so the returns are not presented as verified independent reliability evidence.

For the remaining rule-scope questions, use the separate [targeted policy-calibration packet](data/targeted_adjudication_packet_v1.md). Share that file only; keep the private ID mapping in `work/targeted_adjudication_mapping_v1.json` out of the reviewer's copy.

The received response and proposed label treatment are recorded in [the targeted adjudication return](reports/targeted_adjudication_return_v1.md). The frozen v2 labels and scores remain unchanged pending project-owner sign-off.

The current [course report draft](reports/course_report_draft.md) consolidates the problem, trade-offs, evaluation, results, and limitations. See the [PE6201 submission-readiness checklist](docs/course_submission_checklist.md) for the rubric mapping and remaining course-specific checks.

The batch evaluator uses separate Level 1 evidence extraction and Level 2 policy decision calls, constrained to structured outputs. A local dry run validates the primary 30-case input without calling an API:

```powershell
python -m src.evaluate_ai
```

The batch paid run uses OpenRouter's Responses API and defaults to `openai/gpt-6-sol`. It is blocked unless the data has a matching frozen manifest, an API key is set locally, the conservative cost preflight is within the US$1.50 ceiling, and the command includes `--run-api --confirm-paid-run`. For compatibility with the key already configured on the user's machine, `OPENAI_API_KEY` is also accepted as a fallback name. Never commit an API key. See [AI evaluation design](docs/ai_api_design.md) for the API and cost basis.

Each prompt version writes to its own output file. If a run is interrupted, rerun the same command with `--resume`; completed cases are preserved and only missing cases are sent. The original development run and the extension run have both completed all 30 cases; results and their development-evidence caveat are summarized in the reports linked above.

## Planned course deliverables

- Problem statement and scope
- Business/technical trade-off analysis
- Reproducible code and labeled evaluation data
- A single-script review command with a no-call default and explicit paid-run guard
- Measured results, including false positives, false negatives, borderline handling, structured-output validity, and API cost per script
- Recorded demo (a concise [demo script](reports/demo_script.md) is prepared)
- Self-appraisal/cover page if required by the course instructions

## Source and use limits

The source is CHANEL's official [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), accessed 2026-09-29. The prototype is an independent academic project, not affiliated with or approved by CHANEL. It reviews text fields supplied by the user; it cannot verify actual screen visibility, spoken audibility, or video timing. It supports human review and is not legal advice.


For job applications, see the [portfolio positioning note](docs/portfolio_positioning.md), which describes the workbench workflow, relevant role fit, an honest interview narrative, and current product gaps.


## Interactive review workbench

Start the local interface with `python -m src.web_app`, then open `http://127.0.0.1:8765`. The saved example and keyword baseline make no API call. A live AI review displays a cost estimate and requires explicit confirmation before sending two paid model requests. The prototype does not save script drafts or reviewer decisions. See the [demo walkthrough](reports/demo_script.md) and [portfolio positioning note](docs/portfolio_positioning.md).
