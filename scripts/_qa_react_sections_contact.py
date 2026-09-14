#!/usr/bin/env python3
"""Playwright QA for the React Sections Contact previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant renders the actual section with zero console errors and zero
    horizontal overflow at  320/375/768/1024/1280/1440 (light AND dark)
  - static: exactly the four direction directories and the 3 required files
    per variant, metadata schema, no `any`, no hex outside color-mix(..., #000),
    no raw palette utilities, no `!important`, no `transition-all`, no emoji,
    no <img>/external URLs, no lorem, no fake role=button controls
  - structure: exactly one h2, section aria-labelledby wiring, a semantic
    <form> with four typed fields (Name,Email,Company optional,Message),every
    label properly associated, native type=email + autocomplete, required
    Name/Email/Message, anda real <button type=submit>
  - form interaction (tested as a user would): submitting the empty form shows
    visible per-field errors for the required fields (`role="alert"` +
    `aria-invalid` + `aria-describedby`); malformed email shows a specific error
    and clears the other fields' errors; valid submission resolves an announced
    success state (`role="status"`);entered values are preserved across failed
    validation attempts;the page never navigates or reloads
  - network: after the page settles, form interaction fires ZERO new
    network requests — the demo never transmits anything anywhere
  - keyboard: Tab reaches a form field and Enter submits (empty -> error,
    valid -> success);:focus-visible shows a 2px outline;;reduced
    motion kills transitions;;themes flip with the page toggle except the pinned
    dark-premium variant, which holds its dark mapping in both page themes
  - generator: `_gen_react_sections_contact.py --check` reports no drift;
    `scripts/validate.py` passes

The family ships exactly the four DevSnips visual directions; this script
also asserts no other variant directories exist. Run from the repo root
with a static server on :8765:

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
SLUGS = ["minimal", "dark-premium", "bento", "neo-brutalist"]
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
    check(
        dirs == sorted(SLUGS),
        f"family contains exactly the four direction variants, got {dirs}",
    )
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
        check("role=\"alert\"" in tsx, f"{slug}: accessible error regions")
        check("role=\"status\"" in tsx, f"{slug}: accessible success region")
        check("aria-describedby" in tsx, f"{slug}: errors are aria-describedby-wired")
        check("aria-invalid" in tsx, f"{slug}: fields carry aria-invalid on error")
        check("onSubmit" in tsx, f"{slug}: exposes onSubmit")
        check("noValidate" in tsx, f"{slug}: custom validation via noValidate")
        check("type=\"email\"" in tsx, f"{slug}: email field uses type=email")
        check("autoComplete: \"email\"" in tsx, f"{slug}: email autocompletes")
        check("type=\"submit\"" in tsx, f"{slug}: real submit button")
        check('role="button"' not in tsx, f"{slug}: no fake role=button controls")

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


def _field_attrs(page, name: str):
    return page.evaluate(
        """(name) => {
            const form = document.querySelector('#ds-root section form');
            if (!form) return null;
            const el = form.querySelector(`[name="${name}"]`);
            if (!el) return null;
            return {
                required: el.required,
                type: el.type,
                autocomplete: el.autocomplete,
                invalid: el.getAttribute('aria-invalid'),
                describedby: el.getAttribute('aria-describedby'),
            };
        }""",
        name,
    )


def _visible_alert_texts(page):
    return page.evaluate(
        """(() => {
            const alerts = [...document.querySelectorAll('#ds-root section [role="alert"]')];
            return alerts
                .filter(a => a.getBoundingClientRect().width > 0)
                .map(a => a.textContent.trim());
        })()"""
    )


def _visible_status_text(page):
    return page.evaluate(
        """(() => {
            const s = document.querySelector('#ds-root section [role="status"]');
            return s && s.getBoundingClientRect().width > 0
                ? s.textContent.trim()
                : null;
        })()"""
    )


def marker_survives(page):
    return page.evaluate(
        "document.querySelector('#ds-root section').dataset.qaMarker === 'contact-qa'"
    )


def form_checks(page, slug: str) -> None:
    """Real user-grade form behavior: structure, labels, invalid, valid,
    preservation, navigation, zero network on interaction."""
    form = page.query_selector("#ds-root section form")
    check(form is not None, f"{slug}: semantic <form> present")
    if form is None:
        return

    controls = page.evaluate(
        """(() => {
            const form = document.querySelector('#ds-root section form');
            const els = [...form.querySelectorAll('input, textarea')];
            return els.map(el => el.name);
        })()"""
    )
    check(
        sorted(controls) == ["company", "email", "message", "name"],
        f"{slug}: four typed fields present (got {sorted(controls)})",
    )
    fields_ok = page.evaluate(
        """(() => {
            const form = document.querySelector('#ds-root section form');
            const els = [...form.querySelectorAll('input, textarea')];
            return els.every(el => {
                const label = document.querySelector(`label[for="${el.id}"]`);
                return label && label.textContent.trim().length > 0;
            });
        })()"""
    )
    check(fields_ok, f"{slug}: every field has an associated visible label")

    email_ok = page.evaluate(
        """(() => {
            const form = document.querySelector('#ds-root section form');
            const el = form.querySelector('[name="email"]');
            return el && el.type === 'email' && el.required === true
                && el.autocomplete === 'email';
        })()"""
    )
    check(email_ok, f"{slug}: email type=email required autocomplete=email")

    req_name = _field_attrs(page, "name") or {}
    req_email = _field_attrs(page, "email") or {}
    req_msg = _field_attrs(page, "message") or {}
    req_co = _field_attrs(page, "company") or {}
    check(
        req_name.get("required") and req_email.get("required")and req_msg.get("required")
        and not req_co.get("required"),
        f"{slug}: name/email/message required, company optional",
    )

    url_before = page.url

    page.evaluate("document.querySelector('#ds-root section').dataset.qaMarker = 'contact-qa'")
    submit = page.query_selector("#ds-root section button[type=submit]")
    check(submit is not None, f"{slug}: submit button exists")
    if submit is None:
        return

    submit.click()
    page.wait_for_timeout(250)
    errs = _visible_alert_texts(page)
    check(
        len(errs) >= 3,
        f"{slug}: empty submit shows visible errors (got {errs[:6]})",
    )
    for name in ("name", "email", "message"):
        attrs = _field_attrs(page, name) or {}
        check(
            attrs.get("invalid") == "true",
            f"{slug}: empty submit marks {name} aria-invalid",
        )
        db = attrs.get("describedby") or ""
        if db:
            check(
                page.evaluate("id => !!id && !!document.getElementById(id)", db),
                f"{slug}: {name} error is aria-describedby-resolved",
            )
    company = _field_attrs(page, "company") or {}
    check(
        not company.get("invalid"),
        f"{slug}: optional company stays valid-on-empty",
    )
    check(
        page.url == url_before and marker_survives(page),
        f"{slug}: empty submit does not navigate or reload",
    )

    page.fill("#ds-root section form [name='name']", "Ada Lovelace")
    page.fill("#ds-root section form [name='email']", "not-an-email")
    page.fill("#ds-root section form [name='message']", "We need help scoping an editor SDK.")
    submit.click()
    page.wait_for_timeout(250)
    errs = _visible_alert_texts(page)
    check(
        any("valid email" in e for e in errs),
        f"{slug}: malformed email shows specific error (got {errs[:6]})",
    )
    check(
        not any("Enter your" in e for e in errs),
        f"{slug}: malformed email clears other fields' errors",
    )
    email_a = _field_attrs(page, "email") or {}
    name_a = _field_attrs(page, "name") or {}
    check(email_a.get("invalid") == "true", f"{slug}: malformed email marks email invalid")
    check(not name_a.get("invalid"), f"{slug}: cleared name no longer invalid")
    preserved = page.evaluate(
        """(() => {
            const form = document.querySelector('#ds-root section form');
            return {
                name: form.querySelector('[name="name"]').value,
                email: form.querySelector('[name="email"]').value,
                message: form.querySelector('[name="message"]').value,
            };
        })()"""
    )
    check(
        preserved == {
            "name": "Ada Lovelace",
            "email": "not-an-email",
            "message": "We need help scoping an editor SDK.",
        },
        f"{slug}: entered values preserved after failed validation",
    )
    check(
        page.url == url_before and marker_survives(page),
        f"{slug}: malformed submit does not navigate or reload",
    )

    page.fill("#ds-root section form [name='email']", "ada@example.dev")
    page.fill("#ds-root section form [name='company']", "Analytical Engines")
    submit.click()
    page.wait_for_timeout(350)
    status = _visible_status_text(page)
    check(
        bool(status) and "Thanks" in (status or ""),
        f"{slug}: valid submit shows announced success state (got {status!r})",
    )
    check(_visible_alert_texts(page) == [], f"{slug}: no visible errors after valid submit")
    email_ok2 = _field_attrs(page, "email") or {}
    check(not email_ok2.get("invalid"), f"{slug}: valid submit clears aria-invalid")
    check(
        page.url == url_before and marker_survives(page),
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
            requests: list[str] = []
            page.on(
                "request",
                lambda r: (requests.append(r.url) if r.resource_type != "document" else None),
            )

            page.goto(BASE + f"{slug}/preview.html", wait_until="domcontentloaded")
            page.wait_for_selector("#ds-root section", timeout=20000)
            page.set_viewport_size({"width": 1280, "height": 900})
            try:
                page.evaluate("document.fonts.ready.then(() => true)")
            except Exception:
                pass
            page.wait_for_timeout(400)
            requests.clear()

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
            mailto_count = page.evaluate(
                """[...document.querySelectorAll('#ds-root section a[href]')]
                   .filter(a => a.getAttribute('href').startsWith('mailto:')).length"""
            )
            check(mailto_count >= 1, f"{slug}: real mailto contact link (got {mailto_count})")

            form_checks(page, slug)
            check(
                requests == [],
                f"{slug}: form interaction fires zero new network requests (got {requests[:3]})",
            )

            page.goto(BASE + f"{slug}/preview.html", wait_until="domcontentloaded")
            page.wait_for_selector("#ds-root section", timeout=20000)
            page.set_viewport_size({"width": 1280, "height": 900})
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            page.evaluate("document.body.focus()")
            reached = False
            for _ in range(12):
                page.keyboard.press("Tab")
                tag = page.evaluate("document.activeElement.tagName.toLowerCase()")
                if tag in ("input", "textarea"):
                    reached = True
                    break
            check(reached, f"{slug}: Tab reaches a form field")
            outline = page.evaluate(
                "getComputedStyle(document.activeElement).outlineWidth"
            )
            check(outline == "2px", f"{slug}: focus-visible 2px outline (got {outline})")
            page.keyboard.press("Enter")
            page.wait_for_timeout(250)
            kb_err = page.evaluate(
                """(() => {
                    return [...document.querySelectorAll('#ds-root section [role="alert"]')]
                        .some(a => a.getBoundingClientRect().width > 0);
                })()"""
            )
            check(kb_err, f"{slug}: keyboard Enter on empty form shows error")
            page.keyboard.type("Keyboard Case")
            page.evaluate("document.querySelector('#ds-root section form [name=\"email\"]').focus()")
            page.keyboard.type("kb@example.dev")
            page.evaluate(
                "document.querySelector('#ds-root section form [name=\"message\"]').value = 'Short keyboard message.'"
            )
            page.keyboard.press("Enter")
            page.wait_for_timeout(350)
            kb_ok = page.evaluate(
                """(() => {
                    const s = document.querySelector('#ds-root section [role="status"]');
                    return s ? s.getBoundingClientRect().width > 0 : false;
                })()"""
            )
            check(kb_ok, f"{slug}: keyboard Enter on valid form shows success")

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
                        overflow <=  0,
                        f"{slug}: no h-overflow @ {width}px {theme} (got {overflow})",
                    )

            page.set_viewport_size({"width": 375, "height": 900})
            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            page.fill(
                "#ds-root section form [name='email']",
                "this-is-a-very-long-email-address-that-should-not-break-the-layout@example.dev",
            )
            page.wait_for_timeout(100)
            overflow = page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            check(overflow <=  0, f"{slug}: long email does not break layout @375 (got {overflow})")

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

            page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
            page.emulate_media(reduced_motion="reduce")
            motion_props = page.evaluate(
                """(() => {
                    const els = [...document.querySelectorAll(
                        '#ds-root section input, #ds-root section textarea, #ds-root section button, #ds-root section a'
                    )];
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
        [sys.executable, str(ROOT / "_gen_react_sections_contact.py"), "--check"],
        capture_output=True,
        text=True,
    )
    check(drift.returncode ==  0, "generator --check reports no drift")
    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        capture_output=True,
        text=True,
    )
    check(validate.returncode ==  0, "scripts/validate.py passes")


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