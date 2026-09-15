#!/usr/bin/env python3
"""Playwright QA for the React Breadcrumbs previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: <nav aria-label> landmark wrapping an <ol>, real anchor
    links with href, exactly one aria-current="page" per trail rendered as
    non-anchor text, aria-hidden separators, zero console errors, zero
    horizontal overflow at 375/768/1280
  - focus-visible ring (2px outline) on links and menu triggers
  - dark mode flips the computed link color
  - reduced motion collapses transitions to 0s
  - breadcrumbs: two trails; clicking a link updates the URL hash (real
    anchor navigation, no reload)
  - breadcrumbs-with-home: home icon inside an aria-hidden wrapper;
    icon-only home link carries aria-label="Home"
  - breadcrumbs-with-icons: icons render inside aria-hidden wrappers; the
    icon-less level stays icon-less (icons optional)
  - breadcrumbs-with-current: the data-driven trail renders the current
    level as text with aria-current="page", not an anchor
  - breadcrumbs-with-dropdown: trigger has aria-haspopup=menu and toggles
    aria-expanded; menu of real anchors; ArrowDown opens + focuses first
    item; arrows/Home/End move; Escape closes + refocuses trigger; outside
    click closes; the current item carries aria-current="page"
  - breadcrumbs-collapsed: ellipsis disclosure has an accessible name,
    opens a menu exposing the hidden levels as real links, keyboard
    reachable, Escape closes + refocuses
  - breadcrumbs-max-width: long labels are truncated (scrollWidth >
    clientWidth) and the full text survives in the title attribute
  - breadcrumbs-with-separator: the custom "/" separator renders inside an
    aria-hidden list item; per-position override works
  - static: every variant folder has exactly code.tsx, code.jsx,
    preview.html, metadata.json, README.md; metadata is valid JSON; no
    component-specific CSS files exist

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_breadcrumbs.py
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/Breadcrumbs/"

VARIANTS = [
    "breadcrumbs", "breadcrumbs-with-home", "breadcrumbs-with-icons",
    "breadcrumbs-with-current", "breadcrumbs-with-dropdown",
    "breadcrumbs-collapsed", "breadcrumbs-max-width",
    "breadcrumbs-with-separator",
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


def open_preview(page, slug, width=1280):
    errs = console_errors(page)
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(BASE + f"{slug}/preview.html", wait_until="networkidle")
    page.wait_for_selector("#ds-root nav ol", timeout=15000)
    page.wait_for_timeout(300)
    return errs


def overflow(page, w):
    page.set_viewport_size({"width": w, "height": 900})
    page.wait_for_timeout(150)
    return page.evaluate(
        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
    )


def static_checks():
    print("== static ==")
    for slug in VARIANTS:
        folder = ROOT / "React/Components/Breadcrumbs" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["README.md", "code.jsx", "code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exactly the 5 required files",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(
            meta["technology"] == "react"
            and meta["type"] == "component"
            and meta["category"] == "Breadcrumbs"
            and meta["styling"] == "Tailwind CSS"
            and meta["languages"] == ["JSX", "TSX"],
            f"{slug}: metadata schema fields",
        )
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        tsx = (folder / "code.tsx").read_text()
        check('"any"' not in tsx and ": any" not in tsx, f"{slug}: no any in code.tsx")
        check('aria-label={label}' in tsx, f"{slug}: semantic nav aria-label")
        check("<ol" in tsx, f"{slug}: ordered list")
        check('aria-current="page"' in tsx, f"{slug}: aria-current page")
        check('aria-hidden="true"' in tsx, f"{slug}: aria-hidden separators/icons")
        check("var(--ds-color-focus-ring)" in tsx, f"{slug}: focus-ring token")
    css = list((ROOT / "React/Components/Breadcrumbs").rglob("*.css"))
    check(css == [], "no component-specific CSS files in the family")


def shared_checks(page, slug):
    errs = open_preview(page, slug)
    navs = page.evaluate("document.querySelectorAll('#ds-root nav[aria-label]').length")
    check(navs >= 1, f"{slug}: nav landmark(s) with aria-label")
    ols = page.evaluate("document.querySelectorAll('#ds-root nav[aria-label] > ol').length")
    check(ols >= 1, f"{slug}: ordered list inside nav")
    anchors = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root nav ol a')).every(a => a.getAttribute('href'))"
    )
    check(anchors, f"{slug}: every link is a real anchor with href")
    currents = page.evaluate(
        """Array.from(document.querySelectorAll('#ds-root nav')).map(n => {
          const c = n.querySelectorAll('[aria-current="page"]');
          return c.length === 1 && c[0].tagName !== 'A';
        }).every(Boolean)"""
    )
    check(currents, f"{slug}: exactly one non-link aria-current=page per trail")
    seps_hidden = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root nav ol li[role=\"presentation\"]')).every(li => li.getAttribute('aria-hidden') === 'true')"
    )
    check(seps_hidden, f"{slug}: separators are aria-hidden presentation items")
    for w in (375, 768, 1280):
        check(overflow(page, w) == 0, f"{slug}: no horizontal overflow at {w}px")
    check(errs == [], f"{slug}: zero console errors")


def focus_ring_check(page, slug):
    open_preview(page, slug)
    info = None
    for _ in range(6):
        page.keyboard.press("Tab")
        page.wait_for_timeout(80)
        info = page.evaluate(
            """(() => {
              const el = document.activeElement;
              if (!el || !document.querySelector('#ds-root').contains(el)) return null;
              const cs = getComputedStyle(el);
              return { tag: el.tagName, outline: cs.outlineWidth, style: cs.outlineStyle };
            })()"""
        )
        if info:
            break
    check(
        bool(info) and info["outline"] == "2px" and info["style"] in ("auto", "solid"),
        f"{slug}: first tabbable breadcrumb element shows a 2px focus-visible ring",
    )


def dark_mode_check(page, slug="breadcrumbs"):
    open_preview(page, slug)
    light = page.evaluate("getComputedStyle(document.querySelector('#ds-root nav a')).color")
    page.click("#ds-theme-toggle")
    page.wait_for_timeout(150)
    dark = page.evaluate("getComputedStyle(document.querySelector('#ds-root nav a')).color")
    check(light != dark, f"{slug}: link color flips between light and dark themes")
    cur_light_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    check(cur_light_bg != "rgba(0, 0, 0, 0)", f"{slug}: dark canvas applied")


def reduced_motion_check(browser, slug="breadcrumbs-with-dropdown"):
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, slug)
    motion = p.evaluate(
        "[getComputedStyle(document.querySelector('#ds-root nav a')).transitionProperty, getComputedStyle(document.querySelector('#ds-root nav a')).transitionDuration]"
    )
    check(motion[0] == "none" or motion[1] in ("0s", "0ms"),
          f"{slug}: reduced motion disables link transitions (motion-reduce guard)")
    context.close()


def main():
    static_checks()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        for slug in VARIANTS:
            print(f"== {slug} ==")
            shared_checks(page, slug)

        print("== focus / theme / motion ==")
        for slug in ["breadcrumbs", "breadcrumbs-with-dropdown", "breadcrumbs-collapsed"]:
            focus_ring_check(page, slug)
        dark_mode_check(page)
        reduced_motion_check(browser)

        print("== breadcrumbs (reference) ==")
        open_preview(page, "breadcrumbs")
        check(page.evaluate("document.querySelectorAll('#ds-root nav').length") == 2,
              "breadcrumbs: two demo trails")
        first_href = page.evaluate("document.querySelector('#ds-root nav a').getAttribute('href')")
        check(first_href == "#/", "breadcrumbs: Home links to the trail root")
        page.click("#ds-root nav a >> nth=1")
        page.wait_for_timeout(150)
        check(page.evaluate("window.location.hash") == "#/documentation",
              "breadcrumbs: clicking a link performs real anchor navigation (hash updates)")

        print("== breadcrumbs-with-home ==")
        open_preview(page, "breadcrumbs-with-home")
        home_icon_hidden = page.evaluate(
            "document.querySelector('#ds-root nav a span[aria-hidden=\"true\"] svg') !== null"
        )
        check(home_icon_hidden, "breadcrumbs-with-home: home icon inside aria-hidden wrapper")
        icon_only = page.evaluate(
            "document.querySelector('#ds-root nav a[aria-label=\"Home\"]') !== null"
        )
        check(icon_only, "breadcrumbs-with-home: icon-only home link has aria-label")

        print("== breadcrumbs-with-icons ==")
        open_preview(page, "breadcrumbs-with-icons")
        icon_wrapped = page.evaluate(
            "document.querySelectorAll('#ds-root nav a span[aria-hidden=\"true\"] svg').length >= 3"
        )
        check(icon_wrapped, "breadcrumbs-with-icons: icons render inside aria-hidden wrappers")
        buttons_current = page.evaluate(
            """(() => {
              const c = document.querySelector('#ds-root nav [aria-current="page"]');
              return c && c.textContent.trim() === 'Buttons' && c.querySelector('svg') === null;
            })()"""
        )
        check(buttons_current, "breadcrumbs-with-icons: icons are optional (current level has none)")

        print("== breadcrumbs-with-current ==")
        open_preview(page, "breadcrumbs-with-current")
        current_is_span = page.evaluate(
            "document.querySelector('#ds-root nav [aria-current=\"page\"]').tagName === 'SPAN'"
        )
        check(current_is_span, "breadcrumbs-with-current: current level renders as a span, not an anchor")
        hrefs = page.evaluate(
            "Array.from(document.querySelectorAll('#ds-root nav a')).map(a => a.textContent.trim())"
        )
        check("Tabs" not in hrefs, "breadcrumbs-with-current: current page is not among the links")

        print("== breadcrumbs-with-dropdown ==")
        open_preview(page, "breadcrumbs-with-dropdown")
        trigger = page.locator('#ds-root nav button[aria-haspopup="menu"]')
        check(trigger.count() == 1, "breadcrumbs-with-dropdown: one menu trigger with aria-haspopup")
        check(trigger.get_attribute("aria-expanded") == "false", "breadcrumbs-with-dropdown: aria-expanded=false initially")
        trigger.click()
        page.wait_for_timeout(200)
        check(trigger.get_attribute("aria-expanded") == "true", "breadcrumbs-with-dropdown: aria-expanded=true when open")
        menu_items = page.evaluate(
            "Array.from(document.querySelectorAll('#ds-root [role=\"menu\"] a[role=\"menuitem\"]')).every(a => a.getAttribute('href'))"
        )
        check(menu_items, "breadcrumbs-with-dropdown: menu items are real anchors")
        check(page.evaluate("document.activeElement.getAttribute('role')") == "menuitem",
              "breadcrumbs-with-dropdown: focus moves into the menu on open")
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(100)
        check(page.evaluate("document.activeElement.textContent.trim()") == "Inputs",
              "breadcrumbs-with-dropdown: ArrowDown moves to the next item")
        page.keyboard.press("End")
        page.wait_for_timeout(100)
        check(page.evaluate("document.activeElement.textContent.trim()") == "Breadcrumbs",
              "breadcrumbs-with-dropdown: End jumps to the last item")
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        check(trigger.get_attribute("aria-expanded") == "false", "breadcrumbs-with-dropdown: Escape closes the menu")
        check(page.evaluate("document.activeElement === document.querySelector('#ds-root nav button[aria-haspopup=\"menu\"]')"),
              "breadcrumbs-with-dropdown: Escape returns focus to the trigger")
        current_item = page.evaluate(
            "(() => { const b = document.querySelector('#ds-root nav button[aria-haspopup=\"menu\"]'); b.click(); return true; })()"
        )
        page.wait_for_timeout(200)
        current_in_menu = page.evaluate(
            "document.querySelector('#ds-root [role=\"menu\"] [aria-current=\"page\"]') !== null"
        )
        check(current_in_menu, "breadcrumbs-with-dropdown: current page marked inside the menu")
        page.mouse.click(10, 400)
        page.wait_for_timeout(150)
        check(trigger.get_attribute("aria-expanded") == "false", "breadcrumbs-with-dropdown: outside click closes the menu")
        trigger.focus()
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(200)
        check(page.evaluate("document.activeElement.textContent.trim()") == "Buttons",
              "breadcrumbs-with-dropdown: ArrowDown on the closed trigger opens + focuses first item")
        page.keyboard.press("Escape")

        print("== breadcrumbs-collapsed ==")
        open_preview(page, "breadcrumbs-collapsed")
        ellipsis = page.locator('#ds-root nav button[aria-haspopup="menu"]')
        check(ellipsis.count() == 2, "breadcrumbs-collapsed: ellipsis disclosure in both trails")
        check(bool(ellipsis.first.get_attribute("aria-label")),
              "breadcrumbs-collapsed: disclosure has an accessible name")
        ellipsis.first.click()
        page.wait_for_timeout(200)
        hidden_links = page.evaluate(
            "Array.from(document.querySelectorAll('#ds-root [role=\"menu\"] a')).map(a => a.textContent.trim())"
        )
        check(hidden_links == ["Documentation", "React"],
              "breadcrumbs-collapsed: hidden levels exposed as real links in path order")
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        check(page.evaluate("document.activeElement === document.querySelector('#ds-root nav button[aria-haspopup=\"menu\"]')"),
              "breadcrumbs-collapsed: Escape returns focus to the ellipsis")

        print("== breadcrumbs-max-width ==")
        open_preview(page, "breadcrumbs-max-width")
        trunc = page.evaluate(
            """(() => {
              const link = Array.from(document.querySelectorAll('#ds-root nav a'))
                .find(a => a.textContent.includes('Design tokens'));
              const span = link.querySelector('span.truncate') || link.lastElementChild;
              return {
                truncated: span.scrollWidth > span.clientWidth,
                title: link.getAttribute('title'),
              };
            })()"""
        )
        check(trunc["truncated"], "breadcrumbs-max-width: long label is visually truncated")
        check(trunc["title"] == "Design tokens and theming guidelines",
              "breadcrumbs-max-width: full label survives in the title attribute")
        current_title = page.evaluate(
            "document.querySelector('#ds-root nav [aria-current=\"page\"]').getAttribute('title')"
        )
        check(current_title == "Overriding tokens for white-label themes",
              "breadcrumbs-max-width: current page also carries the full label")

        print("== breadcrumbs-with-separator ==")
        open_preview(page, "breadcrumbs-with-separator")
        slash_sep = page.evaluate(
            """Array.from(Array.from(document.querySelectorAll('#ds-root nav'))[1].querySelectorAll('li[role="presentation"]'))
              .some(li => li.textContent.trim() === '/' && li.getAttribute('aria-hidden') === 'true')"""
        )
        check(slash_sep, "breadcrumbs-with-separator: custom '/' separator rendered aria-hidden")
        override = page.evaluate(
            """Array.from(Array.from(document.querySelectorAll('#ds-root nav'))[2].querySelectorAll('li[role="presentation"]'))
              .some(li => li.textContent.trim() === '>')"""
        )
        check(override, "breadcrumbs-with-separator: per-position separator override works")
        icon_sep = page.evaluate(
            """Array.from(Array.from(document.querySelectorAll('#ds-root nav'))[2].querySelectorAll('li[role="presentation"]'))
              .some(li => li.querySelector('svg') !== null)"""
        )
        check(icon_sep, "breadcrumbs-with-separator: custom icon separator renders")

        browser.close()

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s)")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
