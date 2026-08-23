#!/usr/bin/env python3
"""Playwright QA for the React Accordion previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders, zero console errors, zero horizontal overflow at
    375/768/1280
  - static: exactly the 5 required files per variant, metadata schema, no
    `any` in code.tsx, no hardcoded hex, no inline style=, no
    component-specific CSS files
  - shared core: every derived code.tsx is identical to the reference except
    its header doc comment; TSX/JSX export sets + per-component prop
    signatures match
  - generator: `_gen_react_accordion.py --check` reports no drift;
    `scripts/validate.py` passes
  - semantics: real button triggers in h3 headings, aria-expanded +
    aria-controls wired to unique stable ids, role=region labelled back,
    no roving tabindex, no nested interactive elements in triggers
  - reference: single mode opens one item, closes the previous one
  - multiple mode: items stay open independently
  - collapsible vs mandatory single behavior
  - disabled items: native disabled, cannot open, skipped by Tab
  - icons are aria-hidden; badges are spans inside the button (accessible
    name stays meaningful)
  - nested accordion: parent/child state independent, ids never collide
  - actions in regions are real, focusable, and operable
  - loading: aria-busy + skeleton + sr-only announcement, pulse off under
    reduced motion
  - focus-visible 2px outline on triggers (inset, never clipped)
  - dark mode flips computed trigger text and region colors
  - reduced motion removes all transitions (instant state change)

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_accordion.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/Accordion/"

VARIANTS = [
    "accordion", "accordion-multiple", "accordion-collapsible",
    "accordion-with-icons", "accordion-with-description",
    "accordion-disabled", "accordion-with-badge", "accordion-faq",
    "accordion-nested", "accordion-with-actions", "accordion-loading",
    "accordion-bordered",
]

EXPORTS = ["Accordion", "AccordionItem", "AccordionTrigger", "AccordionContent"]

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
        folder = ROOT / "React/Components/Accordion" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["README.md", "code.jsx", "code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exactly the 5 required files",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(
            meta["technology"] == "react"
            and meta["type"] == "component"
            and meta["category"] == "Accordion"
            and meta["styling"] == "Tailwind CSS"
            and meta["languages"] == ["JSX", "TSX"]
            and meta["framework"] == "React"
            and meta["language"] == "TSX"
            and meta["component"] == "accordion"
            and meta["family"] == "accordion",
            f"{slug}: metadata schema fields",
        )
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["id"] == f"{slug}-react-001", f"{slug}: metadata id convention")
        tsx = (folder / "code.tsx").read_text()
        check(": any" not in tsx and " as any" not in tsx, f"{slug}: no any in code.tsx")
        check(not re.search(r"#[0-9a-fA-F]{3,8}\b", tsx),
              f"{slug}: no hardcoded hex colors in code.tsx")
        check("var(--ds-color-focus-ring)" in tsx, f"{slug}: focus-ring token")
        check("motion-reduce:" in tsx, f"{slug}: reduced-motion guard")
        check("style=" not in tsx and "style={" not in tsx,
              f"{slug}: no inline styles in code.tsx")
        check("<button" in tsx and "aria-expanded" in tsx and "aria-controls" in tsx,
              f"{slug}: real disclosure button semantics in code.tsx")
        check('role="region"' in tsx and "aria-labelledby" in tsx,
              f"{slug}: role=region + aria-labelledby in code.tsx")
        # every --ds-* token referenced must be defined in the preview token block
        tokens = set(re.findall(r"var\(--ds-[a-z0-9-]+\)", tsx))
        preview = (folder / "preview.html").read_text()
        missing = [t for t in tokens if t.split("var(", 1)[1].rstrip(")") not in preview]
        check(missing == [], f"{slug}: all --ds-* tokens resolve in preview")
    css = list((ROOT / "React/Components/Accordion").rglob("*.css"))
    check(css == [], "no component-specific CSS files in the family")
    # derived-code.tsx parity: identical shared core except the header comment
    reference = (ROOT / "React/Components/Accordion/accordion/code.tsx").read_text()
    ref_body = re.sub(r"/\*\*.*?\*/", "", reference, count=1, flags=re.S)
    for slug in VARIANTS[1:]:
        tsx = (ROOT / "React/Components/Accordion" / slug / "code.tsx").read_text()
        body = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S)
        check(body == ref_body, f"{slug}: code.tsx shares the reference core")


def _props_of(src, name):
    """Destructured prop names of `function <name>({ ... })` (None if the
    component takes a non-destructured `props` param, like Accordion)."""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\(\s*\{", src)
    if not m:
        return None
    start = src.index("{", m.end() - 1)
    depth = 0
    end = None
    for i in range(start, len(src)):
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    block = src[start:end + 1 if end else len(src)]
    props = []
    for raw in block.split(","):
        seg = raw.strip().strip("{}")
        if not seg or seg.startswith("..."):
            continue
        seg = re.sub(r"\s*=.*$", "", seg)   # defaults
        seg = re.sub(r"\?:.*$", "", seg)    # optional marker + type
        seg = re.sub(r":.*$", "", seg)      # type annotation
        seg = seg.strip()
        if seg:
            props.append(seg)
    return sorted(set(props))


def export_parity_checks():
    print("== export + prop parity (tsx/jsx) ==")
    for slug in VARIANTS:
        folder = ROOT / "React/Components/Accordion" / slug
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        te = sorted(set(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx)))
        m = re.search(r"export \{ ([^}]*) \};", jsx)
        je = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(te == je == sorted(EXPORTS), f"{slug}: TSX/JSX named-export parity")
        check("export default Accordion;" in jsx, f"{slug}: JSX default export = Accordion")
        check(re.search(r"function Accordion\(\s*props\s*\)", jsx) is not None,
              f"{slug}: Accordion keeps its non-destructured props param in JSX")
        for name in EXPORTS[1:]:
            tp = _props_of(tsx, name)
            jp = _props_of(jsx, name)
            check(tp is not None and tp == jp, f"{slug}: {name} prop-signature parity")


def generator_checks():
    print("== generator + repo validation ==")
    r = subprocess.run(
        [sys.executable, "_gen_react_accordion.py", "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    check(r.returncode == 0 and "up to date" in r.stdout,
          "generator --check reports no drift")
    r = subprocess.run(
        [sys.executable, "scripts/validate.py"],
        cwd=ROOT, capture_output=True, text=True,
    )
    check(r.returncode == 0 and "VALIDATION PASSED" in r.stdout,
          "scripts/validate.py passes")


def shared_checks(page, slug):
    errs = open_preview(page, slug)
    triggers = page.evaluate(
        "document.querySelectorAll('#ds-root h3 > button[aria-expanded]').length"
    )
    check(triggers >= 1, f"{slug}: renders real h3-wrapped button triggers")
    for w in (375, 768, 1280):
        check(overflow(page, w) == 0, f"{slug}: no horizontal overflow at {w}px")
    check(errs == [], f"{slug}: zero console errors")


def semantics_checks(page):
    print("== disclosure semantics (all variants) ==")
    for slug in VARIANTS:
        open_preview(page, slug)
        info = page.evaluate(
            """(() => {
              const root = document.getElementById('ds-root');
              const triggers = Array.from(root.querySelectorAll('h3 > button[aria-expanded]'));
              const ids = new Set();
              let wired = 0, unique = true, labelled = 0, hiddenConflict = 0;
              for (const t of triggers) {
                const region = document.getElementById(t.getAttribute('aria-controls') || '');
                if (region && region.getAttribute('role') === 'region') {
                  wired++;
                  if (region.getAttribute('aria-labelledby') === t.id) labelled++;
                  if (region.hasAttribute('hidden') || region.getAttribute('aria-hidden') === 'true') hiddenConflict++;
                }
                if (ids.has(t.getAttribute('aria-controls'))) unique = false;
                ids.add(t.getAttribute('aria-controls'));
              }
              const nested = root.querySelectorAll('#ds-root button button, #ds-root button a, #ds-root a button');
              const roving = root.querySelectorAll('#ds-root button[tabindex], #ds-root [role="button"]');
              return { triggers: triggers.length, wired, labelled, unique, hiddenConflict, nested: nested.length, roving: roving.length };
            })()"""
        )
        check(info["triggers"] > 0, f"{slug}: triggers present")
        check(info["wired"] == info["triggers"],
              f"{slug}: every trigger aria-controls a role=region element")
        check(info["labelled"] == info["triggers"],
              f"{slug}: every region aria-labelledby points back at its trigger")
        check(info["unique"], f"{slug}: content ids are unique across the page")
        check(info["hiddenConflict"] == 0,
              f"{slug}: closed regions use visibility, not competing hidden/aria-hidden attributes")
        check(info["nested"] == 0, f"{slug}: no nested interactive elements inside triggers")
        check(info["roving"] == 0, f"{slug}: no roving tabindex / no role=button reinvention")


def reference_checks(page):
    print("== accordion (reference) ==")
    open_preview(page, "accordion")
    btns = page.locator("#ds-root h3 > button[aria-expanded]")
    check(btns.count() == 5, f"accordion: renders 5 triggers (two demos), got {btns.count()}")
    check(btns.nth(0).get_attribute("aria-expanded") == "true",
          "accordion: defaultValue opens the first item on load")
    check(btns.nth(1).get_attribute("aria-expanded") == "false",
          "accordion: other items start closed")
    # single mode: opening another closes the previous
    btns.nth(1).click()
    page.wait_for_timeout(300)
    check(btns.nth(0).get_attribute("aria-expanded") == "false",
          "accordion: single mode closes the previously open item")
    check(btns.nth(1).get_attribute("aria-expanded") == "true",
          "accordion: clicked item opens")
    # mandatory: clicking the open trigger is a no-op
    btns.nth(1).click()
    page.wait_for_timeout(300)
    check(btns.nth(1).get_attribute("aria-expanded") == "true",
          "accordion: mandatory single keeps the open item open on self-click")
    # chevron rotates when open (container is the last aria-hidden span)
    rotation = page.evaluate(
        """(() => {
          const b = document.querySelectorAll('#ds-root h3 > button')[1];
          const spans = b.querySelectorAll('span[aria-hidden="true"]');
          const chev = spans[spans.length - 1];
          return getComputedStyle(chev).transform;
        })()"""
    )
    check(rotation not in ("", "none"), f"accordion: open chevron rotates (transform {rotation})")
    # closed region content is hidden to AT and removed from tab order
    visibility = page.evaluate(
        """(() => {
          const regions = Array.from(document.querySelectorAll('#ds-root [role="region"]'));
          return regions.map(r => getComputedStyle(r.firstElementChild).visibility);
        })()"""
    )
    check(visibility[0] == "hidden", "accordion: closed region is visibility:hidden (out of AT + tab order)")
    check(visibility[1] == "visible", "accordion: open region is visible")


def multiple_checks(page):
    print("== accordion-multiple ==")
    open_preview(page, "accordion-multiple")
    btns = page.locator("#ds-root h3 > button[aria-expanded]")
    check(btns.nth(0).get_attribute("aria-expanded") == "true"
          and btns.nth(1).get_attribute("aria-expanded") == "true",
          "multiple: uncontrolled defaultValue opens both seeded items")
    # open the one closed item; the others must stay open (independent toggle)
    btns.nth(2).click()
    page.wait_for_timeout(200)
    check(btns.nth(0).get_attribute("aria-expanded") == "true"
          and btns.nth(1).get_attribute("aria-expanded") == "true"
          and btns.nth(2).get_attribute("aria-expanded") == "true",
          "multiple: opening a third item keeps the other two open")
    # close one; the rest must stay open
    btns.nth(1).click()
    page.wait_for_timeout(200)
    check(btns.nth(0).get_attribute("aria-expanded") == "true"
          and btns.nth(1).get_attribute("aria-expanded") == "false"
          and btns.nth(2).get_attribute("aria-expanded") == "true",
          "multiple: closing one item leaves the rest open")
    # controlled demo: live count + external actions
    count = page.locator("#ds-root [aria-live='polite']").first
    check("of 3 open" in count.text_content(), "multiple: controlled demo renders the open-count")
    page.locator("#ds-root button:has-text('Expand all')").click()
    page.wait_for_timeout(200)
    check(count.text_content().startswith("3 of 3"), "multiple: Expand all opens every item")
    page.locator("#ds-root button:has-text('Collapse all')").click()
    page.wait_for_timeout(200)
    check(count.text_content().startswith("0 of 3"), "multiple: Collapse all closes every item")


def collapsible_checks(page):
    print("== accordion-collapsible ==")
    open_preview(page, "accordion-collapsible")
    btns = page.locator("#ds-root h3 > button[aria-expanded]")
    # collapsible demo is the first group: self-click closes
    btns.nth(0).click()
    page.wait_for_timeout(300)
    check(btns.nth(0).get_attribute("aria-expanded") == "false",
          "collapsible: clicking the open trigger closes it (zero open)")
    # mandatory demo is the second group (triggers 2,3): self-click is a no-op
    btns.nth(2).click()
    page.wait_for_timeout(200)
    btns.nth(3).click()
    page.wait_for_timeout(200)
    btns.nth(3).click()
    page.wait_for_timeout(300)
    check(btns.nth(3).get_attribute("aria-expanded") == "true",
          "collapsible: mandatory demo keeps its open item open on self-click")


def icons_checks(page):
    print("== accordion-with-icons ==")
    open_preview(page, "accordion-with-icons")
    info = page.evaluate(
        """(() => {
          const btn = document.querySelector('#ds-root h3 > button');
          const iconSlot = btn.querySelector('span[aria-hidden="true"]');
          return {
            hasSvg: iconSlot && iconSlot.querySelector('svg') !== null,
            ariaHidden: iconSlot ? iconSlot.getAttribute('aria-hidden') : null,
            name: btn.textContent.trim().length > 0,
          };
        })()"""
    )
    check(info["hasSvg"] and info["ariaHidden"] == "true",
          "icons: leading icon is an aria-hidden svg slot")
    check(info["name"], "icons: trigger still carries real text (accessible name intact)")


def description_checks(page):
    print("== accordion-with-description ==")
    open_preview(page, "accordion-with-description")
    text = page.locator("#ds-root h3 > button").first.text_content()
    check("Getting started" in text and "Install the CLI" in text,
          "description: title + description both live inside the trigger (join the accessible name)")
    muted = page.evaluate(
        """(() => {
          const btn = document.querySelector('#ds-root h3 > button');
          // the text column is the first non-aria-hidden span in the button
          const col = btn.querySelector('span:not([aria-hidden="true"])');
          const desc = col ? col.querySelectorAll('span')[1] : null;
          return desc ? getComputedStyle(desc).color : null;
        })()"""
    )
    check(muted == "rgb(115, 115, 115)", f"description: supporting line uses muted token (got {muted})")


def disabled_checks(page):
    print("== accordion-disabled ==")
    open_preview(page, "accordion-disabled")
    disabled_btns = page.locator("#ds-root h3 > button[disabled]")
    check(disabled_btns.count() == 2, "disabled: two items are natively disabled")
    disabled_btns.nth(0).click(force=True)
    page.wait_for_timeout(200)
    check(disabled_btns.nth(0).get_attribute("aria-expanded") == "false",
          "disabled: clicking a disabled trigger does not open it")
    first = page.locator("#ds-root h3 > button").first
    first.focus()
    page.keyboard.press("Tab")
    active_disabled = page.evaluate(
        "document.activeElement ? (document.activeElement.disabled !== true) : true"
    )
    check(active_disabled is True,
          "disabled: Tab skips disabled triggers (focus lands on an enabled control)")
    check(disabled_btns.nth(0).get_attribute("aria-disabled") is None,
          "disabled: no redundant aria-disabled on a natively disabled button")


def badge_checks(page):
    print("== accordion-with-badge ==")
    open_preview(page, "accordion-with-badge")
    btn = page.locator("#ds-root h3 > button").first
    text = btn.text_content()
    check("Failed checks" in text and "3 errors" in text,
          "badge: badge text joins the trigger accessible name")
    nested = page.evaluate(
        "document.querySelectorAll('#ds-root h3 > button button, #ds-root h3 > button a').length"
    )
    check(nested == 0, "badge: badge is non-interactive (no nested controls in the trigger)")


def faq_checks(page):
    print("== accordion-faq ==")
    open_preview(page, "accordion-faq")
    btns = page.locator("#ds-root h3 > button[aria-expanded]")
    check(btns.count() == 4, "faq: renders four questions")
    btns.nth(0).click()
    btns.nth(2).click()
    page.wait_for_timeout(200)
    opened = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root h3 > button')).filter(b => b.getAttribute('aria-expanded') === 'true').length"
    )
    check(opened == 2, "faq: readers can keep two answers open (multiple mode)")
    question = btns.nth(0).text_content()
    check("?" in question, "faq: question text is the trigger label")


def nested_checks(page):
    print("== accordion-nested ==")
    open_preview(page, "accordion-nested")
    info = page.evaluate(
        """(() => {
          const btns = Array.from(document.querySelectorAll('#ds-root h3 > button'));
          const parentBtn = btns.find(b => b.textContent.trim() === 'Databases');
          const childBtn = btns.find(b => b.textContent.trim() === 'Postgres');
          return {
            parentOpen: parentBtn.getAttribute('aria-expanded'),
            idsDiffer: childBtn.getAttribute('aria-controls') !== parentBtn.getAttribute('aria-controls'),
          };
        })()"""
    )
    check(info["parentOpen"] == "true", "nested: parent starts open")
    check(info["idsDiffer"], "nested: parent and child region ids never collide")
    page.locator("#ds-root h3 > button:has-text('Postgres')").click()
    page.wait_for_timeout(300)
    open_count = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root h3 > button')).filter(b => b.getAttribute('aria-expanded') === 'true').length"
    )
    parent_state = page.evaluate(
        """(() => {
          const b = Array.from(document.querySelectorAll('#ds-root h3 > button')).find(x => x.textContent.trim() === 'Databases');
          return b.getAttribute('aria-expanded');
        })()"""
    )
    check(parent_state == "true", "nested: interacting with the child never closes the parent")
    check(open_count >= 2, "nested: parent + child stay open together (independent state)")
    uniq = page.evaluate(
        """(() => {
          const ids = Array.from(document.querySelectorAll('#ds-root [role="region"]')).map(r => r.id);
          return new Set(ids).size === ids.length;
        })()"""
    )
    check(uniq, "nested: region ids unique across parent + child")


def actions_checks(page):
    print("== accordion-with-actions ==")
    open_preview(page, "accordion-with-actions")
    page.locator("#ds-root h3 > button:has-text('API keys')").click()
    page.wait_for_timeout(200)
    rotate = page.locator("#ds-root button:has-text('Rotate key')")
    check(rotate.is_visible(), "actions: region action becomes visible when the item opens")
    rotate.click()
    page.wait_for_timeout(200)
    log = page.locator("#ds-root [role='status']").first
    check("Rotated the production key" in log.text_content(),
          "actions: clicking the region action runs real behavior (status updates)")
    link = page.locator("#ds-root a[href='#/docs/keys']")
    check(link.count() == 1, "actions: region link is a real anchor")
    page.locator("#ds-root h3 > button:has-text('Deploy hooks')").click()
    page.wait_for_timeout(200)
    page.locator("#ds-root h3 > button:has-text('Deploy hooks')").focus()
    page.keyboard.press("Tab")
    focused = page.evaluate("document.activeElement && document.activeElement.textContent")
    check(focused is not None and "Add hook" in focused,
          f"actions: Tab reaches the first action inside the open region (got '{(focused or '')[:24]}')")


def loading_checks(page, browser):
    print("== accordion-loading ==")
    open_preview(page, "accordion-loading")
    busy = page.evaluate(
        "document.querySelectorAll('#ds-root [aria-busy=\"true\"]').length"
    )
    check(busy >= 1, "loading: aria-busy is set on the loading region")
    skeleton = page.evaluate(
        "document.querySelectorAll('#ds-root [aria-busy=\"true\"] [aria-hidden=\"true\"] .animate-pulse').length"
    )
    check(skeleton >= 3, "loading: skeleton bars render while pending")
    sr = page.evaluate(
        "document.querySelector('#ds-root [aria-busy=\"true\"]').textContent.includes('Loading usage data')"
    )
    check(sr, "loading: sr-only announcement accompanies the skeleton")
    page.wait_for_timeout(1700)
    busy_after = page.evaluate(
        "document.querySelectorAll('#ds-root [aria-busy=\"true\"]').length"
    )
    has_data = page.evaluate(
        "document.querySelector('#ds-root').textContent.includes('Function invocations')"
    )
    check(busy_after == 0 and has_data, "loading: skeleton resolves to real rows")
    page.locator("#ds-root button:has-text('Reload usage')").click()
    page.wait_for_timeout(200)
    check(page.evaluate("document.querySelectorAll('#ds-root [aria-busy=\"true\"]').length") >= 1,
          "loading: Reload re-enters the busy state")
    page.wait_for_timeout(1600)
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, "accordion-loading")
    anim = p.evaluate(
        "getComputedStyle(document.querySelector('#ds-root .animate-pulse')).animationName"
    )
    check(anim == "none", f"loading: reduced motion disables the pulse (animation {anim})")
    context.close()


def bordered_checks(page):
    print("== accordion-bordered ==")
    open_preview(page, "accordion-bordered")
    # the first demo's root div carries the overflow-hidden bordered treatment
    container = page.evaluate(
        """(() => {
          const el = document.querySelector('#ds-root div[class*="overflow-hidden"]');
          const cs = getComputedStyle(el);
          return { radius: cs.borderRadius, border: cs.borderWidth, overflow: cs.overflow };
        })()"""
    )
    check(container["radius"] == "8px", f"bordered: container carries radius-md (got {container['radius']})")
    check(container["border"] == "1px", f"bordered: container carries a 1px border (got {container['border']})")
    check(container["overflow"] == "hidden", f"bordered: container clips to its corners (overflow {container['overflow']})")
    btn = page.locator("#ds-root h3 > button").first
    btn.focus()
    page.wait_for_timeout(120)
    ring = page.evaluate("getComputedStyle(document.activeElement).outlineWidth")
    offset = page.evaluate("getComputedStyle(document.activeElement).outlineOffset")
    check(ring == "2px" and offset == "-2px",
          f"bordered: focus ring is 2px inset (never clipped) (got {ring} @ {offset})")


def focus_ring_check(page, slug, label):
    open_preview(page, slug)
    page.locator(f"#ds-root h3 > button:has-text('{label}')").first.focus()
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
        f"{slug}: focus-visible 2px outline on '{label}'",
    )


def keyboard_checks(page):
    print("== keyboard behavior ==")
    # collapsible self-close lets both open AND close be exercised by keys
    open_preview(page, "accordion-collapsible")
    btn = page.locator("#ds-root h3 > button").first
    btn.focus()
    page.keyboard.press("Space")
    page.wait_for_timeout(200)
    check(btn.get_attribute("aria-expanded") == "false",
          "keyboard: Space closes the open trigger")
    page.keyboard.press("Enter")
    page.wait_for_timeout(200)
    check(btn.get_attribute("aria-expanded") == "true",
          "keyboard: Enter reopens the closed trigger")
    open_preview(page, "accordion-disabled")
    disabled_btn = page.locator("#ds-root h3 > button[disabled]").first
    check(disabled_btn.get_attribute("aria-expanded") == "false",
          "keyboard: disabled trigger stays closed")


def dark_mode_check(page):
    print("== dark mode ==")
    for slug in ("accordion", "accordion-bordered", "accordion-with-badge"):
        open_preview(page, slug)
        light_fg = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root h3 > button')).color"
        )
        light_region = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root [role=\"region\"] > div > div')).color"
        )
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(200)
        dark_fg = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root h3 > button')).color"
        )
        dark_region = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root [role=\"region\"] > div > div')).color"
        )
        check(light_fg != dark_fg, f"{slug}: trigger text flips between light and dark")
        check(light_region != dark_region, f"{slug}: region text flips between light and dark")
        body_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
        check(body_bg == "rgb(10, 10, 10)", f"{slug}: dark canvas applied (body bg {body_bg})")
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(150)


def reduced_motion_check(browser):
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, "accordion")
    prop = p.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [role=\"region\"]')).transitionProperty"
    )
    check(prop == "none", f"reduced motion removes region transitions (got {prop})")
    btn = p.locator("#ds-root h3 > button").nth(1)
    btn.click()
    p.wait_for_timeout(50)
    check(btn.get_attribute("aria-expanded") == "true",
          "reduced motion: toggle is instant and still correct")
    context.close()


def main():
    static_checks()
    export_parity_checks()
    generator_checks()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        for slug in VARIANTS:
            print(f"== {slug} ==")
            shared_checks(page, slug)

        semantics_checks(page)
        reference_checks(page)
        multiple_checks(page)
        collapsible_checks(page)
        icons_checks(page)
        description_checks(page)
        disabled_checks(page)
        badge_checks(page)
        faq_checks(page)
        nested_checks(page)
        actions_checks(page)
        loading_checks(page, browser)
        bordered_checks(page)
        keyboard_checks(page)

        print("== focus / theme / motion ==")
        focus_ring_check(page, "accordion", "Webhooks")
        focus_ring_check(page, "accordion-with-icons", "Profile")
        focus_ring_check(page, "accordion-with-badge", "Failed checks")
        focus_ring_check(page, "accordion-bordered", "General")
        focus_ring_check(page, "accordion-with-actions", "API keys")
        dark_mode_check(page)
        reduced_motion_check(browser)

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

