# Short project demo script

**Target length:** about 3 minutes  
**Language:** English  
**Example:** HOLDOUT-03  
**Mode:** Use the local workbench's saved outputs; do not make a live paid API call during recording.

## 0:00–0:20 — Problem and scope

**Show:** The Creator Content Review Workbench header, CHANEL-only scope, and campaign-brief status.

**Say:** “This prototype helps a human reviewer screen a proposed sponsored video script against a narrow set of public CHANEL creator guidelines. It is independent and not affiliated with CHANEL. No private campaign brief was provided, so required selling points are not evaluated.”

## 0:20–0:50 — The example script

**Show:** The preloaded `HOLDOUT-03` draft in the left review panel.

**Say:** “This fictional example discloses the sponsorship, then says: ‘My side-by-side wear test: the rival brand faded sooner.’ The question is not simply whether a competitor is mentioned. The wording may sound like an evidence-based comparison, but the script does not make clear whether the criticism is being presented as impartial.”

## 0:50–1:20 — Keyword baseline

**Show:** The saved keyword result card in the right panel.

**Say:** “The keyword baseline returns `PASS` for this case. It can find literal phrases, but a fixed pattern does not reliably resolve the context around a side-by-side comparison. Across all 30 extension cases, it gets 20 correct.”

## 1:20–1:55 — AI-assisted review

**Show:** The saved AI result card, quoted evidence, rule IDs, and rationale. Point out the "SAVED DEMO · NO API" badge.

**Say:** “The AI returns `HUMAN_REVIEW` and points to CH-CONTEXT-01. It treats the comparison as ambiguous and sends it to a person, rather than deciding that the wording is definitely compliant or definitely a violation. The saved output also shows the evidence extracted in stage one and the decision made in stage two.”

## 1:55–2:20 — Results and operating cost

**Show:** The five evaluation cards at the top of the workbench, including estimated cost and observed wait.

**Say:** “On this same 30-case extension, AI gets 23 correct and the keyword baseline gets 20. AI flags all 10 clear violations and does not falsely flag any clean case, but it sends two clean cases to human review and flags four borderline cases. Estimated AI token cost is about 0.8 US cents per script, and the observed two-call median wait is 10.72 seconds. These are historical measurements, not an invoice or a wait guarantee.”

## 2:20–2:45 — Human decision and export

**Show:** Choose `Escalate`, enter a short rationale, record it locally, and export the review record. Open the downloaded JSON only if time permits; highlight policy source, both methods, the human decision, and `mandatory_selling_points: not_evaluated`.

**Say:** “The reviewer makes the final decision. The downloaded record captures the script, evidence, rule source, decision, and time for handoff. The app does not store a server-side audit history; editing the script invalidates the old review.”

## 2:45–3:00 — Limitation

**Show:** The synthetic-data / development-evidence notice, then reveal the saved reference label only after showing the system outputs.

**Say:** “These are small, synthetic test sets. The prompt was revised after earlier results, so this is a prompt-locked development check, not a final independent benchmark. The prototype also sees structured text only; it cannot confirm whether a disclosure is visible or audible in a finished video. A human remains responsible for the final decision.”

## Recording checklist

- Keep the API key and any credential-setting screen off camera.
- Do not make another paid API call for the demo; the saved outputs are sufficient.
- Reveal the frozen gold label only after showing both system outputs.
- If recording from source, start the local interface with `python -m src.web_app`; opening the saved example makes no API call.
- Demonstrate the local JSON export without uploading the downloaded file to another service. The browser session and downloaded file are the only record; the server does not persist it.
- Keep the repository private until the final privacy, attribution, and course-submission review.
- Avoid presenting the 10-per-class results as a general estimate of CHANEL or industry-wide performance.
