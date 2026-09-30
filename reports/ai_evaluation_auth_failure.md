# AI evaluation attempt: authentication failure

Date: 2026-09-30  
Model selected: `gpt-6-sol`  
Planned: 30 cases, two Responses API stages per case, spending approval ceiling US$1.50.

## Outcome

The configured credential was rejected by `https://api.openai.com/v1/responses` with HTTP 401 `invalid_api_key`. The 30 case rows contain no successful verdicts, no API token usage, and no cost estimate. This was an authentication failure, **not an AI model evaluation**; do not report its zero successful outputs as 0% model accuracy.

At the time of this failed attempt, the project was configured for the direct OpenAI endpoint, while the user intended to use their own OpenRouter key. The key was therefore sent to the wrong provider endpoint. The project has since been adapted to OpenRouter's Responses API; this report remains a record of the failed attempt, not a result from the current configuration. See the [OpenRouter quickstart](https://openrouter.ai/docs/quickstart).

The failed result files were sanitized so they do not retain the provider's echoed masked credential. `src/evaluate_ai.py` now stops on the first 401/403 rather than attempting every case after an authentication failure.
