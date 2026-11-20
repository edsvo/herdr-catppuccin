#!/usr/bin/env python3
"""Check relative links and anchors in the documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ("README.md", "PREVIEWS.md", "THIRD-PARTY-NOTICES.md")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)", re.S)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.M)


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def anchors(text: str) -> set[str]:
    return {slug(match.group(2)) for match in HEADING.finditer(text)}


def check_file(name: str, errors: list[str]) -> None:
    path = ROOT / name
    if not path.exists():
        errors.append(f"{name} is missing")
        return

    text = path.read_text(encoding="utf-8")
    known = anchors(text)
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        line = text.count("\n", 0, match.start()) + 1

        if target.startswith(("http://", "https://", "mailto:")):
            continue

        if target.startswith("#"):
            if target[1:] not in known:
                errors.append(f"{name}:{line}: missing anchor {target}")
            continue

        file_part, _, anchor = target.partition("#")
        linked = ROOT / file_part
        if not linked.exists():
            errors.append(f"{name}:{line}: missing file {file_part}")
            continue

        if anchor and linked.suffix == ".md":
            linked_text = linked.read_text(encoding="utf-8")
            if anchor not in anchors(linked_text):
                errors.append(f"{name}:{line}: missing anchor {target}")


def main() -> int:
    errors: list[str] = []
    for name in DOCS:
        check_file(name, errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("links are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
