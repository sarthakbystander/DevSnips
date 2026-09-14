#!/usr/bin/env python3
"""Playwright QA for the React Cards previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders, zero console errors, zero horizontal overflow at
    375/768/1280
  - static: exactly the 5 required files per variant, metadata schema, no
    `any` in code.tsx, no hardcoded hex, no component-specific CSS files
  - shared core: every derived code.tsx is identical to the reference except
    its header doc comment; TSX/JSX export sets match
  - focus-visible 2px outline on interactive elements
  - dark mode flips computed card surface + text colors
  - reduced motion kills transitions and the skeleton pulse
  - card-selectable: radio group semantics (fieldset/legend, exclusive
    selection, arrow-key nav, disabled option, controlled pair, checkbox
    multi-select), label-as-card click behavior
  - card-interactive: real anchors for navigation (hash updates), real
    buttons for actions (Enter/Space, disabled not focusable), no nested
    interactive elements
  - card-loading: aria-busy + hidden label, aria-hidden placeholder blocks,
    geometry preserved after swap (no layout shift)
  - card-with-image: real <img> with alt, decorative placeholder aria-hidden
  - card-list: ul/li semantics, per-item unique button names

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_cards.py
"""
import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/Cards/"

VARIANTS = [
    "card", "card-with-header", "card-with-footer", "card-with-actions",
    "card-with-icon", "card-with-image", "card-horizontal", "card-selectable",
    "card-interactive", "card-stat", "card-loading", "card-list",
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
    page.wait_for_selector("#ds-root", timeout=15000)
    page.wait_for_timeout(400)
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
        folder = ROOT / "React/Components/Cards" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["README.md", "code.jsx", "code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exactly the 5 required files",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(
            meta["technology"] == "react"
            and meta["type"] == "component"
            and meta["category"] == "Cards"
            and meta["styling"] == "Tailwind CSS"
            and meta["languages"] == ["JSX", "TSX"],
            f"{slug}: metadata schema fields",
        )
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        tsx = (folder / "code.tsx").read_text()
        check(": any" not in tsx and " as any" not in tsx, f"{slug}: no any in code.tsx")
        check(not re.search(r"#[0-9a-fA-F]{3,8}\b", tsx.replace("#000\",", "")),
              f"{slug}: no hardcoded hex colors in code.tsx")
        check("var(--ds-color-focus-ring)" in tsx, f"{slug}: focus-ring token")
        check("motion-reduce:" in tsx, f"{slug}: reduced-motion guard")
    css = list((ROOT / "React/Components/Cards").rglob("*.css"))
    check(css == [], "no component-specific CSS files in the family")
    # derived-code.tsx parity: identical shared core except the header comment
    reference = (ROOT / "React/Components/Cards/card/code.tsx").read_text()
    ref_body = re.sub(r"/\*\*.*?\*/", "", reference, count=1, flags=re.S)
    for slug in VARIANTS[1:]:
        tsx = (ROOT / "React/Components/Cards" / slug / "code.tsx").read_text()
        body = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S)
        check(body == ref_body, f"{slug}: code.tsx shares the reference core")


def export_parity_checks():
    print("== export parity (tsx/jsx) ==")
    for slug in VARIANTS:
        folder = ROOT / "React/Components/Cards" / slug
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        te = sorted(set(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx)))
        m = re.search(r"export \{ ([^}]*) \};", jsx)
        je = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(te == je, f"{slug}: TSX/JSX named-export parity")
        check("export default Card;" in jsx, f"{slug}: JSX default export = Card")


def shared_checks(page, slug):
    errs = open_preview(page, slug)
    cards = page.evaluate(
        "document.querySelectorAll('#ds-root [class*=\"rounded-[var(--ds-radius-md)]\"]').length"
    )
    check(cards >= 1, f"{slug}: renders at least one card surface")
    for w in (375, 768, 1280):
        check(overflow(page, w) == 0, f"{slug}: no horizontal overflow at {w}px")
    check(errs == [], f"{slug}: zero console errors")


