# Cursor

Status: **partially verified.** Cursor's official help page confirms the "bring your own key" flow. It does not document the "Override Base URL" trick that the community uses to point Cursor at a third-party, OpenAI-compatible provider — that part is still community-reported only. Checked 2026-09-26.

## Official: bring your own key (confirmed)

Source: [cursor.com/help/models-and-usage/api-keys](https://cursor.com/help/models-and-usage/api-keys)

1. Open **Cursor Settings → Models**.
2. Paste your API key into the field for the matching provider, then click **Save**.
3. Officially supported providers are **OpenAI, Anthropic, Google, Azure OpenAI, and AWS Bedrock** — this list does not include arbitrary OpenAI-compatible endpoints.

Confirmed limits from the same page:

- Custom API keys only apply to **chat models**. Tab completion always uses Cursor's own built-in models, regardless of your key.
- Cursor's Zero Data Retention policy does **not** apply when you bring your own key; your data follows your chosen provider's privacy policy instead.
- Your key is not stored on Cursor's servers, but it is sent to Cursor's backend with every request over an encrypted connection, not directly to the provider.
- On Team/Enterprise plans, Cursor still charges its own per-token rate on top of your provider's bill.

## Community-reported: pointing Cursor at a free provider (unverified)

This part is **not** in Cursor's official docs. It comes from Cursor's community forum (forum.cursor.com), so treat it as a starting point, not a guarantee.

Reported steps: Cursor Settings → Models has an **Override OpenAI Base URL** field alongside the OpenAI API key field. Users report pasting a free provider's OpenAI-compatible base URL (from [`providers.json`](../../providers.json)) there, along with that provider's key, then adding the provider's model ID as a custom model.

Reported problems from forum threads:

- With the override enabled, Cursor's own built-in models can stop working, because requests get sent to the overridden URL instead.
- Some Cursor models, such as Composer 2.5, are reported to return "This model does not support custom API keys" while the override is active.
- Users have asked for a separate base URL per custom model; that request was open at last check, so the override reportedly applies to all OpenAI-key traffic at once.

These reports may be outdated by the time you read this. If you confirm current behavior against Cursor's own docs or a support reply, open a pull request or issue so this section can be marked verified.
