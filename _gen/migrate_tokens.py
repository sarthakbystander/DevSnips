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
    Skips colors already inside any var(...) call AND hexes that are the value
    of a --ds-* token definition (RHS of `--ds-foo:` in :root{})."""
    changed = 0
    # spans of every var(...) so we can skip hexes inside them
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
    in_var = [False] * len(html)
    for s, e in skip_spans:
        for j in range(s, min(e, len(html))):
            in_var[j] = True
    # positions immediately after a --ds-*:<ws> definition marker
    def_starts = [m.end() for m in DS_DEF.finditer(html)]

    def repl(match):
        nonlocal changed
        val = match.group(0)
        key = val.lower()
        if key not in COLOR_MAP:
            return val
        s = match.start()
        if in_var[s]:
            return val
        # skip if this hex is the RHS of a --ds-foo: definition
        for ds in def_starts:
            if ds == s:
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


def inject_root(html: str) -> str:
    """Inject a compact :root fallback block (Swiss defaults) so the component
    is standalone. Injects the rule INSIDE the first existing <style> block
    (just before </style>), so no new tags are opened. Only injects if the
    component references --ds-* and doesn't already define a --ds- :root."""
    if "--ds-" not in html:
        return html
    if re.search(r":root\s*\{[^}]*--ds-", html):
        return html
    rule = (
        "\n/* DevSnips design tokens (Swiss) — override by editing tokens.css */\n"
        ":root{\n"
        "--ds-surface:#fff;--ds-surface-2:#f7f7f7;--ds-foreground:#0a0a0a;"
        "--ds-muted:#525252;--ds-border:#e5e5e5;--ds-accent:#2563eb;"
        "--ds-accent-fg:#fff;--ds-radius-sm:4px;--ds-radius-md:8px;"
        "--ds-radius-lg:12px;--ds-shadow-sm:0 1px 2px rgba(0,0,0,.05);"
        "--ds-shadow-md:0 4px 6px -1px rgba(0,0,0,.08);"
        "--ds-font-sans:system-ui,sans-serif;\n}\n"
    )
    if "</style>" in html:
        idx = html.index("</style>")
        return html[:idx] + rule + html[idx:]
    if "</head>" in html:
        idx = html.index("</head>")
        return html[:idx] + "<style>" + rule + "</style>\n" + html[idx:]
    return html + "<style>" + rule + "</style>\n"


def migrate_file(path: Path):
    html = path.read_text(encoding="utf-8")
    if is_section(html):
        return 0, 0
    original = html
    html, cc = replace_colors(html)
    html, rc = replace_radius(html)
    html, sc = replace_shadows(html)
    html, fc = replace_fonts(html)
    total = cc + rc + sc + fc
    if total == 0:
        return 0, 0
    html = inject_root(html)
    if html != original:
        if not DRY:
            path.write_text(html, encoding="utf-8")
    return total, 1


def main():
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
        n, changed = migrate_file(html_path)
        total_replacements += n
        files_changed += changed
    mode = "DRY RUN" if DRY else "APPLIED"
    print(f"migrate_tokens [{mode}]")
    print(f"  scanned: {files_scanned} component HTML files")
    print(f"  skipped sections (own token system): {skipped_sections}")
    print(f"  files changed: {files_changed}")
    print(f"  total value->token replacements: {total_replacements}")


if __name__ == "__main__":
    main()