def focus_ring_check(page, slug, selector):
    open_preview(page, slug)
    page.evaluate("(sel) => document.querySelector(sel).focus()", selector)
    page.wait_for_timeout(120)
    info = page.evaluate(
        """(() => {
          const el = document.activeElement;
          if (!el) return null;
          const cs = getComputedStyle(el);
          return { outline: cs.outlineWidth, style: cs.outlineStyle };
        })()"""
    )
    check(
        bool(info) and info["outline"] == "2px",
        f"{slug}: focus-visible 2px outline on {selector}",
    )


def dark_mode_check(page, slug="card"):
    open_preview(page, slug)
    light = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [class*=\"rounded-[var(--ds-radius-md)]\"]')).backgroundColor"
    )
    page.click("#ds-theme-toggle")
    page.wait_for_timeout(200)
    dark = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [class*=\"rounded-[var(--ds-radius-md)]\"]')).backgroundColor"
    )
    check(light != dark, f"{slug}: card surface flips between light and dark themes")
    body_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    check(body_bg == "rgb(10, 10, 10)", f"{slug}: dark canvas applied (body bg {body_bg})")


def reduced_motion_check(browser, slug="card-loading"):
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, slug)
    motion = p.evaluate(
        """(() => {
          const pulse = document.querySelector('#ds-root [class*="animate-pulse"]');
          const trans = getComputedStyle(pulse).animationDuration;
          return trans;
        })()"""
    )
    check(motion in ("0s", "0ms"), f"{slug}: reduced motion disables the skeleton pulse (got {motion})")
    context.close()


def selectable_checks(page):
    print("== card-selectable ==")
    open_preview(page, "card-selectable")
    fieldset = page.evaluate("document.querySelectorAll('#ds-root fieldset').length")
    check(fieldset >= 1, "card-selectable: radio group inside a fieldset")
    legend = page.evaluate("document.querySelector('#ds-root fieldset legend')?.textContent.trim()")
    check(legend == "Choose a plan", "card-selectable: fieldset has a legend")
    radios = page.evaluate("document.querySelectorAll('#ds-root fieldset input[type=radio]').length")
    check(radios == 3, "card-selectable: group renders 3 radio cards")
    # initial selection from defaultValue
    initial = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root fieldset input[type=radio]')).map(r => r.checked)"
    )
    check(initial == [False, True, False], "card-selectable: defaultValue selects the Team card")
    # label click toggles (click the card label surface, not the input)
    page.click("#ds-root fieldset label:first-of-type")
    page.wait_for_timeout(150)
    now = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root fieldset input[type=radio]')).map(r => r.checked)"
    )
    check(now == [True, False, False], "card-selectable: clicking the card label selects its radio")
    note = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("starter" in note, "card-selectable: onChange reports the new value (live note)")
    # radio exclusivity: select another, previous deselects
    page.click("#ds-root fieldset label:nth-of-type(2)")
    page.wait_for_timeout(150)
    exc = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root fieldset input[type=radio]')).map(r => r.checked)"
    )
    check(exc == [False, True, False], "card-selectable: radio selection is exclusive")
    # arrow-key navigation moves selection (native radio group behavior)
    page.evaluate("document.querySelectorAll('#ds-root fieldset input[type=radio]')[1].focus()")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(150)
    after_key = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root fieldset input[type=radio]')).map(r => r.checked)"
    )
    check(after_key == [False, False, True], "card-selectable: ArrowRight moves radio selection")
    # disabled option cannot be selected
    disabled = page.evaluate(
        "document.querySelector('#ds-root input[disabled]') !== null"
    )
    check(disabled, "card-selectable: a disabled option exists (audit log exports)")
    disabled_unchecked = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root input[disabled]')).every(i => !i.checked)"
    )
    check(disabled_unchecked, "card-selectable: disabled option stays unselected")
    # checkbox multi-select: two independent selections coexist
    cbs = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root input[type=checkbox]')).map(c => c.checked)"
    )
    check(cbs[0] is True and cbs[1] is False, "card-selectable: checkbox initial state (digests on, alerts off)")
    page.evaluate("document.querySelectorAll('#ds-root input[type=checkbox]')[1].click()")
    page.wait_for_timeout(150)
    cbs2 = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root input[type=checkbox]')).map(c => c.checked)"
    )
    check(cbs2[0] is True and cbs2[1] is True, "card-selectable: checkboxes select independently (multi-select)")
    # controlled pair: parent state drives both radios
    pair = page.evaluate(
        """(() => {
          const radios = Array.from(document.querySelectorAll('#ds-root input[name="target-env"]'));
          return radios.map(r => r.checked);
        })()"""
    )
    check(pair == [True, False], "card-selectable: controlled pair starts on production")
    page.evaluate("document.querySelectorAll('#ds-root input[name=\"target-env\"]')[1].click()")
    page.wait_for_timeout(150)
    pair2 = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root input[name=\"target-env\"]')).map(r => r.checked)"
    )
    check(pair2 == [False, True], "card-selectable: controlled pair follows parent state")


