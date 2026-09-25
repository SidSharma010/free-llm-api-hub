# free-llm-api-hub

A directory of LLM APIs that offer a free tier: base URLs, model IDs, rate limits, signup links, and setup guides for common coding tools.

All data lives in [`providers.json`](providers.json). Every provider has a `last_verified` date. A value that could not be confirmed from the provider's official documentation is recorded as `unverified` rather than estimated.

## Providers

The table is generated from `providers.json` by `scripts/render_table.py`. "Responses API" matters for Codex CLI (see the [guides](#setup-guides)).

<!-- PROVIDERS:START -->
| Provider | Base URL | Free limits | Card required | Responses API | Last verified |
|---|---|---|---|---|---|
| [Groq](https://console.groq.com/keys) | `https://api.groq.com/openai/v1` | Free plan: 30 RPM, 1K RPD, 8K TPM, 200K TPD on the chat models listed below. Limits apply per organization. | unverified | Yes | 2026-09-25 |
| [Cerebras](https://cloud.cerebras.ai) | `https://api.cerebras.ai/v1` | Documented as a free trial tier: 5 RPM, 30K uncached TPM, 90K total TPM, 1M tokens per hour, 1M tokens per day on gpt-oss-120b and qwen-3.8-27b. | Yes | unverified | 2026-09-25 |
| [Google AI Studio (Gemini API)](https://aistudio.google.com/apikey) | `https://generativelanguage.googleapis.com/v1beta/openai/` | Google does not publish numeric free-tier RPM/RPD/TPM values in its docs. Its own rate-limits page states limits depend on usage tier and instructs users to check the AI Studio dashboard, which requires sign-in and is account-specific. Confirmed absent from official docs, not merely unresearched. | No | unverified | 2026-09-25 |
| [OpenRouter](https://openrouter.ai/settings/keys) | `https://openrouter.ai/api/v1` | Free model variants (IDs ending in :free): 20 requests per minute. 50 requests per day if you have purchased less than $10 in credits (lifetime); 1,000 requests per day once you have purchased $10 or more in credits (lifetime). Confirmed from OpenRouter's own API reference. | unverified | unverified | 2026-09-25 |
| [Mistral AI](https://console.mistral.ai) | `https://api.mistral.ai/v1` | Mistral's docs state a free API tier exists with 'restrictive rate limits' but do not publish the numeric values; they direct users to console.mistral.ai/limits/, which requires an account login and is workspace-specific. Confirmed absent from official docs. | No | unverified | 2026-09-25 |
| [Cloudflare Workers AI](https://dash.cloudflare.com/sign-up) | `https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1` | 10,000 neurons per day at no charge; limits reset daily at 00:00 UTC. | unverified | partial | 2026-09-25 |
| [NVIDIA NIM (build.nvidia.com)](https://build.nvidia.com) | `https://integrate.api.nvidia.com/v1` | NVIDIA does not publish a fixed free-tier RPM in its official docs. A moderator on NVIDIA's own developer forum stated limits 'depend on model, use-case and the amount of current overall traffic' and declined to give a fixed figure. Developers commonly report roughly 40 RPM in forum threads, but this is not an official published number and should not be relied on. | unverified | unverified | 2026-09-25 |
| [Hugging Face Inference Providers](https://huggingface.co/settings/tokens) | `https://router.huggingface.co/v1` | Free users receive $0.10 of Inference Providers credit per month, subject to change. Further use requires purchasing credits. | unverified | Yes | 2026-09-25 |
| [Together AI](https://api.together.ai/) | `https://api.together.ai/v1` | Together AI does not publish fixed per-model rate limits; its docs state limits are dynamic and scale with usage and live model capacity. Separately, its own pricing page lists one specific model, Ternary Bonsai 27B, priced at $0.00 per token for both input and output, confirmed live on together.ai/pricing. Other models on the platform are paid. | unverified | unverified | 2026-09-25 |
<!-- PROVIDERS:END -->

Free tiers change without notice. Confirm current limits on the provider's own page before relying on them, and open an issue if a row is out of date.

## Scope

- Included: providers with an ongoing free tier or recurring free credit, checked against official documentation.
- Included with flags: providers that require a payment method (`Card required: Yes`) or describe the plan as a trial. Cerebras is currently in this group.
- Not included: one-time signup credits, unofficial proxies and resellers, and local or self-hosted runtimes.
- Removed: GitHub Models, which GitHub's documentation says was retired on 2026-07-30.

## Setup guides

| Tool | Guide | Status |
|---|---|---|
| Aider | [docs/guides/aider.md](docs/guides/aider.md) | Verified against Aider docs |
| Cline | [docs/guides/cline.md](docs/guides/cline.md) | Verified against Cline docs |
| Codex CLI | [docs/guides/codex-cli.md](docs/guides/codex-cli.md) | Verified against Codex docs; requires the Responses API |
| Claude Code | [docs/guides/claude-code.md](docs/guides/claude-code.md) | Requires an Anthropic-format endpoint; read the support note |
| Cursor | [docs/guides/cursor.md](docs/guides/cursor.md) | Partially verified: BYOK flow confirmed by Cursor's own docs; the free-provider override trick is still community-reported |

## Testing a key

`scripts/test_key.py` checks that a key is accepted by a provider. It uses only the Python 3 standard library. The key is read from an environment variable, never from a command-line argument.

```bash
python scripts/test_key.py --list
export GROQ_API_KEY=your-key
python scripts/test_key.py groq
python scripts/test_key.py groq --chat openai/gpt-oss-20b
```

The default check calls `GET {base_url}/models`. `--chat MODEL` also sends one short completion, which counts against your free limits. Cloudflare needs `--account-id`.

## Validating the data

```bash
python scripts/validate_providers.py
python scripts/render_table.py --check
```

The first command checks `providers.json` against the schema. The second confirms the README table matches the data. Both run in CI.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections must cite an official source.

## License and acknowledgements

MIT, see [LICENSE](LICENSE).

Acknowledgements: this project was prompted by [open-free-llm-api/awesome-freellm-apis](https://github.com/open-free-llm-api/awesome-freellm-apis) (MIT) and [freellm.net](https://freellm.net). All content here was written independently and checked against provider documentation.
