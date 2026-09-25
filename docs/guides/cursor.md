# Cursor

Status: **unverified.** No current official Cursor documentation page for custom base URLs was found on 2026-09-26. The `docs.cursor.com` settings page redirects to the general docs, which do not cover it.

What follows comes from Cursor community forum threads (forum.cursor.com), not from Cursor's documentation. Treat it as a starting point and check Cursor's own docs and settings.

## Reported setup

Cursor Settings → Models has an **OpenAI API Key** field and an **Override OpenAI Base URL** option. Users report entering a provider's key and its OpenAI-format base URL from `providers.json` there, then adding the provider's model ID as a custom model.

## Reported problems

Forum threads describe these issues:

- With the override enabled, Cursor's own built-in models stop working, because requests are sent to the overridden URL.
- Some Cursor models, such as Composer 2.5, return "This model does not support custom API keys" while the override is on.
- Users have asked for a separate base URL per custom model. That request is open, so the override applies to all OpenAI-key traffic.

These reports may be out of date. Cursor's behaviour and plan requirements can change.

## If you can confirm this

Open a pull request or issue linking Cursor's official documentation for custom endpoints. Once confirmed, this guide can be marked verified.
