#!/usr/bin/env python3
"""Validate providers.json against the schema described in CONTRIBUTING.md.

Usage: python scripts/validate_providers.py [path/to/providers.json]
Exits 0 when valid, 1 when any problem is found.
"""
import datetime
import json
import re
import sys
from pathlib import Path

UNVERIFIED = "unverified"
REQUIRED = [
    "id", "name", "signup_url", "docs_url", "api_base_url", "api_format",
    "supports_responses_api", "anthropic_base_url", "card_required",
    "limits", "models", "notes", "sources", "last_verified",
]
API_FORMATS = {"openai-chat"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https://[^\s]+$")


def check_url(problems, where, value, allow_none=False):
    if value is None and allow_none:
        return
    if not isinstance(value, str) or not URL_RE.match(value):
        problems.append(f"{where}: must be an https URL, got {value!r}")


def validate_provider(index, p):
    problems = []
    name = p.get("id", f"#{index}") if isinstance(p, dict) else f"#{index}"
    where = f"provider {name}"
    if not isinstance(p, dict):
        return [f"{where}: must be an object"]

    for key in REQUIRED:
        if key not in p:
            problems.append(f"{where}: missing field '{key}'")
    unknown = set(p) - set(REQUIRED)
    if unknown:
        problems.append(f"{where}: unknown fields {sorted(unknown)}")
    if problems:
        return problems

    if not ID_RE.match(p["id"]):
        problems.append(f"{where}: id must be lowercase letters, digits and hyphens")
    if not isinstance(p["name"], str) or not p["name"].strip():
        problems.append(f"{where}: name must be a non-empty string")

    check_url(problems, f"{where}.signup_url", p["signup_url"])
    check_url(problems, f"{where}.docs_url", p["docs_url"])
    check_url(problems, f"{where}.api_base_url", p["api_base_url"])
    check_url(problems, f"{where}.anthropic_base_url", p["anthropic_base_url"], allow_none=True)

    if p["api_format"] not in API_FORMATS:
        problems.append(f"{where}: api_format must be one of {sorted(API_FORMATS)}")
    if p["supports_responses_api"] not in (True, False, "partial", UNVERIFIED):
        problems.append(f"{where}: supports_responses_api must be true, false, \"partial\" or \"unverified\"")
    if p["card_required"] not in (True, False, UNVERIFIED):
        problems.append(f"{where}: card_required must be true, false or \"unverified\"")

    limits = p["limits"]
    if not isinstance(limits, dict) or set(limits) != {"summary", "detail_url"}:
        problems.append(f"{where}: limits must have exactly 'summary' and 'detail_url'")
    else:
        if not isinstance(limits["summary"], str) or not limits["summary"].strip():
            problems.append(f"{where}: limits.summary must be a non-empty string")
        check_url(problems, f"{where}.limits.detail_url", limits["detail_url"])

    if not isinstance(p["models"], list):
        problems.append(f"{where}: models must be a list")
    else:
        seen = set()
        for m in p["models"]:
            if not isinstance(m, dict) or set(m) != {"id"} or not isinstance(m["id"], str) or not m["id"]:
                problems.append(f"{where}: each model must be an object with only a non-empty 'id'")
            elif m["id"] in seen:
                problems.append(f"{where}: duplicate model id {m['id']!r}")
            else:
                seen.add(m["id"])

    if not isinstance(p["notes"], str):
        problems.append(f"{where}: notes must be a string")

    if not isinstance(p["sources"], list) or not p["sources"]:
        problems.append(f"{where}: sources must be a non-empty list")
    else:
        for s in p["sources"]:
            check_url(problems, f"{where}.sources", s)

    try:
        date = datetime.date.fromisoformat(p["last_verified"])
        if date > datetime.date.today():
            problems.append(f"{where}: last_verified is in the future")
    except (TypeError, ValueError):
        problems.append(f"{where}: last_verified must be an ISO date (YYYY-MM-DD)")

    return problems


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "providers.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {path}: {exc}")
        return 1

    problems = []
    if data.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    providers = data.get("providers")
    if not isinstance(providers, list) or not providers:
        problems.append("providers must be a non-empty list")
        providers = []

    ids = set()
    for i, p in enumerate(providers):
        problems.extend(validate_provider(i, p))
        pid = p.get("id") if isinstance(p, dict) else None
        if pid in ids:
            problems.append(f"duplicate provider id {pid!r}")
        ids.add(pid)

    if problems:
        print(f"{path}: {len(problems)} problem(s)")
        for line in problems:
            print(f"  - {line}")
        return 1
    print(f"{path}: OK ({len(providers)} providers)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
