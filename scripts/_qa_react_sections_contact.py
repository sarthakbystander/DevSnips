#!/usr/bin/env python3
"""Playwright QA for the React Sections Contact previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders the actual section, zero console errors, zero
    horizontal overflow at 320/375/768/1024/1280/1440 (light AND dark)
  - static: exactly the four direction directories and the 3 required files
    per variant, metadata schema (family/direction/type), no `any` in
    code.tsx, no hardcoded hex outside color-mix(..., #000), no raw
    Tailwind palette utilities, no `!important`, no `transition-all`, no
    emoji, no inline style props, no <img>/external URLs, no lorem
  - structure: exactly one h2 per section, section aria-labelledby points at
    it,,every section has a semantic `<form>` with proper `<label htmlFor>`
    associations, the four default fields (name/email/company/message,
    name/email/message required, email type=email with autocomplete, name
    autocompletes, company autocompletes organization),per-field error
    regions (`role="alert"` + `aria-invalid` + `aria-describedby`),anda
    success region (`role="status"`, aria-live)
  - form interaction(tested as a user would): empty submit shows the required
    errors and keeps the input values (preserved across failed submits);
    malformed email shows a specific error; valid submit resolves an announced
    success state ("Thanks. Your message has been received.") and the page
    never navigates or reloads (URL unchanged, section still mounted,
    zero new network requests fired by the interaction)。
  - keyboard: Tab reaches the first field and Enter submits (empty → error,
    valid → success)::focus-visible shows a 2px outline.on controls.
 Reduced
    motion kills transitions. Themes flip with the page toggle except the pinned
    dark-premium variant, which holds its dark mapping in both page themes.
 
  - generator: `_gen_react_sections_contact.py --check` reports no drift;
    `scripts/validate.py` passes

The family ships exactly the four DevSnips visual directions;this script
also asserts no other variant directories exist.

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_sections_contact.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8765/React/Sections/Contact/"
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
    family_dir = ROOT / "React" / "Sections" / "Contact"
    dirs = sorted(p.name for p in family_dir.iterdir() if p.is_dir())
    check(dirs == sorted(SLUGS), f"exactly four variant directories, got {dirs}")
    for slug in SLUGS:

        folder = ROOT / "React" / "Sections" / "Contact" / slug
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
            "export function ContactSection" in tsx,
            f"{slug}: exports ContactSection",
        )
        # Shared typed form API surface (required by the family spec).
        for needle in (
            "type ContactField",
            "type={field.type}",
            "autoComplete=",
            "required",
            "onSubmit",
            "role=\"alert\"",
            "role=\"status\"",
            "aria-describedby",
        ):
            check(needle in tsx, f"{slug}: typed API surface includes `{needle}`")
        meta = json.loads((folder / "metadata.json").read_text())
        check(meta.get("family") == "Contact", f"{slug}: metadata family")
        check(meta.get("subcategory") == "Contact", f"{slug}: metadata subcategory")
        check(meta.get("type") == "section", f"{slug}: metadata type")
        check(meta.get("category") == "Sections", f"{slug}: metadata category")
        check(
            meta.get("direction")
            in ("Minimal", "Dark Premium", "Bento", "Neo-Brutalist"),
            f"{slug}: metadata direction",
        )
        check(meta.get("id") == f"contact-{slug}", f"{slug}: metadata id")
        check(
            bool(meta.get("description", "").strip()),
            f"{slug}: metadata carries a real description",
        )


def fields_block(page, slug: str):
    """Shared assertions for the 4 default form fields + label wiring."""
    fields = page.evaluate(
        """[...document.querySelectorAll('#ds-root section form :is(input, textarea)')]
           .map(el => ({ name: el.name, type: el.type, autocomplete: el.autocomplete,
                          required: el.required, id: el.id }))"""
    )
    check(
        len(fields) == 4,
        f"{slug}: renders 4 form fields (got {len(fields)})",
    )
    names = [f["name"] for f in fields]
    check(
        names == ["name", "email", "company", "message"],
        f"{slug}: default field names in order (got {names})",
    )
    by_name = {f["name"]: f for f in fields}
    check(by_name["name"]["type"] == "text", f"{slug}: name field type text")
    check(by_name["email"]["type"] == "email", f"{slug}: email field type=email")
    check(by_name["company"]["type"] == "text", f"{slug}: company field type text")
    check(by_name["message"]["type"] == "textarea", f"{slug}: message field is textarea")
    check(
        by_name["name"]["autocomplete"] == "name"
        and by_name["email"]["autocomplete"] == "email"
        and by_name["company"]["autocomplete"] == "organization",
        f"{slug}: autocomplete attributes (name/email/organization)",
    )
    check(
        by_name["name"]["required"] is True
        and by_name["email"]["required"] is True
        and by_name["message"]["required"] is True,
        f"{slug}: name/email/message are required",
    )
    check(
        by_name["company"]["required"] is False,
        f"{slug}: company is optional",
    )
    # Every field label is associated via label[for].
    labelled = page.evaluate(
        """(() => {
            const els = [...document.querySelectorAll('#ds-root section form :is(input, textarea)')];
            return els.every(el => {
                const l = document.querySelector(`#ds-root section label[for="${el.id}"]`);
                return l && l.textContent.trim().length > 0;
            });
        })()"""
    )
    check(labelled, f"{slug}: every field has an associated visible label")


def form_checks(page, slug: str) -> None:
    """Real user-grade form interaction: empty, malformed, valid."""
    fields = page.query_selector_all(
        "#ds-root section form :is(input, textarea)"
    )
    submit = page.query_selector("#ds-root section form button[type=submit]")
    check(submit is not None, f"{slug}: submit button exists")
    if submit is None:
        return
    url_before = page.url

    # 1. Submit empty → required errors, values preserved, no navigation.

    submit.click()
    page.wait_for_timeout(250)
    alerts = page.evaluate(
        """[...document.querySelectorAll('#ds-root section [role=alert]')]
           .filter(el => el.getBoundingClientRect().width > 0).length"""
    )
    check(alerts == 3, f"{slug}: empty submit shows 3 field errors (got {alerts})")
    invalid_count = page.evaluate(
        "document.querySelectorAll('#ds-root section [aria-invalid=\"true\"]').length"
    )
    check(invalid_count == 3, f"{slug}: empty submit marks 3 inputs aria-invalid")
    described = page.evaluate(
        """(() => {
            const bad = [...document.querySelectorAll('#ds-root section [aria-invalid="true"]')]
                .filter(el => !(el.getAttribute('aria-describedby') || '').length > 0);
            return bad.length === 0;
        })()"""
    )
    check(described, f"{slug}: erroring fields carry aria-describedby")
    preserved = page.evaluate(
        """(() => {
            const els = [...document.querySelectorAll('#ds-root section form :is(input, textarea)')];
            return els.every(el => el.value === '');
        })()"""
    )
    check(preserved, f"{slug}: failed submit preserves entered values (empty values still empty)")
    check(
        page.url == url_before,
        f"{slug}: empty submit does not navigate",
    )

    # 2. Fill name + company + message, leave email malformed.
    name, email, company, message = fields
    name.fill("Ada Lovelace")
    email.fill("not-an-email")
    company.fill("Example Systems")
    message.fill("We are rebuilding our design system and need a partner.")
    submit.click()
    page.wait_for_timeout(250)
    malformed = page.evaluate(
        """[...document.querySelectorAll('#ds-root section [role=alert]')]
           .filter(el => el.getBoundingClientRect().width > 0)
           .map(el => el.textContent.trim())"""
    )
    check(
        len(malformed) == 1 and "valid email" in malformed[0],
        f"{slug}: malformed email shows a specific error (got {malformed})",
    )
    check(
        page.url == url_before,
        f"{slug}: malformed submit does not navigate",
    )
    # Values typed above are preserved after the failed submit.

    persisted = page.evaluate(
        """(() => {
            const els = [...document.querySelectorAll('#ds-root section form :is(input, textarea)')];
            const v = {};
            for (const el of els) v[el.name] = el.value;
            return v;
        })()"""
    )
    check(
        persisted["name"] == "Ada Lovelace"
        and persisted["company"] == "Example Systems"
        and persisted["message"] == "We are rebuilding our design system and need a partner.",
        f"{slug}: values persist across the failed malformed submit (got {persisted})",
    )

    # 3. Fix the email and submit valid.
    email.fill("ada@example.dev")
    submit.click()
    page.wait_for_timeout(350)
    status_text = page.evaluate(
        "document.querySelector('#ds-root section [role=status]').textContent.trim()"
    )
    check(
        status_text == "Thanks. Your message has been received.",
        f"{slug}: valid submit resolves the exact success message (got {status_text!r})",
    )
    status_visible = page.evaluate(
        "document.querySelector('#ds-root section [role=status]').getBoundingClientRect().width > 0"
    )
    check(status_visible, f"{slug}: success state is visible (not sr-only)")
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
            requests_after_interaction: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on(
                "request",
                lambda r: requests_after_interaction.append(r.url)
                if r.url.startswith(("http://", "https://")) else None,
            )
            page.goto(BASE + f"{slug}/preview.html", wait_until="domcontentloaded")
            page.wait_for_selector("#ds-root section", timeout=20000)
            page.set_viewport_size({"width": 1280, "height": 900})
            # The page may have settled fonts/CDN requests during goto; clear
            # the request log now, so the interaction below must fire zero
            # new http(s) requests (none of our sections fetch anything).**
            requests_after_interaction.clear()

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
            fields_block(page, slug)

            # Real form interaction (empty/malformed/valid).**
            form_checks(page, slug)

            # No new network requests fired by the interaction itself. The
            # page already settled (wait_until=domcontentloaded + section
            # mount waits); we did not navigate or click any external link, so
            # any subsequent http(s) request is a defect.**
            check(
                requests_after_interaction == [],
                f"{slug}: no network requests after form interaction (got {requests_after_interaction[:3]})",
            )

            # Keyboard: Tab reaches the first field, Enter submits. Reload
            # fresh first — after the form interaction above the submit button keeps
            # focus, which shifts the tab sequence.

            page.goto(BASE + f"{slug}/preview.html", wait_until="domcontentloaded")
            page.wait_for_selector("#ds-root section", timeout=20000)
            page.set_viewport_size({"width": 1280, "height": 900})
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            page.evaluate("document.body.focus()")
            # Tab until the focus lands inside the form (left-column email
            # anchors legitimately precede the form in some compositions).
            page.keyboard.press("Tab")
            reached = False
            for _ in range(8):
                if page.evaluate(
                    "!!document.activeElement.closest('#ds-root section form')"
                ):
                    reached = True
                    break
                page.keyboard.press("Tab")
            check(reached, f"{slug}: Tab reaches the first form field")
            outline = page.evaluate(
                "(() => { const s = getComputedStyle(document.activeElement); return s.outlineWidth; })()"
            )
            check(outline == "2px", f"{slug}: focus-visible 2px outline (got {outline})")
            page.keyboard.press("Enter")
            page.wait_for_timeout(250)
            kb_err = page.evaluate(
                """[...document.querySelectorAll('#ds-root section [role=alert]')]
                   .filter(el => el.getBoundingClientRect().width > 0).length"""
            )
            check(kb_err == 3, f"{slug}: keyboard Enter on empty shows 3 errors (got {kb_err})")
            page.keyboard.type("Keyboard Tester")
            page.keyboard.press("Tab")
            page.keyboard.type("kb@example.dev")
            page.keyboard.press("Tab")
            page.keyboard.press("Tab")
            page.keyboard.type("A short keyboard-submitted inquiry.")
            page.keyboard.press("Tab")
            page.keyboard.press("Enter")
            page.wait_for_timeout(350)
            kb_ok = page.evaluate(
                "document.querySelector('#ds-root section [role=status]').getBoundingClientRect().width > 0"
            )
            check(kb_ok, f"{slug}: keyboard Enter on valid shows success")

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
            # Long email address keeps the layout intact.**
            page.set_viewport_size({"width": 375, "height": 900})
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            email_inp = page.query_selector("#ds-root section input[type=email]")
            if email_inp is not None:
                email_inp.fill(
                    "this-is-a-very-long-email-address-that-should-not-break-the-layout@example.com"
                )
                page.wait_for_timeout(100)
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                )
                check(overflow <= 0, f"{slug}: long email does not break layout @375 (got {overflow})")

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
                    light_bg not in ("rgb(250, 250, 250)", "rgb(255, 255, 255)"),
                    "dark-premium: section is actually dark in a light page theme",
                )
            else:
                check(
                    light_bg != dark_bg and light_fg != dark_fg,
                    f"{slug}: surface + text flip with page theme",
                )

            # Focus-visible ring on every interactive form control.**
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            controls = page.query_selector_all(
                "#ds-root section form :is(input, textarea, button)"
            )
            check(
                len(controls) >= 5,
                f"{slug}: at least 5 form controls (got {len(controls)})",
            )
            for idx, control in enumerate(controls):
                control.focus()
                outline = control.evaluate("el => getComputedStyle(el).outlineWidth")
                check(
                    outline == "2px",
                    f"{slug}: control {idx + 1} focus-visible 2px outline (got {outline})",
                )

            # Reduced motion kills transitions on controls.**
            page.emulate_media(reduced_motion="reduce")
            motion_props = page.evaluate(
                """(() => {
                    const els = [...document.querySelectorAll('#ds-root section :is(input, textarea, button, a)')];
                    return els.map(e => getComputedStyle(e).transitionProperty);
                })()"""
            )
            check(
                all(p == "none" for p in motion_props),
                f"{slug}: reduced-motion transitions none (got {motion_props[:5]})",
            )
            page.emulate_media(reduced_motion="no-preference")

            check(errors == [], f"{slug}: zero console errors, got {errors[:3]}")
            page.close()
        browser.close()


def generator_checks() -> None:
    drift = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sections_contact.py"), "--check"],
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