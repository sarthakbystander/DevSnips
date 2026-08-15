#!/usr/bin/env python3
"""Quick QA for a Vanilla template: overflow + console errors + interactions."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

WIDTHS = [320, 375, 768, 1024, 1280, 1920]


def qa(file_url, checks=None):
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        msgs = []
        page.on("console", lambda m: msgs.append(f"{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: msgs.append(f"pageerror: {e}"))
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(400)

        # Overflow check
        for w in WIDTHS:
            page.set_viewport_size({"width": w, "height": 900})
            page.wait_for_timeout(150)
            ow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ow > 1:
                errors.append(f"overflow at {w}px: +{ow}px")

        # Interaction checks
        if checks:
            for name, fn in checks.items():
                try:
                    page.set_viewport_size({"width": 1280, "height": 900})
                    fn(page)
                    print(f"  check ok: {name}")
                except Exception as e:
                    errors.append(f"check '{name}' failed: {e}")

        if msgs:
            errors.append("console errors: " + " | ".join(msgs))
        browser.close()
    return errors


def dp_checks(page):
    # Theme toggle flips data-theme
    t = page.query_selector("[data-theme-toggle]")
    assert t, "no theme toggle"
    before = page.evaluate("document.documentElement.getAttribute('data-theme')")
    t.click()
    after = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert before != after, f"theme did not toggle: {before}->{after}"
    # Reveal elements become visible
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(700)
    visible = page.evaluate(
        "document.querySelectorAll('.reveal.is-visible').length"
    )
    assert visible >= 3, f"only {visible} reveal elements visible"


def ec_checks(page):
    # Schedule tabs: click Day 2 -> panel switches, aria-selected flips
    tabs = page.query_selector_all('.tab-link')
    assert len(tabs) == 2, f"expected 2 tabs, got {len(tabs)}"
    assert tabs[0].get_attribute('aria-selected') == 'true', "day1 not selected initially"
    tabs[1].click()
    page.wait_for_timeout(200)
    s2 = [t.get_attribute('aria-selected') for t in tabs]
    assert s2 == ['false', 'true'], f"tab switch failed: {s2}"
    p2visible = page.evaluate("document.getElementById('panel-day2').getAttribute('data-active')")
    assert p2visible == 'true', "day2 panel not active"
    p1hidden = page.evaluate("document.getElementById('panel-day1').hasAttribute('hidden')")
    assert p1hidden, "day1 panel not hidden after switch"
    # Countdown values are non-zero digits
    dv = page.evaluate("document.getElementById('cd-days').textContent")
    assert dv and dv.strip().isdigit(), f"countdown days not numeric: {dv!r}"
    # Theme toggle
    t = page.query_selector('[data-theme-toggle]')
    before = page.evaluate("document.documentElement.getAttribute('data-theme')")
    t.click()
    after = page.evaluate("document.documentElement.getAttribute('data-theme')")
    assert before != after, "theme did not toggle"


def pl_checks(page):
    # FAQ accordion single-open
    triggers = page.query_selector_all(".faq-trigger")
    assert len(triggers) >= 2, "no FAQ triggers"
    triggers[0].click()
    page.wait_for_timeout(250)
    state = page.evaluate("""() => {
      const ts = Array.from(document.querySelectorAll('.faq-trigger'));
      return ts.map(t => t.getAttribute('aria-expanded') === 'true' ? 1 : 0);
    }""")
    assert state[0] == 1, "first panel did not open"
    # Open second -> first should close (single-open)
    triggers[1].click()
    page.wait_for_timeout(250)
    state2 = page.evaluate("""() => {
      return Array.from(document.querySelectorAll('.faq-trigger'))
        .map(t => t.getAttribute('aria-expanded') === 'true' ? 1 : 0);
    }""")
    assert state2 == [0, 1] + [0] * (len(triggers) - 2), f"single-open failed: {state2}"
    # Waitlist form validation + success
    page.set_viewport_size({"width": 1280, "height": 1600})
    page.evaluate("document.getElementById('waitlist').scrollIntoView()")
    page.wait_for_timeout(200)
    form = page.query_selector("#waitlist-form")
    assert form, "no waitlist form"
    # Submit empty -> errors
    page.query_selector("#wl-submit").click()
    page.wait_for_timeout(150)
    bad = page.evaluate("document.querySelectorAll('#waitlist-form [aria-invalid=\"true\"]').length")
    assert bad == 2, f"expected 2 invalid fields, got {bad}"
    # Fill + submit -> success
    page.fill("#wl-name", "Test User")
    page.fill("#wl-email", "test@team.dev")
    page.query_selector("#wl-submit").click()
    page.wait_for_timeout(200)
    visible = page.evaluate("document.getElementById('wl-success').getAttribute('data-visible')")
    assert visible == "true", "success state not shown"


if __name__ == "__main__":
    target = sys.argv[1]
    checks = None
    if "developer-portfolio" in target:
        checks = {"theme-toggle + reveal": dp_checks}
    elif "product-launch" in target:
        checks = {"faq + waitlist": pl_checks}
    elif "event-conference" in target:
        checks = {"tabs + countdown + theme": ec_checks}
    errs = qa("file://" + str(Path(target).resolve()), checks)
    if errs:
        print("FAIL:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print("QA PASS:", target)
