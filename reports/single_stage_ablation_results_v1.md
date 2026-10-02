# One-stage versus two-stage synthetic development comparison

The [pre-run protocol](single_stage_ablation_protocol_v1.md) fixed a one-call alternative before this ablation. On 2026-10-02 it was run once on the frozen 30-case synthetic extension with the same `openai/gpt-6-sol` model. The [one-stage case outputs](single_stage_ablation_extension_v2.jsonl), [saved two-stage outputs](ai_evaluation_extension_v2.jsonl), [frozen cases](../data/extension_cases_v2.jsonl), prompt lock, and [summary](single_stage_ablation_extension_v2_summary.json) are retained. `python scripts/analyze_single_stage_ablation.py` independently recomputes the paired verdict, token-cost and latency comparison without another API call.

| Measure on these 30 constructed cases | One stage | Two stages |
|---|---:|---:|
| Exact overall verdict matches | 22/30 (73.3%) | 23/30 (76.7%) |
| Clear violations given `FLAG` | 9/10 | 10/10 |
| Clear violations marked `PASS` | 1/10 | 0/10 |
| Clean cases falsely given `FLAG` | 0/10 | 0/10 |
| Borderline cases sent to `HUMAN_REVIEW` | 5/10 | 5/10 |
| Model requests | 30 | 60 |
| Usage-based estimated API cost | US$0.116832 | US$0.237478 |
| Median saved latency per case | 4.149 s | 10.716 s |

The overall verdicts differed on **one** case, `HOLDOUT-19`. The script's only relationship language is a bare thank-you to CHANEL, with spoken and visual endorsement but no clear paid-relationship disclosure in caption, speech, or on-screen text. The frozen reference verdict is `FLAG` under `CH-DISC-01`. The one-stage reviewer returned `PASS` with no findings; the two-stage reviewer returned `FLAG`. The latter's cited rule was `CH-DISC-02`, not the frozen reference's `CH-DISC-01`. Therefore the two-stage run **matched the overall class** but did not match the reference rule ID. The existing headline score is verdict-only and should not be read as rule-level correctness.

One stage cost **49.2%** as much as two stages in these saved calls and had a shorter median response time. The one observed safe miss matters for a pre-publication decision-support product, but a single paired difference cannot establish that two stages are generally more accurate or safer. The one-stage prompt was designed after earlier two-stage outputs were inspected; model responses can vary; the synthetic examples and reference labels are project-authored and partly disputed. This is a **retrospective development ablation**, not independent validation or a causal isolation of stage count. A future comparison should lock both methods before collecting a new independently labelled set and include repeated model runs, rule-level evidence review, and human correction time.
