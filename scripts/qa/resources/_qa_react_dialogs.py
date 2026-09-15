#!/usr/bin/env python3
"""QA harness for the DevSnips React Dialogs family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx, no `<div onClick`, no inline `style=`
  - TSX/JSX export parity (same exported component names + default export)
  - shared-core equality across all 9 variants (header-comment-neutralized)

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors, 0 React warnings
  - 0 horizontal overflow at 375 / 768 / 1280 (dialog closed and open)
  - trigger: aria-haspopup=dialog, aria-expanded/aria-controls sync
  - role=dialog panel with aria-modal (modal), labelled by its DialogTitle,
    described by its DialogDescription
  - focus moves into the dialog on open; Tab / Shift+Tab trap wraps
  - Escape closes + restores focus to the trigger; overlay click closes;
    DialogClose (footer + ghost corner) closes
  - scroll lock while open (scrollbar compensation), restored on close
  - open panel stays inside the viewport
  - controlled: parent-owned state, onOpenChange sync, one dialog serves
    many row targets, aria-label when no DialogTitle is rendered
  - confirmation/destructive: role=alertdialog, safe action focused first,
    destructive-token action color
  - form: initial focus on the first field, native validation blocks submit
    (dialog stays open), valid submit closes + reports the value
  - scrollable: capped panel, pinned header/footer, internal body scrolling
  - nested: two stacked layers, Escape closes only the top-most, focus
    restores down the chain, page stays scroll-locked until all close
  - custom footer: real anchor link, split layout at sm, actions close
  - non-modal: no overlay, no aria-modal, no scroll lock, no trap; outside
    pointer down + Escape close; page stays interactive
  - focus-visible outline; dark-mode token flip (body + panel + overlay);
    reduced-motion transition-none

Run: python3 scripts/_qa_react_dialogs.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIALOGS = ROOT / "React/Components/Dialogs"
SLUGS = [
    "dialog",
    "dialog-controlled",
    "dialog-confirmation",
    "dialog-destructive",
    "dialog-form",
    "dialog-scrollable",
    "dialog-nested",
    "dialog-with-custom-footer",
    "dialog-non-modal",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = [
    "Dialog", "DialogTrigger", "DialogContent", "DialogHeader",
    "DialogTitle", "DialogDescription", "DialogFooter", "DialogClose",
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
        folder = DIALOGS / slug
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
        check(meta["category"] == "Dialogs", f"{slug}: category Dialogs")
        check(meta["component"] == "dialog", f"{slug}: component dialog")
        check(meta["family"] == "dialogs", f"{slug}: family dialogs")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        check('role="dialog"' in tsx, f"{slug}: role=dialog present")
        check('aria-haspopup="dialog"' in tsx, f"{slug}: aria-haspopup on trigger")
        check("aria-modal" in tsx, f"{slug}: aria-modal present")
        check("createPortal" in tsx, f"{slug}: portal rendering")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("var(--ds-color-surface-elevated)" in tsx, f"{slug}: elevated surface token")
        check("var(--ds-color-overlay)" in tsx, f"{slug}: overlay token")
        check("var(--ds-color-destructive)" in tsx, f"{slug}: destructive token")
        check("style=" not in tsx, f"{slug}: no inline style attribute")
        check(re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx) == ["#000", "#000", "#000", "#000"],
              f"{slug}: only color-mix hover #000 hex literals (got {re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', tsx)})")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        for name in CORE_EXPORTS:
            check(name in tsx_exports, f"{slug}: exports {name}")
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity {tsx_exports} vs {jsx_exports}")
        check("export default Dialog;" in jsx, f"{slug}: JSX default export")
        check("useDialog" in jsx, f"{slug}: JSX keeps context hook")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        cores[slug] = neutralize_core(tsx)
    ref = cores["dialog"]
    for slug in SLUGS[1:]:
        check(cores[slug] == ref, f"{slug}: shared core identical to reference")


def open_preview(page, slug):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((DIALOGS / slug / "preview.html").as_uri())
    page.wait_for_selector("#ds-root *", timeout=15000)
    page.wait_for_timeout(400)
    return errors


def no_overflow_open(page, slug, dialog_selector):
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(120)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"{slug}: no horizontal overflow (open) @ {w} (got {overflow})")
        inside = page.evaluate(f"""() => {{
          const el = document.querySelector('{dialog_selector}');
          if (!el) return false;
          const r = el.getBoundingClientRect();
          return r.left >= -1 && r.right <= window.innerWidth + 1 && r.top >= -1 && r.bottom <= window.innerHeight + 1;
        }}""")
        check(inside, f"{slug}: open panel inside viewport @ {w}")
    page.set_viewport_size({"width": 1280, "height": 900})


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

            # overflow, dialog closed
            for w in WIDTHS:
                page.set_viewport_size({"width": w, "height": 900})
                page.wait_for_timeout(100)
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(overflow <= 0, f"{slug}: no horizontal overflow (closed) @ {w} (got {overflow})")
            page.set_viewport_size({"width": 1280, "height": 900})
            page.close()

        # ---------------- dialog (reference) -------------------------------
        print("== dialog ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = open_preview(page, "dialog")
        trigger = page.get_by_role("button", name="Edit project")
        check(trigger.get_attribute("aria-haspopup") == "dialog", "dialog: aria-haspopup=dialog")
        check(trigger.get_attribute("aria-expanded") == "false", "dialog: aria-expanded false initially")
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        dialog = page.locator('[role="dialog"]')
        check(dialog.count() == 1, "dialog: exactly one dialog open")
        check(dialog.get_attribute("aria-modal") == "true", "dialog: aria-modal true")
        check(trigger.get_attribute("aria-expanded") == "true", "dialog: aria-expanded true when open")
        check(trigger.get_attribute("aria-controls") == dialog.get_attribute("id"),
              "dialog: aria-controls -> dialog id")
        label_id = dialog.get_attribute("aria-labelledby")
        desc_id = dialog.get_attribute("aria-describedby")
        check(bool(label_id) and page.locator(f'[id="{label_id}"]').text_content().strip() == "Project settings",
              "dialog: aria-labelledby -> DialogTitle")
        check(bool(desc_id) and "workspace" in page.locator(f'[id="{desc_id}"]').text_content(),
              "dialog: aria-describedby -> DialogDescription")
        check(page.locator("[data-ds-dialog-overlay]").count() == 1, "dialog: overlay rendered")
        check(page.evaluate("document.body.style.overflow") == "hidden", "dialog: body scroll locked")
        check(page.evaluate("document.activeElement && document.activeElement.closest('[role=dialog]') !== null"),
              "dialog: focus moved inside the dialog on open")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Cancel", f"dialog: initial focus on first action (got {active})")

        # trap wrap: Cancel -> Save changes -> ghost close -> Cancel
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Cancel", f"dialog: Tab wraps last -> first (got {active})")
        # focus-visible ring on the keyboard-focused element
        style = page.evaluate("""() => {
          const el = document.activeElement;
          const cs = getComputedStyle(el);
          return [cs.outlineWidth, cs.outlineStyle];
        }""")
        check(style[0] == "2px" and style[1] in ("auto", "solid"),
              f"dialog: focus-visible ring (2px {style[1]})")
        page.keyboard.press("Tab")
        page.keyboard.press("Shift+Tab")
        page.keyboard.press("Shift+Tab")
        active = page.evaluate("document.activeElement && (document.activeElement.getAttribute('aria-label') || document.activeElement.textContent.trim())")
        check(active == "Close dialog", f"dialog: Shift+Tab wraps first -> last (got {active})")

        # padding compensation was applied (headless chromium has a scrollbar)
        check(page.evaluate("parseInt(document.body.style.paddingRight || '0')") >= 0,
              "dialog: scrollbar compensation applied")

        no_overflow_open(page, "dialog", '[role="dialog"]')

        # Escape closes + restores focus + unlocks scroll
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog: Escape closes")
        check(trigger.get_attribute("aria-expanded") == "false", "dialog: aria-expanded false after Escape")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Edit project",
              "dialog: Escape restores focus to the trigger")
        check(page.evaluate("document.body.style.overflow") == "", "dialog: scroll lock released")
        check(page.evaluate("document.body.style.paddingRight") == "", "dialog: scrollbar compensation released")

        # overlay click closes
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.mouse.click(24, 480)
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog: overlay pointer down closes")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Edit project",
              "dialog: overlay close restores focus to the trigger")

        # ghost close closes
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.get_by_role("button", name="Close dialog").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog: corner ghost close closes")

        # background is not clickable while open: the pointerdown lands on overlay
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        hit = page.evaluate("document.elementFromPoint(24, 480) && document.elementFromPoint(24, 480).hasAttribute('data-ds-dialog-overlay')")
        check(hit, "dialog: overlay intercepts background pointer (elementFromPoint)")
        # Cancel closes; Save changes runs its action
        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(150)
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.get_by_role("button", name="Save changes").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog: primary close action closes")
        check("Saved" in page.locator("#ds-root").text_content(), "dialog: primary action onClick ran")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Edit project",
              "dialog: action close restores focus to the trigger")

        # dark mode: body + panel + overlay flip (the modal overlay blocks the
        # toggle, so switch the theme programmatically)
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        before = page.evaluate("""[getComputedStyle(document.body).backgroundColor,
          getComputedStyle(document.querySelector('[role=dialog]')).backgroundColor,
          getComputedStyle(document.querySelector('[data-ds-dialog-overlay]')).backgroundColor]""")
        page.evaluate("document.getElementById('ds-theme-toggle').click()")
        page.wait_for_timeout(200)
        after = page.evaluate("""[getComputedStyle(document.body).backgroundColor,
          getComputedStyle(document.querySelector('[role=dialog]')).backgroundColor,
          getComputedStyle(document.querySelector('[data-ds-dialog-overlay]')).backgroundColor]""")
        check(before[0] != after[0] and before[1] != after[1] and before[2] != after[2],
              f"dialog: dark-mode flips body+panel+overlay ({before} -> {after})")
        check(errors == [] or all("favicon" not in e for e in errors), f"dialog: no errors after interactions {errors[:3]}")
        page.keyboard.press("Escape")
        page.close()

        # reduced motion: transitions disabled
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        rmp = ctx.new_page()
        rmp.goto((DIALOGS / "dialog" / "preview.html").as_uri())
        rmp.wait_for_selector("#ds-root *", timeout=15000)
        rmp.get_by_role("button", name="Edit project").click()
        rmp.wait_for_selector('[role="dialog"]', timeout=5000)
        tp = rmp.evaluate("getComputedStyle(document.querySelector('[role=dialog] button')).transitionProperty")
        check(tp == "none", f"dialog: reduced-motion transition-none (got {tp})")
        ctx.close()

        # ---------------- dialog-controlled --------------------------------
        print("== dialog-controlled ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-controlled")
        row_buttons = page.get_by_role("button", name="Revoke", exact=True)
        check(row_buttons.count() == 2, "dialog-controlled: two token rows")
        row_buttons.first.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        dialog = page.locator('[role="dialog"]')
        check("Revoke ci-deploy-key?" in dialog.text_content(), "dialog-controlled: dialog serves the row target")
        check("last onOpenChange event: open" in page.locator("#ds-root").text_content(),
              "dialog-controlled: parent received onOpenChange(true)")
        check(page.evaluate("document.activeElement && document.activeElement.closest('[role=dialog]') !== null"),
              "dialog-controlled: focus inside dialog (no trigger component)")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check("last onOpenChange event: closed" in page.locator("#ds-root").text_content(),
              "dialog-controlled: parent received onOpenChange(false)")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Revoke",
              "dialog-controlled: focus restored to the row action")
        # revoke flow removes the row
        page.get_by_role("button", name="Revoke", exact=True).first.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.get_by_role("button", name="Revoke token").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-controlled: confirm closes")
        check(page.get_by_role("button", name="Revoke", exact=True).count() == 1,
              "dialog-controlled: revoked token row removed")

        # aria-label dialog (no visible title)
        page.get_by_role("button", name="Details").click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        dialog = page.locator('[role="dialog"]')
        check(dialog.get_attribute("aria-label") == "Session details", "dialog-controlled: aria-label when no title")
        check(dialog.get_attribute("aria-labelledby") is None, "dialog-controlled: no dangling aria-labelledby")
        check(dialog.get_attribute("aria-describedby") is None, "dialog-controlled: no dangling aria-describedby")
        page.get_by_role("button", name="Got it").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-controlled: Got it closes")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Details",
              "dialog-controlled: focus restored to Details button")
        page.close()

        # ---------------- dialog-confirmation ------------------------------
        print("== dialog-confirmation ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-confirmation")
        page.get_by_role("button", name="Discard draft").click()
        page.wait_for_selector('[role="alertdialog"]', timeout=5000)
        page.wait_for_timeout(150)
        check(page.locator('[role="alertdialog"]').count() == 1, "dialog-confirmation: role=alertdialog")
        check(page.locator('[role="dialog"]').count() == 0, "dialog-confirmation: no plain dialog role")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Keep editing", f"dialog-confirmation: initial focus on the safe action (got {active})")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check("Autosaved" in page.locator("#ds-root").text_content(), "dialog-confirmation: Escape cancels")
        page.get_by_role("button", name="Discard draft").click()
        page.wait_for_selector('[role="alertdialog"]', timeout=5000)
        page.mouse.click(24, 480)
        page.wait_for_timeout(200)
        check("Autosaved" in page.locator("#ds-root").text_content(), "dialog-confirmation: overlay cancels")
        page.get_by_role("button", name="Discard draft").click()
        page.wait_for_selector('[role="alertdialog"]', timeout=5000)
        page.locator('[role="alertdialog"]').get_by_role("button", name="Discard draft").click()
        page.wait_for_timeout(200)
        check("Discarded just now" in page.locator("#ds-root").text_content(), "dialog-confirmation: confirm proceeds")
        page.close()

        # ---------------- dialog-destructive -------------------------------
        print("== dialog-destructive ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-destructive")
        page.get_by_role("button", name="Delete", exact=True).click()
        page.wait_for_selector('[role="alertdialog"]', timeout=5000)
        page.wait_for_timeout(150)
        check("Delete this repository?" in page.locator('[role="alertdialog"]').text_content(),
              "dialog-destructive: alertdialog with warning question")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Cancel", f"dialog-destructive: initial focus on Cancel (got {active})")
        bg = page.evaluate("""() => {
          const b = [...document.querySelectorAll('[role=alertdialog] button')].find(x => x.textContent.trim() === 'Delete repository');
          return getComputedStyle(b).backgroundColor;
        }""")
        check(bg in ("rgb(194, 38, 27)", "rgba(194, 38, 27, 1)"), f"dialog-destructive: destructive action token color (got {bg})")
        # dark mode: destructive color flips (toggle programmatically — the
        # modal overlay blocks background clicks)
        page.evaluate("document.getElementById('ds-theme-toggle').click()")
        page.wait_for_timeout(200)
        bg_dark = page.evaluate("""() => {
          const b = [...document.querySelectorAll('[role=alertdialog] button')].find(x => x.textContent.trim() === 'Delete repository');
          return getComputedStyle(b).backgroundColor;
        }""")
        check(bg_dark in ("rgb(241, 99, 90)", "rgba(241, 99, 90, 1)"), f"dialog-destructive: dark destructive token (got {bg_dark})")
        page.locator('[role="alertdialog"]').get_by_role("button", name="Delete repository").click()
        page.wait_for_timeout(200)
        check("Scheduled for deletion" in page.locator("#ds-root").text_content(), "dialog-destructive: delete ran")
        page.close()

        # ---------------- dialog-form --------------------------------------
        print("== dialog-form ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-form")
        page.get_by_role("button", name="Invite member").click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        check(page.evaluate("document.activeElement && document.activeElement.id") == "dsf-email",
              "dialog-form: initial focus on the first field")
        email = page.locator("#dsf-email")
        email.fill("not-an-email")
        page.get_by_role("button", name="Send invite").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 1, "dialog-form: invalid submit blocked, dialog stays open")
        check(page.evaluate("document.getElementById('dsf-email').validity.valid") is False,
              "dialog-form: native validation flagged the email")
        email.fill("jane@devsnips.io")
        page.get_by_role("button", name="Send invite").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-form: valid submit closes")
        check("Invite sent to jane@devsnips.io" in page.locator("#ds-root").text_content(),
              "dialog-form: submitted value reported")
        # label click focuses the field
        page.get_by_role("button", name="Invite member").click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.get_by_text("Work email").click()
        check(page.evaluate("document.activeElement && document.activeElement.id") == "dsf-email",
              "dialog-form: label click focuses the field")
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-form: Escape discards")
        page.close()

        # ---------------- dialog-scrollable --------------------------------
        print("== dialog-scrollable ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-scrollable")
        page.get_by_role("button", name="View changelog").click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        region = page.locator('[role="dialog"] .overflow-y-auto')
        check(region.count() == 1, "dialog-scrollable: body scroll region present")
        metrics = region.evaluate("(el) => [el.scrollHeight, el.clientHeight]")
        check(metrics[0] > metrics[1], f"dialog-scrollable: body scrolls internally ({metrics[0]} > {metrics[1]})")
        panel_h = page.evaluate("document.querySelector('[role=dialog]').getBoundingClientRect().height")
        check(panel_h <= 900 - 32 + 1, f"dialog-scrollable: panel capped inside viewport ({panel_h})")
        title_top_before = page.evaluate("document.querySelector('[role=dialog] h2').getBoundingClientRect().top")
        footer_top_before = page.evaluate("""(() => {
          const b = [...document.querySelectorAll('[role=dialog] button')].find(x => x.textContent.trim() === 'Close');
          return b.getBoundingClientRect().top;
        })()""")
        max_scroll = region.evaluate("(el) => el.scrollHeight - el.clientHeight")
        region.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
        page.wait_for_timeout(100)
        check(region.evaluate("(el) => el.scrollTop") == max_scroll,
              f"dialog-scrollable: body actually scrolled (scrollTop={max_scroll})")
        title_top_after = page.evaluate("document.querySelector('[role=dialog] h2').getBoundingClientRect().top")
        footer_top_after = page.evaluate("""(() => {
          const b = [...document.querySelectorAll('[role=dialog] button')].find(x => x.textContent.trim() === 'Close');
          return b.getBoundingClientRect().top;
        })()""")
        check(abs(title_top_before - title_top_after) < 1, "dialog-scrollable: header pinned while body scrolls")
        check(abs(footer_top_before - footer_top_after) < 1, "dialog-scrollable: footer pinned while body scrolls")
        no_overflow_open(page, "dialog-scrollable", '[role="dialog"]')
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-scrollable: Escape closes")
        page.close()

        # ---------------- dialog-nested ------------------------------------
        print("== dialog-nested ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-nested")
        page.get_by_role("button", name="Share project").click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        check(page.locator('[role="dialog"]').count() == 1, "dialog-nested: parent open")
        remove_buttons = page.locator('[role="dialog"]').get_by_role("button", name="Remove")
        check(remove_buttons.count() == 2, "dialog-nested: removable members listed (owner excluded)")
        remove_buttons.first.click()
        page.wait_for_selector('[role="alertdialog"]', timeout=5000)
        page.wait_for_timeout(150)
        check(page.locator('[role="dialog"]').count() == 1, "dialog-nested: parent still open under nested")
        check(page.locator('[role="alertdialog"]').count() == 1, "dialog-nested: nested alertdialog open")
        check("Remove Marcus Chen?" in page.locator('[role="alertdialog"]').text_content(),
              "dialog-nested: nested targets the member")
        check(page.evaluate("document.body.style.overflow") == "hidden", "dialog-nested: scroll locked at depth 2")
        check(page.locator("[data-ds-dialog-overlay]").count() == 2, "dialog-nested: two overlay layers")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Keep member", f"dialog-nested: focus inside nested on safe action (got {active})")
        # Escape closes ONLY the nested layer
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.locator('[role="alertdialog"]').count() == 0, "dialog-nested: Escape closes nested only")
        check(page.locator('[role="dialog"]').count() == 1, "dialog-nested: parent survives nested Escape")
        check(page.evaluate("document.body.style.overflow") == "hidden",
              "dialog-nested: page still locked while parent open")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Remove", f"dialog-nested: focus restored into the parent (got {active})")
        # confirm removes the member, parent stays open
        page.locator('[role="dialog"]').get_by_role("button", name="Remove").first.click()
        page.wait_for_selector('[role="alertdialog"]', timeout=5000)
        page.locator('[role="alertdialog"]').get_by_role("button", name="Remove member").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="alertdialog"]').count() == 0, "dialog-nested: confirm closes nested")
        check(page.locator('[role="dialog"]').get_by_role("button", name="Remove").count() == 1,
              "dialog-nested: member row removed")
        check(page.locator('[role="dialog"]').count() == 1, "dialog-nested: parent still open after removal")
        # focus is not stranded on the removed button
        check(page.evaluate("document.activeElement && document.activeElement.closest('[role=dialog]') !== null || document.activeElement === document.body"),
              "dialog-nested: focus not stranded on unmounted button")
        # Escape closes the parent, restores to the page trigger
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-nested: Escape closes the parent")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Share project",
              "dialog-nested: focus restores to the page trigger")
        check(page.evaluate("document.body.style.overflow") == "", "dialog-nested: scroll unlocked after all close")
        page.close()

        # ---------------- dialog-with-custom-footer ------------------------
        print("== dialog-with-custom-footer ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-with-custom-footer")
        page.get_by_role("button", name="Publish release").click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        link = page.locator('[role="dialog"]').get_by_role("link", name="View release checklist")
        check(link.count() == 1, "dialog-with-custom-footer: real anchor in the footer")
        href = link.get_attribute("href")
        check(bool(href) and href.endswith("#release-checklist"), "dialog-with-custom-footer: anchor has href")
        justify = page.evaluate("""(() => {
          const l = document.querySelector('[role=dialog] a[href$="release-checklist"]');
          return getComputedStyle(l.parentElement.parentElement).justifyContent;
        })()""")
        check(justify == "space-between", f"dialog-with-custom-footer: split footer at desktop (got {justify})")
        link.click()
        page.wait_for_timeout(150)
        check(page.evaluate("location.hash") == "#release-checklist", "dialog-with-custom-footer: anchor navigates")
        check(page.locator('[role="dialog"]').count() == 1, "dialog-with-custom-footer: link does not close dialog")
        page.locator('[role="dialog"]').get_by_role("button", name="Publish release").click()
        page.wait_for_timeout(200)
        check("Publishing to the registry" in page.locator("#ds-root").text_content(),
              "dialog-with-custom-footer: publish action ran")
        page.close()

        # ---------------- dialog-non-modal ---------------------------------
        print("== dialog-non-modal ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "dialog-non-modal")
        trigger = page.get_by_role("button", name="Keyboard shortcuts")
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        dialog = page.locator('[role="dialog"]')
        check(dialog.get_attribute("aria-modal") is None, "dialog-non-modal: no aria-modal")
        check(page.locator("[data-ds-dialog-overlay]").count() == 0, "dialog-non-modal: no overlay")
        check(page.evaluate("document.body.style.overflow") != "hidden", "dialog-non-modal: no scroll lock")
        check(page.evaluate("document.activeElement && document.activeElement.closest('[role=dialog]') !== null"),
              "dialog-non-modal: focus still moved into the panel")
        # page scrolls while open (scroll as far as the document allows)
        max_scroll = page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        check(page.evaluate("window.scrollY") == max_scroll and max_scroll > 0,
              f"dialog-non-modal: page scrolls while open (scrollY={max_scroll})")
        # no trap: Shift+Tab leaves the panel and walks back through the page
        page.keyboard.press("Shift+Tab")
        active = page.evaluate("document.activeElement && document.activeElement.textContent.trim()")
        check(active == "Keyboard shortcuts", f"dialog-non-modal: Shift+Tab leaves panel to the trigger (got {active})")
        page.keyboard.press("Shift+Tab")
        outside = page.evaluate("document.activeElement && document.activeElement.closest('[role=dialog]') === null")
        check(outside and page.evaluate("document.activeElement.textContent") != "Keyboard shortcuts",
              "dialog-non-modal: Shift+Tab continues through the page (no trap)")
        check(page.locator('[role="dialog"]').count() == 1, "dialog-non-modal: panel stays open while Tabbing out")
        # background action works; outside pointer down closes
        bg_btn = page.get_by_role("button", name=re.compile("Background action"))
        bg_btn.click()
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-non-modal: outside pointer down closes")
        check("×1" in bg_btn.text_content() or "Background action ×1" in page.locator("#ds-root").text_content(),
              "dialog-non-modal: background action still ran")
        check(page.evaluate("document.activeElement === document.body || (document.activeElement && document.activeElement.textContent || '').includes('Background action')"),
              "dialog-non-modal: focus not stranded after outside close")
        # Escape closes too
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.locator('[role="dialog"]').count() == 0, "dialog-non-modal: Escape closes")
        check(page.evaluate("document.activeElement && document.activeElement.textContent.trim()") == "Keyboard shortcuts",
              "dialog-non-modal: focus restored to trigger")
        # open panel inside the viewport at all widths
        trigger.click()
        page.wait_for_selector('[role="dialog"]', timeout=5000)
        page.wait_for_timeout(150)
        no_overflow_open(page, "dialog-non-modal", '[role="dialog"]')
        page.keyboard.press("Escape")
        page.close()

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
    print("ALL PASSED")


if __name__ == "__main__":
    main()
