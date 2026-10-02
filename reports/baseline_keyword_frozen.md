# Keyword baseline result on the frozen dataset

**Historical stage record:** Statements below about AI not yet having run describe the state on 2026-09-29. Later saved synthetic and real-caption AI runs are indexed in the [current evaluation guide](README.md).

Run date: 2026-09-29  
Dataset: 30 fictional English scripts, SHA-256 `cff65dc75a88a6aae1536758fcb67312b69574407ff255dcc7be7fa1b7ed3ac2`  
Method: deterministic keyword/rule-search baseline in `src/baseline.py`; no external API calls.

## Results

- Accuracy: **24/30 (80.0%)**.
- `FLAG` cases: 10/10 classified as `FLAG`.
- `PASS` cases: 9/10 classified as `PASS`; 1 was escalated to `HUMAN_REVIEW`.
- `HUMAN_REVIEW` cases: 5/10 escalated correctly; the other 5 were classified as `PASS`.
- False positives on clean `PASS` scripts (predicted `FLAG`): **0**.
- False negatives on known violations (predicted `PASS` for a `FLAG` case): **0**.
- Borderline escalation: **5/10 (50%)**.
- Keyword-baseline API cost: **$0**.

| Gold \\ Predicted | FLAG | HUMAN_REVIEW | PASS |
|---|---:|---:|---:|
| FLAG | 10 | 0 | 0 |
| HUMAN_REVIEW | 0 | 5 | 5 |
| PASS | 0 | 1 | 9 |

## Interpretation and limits

The 80% accuracy is for this small, deliberately balanced, synthetic test set only. The baseline catches the constructed clear violations and avoids flagging clean cases, but it escalates only half of the intentionally borderline cases; the remaining half are passed through. Therefore accuracy alone overstates its usefulness for a human-review workflow. The benchmark is not evidence of real-world CHANEL moderation performance, and the AI system has not yet been run.
