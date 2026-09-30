# Keyword baseline on the 30-case holdout

**Dataset:** `extension_cases_v2.jsonl` (frozen v2)  
**Run:** local keyword baseline, no API calls  
**Date:** 2026-09-30

The deterministic keyword baseline scored **20/30 (66.7%)** on the new balanced holdout. Gold labels are rows; baseline predictions are columns.

| Gold \ Prediction | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 9 | 0 | 1 |
| HUMAN_REVIEW | 2 | 3 | 5 |
| PASS | 2 | 0 | 8 |

It flagged 9/10 clear violations and marked one violation `PASS`. It incorrectly flagged 2/10 clean cases. It escalated 3/10 borderline cases to a person; on the other 7, it chose a definitive verdict. The model was correct on 8/10 clean cases.

This is an actual measured baseline on the holdout, not a result inferred from the earlier 30 cases. Do not tune the keyword patterns against this set and continue calling it a holdout. The saved per-case results are in [baseline_keyword_holdout_extension_v2.json](baseline_keyword_holdout_extension_v2.json).

## AI holdout run status

The AI reviewer has not been run on these cases. The revised prompt should be locked before its first call. Using the previous run's observed average, a 30-case run is estimated at about **US$0.214**; the conservative preflight ceiling is **US$1.144**, within the project's authorized US$1.50 cap. Actual token billing will depend on outputs and should be checked in the provider dashboard.

The evaluation command to run from the project directory in the PowerShell session where the API key is configured is:

```powershell
python -m src.evaluate_ai data/extension_cases_v2.jsonl --manifest data/extension_frozen_manifest_v2.json --output reports/ai_evaluation_extension_v2.jsonl --summary reports/ai_evaluation_extension_v2_summary.json --run-api --confirm-paid-run
```

The 30-case call is separate from the original development run. Do not change the prompt after examining these results; any later prompt revision would need another fresh holdout.
