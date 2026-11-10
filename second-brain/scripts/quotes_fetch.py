#!/usr/bin/env python3
"""Fetch attributed quotes for the Quote Curator from free public APIs.

Sources (check each provider's terms before commercial use):
  - ZenQuotes: https://zenquotes.io  (free tier requires a link back to
    zenquotes.io wherever quotes are displayed)
  - Quotable (community mirror, open source): https://api.quotable.io

The script pulls a batch, filters by keyword theme, de-duplicates against
30_Resources/Inspiration/Quotes/_used.md and writes a Markdown table the
Quote Curator prompt can refine. It does not verify attribution; that is
the curator's job.

Usage:
  python quotes_fetch.py --theme architecture --count 30
  python quotes_fetch.py --theme manufacturing --source quotable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
QUOTES_DIR = HERE.parent / "30_Resources" / "Inspiration" / "Quotes"
USED = QUOTES_DIR / "_used.md"

THEME_KEYWORDS = {
    "architecture": ["architect", "building", "design", "space", "form", "structure", "house", "light"],
    "manufacturing": ["quality", "craft", "work", "make", "build", "process", "detail", "excellence", "tools"],
    "innovation": ["innovat", "invent", "idea", "create", "future", "change", "imagin", "possible"],
    "leadership": ["lead", "character", "courage", "discipline", "responsib", "integrity"],
    "learning": ["learn", "knowledge", "memory", "study", "teach", "wisdom", "curios"],
}

# Quotable tags that map well to our themes.
QUOTABLE_TAGS = {
    "architecture": "architecture|design|art",
    "manufacturing": "work|business|technology",
    "innovation": "technology|future|change|creativity",
    "leadership": "leadership|character|courage",
    "learning": "education|knowledge|wisdom",
}


def fetch_zenquotes(n: int) -> list[dict]:
    out: list[dict] = []
    while len(out) < n:
        r = requests.get("https://zenquotes.io/api/quotes", timeout=30)
        r.raise_for_status()
        for item in r.json():
            out.append({"quote": item.get("q", "").strip(), "author": item.get("a", "").strip(), "source": "zenquotes.io"})
        if len(r.json()) < 50:
            break
    return out[: n * 3]


def fetch_quotable(theme: str, n: int) -> list[dict]:
    tags = QUOTABLE_TAGS.get(theme, "")
    r = requests.get("https://api.quotable.io/quotes/random", params={"limit": min(n * 3, 50), "tags": tags}, timeout=30)
    r.raise_for_status()
    return [{"quote": q["content"].strip(), "author": q["author"].strip(), "source": "quotable.io"} for q in r.json()]


def load_used() -> set[str]:
    if not USED.exists():
        return set()
    return {line.strip().lower() for line in USED.read_text().splitlines() if line.strip().startswith('"')}


def matches(theme: str, quote: str) -> bool:
    kws = THEME_KEYWORDS.get(theme, [])
    q = quote.lower()
    return any(k in q for k in kws) if kws else True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--theme", required=True, choices=sorted(THEME_KEYWORDS))
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--source", choices=["zenquotes", "quotable", "both"], default="both")
    ap.add_argument("--out", default=None, help="output markdown path")
    args = ap.parse_args()

    pool: list[dict] = []
    try:
        if args.source in ("zenquotes", "both"):
            pool += fetch_zenquotes(args.count)
    except Exception as exc:  # noqa: BLE001
        print(f"zenquotes failed: {exc}", file=sys.stderr)
    try:
        if args.source in ("quotable", "both"):
            pool += fetch_quotable(args.theme, args.count)
    except Exception as exc:  # noqa: BLE001
        print(f"quotable failed: {exc}", file=sys.stderr)

    used = load_used()
    seen: set[str] = set()
    picked: list[dict] = []
    for item in pool:
        key = re.sub(r"\W+", " ", item["quote"].lower()).strip()
        if not item["quote"] or key in seen or f'"{item["quote"].lower()}"' in used:
            continue
        if not matches(args.theme, item["quote"]):
            continue
        seen.add(key)
        picked.append(item)
        if len(picked) >= args.count:
            break

    out = Path(args.out) if args.out else QUOTES_DIR / f"{date.today().isoformat()}_{args.theme}_raw.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Raw quotes: {args.theme} ({date.today().isoformat()})",
        "",
        "Unverified attributions. Run the Quote Curator prompt on this table before use.",
        "Attribution: quotes via zenquotes.io (link back required on free tier) and quotable.io.",
        "",
        "| # | Quote | Attributed to | Source |",
        "|---|---|---|---|",
    ]
    for i, q in enumerate(picked, 1):
        lines.append(f"| {i} | \"{q['quote']}\" | {q['author']} | {q['source']} |")
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {len(picked)} quotes to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