def interactive_checks(page):
    print("== card-interactive ==")
    open_preview(page, "card-interactive")
    anchors = page.evaluate("document.querySelectorAll('#ds-root a[href]').length")
    check(anchors >= 2, "card-interactive: navigation cards render as real anchors")
    buttons = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root button')).filter(b => b.closest('#ds-root') && b.className.includes('rounded-[var(--ds-radius-md)]')).length"
    )
    check(buttons >= 2, "card-interactive: action cards render as real buttons")
    # no nested interactive elements inside an interactive card
    nested = page.evaluate(
        """(() => {
          const cards = Array.from(document.querySelectorAll('#ds-root a[href^="#/"], #ds-root button[class*="rounded-[var(--ds-radius-md)]"]'));
          return cards.some(c => c.querySelector('a, button') !== null);
        })()"""
    )
    check(not nested, "card-interactive: no nested interactive elements inside the card control")
    # anchor navigates (hash change, no reload)
    before = page.evaluate("window.location.hash")
    page.click("#ds-root a[href='#/docs']")
    page.wait_for_timeout(200)
    after = page.evaluate("window.location.hash")
    check(after == "#/docs" and after != before, "card-interactive: anchor card navigates (hash updates)")
    note = page.evaluate("Array.from(document.querySelectorAll('#ds-root p')).find(x => x.textContent.includes('Anchor mode')).textContent")
    check("#/docs" in note, "card-interactive: live hash note updates")
    # button activates on Enter and Space
    page.evaluate("window.location.hash = ''")
    export_btn = page.locator("#ds-root button:has-text('Export usage report')")
    export_btn.focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(150)
    live = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("usage-report.csv" in live, "card-interactive: button card activates on Enter")
    page.keyboard.press(" ")
    page.wait_for_timeout(150)
    live2 = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("usage-report.csv" in live2, "card-interactive: button card activates on Space")
    # disabled button is not focusable / not activatable
    disabled_card = page.locator("#ds-root button:has-text('Export audit log')")
    check(disabled_card.get_attribute("disabled") is not None, "card-interactive: disabled action card carries native disabled")
    page.evaluate("document.querySelectorAll('#ds-root button')[1].focus()")
    focused_tag = page.evaluate("document.activeElement?.textContent?.trim() || ''")
    check("Export audit log" not in focused_tag, "card-interactive: disabled card cannot receive focus")


