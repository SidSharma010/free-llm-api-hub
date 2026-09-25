#!/usr/bin/env python3
"""Check that an API key works against a provider listed in providers.json.

The key is read from an environment variable, never from the command line, and
is sent only to the provider's own api_base_url.

Usage:
  export GROQ_API_KEY=...
  python scripts/test_key.py groq
  python scripts/test_key.py groq --chat openai/gpt-oss-20b
  python scripts/test_key.py cloudflare-workers-ai --account-id YOUR_ACCOUNT_ID
  python scripts/test_key.py --list

The default check calls GET {base_url}/models. With --chat MODEL it also sends
one short chat completion (this counts against your free limits).
Exit code: 0 key accepted, 1 key rejected or request failed, 2 usage error.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROVIDERS_FILE = Path(__file__).resolve().parent.parent / "providers.json"
TIMEOUT = 30


def load_providers():
    data = json.loads(PROVIDERS_FILE.read_text(encoding="utf-8"))
    return {p["id"]: p for p in data["providers"]}


def default_env_name(provider_id):
    return provider_id.upper().replace("-", "_") + "_API_KEY"


def request(url, key, body=None):
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        return None, str(exc)


def describe(status, body):
    if status is None:
        return f"request failed: {body}"
    if status == 200:
        return "accepted"
    if status in (401, 403):
        return f"rejected (HTTP {status}): check the key and its permissions"
    if status == 429:
        return "HTTP 429: rate limited; the key was recognised but a limit was reached"
    snippet = " ".join(body.split())[:200]
    return f"HTTP {status}: {snippet}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("provider", nargs="?", help="provider id from providers.json")
    parser.add_argument("--list", action="store_true", help="list provider ids and exit")
    parser.add_argument("--key-env", help="environment variable holding the key (default: <ID>_API_KEY)")
    parser.add_argument("--account-id", help="account id, for providers whose base URL contains {account_id}")
    parser.add_argument("--chat", metavar="MODEL", help="also send one short chat completion with this model")
    args = parser.parse_args()

    providers = load_providers()
    if args.list:
        for pid in providers:
            print(f"{pid}  (key variable: {default_env_name(pid)})")
        return 0
    if not args.provider:
        parser.print_usage(sys.stderr)
        return 2
    if args.provider not in providers:
        print(f"error: unknown provider {args.provider!r}; use --list", file=sys.stderr)
        return 2

    provider = providers[args.provider]
    env_name = args.key_env or default_env_name(args.provider)
    key = os.environ.get(env_name)
    if not key:
        print(f"error: environment variable {env_name} is not set", file=sys.stderr)
        return 2

    base = provider["api_base_url"]
    if "{account_id}" in base:
        if not args.account_id:
            print("error: this provider needs --account-id", file=sys.stderr)
            return 2
        base = base.replace("{account_id}", args.account_id)
    base = base.rstrip("/")

    print(f"{provider['name']}: GET {base}/models")
    status, body = request(f"{base}/models", key)
    print(f"  {describe(status, body)}")
    ok = status == 200

    if args.chat:
        print(f"{provider['name']}: POST {base}/chat/completions (model {args.chat})")
        payload = {
            "model": args.chat,
            "messages": [{"role": "user", "content": "Reply with the single word: ok"}],
            "max_tokens": 16,
        }
        status, body = request(f"{base}/chat/completions", key, payload)
        print(f"  {describe(status, body)}")
        ok = ok and status == 200

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
