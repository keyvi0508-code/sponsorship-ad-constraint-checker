# Public-caption evaluation: intake gate and evidence limits

**Status:** intake gate, caption-only keyword screen and two-stage AI pilot run locally on 2026-10-02. The 23-post results and critique are documented in [the AI pilot report](../reports/public_caption_ai_pilot_v1.md). The existing 60 synthetic cases and their saved scores are unchanged.

## Why the current script interface cannot take a public caption directly

The current `validate_script_input` requires `caption` and `scenes`, but accepts `scenes: []`. The keyword baseline treats an empty scene list as no scene disclosure to check. In an audit-only minimal input with `caption: ["#CHANELpartner"]` and `scenes: []`, validation returned no errors and the baseline returned `PASS`; with `caption: ["#gifted"]`, it returned `FLAG`. Neither result is a defensible **full published-video** decision when scenes were unobserved rather than verified absent. The two-stage AI decision schema also lacks `UNKNOWN`. Do not construct real-post inputs by replacing unobserved speech or overlay with empty arrays or `false`.

The existing ten-post inventory records links, short summaries and markers, not complete caption wording. That inventory alone is insufficient for a semantic model run. Search snippets are not source text. Obtain the original visible caption and its access date before running a caption-level review; distinguish a complete captured caption from a partially visible one.

## Evidence contract for the expanded 20–30-post pilot

For every included post record the original URL, creator, access date, discovery route, eligibility reason, exact caption text available to the reviewer, whether the caption capture is complete or partial, and a short source-backed evidence excerpt. Record spoken disclosure, on-screen disclosure, product use, compensation/brief, and caption-fold visibility as **verified present**, **verified absent**, or **unverified** where relevant. An empty string or list means verified absence only; unverified is a separate state. Preserve the source list and selection order before examining system outputs. Avoid deriving all posts from a partnership-hashtag query, because that route preferentially finds already-disclosed posts.

Use three distinct output fields:

1. `caption_observation`: what the visible text literally contains, including disclosure markers and exact evidence quotes; a missing marker in a partial caption is `UNKNOWN`, not confirmed absence.
2. `caption_review`: keyword and AI suggestions about the **observed caption only**, with evidence and limitations. A clear caption-level issue can be raised, but a caption-level `PASS` must never be presented as video compliance.
3. `full_review_status`: `UNKNOWN` whenever a fact needed for a complete video decision is unverified. `HUMAN_REVIEW` is reserved for a genuinely ambiguous policy judgement on sufficiently supplied evidence; it is not a substitute for missing input. Keep the raw model suggestion separate from this evidence gate so a potentially unsafe `PASS` remains visible as a failure mode.

The runner must reject or gate incomplete public-post inputs before the existing full-script `PASS` can be shown as a final result. It must not send labels, peer-review notes, source-search hints, or an existing `full_policy_verdict` to the model. The public pilot is descriptive: report category counts, method disagreements and representative cases, **not** accuracy, precision, recall, or a pooled score with the synthetic sets. A full evaluation requires permissioned drafts or complete media, independent rule-level labels, and a frozen prompt and target before scoring.

## Implemented readiness gate

`src/public_caption_intake.py` accepts a complete or partial original-post caption capture and reports literal disclosure examples separately from the full-review status. `scripts/inspect_public_caption_intake.py` runs this gate without an API call. On the original ten inventory rows it returns `NEEDS_CAPTION_CAPTURE` for all ten and full-review `UNKNOWN` for all ten. This does **not** retract the earlier human-observed marker notes; the gate deliberately refuses to reconstruct an exact caption from those notes. Five focused tests check that a visible marker, a missing marker, and a partial caption cannot be promoted to a full-video `PASS`.

Run `python scripts/inspect_public_caption_intake.py` for the current inventory, or pass a different JSONL path. A row intended for caption review needs `caption_capture` (`complete` or `partial`) and non-empty `caption_text` copied from the original post. The gate itself only reports readiness and literal marker observations. It does not run either review method or calculate accuracy.

## Caption-only review stage

The expanded [23-post source selection](../reports/public_caption_source_selection_v1.md) was locked before method outputs. `scripts/evaluate_public_captions.py` checks its SHA-256 manifest and row order, then runs the free caption-only keyword screen. `src/public_caption_reviewer.py` contains a separately versioned two-stage AI path: literal signal extraction followed by rule judgement. It sends only the observed caption text and first-stage signals to OpenRouter, not the source-search route, creator identifier, or any label field. Exact extracted quotations are checked against the captured caption. The paid AI path was run by the project owner from their own PowerShell on 2026-10-02; its [per-case output](../reports/public_caption_ai_v1.jsonl) and [summary](../reports/public_caption_ai_v1_summary.json) are saved. `python scripts/analyze_public_caption_pilot.py` rechecks both saved methods without another API call.

Both paths return a **caption suggestion** separately from the evidence-gated `full_review_status: UNKNOWN`. A keyword `PASS` means a listed marker was found; it is not a full caption-policy assessment. An AI `PASS` means no apparent issue in observed caption text only. Neither may certify the uninspected video. Without independent real-post compliance labels, this pilot reports behavior and disagreements, not accuracy.
