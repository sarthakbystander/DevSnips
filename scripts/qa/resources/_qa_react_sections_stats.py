#!/usr/bin/env python3
"""Playwright QA for the React Sections Stats previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders the actual section, zero console errors, zero
    horizontal overflow at 320/375/768/1024/1280/1440 (light AND dark)
  - static: exactly the 3 required files per variant, metadata schema
    (family/direction/type), no `any` in code.tsx, no hardcoded hex outside
    color-mix(..., #000), no raw Tailwind palette utilities, no `!important`,
    no `transition-all`, no emoji, no inline style props, no <img>/external
    URLs, no lorem ipsum
  - structure: exactly one h2 per section, section aria-labelledby points at
    it, every big numeric value uses tabular-nums (§5.3)
  - themes: light/dark page toggle flips computed section surface + text
    colors; the `dark-premium` variant keeps its pinned dark mapping
    in both page themes
  - focus: keyboard focus shows a 2px focus-visible outline on interactive
    elements (`minimal` and `bento` are intentionally action-free)
  - motion: prefers-reduced-motion kills transitions
  - generator: `_gen_react_sections_stats.py --check` reports no drift;
    `scripts/validate.py` passes

The family ships exactly the four DevSnips visual directions; this script
also asserts no other variant directories exist.

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_sections_stats.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8765/React/Sections/Stats/"
SLUGS = [
    "minimal",
    "dark-premium",
    "bento",
    "neo-brutalist",
]
ACTION_FREE = {"minimal", "bento"}
WIDTHS = [320, 375, 768, 1024, 1280, 1440]

checks = 0
failures: list[str] = []


def check(cond: bool, label: str) -> None:
    global checks
    checks += 1
    if not cond:
        failures.append(label)
        print("FAIL:", label)


def static_checks() -> None:
    palette = re.compile(
        r"\b(?:bg|text|border|fill|stroke|from|to|via)-(?:slate|gray|zinc|"
        r"neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|"
        r"cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d"
    )
    hex_lit = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    emoji = re.compile(
        "[\U0001F000-\U0001FAFF☀-➿\U00020000-\U0002FFFF]", re.UNICODE
    )
    family_dir = ROOT / "React" / "Sections" / "Stats"
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    check(dirs == sorted(SLUGS), f"exactly four variant directories, got {dirs}")
    for slug in SLUGS:
        folder = ROOT / "React" / "Sections" / "Stats" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exact 3-file shape, got {files}",
        )
        tsx = (folder / "code.tsx").read_text()
        check(
            not re.search(r":\s*any\b|<any>|\bas\s+any\b", tsx),
            f"{slug}: no `any`",
        )
        # `#000` inside color-mix hover darkening is the one sanctioned
        # literal (React/Sections/DESIGN_TOKENS.md §2) — remove it, then
        # scan for everything else.
        stripped = tsx.replace("#000", "")
        check(
            not hex_lit.search(stripped),
            f"{slug}: no hex literals outside color-mix",
        )
        check(not palette.search(tsx), f"{slug}: no raw palette utilities")
        check("!important" not in tsx, f"{slug}: no !important")
        check("transition-all" not in tsx, f"{slug}: no transition-all")
        check(not emoji.search(tsx), f"{slug}: no emoji")
        check('style={' not in tsx, f"{slug}: no inline style props")
        check("<img" not in tsx, f"{slug}: no <img> elements")
        check(
            "http://" not in tsx and "https://" not in tsx,
            f"{slug}: no external URLs",
        )
        check(
            "lorem" not in tsx.lower(),
            f"{slug}: no lorem ipsum",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta.get("family") == "Stats", f"{slug}: metadata family")
        check(meta.get("subcategory") == "Stats", f"{slug}: metadata subcategory")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(
            meta.get("direction")
            in ("Minimal", "Dark Premium", "Bento", "Neo-Brutalist"),
            f"{slug}: metadata direction",
        )
        check(meta.get("id") == f"stats-{slug}", f"{slug}: metadata id")


def browser_checks() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in SLUGS:
            page = browser.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(BASE + f"{slug}/preview.html", wait_until="networkidle")
            page.wait_for_selector("section", timeout=15000)

            # Structure: one h2, aria-labelledby wiring.
            h2_count = page.evaluate(
                "document.querySelectorAll('#ds-root section h2').length"
            )
            check(h2_count == 1, f"{slug}: exactly one h2 in the section")
            labelled = page.evaluate(
                """(() => {
                    const s = document.querySelector('#ds-root section');
                    const id = s.getAttribute('aria-labelledby');
                    return !!id && !!document.getElementById(id);
                })()"""
            )
            check(labelled, f"{slug}: section aria-labelledby resolves")
            # §11.3: 3–4 numbers minimum, §5.3: big numeric data (≥24px
            # rendered glyphs) must use tabular-nums.
            stat_count = page.evaluate(
                "document.querySelectorAll('#ds-root section .tabular-nums').length"
            )
            check(stat_count >= 3, f"{slug}: at least 3 stat values (got {stat_count})")
            tabular = page.evaluate(
                """(() => {
                    const s = document.querySelector('#ds-root section');
                    return [...s.querySelectorAll('p, span, dd')]
                        .filter(el => el.children.length === 0
                            && /\\d/.test(el.textContent)
                            && parseFloat(getComputedStyle(el).fontSize) >= 24)
                        .every(el => getComputedStyle(el).fontVariantNumeric
                            .includes('tabular-nums'));
                })()"""
            )
            check(tabular, f"{slug}: big numeric values use tabular-nums")

            # Zero horizontal overflow at every QA width, both themes.
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                for theme in ("light", "dark"):
                    page.evaluate(
                        "t => document.documentElement.setAttribute('data-theme', t)",
                        theme,
                    )
                    overflow = page.evaluate(
                        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                    )
                    check(
                        overflow <= 0,
                        f"{slug}: no h-overflow @ {width}px {theme} (got {overflow})",
                    )

            # Theme flip: section surface + text change with page theme —
            # except the pinned Dark Premium variant, which must hold dark.
            page.set_viewport_size({"width": 1280, "height": 900})

            def section_colors(theme: str):
                page.evaluate(
                    "t => document.documentElement.setAttribute('data-theme', t)",
                    theme,
                )
                return page.evaluate(
                    """(() => {
                        const s = document.querySelector('#ds-root section');
                        const cs = getComputedStyle(s);
                        return [cs.backgroundColor, cs.color];
                    })()"""
                )

            light_bg, light_fg = section_colors("light")
            dark_bg, dark_fg = section_colors("dark")
            if slug == "dark-premium":
                check(
                    light_bg == dark_bg and light_fg == dark_fg,
                    "dark-premium: pinned dark mapping holds across page themes",
                )
                check(
                    light_bg != "rgb(250, 250, 250)",
                    "dark-premium: section is actually dark in a light page theme",
                )
            else:
                check(
                    light_bg != dark_bg and light_fg != dark_fg,
                    f"{slug}: surface + text flip with page theme",
                )

            # Focus-visible ring on the first interactive element.
            page.evaluate(
                "document.documentElement.setAttribute('data-theme', 'light')"
            )
            focusable = page.query_selector(
                "#ds-root section a[href], #ds-root section button"
            )
            if slug in ACTION_FREE:
                # These compositions are intentionally action-free.
                check(
                    focusable is None,
                    f"{slug}: no interactive elements (by design)",
                )
            elif focusable is not None:
                focusable.focus()
                outline = focusable.evaluate(
                    "el => getComputedStyle(el).outlineWidth"
                )
                check(outline == "2px", f"{slug}: focus-visible 2px outline (got {outline})")
            else:
                check(False, f"{slug}: at least one interactive element")

            # Reduced motion kills transitions.
            page.emulate_media(reduced_motion="reduce")
            transitioned = page.query_selector(
                "#ds-root section a[href], #ds-root section button, #ds-root section [class*='transition']"
            )
            if transitioned is not None:
                prop = transitioned.evaluate(
                    "el => getComputedStyle(el).transitionProperty"
                )
                check(prop == "none", f"{slug}: reduced-motion transition-property none (got {prop})")
            page.emulate_media(reduced_motion="no-preference")

            check(errors == [], f"{slug}: zero console errors, got {errors[:3]}")
            page.close()

        browser.close()


def generator_checks() -> None:
    drift = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_stats.py"), "--check"],
        capture_output=True,
        text=True,
    )
    check(drift.returncode == 0, "generator --check reports no drift")
    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        capture_output=True,
        text=True,
    )
    check(validate.returncode == 0, "scripts/validate.py passes")


def main() -> int:
    static_checks()
    generator_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for failure in failures:
            print(" -", failure)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
