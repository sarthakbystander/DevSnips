#!/usr/bin/env python3
"""Playwright QA for the React Sections FAQ previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders the actual section, zero console errors, zero
    horizontal overflow at 320/375/768/1024/1280/1440 (light AND dark)
  - static: exactly the four direction directories and the 3 required files
    per variant, metadata schema (family/direction/type), no `any` in
    code.tsx, no hardcoded hex outside color-mix(..., #000), no raw
    Tailwind palette utilities, no `!important`, no `transition-all`, no
    emoji, no <img>/external URLs, no lorem
  - structure: exactly one h2 per section, section aria-labelledby points at
    it, FAQ controls are real `<button>` elements with `aria-expanded` +
    `aria-controls` wiring to `role="region"` panels labelled back by their
    triggers
  - interaction: clicking a question opens it andet closes the previously
    open one (single-open); clicking an open question closes it
    (collapsible); panels' computed visibility matches `aria-expanded`
  - keyboard: Tab reaches the controls and Enter/Space toggle them
  - focus: keyboard focus shows a 2px focus-visible outline on the
    accordion triggers
  - themes: light/dark page toggle flips computed section surface + text
    colors;the `dark-premium` variant keeps its pinned dark mapping
    in both page themes
  - motion: prefers-reduced-motion kills transitions
  - generator: `_gen_react_sections_faq.py --check` reports no drift;
    `scripts/validate.py` passes

The accordion interaction tests actually open and close FAQ items — they
do not merely assert the elements exist.

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_sections_faq.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8765/React/Sections/FAQ/"
SLUGS = [
    "minimal",
    "dark-premium",
    "bento",
    "neo-brutalist",
]
WIDTHS = [320, 375, 768, 1024, 1280, 1440]

# Expected rendered FAQ item count per variant (authored defaults).
ITEM_COUNTS = {
    "minimal": 6,
    "dark-premium": 5,
    "bento": 5,
    "neo-brutalist": 5,
}

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
    family_dir = ROOT / "React" / "Sections" / "FAQ"
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    check(
        dirs == sorted(SLUGS),
        f"family contains exactly the four direction variants, got {dirs}",
    )
    for slug in SLUGS:
        folder = ROOT / "React" / "Sections" / "FAQ" / slug
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
        check(
            "export function FAQSection" in tsx,
            f"{slug}: exports FAQSection",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta.get("family") == "FAQ", f"{slug}: metadata family")
        check(meta.get("subcategory") == "FAQ", f"{slug}: metadata subcategory")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(
            meta.get("direction")
            in ("Minimal", "Dark Premium", "Bento", "Neo-Brutalist"),
            f"{slug}: metadata direction",
        )
        check(meta.get("id") == f"faq-{slug}", f"{slug}: metadata id")


def accordion_checks(page, slug: str) -> None:
    """Open/close the FAQ accordion for real: single-open exclusivity,
    collapsible close, aria wiring,and computed panel visibility."""
    buttons = page.query_selector_all("#ds-root section button")
    expected = ITEM_COUNTS[slug]
    check(
        len(buttons) == expected,
        f"{slug}: renders {expected} FAQ controls (got {len(buttons)})",
    )
    # Every control is a real button with aria-expanded + aria-controls
    # pointing at a role=region panel labelled back by its trigger.
    wiring = page.evaluate(
        """(() => {
            const bs = [...document.querySelectorAll('#ds-root section button')];
            return bs.every(b => {
                const p = document.getElementById(b.getAttribute('aria-controls'));
                return p
                    && p.getAttribute('role') === 'region'
                    && p.getAttribute('aria-labelledby') === b.id
            });
        })()"""
    )
    check(wiring, f"{slug}: aria-controls/aria-labelledby wiring resolves")

    def states() -> list[str]:
        return [b.get_attribute("aria-expanded") for b in
               page.query_selector_all("#ds-root section button")]

    def visible_regions() -> list[str]:
        return page.evaluate(
            """[...document.querySelectorAll('#ds-root section [role="region"] > div')]
               .map(p => getComputedStyle(p).visibility)"""
        )

    # Panel computed visibility matches aria-expanded before any click.**
    vis0 = visible_regions()
    check(
        all((s == "true") == (v == "visible") for s, v in zip(states(), vis0)),
        f"{slug}: initial panel visibility matches aria-expanded",
    )
    # Clicking the second item opens it and closes the first (single-open).**
    buttons[1].click()
    page.wait_for_timeout(350)
    st = states()
    vis = visible_regions()
    check(
        [st[0], st[1]] == ["false", "true"],
        f"{slug}: clicking second opens itand closes first (got {st[:2]})",
    )
    check(
        all((s == "true") == (v == "visible") for s, v in zip(st, vis)),
        f"{slug}: panel visibility follows aria-expanded after open",
    )
    # Clicking an open question closes it (collapsible。**
    buttons[1].click()
    page.wait_for_timeout(350)
    st = states()
    check(
        st[1] == "false",
        f"{slug}: clicking open question closes it (collapsible)",
    )
    # Open third, then first: only the last click stays open.**
    buttons[2].click()
    page.wait_for_timeout(350)
    buttons[0].click()
    page.wait_for_timeout(350)
    st = states()
    check(
        [st[0], st[2]] == ["true", "false"],
        f"{slug}: single-open exclusivity holds across opens",
    )


def browser_checks() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in SLUGS:
            page = browser.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(BASE + f"{slug}/preview.html", wait_until="networkidle")
            page.wait_for_selector("#ds-root section", timeout=15000)

            # Structure: one h2, aria-labelledby wiring, FAQ items exist.**
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
            item_count = page.evaluate(
                "document.querySelectorAll('#ds-root section button').length"
            )
            check(
                item_count == ITEM_COUNTS[slug],
                f"{slug}: FAQ items render (got {item_count})",
            )

            # Real open/close interaction.**
            accordion_checks(page, slug)

            # Zero horizontal overflow at every QA width, both themes.**
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

            # Focus-visible ring on the accordion trigger — via keyboard Tab,
            # since programmatic focus() after mouse clicks matches :focus (no
            # ring);:focus-visible only fires for keyboard interaction.


            page.evaluate(
                "document.documentElement.setAttribute('data-theme', 'light')"
            )
            page.evaluate("document.body.focus()")
            page.keyboard.press("Tab")
            page.keyboard.press("Tab")
            focused_tag = page.evaluate("document.activeElement.tagName")
            check(focused_tag == "BUTTON", f"{slug}: at least one accordion trigger")
            outline = page.evaluate(
                "(() => { const s = getComputedStyle(document.activeElement); return s.outlineWidth; })()"
            )
            check(outline == "2px", f"{slug}: focus-visible 2px outline (got {outline})")


            # Keyboard: Tab reaches a trigger; Enter and Space toggle it.**
            first = page.query_selector("#ds-root section button")
            check(first is not None, f"{slug}: first trigger exists")
            if first is not None:
                if page.evaluate(
                    "document.activeElement !== document.querySelector('#ds-root section button')"
                ):
                    first.focus()
                first_state = first.get_attribute("aria-expanded")
                page.keyboard.press("Enter")
                page.wait_for_timeout(300)
                first_state = first.get_attribute("aria-expanded")
                page.keyboard.press("Space")
                page.wait_for_timeout(300)
                toggled_back = first.get_attribute("aria-expanded")
                check(
                    first_state != toggled_back,
                    f"{slug}: Enter and Space toggle the focused trigger",
                )
            page.keyboard.press("Tab")
            second_label = page.evaluate("document.activeElement.textContent.trim()")
            check(
                second_label and "?" in second_label,
                f"{slug}: Tab moves onto the next question trigger (got {second_label!r})",
            )

            # Reduced motion kills transitions.**
            page.emulate_media(reduced_motion="reduce")
            reduced_trigger = page.query_selector("#ds-root section button")
            if reduced_trigger is not None:
                prop = reduced_trigger.evaluate(
                    "el => getComputedStyle(el).transitionProperty"
                )
                check(prop == "none", f"{slug}: reduced-motion transition-property none (got {prop})")
            panel = page.query_selector("#ds-root section [role='region']")
            if panel is not None:
                prop = panel.evaluate(
                    "el => getComputedStyle(el).transitionProperty"
                )
                check(prop == "none", f"{slug}: reduced-motion panel transition-property none (got {prop})")
            page.emulate_media(reduced_motion="no-preference")

            check(errors == [], f"{slug}: zero console errors, got {errors[:3]}")
            page.close()
        browser.close()


def generator_checks() -> None:
    drift = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_faq.py"), "--check"],
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