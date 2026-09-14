#!/usr/bin/env python3
"""Playwright QA for the React Tabs previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: tablist/tab/tabpanel roles, aria-selected/aria-controls/
    aria-labelledby associations, zero console errors, zero horizontal
    overflow at 375/768/1280
  - tabs: click switches selection; Arrow keys + Home/End navigate; roving
    tabIndex (exactly one tabbable tab per list); controlled + uncontrolled
  - tabs-with-icons: icons render inside aria-hidden wrappers
  - tabs-with-badge: badge chips render with the accent token
  - tabs-with-count: count chips render with tabular figures
  - tabs-underline: selected tab carries the 2px primary underline
  - tabs-contained: tablist sits on a surface; selected tab lifts
  - tabs-vertical: aria-orientation=vertical; ArrowUp/ArrowDown navigate;
    layout stacks below sm
  - tabs-scrollable: the list scrolls horizontally; keyboard focus scrolls
    into view
  - tabs-disabled: disabled tabs cannot activate and are skipped by keys
  - tabs-with-panel: every panel stays mounted; only the active one is
    visible (hidden attribute toggles)
  - tabs-with-add-action: the + button is outside the tablist, has an
    accessible name, and actually adds + selects a tab
  - dark mode flips the computed surface colors
  - reduced motion collapses transitions to 0s

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_tabs.py
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/Tabs/"

VARIANTS = [
    "tabs", "tabs-with-icons", "tabs-with-badge", "tabs-with-count",
    "tabs-underline", "tabs-contained", "tabs-vertical", "tabs-scrollable",
    "tabs-disabled", "tabs-with-panel", "tabs-with-add-action",
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
    page.wait_for_selector('#ds-root [role="tablist"] [role="tab"]', timeout=15000)
    page.wait_for_timeout(300)
    return errs


def overflow(page, w):
    page.set_viewport_size({"width": w, "height": 900})
    page.wait_for_timeout(150)
    return page.evaluate(
        "() => Math.max(document.documentElement.scrollWidth - window.innerWidth, 0)"
    )


def selected_tab(page, scope=0):
    return page.locator('#ds-root [role="tablist"]').nth(scope).locator('[role="tab"][aria-selected="true"]')


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()

        # ---------------- generic pass: structure + semantics ------------
        print("== generic structure pass ==")
        for slug in VARIANTS:
            errs = open_preview(page, slug)
            tabs = page.locator('#ds-root [role="tab"]').all()
            check(len(tabs) >= 2, f"{slug}: >=2 tabs render")
            check(len(errs) == 0, f"{slug}: zero console errors")
            # every tab's aria-controls points at a real panel, and the panel
            # points back via aria-labelledby
            assoc_ok = True
            for tab in tabs:
                tid = tab.get_attribute("id")
                pid = tab.get_attribute("aria-controls")
                if not tid or not pid:
                    assoc_ok = False
                    break
                panel = page.locator(f"#{pid}")
                if panel.count() != 1:
                    assoc_ok = False
                    break
                if panel.get_attribute("aria-labelledby") != tid:
                    assoc_ok = False
                    break
                if panel.get_attribute("role") != "tabpanel":
                    assoc_ok = False
                    break
            check(assoc_ok, f"{slug}: aria-controls/aria-labelledby associations")
            for w in (375, 768, 1280):
                check(overflow(page, w) == 0, f"{slug}: zero overflow @ {w}px")

        # ---------------- tabs (reference) -------------------------------
        print("== tabs ==")
        open_preview(page, "tabs")
        first = page.locator('#ds-root [role="tablist"]').nth(0)
        check(selected_tab(page).text_content().strip() == "Activity",
              "tabs: default controlled selection is Activity")
        first.locator('[role="tab"]').nth(2).click()  # Files
        check(selected_tab(page).text_content().strip() == "Files",
              "tabs: click selects Files")
        panel_text = page.locator('#ds-root [role="tabpanel"]:not([hidden])').nth(0).text_content()
        check("8 tracked files" in panel_text, "tabs: Files panel visible after selection")
        # roving tabIndex: exactly one tabbable tab in each list
        for i in range(2):
            tabs_in_list = page.locator('#ds-root [role="tablist"]').nth(i).locator('[role="tab"]')
            zero = tabs_in_list.evaluate_all("els => els.filter(e => e.tabIndex === 0).length")
            check(zero == 1, f"tabs: list {i} roving tabIndex (one tabbable tab)")
        # keyboard: ArrowRight/ArrowLeft wrap, Home/End
        first.locator('[role="tab"][aria-selected="true"]').focus()
        page.keyboard.press("ArrowRight")
        check(selected_tab(page).text_content().strip() == "Settings", "tabs: ArrowRight moves to Settings")
        page.keyboard.press("ArrowRight")  # wraps to Overview
        check(selected_tab(page).text_content().strip() == "Overview", "tabs: ArrowRight wraps to Overview")
        page.keyboard.press("ArrowLeft")   # wraps back to Settings
        check(selected_tab(page).text_content().strip() == "Settings", "tabs: ArrowLeft wraps to Settings")
        page.keyboard.press("Home")
        check(selected_tab(page).text_content().strip() == "Overview", "tabs: Home activates first tab")
        page.keyboard.press("End")
        check(selected_tab(page).text_content().strip() == "Settings", "tabs: End activates last tab")
        focused = page.evaluate("() => document.activeElement && document.activeElement.textContent.trim()")
        check(focused == "Settings", "tabs: focus follows selection (automatic activation)")
        note = page.locator("#ds-root").text_content()
        check("current value: settings" in note.replace("\n", " "), "tabs: controlled note reflects value")
        # uncontrolled second list works on its own
        second = page.locator('#ds-root [role="tablist"]').nth(1)
        second.locator('[role="tab"]').nth(1).click()
        check(second.locator('[role="tab"][aria-selected="true"]').text_content().strip() == "History",
              "tabs: uncontrolled defaultValue list selects History")
        # focus-visible ring on keyboard-driven focus
        first.locator('[role="tab"][aria-selected="true"]').focus()
        page.keyboard.press("ArrowRight")
        style = page.evaluate("""() => {
          const el = document.activeElement;
          const cs = getComputedStyle(el);
          return [cs.outlineWidth, cs.outlineStyle, cs.outlineColor];
        }""")
        check(style[0] == "2px" and style[1] in ("auto", "solid"),
              f"tabs: focus-visible ring (2px {style[1]})")

        # ---------------- tabs-with-icons --------------------------------
        print("== tabs-with-icons ==")
        open_preview(page, "tabs-with-icons")
        tabs = page.locator('#ds-root [role="tab"]')
        icons_ok = True
        for i in range(tabs.count()):
            icon = tabs.nth(i).locator('span[aria-hidden="true"] svg')
            if icon.count() != 1:
                icons_ok = False
        check(icons_ok, "tabs-with-icons: every tab carries an aria-hidden icon")
        tabs.nth(1).click()
        check(selected_tab(page).text_content().strip() == "Notifications",
              "tabs-with-icons: click selects Notifications")

        # ---------------- tabs-with-badge --------------------------------
        print("== tabs-with-badge ==")
        open_preview(page, "tabs-with-badge")
        list_text = page.locator('#ds-root [role="tablist"]').text_content()
        check("New" in list_text and "Beta" in list_text, "tabs-with-badge: New + Beta chips render")
        badge_cls = page.locator('#ds-root [role="tab"]').nth(1).locator("span").last.get_attribute("class")
        check("accent" in badge_cls, "tabs-with-badge: badge uses the accent token")

        # ---------------- tabs-with-count --------------------------------
        print("== tabs-with-count ==")
        open_preview(page, "tabs-with-count")
        count_tab = page.locator('#ds-root [role="tab"]').nth(1)
        check("12" in count_tab.text_content(), "tabs-with-count: count 12 renders")
        chip = count_tab.locator("span").last
        check("tabular-nums" in (chip.get_attribute("class") or ""),
              "tabs-with-count: count chip uses tabular figures")
        count_tab.click()
        check(selected_tab(page).text_content().strip().startswith("Comments"),
              "tabs-with-count: count tab activates")

        # ---------------- tabs-underline ---------------------------------
        print("== tabs-underline ==")
        open_preview(page, "tabs-underline")
        sel = selected_tab(page)
        bw = sel.evaluate("el => getComputedStyle(el).borderBottomWidth")
        bc = sel.evaluate("el => getComputedStyle(el).borderBottomColor")
        check(bw == "2px", "tabs-underline: selected underline is 2px")
        check(bc != "rgba(0, 0, 0, 0)" and bc != "transparent", "tabs-underline: underline has the primary color")
        idle = page.locator('#ds-root [role="tab"][aria-selected="false"]').first
        ibc = idle.evaluate("el => getComputedStyle(el).borderBottomColor")
        check(ibc == "rgba(0, 0, 0, 0)" or ibc == "transparent", "tabs-underline: idle underline transparent")

        # ---------------- tabs-contained ---------------------------------
        print("== tabs-contained ==")
        open_preview(page, "tabs-contained")
        lst = page.locator('#ds-root [role="tablist"]').first
        lbg = lst.evaluate("el => getComputedStyle(el).backgroundColor")
        check(lbg not in ("rgba(0, 0, 0, 0)", "transparent"), "tabs-contained: tablist sits on a surface")
        sbg = selected_tab(page).evaluate("el => getComputedStyle(el).backgroundColor")
        check(sbg != lbg, "tabs-contained: selected tab lifts onto a different surface")

        # ---------------- tabs-vertical ----------------------------------
        print("== tabs-vertical ==")
        open_preview(page, "tabs-vertical")
        lst = page.locator('#ds-root [role="tablist"]').first
        check(lst.get_attribute("aria-orientation") == "vertical", "tabs-vertical: aria-orientation=vertical")
        selected_tab(page).focus()
        page.keyboard.press("ArrowDown")
        check(selected_tab(page).text_content().strip() == "Security", "tabs-vertical: ArrowDown navigates")
        page.keyboard.press("ArrowUp")
        check(selected_tab(page).text_content().strip() == "General", "tabs-vertical: ArrowUp navigates")
        # mobile stacking: list above the panel at 375
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(150)
        lst_box = page.locator('#ds-root [role="tablist"]').first.bounding_box()
        panel_box = page.locator('#ds-root [role="tabpanel"]:not([hidden])').first.bounding_box()
        check(lst_box["y"] + lst_box["height"] <= panel_box["y"] + 1,
              "tabs-vertical: list stacks above the panel below sm")

        # ---------------- tabs-scrollable --------------------------------
        print("== tabs-scrollable ==")
        open_preview(page, "tabs-scrollable")
        lst = page.locator('#ds-root [role="tablist"]').first
        dims = lst.evaluate("el => [el.scrollWidth, el.clientWidth]")
        check(dims[0] > dims[1], "tabs-scrollable: list overflows its container")
        selected_tab(page).focus()
        page.keyboard.press("End")
        page.wait_for_timeout(100)
        sl = lst.evaluate("el => el.scrollLeft")
        check(sl > 0, "tabs-scrollable: keyboard focus scrolls the list")

        # ---------------- tabs-disabled ----------------------------------
        print("== tabs-disabled ==")
        open_preview(page, "tabs-disabled")
        disabled = page.locator('#ds-root [role="tab"][disabled]')
        check(disabled.count() == 2, "tabs-disabled: two disabled tabs")
        # native disabled prevents activation
        disabled.first.evaluate("el => el.click()")
        check(disabled.first.get_attribute("aria-selected") == "false",
              "tabs-disabled: disabled tab cannot activate via click")
        # End skips disabled tabs (last enabled is Activity)
        selected_tab(page).focus()
        page.keyboard.press("End")
        check(selected_tab(page).text_content().strip() == "Activity",
              "tabs-disabled: End skips disabled tabs")
        # disabled tabs are not in the tab order
        ti = disabled.first.evaluate("el => el.tabIndex")
        check(ti == -1, "tabs-disabled: disabled tab not tabbable")

        # ---------------- tabs-with-panel --------------------------------
        print("== tabs-with-panel ==")
        open_preview(page, "tabs-with-panel")
        panels = page.locator('#ds-root [role="tabpanel"]')
        check(panels.count() == 3, "tabs-with-panel: all three panels stay mounted")
        hidden = panels.evaluate_all("els => els.filter(e => e.hidden).length")
        check(hidden == 2, "tabs-with-panel: exactly one panel visible (hidden toggles)")
        page.locator('#ds-root [role="tab"]').nth(2).click()  # Files
        hidden_after = panels.evaluate_all("els => els.filter(e => e.hidden).length")
        check(hidden_after == 2, "tabs-with-panel: switching still keeps panels mounted")

        # ---------------- tabs-with-add-action ---------------------------
        print("== tabs-with-add-action ==")
        open_preview(page, "tabs-with-add-action")
        add = page.locator('#ds-root button[aria-label="Add a project"]')
        check(add.count() == 1, "tabs-with-add-action: add button has an accessible label")
        in_list = add.evaluate("el => !!el.closest('[role=\"tablist\"]')")
        check(in_list is False, "tabs-with-add-action: add button is outside the tablist")
        before = page.locator('#ds-root [role="tab"]').count()
        add.click()
        page.wait_for_timeout(150)
        after = page.locator('#ds-root [role="tab"]').count()
        check(after == before + 1, "tabs-with-add-action: clicking + appends a tab")
        check(selected_tab(page).text_content().strip().startswith("Project"),
              "tabs-with-add-action: the new tab is selected")

        # ---------------- dark mode + reduced motion ---------------------
        print("== dark mode / reduced motion ==")
        open_preview(page, "tabs")
        light_bg = selected_tab(page).evaluate("el => getComputedStyle(el).backgroundColor")
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(150)
        dark_bg = selected_tab(page).evaluate("el => getComputedStyle(el).backgroundColor")
        dark = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        check(dark == "dark" and dark_bg != light_bg, "tabs: dark mode flips the selected surface")

        ctx2 = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
        page2 = ctx2.new_page()
        open_preview(page2, "tabs")
        motion = page2.locator('#ds-root [role="tab"]').first.evaluate(
            "el => [getComputedStyle(el).transitionProperty, getComputedStyle(el).transitionDuration]")
        check(motion[0] == "none" or motion[1] in ("0s", "0ms"),
              "tabs: reduced-motion disables transitions (motion-reduce guard)")
        ctx2.close()

        browser.close()

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s)")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL TABS QA CHECKS PASSED")


if __name__ == "__main__":
    main()
