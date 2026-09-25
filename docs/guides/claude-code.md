# Claude Code

Last verified: 2026-09-26.

Sources: [Claude Code gateway compatibility guide](https://code.claude.com/docs/en/llm-gateway-protocol), [Claude Code LLM gateway overview](https://code.claude.com/docs/en/llm-gateway), [OpenRouter: Claude Code integration](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration).

## What Claude Code needs

Claude Code does not speak the OpenAI Chat Completions format. Anthropic's gateway guide lists the API formats it supports:

| Format | Selected by |
|---|---|
| Anthropic Messages (`/v1/messages`) | `ANTHROPIC_BASE_URL` |
| Amazon Bedrock InvokeModel | `ANTHROPIC_BEDROCK_BASE_URL` with `CLAUDE_CODE_USE_BEDROCK=1` |
| Google Cloud Agent Platform rawPredict | `ANTHROPIC_VERTEX_BASE_URL` with `CLAUDE_CODE_USE_VERTEX=1` |

Pointing Claude Code at an OpenAI-format base URL, such as the `api_base_url` of most providers in this directory, will not work. A provider must expose an Anthropic-format endpoint.

## Support statement

Anthropic's documentation says it "doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway." The setup below is documented by OpenRouter, not by Anthropic. Using it with non-Claude or free models is outside what Anthropic supports, and features that depend on Claude-specific behaviour may not work.

## OpenRouter setup

OpenRouter documents an Anthropic-format endpoint at `https://openrouter.ai/api`. Its instructions:

```bash
export OPENROUTER_API_KEY="<your-openrouter-api-key>"
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""
export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1
```

Per OpenRouter's documentation:

- `ANTHROPIC_BASE_URL` must be the full URL `https://openrouter.ai/api`, not the `/api/v1` OpenAI-format URL.
- `ANTHROPIC_API_KEY` must be set to an empty string so it does not conflict with `ANTHROPIC_AUTH_TOKEN`.
- Define `OPENROUTER_API_KEY` before the line that references it.
- The variables can go in your shell profile or in `.claude/settings.local.json` in the project.
- Run `/logout` in Claude Code to clear any cached Anthropic login, then restart it.
- `/status` should show `ANTHROPIC_AUTH_TOKEN` and the OpenRouter base URL.

Anthropic's docs add that setting only `ANTHROPIC_BASE_URL` without a gateway credential does not replace a saved claude.ai login; that login's limits and billing still apply.

## Other providers

No other provider in `providers.json` has a confirmed Anthropic-format endpoint (`anthropic_base_url` is `null`). Do not assume one exists. If you know of one, open an issue with a link to the provider's documentation.
