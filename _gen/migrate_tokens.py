"""Deterministic Vanilla token migrator — ad-hoc values -> var(--ds-*, fallback).

Replaces hardcoded colors / spacing / radius / shadows / fonts in legacy
component HTML with `var(--ds-<token>, <original-value>)` references so the
component renders identically until `tokens.css` is themed. Every replacement
keeps the original value as the var() fallback, so this migration CANNOT
visually break a component.

Skips the 65 migrated Neo-Brutalist sections (they have their own --bg/--
surface/--radius token system + prefers-color-scheme) — those are a deliberate,
already-cohesive design system.

Usage:
    python3 -m _gen.migrate_tokens            # apply (writes files)
    DRY_RUN=1 python3 -m _gen.migrate_tokens  # report only, no writes
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMP = ROOT / "Vanilla" / "Components"
DRY = bool(__import__("os").environ.get("DRY_RUN"))

# ---- value -> token mappings (matched literally, case-insensitive for hex) ----

# Colors: map exact raw colors to token names. The fallback in var() is the
# original value, so a component using #4a90e2 keeps #4a90e2 unless themed.
COLOR_MAP = {
    # surfaces / backgrounds (light)
    "#ffffff": "--ds-surface",
    "#fff": "--ds-surface",
    "#fafafa": "--ds-surface",
    "#f5f5f5": "--ds-surface-2",
    "#f8f9fa": "--ds-surface-2",
    "#f4f4f4": "--ds-surface-2",
    "#f1f1f1": "--ds-surface-2",
    "#f7f7f7": "--ds-surface-2",
    "#eee": "--ds-surface-3",
    "#eeeeee": "--ds-surface-3",
    "#ededed": "--ds-surface-3",
    "#ddd": "--ds-border",
    "#dddddd": "--ds-border",
    "#ccc": "--ds-border-strong",
    "#cccccc": "--ds-border-strong",
    # foreground / text (dark)
    "#0a0a0a": "--ds-foreground",
    "#000000": "--ds-foreground",
    "#000": "--ds-foreground",
    "#333": "--ds-foreground",
    "#333333": "--ds-foreground",
    "#151515": "--ds-foreground",
    "#1a1a1a": "--ds-foreground",
    "#222": "--ds-foreground",
    # muted text
    "#525252": "--ds-muted",
    "#666": "--ds-muted",
    "#666666": "--ds-muted",
    "#555": "--ds-muted",
    "#555555": "--ds-muted",
    "#6b6b6b": "--ds-muted",
    "#999": "--ds-subtle",
    "#999999": "--ds-subtle",
    "#a3a3a3": "--ds-subtle",
    # accents (blues/indigos) -> --ds-accent
    "#2563eb": "--ds-accent",
    "#4a90e2": "--ds-accent",
    "#4f46e5": "--ds-accent",
    "#6366f1": "--ds-accent",
    "#6a5af9": "--ds-accent",
    "#007bff": "--ds-accent",
    "#357abd": "--ds-accent",
    "#0069d9": "--ds-accent-hover",
    # semantic
    "#4caf50": "--ds-success",
    "#16a34a": "--ds-success",
    "#2e7d32": "--ds-success",
    "#388e3c": "--ds-success",
    "#e8f5e9": "--ds-success-soft",
    "#f0fdf4": "--ds-success-soft",
    "#f44336": "--ds-danger",
    "#dc2626": "--ds-danger",
    "#c62828": "--ds-danger",
    "#d32f2f": "--ds-danger",
    "#ffebee": "--ds-danger-soft",
    "#fef2f2": "--ds-danger-soft",
    "#ffc107": "--ds-warning",
    "#d97706": "--ds-warning",
    "#fff8e1": "--ds-warning-soft",
    "#fffbeb": "--ds-warning-soft",
    # grays not yet covered
    "#f2f2f2": "--ds-surface-2",
    "#f9f9f9": "--ds-surface-2",
    "#f4f4f5": "--ds-surface-3",
    "#111": "--ds-foreground",
    "#111111": "--ds-foreground",
    "#888": "--ds-subtle",
    "#888888": "--ds-subtle",
}

# Radius: only standalone border-radius declarations (not compound corners).
RADIUS_MAP = {
    "4px": "--ds-radius-sm",
    "5px": "--ds-radius-sm",
    "6px": "--ds-radius-md",
    "8px": "--ds-radius-md",
    "10px": "--ds-radius-lg",
    "12px": "--ds-radius-lg",
    "16px": "--ds-radius-xl",
    "18px": "--ds-radius-xl",
    "24px": "--ds-radius-2xl",
    "25px": "--ds-radius-2xl",
    "28px": "--ds-radius-2xl",
    "50px": "--ds-radius-full",
    "999px": "--ds-radius-full",
    "9999px": "--ds-radius-full",
}

# Shadow: bespoke shadow strings -> token. Match the whole declaration value.
SHADOW_MAP = {
    "0 2px 5px rgba(0,0,0,0.1)": "--ds-shadow-md",
    "0 2px 5px rgba(0, 0, 0, 0.1)": "--ds-shadow-md",
    "0 4px 6px rgba(0, 0, 0, 0.1)": "--ds-shadow-md",
    "0 4px 12px rgba(0, 0, 0, 0.15)": "--ds-shadow-lg",
    "0 4px 8px 0 rgba(0, 0, 0, 0.2)": "--ds-shadow-md",
    "0 2px 4px rgba(0, 0, 0, 0.1)": "--ds-shadow-sm",
    "0 1px 2px rgba(0, 0, 0, 0.05)": "--ds-shadow-sm",
    "0px 8px 16px 0px rgba(0,0,0,0.2)": "--ds-shadow-lg",
    "0px 8px 16px 0px rgba(0,0,0,0.15)": "--ds-shadow-lg",
}

# Font family -> --ds-font-sans
FONT_MAP = {
    "Arial, sans-serif": "--ds-font-sans",
    "Arial, Helvetica, sans-serif": "--ds-font-sans",
    "Arial, Helvetica, sans-serif;": "--ds-font-sans",
    "Arial": "--ds-font-sans",
    "arial": "--ds-font-sans",
    "sans-serif": "--ds-font-sans",
}

ROOT_DEFAULTS = "  :root{\n" + "".join(
    f"  {t}:{v};\n" for t, v in [
        # compact inline fallbacks so the component is standalone
    ]) + "  }\n"


def is_section(html: str) -> bool:
    """The 65 migrated neo-brutalist sections have their own token system."""
    return "prefers-color-scheme" in html and "--bg" in html and "--radius" in html


VAR_OPEN = re.compile(r"var\(")
# a --ds-* token definition: --ds-foo:#fff  (the RHS is the token's value,
# not a usage — must NOT be wrapped)
DS_DEF = re.compile(r"--ds-[a-z0-9-]+\s*:\s*(?=#)")


def replace_colors(html: str):
    """Replace hex color VALUES in CSS declarations with var(--ds-*, fallback).
    Skips colors already inside any var(...) call AND the entire injected
    Swiss :root / @media token-definition block (those hexes ARE the token
    values, not usage)."""
    changed = 0
    # spans to skip: every var(...) and the Swiss definition block
    skip_spans = []
    for m in VAR_OPEN.finditer(html):
        depth = 1
        i = m.end()
        while i < len(html) and depth > 0:
            if html[i:i + 4] == "var(":
                depth += 1; i += 4
            elif html[i] == ")":
                depth -= 1; i += 1
            else:
                i += 1
        skip_spans.append((m.start(), i))
    sb = _find_swiss_block(html)
    if sb:
        skip_spans.append(sb)
    in_skip = [False] * len(html)
    for s, e in skip_spans:
        for j in range(s, min(e, len(html))):
            in_skip[j] = True

    def repl(match):
        nonlocal changed
        val = match.group(0)
        key = val.lower()
        if key not in COLOR_MAP:
            return val
        if in_skip[match.start()]:
            return val
        changed += 1
        return f"var({COLOR_MAP[key]}, {val})"

    html = re.sub(r"#[0-9a-fA-F]{3,8}\b", repl, html)
    return html, changed


def replace_radius(html: str):
    """Replace standalone border-radius values (single value only)."""
    changed = 0

    def repl(match):
        nonlocal changed
        val = match.group(1).strip()
        if val in RADIUS_MAP:
            changed += 1
            return f"border-radius: var({RADIUS_MAP[val]}, {val})"
        return match.group(0)

    html = re.sub(r"border-radius\s*:\s*([0-9]+px)\b", repl, html)
    return html, changed


def replace_shadows(html: str):
    """Replace bespoke box-shadow values with var(--ds-shadow-*, fallback)."""
    changed = 0

    def repl(match):
        nonlocal changed
        val = match.group(1).strip()
        if val in SHADOW_MAP:
            changed += 1
            return f"box-shadow: var({SHADOW_MAP[val]}, {val})"
        return match.group(0)

    html = re.sub(r"box-shadow\s*:\s*([^;}]*)", repl, html)
    return html, changed


def replace_fonts(html: str):
    changed = 0

    def repl(match):
        nonlocal changed
        val = match.group(1).strip().rstrip(";")
        if val in FONT_MAP:
            changed += 1
            return f"font-family: var({FONT_MAP[val]}, {val})"
        return match.group(0)

    html = re.sub(r"font-family\s*:\s*([^;}]*)", repl, html)
    return html, changed


def _find_swiss_block(html: str):
    """Return (start, end) of an existing injected Swiss block (the comment
    marker through the closing brace of the :root rule AND any following
    dark-mode @media rule), or None. Handles nested braces in @media."""
    marker = "/* DevSnips design tokens"
    ms = html.find(marker)
    if ms < 0:
        return None
    # find the first :root{ after the marker
    ridx = html.find(":root{", ms)
    if ridx < 0:
        return None
    bidx = html.find("{", ridx)
    end = _match_brace(html, bidx)
    if end < 0:
        return None
    pos = end + 1
    # skip whitespace, then an optional @media (prefers-color-scheme: dark){...}
    while pos < len(html) and html[pos] in " \t\r\n":
        pos += 1
    if html[pos:pos + 5] == "@medi".lower() or html[pos:pos + 6] == "@media":
        mbidx = html.find("{", pos)
        if mbidx >= 0:
            mend = _match_brace(html, mbidx)
            if mend >= 0:
                pos = mend + 1
    return ms, pos


def _match_brace(html: str, open_idx: int) -> int:
    """Given index of '{', return index of matching '}' (-1 if unbalanced)."""
    depth = 0
    i = open_idx
    while i < len(html):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def inject_root(html: str) -> str:
    """Inject the full Swiss design-token :root block + dark-mode override so
    every var(--ds-*) reference resolves to the Swiss value (not the original
    fallback). Injects INSIDE the first existing <style> block (before
    </style>), so no new tags are opened. Idempotent: if a Swiss block is
    already present, it is replaced with the current one (brace-matched)."""
    if "--ds-" not in html:
        return html
    block = _SWISS_BLOCK
    existing = _find_swiss_block(html)
    if existing:
        s, e = existing
        if html[s:e] == block.strip("\n"):
            return html  # already current
        return html[:s] + block + html[e:]
    if "</style>" in html:
        idx = html.index("</style>")
        return html[:idx] + block + html[idx:]
    if "</head>" in html:
        idx = html.index("</head>")
        return html[:idx] + "<style>" + block + "</style>\n" + html[idx:]
    return html + "<style>" + block + "</style>\n"


# The compact Swiss token block injected into every migrated component.
# Mirrors Vanilla/Components/tokens.css. No self-references (every value is
# a literal). Dark-mode override included so components respect the OS theme.
_SWISS_BLOCK = (
    "\n/* DevSnips design tokens (Swiss) — edit tokens.css to re-theme */\n"
    ":root{\n"
    "--ds-bg:#fff;--ds-surface:#fff;--ds-surface-2:#f7f7f7;--ds-surface-3:#ededed;"
    "--ds-foreground:#0a0a0a;--ds-muted:#525252;--ds-subtle:#a3a3a3;"
    "--ds-border:#e5e5e5;--ds-border-strong:#d4d4d4;"
    "--ds-accent:#2563eb;--ds-accent-hover:#1d4ed8;--ds-accent-fg:#fff;--ds-accent-soft:#eff6ff;"
    "--ds-success:#16a34a;--ds-success-soft:#f0fdf4;"
    "--ds-warning:#d97706;--ds-warning-soft:#fffbeb;"
    "--ds-danger:#dc2626;--ds-danger-soft:#fef2f2;"
    "--ds-info:#2563eb;--ds-info-soft:#eff6ff;"
    "--ds-font-sans:system-ui,-apple-system,'Segoe UI',Roboto,Inter,'Helvetica Neue',Arial,sans-serif;"
    "--ds-font-mono:ui-monospace,'SF Mono','JetBrains Mono',Menlo,Consolas,monospace;"
    "--ds-text-xs:.75rem;--ds-text-sm:.875rem;--ds-text-base:1rem;--ds-text-lg:1.125rem;"
    "--ds-text-xl:1.25rem;--ds-text-2xl:1.5rem;--ds-text-3xl:1.875rem;--ds-text-4xl:2.25rem;"
    "--ds-leading-tight:1.25;--ds-leading-normal:1.5;--ds-leading-relaxed:1.625;"
    "--ds-weight-normal:400;--ds-weight-medium:500;--ds-weight-semibold:600;--ds-weight-bold:700;"
    "--ds-space-0:0;--ds-space-px:1px;--ds-space-1:.25rem;--ds-space-2:.5rem;--ds-space-3:.75rem;"
    "--ds-space-4:1rem;--ds-space-5:1.25rem;--ds-space-6:1.5rem;--ds-space-8:2rem;"
    "--ds-space-10:2.5rem;--ds-space-12:3rem;--ds-space-16:4rem;"
    "--ds-radius-sm:.25rem;--ds-radius-md:.5rem;--ds-radius-lg:.75rem;--ds-radius-xl:1rem;"
    "--ds-radius-2xl:1.5rem;--ds-radius-full:9999px;"
    "--ds-shadow-sm:0 1px 2px 0 rgba(0,0,0,.05);"
    "--ds-shadow-md:0 4px 6px -1px rgba(0,0,0,.08),0 2px 4px -2px rgba(0,0,0,.05);"
    "--ds-shadow-lg:0 10px 15px -3px rgba(0,0,0,.1),0 4px 6px -4px rgba(0,0,0,.05);"
    "--ds-duration-fast:120ms;--ds-duration-normal:200ms;--ds-duration-slow:300ms;"
    "--ds-ease-out:cubic-bezier(.16,1,.3,1);--ds-ease-in-out:cubic-bezier(.4,0,.2,1);"
    "--ds-ring:0 0 0 2px #2563eb;--ds-container:1200px;--ds-gutter:1rem;\n}\n"
    "@media (prefers-color-scheme: dark){:root{"
    "--ds-bg:#0a0a0a;--ds-surface:#111;--ds-surface-2:#171717;--ds-surface-3:#1f1f1f;"
    "--ds-foreground:#fafafa;--ds-muted:#a3a3a3;--ds-subtle:#737373;"
    "--ds-border:#262626;--ds-border-strong:#404040;"
    "--ds-accent:#3b82f6;--ds-accent-hover:#60a5fa;--ds-accent-fg:#fff;--ds-accent-soft:#172554;"
    "--ds-success:#22c55e;--ds-success-soft:#052e16;"
    "--ds-warning:#f59e0b;--ds-warning-soft:#422006;"
    "--ds-danger:#ef4444;--ds-danger-soft:#450a0a;"
    "--ds-info:#3b82f6;--ds-info-soft:#172554;"
    "--ds-ring:0 0 0 2px #3b82f6;}}\n"
)


def migrate_file(path: Path, refresh: bool = False):
    html = path.read_text(encoding="utf-8")
    if is_section(html):
        return 0, 0
    original = html
    html, cc = replace_colors(html)
    html, rc = replace_radius(html)
    html, sc = replace_shadows(html)
    html, fc = replace_fonts(html)
    total = cc + rc + sc + fc
    # On refresh, always (re)inject the block even with 0 new replacements so
    # the Swiss token set stays current (e.g. new tokens added).
    if refresh and "--ds-" in html:
        html = inject_root(html)
    elif total == 0:
        return 0, 0
    else:
        html = inject_root(html)
    if html != original:
        if not DRY:
            path.write_text(html, encoding="utf-8")
        # count as a change on refresh even if 0 value replacements
        return (total if total else 1), 1
    return total, 0


def main():
    import sys
    refresh = "--refresh-blocks" in sys.argv
    total_replacements = 0
    files_changed = 0
    files_scanned = 0
    skipped_sections = 0
    for mf in sorted(COMP.rglob("metadata.json")):
        leaf = mf.parent
        html_path = next((f for f in leaf.iterdir()
                          if f.suffix == ".html"), None)
        if not html_path:
            continue
        files_scanned += 1
        html = html_path.read_text(encoding="utf-8")
        if is_section(html):
            skipped_sections += 1
            continue
        n, changed = migrate_file(html_path, refresh=refresh)
        total_replacements += n
        files_changed += changed
    mode = "DRY RUN" if DRY else "APPLIED"
    if refresh:
        mode += " (refresh-blocks)"
    print(f"migrate_tokens [{mode}]")
    print(f"  scanned: {files_scanned} component HTML files")
    print(f"  skipped sections (own token system): {skipped_sections}")
    print(f"  files changed: {files_changed}")
    print(f"  total value->token replacements: {total_replacements}")


if __name__ == "__main__":
    main()
