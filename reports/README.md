# Evaluation guide

This directory retains measured keyword and AI results, prompt-development history, peer-review returns, and label-adjudication notes. The two 30-case splits must be read separately. The 60-case combined file is a convenience for inspection, **not** a new independent benchmark or a pooled headline score.

The [public-Reel feasibility pilot](real_public_reels_pilot_v1.md) uses ten real source-linked posts. It records caption-level observations only, has no full-video verdicts, and is **not** part of either scored split. Its counts can be checked with `python scripts/summarize_real_pilot.py`.

The later [23-post real-caption development pilot](public_caption_ai_pilot_v1.md) locks original-post caption text from four discovery routes before method review. Keyword suggestions were 11 `PASS`, 4 `HUMAN_REVIEW`, 8 `UNKNOWN`; AI suggestions were 5, 14, 4. The methods disagreed on 14 posts. Full-video status is `UNKNOWN` for all 23. The [case-level AI output](public_caption_ai_v1.jsonl), [cost and usage summary](public_caption_ai_v1_summary.json), [saved-output audit](public_caption_pilot_analysis_v1.json), and [coded disagreement analysis](public_caption_disagreement_audit_v1.md) are retained. `python scripts/summarize_public_caption_disagreements.py` validates the category counts against the saved outputs. These are descriptive suggestions, **not** compliance labels or accuracy results.

## What was evaluated

| Split | Cases and reference labels | Keyword result | AI result and summary | Status |
|---|---|---|---|---|
| Primary | [`primary_cases.jsonl`](../data/primary_cases.jsonl), [`frozen_manifest.json`](../data/frozen_manifest.json) | [`baseline_keyword_frozen.json`](baseline_keyword_frozen.json) | [`ai_evaluation_rubric-clarification-2026-09-30-v1.jsonl`](ai_evaluation_rubric-clarification-2026-09-30-v1.jsonl), [summary](ai_evaluation_rubric-clarification-2026-09-30-v1_summary.json) | Prompt was revised after earlier primary-set outputs; development evidence. |
| Extension | [`extension_cases_v2.jsonl`](../data/extension_cases_v2.jsonl), [`extension_frozen_manifest_v2.json`](../data/extension_frozen_manifest_v2.json) | [`baseline_keyword_holdout_extension_v2.json`](baseline_keyword_holdout_extension_v2.json) | [`ai_evaluation_extension_v2.jsonl`](ai_evaluation_extension_v2.jsonl), [summary](ai_evaluation_extension_v2_summary.json) | Revised prompt held fixed; supplementary synthetic development check, not real-world validation. |

The frozen case files each contain ten `PASS`, ten `FLAG`, and ten `HUMAN_REVIEW` labels. The model request now uses an explicit input allowlist. The [offline leakage audit](model_input_leakage_audit_v1.md) confirms no private fields in either stage across all 60 saved cases, including a stress check with newly named label fields. We did **not** perform a deliberately leaked-input before/after score experiment; feeding the answer to a model would contaminate that score. [`data/README.md`](../data/README.md) explains case construction, label history, and what the blind-review return can and cannot establish.

Run `python scripts/verify_synthetic_dataset.py` to check all frozen dataset hashes, class balance, split order, and the combined-file derivation. The [provenance note](../data/synthetic_data_provenance.md) explains why this reproduces the evaluated files but not the original authoring process; no historical generator prompt was retained. A newly generated, separately versioned 30-case [prospective fixture](../data/prospective_synthetic_fixture_v1.jsonl) has a real [construction script](../scripts/generate_prospective_cases.py) and exact-byte `--check` path. It is unreviewed and unscored, and does not change any result above.

The [single-stage ablation protocol](single_stage_ablation_protocol_v1.md) locked a one-call alternative before its paid run. The [measured retrospective comparison](single_stage_ablation_results_v1.md) found 22/30 exact verdict matches for one stage versus 23/30 for the saved two-stage run, with one `FLAG` case marked `PASS` only by one stage. Its cost was US$0.116832 versus US$0.237478. This is synthetic development evidence, not independent validation. Run `python scripts/analyze_single_stage_ablation.py` to recheck the saved outputs.

## How to read the numbers

- **Three-class accuracy:** exact verdict matches divided by 30; an always-one-class predictor gets 10/30 on this balanced set.
- **Clear-violation catch rate:** gold `FLAG` cases predicted `FLAG`. A gold `FLAG` predicted `PASS` is a false negative; a case sent to `HUMAN_REVIEW` is a separate escalation.
- **False flags on clean:** gold `PASS` cases predicted `FLAG`. A clean case sent to `HUMAN_REVIEW` consumes human time but is not counted as a false `FLAG`.
- **Borderline escalation:** gold `HUMAN_REVIEW` cases predicted `HUMAN_REVIEW`. Overconfident `FLAG` and `PASS` decisions are shown separately in the confusion matrices.
- **Structured-output rate:** parseable, schema-conforming outputs divided by cases attempted. It does not show whether verdicts or cited reasons are right.
- **Cost:** API-reported input and output tokens multiplied by the recorded rate per million, then divided by case count for cost per script. These are estimates, not the provider invoice; they exclude human work, infrastructure and interrupted requests.

The primary revised AI scored **27/30** versus **24/30** for keyword search. The extension AI scored **23/30** versus **20/30**. In the extension the AI flagged 10/10 clear violations, falsely flagged 0/10 clean cases, escalated 2/10 clean cases and 5/10 borderline cases. Its total `HUMAN_REVIEW` rate was 7/30. The keyword method flagged 9/10 clear violations, falsely flagged 2/10 clean cases, and escalated 3/10 borderline cases. See the [extension comparison and both confusion matrices](holdout_keyword_baseline_results.md).

No numeric success target was registered before these runs. [Product metrics](../docs/product_overview.md#metrics-targeted-and-reached) distinguish these observations from targets for a **future** independently labelled evaluation. A later targeted 11-case blind re-review proposed four overall label changes after outputs had been seen. The reported scores stay against the original frozen labels; [sensitivity analysis](label_adjudication_sensitivity_v1.md) is explicitly hypothetical.

## Reproduce without spending API credit

From the repository root, use Python 3.9 or later:

```powershell
python -m unittest discover -s tests -v
python -m src.evaluate_baseline data/primary_cases.jsonl
python -m src.evaluate_baseline data/extension_cases_v2.jsonl
python -m src.review_one examples/review_case.json
```

The first command checks code behavior. The next two re-run the deterministic method on the original inputs; compare the printed summaries with the saved baseline artifacts. The last command validates a single fictional script and previews AI cost but makes **no API request**. Re-running historical AI predictions requires a paid service and may produce different results; the saved per-case outputs, prompt version, model, token usage and date are provided to inspect the actual reported runs. See [`docs/ai_api_design.md`](../docs/ai_api_design.md) before any optional live call.
