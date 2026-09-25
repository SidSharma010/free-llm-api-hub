# Codex CLI

Last verified: 2026-09-26. Source: [Codex configuration reference](https://developers.openai.com/codex/config-reference).

## The Responses API requirement

Codex CLI can use a custom model provider, but the configuration reference states that `wire_api` accepts `responses` as the only supported value, and that it is the default. Codex therefore needs an endpoint that implements the OpenAI Responses API (`/v1/responses`). A provider that offers only Chat Completions will not work.

In `providers.json` this is the `supports_responses_api` field:

| Value | Meaning |
|---|---|
| `true` | The provider's docs describe a Responses API endpoint. |
| `"partial"` | Documented only for some models or with restrictions; read the provider's `notes`. |
| `"unverified"` | Not confirmed from official docs. Do not assume it works. |
| `false` | The provider's docs state it is not supported. |

As of the verification date, only Groq and Hugging Face are `true`, and both describe their Responses API as beta. Cloudflare Workers AI is `"partial"`.

## Provider definition

The configuration reference lists these keys under `model_providers.<id>`: `name`, `base_url`, `wire_api`, and for authentication `env_key` (the name of an environment variable holding the key). A Groq entry looks like this:

```toml
[model_providers.groq]
name = "Groq"
base_url = "https://api.groq.com/openai/v1"
env_key = "GROQ_API_KEY"
wire_api = "responses"
```

Select the provider and model with the top-level keys described in the configuration reference. Those top-level key names were not checked for this guide, so follow the reference rather than copying them from here.

## Groq limitations

Groq's Responses API is documented as beta and does not support `previous_response_id`, `store`, `truncation`, `include`, `safety_identifier`, `prompt_cache_key`, reusable `prompt`, or stateful conversations. Codex features that depend on these may fail. This guide has not tested Codex against Groq end to end.

## Hugging Face

Hugging Face documents a Responses API (beta) at `https://router.huggingface.co/v1/responses`, and states that all Inference Providers chat completion models should be compatible. It also has its own Codex setup guide, linked from its [Inference Providers page](https://huggingface.co/docs/inference-providers/index).
