#!/usr/bin/env python3
"""QA harness for the DevSnips React Sidebar family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields + family values
  - no `any` in code.tsx, no `<div onClick`, no inline `style=` attribute, no
    hex color literals
  - disclosure/dialog-pattern assertions: semantic aside + nav landmarks,
    real anchors, aria-current / aria-expanded / aria-controls wiring,
    role="dialog" + aria-modal on the mobile drawer only
  - anti-AI design rules: no gradients, no glassmorphism/backdrop-blur, no
    emoji, no neon/purple vocabulary in code.tsx or preview.html
  - TSX/JSX export parity (19 exports) + prop-name parity per export
  - shared-core equality across all 12 variants (header-comment-neutralized)
  - generator --check (no drift) + scripts/validate.py gates

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors
  - 0 horizontal overflow at 375 / 768 / 1280 (drawer closed AND open)
  - one visible navigation landmark per mode; real anchors; real buttons;
    no nested interactive elements
  - desktop expanded mode (256px) / collapsed mode (64px) via trigger + rail
  - collapsed rail: sr-only labels (accessible names intact), measured
    fixed-position tooltips on hover AND keyboard focus, badge dots
  - mobile drawer: dialog semantics, overlay, focus moves in on open, Tab
    trap wraps, Escape closes + restores focus to the trigger, outside
    pointer closes, close button closes, body scroll locks + releases,
    link activation closes
  - active navigation: exactly one aria-current, follows hash navigation,
    active child auto-expands + indicates the parent
  - nested navigation: aria-expanded toggling, chevron rotation, keyboard
    operation, disabled rows non-interactive
  - search: real filtering, parent preservation, empty state, clear + Escape
  - collapsible groups: independent state + external coordination
  - badges / user area / footer actions / dashboard composition
  - focus-visible 2px outline; light/dark token flip; reduced-motion guard

Run: python3 scripts/_qa_react_sidebar.py
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIDEBAR = ROOT / "React/Components/Sidebar"
SLUGS = [
    "sidebar",
    "sidebar-collapsed",
    "sidebar-mobile",
    "sidebar-with-groups",
    "sidebar-with-nested-navigation",
    "sidebar-with-active-state",
    "sidebar-with-badges",
    "sidebar-with-user",
    "sidebar-with-footer-actions",
    "sidebar-with-search",
    "sidebar-collapsible-groups",
    "sidebar-dashboard",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = [
    "SidebarProvider", "Sidebar", "SidebarHeader", "SidebarContent",
    "SidebarFooter", "SidebarGroup", "SidebarGroupLabel", "SidebarMenu",
    "SidebarMenuItem", "SidebarMenuButton", "SidebarMenuCollapsible",
    "SidebarMenuSub", "SidebarMenuSubItem", "SidebarMenuSubButton",
    "SidebarTrigger", "SidebarRail", "SidebarSearch", "SidebarNav",
    "useSidebar",
]
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]", flags=re.UNICODE
)
BANNED_RE = re.compile(
    r"gradient|glassmorphism|backdrop-blur|backdrop-filter|neon|purple|violet|fuchsia",
    flags=re.IGNORECASE,
)

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


def prop_signature(src: str, name: str) -> list[str]:
    """Destructured prop names of `export function <name>(...)` (TSX) or the
    plain `function <name>(...)` (JSX, exports hoisted to a trailing block),
    handling multi-line parameter lists (defaults + types stripped)."""
    m = re.search(rf"export\s+function\s+{name}\s*\(", src) \
        or re.search(rf"(?<![\w$])function\s+{name}\s*\(", src)
    if not m:
        return []
    start = src.index("(", m.end() - 1)
    depth, end = 0, None
    for i in range(start, len(src)):
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    block = src[start : end + 1 if end else len(src)]
    if not block.lstrip().lstrip("(").lstrip().startswith("{"):
        # Identifier-param component (e.g. `function X(props)`) — collect the
        # destructured props from `const { ... } = props` statements instead.
        body_end = src.find("\nexport function ", m.end())
        body = src[m.end() : body_end if body_end > -1 else len(src)]
        props = set()
        for dm in re.finditer(r"const \{([^}]*)\} = props", body):
            for raw in dm.group(1).split(","):
                seg = raw.strip()
                if not seg or seg.startswith("..."):
                    continue
                seg = re.sub(r"\s*=.*$", "", seg)
                seg = re.sub(r"\?:.*$", "", seg)
                seg = re.sub(r":.*$", "", seg)
                seg = seg.strip().strip('"')
                if seg:
                    props.add(seg)
        return sorted(props)
    props = []
    for raw in block.split(","):
        seg = raw.strip().strip("(){}").strip()
        if not seg or seg.startswith("..."):
            continue
        seg = re.sub(r"\s*=.*$", "", seg)
        seg = re.sub(r"\?:.*$", "", seg)
        seg = re.sub(r":.*$", "", seg)
        seg = seg.strip().strip('"')
        if seg:
            props.append(seg)
    return sorted(set(props))


def static_checks():
    print("static checks")
    cores = {}
    for slug in SLUGS:
        folder = SIDEBAR / slug
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
        check(meta["category"] == "Sidebar", f"{slug}: category Sidebar")
        check(meta["component"] == "sidebar", f"{slug}: component sidebar")
        check(meta["family"] == "sidebar", f"{slug}: family sidebar")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")
        check(meta["responsive"] is True, f"{slug}: responsive true")
        check(meta["darkMode"] is True, f"{slug}: darkMode true")
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        preview = (folder / "preview.html").read_text()
        readme = (folder / "README.md").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        check("style=" not in tsx, f"{slug}: no inline style attribute")
        check(re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx) == [],
              f"{slug}: no hex color literals")
        # Comment-stripped view for pattern assertions (header docs may
        # legitimately discuss the patterns being avoided).
        tsx_code = re.sub(r"/\*.*?\*/", "", tsx, flags=re.S)
        check("<aside" in tsx and "<nav" in tsx and "aria-label" in tsx,
              f"{slug}: semantic aside + nav landmarks")
        check("<a" in tsx and "href" in tsx, f"{slug}: real anchors")
        check("<button" in tsx, f"{slug}: real buttons")
        check('role="dialog"' in tsx and 'aria-modal="true"' in tsx,
              f"{slug}: mobile drawer dialog semantics")
        check("aria-current" in tsx, f"{slug}: aria-current wiring")
        check("aria-expanded" in tsx, f"{slug}: aria-expanded wiring")
        check("aria-controls" in tsx, f"{slug}: aria-controls wiring")
        check("aria-disabled" in tsx, f"{slug}: aria-disabled pattern")
        check("focus-visible:outline-2" in tsx, f"{slug}: focus-visible ring")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("var(--ds-color-surface)" in tsx, f"{slug}: surface token")
        check("var(--ds-color-focus-ring)" in tsx, f"{slug}: focus-ring token")
        check("var(--ds-color-overlay)" in tsx, f"{slug}: overlay token")
        check("var(--ds-color-border)" in tsx, f"{slug}: border token")
        check("var(--ds-color-muted-foreground)" in tsx, f"{slug}: muted-foreground token")
        check("var(--ds-color-surface-active)" in tsx, f"{slug}: surface-active token")
        check("var(--ds-radius-sm)" in tsx, f"{slug}: radius token")
        check(not BANNED_RE.search(tsx_code), f"{slug}: no banned aesthetics in code.tsx")
        # Scan the preview's markup/showcase only: the shared preview-shell
        # <style> block is infrastructure (the token block legitimately
        # contains rgba() values), and negated claims are documentation.
        preview_body = re.sub(r"<style>.*?</style>", "", preview, flags=re.S)
        preview_body = re.sub(r"no\s+(gradients?|glassmorphism|backdrop[- ]blur),?", "", preview_body, flags=re.I)
        check(not BANNED_RE.search(preview_body), f"{slug}: no banned aesthetics in preview.html")
        check(not EMOJI_RE.search(tsx), f"{slug}: no emoji in code.tsx")
        check(not EMOJI_RE.search(preview), f"{slug}: no emoji in preview.html")
        check("https://unpkg.com/react@18/umd/react.development.js" in preview,
              f"{slug}: preview loads React 18 UMD")
        check("https://unpkg.com/react-dom@18/umd/react-dom.development.js" in preview,
              f"{slug}: preview loads ReactDOM UMD")
        check("https://cdn.tailwindcss.com" in preview, f"{slug}: preview loads Tailwind CDN")
        check("--ds-color-surface" in preview, f"{slug}: preview token block")
        check('data-theme="light"' in preview and "ds-react-theme" in preview,
              f"{slug}: preview no-flash theme init")
        for section in ["## Installation", "## Usage", "## Props", "## Compound Components",
                        "## Navigation Data", "## Responsive Behavior", "## Accessibility",
                        "## Keyboard Interaction", "## Active Navigation",
                        "## Controlled and Uncontrolled State",
                        "## Styling", "## Design Tokens", "## Notes and Limitations"]:
            check(section in readme, f"{slug}: README has '{section}'")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        check(tsx_exports == sorted(CORE_EXPORTS), f"{slug}: exports all 19 primitives")
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        for name in CORE_EXPORTS:
            tp, jp = prop_signature(tsx, name), prop_signature(jsx, name)
            check(tp == jp, f"{slug}: {name} prop parity {tp} vs {jp}")
        cores[slug] = neutralize_core(tsx)
    ref = cores["sidebar"]
    for slug in SLUGS[1:]:
        check(cores[slug] == ref, f"{slug}: shared core identical to reference")

    # Generator drift gate.
    gen = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_sidebar.py"), "--check"],
        capture_output=True, text=True, cwd=ROOT,
    )
    check(gen.returncode == 0, f"generator --check clean ({gen.stdout.strip()} {gen.stderr.strip()[:200]})")

    # Repository validator gate.
    val = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate.py")],
        capture_output=True, text=True, cwd=ROOT,
    )
    check(val.returncode == 0, f"scripts/validate.py passes ({val.stdout.strip()[-160:]})")


def open_preview(page, slug, width=1280, hash_route=None):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.set_viewport_size({"width": width, "height": 900})
    uri = (SIDEBAR / slug / "preview.html").as_uri()
    if hash_route:
        uri += hash_route
    page.goto(uri)
    page.wait_for_selector("#ds-root aside", state="attached", timeout=20000)
    page.wait_for_timeout(400)
    return errors


def no_overflow(page, slug, state):
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(200)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"{slug}: no horizontal overflow ({state}) @ {w} (got {overflow})")


def aside(page):
    return page.locator("#ds-root aside").first


def open_drawer(page, slug):
    """Open the mobile drawer at 375px via the trigger; return dialog."""
    page.set_viewport_size({"width": 375, "height": 900})
    page.wait_for_timeout(250)
    trigger = page.get_by_role("button", name="Toggle sidebar")
    check(trigger.count() == 1, f"{slug}: exactly one sidebar trigger")
    check(trigger.get_attribute("aria-expanded") == "false",
          f"{slug}: trigger aria-expanded=false with drawer closed")
    check(trigger.get_attribute("aria-controls") is not None,
          f"{slug}: trigger has aria-controls")
    trigger.click()
    page.wait_for_timeout(350)
    dialog = page.get_by_role("dialog")
    check(dialog.count() == 1, f"{slug}: drawer renders role=dialog")
    check(dialog.is_visible(), f"{slug}: drawer visible at 375px")
    check(dialog.get_attribute("aria-modal") == "true", f"{slug}: drawer aria-modal=true")
    check(bool(dialog.get_attribute("aria-label")), f"{slug}: drawer has an accessible name")
    check(trigger.get_attribute("aria-expanded") == "true",
          f"{slug}: trigger aria-expanded=true with drawer open")
    overlay = page.locator("[data-ds-sidebar-overlay]")
    check(overlay.count() == 1, f"{slug}: overlay rendered")
    # Overlay covers the viewport area beside the drawer.
    cover = page.evaluate(
        "() => { const o = document.querySelector('[data-ds-sidebar-overlay]').getBoundingClientRect();"
        " return o.width >= window.innerWidth && o.height >= window.innerHeight; }")
    check(cover, f"{slug}: overlay covers the viewport")
    check(page.evaluate("document.body.style.overflow") == "hidden",
          f"{slug}: body scroll locked while drawer open")
    # Drawer fits the viewport.
    box = dialog.bounding_box()
    check(box["width"] <= 375 - 40, f"{slug}: drawer fits viewport with room ({box['width']}px)")
    check(box["x"] == 0 and box["y"] == 0, f"{slug}: drawer pinned to the left edge")
    return dialog


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
            check(aside(page).count() == 1, f"{slug}: desktop landmark rendered")
            nav = aside(page).locator("nav").first
            check(bool(nav.get_attribute("aria-label")), f"{slug}: nav landmark labelled")
            check(nav.locator("a[href]").count() > 0, f"{slug}: navigation links are real anchors")
            check(nav.locator("button").count() > 0, f"{slug}: navigation has real buttons")
            nested = page.evaluate(
                "document.querySelectorAll('#ds-root aside a button, #ds-root aside button a, "
                "#ds-root aside a a, #ds-root aside button button').length")
            check(nested == 0, f"{slug}: no nested interactive elements")
            check(page.locator("#ds-root [role='menu'], #ds-root [role='menuitem']").count() == 0,
                  f"{slug}: no menu/menuitem roles on navigation")
            # Exactly one visible navigation landmark at desktop width.
            check(aside(page).is_visible(), f"{slug}: desktop landmark visible @1280")
            width = aside(page).evaluate("el => el.getBoundingClientRect().width")
            expected = 64 if slug == "sidebar-collapsed" else 256
            check(width == expected, f"{slug}: expanded width {expected}px (got {width})")
            no_overflow(page, slug, "drawer closed")
            # Drawer flow at 375.
            dialog = open_drawer(page, slug)
            # Focus moved into the drawer.
            check(page.evaluate("document.querySelector('#ds-root [role=dialog]').contains(document.activeElement)"),
                  f"{slug}: focus moved into the drawer on open")
            no_overflow(page, slug, "drawer open")
            page.close()

        # ---------------- sidebar (reference) ------------------------------
        print("== sidebar (reference) ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar")
        nav = aside(page).locator("nav").first
        check(nav.get_attribute("aria-label") == "Main", "sidebar: landmark label 'Main'")
        current = aside(page).locator('[aria-current="page"]')
        check(current.count() == 1, "sidebar: exactly one aria-current item")
        check(current.first.inner_text().strip() == "Overview", "sidebar: current item is Overview")
        # Active follows hash navigation.
        aside(page).get_by_role("link", name="Analytics", exact=True).click()
        page.wait_for_timeout(250)
        current = aside(page).locator('[aria-current="page"]')
        check(current.count() == 1 and current.first.inner_text().strip() == "Analytics",
              "sidebar: aria-current follows navigation")
        # Active treatment: surface + inset indicator (not color alone).
        treatment = current.first.evaluate(
            "el => { const s = getComputedStyle(el); return { bg: s.backgroundColor, shadow: s.boxShadow, weight: s.fontWeight }; }")
        check(treatment["bg"] != "rgba(0, 0, 0, 0)", "sidebar: active row has a surface fill")
        check("inset" in treatment["shadow"], "sidebar: active row has the inset indicator bar")
        check(int(treatment["weight"]) >= 500, "sidebar: active row is medium weight")
        # Collapsible disclosure: aria-expanded + aria-controls + chevron.
        trigger = aside(page).get_by_role("button", name="Projects", exact=True)
        check(trigger.count() == 1, "sidebar: collapsible parent is a real button")
        expanded_before = trigger.get_attribute("aria-expanded")
        controls = trigger.get_attribute("aria-controls")
        check(expanded_before in ("true", "false"), "sidebar: parent has aria-expanded")
        check(bool(controls), "sidebar: parent has aria-controls")
        if expanded_before == "false":
            trigger.click()
            page.wait_for_timeout(200)
        check(trigger.get_attribute("aria-expanded") == "true", "sidebar: parent expands")
        sub = page.locator(f'[id="{controls}"]')
        check(sub.count() == 1 and sub.is_visible(), "sidebar: aria-controls points at the rendered nested list")
        chevron_rotate = trigger.locator("svg").last.evaluate(
            "el => getComputedStyle(el).transform")
        check(chevron_rotate not in ("none", ""), "sidebar: chevron rotates when open")
        trigger.click()
        page.wait_for_timeout(200)
        check(trigger.get_attribute("aria-expanded") == "false", "sidebar: parent collapses")
        check(page.locator(f'[id="{controls}"]').count() == 0, "sidebar: nested list unmounts when closed")
        # Keyboard: Enter/Space toggle the parent.
        trigger.press("Enter")
        page.wait_for_timeout(150)
        check(trigger.get_attribute("aria-expanded") == "true", "sidebar: Enter toggles the parent")
        trigger.press("Space")
        page.wait_for_timeout(150)
        check(trigger.get_attribute("aria-expanded") == "false", "sidebar: Space toggles the parent")
        # Collapse via trigger; expand via rail.
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(300)
        check(aside(page).evaluate("el => el.getBoundingClientRect().width") == 64,
              "sidebar: trigger collapses to the 64px rail")
        page.get_by_role("button", name="Expand sidebar").click()
        page.wait_for_timeout(300)
        check(aside(page).evaluate("el => el.getBoundingClientRect().width") == 256,
              "sidebar: rail expands back to 256px")
        page.close()

        # ---------------- sidebar-collapsed --------------------------------
        print("== sidebar-collapsed ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-collapsed")
        check(aside(page).evaluate("el => el.getBoundingClientRect().width") == 64,
              "sidebar-collapsed: loads as the 64px rail")
        # Labels stay in the accessibility tree: the links keep their names.
        names = aside(page).evaluate(
            "el => Array.from(el.querySelectorAll('a[href]')).map(a => ({ name: a.textContent.trim(), labeled: (a.getAttribute('aria-label') || a.textContent.trim()).length > 0 }))")
        check(len(names) > 0 and all(n["labeled"] for n in names),
              "sidebar-collapsed: every icon row keeps an accessible name")
        # Visible label text is sr-only (visually hidden).
        hidden_labels = aside(page).evaluate(
            "el => { const spans = Array.from(el.querySelectorAll('a .sr-only, button .sr-only'));"
            " return spans.filter(s => s.getBoundingClientRect().width <= 1 || getComputedStyle(s).clip !== 'auto').length; }")
        check(hidden_labels > 0, "sidebar-collapsed: labels render sr-only in the rail")
        # Measured tooltip on hover: fixed position, visible, correct text.
        analytics = aside(page).get_by_role("link", name="Analytics", exact=True)
        analytics.hover()
        page.wait_for_timeout(300)
        tip = page.evaluate(
            "() => { const tips = Array.from(document.querySelectorAll('#ds-root aside a span[aria-hidden=true]'))"
            ".filter(s => s.style.visibility === 'visible');"
            " return tips.map(t => ({ text: t.textContent, pos: getComputedStyle(t).position })); }")
        check(len(tip) == 1 and tip[0]["text"] == "Analytics",
              f"sidebar-collapsed: hover shows the measured tooltip (got {tip})")
        check(tip and tip[0]["pos"] == "fixed", "sidebar-collapsed: tooltip is fixed-position (escapes the scroll container)")
        # Tooltip on keyboard focus too.
        page.evaluate("document.activeElement.blur && document.activeElement.blur()")
        analytics.focus()
        page.wait_for_timeout(300)
        tip_focused = page.evaluate(
            "() => Array.from(document.querySelectorAll('#ds-root aside a span[aria-hidden=true]'))"
            ".filter(s => s.style.visibility === 'visible').map(s => s.textContent)")
        check(tip_focused == ["Analytics"], "sidebar-collapsed: keyboard focus shows the tooltip")
        analytics.evaluate("el => el.blur()")
        page.wait_for_timeout(300)
        tip_after_blur = page.evaluate(
            "() => Array.from(document.querySelectorAll('#ds-root aside a span[aria-hidden=true]'))"
            ".filter(s => s.style.visibility === 'visible').length")
        check(tip_after_blur == 0, "sidebar-collapsed: blur hides the tooltip")
        # Badge collapses to a dot; count stays sr-only.
        inbox = aside(page).get_by_role("link", name=re.compile("Inbox"))
        check("4" in inbox.inner_text(), "sidebar-collapsed: badge count stays in the accessibility tree")
        dot = inbox.evaluate(
            "el => Array.from(el.querySelectorAll('span[aria-hidden=true]'))"
            ".some(s => { const r = s.getBoundingClientRect(); const b = getComputedStyle(s).borderRadius;"
            " return r.width <= 8 && r.width > 0 && parseFloat(b) >= r.width / 2; })")
        check(dot, "sidebar-collapsed: badge renders as a dot in the rail")
        # Active state remains obvious in the rail.
        current = aside(page).locator('[aria-current="page"]')
        check(current.count() == 1, "sidebar-collapsed: aria-current survives in the rail")
        shadow = current.first.evaluate("el => getComputedStyle(el).boxShadow")
        check("inset" in shadow, "sidebar-collapsed: active indicator bar survives in the rail")
        # Activating the collapsed Projects icon expands + opens in one step.
        projects = aside(page).get_by_role("button", name="Projects", exact=True)
        projects.click()
        page.wait_for_timeout(350)
        check(aside(page).evaluate("el => el.getBoundingClientRect().width") == 256,
              "sidebar-collapsed: activating a parent icon expands the sidebar")
        check(aside(page).get_by_role("link", name="Backlog", exact=True).is_visible(),
              "sidebar-collapsed: the group is open after the one-step expansion")
        # Controlled state readout tracks the rail.
        check(page.get_by_text("expanded", exact=True).count() > 0,
              "sidebar-collapsed: controlled state readout updated")
        # The demo's Collapse button drives the same controlled state.
        page.get_by_role("button", name="Collapse", exact=True).click()
        page.wait_for_timeout(300)
        check(aside(page).evaluate("el => el.getBoundingClientRect().width") == 64,
              "sidebar-collapsed: external Collapse button collapses the rail")
        page.close()

        # ---------------- sidebar-mobile -----------------------------------
        print("== sidebar-mobile ==")
        page = browser.new_page(viewport={"width": 375, "height": 900})
        open_preview(page, "sidebar-mobile", width=375)
        dialog = open_drawer(page, "sidebar-mobile")
        # Event log recorded the open.
        check(page.get_by_text(re.compile("Drawer opened")).count() > 0,
              "sidebar-mobile: controlled log records the open")
        # Tab trap: from the first focusable, Shift+Tab wraps to the last
        # (the built-in close button); Tab from the last wraps to the first.
        dialog.locator("a[href]").first.focus()
        page.keyboard.press("Shift+Tab")
        page.wait_for_timeout(150)
        check(page.evaluate("document.activeElement.getAttribute('aria-label')") == "Close navigation",
              "sidebar-mobile: Shift+Tab from the first link wraps to the close button")
        page.keyboard.press("Tab")
        page.wait_for_timeout(150)
        check(page.evaluate("document.querySelector('#ds-root [role=dialog]').contains(document.activeElement)"),
              "sidebar-mobile: Tab from the close button wraps into the drawer")
        # Escape closes + restores focus to the trigger.
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        check(page.get_by_role("dialog").count() == 0, "sidebar-mobile: Escape closes the drawer")
        check(page.evaluate("document.activeElement.getAttribute('aria-label')") == "Toggle sidebar",
              "sidebar-mobile: focus returns to the trigger after Escape")
        check(page.evaluate("document.body.style.overflow") != "hidden",
              "sidebar-mobile: scroll lock released on close")
        check(page.get_by_text(re.compile("Drawer closed")).count() > 0,
              "sidebar-mobile: controlled log records the close")
        # Reopen; the close button closes.
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(300)
        page.get_by_role("button", name="Close navigation").click()
        page.wait_for_timeout(300)
        check(page.get_by_role("dialog").count() == 0, "sidebar-mobile: close button closes the drawer")
        check(page.evaluate("document.activeElement.getAttribute('aria-label')") == "Toggle sidebar",
              "sidebar-mobile: focus returns to the trigger after the close button")
        # Reopen; outside pointer (overlay) closes.
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(300)
        page.locator("[data-ds-sidebar-overlay]").dispatch_event("pointerdown")
        page.wait_for_timeout(300)
        check(page.get_by_role("dialog").count() == 0, "sidebar-mobile: overlay pointer closes the drawer")
        # Reopen; activating a navigation link closes the drawer.
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(300)
        page.get_by_role("dialog").get_by_role("link", name="Analytics", exact=True).click()
        page.wait_for_timeout(300)
        check(page.get_by_role("dialog").count() == 0, "sidebar-mobile: link activation closes the drawer")
        check(page.evaluate("window.location.hash") == "#/analytics",
              "sidebar-mobile: navigation proceeded after drawer close")
        page.close()

        # ---------------- sidebar-with-groups ------------------------------
        print("== sidebar-with-groups ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-groups")
        for label in ["Workspace", "Admin"]:
            check(aside(page).get_by_text(label, exact=True).count() > 0,
                  f"sidebar-with-groups: '{label}' group label rendered")
        # Group labels become sr-only in the rail but stay in the tree.
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(300)
        label_state = aside(page).evaluate(
            "el => { const p = Array.from(el.querySelectorAll('p')).find(p => p.textContent.trim() === 'Workspace');"
            " if (!p) return null; const r = p.getBoundingClientRect();"
            " return { cls: p.className, w: r.width, h: r.height }; }")
        check(label_state is not None and "sr-only" in label_state["cls"],
              "sidebar-with-groups: group labels become sr-only in the rail")
        page.close()

        # ---------------- sidebar-with-nested-navigation -------------------
        print("== sidebar-with-nested-navigation ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-nested-navigation")
        # Projects starts open (defaultOpen) with its nested list.
        backlog = aside(page).get_by_role("link", name="Backlog", exact=True)
        check(backlog.count() == 1 and backlog.is_visible(), "sidebar-with-nested: defaultOpen renders the nested list")
        # Third level renders under Components.
        buttons3 = aside(page).get_by_role("link", name="Buttons", exact=True)
        check(buttons3.count() == 1 and buttons3.is_visible(), "sidebar-with-nested: third level renders")
        indent = buttons3.evaluate("el => el.getBoundingClientRect().left") - backlog.evaluate("el => el.getBoundingClientRect().left")
        check(indent > 8, f"sidebar-with-nested: third level indents further ({indent}px)")
        # Active child indicates the parent (weight, no fill).
        backlog.click()
        page.wait_for_timeout(250)
        check(backlog.get_attribute("aria-current") == "page", "sidebar-with-nested: child takes aria-current")
        parent = aside(page).get_by_role("button", name="Projects", exact=True)
        check(parent.get_attribute("aria-current") is None, "sidebar-with-nested: parent has no aria-current")
        pstyle = parent.evaluate("el => ({ w: getComputedStyle(el).fontWeight, bg: getComputedStyle(el).backgroundColor })")
        check(int(pstyle["w"]) >= 500 and pstyle["bg"] == "rgba(0, 0, 0, 0)",
              "sidebar-with-nested: parent indication = weight only, no fill")
        # Disabled nested row is a non-interactive span.
        disabled = aside(page).locator('span[aria-disabled="true"]', has_text="Releases (soon)")
        check(disabled.count() == 1, "sidebar-with-nested: disabled row is an aria-disabled span")
        check(disabled.evaluate("el => el.tabIndex") == -1, "sidebar-with-nested: disabled row is not focusable")
        check(disabled.get_by_role("link").count() == 0, "sidebar-with-nested: disabled row exposes no link")
        page.close()

        # ---------------- sidebar-with-active-state ------------------------
        print("== sidebar-with-active-state ==")
        # Direct load on a child route: the parent auto-expands.
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-active-state", hash_route="#/projects/backlog")
        child = aside(page).get_by_role("link", name="Backlog", exact=True)
        check(child.count() == 1 and child.is_visible(),
              "sidebar-with-active: active child visible on direct load (parent auto-expanded)")
        check(child.get_attribute("aria-current") == "page",
              "sidebar-with-active: child route carries aria-current on load")
        parent = aside(page).get_by_role("button", name="Projects", exact=True)
        check(parent.get_attribute("aria-expanded") == "true",
              "sidebar-with-active: parent auto-expanded for the active child")
        pstyle = parent.evaluate("el => ({ w: getComputedStyle(el).fontWeight, bg: getComputedStyle(el).backgroundColor })")
        check(int(pstyle["w"]) >= 500 and pstyle["bg"] == "rgba(0, 0, 0, 0)",
              "sidebar-with-active: parent indication = weight only")
        # Manual override: collapse the parent of the active child; it stays.
        parent.click()
        page.wait_for_timeout(250)
        check(parent.get_attribute("aria-expanded") == "false",
              "sidebar-with-active: manual collapse of the active parent sticks")
        # Navigating re-auto-expands on a new active child.
        aside(page).get_by_role("button", name="Projects", exact=True).click()
        page.wait_for_timeout(200)
        aside(page).get_by_role("link", name="Releases", exact=True).click()
        page.wait_for_timeout(250)
        current = aside(page).locator('[aria-current="page"]')
        check(current.count() == 1 and current.first.inner_text().strip() == "Releases",
              "sidebar-with-active: aria-current moves between children")
        page.close()

        # ---------------- sidebar-with-badges ------------------------------
        print("== sidebar-with-badges ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-badges")
        inbox = aside(page).get_by_role("link", name=re.compile("Inbox"))
        check("4" in inbox.inner_text(), "sidebar-with-badges: inbox count chip rendered")
        chip = inbox.evaluate(
            "el => { const chip = Array.from(el.querySelectorAll('span')).find(s => s.textContent.trim() === '4');"
            " if (!chip) return null; const r = chip.getBoundingClientRect();"
            " const row = el.getBoundingClientRect();"
            " return { h: r.height, within: r.right <= row.right + 1, v: getComputedStyle(chip).fontVariantNumeric || getComputedStyle(chip).getPropertyValue('font-variant-numeric') }; }")
        check(chip is not None and chip["within"], "sidebar-with-badges: badge stays inside the row")
        check(chip is not None and chip["h"] <= 22, "sidebar-with-badges: badge keeps row geometry")
        beta = aside(page).get_by_role("link", name=re.compile("Labs"))
        check("Beta" in beta.inner_text(), "sidebar-with-badges: status chip rendered")
        # Live update: Mark all read clears the count.
        mark = aside(page).get_by_role("button", name="Mark all read", exact=True)
        check(mark.count() == 1, "sidebar-with-badges: action row is a real button")
        mark.click()
        page.wait_for_timeout(250)
        check("4" not in aside(page).get_by_role("link", name=re.compile("Inbox")).inner_text(),
              "sidebar-with-badges: Mark all read clears the badge")
        check(page.get_by_text(re.compile("Unread inbox items")).first.inner_text().strip().endswith("0"),
              "sidebar-with-badges: status readout reflects the cleared count")
        exhausted = aside(page).locator('span[aria-disabled="true"]', has_text="Mark all read")
        check(exhausted.count() == 1, "sidebar-with-badges: exhausted action becomes an aria-disabled span")
        check(aside(page).get_by_role("button", name="Mark all read", exact=True).count() == 0,
              "sidebar-with-badges: exhausted action is no longer a button")
        page.close()

        # ---------------- sidebar-with-user --------------------------------
        print("== sidebar-with-user ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-user")
        footer = aside(page).locator("div.mt-auto").first
        check(footer.get_by_text("Ava Khan", exact=True).count() == 1, "sidebar-with-user: user name rendered")
        check(footer.get_by_text("ava@forge.dev", exact=True).count() == 1, "sidebar-with-user: user email rendered")
        check(footer.get_by_role("link", name="Account", exact=True).count() == 1,
              "sidebar-with-user: account link rendered")
        signout = footer.get_by_role("button", name="Sign out", exact=True)
        check(signout.count() == 1, "sidebar-with-user: sign out is a real button")
        signout.click()
        page.wait_for_timeout(250)
        check(page.get_by_text(re.compile("Sign out requested")).count() > 0,
              "sidebar-with-user: sign out action produces feedback")
        # Rail adaptation: name/email become sr-only, avatar remains.
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(300)
        user_state = aside(page).evaluate(
            "el => { const t = Array.from(el.querySelectorAll('span')).find(s => s.textContent.includes('Ava Khan'));"
            " const avatar = Array.from(el.querySelectorAll('span[aria-hidden=true]')).find(s => s.textContent.trim() === 'AK');"
            " return { nameSrOnly: t ? t.className.includes('sr-only') : false, avatarVisible: avatar ? avatar.getBoundingClientRect().width > 0 : false }; }")
        check(user_state["nameSrOnly"], "sidebar-with-user: identity text becomes sr-only in the rail")
        check(user_state["avatarVisible"], "sidebar-with-user: avatar remains visible in the rail")
        page.close()

        # ---------------- sidebar-with-footer-actions ----------------------
        print("== sidebar-with-footer-actions ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-footer-actions")
        footer = aside(page).locator("div.mt-auto").first
        settings = footer.get_by_role("link", name="Settings", exact=True)
        check(settings.count() == 1, "sidebar-with-footer-actions: Settings is a real link")
        signout = footer.get_by_role("button", name="Sign out", exact=True)
        check(signout.count() == 1, "sidebar-with-footer-actions: Sign out is a real button")
        signout.press("Enter")
        page.wait_for_timeout(250)
        check(page.get_by_text(re.compile("Signed out at")).count() > 0,
              "sidebar-with-footer-actions: Enter activates sign out with feedback")
        check(page.get_by_role("button", name="Sign back in").count() == 1,
              "sidebar-with-footer-actions: recovery action rendered")
        page.get_by_role("button", name="Sign back in").click()
        page.wait_for_timeout(250)
        check(page.get_by_text("Workspace session active.").count() == 1,
              "sidebar-with-footer-actions: sign back in restores the session")
        page.close()

        # ---------------- sidebar-with-search ------------------------------
        print("== sidebar-with-search ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-with-search")
        field = aside(page).get_by_label("Search navigation")
        check(field.count() == 1, "sidebar-with-search: labelled search field rendered")
        check(field.get_attribute("type") == "search", "sidebar-with-search: input type=search")
        # Parent match keeps the subtree.
        field.fill("settings")
        page.wait_for_timeout(300)
        check(aside(page).get_by_role("button", name="Settings", exact=True).count() == 1,
              "sidebar-with-search: parent match keeps the parent")
        check(aside(page).get_by_role("link", name="Billing", exact=True).is_visible(),
              "sidebar-with-search: parent match keeps its subtree visible")
        check(aside(page).get_by_role("link", name="Overview", exact=True).count() == 0,
              "sidebar-with-search: non-matching rows are filtered out")
        # Child match keeps the parent chain (visible + expanded).
        field.fill("billing")
        page.wait_for_timeout(300)
        settings_parent = aside(page).get_by_role("button", name="Settings", exact=True)
        check(settings_parent.count() == 1, "sidebar-with-search: child match keeps the parent")
        check(settings_parent.get_attribute("aria-expanded") == "true",
              "sidebar-with-search: parent of a match is expanded")
        check(aside(page).get_by_role("link", name="Billing", exact=True).is_visible(),
              "sidebar-with-search: matching child visible")
        check(aside(page).get_by_role("link", name="Members", exact=True).count() == 0,
              "sidebar-with-search: non-matching siblings filtered")
        # Empty state.
        field.fill("zzz")
        page.wait_for_timeout(300)
        status = aside(page).locator("[role='status']")
        check(status.count() == 1, "sidebar-with-search: empty state is a status region")
        check("zzz" in status.inner_text(), "sidebar-with-search: empty state names the query")
        # Clear via the clear button.
        clear = aside(page).get_by_role("button", name="Clear search")
        check(clear.count() == 1, "sidebar-with-search: clear button rendered while query non-empty")
        clear.click()
        page.wait_for_timeout(300)
        check(field.input_value() == "", "sidebar-with-search: clear button resets the query")
        check(aside(page).get_by_role("link", name="Overview", exact=True).count() == 1,
              "sidebar-with-search: clearing restores the full tree")
        # Escape clears (and does not close anything).
        field.fill("analytics")
        page.wait_for_timeout(250)
        field.press("Escape")
        page.wait_for_timeout(250)
        check(field.input_value() == "", "sidebar-with-search: Escape clears the query")
        # Case-insensitivity.
        field.fill("BILLING")
        page.wait_for_timeout(300)
        check(aside(page).get_by_role("link", name="Billing", exact=True).is_visible(),
              "sidebar-with-search: matching is case-insensitive")
        page.close()

        # ---------------- sidebar-collapsible-groups -----------------------
        print("== sidebar-collapsible-groups ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-collapsible-groups")
        projects = aside(page).get_by_role("button", name="Projects", exact=True)
        components = aside(page).get_by_role("button", name="Components", exact=True)
        admin = aside(page).get_by_role("button", name="Admin", exact=True)
        check(projects.get_attribute("aria-expanded") == "true", "sidebar-collapsible-groups: Projects starts open")
        check(components.get_attribute("aria-expanded") == "false", "sidebar-collapsible-groups: Components starts closed")
        check(admin.get_attribute("aria-expanded") == "false", "sidebar-collapsible-groups: Admin starts closed")
        # Independent toggling.
        components.click()
        page.wait_for_timeout(200)
        check(components.get_attribute("aria-expanded") == "true", "sidebar-collapsible-groups: Components toggles independently")
        check(projects.get_attribute("aria-expanded") == "true", "sidebar-collapsible-groups: Projects unaffected")
        # External coordination.
        page.get_by_role("button", name="Collapse all", exact=True).click()
        page.wait_for_timeout(250)
        for name, btn in [("Projects", projects), ("Components", components), ("Admin", admin)]:
            check(btn.get_attribute("aria-expanded") == "false",
                  f"sidebar-collapsible-groups: Collapse all closes {name}")
        check(aside(page).get_by_role("link", name="Backlog", exact=True).count() == 0,
              "sidebar-collapsible-groups: collapsed groups unmount their rows")
        page.get_by_role("button", name="Expand all", exact=True).click()
        page.wait_for_timeout(250)
        for name, btn in [("Projects", projects), ("Components", components), ("Admin", admin)]:
            check(btn.get_attribute("aria-expanded") == "true",
                  f"sidebar-collapsible-groups: Expand all opens {name}")
        check(page.get_by_text(re.compile("Open groups")).first.inner_text().strip().endswith("projects, components, admin"),
              "sidebar-collapsible-groups: status readout reflects the map")
        page.close()

        # ---------------- sidebar-dashboard --------------------------------
        print("== sidebar-dashboard ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-dashboard")
        check(aside(page).locator("nav").first.get_attribute("aria-label") == "Console",
              "sidebar-dashboard: landmark label 'Console'")
        check(aside(page).get_by_text("Platform", exact=True).count() == 1,
              "sidebar-dashboard: Platform group rendered")
        check(aside(page).get_by_text("Workspace", exact=True).count() == 1,
              "sidebar-dashboard: Workspace group rendered")
        check("4" in aside(page).get_by_role("link", name=re.compile("Inbox")).inner_text(),
              "sidebar-dashboard: inbox badge rendered")
        check("Beta" in aside(page).get_by_role("link", name=re.compile("Integrations")).inner_text(),
              "sidebar-dashboard: beta badge rendered")
        check(aside(page).get_by_text("Ava Khan", exact=True).count() == 1,
              "sidebar-dashboard: user area rendered")
        current = aside(page).locator('[aria-current="page"]')
        check(current.count() == 1 and current.first.inner_text().strip() == "Overview",
              "sidebar-dashboard: exactly one current item (Overview)")
        # Nested active flow.
        aside(page).get_by_role("button", name="Projects", exact=True).click()
        page.wait_for_timeout(200)
        aside(page).get_by_role("link", name="Active sprint", exact=True).click()
        page.wait_for_timeout(250)
        current = aside(page).locator('[aria-current="page"]')
        check(current.count() == 1 and current.first.inner_text().strip() == "Active sprint",
              "sidebar-dashboard: nested route takes aria-current")
        # Full drawer flow at 375.
        dialog = open_drawer(page, "sidebar-dashboard")
        check(dialog.get_by_role("link", name=re.compile("Inbox")).count() == 1,
              "sidebar-dashboard: drawer exposes the same navigation")
        check(dialog.get_by_text("Ava Khan", exact=True).count() == 1,
              "sidebar-dashboard: drawer exposes the user area")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        check(page.get_by_role("dialog").count() == 0, "sidebar-dashboard: drawer closes")
        page.close()

        # ---------------- keyboard + a11y sweeps ---------------------------
        print("== keyboard / a11y sweeps ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar")
        # Tab order: brand link is the first stop inside the landmark.
        brand = aside(page).get_by_role("link", name="Forge home")
        brand.focus()
        page.keyboard.press("Tab")
        page.wait_for_timeout(100)
        first_row = page.evaluate("document.activeElement.textContent.trim()")
        check(first_row == "Overview", f"sidebar: Tab from brand reaches the first row (got {first_row!r})")
        # Shift+Tab returns.
        page.keyboard.press("Shift+Tab")
        page.wait_for_timeout(100)
        check(page.evaluate("document.activeElement.getAttribute('aria-label')") == "Forge home",
              "sidebar: Shift+Tab returns to the brand")
        # focus-visible ring on a row.
        row = aside(page).get_by_role("link", name="Analytics", exact=True)
        row.focus()
        page.wait_for_timeout(150)
        outline = row.evaluate("el => getComputedStyle(el).outlineWidth")
        check(outline == "2px", f"sidebar: focus-visible 2px ring (got {outline})")
        # Drawer focus trap first-stop: focus enters the drawer and wraps.
        dialog = open_drawer(page, "sidebar")
        active_in = page.evaluate("document.activeElement && document.activeElement.tagName")
        check(active_in in ("A", "BUTTON", "INPUT"), "sidebar: drawer's first focus is a real control")
        page.close()

        # ---------------- dark mode + reduced motion -----------------------
        print("== dark mode / reduced motion ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "sidebar-dashboard")
        light = page.evaluate(
            "() => ({ body: getComputedStyle(document.body).backgroundColor,"
            " surface: getComputedStyle(document.querySelector('#ds-root aside')).backgroundColor })")
        page.locator("#ds-theme-toggle").click()
        page.wait_for_timeout(300)
        dark = page.evaluate(
            "() => ({ body: getComputedStyle(document.body).backgroundColor,"
            " surface: getComputedStyle(document.querySelector('#ds-root aside')).backgroundColor })")
        check(light["body"] != dark["body"], "dark mode: body background flips")
        check(light["surface"] != dark["surface"], "dark mode: sidebar surface flips")
        # Dark drawer token flip.
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(250)
        page.get_by_role("button", name="Toggle sidebar").click()
        page.wait_for_timeout(350)
        drawer_surface = page.evaluate(
            "() => getComputedStyle(document.querySelector('#ds-root [role=dialog]')).backgroundColor")
        check(drawer_surface == dark["surface"], "dark mode: drawer surface matches the dark token")
        overlay_alpha = page.evaluate(
            "() => getComputedStyle(document.querySelector('[data-ds-sidebar-overlay]')).backgroundColor")
        check("rgba" in overlay_alpha, "dark mode: overlay renders the overlay token")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        page.close()
        # Reduced motion.
        page = browser.new_page(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        open_preview(page, "sidebar-collapsed")
        row = aside(page).get_by_role("link", name="Analytics", exact=True)
        transition = row.evaluate("el => getComputedStyle(el).transitionProperty")
        check(transition in ("none", ""), f"reduced motion: row transitions disabled (got {transition!r})")
        aside_transition = aside(page).evaluate("el => getComputedStyle(el).transitionProperty")
        check(aside_transition in ("none", ""), f"reduced motion: width transition disabled (got {aside_transition!r})")
        page.close()

        # ---------------- 375 / 768 / 1280 spot assertions -----------------
        print("== viewport spot checks ==")
        page = browser.new_page(viewport={"width": 768, "height": 900})
        open_preview(page, "sidebar-dashboard", width=768)
        check(aside(page).is_visible(), "responsive: desktop column visible at 768 (md breakpoint)")
        trigger_expanded_state = page.get_by_role("button", name="Toggle sidebar").get_attribute("aria-expanded")
        check(trigger_expanded_state == "true", "responsive: trigger reflects desktop mode at 768")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(300)
        check(not aside(page).is_visible(), "responsive: desktop column hidden at 375")
        check(page.get_by_role("button", name="Toggle sidebar").get_attribute("aria-expanded") == "false",
              "responsive: trigger reflects mobile mode at 375")
        page.close()

        browser.close()

    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    static_checks()
    browser_checks()
