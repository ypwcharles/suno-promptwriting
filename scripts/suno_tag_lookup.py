#!/usr/bin/env python3
"""
Search curated Suno tag references (derived from the bundled `suno.md`) without loading the full doc.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INDEX = SKILL_DIR / "references" / "libraries" / "tag-index-curated.md"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _iter_tag_lines(markdown: str) -> list[str]:
    lines = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not re.match(r"^- \*?`?\[.+\]`?\*?(?:\s+-\s+.+)?$", line):
            continue
        lines.append(line)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Lookup Suno meta/style tags from curated references.")
    parser.add_argument("--query", "-q", action="append", required=True, help="Keyword to search (repeatable).")
    parser.add_argument("--file", default=str(DEFAULT_INDEX), help="Markdown tag index file to search.")
    parser.add_argument("--limit", type=int, default=50, help="Max results to print.")
    args = parser.parse_args()

    index_path = Path(args.file).expanduser().resolve()
    markdown = index_path.read_text(encoding="utf-8")
    tag_lines = _iter_tag_lines(markdown)

    queries = [_normalize(q) for q in args.query]

    matches: list[str] = []
    for line in tag_lines:
        hay = _normalize(line)
        if all(q in hay for q in queries):
            matches.append(line)
            if len(matches) >= args.limit:
                break

    if not matches:
        print("No matches.")
        return

    for m in matches:
        print(m)


if __name__ == "__main__":
    main()
