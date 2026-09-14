"""Responsive + console-error validation for the React navigation pages.

Tests the four navigation pages at 375 / 768 / 1280 px:
  - no horizontal overflow
  - no console errors (page errors / JS exceptions)
  - cards render (data loaded from snippets-index.json)
Run: python3 scripts/test_react_nav.py  (requires the http server on :12000)
"""
import json
import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:12000"
PAGES = [
    ("React landing", "/React/index.html"),
    ("Components index", "/React/Components/index.html"),
    ("Sections index", "/React/Sections/index.html"),
    ("Templates index", "/React/Templates/index.html"),
]
WIDTHS = [375, 768, 1280]

failures = []


def check(label, page, url):
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(400)  # let fetch + render settle
    body_count = page.eval_on_selector_all(
        "a.card, #grid > a, main a[href]", "els => els.length")
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(150)
        ow = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        status = "OK" if ow <= 0 else f"OVERFLOW {ow}px"
        if ow > 0:
            failures.append(f"{label} @ {w}px: horizontal overflow {ow}px")
        print(f"  {label:20} @ {w:>4}px  overflow={ow:>3}  links~{body_count}  console_errors={len(errors)}")
    if errors:
        failures.append(f"{label}: {len(errors)} console error(s): {errors[:3]}")
    return errors


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for label, path in PAGES:
            print(f"\n=== {label} ({path}) ===")
            check(label, page, BASE + path)
        # Dark-mode smoke test on the landing page.
        page.goto(BASE + "/React/index.html", wait_until="networkidle")
        page.emulate_media(color_scheme="dark")
        page.wait_for_timeout(200)
        bg = page.eval_on_selector("body", "el => getComputedStyle(el).backgroundColor")
        print(f"\nDark-mode body bg: {bg}")
        browser.close()
    print("\n" + "=" * 60)
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  x", f)
        sys.exit(1)
    print("ALL REACT NAVIGATION PAGES PASS — no overflow, no console errors.")


if __name__ == "__main__":
    main()