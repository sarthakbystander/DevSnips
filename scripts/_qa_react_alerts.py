#!/usr/bin/env python3
"""Playwright QA for the React Alerts previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders, zero console errors, zero horizontal overflow at
    375/768/1280
  - static: exactly the 5 required files per variant, metadata schema, no
    `any` in code.tsx, no hardcoded hex, no component-specific CSS files
  - shared core: every derived code.tsx is identical to the reference except
    its header doc comment; TSX/JSX export sets + per-component prop
    signatures match
  - generator: `_gen_react_alerts.py --check` reports no drift;
    `scripts/validate.py` passes
  - roles: default/info/success → role=status, warning/destructive →
    role=alert, role={null} renders no role attribute
  - title/description association: aria-labelledby/aria-describedby point at
    the rendered title/description; omitted when the region is absent
  - icons: every svg inside an alert is inside an aria-hidden slot
  - alert-dismissible: click + keyboard dismissal, onDismiss fires, close
    button accessible names, focus moves to the next operable element,
    controlled mode follows parent state
  - alert-with-action: real buttons fire handlers
  - alert-with-link: real anchors navigate (hash updates)
  - alert-live: save mounts a role=status alert, failure mounts a role=alert
    alert, one live alert at a time, no nested live regions
  - focus-visible 2px outline on close + action controls
  - dark mode flips computed alert surface + text colors
  - reduced motion kills transitions
  - long unbroken content does not overflow its alert

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_alerts.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/Alerts/"

VARIANTS = [
    "alert", "alert-info", "alert-success", "alert-warning",
    "alert-destructive", "alert-with-icon", "alert-with-action",
    "alert-with-link", "alert-dismissible", "alert-compact",
    "alert-rich", "alert-live",
]

EXPORTS = ["Alert", "AlertIcon", "AlertTitle", "AlertDescription", "AlertAction", "AlertClose"]

# JS snippet evaluating to the array of alert ROOT elements in the showcase:
# ids start with "alert-" but the title/description ids derived from them end
# with -title / -description, so those are filtered out.
ALERT_ROOTS = (
    "Array.from(document.querySelectorAll('#ds-root [id^=\"alert-\"]'))"
    ".filter(el => !/-(title|description)$/.test(el.id))"
)

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
        folder = ROOT / "React/Components/Alerts" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["README.md", "code.jsx", "code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exactly the 5 required files",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(
            meta["technology"] == "react"
            and meta["type"] == "component"
            and meta["category"] == "Alerts"
            and meta["styling"] == "Tailwind CSS"
            and meta["languages"] == ["JSX", "TSX"]
            and meta["framework"] == "React"
            and meta["language"] == "TSX"
            and meta["component"] == "alert"
            and meta["family"] == "alerts",
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
    css = list((ROOT / "React/Components/Alerts").rglob("*.css"))
    check(css == [], "no component-specific CSS files in the family")
    # derived-code.tsx parity: identical shared core except the header comment
    reference = (ROOT / "React/Components/Alerts/alert/code.tsx").read_text()
    ref_body = re.sub(r"/\*\*.*?\*/", "", reference, count=1, flags=re.S)
    for slug in VARIANTS[1:]:
        tsx = (ROOT / "React/Components/Alerts" / slug / "code.tsx").read_text()
        body = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S)
        check(body == ref_body, f"{slug}: code.tsx shares the reference core")


def _props_of(src, name):
    """Destructured prop names of `function <name>({ ... })` (the balanced
    brace block right after the opening paren)."""
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
        folder = ROOT / "React/Components/Alerts" / slug
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        te = sorted(set(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx)))
        m = re.search(r"export \{ ([^}]*) \};", jsx)
        je = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(te == je == sorted(EXPORTS), f"{slug}: TSX/JSX named-export parity")
        check("export default Alert;" in jsx, f"{slug}: JSX default export = Alert")
        for name in EXPORTS:
            tp = _props_of(tsx, name)
            jp = _props_of(jsx, name)
            check(tp is not None and tp == jp, f"{slug}: {name} prop-signature parity")


def generator_checks():
    print("== generator + repo validation ==")
    r = subprocess.run(
        [sys.executable, "_gen_react_alerts.py", "--check"],
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
    rendered = page.evaluate("document.querySelectorAll('#ds-root *').length")
    check(rendered > 0, f"{slug}: showcase renders content")
    for w in (375, 768, 1280):
        check(overflow(page, w) == 0, f"{slug}: no horizontal overflow at {w}px")
    check(errs == [], f"{slug}: zero console errors")


def role_checks(page):
    print("== roles ==")
    expectations = {
        "alert": "status",
        "alert-info": "status",
        "alert-success": "status",
        "alert-warning": "alert",
        "alert-destructive": "alert",
    }
    for slug, role in expectations.items():
        open_preview(page, slug)
        first = page.evaluate("document.querySelector('#ds-root [role]')?.getAttribute('role')")
        check(first == role, f"{slug}: first alert has role={role}")
    # reference variant: the static demo opts out with role={null}
    open_preview(page, "alert")
    roles = page.evaluate(ALERT_ROOTS + ".map(a => a.getAttribute('role'))")
    check(roles == ["status", None], f"alert: role={{null}} demo renders no role attribute (got {roles})")
    # no variant blanket-promotes everything to role=alert
    open_preview(page, "alert-info")
    n_alert = page.evaluate("document.querySelectorAll('#ds-root [role=\"alert\"]').length")
    check(n_alert == 0, "alert-info: informational message is not role=alert")


def association_checks(page):
    print("== title/description association ==")
    open_preview(page, "alert")
    info = page.evaluate(
        """(() => {
          const a = document.querySelector('#ds-root [role="status"]');
          const title = document.getElementById(a.getAttribute('aria-labelledby'));
          const desc = document.getElementById(a.getAttribute('aria-describedby'));
          return {
            labelledby: a.getAttribute('aria-labelledby'),
            describedby: a.getAttribute('aria-describedby'),
            titleText: title ? title.textContent.trim() : null,
            descText: desc ? desc.textContent.trim().slice(0, 30) : null,
            titleTag: title ? title.tagName : null,
          };
        })()"""
    )
    check(bool(info["labelledby"]) and info["titleText"] == "Usage resets on the 1st",
          "alert: aria-labelledby points at the rendered title")
    check(bool(info["describedby"]) and info["descText"].startswith("Your plan"),
          "alert: aria-describedby points at the rendered description")
    check(info["titleTag"] == "P", "alert: title is a <p> (stays out of the page outline)")
    # description-only alert: labelledby omitted entirely, not pointing at nothing
    second = page.evaluate(
        """(() => {
          const a = %s[1];
          return { labelledby: a.getAttribute('aria-labelledby'), describedby: a.getAttribute('aria-describedby') };
        })()""" % ALERT_ROOTS
    )
    check(second["labelledby"] is None and bool(second["describedby"]),
          "alert: aria-labelledby omitted when no title is rendered")


def icon_checks(page):
    print("== decorative icons ==")
    for slug in ("alert-info", "alert-success", "alert-warning", "alert-destructive", "alert-with-icon", "alert-rich"):
        open_preview(page, slug)
        bad = page.evaluate(
            """(() => {
              const svgs = Array.from(document.querySelectorAll('#ds-root [id^="alert-"] svg'));
              return svgs.filter(s => s.closest('[aria-hidden="true"]') === null).length;
            })()"""
        )
        check(bad == 0, f"{slug}: every svg inside an alert is aria-hidden")


def dismissible_checks(page):
    print("== alert-dismissible ==")
    open_preview(page, "alert-dismissible")
    # close buttons carry accessible names
    names = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root button[aria-label]')).map(b => b.getAttribute('aria-label'))"
    )
    check("Dismiss alert" in names, "alert-dismissible: default close label 'Dismiss alert'")
    check("Dismiss deployment message" in names, "alert-dismissible: custom closeLabel applied")
    # uncontrolled: click close → alert unmounts + onDismiss fires
    before = page.evaluate("document.querySelectorAll('#ds-root [role=\"status\"]').length")
    page.click("#ds-root button[aria-label='Dismiss alert']")
    page.wait_for_timeout(250)
    after = page.evaluate("document.querySelectorAll('#ds-root [role=\"status\"]').length")
    check(before == 2 and after == 1, "alert-dismissible: uncontrolled alert unmounts on click")
    log = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root p')).find(p => p.textContent.includes('onDismiss'))?.textContent"
    )
    check(bool(log) and "fired" in log, "alert-dismissible: onDismiss fires (uncontrolled)")
    # keyboard: reset, Tab to close, Enter → dismissed, focus moves to Reset demo
    page.click("#ds-root button:has-text('Reset demo')")
    page.wait_for_timeout(250)
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"status\"]').length") == 2,
          "alert-dismissible: Reset demo remounts the alert")
    page.evaluate("document.querySelector('#ds-root button[aria-label=\"Dismiss alert\"]').focus()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(250)
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"status\"]').length") == 1,
          "alert-dismissible: close button dismisses with Enter")
    focused = page.evaluate("document.activeElement?.textContent?.trim() || ''")
    check("Reset demo" in focused, "alert-dismissible: focus moves to the next operable element after dismissal")
    # controlled: close fires onDismiss, parent sets open=false, Show again appears
    page.click("#ds-root button[aria-label='Dismiss deployment message']")
    page.wait_for_timeout(250)
    event_log = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root p')).find(p => p.textContent.includes('open=false'))?.textContent"
    )
    check(bool(event_log), "alert-dismissible: controlled onDismiss → parent set open=false")
    show_again = page.locator("#ds-root button:has-text('Show again')")
    check(show_again.count() == 1, "alert-dismissible: controlled alert hides, Show again appears")
    show_again.click()
    page.wait_for_timeout(250)
    # the uncontrolled demo alert was dismissed earlier in the flow, so only
    # the controlled alert returns.
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"status\"]').length") == 1,
          "alert-dismissible: controlled alert returns when parent sets open=true")


def action_checks(page):
    print("== alert-with-action ==")
    open_preview(page, "alert-with-action")
    buttons = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root [id^=\"alert-\"] button')).map(b => b.textContent.trim())"
    )
    check(buttons == ["Upgrade plan", "Compare plans", "Update billing", "Retry charge"],
          "alert-with-action: actions are real <button> elements")
    page.click("#ds-root button:has-text('Upgrade plan')")
    page.wait_for_timeout(150)
    log = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("Upgrade plan" in log, "alert-with-action: action button fires its handler")
    page.click("#ds-root button:has-text('Retry charge')")
    page.wait_for_timeout(150)
    log = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("Retry charge" in log, "alert-with-action: second alert's action fires independently")


def link_checks(page):
    print("== alert-with-link ==")
    open_preview(page, "alert-with-link")
    anchors = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root [id^=\"alert-\"] a[href]')).map(a => a.getAttribute('href'))"
    )
    check(len(anchors) == 4 and all(h.startswith("#/") for h in anchors),
          "alert-with-link: links are real <a href> anchors")
    page.click("#ds-root a[href='#/changelog']")
    page.wait_for_timeout(200)
    check(page.evaluate("window.location.hash") == "#/changelog",
          "alert-with-link: anchor navigates (hash updates)")
    note = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root p')).find(p => p.textContent.includes('current hash')).textContent"
    )
    check("#/changelog" in note, "alert-with-link: live hash note updates")
    underlined = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root a[href=\"#/changelog\"]')).textDecorationLine.includes('underline')"
    )
    check(underlined, "alert-with-link: links are underlined (not color alone)")


def live_checks(page):
    print("== alert-live ==")
    open_preview(page, "alert-live")
    check(page.evaluate("document.querySelectorAll('#ds-root [role]').length") == 0,
          "alert-live: no live alert pre-rendered before the event")
    page.click("#ds-root button:has-text('Save settings')")
    page.wait_for_timeout(900)
    status = page.evaluate(
        """(() => {
          const a = document.querySelector('#ds-root [role="status"]');
          return a ? a.textContent : null;
        })()"""
    )
    check(bool(status) and "Settings saved" in status,
          "alert-live: save mounts a role=status (polite) alert")
    page.click("#ds-root button:has-text('Simulate failure')")
    page.wait_for_timeout(900)
    alert_text = page.evaluate(
        "document.querySelector('#ds-root [role=\"alert\"]')?.textContent || null"
    )
    check(bool(alert_text) and "could not be saved" in alert_text,
          "alert-live: failure mounts a role=alert (assertive) alert")
    count = page.evaluate("document.querySelectorAll('#ds-root [role=\"status\"], #ds-root [role=\"alert\"]').length")
    check(count == 1, "alert-live: one live alert at a time (no stacked duplicates)")
    nested = page.evaluate(
        """(() => {
          const a = document.querySelector('#ds-root [role="alert"]');
          let p = a.parentElement;
          while (p && p.id !== 'ds-root') {
            if (p.getAttribute('aria-live')) return true;
            p = p.parentElement;
          }
          return false;
        })()"""
    )
    check(not nested, "alert-live: alert is not nested inside another live region")
    static_role = page.evaluate(
        "(() => { const all = %s; return all[all.length - 1].getAttribute('role'); })()" % ALERT_ROOTS
    )
    check(static_role is None, "alert-live: static contrast demo has no role")


def nested_interactive_checks(page):
    print("== no nested interactive elements ==")
    for slug in ("alert-with-action", "alert-with-link", "alert-dismissible", "alert-rich", "alert-compact"):
        open_preview(page, slug)
        bad = page.evaluate(
            """(() => {
              const controls = Array.from(document.querySelectorAll('#ds-root [id^="alert-"] button, #ds-root [id^="alert-"] a'));
              return controls.filter(c => c.querySelector('button, a') !== null).length;
            })()"""
        )
        check(bad == 0, f"{slug}: no interactive element nested inside another")


def rich_checks(page):
    print("== alert-rich ==")
    open_preview(page, "alert-rich")
    page.click("#ds-root button:has-text('Update now')")
    page.wait_for_timeout(150)
    log = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("Update now" in log, "alert-rich: primary action fires")
    close_buttons = page.evaluate("document.querySelectorAll('#ds-root button[aria-label=\"Dismiss alert\"]').length")
    check(close_buttons == 2, "alert-rich: both rich alerts are dismissible")
    page.click("#ds-root [role='alert'] button[aria-label='Dismiss alert']")
    page.wait_for_timeout(250)
    log = page.evaluate("document.querySelector('#ds-root [aria-live=polite]').textContent")
    check("incident" in log, "alert-rich: dismiss fires onDismiss")
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"alert\"]').length") == 0,
          "alert-rich: dismissed alert unmounts")


def long_content_checks(page):
    print("== long content ==")
    open_preview(page, "alert-info", width=375)
    ok = page.evaluate(
        """(() => {
          const a = document.querySelector('#ds-root [role="status"]');
          const desc = a.querySelector('[id$="-description"]');
          return desc.scrollWidth <= desc.clientWidth + 1 && a.scrollWidth <= a.clientWidth + 1;
        })()"""
    )
    check(ok, "alert-info: long unbroken string does not overflow its alert at 375px")


def focus_ring_check(page, slug, selector):
    open_preview(page, slug)
    page.locator(selector).first.focus()
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


def dark_mode_check(page, slug="alert-warning"):
    open_preview(page, slug)
    light_bg = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [role]')).backgroundColor"
    )
    light_fg = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [role]')).color"
    )
    page.click("#ds-theme-toggle")
    page.wait_for_timeout(200)
    dark_bg = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [role]')).backgroundColor"
    )
    dark_fg = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [role]')).color"
    )
    check(light_bg != dark_bg, f"{slug}: alert surface flips between light and dark themes")
    check(light_fg != dark_fg, f"{slug}: alert text flips between light and dark themes")
    body_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    check(body_bg == "rgb(10, 10, 10)", f"{slug}: dark canvas applied (body bg {body_bg})")


def reduced_motion_check(browser, slug="alert-dismissible"):
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, slug)
    prop = p.evaluate(
        "getComputedStyle(document.querySelector('#ds-root button[aria-label=\"Dismiss alert\"]')).transitionProperty"
    )
    check(prop == "none", f"{slug}: reduced motion disables transitions (got transition-property: {prop})")
    context.close()


def compact_checks(page):
    print("== alert-compact ==")
    open_preview(page, "alert-compact")
    roles = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root [role]')).map(a => a.getAttribute('role'))"
    )
    check(roles == ["status", "status", "alert", "status"],
          f"alert-compact: density keeps the semantic roles (got {roles})")
    padding = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root [role]')).paddingTop"
    )
    check(padding == "8px", f"alert-compact: compact padding applied (got {padding})")
    close_size = page.evaluate(
        "document.querySelector('#ds-root button[aria-label=\"Dismiss alert\"]').getBoundingClientRect().width"
    )
    check(close_size == 28, f"alert-compact: compact close target is 28px (got {close_size})")


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

        role_checks(page)
        association_checks(page)
        icon_checks(page)
        dismissible_checks(page)
        action_checks(page)
        link_checks(page)
        live_checks(page)
        nested_interactive_checks(page)
        rich_checks(page)
        compact_checks(page)
        long_content_checks(page)

        print("== focus / theme / motion ==")
        focus_ring_check(page, "alert-dismissible", "#ds-root button[aria-label='Dismiss alert']")
        focus_ring_check(page, "alert-with-action", "#ds-root button:has-text('Upgrade plan')")
        focus_ring_check(page, "alert-with-link", "#ds-root a[href='#/changelog']")
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
