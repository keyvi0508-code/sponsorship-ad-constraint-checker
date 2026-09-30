# AI evaluation design

## Two-stage review

The AI path makes two Responses API calls per script so evidence extraction remains separate from the policy decision. The single-script entry point is `python -m src.review_one path/to/script.json`; the batch evaluator is `python -m src.evaluate_ai`:

1. Level 1 returns only verbatim evidence snippets and their script locations.
2. Level 2 receives the original review input and Level 1 evidence, applies the source-grounded rules, and returns `PASS`, `FLAG`, or `HUMAN_REVIEW` with rule IDs and short rationales.

The evaluator strips `ground_truth` and `annotator_notes` before either request. Each response is constrained by a JSON Schema. API input/output token usage, per-case latency, estimated cost, invalid/error cases, and the confusion matrix are recorded. No API request is made unless the command is explicitly run with `--run-api`.

Level 2 instructions carry a prompt version (`rubric-clarification-2026-09-30-v1`) and distinguish competitor impartiality from first-hand product-use review. This version was drafted after inspecting the initial AI run's disagreements. Its original 30-case development run and the later 30-case extension run both completed, but the extension is still labeled development evidence because the prompt was revised after earlier outputs were inspected. Do not describe either run as an untouched independent benchmark.

The one-script command defaults to a no-call preflight and requires both `--run-api` and `--confirm-paid-run` before sending a request. It rejects evaluation-only fields such as `ground_truth`, validates the input schema, estimates a conservative upper bound, and defaults to a US$0.10 per-review ceiling. The batch evaluator separately requires a frozen manifest, explicit paid-run flags, and respects its US$1.50 ceiling. Interrupted batch runs can be continued with `--resume`; the evaluator checks that saved rows match the requested model and prompt version, then sends only cases without completed rows. Existing output files are not overwritten by a fresh run.

Both command paths use the same two-stage reviewer and structured schemas. A dry run, schema validation, unit tests, and the deterministic keyword baseline can all be run without an API key or network request. The one-script sample in `examples/review_case.json` is fictional and deliberately has no evaluation label.

## Cost basis

The current default is `openai/gpt-6-sol` through OpenRouter's Responses API at `https://openrouter.ai/api/v1/responses`. The OpenRouter model page was checked 2026-09-30 and listed standard routing at $2.00 per million input tokens and $10.00 per million output tokens. Actual routed provider pricing can vary, so the report calls its computed amount an estimate. Before sending requests, the evaluator estimates a conservative upper bound from UTF-8 request bytes, includes the maximum output allowance for both stages and carries the Level 1 output into the Level 2 input estimate; it blocks the run if that bound exceeds the user's approved US$1.50 ceiling. Afterward it records API-reported token counts and calculates cost using the date-stamped rate snapshot in `src/evaluate_ai.py`. Re-check prices and the user's OpenRouter spend settings before any later run.

Set `OPENROUTER_API_KEY` in the local environment. The legacy `OPENAI_API_KEY` name is accepted as a fallback because the user's OpenRouter key was initially stored under that variable name. Neither variable should be written to project files or committed. `provider.require_parameters` asks OpenRouter to route only to endpoints that support the request's required structured-output parameters.

## Provider documentation

- [OpenRouter Responses API](https://openrouter.ai/docs/api/api-reference/responses/create-responses)
- [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs)
- [OpenRouter GPT-6 Sol model and pricing](https://openrouter.ai/openai/gpt-6-sol)
- [OpenRouter quickstart and API key usage](https://openrouter.ai/docs/quickstart)
