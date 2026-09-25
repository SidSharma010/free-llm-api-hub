# Contributing

Corrections and new providers are welcome. The rules below keep the data trustworthy.

## Rules for data

1. **Cite official sources.** Every value must come from the provider's own documentation or dashboard, and the page must be listed in the provider's `sources`. Blog posts, forum threads, social media and other directories are not sources.
2. **Do not guess.** If you cannot confirm a value from an official source, set it to `"unverified"` (or leave `models` empty). An unverified value is more useful than a wrong one.
3. **Update `last_verified`.** Set it to the date you checked the sources, in `YYYY-MM-DD` format.
4. **Write fresh content.** Do not copy text from other directories or lists.
5. **Stay plain.** No promotional language. State limits, requirements and caveats as the provider states them.

## Scope

Providers with an ongoing free tier or recurring free credit. One-time signup credits, unofficial proxies and resellers, and local runtimes are out of scope. Providers that require a payment method are allowed if `card_required` is `true`.

## Editing providers.json

Each provider has these fields. `scripts/validate_providers.py` enforces them.

| Field | Type | Notes |
|---|---|---|
| `id` | string | Lowercase letters, digits and hyphens. Unique. |
| `name` | string | Display name. |
| `signup_url` | https URL | Where to create a key. |
| `docs_url` | https URL | The provider's main documentation page for limits. |
| `api_base_url` | https URL | OpenAI-format base URL. May contain `{account_id}`. |
| `api_format` | `"openai-chat"` | Only value currently allowed. |
| `supports_responses_api` | `true`, `false`, `"partial"`, `"unverified"` | Needed by Codex CLI. |
| `anthropic_base_url` | https URL or `null` | Anthropic-format endpoint, if the provider documents one. Needed by Claude Code. |
| `card_required` | `true`, `false`, `"unverified"` | Whether a payment method is needed for the free tier. |
| `limits` | object | `summary` (string) and `detail_url` (https URL). |
| `models` | list | Objects with only an `id`. Only IDs listed in official docs. |
| `notes` | string | Caveats, requirements, and anything unverified. |
| `sources` | list of https URLs | Official pages the values came from. |
| `last_verified` | date | `YYYY-MM-DD`, not in the future. |

## Before opening a pull request

```bash
python scripts/validate_providers.py
python scripts/render_table.py       # regenerates the README table
python scripts/render_table.py --check
```

Do not edit the README table by hand; it is generated. If you have an API key, `python scripts/test_key.py <provider>` confirms the base URL works. Never put a key in an issue, a pull request, or the repository.

## Guides

Setup guides in `docs/guides/` must state which official page each instruction comes from. Mark anything that is not from the tool's own documentation as unverified.

## Reporting a change

Use the issue templates: one for a correction to existing data, one for suggesting a new provider.
