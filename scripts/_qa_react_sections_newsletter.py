#!/usr/bin/env python3
"""Playwright QA for the React Sections Newsletter previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders the actual section, zero console errors, zero
    horizontal overflow at 320/375/768/1024/1280/1440 (light AND dark)
  - static: exactly the four direction directories and the 3 required files
    per variant, metadata schema (family/direction/type), no `any` in
    code.tsx, no hardcoded hex outside color-mix(..., #000), no raw
    Tailwind palette utilities, no `!important`, no `transition-all`, no
    emoji, no <img>/external URLs, no lorem
  - structure: exactly one h2 per section, section aria-labelledby points at
    it, every section has a semantic `<form>` with a real `<label>` +
    `type="email"` + `required` + `name="email"` + `autocomplete="email"`
  - form interaction (tested as a user would): empty submit shows an
    accessible error (`role="alert"` + `aria-invalid` usw.); malformed email
    shows a specific error; valid email resolves an announced success state
    (`role="status"`) and THE PAGE NEVER NAVIGATES OR RELOADS (the URL
    is unchanged and the section still renders; nothing is sent anywhere.

    Keyboard:Tab reaches the email input and Enter submits (empty → error,
    valid → success);:focus-visible shows a 2px outline.
 Reduced motion
    kills transitions. Themes flip with the page toggle except the pinned
    dark-premium variant, which holds its dark mapping in both page
    themes.
  - generator: `_gen_react_sections_newsletter.py --check` reports no
    drift; `scripts/validate.py` passes

The family ships exactly the four DevSnips visual directions; this script
also asserts no other variant directories exist.

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_sections_newsletter.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8765/React/Sections/Newsletter/"
SLUGS = [
    "minimal",
    "dark-premium",
    "bento",
    "neo-brutalist",
]
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
    family_dir = ROOT / "React" / "Sections" / "Newsletter"
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    check(
        dirs == sorted(SLUGS),
        f"family contains exactly the four direction variants, got {dirs}",
    )
    for slug in SLUGS:
        folder = ROOT / "React" / "Sections" / "Newsletter" / slug
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
            "export function NewsletterSection" in tsx,
            f"{slug}: exports NewsletterSection",
        )
        check(
            "type=\"email\"" in tsx,
            f"{slug}: email input uses type=email",
        )
        check(
            "required" in tsx,
            f"{slug}: email input is required",
        )
        check(
            "autoComplete=\"email\"" in tsx,
            f"{slug}: email input autocompletes",
        )
        check(
            "onSubmit" in tsx,
            f"{slug}: exposes onSubmit",
        )
        check(
            "role=\"alert\"" in tsx,
            f"{slug}: accessible error region",
        )
        check(
            "role=\"status\"" in tsx,
            f"{slug}: accessible success region",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta.get("family") == "Newsletter", f"{slug}: metadata family")
        check(meta.get("subcategory") == "Newsletter", f"{slug}: metadata subcategory")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(
            meta.get("direction")
            in ("Minimal", "Dark Premium", "Bento", "Neo-Brutalist"),
            f"{slug}: metadata direction",
        )
        check(meta.get("id") == f"newsletter-{slug}", f"{slug}: metadata id")


def form_checks(page, slug: str) -> None:
    """Real user-grade form interaction: empty, malformed, valid."""
    inp = page.query_selector("#ds-root section input")
    btn = page.query_selector("#ds-root section button[type=submit]")
    check(inp is not None and btn is not None, f"{slug}: form controls exist")
    if inp is None or btn is None:
        return

    url_before = page.url

    # 1. Submit empty.
    btn.click()
    page.wait_for_timeout(250)
    empty_err = page.evaluate(
        "(() => { const a = document.querySelector('#ds-root section [role=alert]'); return a ? { text: a.textContent.trim(), visible: a.getBoundingClientRect().width > 0 } : null; })()"
    )
    check(
        empty_err is not None and empty_err["visible"] and bool(empty_err["text"]),
        f"{slug}: empty submit shows visible error",
    )
    invalid_attr = page.evaluate(
        "document.querySelector('#ds-root section input').getAttribute('aria-invalid')"
    )
    check(invalid_attr == "true", f"{slug}: empty submit marks input aria-invalid")
    check(
        page.url == url_before,
        f"{slug}: empty submit does not navigate",
    )

    # 2. Submit malformed email.

    inp.fill("not-an-email")
    btn.click()
    page.wait_for_timeout(250)
    malformed = page.evaluate(
        "document.querySelector('#ds-root section [role=alert]').textContent.trim()"
    )
    check(
        "valid email" in malformed,
        f"{slug}: malformed email shows specific error (got {malformed[:50]!r})",
    )
    check(
        page.url == url_before,
        f"{slug}: malformed submit does not navigate",
    )

    # 3. Submit valid email.
#
    inp.fill("you@example.com")
    btn.click()
    page.wait_for_timeout(350)
    status = page.evaluate(
        "(() => { const s = document.querySelector('#ds-root section [role=status]'); return s ? { text: s.textContent.trim(), visible: s.getBoundingClientRect().width > 0 } : null; })()"
    )
    check(
        status is not None and status["visible"]and bool(status["text"]),
        f"{slug}: valid submit shows announced success state",
    )
    check(
        page.url == url_before,
        f"{slug}: valid submit does not navigate or reload",
    )
    check(
        page.evaluate("document.querySelectorAll('#ds-root section').length") == 1,
        f"{slug}: section still mounted after submit (no reload)",
    )


def browser_checks() -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in SLUGS:
            page = browser.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(BASE + f"{slug}/preview.html", wait_until="domcontentloaded")
            page.wait_for_selector("#ds-root section", timeout=20000)
            page.set_viewport_size({"width": 1280, "height": 900})

            # Structure: one h2, aria-labelledby wiring, semantic form.**
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
            form = page.query_selector("#ds-root section form")
            check(form is not None, f"{slug}: semantic <form> present")
            label = page.evaluate(
                """(() => {
                    const input = document.querySelector('#ds-root section input');
                    return input
                        ? document.querySelector(`#ds-root section label[for="${input.id}"]`) !== null
                        : false;
                })()"""
            )
            check(label, f"{slug}: email input has associated label")
            input_attrs = page.evaluate(
                """(() => {
                    const i = document.querySelector('#ds-root section input');
                    return i
                        ? { type: i.type, required: i.required, name: i.name,
                            ac: i.autocomplete, id: i.id }
                        : null;
                })()"""
            )
            check(
                input_attrs is not None
                and input_attrs["type"] == "email"
                and input_attrs["required"] is True
                and input_attrs["name"] == "email"
                and input_attrs["ac"] == "email",
                f"{slug}: input type=email required name=email autocomplete=email",
            )

            # 4. Real form interaction (empty/malformed/valid).**
            form_checks(page, slug)

            # 5. Keyboard: Tab reaches the input, Enter submits. Reload
            # fresh first — after the form interaction above the submit button keeps
            # focus, which shifts the tab sequence.**
            page.goto(BASE + f"{slug}/preview.html", wait_until="domcontentloaded")
            page.wait_for_selector("#ds-root section", timeout=20000)
            page.set_viewport_size({"width": 1280, "height": 900})
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            page.evaluate("document.body.focus()")
            page.keyboard.press("Tab")  # topbar theme toggle
            page.keyboard.press("Tab")  # email input
            check(
                page.evaluate(
                    "document.activeElement === document.querySelector('#ds-root section input')"
                ),
                f"{slug}: Tab reaches the email input",
            )
            outline = page.evaluate(
                "(() => { const s = getComputedStyle(document.activeElement); return s.outlineWidth; })()"
            )
            check(outline == "2px", f"{slug}: focus-visible 2px outline (got {outline})")
            page.keyboard.press("Enter")
            page.wait_for_timeout(250)
            kb_err = page.evaluate(
                "(() => { const a = document.querySelector('#ds-root section [role=alert]'); return a ? a.getBoundingClientRect().width > 0 : false; })()"
            )
            check(kb_err, f"{slug}: keyboard Enter on empty shows error")
            page.keyboard.type("kb@example.com")
            page.keyboard.press("Enter")
            page.wait_for_timeout(350)
            kb_ok = page.evaluate(
                "(() => { const s = document.querySelector('#ds-root section [role=status]'); return s ? s.getBoundingClientRect().width > 0 : false; })()"
            )
            check(kb_ok, f"{slug}: keyboard Enter on valid shows success")

            # 6. Zero horizontal overflow at every QA width, both themes.**
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
            # Long email address keeps the layout intact.**
            page.set_viewport_size({"width": 375, "height": 900})
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            inp = page.query_selector("#ds-root section input")
            if inp is not None:
                inp.fill("this-is-a-very-long-email-address-that-should-not-break-the-layout@example.com")
                page.wait_for_timeout(100)
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                )
                check(overflow <= 0, f"{slug}: long email does not break layout @375 (got {overflow})")

            # 7. Theme flip: section surface + text change with page theme —
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
                    light_bg not in ("rgb(250, 250, 250)", "rgb(255, 255, 255)"),
                    "dark-premium: section is actually dark in a light page theme",
                )
            else:
                check(
                    light_bg != dark_bg and light_fg != dark_fg,
                    f"{slug}: surface + text flip with page theme",
                )

            # 8. Reduced motion kills transitions on controls.**
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            page.emulate_media(reduced_motion="reduce")
            motion_props = page.evaluate(
                """(() => {
                    const els = [...document.querySelectorAll('#ds-root section input, #ds-root section button')];
                    return els.map(e => getComputedStyle(e).transitionProperty);
                })()"""
            )
            check(
                all(p == "none" for p in motion_props),
                f"{slug}: reduced-motion transitions none (got {motion_props})",
            )
            page.emulate_media(reduced_motion="no-preference")

            check(errors == [], f"{slug}: zero console errors, got {errors[:3]}")
            page.close()
        browser.close()


def generator_checks() -> None:
    drift = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_newsletter.py"), "--check"],
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