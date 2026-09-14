#!/usr/bin/env python3
"""Playwright QA for the React Switches previews.

Verifies the behavior-critical guarantees (not cosmetics):
  - switch: render + Space toggles + aria-checked + focus-visible + dark mode
  - switch-with-label: label click toggles the native input
  - switch-with-error: error renders + aria-invalid + role=alert
  - switch-disabled: native disabled attribute prevents toggling
  - switch-loading: aria-busy blocks interaction until the async save resolves
  - switch-group / switch-card-group: independent toggles; fieldset/legend
  - switch-card: card click toggles
  - switch-with-icon: leading icon rendered
  - switch-with-status: status text tracks the checked state
  - role=switch + aria-checked attributes present on every variant
  - reduced-motion: computed transition duration collapses to 0s
Also checks zero horizontal overflow at 375/768/1280 + 0 console errors.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/"

SWITCHES = [
    "switch", "switch-with-label", "switch-with-description",
    "switch-with-helper", "switch-with-error", "switch-disabled",
    "switch-loading", "switch-group", "switch-card", "switch-card-group",
    "switch-with-icon", "switch-with-status",
]

failures = []


def check(cond, label):
    if cond:
        print(f"  ok: {label}")
    else:
        print(f"  FAIL: {label}")
        failures.append(label)


def console_errors(page):
    errs = []

    def on_console(msg):
        if msg.type == "error":
            errs.append(msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    return errs


def open_preview(page, slug):
    errs = console_errors(page)
    page.goto(BASE + f"Switches/{slug}/preview.html", wait_until="networkidle")
    page.wait_for_selector("#ds-root input[role=switch]", timeout=15000)
    page.wait_for_timeout(400)  # let babel/React settle
    return errs


def overflow(page, w):
    page.set_viewport_size({"width": w, "height": 900})
    page.wait_for_timeout(150)
    return page.evaluate(
        "() => Math.max(document.documentElement.scrollWidth - window.innerWidth, 0)"
    )


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()

        # --- generic pass: zero console errors + semantics + overflow ------
        for slug in SWITCHES:
            errs = open_preview(page, slug)
            total = page.locator("#ds-root input[role=switch]").count()
            aria_checked = page.locator("#ds-root input[role=switch][aria-checked]").count()
            check(total > 0 and aria_checked == total, f"{slug}: {total} switches with role+aria-checked")
            for w in (375, 768, 1280):
                ov = overflow(page, w)
                check(ov == 0, f"{slug}: zero horizontal overflow at {w}px (got {ov})")
            console_text = [e for e in errs if "tailwindcss.com" not in e]
            check(len(console_text) == 0, f"{slug}: no console errors ({console_text[:2]})")

        # --- switch: click + Space + disabled ------------------------------
        errs = open_preview(page, "switch")
        first = page.locator("#ds-root input[role=switch]").first
        check(first.get_attribute("aria-checked") in ("true", "false"), "switch: aria-checked present")
        before = first.is_checked()
        first.click()
        check(first.is_checked() != before, "switch: click toggles")
        check(first.get_attribute("aria-checked") == ("true" if first.is_checked() else "false"), "switch: aria-checked tracks click")
        page.evaluate("() => document.body.classList.add('x')")
        first.focus()
        page.keyboard.press("Space")
        check(first.is_checked() == before, "switch: Space toggles back")
        disabled_sw = page.locator("#ds-root input[role=switch][disabled]").first
        d_before = disabled_sw.is_checked()
        disabled_sw.click(force=True)
        check(disabled_sw.is_checked() == d_before, "switch: disabled stays fixed")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch: no console errors")

        # --- focus-visible ring -------------------------------------------
        page.keyboard.press("Tab")
        el = page.evaluate("""() => {
          const el = document.activeElement;
          if (!el) return null;
          const cs = getComputedStyle(el);
          return {tag: el.tagName, role: el.getAttribute("role"), outlineWidth: cs.outlineWidth, outlineStyle: cs.outlineStyle};
        }""")
        check(el and el["tag"] == "INPUT" and el["role"] == "switch", "switch: Tab focuses a switch input")
        check(el and float(el["outlineWidth"].replace("px", "")) >= 2 and el["outlineStyle"] in ("solid", "auto"), f"switch: focus-visible outline visible ({el})")

        # --- dark mode tokens flip -----------------------------------------
        before_bg = page.evaluate("() => getComputedStyle(document.body).backgroundColor")
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(200)
        after_bg = page.evaluate("() => getComputedStyle(document.body).backgroundColor")
        check(before_bg != after_bg, f"switch: dark mode flips body bg ({before_bg} -> {after_bg})")
        page.click("#ds-theme-toggle")

        # --- switch-with-label: label click toggles ------------------------
        errs = open_preview(page, "switch-with-label")
        target = page.locator("#ds-root label", has_text="Security alerts")
        input_el = target.locator("input[role=switch]")
        before = input_el.is_checked()
        target.locator("span").last.click()
        check(input_el.is_checked() != before, "switch-with-label: label click toggles")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-with-label: no console errors")

        # --- switch-with-error: aria-invalid + role=alert ------------------
        errs = open_preview(page, "switch-with-error")
        invalid = page.locator("#ds-root input[role=switch][aria-invalid=true]")
        check(invalid.count() >= 1, "switch-with-error: aria-invalid=true rendered")
        check(page.locator("#ds-root [role=alert]").count() >= 1, "switch-with-error: role=alert rendered")
        first_err = invalid.first
        check(first_err.get_attribute("aria-describedby"), "switch-with-error: error linked via aria-describedby")
        # toggle the first errored switch on -> error resolves
        first_err.click()
        page.wait_for_timeout(150)
        check(invalid.count() == 1, "switch-with-error: toggling resolves its error (static error remains)")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-with-error: no console errors")

        # --- switch-disabled: native disabled ------------------------------
        errs = open_preview(page, "switch-disabled")
        sw = page.locator("#ds-root input[role=switch]").first
        check(sw.get_attribute("disabled") is not None, "switch-disabled: disabled attribute set")
        before = sw.is_checked()
        sw.click(force=True)
        check(sw.is_checked() == before, "switch-disabled: click does not toggle")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-disabled: no console errors")

        # --- switch-loading: aria-busy blocks until resolve ----------------
        errs = open_preview(page, "switch-loading")
        busy0 = page.locator("#ds-root input[role=switch][aria-busy=true]")
        check(busy0.count() == 1, "switch-loading: initially one aria-busy switch")
        check(busy0.first.get_attribute("disabled") is not None, "switch-loading: busy switch disabled")
        analytics = page.locator("#ds-root label", has_text="Cloud backup").locator("input[role=switch]").first
        before = analytics.is_checked()
        analytics.click()
        page.wait_for_selector("#ds-root input[role=switch][aria-busy=true]", timeout=3000)
        check(analytics.get_attribute("disabled") is not None, "switch-loading: disables during save")
        check(analytics.is_checked() == before, "switch-loading: state held until save resolves")
        page.wait_for_timeout(1100)
        check(analytics.is_checked() != before, "switch-loading: save resolves -> state applies")
        check(page.locator("#ds-root input[role=switch][aria-busy=true]").count() == 1, "switch-loading: busy clears after resolve (only static busy demo remains)")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-loading: no console errors")

        # --- switch-group: independent toggles -----------------------------
        errs = open_preview(page, "switch-group")
        check(page.locator("#ds-root fieldset").count() == 1, "switch-group: fieldset rendered")
        check(page.locator("#ds-root legend").count() == 1, "switch-group: legend rendered")
        email = page.locator("#ds-root input#ds-root-email, #ds-root input[value=email]").first
        # locate by value (ids are generated)
        email = page.locator("#ds-root input[role=switch][value=email]")
        desktop = page.locator("#ds-root input[role=switch][value=desktop]")
        e_before = email.is_checked()
        d_before = desktop.is_checked()
        email.click()
        check(email.is_checked() != e_before, "switch-group: email toggles")
        check(desktop.is_checked() == d_before, "switch-group: desktop unaffected (independent)")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-group: no console errors")

        # --- switch-card: card click toggles ------------------------------
        errs = open_preview(page, "switch-card")
        card = page.locator("#ds-root label", has_text="Public profile")
        input_el = card.locator("input[role=switch]")
        before = input_el.is_checked()
        card.locator("span").first.click()
        check(input_el.is_checked() != before, "switch-card: card click toggles")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-card: no console errors")

        # --- switch-card-group: independent + responsive -------------------
        errs = open_preview(page, "switch-card-group")
        check(page.locator("#ds-root fieldset").count() == 1, "switch-card-group: fieldset rendered")
        analytics = page.locator("#ds-root input[role=switch][value=analytics]")
        public = page.locator("#ds-root input[role=switch][value=public]")
        a_before = analytics.is_checked()
        p_before = public.is_checked()
        public.click()
        check(public.is_checked() != p_before, "switch-card-group: public toggles")
        check(analytics.is_checked() == a_before, "switch-card-group: analytics unaffected")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(150)
        cols = page.evaluate("() => getComputedStyle(document.querySelector('#ds-root fieldset > div')).gridTemplateColumns.split(' ').length")
        check(cols == 1, f"switch-card-group: single column at 375px (got {cols})")
        page.set_viewport_size({"width": 1280, "height": 900})
        page.wait_for_timeout(150)
        cols = page.evaluate("() => getComputedStyle(document.querySelector('#ds-root fieldset > div')).gridTemplateColumns.split(' ').length")
        check(cols == 2, f"switch-card-group: two columns at 1280px (got {cols})")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-card-group: no console errors")

        # --- switch-with-icon: icon rendered -------------------------------
        errs = open_preview(page, "switch-with-icon")
        first_label = page.locator("#ds-root label").first
        check(first_label.locator("svg").count() >= 1, "switch-with-icon: icon svg rendered")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-with-icon: no console errors")

        # --- switch-with-status: status text tracks state ------------------
        errs = open_preview(page, "switch-with-status")
        row = page.locator("#ds-root label", has_text="Analytics")
        input_el = row.locator("input[role=switch]")
        status = row.locator("span", has_text="Enabled").first
        check(status.count() == 1, "switch-with-status: initial Enabled")
        input_el.click()
        page.wait_for_timeout(150)
        check(row.locator("span", has_text="Disabled").first.count() == 1, "switch-with-status: flips to Disabled")
        desc = input_el.get_attribute("aria-describedby")
        check(bool(desc), "switch-with-status: aria-describedby links status")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch-with-status: no console errors")

        # --- reduced motion: transition collapses --------------------------
        ctx2 = browser.new_context(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        page2 = ctx2.new_page()
        errs = console_errors(page2)
        page2.goto(BASE + "Switches/switch/preview.html", wait_until="networkidle")
        page2.wait_for_selector("#ds-root input[role=switch]", timeout=15000)
        page2.wait_for_timeout(400)
        transition = page2.evaluate("""() => {
          const el = document.querySelector('#ds-root input[role=switch]');
          const cs = getComputedStyle(el);
          return {duration: cs.transitionDuration, property: cs.transitionProperty};
        }""")
        check(transition["property"] == "none" or transition["duration"] in ("0s", "0.0s"), f"switch: reduced-motion collapses transition ({transition})")
        console_text = [e for e in errs if "tailwindcss.com" not in e]
        check(len(console_text) == 0, "switch (reduced motion ctx): no console errors")

        browser.close()

    print()
    if failures:
        print(f"FAILED: {len(failures)} checks")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL SWITCH QA CHECKS PASSED")


if __name__ == "__main__":
    main()
