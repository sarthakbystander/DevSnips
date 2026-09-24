#!/usr/bin/env python3
"""Guard the path references quoted in agent-facing Markdown docs.

Those docs are the authoritative map of the repository for agents, and they
quote concrete paths inline in backticks (`` `scripts/tooling/validators/validate.py` ``).
When a file or directory moves, those references rot silently — the existing
validators only inspect metadata/index/architecture, never the docs that
describe them.

Scanned documents:

  - `agents/resources/*.md` — the repository-side deep agent docs
  - `library/**/AGENTS.md` — per-resource agent guidance the CLI ships to users
  - `integrations/mcp/**/*.md` — MCP server agent docs

This checks every path-like backticked token in those files and fails when it
resolves to nothing. Resolution tries, in order:

  - the repository root
  - each doc's own context directories (`agents/resources/`, `scripts/`,
    `integrations/mcp/` and its package dir, `docs/`, `cli/`, `library/`)
  - `library/<token>` (the registry is tech-first, without the `library/` prefix)

Markdown prose and fenced code blocks are elided first; a doc can additionally
fence an intentional list of non-existent paths between
`<!-- path-check: ignore-start -->` and `<!-- path-check: ignore-end -->`
markers (used by the "known gaps" ledger in `architecture.md`).

Run:  python3 scripts/tooling/validators/check_agent_doc_paths.py
Exit: 0 when every path-like token resolves, 1 otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # -> repo root
DOC_GLOBS = (
    "agents/resources/*.md",
    "library/**/AGENTS.md",
    "integrations/mcp/**/*.md",
)

BACKTICK = re.compile(r"`([^`]+)`")

# Fenced code blocks (``` / ~~~) contain backticks that would otherwise shift
# inline-code pairing for the rest of the file, so they are removed before
# scanning. Paths quoted inside a fence are illustrative, not references.
FENCE = re.compile(r"^\s*(```|~~~)")


def strip_fences(text: str) -> str:
    """Blank out fenced code blocks, preserving line numbers."""
    out = []
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def strip_ignored(text: str) -> str:
    """Blank lines inside `ignore-start` / `ignore-end` regions."""
    out = []
    ignoring = False
    for line in text.splitlines():
        if IGNORE_START in line:
            ignoring = True
            out.append("")
            continue
        if IGNORE_END in line:
            ignoring = False
            out.append("")
            continue
        out.append("" if ignoring else line)
    return "\n".join(out)


def prepare(text: str) -> str:
    """Apply all elisions while preserving line numbers."""
    return strip_ignored(strip_fences(text))


# A backtick span may quote several paths at once (`agents/a/, agents/b/`).
TOKEN_SPLIT = re.compile(r"[,\s]+")

# A doc may deliberately name a path that does not exist (a "known stale
# references" ledger). Such regions are fenced with explicit markers so the
# check stays accurate without the ledger being silently wrong.
IGNORE_START = "<!-- path-check: ignore-start -->"
IGNORE_END = "<!-- path-check: ignore-end -->"

# Bases a relative token may be resolved against, beyond the repo root.
CONTEXT_BASES = [
    ROOT,
    ROOT / "agents" / "resources",
    ROOT / "scripts",
    ROOT / "integrations" / "mcp",
    ROOT / "integrations" / "mcp" / "src" / "devsnips_mcp",
    ROOT / "docs",
    ROOT / "cli",
    ROOT / "library",
]

# Directories at the repository root. A token anchored to one of these makes a
# concrete location claim and must resolve.
ROOT_PREFIXES = {
    "library", "scripts", "agents", "cli", "docs", "integrations",
    "reports", ".github", "website",
}

# Tokens that look like paths but are deliberately not repository paths.
# Matched by exact value or as a leading prefix; each has a stated reason.
ALLOWED_NON_PATHS = {
    # Example git branch names quoted in conventions.md.
    "feat/your-component": "example git branch name",
    "chore/complete-library-path-integration": "example git branch name",
    # CLI init output: created at run time in a user project, gitignored here.
    "devsnips/": "CLI init output, gitignored",
    # The published static site is a generated, uncommitted surface.
    "website/": "generated published site, not committed",
}

# Leading bracket/quote noise, and trailing punctuation, trimmed from a token
# before checking. `.` is deliberately not a leading trim character: it would
# corrupt `.github/...` and `./src/...`.
LEAD_TRIM = "`()[]{}<>\"'"
TRAIL_TRIM = "`()[]{}<>.,;:\"'"


def normalize(raw: str) -> str:
    return raw.strip().lstrip(LEAD_TRIM).rstrip(TRAIL_TRIM)


def is_checkable(token: str) -> bool:
    """True when a backticked token makes a concrete repository location claim.

    Only tokens anchored to a repository-root directory are checked. This keeps
    the tool predictable: prose such as ``HTML/CSS/JS``, illustrative manifest
    entries such as ``pages/index.html``, project-relative ``./src/...`` paths,
    and URLs are all ignored.
    """
    if not token:
        return False
    if any(token.startswith(p) for p in ALLOWED_NON_PATHS):
        return False
    if token.startswith(("http://", "https://")):
        return False
    if any(c in token for c in "<>{}[]|*?`"):  # globs, placeholders, unions
        return False
    if "..." in token or " " in token:
        return False
    if token.startswith(("./", "../")):  # project-relative, not repo-relative
        return False
    parts = token.rstrip("/").split("/")
    return parts[0] in ROOT_PREFIXES


def resolves(token: str) -> bool:
    for candidate in {token, token.rstrip("/")}:
        for base in CONTEXT_BASES:
            if (base / candidate).exists():
                return True
    # Registry paths are tech-first: Tailwind/Components/... lives under library/.
    if (ROOT / "library" / token.strip("/")).exists():
        return True
    return False


def main():
    files = sorted({p for glob in DOC_GLOBS for p in ROOT.glob(glob)})
    if not files:
        print(f"No files matched {DOC_GLOBS}", file=sys.stderr)
        return 1

    failures = 0
    checked = 0
    for path in files:
        text = prepare(path.read_text(encoding="utf-8"))
        file_failures = []
        for match in BACKTICK.finditer(text):
            span = match.group(1).strip()
            for raw in TOKEN_SPLIT.split(span):
                token = normalize(raw)
                if not is_checkable(token):
                    continue
                checked += 1
                if not resolves(token):
                    line_no = text[: match.start()].count("\n") + 1
                    file_failures.append((line_no, token))
        if file_failures:
            failures += len(file_failures)
            print(f"{path.relative_to(ROOT)}: {len(file_failures)} unresolved path(s)")
            for line_no, token in file_failures:
                print(f"  line {line_no}: {token}")

    if failures:
        print(f"\nFAILED: {failures} unresolved path reference(s).")
        return 1
    print(f"OK: all path references in scanned agent docs resolve ({checked} checked, "
          f"{len(files)} files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
