# CHANEL Sponsorship Script Brand-Rule Checker

An English-only course-project prototype that helps a human reviewer check a proposed sponsored-video script against CHANEL's publicly available creator guidelines. It compares an actually measured keyword-search baseline with an AI-assisted reviewer and routes ambiguous cases to a person.

## Scope

The MVP focuses on disclosure wording and sponsor identity, placement represented in structured script fields, and contextual competitor criticism. It does not claim to know CHANEL's private campaign brief or required selling points. See [scope](scope.md), [decisions](decisions.md), [evaluation plan](plan.md), and [brand-source assessment](docs/brand_source_research.md).

## Evaluation

The project dataset now has 60 English-language instances: 20 `PASS`, 20 `FLAG`, and 20 `HUMAN_REVIEW`, split into the original 30-case development set and a new 30-case holdout. The original frozen v2 scores remain unchanged: keyword baseline 24/30 (80.0%), initial AI prompt 26/30 (86.7%), and revised development prompt 27/30 (90.0%) at an estimated US$0.213760. The measured keyword baseline scored 20/30 (66.7%) on the new holdout; the AI holdout run is pending. See [the original-run analysis](reports/ai_evaluation_prompt_v1_results.md), [holdout baseline analysis](reports/holdout_keyword_baseline_results.md), [combined data](data/combined_cases_v3_60.jsonl), and [extension adjudication report](reports/extension_peer_review_adjudication_v1.md). The revised prompt was shaped after reviewing initial errors, so its original score is development evidence, not a held-out test. Reviewer identity was not provided, and two original-set label questions remain documented; all cases are synthetic and results are limited to this prototype.

A separate, balanced 30-case extension was blind-reviewed and adjudicated. Initial reviewer agreement with draft labels was 21/30 (70.0%); after two documented label changes, agreement with the reviewer is 22/30 (73.3%). The extension is frozen as a new version. Its measured keyword baseline scored 20/30 (66.7%); the AI holdout run is pending. Report its holdout score separately from the original development-set result. See the [blind review and adjudication report](reports/extension_peer_review_adjudication_v1.md), [holdout baseline analysis](reports/holdout_keyword_baseline_results.md), [frozen extension data](data/extension_cases_v2.jsonl), and [60-case combined data](data/combined_cases_v3_60.jsonl). The private blind-ID mapping is not included.

## Blind review and AI-run safety

The latest blind-label round used [review instructions](data/peer_review_instructions.md) and [blind packet v2](data/peer_review_packet_v2.md). Historical packets and comparisons remain in the repository for audit context. Reviewer identity/provenance was not supplied, so the returns are not presented as verified independent reliability evidence.

For the remaining rule-scope questions, use the separate [targeted policy-calibration packet](data/targeted_adjudication_packet_v1.md). Share that file only; keep the private ID mapping in `work/targeted_adjudication_mapping_v1.json` out of the reviewer's copy.

The received response and proposed label treatment are recorded in [the targeted adjudication return](reports/targeted_adjudication_return_v1.md). The frozen v2 labels and scores remain unchanged pending project-owner sign-off.

The current [course report draft](reports/course_report_draft.md) consolidates the problem, trade-offs, evaluation, results, and limitations.

The AI reviewer uses separate Level 1 evidence extraction and Level 2 policy decision calls, constrained to structured outputs. A local dry run validates the 30-case input without calling an API:

```powershell
python -m src.evaluate_ai
```

The paid run uses OpenRouter's Responses API and defaults to `openai/gpt-6-sol`. It is blocked unless the data has a matching frozen manifest, `OPENROUTER_API_KEY` is set locally, the conservative cost preflight is within the approved US$1.50 ceiling, and the command includes `--run-api --confirm-paid-run`. For compatibility with the key already configured on the user's machine, `OPENAI_API_KEY` is also accepted as a fallback name. Never commit an API key. See [AI evaluation design](docs/ai_api_design.md) for the API and cost basis.

Each prompt version writes to its own output file. If a run is interrupted, rerun with `--resume`; completed cases are preserved and only missing cases are sent. The revised prompt-v1 run has completed all 30 cases; its results are summarized in the report linked above.

## Planned course deliverables

- Problem statement and scope
- Business/technical trade-off analysis
- Reproducible code and labeled evaluation data
- Measured results, including false positives, false negatives, borderline handling, structured-output validity, and API cost per script
- Recorded demo
- Self-appraisal/cover page if required by the course instructions

## Source and use limits

The source is CHANEL's official [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), accessed 2026-09-29. The prototype is an independent academic project, not affiliated with or approved by CHANEL. It reviews text fields supplied by the user; it cannot verify actual screen visibility, spoken audibility, or video timing. It supports human review and is not legal advice.
