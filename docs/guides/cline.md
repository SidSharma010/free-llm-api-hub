# Cline

Last verified: 2026-09-26. Source: [Cline: OpenAI compatible provider](https://docs.cline.bot/provider-config/openai-compatible).

Cline has an "OpenAI Compatible" provider that works with any provider in this directory that has `api_format: openai-chat`.

## Setup

1. Open the Cline settings panel and choose **OpenAI Compatible** as the API provider.
2. Enter the **Base URL** from `providers.json`. Cline's docs stress that this must be the provider's endpoint, not OpenAI's.
3. Enter your **API key**.
4. Enter the **Model ID**, exactly as the provider lists it.
5. Optional: under Model Configuration, set the max output tokens and context window if the provider's limits are lower than the defaults.
6. Click **Verify** to confirm the connection.

## Example: Cerebras

| Field | Value |
|---|---|
| Base URL | `https://api.cerebras.ai/v1` |
| Model ID | `gpt-oss-120b` |

Cerebras requires a payment method to activate its free credits; see its entry in `providers.json`.

## Notes

- Test the key first with `python scripts/test_key.py <provider>`.
- Cline's docs tell you to check each provider's documentation for supported model names and provider-specific options.
