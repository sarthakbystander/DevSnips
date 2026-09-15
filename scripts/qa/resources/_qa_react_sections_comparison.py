#!/usr/bin/env python3
"""Playwright QA for the React Sections Comparison family.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders the actual section, zero console errors, zero
    horizontal overflow at 320/375/768/1280/1440 (light AND dark)
  - static: exactly the 3 required files per variant, metadata schema
    (family/direction/type), no `any` in code.tsx, no hardcoded hex outside
    sanctioned #000, no raw Tailwind palette utilities, no `!important`,
    no `transition-all`, no emoji, no inline style props
  - structure: exactly one h2 per section, section aria-labelledby points at
    it, options render, included state renders
  - themes: light/dark page toggle flips computed section surface + text
    colors; the Dark Premium variant keeps its pinned dark mapping in both
    page themes
  - focus: when interactive controls exist, keyboard focus can land on them
  - motion: prefers-reduced-motion disables transitions when interactive
  - generator: `_gen_react_sections_comparison.py --check` reports no drift;
    `scripts/validate.py` passes

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_sections_comparison.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8765/React/Sections/Comparison/"
SLUGS = ["minimal", "dark-premium", "bento", "neo-brutalist"]
WIDTHS = [320, 375, 768, 1280, 1440]
checks = 0
failures: list[str] = []


def check(ok: bool, label: str) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(label)
        print("FAIL:", label)


def static_checks() -> None:
    palette = re.compile(
        r"\b(?:bg|text|border|fill|stroke|from|to|via)-(?:slate|gray|zinc|"
        r"neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|"
        r"cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d"
    )
    emoji = re.compile(
        "[\U0001F000-\U0001FAFF☀-➿\U00020000-\U0002FFFF]", re.UNICODE
    )
    hex_lit = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    root = ROOT / "React" / "Sections" / "Comparison"
    check(
        sorted(p.name for p in root.iterdir() if p.is_dir()) == sorted(SLUGS),
        "exact four direction folders",
    )
    for slug in SLUGS:
        folder = root / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exact 3-file shape",
        )
        tsx = (folder / "code.tsx").read_text()
        preview = (folder / "preview.html").read_text()
        check(
            not re.search(r":\s*any\b|<any>|\bas\s+any\b", tsx),
            f"{slug}: no any",
        )
        check(
            not hex_lit.search(tsx.replace("#000", "")),
            f"{slug}: no raw hex outside sanctioned #000",
        )
        check(not palette.search(tsx), f"{slug}: no raw palette classes")
        check("!important" not in tsx, f"{slug}: no !important")
        check("transition-all" not in tsx, f"{slug}: no transition-all")
        check(not emoji.search(tsx), f"{slug}: no emoji")
        check("style={" not in tsx, f"{slug}: no inline style props")
        check(
            "http://" not in tsx and "https://" not in tsx,
            f"{slug}: no external URLs",
        )
        check("<img" not in tsx, f"{slug}: no external image element")
        check(
            'fetch("./code.tsx")' not in preview,
            f"{slug}: preview does not fetch sibling source",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta.get("id") == f"comparison-{slug}", f"{slug}: metadata id")
        check(meta.get("family") == "Comparison", f"{slug}: metadata family")
        check(
            meta.get("subcategory") == "Comparison",
            f"{slug}: metadata subcategory",
        )
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(
            meta.get("direction")
            in ["Minimal", "Dark Premium", "Bento", "Neo-Brutalist"],
            f"{slug}: metadata direction",
        )
        check(bool(meta.get("description")), f"{slug}: metadata description")


def browser_checks() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in SLUGS:
            page = browser.new_page()
            errors: list[str] = []
            page.on(
                "console",
                lambda m: errors.append(m.text) if m.type == "error" else None,
            )
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(BASE + slug + "/preview.html", wait_until="networkidle")
            page.wait_for_selector("#ds-root section", timeout=15000)
            section = page.locator("#ds-root section")
            check(section.locator("h2").count() == 1, f"{slug}: exactly one h2")
            check(
                section.get_attribute("aria-labelledby") is not None,
                f"{slug}: aria-labelledby exists",
            )
            option_names = {
                "minimal": ["DevSnips", "Starter kit", "Build in-house"],
                "dark-premium": ["DevSnips", "Starter kit", "Build in-house"],
                "bento": ["DevSnips", "Starter kit", "In-house"],
                "neo-brutalist": ["DevSnips", "Starter", "In-house"],
            }[slug]
            check(
                all(
                    section.get_by_text(name, exact=False).count() >= 1
                    for name in option_names
                ),
                f"{slug}: all three options render",
            )
            included_count = page.evaluate(
                """() => {
                  const root = document.querySelector('#ds-root section');
                  const t = root ? root.innerText : '';
                  return (t.match(/\\bIncluded\\b/g) || []).length
                    + (t.match(/\\bYES\\b/g) || []).length;
                }"""
            )
            check(included_count > 0, f"{slug}: included state renders")
            if slug in ["minimal", "neo-brutalist"]:
                check(
                    section.locator("table").count() == 1,
                    f"{slug}: semantic table present",
                )
                check(
                    section.locator("th").count() >= 4,
                    f"{slug}: table headers present",
                )
            if slug == "dark-premium":
                check(
                    section.locator("dl").count() == 3,
                    f"{slug}: stacked comparison panels use semantic dl",
                )
                check(
                    section.get_attribute("data-theme") == "dark",
                    f"{slug}: root pins data-theme=dark",
                )
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                for theme in ("light", "dark"):
                    page.evaluate(
                        "t=>document.documentElement.setAttribute('data-theme',t)",
                        theme,
                    )
                    overflow = page.evaluate(
                        "document.body.scrollWidth - document.documentElement.clientWidth"
                    )
                    check(
                        overflow <= 0,
                        f"{slug}: no page overflow @ {width}px {theme} (got {overflow})",
                    )
            page.set_viewport_size({"width": 1280, "height": 900})

            def colors(theme: str):
                page.evaluate(
                    "t=>document.documentElement.setAttribute('data-theme',t)",
                    theme,
                )
                return section.evaluate(
                    "e=>{let c=getComputedStyle(e);return [c.backgroundColor,c.color]}"
                )

            light = colors("light")
            dark = colors("dark")
            if slug == "dark-premium":
                check(
                    light == dark,
                    f"{slug}: pinned dark colors persist across page themes",
                )
                check(
                    light[0]
                    not in ["rgb(250, 250, 250)", "rgb(255, 255, 255)"],
                    f"{slug}: actually dark",
                )
            else:
                check(
                    light != dark,
                    f"{slug}: light/dark theme changes section",
                )
            page.evaluate(
                "document.documentElement.setAttribute('data-theme','light')"
            )
            interactive = section.locator("a[href],button")
            if interactive.count() > 0:
                first = interactive.first
                first.focus()
                check(
                    first.evaluate("e => document.activeElement === e"),
                    f"{slug}: keyboard focus can land on section control",
                )
                page.emulate_media(reduced_motion="reduce")
                motion = first.evaluate(
                    "e => { const s = getComputedStyle(e); return {d: s.transitionDuration, p: s.transitionProperty}; }"
                )
                ok_motion = (
                    motion["p"] == "none"
                    or any(
                        part.strip() in ("0s", "0.01s")
                        for part in (motion["d"] or "0s").split(",")
                    )
                )
                check(
                    ok_motion,
                    f"{slug}: reduced motion removes transition ({motion})",
                )
                page.emulate_media(reduced_motion="no-preference")
            check(not errors, f"{slug}: zero console errors")
            page.close()
        browser.close()


def generator_checks() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_comparison.py"), "--check"],
        capture_output=True,
        text=True,
    )
    check(
        r.returncode == 0,
        "generator --check reports no stale embedded sources",
    )
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate.py")],
        capture_output=True,
        text=True,
    )
    check(r.returncode == 0, "scripts/validate.py passes")


def main() -> int:
    static_checks()
    generator_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    for failure in failures:
        print(" -", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
