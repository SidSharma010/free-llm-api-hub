# Aider

Last verified: 2026-09-26. Source: [Aider: OpenAI compatible APIs](https://aider.chat/docs/llms/openai-compat.html).

Aider connects to any endpoint that speaks the OpenAI Chat Completions format. Every provider in this directory with `api_format: openai-chat` can be used this way.

## Setup

macOS and Linux:

```bash
export OPENAI_API_BASE=<base URL from providers.json>
export OPENAI_API_KEY=<your key>
```

Windows (restart the shell afterwards):

```bat
setx OPENAI_API_BASE <base URL from providers.json>
setx OPENAI_API_KEY <your key>
```

Then, from your project directory, prefix the model ID with `openai/`:

```bash
aider --model openai/<model id>
```

## Example: Groq

```bash
export OPENAI_API_BASE=https://api.groq.com/openai/v1
export OPENAI_API_KEY=$GROQ_API_KEY
aider --model openai/openai/gpt-oss-120b
```

The first `openai/` tells Aider to use the OpenAI-compatible client. The rest is the model ID exactly as the provider lists it, so IDs that already contain a slash end up with two.

## Notes

- Test the key first with `python scripts/test_key.py <provider>`.
- Free limits are small. A coding session can use tokens quickly, so check the provider's limits in `providers.json` before a long session.
