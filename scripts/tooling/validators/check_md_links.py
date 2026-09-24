#!/usr/bin/env python3
"""Check every relative link in the repository's Markdown for a real target.

Motivation: resource READMEs cross-link sibling variants and token docs. When a
family is renamed (e.g. `Basic Button/` -> `basic-button/`) those links silently
rot, and nothing in the existing validators notices because they only check
metadata/index/architecture — not Markdown.

Checks each `[text](target)` where `target` is a repository-relative path:
  - resolves relative to the containing file
  - skips `http(s)://` and `mailto:` links
  - verifies the resolved path exists (file or directory)
  - when the target is a Markdown file and carries a `#fragment`, verifies the
    fragment matches a heading slug in that file (GitHub-style slugs)

Run:  python3 scripts/tooling/validators/check_md_links.py
Exit: 0 when every relative link resolves, 1 otherwise.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]  # -> repo root

# Directories that never contain repository Markdown worth checking.
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".agent_tmp"}

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")


def _slug(heading: str) -> str:
    """GitHub-compatible heading slug: lowercase, drop punctuation, spaces→-."""
    text = re.sub(r"`([^`]*)`", r"\1", heading)  # inline code -> its content
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> link text
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)  # drop punctuation
    return re.sub(r"\s", "-", text).strip("-")


def heading_slugs(path: Path):
    """Return the set of anchor slugs defined in a Markdown file, plus deduped -1 variants."""
    slugs = {}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    for line in text.splitlines():
        m = HEADING.match(line)
        if not m:
            continue
        base = _slug(m.group(1))
        if not base:
            continue
        count = slugs.get(base, 0)
        slugs[base] = count + 1
        if count:
            slugs[f"{base}-{count}"] = 1
    return set(slugs)


def markdown_files():
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def check_file(path: Path):
    """Return a list of (line_no, text, target) for links that do not resolve."""
    broken = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return broken

    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        # Split off any query/fragment before resolving the path portion.
        path_part, _, fragment = target.partition("#")
        path_part = path_part.split("?", 1)[0]
        path_part = unquote(path_part)
        fragment = unquote(fragment)
        if path_part.startswith("/"):
            resolved = ROOT / path_part.lstrip("/")
        elif path_part:
            resolved = (path.parent / path_part).resolve()
        else:
            resolved = path  # bare `#anchor` refers to this file
        line_no = text[: match.start()].count("\n") + 1
        if not resolved.exists():
            broken.append((line_no, match.group(0), target))
            continue
        if fragment and resolved.is_file() and resolved.suffix == ".md":
            if fragment not in heading_slugs(resolved):
                broken.append((line_no, match.group(0), target))
    return broken


def main():
    failures = 0
    total_links = 0
    for md in markdown_files():
        broken = check_file(md)
        if broken:
            failures += len(broken)
            rel = md.relative_to(ROOT)
            print(f"{rel}: {len(broken)} broken link(s)")
            for line_no, raw, target in broken:
                print(f"  line {line_no}: {raw} -> {target}")
        total_links += 1

    if failures:
        print(f"\nFAILED: {failures} broken Markdown link(s).")
        return 1
    print(f"OK: all relative Markdown links resolve ({total_links} files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
