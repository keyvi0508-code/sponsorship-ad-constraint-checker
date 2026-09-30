# Creator Content Review Workbench

A human-in-the-loop review tool for sponsored creator scripts. It puts a fast, explainable keyword baseline beside an AI-assisted review, surfaces quoted evidence and uncertainty, and leaves the final disposition with a reviewer.

This independent local prototype uses CHANEL's public [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/) as a narrow example rule set. It is not affiliated with or approved by CHANEL and does not represent a brand's private campaign brief.

## The review workflow

1. Add caption, spoken copy, planned on-screen text, brand context, and first-hand product-use information.
2. Run the free keyword baseline to catch literal signals.
3. Optionally request an AI-assisted review to examine context and evidence. The interface displays a cost estimate and asks for confirmation first.
4. Compare verdicts, evidence quotes, rule IDs, and rationales; route uncertain cases to a person.
5. A reviewer records the final disposition. The model does not approve content.

The current rule scope covers sponsorship disclosure, sponsor identity, disclosure placement represented in structured text fields, and potentially misleading competitor criticism.

## Try the workbench

Python 3.9 or later is required. The app uses the standard library; no package installation is needed.

    python -m src.web_app

Open http://127.0.0.1:8765. The saved example and keyword review work offline without an API call. Drafts and reviewer decisions are not saved. A live AI review sends two requests to OpenRouter and may incur a charge; it requires a local API key and explicit confirmation. Never place a key in a project file or commit it.

For a no-call command-line review and cost preflight:

    python -m src.review_one examples/review_case.json

To run the model, review the estimate and add --run-api --confirm-paid-run. The single-script tool enforces a US$0.10 ceiling and does not overwrite existing result files. See [AI request and cost design](docs/ai_api_design.md).

## Evaluation snapshot

On a balanced 30-case synthetic extension, the AI reviewer scored **23/30 (76.7%)** and the measured keyword baseline scored **20/30 (66.7%)**. The AI flagged all 10 clear violations and made no FLAG decisions on clean cases. It routed 2 clean and 5 borderline cases to HUMAN_REVIEW.

These are small-sample development results, not evidence of production performance. The prompt had been revised after earlier outputs, and all scripts are fictional. This is a prompt-locked development check, not an independent benchmark or proof of real-world lift. See the [evaluation report](reports/holdout_keyword_baseline_results.md), [adjudication notes](reports/extension_peer_review_adjudication_v1.md), and [evaluation data guide](data/README.md).

## Product boundaries

- Text-only: it cannot verify actual video visibility, spoken audibility, or timing.
- No team accounts, persistent review history, configurable rule editor, or campaign-platform integration.
- No live-video, audio, image, multimodal, or real-time moderation.
- The rules cover a narrow interpretation of public guidance; they do not establish legal compliance or private campaign requirements.
- Local demo only; it has not been security-reviewed for multi-user use.

## Run checks

    python -m unittest discover -s tests -v
    python -m src.evaluate_baseline data/extension_cases_v2.jsonl

## Project notes

- [Product positioning and interview narrative](docs/portfolio_positioning.md)
- [Product scope](scope.md) and [design decisions](decisions.md)
- [Demo walkthrough](reports/demo_script.md)
- [Source assessment](docs/brand_source_research.md)
- [Course documentation](docs/course_submission_checklist.md) and [report draft](reports/course_report_draft.md)

Course materials remain as supporting documentation; the workbench is the product being demonstrated.
