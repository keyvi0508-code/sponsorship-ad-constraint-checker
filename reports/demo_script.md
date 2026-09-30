# Short project demo script

**Target length:** about 2 minutes 30 seconds  
**Language:** English  
**Example:** HOLDOUT-03  
**Mode:** Use the saved evaluation outputs; do not make a live paid API call during recording.

## 0:00–0:20 — Problem and scope

**Show:** Project README and the three verdicts.

**Say:** “This prototype helps a human reviewer screen a proposed sponsored video script against a narrow set of public CHANEL creator guidelines. It is an independent course project, not affiliated with CHANEL, and it supports review rather than making final publication decisions.”

## 0:20–0:50 — The example script

**Show:** `data/extension_cases_v2.jsonl`; search for `HOLDOUT-03`.

**Say:** “This fictional example discloses the sponsorship, then says: ‘My side-by-side wear test: the rival brand faded sooner.’ The question is not simply whether a competitor is mentioned. The wording may sound like an evidence-based comparison, but the script does not make clear whether the criticism is being presented as impartial.”

## 0:50–1:20 — Keyword baseline

**Show:** `reports/baseline_keyword_holdout_extension_v2.json`; find `HOLDOUT-03` and its prediction. Then show the baseline matrix in `reports/holdout_keyword_baseline_results.md`.

**Say:** “The keyword baseline returns `PASS` for this case. It can find literal phrases, but a fixed pattern does not reliably resolve the context around a side-by-side comparison. Across all 30 extension cases, it gets 20 correct.”

## 1:20–1:55 — AI-assisted review

**Show:** `reports/ai_evaluation_extension_v2.jsonl`; search for `HOLDOUT-03` and show its verdict, evidence, rule IDs, and rationale.

**Say:** “The AI returns `HUMAN_REVIEW` and points to CH-CONTEXT-01. It treats the comparison as ambiguous and sends it to a person, rather than deciding that the wording is definitely compliant or definitely a violation. The saved output also shows the evidence extracted in stage one and the decision made in stage two.”

## 1:55–2:20 — Results

**Show:** `reports/holdout_keyword_baseline_results.md` and the evaluation summary JSON.

**Say:** “On this same 30-case extension, AI gets 23 correct and the keyword baseline gets 20. AI flags all 10 clear violations and does not falsely flag any clean case, but it sends two clean cases to human review and flags four borderline cases. The estimated AI token cost is about 0.8 US cents per script.”

## 2:20–2:35 — Limitation

**Show:** The report’s interpretation and limitations section.

**Say:** “These are small, synthetic test sets. The prompt was revised after earlier results, so this is a prompt-locked development check, not a final independent benchmark. The prototype also sees structured text only; it cannot confirm whether a disclosure is visible or audible in a finished video. A human remains responsible for the final decision.”

## Recording checklist

- Keep the API key and any credential-setting screen off camera.
- Do not make another paid API call for the demo; the saved outputs are sufficient.
- Reveal the frozen gold label only after showing both system outputs.
- Keep the repository private until the final privacy, attribution, and course-submission review.
- Avoid presenting the 10-per-class results as a general estimate of CHANEL or industry-wide performance.
