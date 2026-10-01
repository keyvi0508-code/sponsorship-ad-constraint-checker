# Short project demo script

**Target length:** about 5 minutes (the instructor accepts 2–8 minutes)  
**Language:** English  
**Example:** HOLDOUT-03  
**Recording:** Show your face and the computer screen together throughout the explanation. Keep the browser text readable.  
**Mode:** Use the local workbench's saved outputs; a live paid API call is unnecessary.

## 0:00–0:30 — Problem, user and scope

**Show:** The Creator Content Review Workbench header, CHANEL-only scope, and campaign-brief status.

**Say:** “A creator-partnership reviewer needs to check tomorrow's sponsored draft before it goes live. Ctrl+F finds words, but can miss a misleading comparison expressed indirectly. This independent prototype checks selected public CHANEL rules and shows evidence for a human decision. It is not CHANEL-approved. No private campaign brief was supplied, so required selling points are not evaluated.”

## 0:30–1:10 — Input and example script

**Show:** The preloaded `HOLDOUT-03` draft in the left review panel.

**Say:** “The input separates caption, spoken words, on-screen text, and product-use context. This fictional example discloses the sponsorship, then says: ‘My side-by-side wear test: the rival brand faded sooner.’ The issue is whether that sounds like an impartial, evidence-based comparison, not the mere presence of a competitor.”

## 1:10–1:45 — Measured keyword baseline

**Show:** The saved keyword result card in the right panel.

**Say:** “The keyword baseline returns `PASS` for this case. It can find literal phrases, but a fixed pattern does not reliably resolve the context around a side-by-side comparison. Across all 30 extension cases, it gets 20 correct.”

## 1:45–2:30 — AI review and architecture

**Show:** The saved AI result card, quoted evidence, rule IDs, and rationale. Point out the "SAVED DEMO · NO API" badge.

**Say:** “The optional AI uses one call to extract exact quotes and another to apply the rules. Here it returns `HUMAN_REVIEW` under CH-CONTEXT-01. The separate evidence and judgement make the suggestion inspectable, but they cost two calls; I have not shown that this is better than one call. The saved result makes no new API request.”

## 2:30–3:20 — Outcomes, cost and critique

**Show:** The five evaluation cards at the top of the workbench, including estimated cost and observed wait.

**Say:** “On the 30-case extension, AI gets 23 correct and the measured keyword method 20. AI flags all 10 clear violations and falsely flags no clean case, but escalates two clean cases and only five of ten borderline ones. Its estimated token cost is about 0.8 US cents per script, with a 10.72-second median wait. These are small synthetic results, not production accuracy, an invoice, or a wait guarantee. I did not pre-register a numeric success threshold.”

## 3:20–4:00 — Human decision and export

**Show:** Choose `Escalate`, enter a short rationale, record it locally, and export the review record. Open the downloaded JSON only if time permits; highlight policy source, both methods, the human decision, and `mandatory_selling_points: not_evaluated`.

**Say:** “The reviewer makes the final decision. The downloaded record captures the script, evidence, rule source, decision, and time for handoff. The app does not store a server-side audit history; editing the script invalidates the old review.”

## 4:00–4:30 — Data, evaluation and code repository

**Show:** The README architecture diagram, `data/README.md`, `reports/README.md`, and the saved extension confusion matrix. Avoid scrolling through many raw files.

**Say:** “The repository explains the persona, input and output, architecture, data provenance, evaluation formulas, and saved results. The two 30-case splits are reported separately. The prompt was tuned after earlier primary results, so the extension is a supplementary development check, not an independent field benchmark. The code and no-call sample can be run from the README.”

## 4:30–5:00 — Rough edges and next test

**Show:** The synthetic-data / development-evidence notice, then reveal the saved reference label only after showing the system outputs.

**Say:** “The product cannot inspect the finished video's actual sound, visibility, or timing, and a downloaded JSON file is not a production audit system. Next I would freeze rules and targets before evaluating permissioned real drafts with independent labels, then measure reviewer time and correction quality. A human remains responsible for the final decision.”

## Recording checklist

- Keep the API key and any credential-setting screen off camera.
- Keep your face visible beside the screen, use readable zoom, and rehearse to finish near five minutes. The teacher will watch no more than the first eight minutes.
- Do not make another paid API call for the demo; the saved outputs are sufficient.
- Reveal the frozen gold label only after showing both system outputs.
- If recording from source, start the local interface with `python -m src.web_app`; opening the saved example makes no API call.
- Demonstrate the local JSON export without uploading the downloaded file to another service. The browser session and downloaded file are the only record; the server does not persist it.
- Keep the repository private until the final privacy, attribution, and course-submission review.
- Avoid presenting the 10-per-class results as a general estimate of CHANEL or industry-wide performance.