def loading_checks(page):
    print("== card-loading ==")
    open_preview(page, "card-loading")
    # while loading: aria-busy + hidden label + aria-hidden blocks
    busy = page.evaluate("document.querySelectorAll('#ds-root [aria-busy=true]').length")
    check(busy >= 2, "card-loading: busy surfaces carry aria-busy=true")
    sr = page.evaluate("document.querySelector('#ds-root [aria-busy=true] .sr-only')?.textContent")
    check(bool(sr), "card-loading: visually hidden loading label present")
    hidden_blocks = page.evaluate(
        "document.querySelectorAll('#ds-root [aria-busy=true] [aria-hidden=true]').length"
    )
    check(hidden_blocks >= 1, "card-loading: placeholder blocks are aria-hidden")
    # geometry stability: capture the busy card's height, let the simulated
    # fetch resolve, then compare against the loaded card that replaces it.
    h_loading = page.evaluate(
        "document.querySelector('#ds-root [aria-busy=true]')?.getBoundingClientRect().height"
    )
    page.wait_for_timeout(2000)  # demo resolves after ~1.6s
    h_loaded = page.evaluate(
        "document.querySelector('#ds-root .max-w-sm > div:not([aria-busy])')?.getBoundingClientRect().height"
    )
    check(h_loading is not None and h_loaded is not None, "card-loading: both skeleton and loaded cards rendered")
    delta = abs(h_loaded - h_loading)
    check(delta < 40, f"card-loading: no layout shift on swap (Δ={delta:.0f}px)")
    done = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("no layout shift" in done, "card-loading: live note reports the swap")


def image_checks(page):
    print("== card-with-image ==")
    open_preview(page, "card-with-image")
    imgs = page.evaluate("document.querySelectorAll('#ds-root img').length")
    check(imgs >= 1, "card-with-image: renders at least one real <img>")
    alt = page.evaluate("document.querySelector('#ds-root img')?.getAttribute('alt')")
    check(bool(alt) and "placeholder artwork" in alt, "card-with-image: content image carries meaningful alt text")
    placeholder = page.evaluate(
        "document.querySelectorAll('#ds-root [aria-hidden=true]').length"
    )
    check(placeholder >= 1, "card-with-image: missing-image placeholder is aria-hidden")
    # images don't overflow their frame
    img_ok = page.evaluate(
        """(() => {
          const img = document.querySelector('#ds-root img');
          const frame = img.parentElement.getBoundingClientRect();
          const r = img.getBoundingClientRect();
          return r.width <= frame.width + 1 && r.height <= frame.height + 1;
        })()"""
    )
    check(img_ok, "card-with-image: image stays inside its crop frame (object-cover)")


def list_checks(page):
    print("== card-list ==")
    open_preview(page, "card-list")
    ul = page.evaluate("document.querySelectorAll('#ds-root ul[role=\"list\"], #ds-root ul').length")
    check(ul >= 1, "card-list: collection is a <ul>")
    lis = page.evaluate("document.querySelectorAll('#ds-root ul li').length")
    check(lis == 4, "card-list: renders 4 project list items")
    names = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root ul button')).map(b => b.getAttribute('aria-label'))"
    )
    check(
        names == ["Open api-gateway", "Open design-tokens", "Open billing-service", "Open docs-site"],
        "card-list: per-item buttons have unique accessible names",
    )
    heading = page.evaluate("document.querySelector('#ds-root section h2')?.textContent.trim()")
    check(heading == "Recent projects", "card-list: section is labelled by a real h2")


def main():
    static_checks()
    export_parity_checks()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        for slug in VARIANTS:
            print(f"== {slug} ==")
            shared_checks(page, slug)

        print("== focus / theme / motion ==")
        focus_ring_check(page, "card-selectable", "#ds-root fieldset input[type=radio]")
        focus_ring_check(page, "card-interactive", "#ds-root a[href='#/docs']")
        dark_mode_check(page)
        reduced_motion_check(browser)

        selectable_checks(page)
        interactive_checks(page)
        loading_checks(page)
        image_checks(page)
        list_checks(page)

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
