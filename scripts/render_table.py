#!/usr/bin/env python3
"""Render the provider table in README.md from providers.json.

Usage:
  python scripts/render_table.py          rewrite the table in README.md
  python scripts/render_table.py --check  exit 1 if README.md is out of date
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- PROVIDERS:START -->"
END = "<!-- PROVIDERS:END -->"


def cell(value):
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return str(value).replace("|", "\\|")


def render(providers):
    rows = [
        "| Provider | Base URL | Free limits | Card required | Responses API | Last verified |",
        "|---|---|---|---|---|---|",
    ]
    for p in providers:
        rows.append(
            "| [{name}]({signup}) | `{base}` | {limits} | {card} | {resp} | {date} |".format(
                name=cell(p["name"]),
                signup=p["signup_url"],
                base=p["api_base_url"],
                limits=cell(p["limits"]["summary"]),
                card=cell(p["card_required"]),
                resp=cell(p["supports_responses_api"]),
                date=p["last_verified"],
            )
        )
    return "\n".join(rows)


def main(argv):
    data = json.loads((ROOT / "providers.json").read_text(encoding="utf-8"))
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        print(f"error: README.md must contain {START} and {END}")
        return 1
    head, rest = readme.split(START, 1)
    _, tail = rest.split(END, 1)
    updated = f"{head}{START}\n{render(data['providers'])}\n{END}{tail}"

    if "--check" in argv:
        if updated != readme:
            print("README.md provider table is out of date; run scripts/render_table.py")
            return 1
        print("README.md provider table is up to date")
        return 0
    readme_path.write_text(updated, encoding="utf-8", newline="\n")
    print("README.md updated")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
