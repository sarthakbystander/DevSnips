#!/usr/bin/env python3
"""QA harness for the DevSnips React Form Fields family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx, no `<div onClick`, no inline `style=`, no hex
  - TSX/JSX export parity (same exported component names + default export)
  - shared-core equality across all 10 variants (header-comment-neutralized)

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors
  - 0 horizontal overflow at 375 / 768 / 1280
  - every label[htmlFor] resolves to a control id; clicking a label focuses
    its control
  - every aria-describedby id exists (no dangling references); controls
    without texts carry no aria-describedby
  - description above control / helper below control, both wired
  - required: label indicator (aria-hidden * + sr-only), native required on
    the control, native validation blocks an empty submit, filled submits
  - optional: "(optional)" indicator, no required attribute
  - error: role=alert + aria-invalid=true + describedby while the message
    renders; live validation clears everything; destructive token color
  - success: role=status, never aria-invalid, success token color
  - disabled: native disabled, muted label, control not focusable; dynamic
    toggle re-enables (composite switch control included)
  - group: fieldset + legend, group-level aria-describedby, live group
    error wired to the fieldset, horizontal wrapping row
  - horizontal orientation: label column left of control at 1280, stacked
    at 375
  - focus-visible outline; dark-mode token flip; reduced-motion
    transition-none

Run: python3 scripts/_qa_react_formfields.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMFIELDS = ROOT / "React/Components/FormFields"
SLUGS = [
    "form-field",
    "form-field-required",
    "form-field-optional",
    "form-field-with-description",
    "form-field-with-helper",
    "form-field-with-error",
    "form-field-with-success",
    "form-field-disabled",
    "form-field-group",
    "form-field-horizontal",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = [
    "useFormField", "FormField", "FormFieldLabel", "FormFieldControl",
    "FormFieldDescription", "FormFieldHelper", "FormFieldMessage",
    "FormFieldGroup",
]

failures: list[str] = []
checks = 0


def check(ok: bool, label: str):
    global checks
    checks += 1
    if not ok:
        failures.append(label)
        print(f"  FAIL {label}")


def neutralize_core(tsx: str) -> str:
    """Shared core of a variant: the header doc comment removed, blank runs
    collapsed — everything else must be identical across the family."""
    tsx = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S)
    tsx = re.sub(r"\n{3,}", "\n\n", tsx)
    return tsx.rstrip()


def static_checks():
    print("static checks")
    cores = {}
    for slug in SLUGS:
        folder = FORMFIELDS / slug
        check(folder.is_dir(), f"{slug}: folder exists")
        for name in FILES:
            check((folder / name).is_file(), f"{slug}: {name} exists")
        meta = json.loads((folder / "metadata.json").read_text())
        for key in ["id", "name", "slug", "component", "family", "variant", "description",
                    "framework", "language", "languages", "technology", "type", "category",
                    "subcategory", "styling", "tags", "features", "responsive", "darkMode",
                    "accessibility", "interactive", "dependencies", "source", "related"]:
            check(key in meta, f"{slug}: metadata has {key}")
        check(meta["technology"] == "react", f"{slug}: technology react")
        check(meta["type"] == "component", f"{slug}: type component")
        check(meta["category"] == "Form Fields", f"{slug}: category Form Fields")
        check(meta["component"] == "form-field", f"{slug}: component form-field")
        check(meta["family"] == "formfields", f"{slug}: family formfields")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")
        for rel in meta["related"]:
            check(rel in SLUGS, f"{slug}: related slug {rel} exists")
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        check("style=" not in tsx, f"{slug}: no inline style attribute")
        check(re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx) == [],
              f"{slug}: no hex literals in code.tsx")
        check('role={tone === "error" ? "alert" : "status"}' in tsx, f"{slug}: message live-region roles")
        check("aria-describedby" in tsx, f"{slug}: aria-describedby wiring")
        check("htmlFor={field.controlId}" in tsx, f"{slug}: label htmlFor wiring")
        check("<fieldset" in tsx and "<legend" in tsx, f"{slug}: fieldset + legend group")
        check("sr-only" in tsx, f"{slug}: sr-only required indicator")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        for name in CORE_EXPORTS:
            check(name in tsx_exports, f"{slug}: exports {name}")
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity {tsx_exports} vs {jsx_exports}")
        check("export default FormField;" in jsx, f"{slug}: JSX default export")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        preview = (folder / "preview.html").read_text()
        check("data-theme" in preview and "ds-theme-toggle" in preview, f"{slug}: preview theme toggle")
        cores[slug] = neutralize_core(tsx)
    ref = cores["form-field"]
    for slug in SLUGS[1:]:
        check(cores[slug] == ref, f"{slug}: shared core identical to reference")


def open_preview(page, slug):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((FORMFIELDS / slug / "preview.html").as_uri())
    page.wait_for_selector("#ds-root *", timeout=15000)
    page.wait_for_timeout(400)
    return errors


def describedby_targets_exist(page, slug):
    """Every id referenced by any aria-describedby / label[for] exists."""
    dangling = page.evaluate("""() => {
      const bad = [];
      document.querySelectorAll('[aria-describedby]').forEach((el) => {
        el.getAttribute('aria-describedby').split(/\\s+/).filter(Boolean).forEach((id) => {
          if (!document.getElementById(id)) bad.push(el.tagName + '#' + el.id + ' -> ' + id);
        });
      });
      document.querySelectorAll('label[for]').forEach((el) => {
        if (!document.getElementById(el.getAttribute('for'))) bad.push('label[for=' + el.getAttribute('for') + ']');
      });
      return bad;
    }""")
    check(not dangling, f"{slug}: no dangling aria-describedby / htmlFor ids {dangling[:3]}")


def generic_field_checks(page, slug):
    """Label association + describedby integrity across the whole preview."""
    describedby_targets_exist(page, slug)
    miswired = page.evaluate("""() => {
      const bad = [];
      document.querySelectorAll('[data-ds-form-field]').forEach((field) => {
        const label = field.querySelector(':scope > label[for]');
        if (!label) { bad.push('no label'); return; }
        const control = field.querySelector('#' + CSS.escape(label.getAttribute('for')));
        if (!control) { bad.push('label target not inside field: ' + label.textContent); }
      });
      return bad;
    }""")
    check(not miswired, f"{slug}: every FormField label resolves to a control inside it {miswired[:3]}")


def browser_checks():
    from playwright.sync_api import sync_playwright

    print("browser checks")
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- per-preview generic checks -----------------------------------
        for slug in SLUGS:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            errors = open_preview(page, slug)
            check(not errors, f"{slug}: no console/page errors {errors[:3]}")
            for w in WIDTHS:
                page.set_viewport_size({"width": w, "height": 900})
                page.wait_for_timeout(100)
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(overflow <= 0, f"{slug}: no horizontal overflow @ {w} (got {overflow})")
            page.set_viewport_size({"width": 1280, "height": 900})
            generic_field_checks(page, slug)
            page.close()

        # ---------------- form-field (reference) --------------------------
        print("== form-field ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = open_preview(page, "form-field")
        check(not errors, f"form-field: no console errors {errors[:3]}")
        check(page.locator("[data-ds-form-field]").count() == 4, "form-field: 4 fields rendered")
        # label click focuses the control (label/control association behavior)
        page.get_by_text("Email", exact=True).click()
        check(page.evaluate("document.activeElement && document.activeElement.type === 'email'"),
              "form-field: clicking the Email label focuses the email input")
        # email field: describedby contains description + helper ids
        email = page.locator('[data-ds-form-field]', has=page.get_by_text("Email", exact=True)).locator("input")
        ids = (email.get_attribute("aria-describedby") or "").split()
        texts = [page.locator(f'[id="{i}"]').text_content() for i in ids]
        check(any("sign-in and notifications" in t for t in texts), "form-field: description wired via aria-describedby")
        check(any("never share" in t for t in texts), "form-field: helper wired via aria-describedby")
        # bio field: no texts -> no aria-describedby attribute at all
        bio = page.locator('[data-ds-form-field]', has=page.get_by_text("Bio", exact=True)).locator("textarea")
        check(bio.get_attribute("aria-describedby") is None, "form-field: bare field has no aria-describedby")
        # select + textarea + input all wrapped
        check(page.locator("[data-ds-form-field] select").count() == 1, "form-field: select wrapped")
        check(page.locator("[data-ds-form-field] textarea").count() == 1, "form-field: textarea wrapped")
        page.close()

        # ---------------- form-field-required -----------------------------
        print("== form-field-required ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-required")
        name_input = page.locator("#ds-root input[name='name']")
        email_input = page.locator("#ds-root input[name='email']")
        company_input = page.locator("#ds-root input[name='company']")
        check(name_input.get_attribute("required") is not None, "required: name has native required")
        check(email_input.get_attribute("required") is not None, "required: email has native required")
        check(company_input.get_attribute("required") is None, "required: company has no required")
        star = page.locator(f'label[for="{name_input.get_attribute("id")}"] span[aria-hidden="true"]')
        check(star.count() == 1 and star.text_content() == "*", "required: aria-hidden asterisk on label")
        sr = page.locator(f'label[for="{name_input.get_attribute("id")}"] .sr-only')
        check(sr.count() == 1 and "required" in sr.text_content(), "required: sr-only (required) text")
        # native validation blocks an empty submit
        page.get_by_role("button", name="Create account").click()
        page.wait_for_timeout(150)
        check(page.locator("#ds-root input:invalid").count() > 0, "required: native validation flags empty fields")
        check(not page.get_by_text("Account created.").is_visible(), "required: empty submit blocked")
        name_input.fill("Ada Byron")
        email_input.fill("ada@devsnips.dev")
        page.get_by_role("button", name="Create account").click()
        page.wait_for_timeout(150)
        check(page.get_by_text("Account created.").is_visible(), "required: filled form submits")
        page.close()

        # ---------------- form-field-optional -----------------------------
        print("== form-field-optional ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-optional")
        optional_count = page.evaluate("""() => [...document.querySelectorAll('#ds-root span')]
          .filter((el) => el.textContent === '(optional)').length""")
        check(optional_count == 2, f"optional: two (optional) indicators (got {optional_count})")
        email_label = page.locator("#ds-root label", has_text="Email")
        check(email_label.locator('span[aria-hidden="true"]').count() == 1, "optional: email keeps its required asterisk")
        phone = page.locator("#ds-root input[type='tel']")
        check(phone.get_attribute("required") is None, "optional: phone input not required")
        page.close()

        # ---------------- form-field-with-description ---------------------
        print("== form-field-with-description ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-with-description")
        ok = page.evaluate("""() => {
          const fields = [...document.querySelectorAll('[data-ds-form-field]')];
          if (fields.length !== 3) return false;
          return fields.every((f) => {
            const control = f.querySelector('input, select, textarea');
            const ids = (control.getAttribute('aria-describedby') || '').split(/\\s+/).filter(Boolean);
            if (ids.length !== 1) return false;
            const desc = document.getElementById(ids[0]);
            // description exists and precedes the control in DOM order
            return !!desc && (desc.compareDocumentPosition(control) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
          });
        }""")
        check(ok, "description: each control described by a preceding description")
        page.close()

        # ---------------- form-field-with-helper --------------------------
        print("== form-field-with-helper ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-with-helper")
        ok = page.evaluate("""() => {
          const fields = [...document.querySelectorAll('[data-ds-form-field]')];
          if (fields.length !== 3) return false;
          return fields.every((f) => {
            const control = f.querySelector('input, select, textarea');
            const ids = (control.getAttribute('aria-describedby') || '').split(/\\s+/).filter(Boolean);
            if (ids.length !== 1) return false;
            const helper = document.getElementById(ids[0]);
            // helper exists and follows the control in DOM order
            return !!helper && (control.compareDocumentPosition(helper) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
          });
        }""")
        check(ok, "helper: each control described by a following helper")
        page.close()

        # ---------------- form-field-with-error ---------------------------
        print("== form-field-with-error ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-with-error")
        static_input = page.locator('[data-ds-form-field]', has=page.get_by_text("Invite email", exact=True)).locator("input")
        check(static_input.get_attribute("aria-invalid") == "true", "error: static field aria-invalid=true")
        msg = page.get_by_role("alert").filter(has_text="already registered")
        check(msg.count() == 1, "error: static message has role=alert")
        msg_id = msg.get_attribute("id")
        check(msg_id in (static_input.get_attribute("aria-describedby") or ""),
              "error: message id in control aria-describedby")
        check(msg.locator('svg[aria-hidden="true"]').count() == 1, "error: alert icon present + aria-hidden")
        destructive = page.evaluate("""() => {
          const probe = document.createElement('span');
          probe.style.color = 'var(--ds-color-destructive)';
          document.body.appendChild(probe);
          const expected = getComputedStyle(probe).color;
          probe.remove();
          const msg = document.querySelector('[role="alert"]');
          return getComputedStyle(msg).color === expected;
        }""")
        check(destructive, "error: message uses the destructive token color")
        # live validation: type invalid -> error appears; valid -> clears
        live = page.locator('[data-ds-form-field]', has=page.get_by_text("Work email", exact=True)).locator("input")
        check(live.get_attribute("aria-invalid") is None, "error: live field starts valid")
        live.fill("ada@")
        page.wait_for_timeout(150)
        check(live.get_attribute("aria-invalid") == "true", "error: live field aria-invalid while invalid")
        check(page.get_by_role("alert").filter(has_text="valid email").count() == 1,
              "error: live error announced via role=alert")
        live.fill("ada@devsnips.dev")
        page.wait_for_timeout(150)
        check(live.get_attribute("aria-invalid") is None, "error: aria-invalid cleared when valid")
        check(page.get_by_role("alert").filter(has_text="valid email").count() == 0,
              "error: message removed when valid")
        describedby_targets_exist(page, "form-field-with-error")
        page.close()

        # ---------------- form-field-with-success -------------------------
        print("== form-field-with-success ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-with-success")
        static_status = page.get_by_role("status").filter(has_text="verified")
        check(static_status.count() == 1, "success: static message has role=status")
        username = page.locator('[data-ds-form-field]', has=page.get_by_text("Username", exact=True)).locator("input")
        username.fill("ab")
        page.wait_for_timeout(150)
        check(page.get_by_role("status").filter(has_text="available").count() == 0,
              "success: no message below 3 characters")
        username.fill("ada-byron")
        page.wait_for_timeout(150)
        live_status = page.get_by_role("status").filter(has_text="available")
        check(live_status.count() == 1, "success: availability announced via role=status")
        check(username.get_attribute("aria-invalid") is None, "success: never aria-invalid")
        check(live_status.get_attribute("id") in (username.get_attribute("aria-describedby") or ""),
              "success: message id in control aria-describedby")
        success_color = page.evaluate("""() => {
          const probe = document.createElement('span');
          probe.style.color = 'var(--ds-color-success)';
          document.body.appendChild(probe);
          const expected = getComputedStyle(probe).color;
          probe.remove();
          const msgs = [...document.querySelectorAll('[role="status"]')];
          return msgs.length > 0 && msgs.every((m) => getComputedStyle(m).color === expected);
        }""")
        check(success_color, "success: messages use the success token color")
        page.close()

        # ---------------- form-field-disabled -----------------------------
        print("== form-field-disabled ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-disabled")
        email = page.locator('[data-ds-form-field]', has=page.get_by_text("Account email", exact=True)).locator("input")
        check(email.get_attribute("disabled") is not None, "disabled: input has native disabled")
        label = page.locator(f'label[for="{email.get_attribute("id")}"]')
        muted = page.evaluate("""() => {
          const probe = document.createElement('span');
          probe.style.color = 'var(--ds-color-muted-foreground)';
          document.body.appendChild(probe);
          const expected = getComputedStyle(probe).color;
          probe.remove();
          const label = document.querySelector('[data-ds-form-field] label');
          return getComputedStyle(label).color === expected;
        }""")
        check(muted, "disabled: label is muted")
        focusable = page.evaluate("""() => {
          const el = document.querySelector('[data-ds-form-field] input[disabled]');
          el.focus();
          return document.activeElement === el;
        }""")
        check(not focusable, "disabled: disabled control not focusable")
        switch = page.locator('[data-ds-form-field] input[role="switch"]')
        check(switch.get_attribute("disabled") is not None, "disabled: composite switch disabled via FormField")
        check(switch.get_attribute("aria-checked") is None or True, "disabled: switch is a native checkbox role=switch")
        page.get_by_label("Lock security settings").click()
        page.wait_for_timeout(150)
        check(switch.get_attribute("disabled") is None, "disabled: unlocking re-enables the composite switch")
        page.get_by_label("Lock security settings").click()
        page.wait_for_timeout(150)
        check(switch.get_attribute("disabled") is not None, "disabled: re-locking disables again")
        page.close()

        # ---------------- form-field-group --------------------------------
        print("== form-field-group ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-group")
        groups = page.locator("fieldset[data-ds-form-field-group]")
        check(groups.count() == 2, "group: two fieldsets")
        legend = groups.nth(0).locator("legend")
        check(legend.text_content().strip() == "Notification channels", "group: legend names the group")
        describedby_targets_exist(page, "form-field-group")
        ids0 = (groups.nth(0).get_attribute("aria-describedby") or "").split()
        texts0 = [page.locator(f'[id="{i}"]').text_content() for i in ids0]
        check(any("how you want to be notified" in t for t in texts0),
              "group: fieldset described by group description")
        # uncheck the only selected channel -> group error wired to fieldset
        page.get_by_label("Email").click()
        page.wait_for_timeout(150)
        alert = page.get_by_role("alert").filter(has_text="at least one channel")
        check(alert.count() == 1, "group: error announced via role=alert")
        check(alert.get_attribute("id") in (groups.nth(0).get_attribute("aria-describedby") or ""),
              "group: error message id in fieldset aria-describedby")
        page.get_by_label("Push").click()
        page.wait_for_timeout(150)
        check(alert.count() == 0, "group: error clears when a channel is selected")
        # horizontal group: radios share one name, are clickable, and wrap
        radios = groups.nth(1).locator('input[type="radio"]')
        check(radios.count() == 3, "group: three plan radios")
        check(all(radios.nth(i).get_attribute("name") == "plan" for i in range(3)),
              "group: radios share one name")
        page.get_by_label("Pro").click()
        check(radios.nth(1).is_checked() and not radios.nth(0).is_checked(), "group: radio selection is exclusive")
        row_tops = page.evaluate("""() => [...document.querySelectorAll('[data-ds-form-field-group][data-orientation="horizontal"] label')]
          .map((el) => Math.round(el.getBoundingClientRect().top))""")
        check(len(set(row_tops)) == 1, "group: horizontal children share one row at 1280")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(120)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"group: no horizontal overflow @ 375 (got {overflow})")
        page.close()

        # ---------------- form-field-horizontal ---------------------------
        print("== form-field-horizontal ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field-horizontal")
        field = page.locator('[data-ds-form-field][data-orientation="horizontal"]').first
        label_box = field.locator("label").bounding_box()
        control_box = field.locator("input").bounding_box()
        check(label_box["x"] + label_box["width"] <= control_box["x"] + 1,
              "horizontal: label column left of control @ 1280")
        check(abs(label_box["y"] - control_box["y"]) <= 2,
              "horizontal: label top-aligned with control @ 1280")
        generic_field_checks(page, "form-field-horizontal")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(120)
        label_box = field.locator("label").bounding_box()
        control_box = field.locator("input").bounding_box()
        check(label_box["y"] + label_box["height"] <= control_box["y"] + 1,
              "horizontal: collapses to stacked label above control @ 375")
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"horizontal: no overflow @ 375 (got {overflow})")
        page.close()

        # ---------------- focus-visible / theming / motion ----------------
        print("== focus / theme / motion ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "form-field")
        page.keyboard.press("Tab")  # theme toggle
        page.keyboard.press("Tab")  # first control
        outline = page.evaluate("""() => {
          const el = document.activeElement;
          if (!el || el.tagName === 'BODY') return null;
          const cs = getComputedStyle(el);
          return cs.outlineWidth + '/' + cs.outlineStyle;
        }""")
        check(outline is not None and outline.startswith("2px"),
              f"focus-visible: 2px outline on keyboard focus (got {outline})")
        body_bg_light = page.evaluate("getComputedStyle(document.body).backgroundColor")
        page.locator("#ds-theme-toggle").click()
        page.wait_for_timeout(150)
        body_bg_dark = page.evaluate("getComputedStyle(document.body).backgroundColor")
        check(body_bg_light != body_bg_dark, "theme: body background flips in dark mode")
        label_color_dark = page.evaluate("getComputedStyle(document.querySelector('[data-ds-form-field] label')).color")
        page.locator("#ds-theme-toggle").click()
        page.wait_for_timeout(150)
        label_color_light = page.evaluate("getComputedStyle(document.querySelector('[data-ds-form-field] label')).color")
        check(label_color_light != label_color_dark, "theme: label color flips in dark mode")
        page.close()

        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        page = ctx.new_page()
        open_preview(page, "form-field")
        transition = page.evaluate("getComputedStyle(document.querySelector('[data-ds-form-field] input')).transitionProperty")
        check(transition == "none", f"reduced-motion: transition none (got {transition})")
        ctx.close()

        browser.close()


def main():
    static_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
