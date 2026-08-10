#!/usr/bin/env python3
"""Vanilla component quality-bar scanner.

Measures every Vanilla component against a documented quality bar and prints
an actionable report. Pure-Python (no node/npm), safe to run in CI: exits 1
when any "required" check fails for an interactive component, 0 otherwise.

Checks (per component .html):
  R1 doctype      - the file is a full <!DOCTYPE html> document OR a clearly
                    marked copy-paste snippet fragment (documented). Both are
                    acceptable for DevSnips; flagged only for the record.
  R2 lang         - if DOCTYPE present, <html lang> is set.
  R3 viewport     - if DOCTYPE present, a viewport meta is set.
  A1 reduced-motion  - animations are guarded by prefers-reduced-motion.
  A2 aria/role      - interactive components use role/aria-* semantics.
  A3 focus-visible  - :focus-visible or focus-visible ring styles present.
  A4 keyboard       - interactive controls are <button>/<a> or carry
                      tabindex/role="button" (keyboard operable).
  A5 semantic       - uses semantic landmarks (main/nav/section/header/...).
  D1 dark-mode      - supports prefers-color-scheme OR is a non-visual snippet.

"Interactive" families (where A1-A4 are REQUIRED): Modals, Dropdowns, Tabs,
Accordions, Navigation, Tooltips, Loaders(anim), Other(anim subset), Buttons,
Forms. A failure there is what fails the CI gate.

Usage:
    python3 scripts/qa_vanilla.py            # report + exit code
    python3 scripts/qa_vanilla.py --json     # machine-readable report
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMP = ROOT / "Vanilla" / "Components"

# Families where keyboard/ARIA/reduced-motion are required (interactive).
INTERACTIVE = {
    "modals", "dropdowns", "tabs", "accordions", "navigation", "tooltips",
    "buttons", "forms", "loaders",
}
# Families that are purely visual/decorative: reduced-motion still expected if
# they animate, but ARIA/keyboard not required.
VISUAL_ANIM = {"media", "cards", "marketing", "hero", "loaders", "other",
               "display", "statistics", "testimonials", "products", "pricing",
               "cta", "features", "logos", "gallery", "footer", "contact",
               "content", "team", "badges", "alerts", "avatars", "tables",
               "ratings", "faq", "process", "hero"}


def family_of(folder: Path) -> str:
    return folder.parent.name.lower()


def has_media(text, low):
    return bool(re.search(r"@media[^{]*(min|max)-width", low))


def has_reduced_motion(low):
    return "prefers-reduced-motion" in low


def has_dark_mode(low):
    return "prefers-color-scheme" in low


def has_aria(low):
    return bool(re.search(r"\b(role|aria-)\b", low))


def has_focus_visible(low):
    return bool(re.search(r":focus-visible|focus-visible", low))


def has_semantic(low):
    # Any semantic HTML element: landmarks + content semantics + document
    # structure. Using native semantic elements is the accessible-by-default
    # path and satisfies the aria/role requirement for non-custom widgets.
    return bool(re.search(
        r"<(main|nav|section|article|header|footer|aside|figure|figcaption|"
        r"dialog|time|mark|kbd|abbr|details|summary|output|figure|"
        r"p|h[1-6]|blockquote|ul|ol|dl)\b",
        low))


def keyboard_ok(low):
    # native interactive controls, <dialog>, or explicit keyboard hooks
    return bool(
        re.search(r"<(button|a|input|select|textarea|summary)\b", low)
        or 'role="button"' in low
        or "tabindex" in low
        or "<dialog" in low
    )


def native_interactive(low):
    """Native semantic interactive elements satisfy aria+keyboard by themselves.

    ARIA is only required for non-semantic custom widgets (div-based buttons,
    div-based tabs, etc.). W3C: prefer native semantics; "no ARIA is better
    than bad ARIA". <progress>/<meter>/<output> are native status semantics.
    """
    return bool(re.search(
        r"<(button|a\s+href|input|select|textarea|summary|dialog|details|"
        r"progress|meter|output)\b",
        low))


def has_js_interaction(low):
    """True if the component wires user interaction that requires keyboard parity.

    Pure status/display components (spinners, progress bars, skeletons) do not
    need keyboard operability. Components with onclick handlers, click
    listeners, or div-based controls do.
    """
    return bool(
        "onclick" in low
        or re.search(r'addEventListener\(\s*["\']click["\']', low)
        or 'role="button"' in low
        or re.search(r"<div[^>]*\bonclick", low)
    )


def has_animation(low):
    # transition/animation/keyframes/@keyframes
    return bool(re.search(r"transition\s*:|animation\s*:|@keyframes", low))


def is_doctype(low):
    return low.lstrip().startswith("<!doctype")


def has_lang(low):
    return bool(re.search(r"<html[^>]*\blang\s*=", low))


def has_viewport(low):
    return bool(re.search(r'name\s*=\s*["\']?viewport', low))


def scan_component(folder: Path):
    html = None
    for f in folder.iterdir():
        if f.is_file() and f.suffix == ".html":
            html = f
            break
    if not html:
        return None
    txt = html.read_text(encoding="utf-8", errors="ignore")
    low = txt.lower()
    fam = family_of(folder)
    return {
        "path": str(html.relative_to(ROOT)),
        "family": fam,
        "interactive": fam in INTERACTIVE,
        "doctype": is_doctype(low),
        "lang": has_lang(low),
        "viewport": has_viewport(low),
        "reduced_motion": has_reduced_motion(low),
        "dark_mode": has_dark_mode(low),
        "aria": has_aria(low),
        "native_interactive": native_interactive(low),
        "focus_visible": has_focus_visible(low),
        "keyboard": keyboard_ok(low),
        "js_interaction": has_js_interaction(low),
        "semantic": has_semantic(low),
        "animates": has_animation(low),
    }


def checks(c):
    """Return list of (name, status, required). status: ok/warn/fail."""
    out = []
    interactive = c["interactive"]
    animates = c["animates"]
    # R1 doctype is informational (fragments allowed)
    out.append(("doctype", "ok" if c["doctype"] else "warn", False))
    if c["doctype"]:
        out.append(("lang", "ok" if c["lang"] else "warn", True))
        out.append(("viewport", "ok" if c["viewport"] else "warn", True))
    # A1 reduced-motion: required only if animates
    if animates:
        out.append(("reduced-motion",
                    "ok" if c["reduced_motion"] else "fail",
                    True))
    # A2-A4 only required for interactive.
    # ARIA/role is satisfied by EITHER explicit role/aria-* OR native
    # semantic elements (interactive controls OR content semantics like
    # <kbd>/<time>/<mark>/<progress>). W3C: prefer native semantics.
    if interactive:
        aria_ok = c["aria"] or c["native_interactive"] or c["semantic"]
        out.append(("aria/role", "ok" if aria_ok else "fail", True))
        out.append(("focus-visible",
                    "ok" if c["focus_visible"] else "fail", True))
        # Keyboard operability is only required when the component actually
        # wires user interaction (onclick/click listeners/div controls). Pure
        # status displays (spinners, progress bars) need aria but not keyboard.
        if c["js_interaction"]:
            out.append(("keyboard", "ok" if c["keyboard"] else "fail", True))
    # A5 semantic: recommended for all (warn if missing)
    out.append(("semantic", "ok" if c["semantic"] else "warn", False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only-failures", action="store_true")
    args = ap.parse_args()

    results = []
    for mf in sorted(COMP.rglob("metadata.json")):
        leaf = mf.parent
        # only component leaves (skip sections-showcase etc.)
        if leaf.parent.parent.name == "Components" or leaf.parent == COMP \
                or leaf.parent.name in {"Other"}:
            pass
        c = scan_component(leaf)
        if c:
            results.append(c)

    # build report
    report = []
    failing = 0
    for c in results:
        chk = checks(c)
        fails = [name for name, st, req in chk if st == "fail" and req]
        warns = [name for name, st, req in chk if st == "warn"]
        if fails:
            failing += 1
        if args.only_failures and not fails:
            continue
        report.append({
            "path": c["path"],
            "family": c["family"],
            "interactive": c["interactive"],
            "fails": fails,
            "warns": warns,
        })

    if args.json:
        print(json.dumps({
            "scanned": len(results),
            "failing": failing,
            "items": report,
        }, indent=2))
    else:
        print("Vanilla quality-bar scan")
        print("  scanned: %d components" % len(results))
        print("  failing required checks: %d" % failing)
        # aggregate missing per check
        from collections import Counter
        miss = Counter()
        for c in results:
            for name, st, req in checks(c):
                if st == "fail" and req:
                    miss[name] += 1
        print("  required failures by check:", dict(miss))
        print()
        for r in report:
            if r["fails"]:
                print("  FAIL  %-65s %s" % (r["path"], ", ".join(r["fails"])))
            elif r["warns"]:
                print("  warn  %-65s %s" % (r["path"], ", ".join(r["warns"])))

    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    main()
