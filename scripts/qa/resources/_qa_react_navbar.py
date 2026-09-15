#!/usr/bin/env python3
"""QA harness for the DevSnips React Navbar family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields + family values
  - no `any` in code.tsx, no `<div onClick`, no inline `style=`, no hex colors
  - disclosure-pattern assertions: semantic <nav>, real anchors, aria-expanded /
    aria-controls / aria-haspopup / aria-current wiring, NO role="menu"/menuitem
  - anti-AI design rules: no gradients, no glassmorphism/backdrop-blur, no
    emoji, no neon/purple vocabulary in code.tsx or preview.html
  - TSX/JSX export parity (15 primitives) + prop-name parity per export
  - shared-core equality across all 10 variants (header-comment-neutralized)

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors
  - 0 horizontal overflow at 375 / 768 / 1280 (mobile menu closed AND open)
  - nav landmark present; navigation links are real anchors; no nested
    interactive elements; no menu/menuitem roles
  - toggle: real button, aria-expanded updates, aria-controls points at the
    actual mobile region, >= 36px touch target
  - mobile menu: Escape closes + focus restored to the toggle, outside
    pointer closes, link activation closes, no layout shift on open
  - focus-visible 2px outline; dark-mode token flip (body + nav surface);
    reduced-motion transition-duration 0s
  - per-variant interaction checks (dropdown keyboard model + flip
    containment, mega-menu groups, sticky pinning, transparent surface,
    side-panel overlay/scroll-lock/focus, user-menu actions)

Run: python3 scripts/_qa_react_navbar.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAVBAR = ROOT / "React/Components/Navbar"
SLUGS = [
    "navbar",
    "navbar-with-actions",
    "navbar-centered",
    "navbar-with-dropdown",
    "navbar-with-mobile-menu",
    "navbar-with-mega-menu",
    "navbar-sticky",
    "navbar-transparent",
    "navbar-with-sidebar-mobile",
    "navbar-with-user-menu",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = [
    "Navbar", "NavbarBrand", "NavbarContent", "NavbarSection", "NavbarItem",
    "NavbarLink", "NavbarAction", "NavbarToggle", "NavbarMobile",
    "NavbarMobileContent", "NavbarDropdown", "NavbarDropdownTrigger",
    "NavbarDropdownContent", "NavbarDropdownItem", "NavbarDivider",
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
        # destructured props from `const { ... } = props` statements in the
        # function body instead.
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
        folder = NAVBAR / slug
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
        check(meta["category"] == "Navbar", f"{slug}: category Navbar")
        check(meta["component"] == "navbar", f"{slug}: component navbar")
        check(meta["family"] == "navbar", f"{slug}: family navbar")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")
        check(meta["responsive"] is True, f"{slug}: responsive true")
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
        check("<nav" in tsx and "aria-label" in tsx, f"{slug}: semantic nav landmark")
        check("<a" in tsx and "href" in tsx, f"{slug}: real anchors")
        check('role="menu"' not in tsx_code and "menuitem" not in tsx_code,
              f"{slug}: no ARIA menu pattern on navigation")
        check("aria-current" in tsx, f"{slug}: aria-current wiring")
        check("aria-expanded" in tsx, f"{slug}: aria-expanded wiring")
        check("aria-controls" in tsx, f"{slug}: aria-controls wiring")
        check("aria-haspopup" in tsx, f"{slug}: aria-haspopup wiring")
        check("aria-disabled" in tsx, f"{slug}: aria-disabled pattern")
        check("focus-visible:outline-2" in tsx, f"{slug}: focus-visible ring")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("var(--ds-color-surface)" in tsx, f"{slug}: surface token")
        check("var(--ds-color-focus-ring)" in tsx, f"{slug}: focus-ring token")
        check("var(--ds-color-overlay)" in tsx, f"{slug}: overlay token (side panel)")
        check(not BANNED_RE.search(tsx_code), f"{slug}: no banned aesthetics in code.tsx")
        # Scan the preview's markup/showcase only: the shared preview-shell
        # <style> block is infrastructure, and negated claims ("no gradients")
        # are documentation of the constraint, not violations.
        preview_body = re.sub(r"<style>.*?</style>", "", preview, flags=re.S)
        preview_body = re.sub(r"no\s+(gradients?|glassmorphism|backdrop[- ]blur),?", "", preview_body, flags=re.I)
        check(not BANNED_RE.search(preview_body), f"{slug}: no banned aesthetics in preview.html")
        check(not EMOJI_RE.search(tsx), f"{slug}: no emoji in code.tsx")
        check(not EMOJI_RE.search(preview), f"{slug}: no emoji in preview.html")
        for section in ["## Installation", "## Usage", "## Props", "## Compound Components",
                        "## Responsive Behavior", "## Keyboard Interaction", "## Accessibility",
                        "## Active Navigation", "## Controlled and Uncontrolled State",
                        "## Styling", "## Design Tokens", "## Notes and Limitations"]:
            check(section in readme, f"{slug}: README has '{section}'")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        check(tsx_exports == sorted(CORE_EXPORTS), f"{slug}: exports all 15 primitives")
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        for name in CORE_EXPORTS:
            tp, jp = prop_signature(tsx, name), prop_signature(jsx, name)
            check(tp == jp, f"{slug}: {name} prop parity {tp} vs {jp}")
        cores[slug] = neutralize_core(tsx)
    ref = cores["navbar"]
    for slug in SLUGS[1:]:
        check(cores[slug] == ref, f"{slug}: shared core identical to reference")


def open_preview(page, slug, width=1280):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.set_viewport_size({"width": width, "height": 900})
    page.goto((NAVBAR / slug / "preview.html").as_uri())
    page.wait_for_selector("#ds-root nav", timeout=15000)
    page.wait_for_timeout(400)
    return errors


def no_overflow(page, slug, state):
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(150)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"{slug}: no horizontal overflow ({state}) @ {w} (got {overflow})")


def open_mobile(page, slug):
    """Open the mobile menu at 375px and return (toggle, region)."""
    page.set_viewport_size({"width": 375, "height": 900})
    page.wait_for_timeout(200)
    toggle = page.get_by_role("button", name=re.compile("navigation menu")).first
    check(toggle.count() == 1, f"{slug}: mobile toggle present at 375")
    controls = toggle.get_attribute("aria-controls")
    check(bool(controls), f"{slug}: toggle has aria-controls")
    check(toggle.get_attribute("aria-expanded") == "false", f"{slug}: aria-expanded=false when closed")
    scroll_before = page.evaluate("document.documentElement.scrollHeight")
    toggle.click()
    page.wait_for_timeout(250)
    check(toggle.get_attribute("aria-expanded") == "true", f"{slug}: aria-expanded=true when open")
    # ids come from React useId and contain colons — use attribute selectors
    region = page.locator(f'[id="{controls}"]')
    check(region.count() == 1, f"{slug}: aria-controls points at the rendered mobile region")
    check(region.is_visible(), f"{slug}: mobile region visible when open")
    scroll_after = page.evaluate("document.documentElement.scrollHeight")
    check(scroll_before == scroll_after,
          f"{slug}: no layout shift opening the mobile menu ({scroll_before} -> {scroll_after})")
    links = region.locator("a[href]")
    check(links.count() > 0, f"{slug}: mobile region exposes navigation anchors")
    return toggle, region


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
            nav = page.locator("#ds-root nav").first
            check(nav.count() == 1, f"{slug}: nav landmark rendered")
            check(bool(nav.get_attribute("aria-label")), f"{slug}: nav landmark labelled")
            check(nav.locator("a[href]").count() > 0, f"{slug}: navigation links are real anchors")
            nested = page.evaluate(
                "document.querySelectorAll('#ds-root nav a button, #ds-root nav button a, "
                "#ds-root nav a a, #ds-root nav button button').length")
            check(nested == 0, f"{slug}: no nested interactive elements")
            check(page.locator('#ds-root [role="menu"], #ds-root [role="menuitem"]').count() == 0,
                  f"{slug}: no menu/menuitem roles rendered")
            no_overflow(page, slug, "mobile closed")
            # mobile menu open/close + overflow open
            toggle, region = open_mobile(page, slug)
            box = toggle.bounding_box()
            check(box["width"] >= 36 and box["height"] >= 36, f"{slug}: toggle >= 36px touch target")
            no_overflow(page, slug, "mobile open")
            # back to 375 (the toggle is hidden at/above the breakpoint),
            # then Escape closes and focus stays on / returns to the toggle
            page.set_viewport_size({"width": 375, "height": 900})
            page.wait_for_timeout(150)
            toggle.press("Escape")
            page.wait_for_timeout(200)
            check(toggle.get_attribute("aria-expanded") == "false", f"{slug}: Escape closes the mobile menu")
            active_label = page.evaluate("document.activeElement && document.activeElement.getAttribute('aria-label')")
            check(active_label == "Open navigation menu",
                  f"{slug}: focus on the toggle after Escape (got {active_label!r})")
            page.close()

        # ---------------- navbar (reference) ------------------------------
        print("== navbar ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar")
        nav = page.locator("#ds-root nav").first
        check(nav.get_attribute("aria-label") == "Main", "navbar: landmark label 'Main'")
        current = nav.locator('[aria-current="page"]')
        check(current.count() == 1, "navbar: exactly one aria-current item")
        check(current.first.inner_text().strip() == "Overview", "navbar: current item is Overview")
        # active follows the hash route
        nav.get_by_role("link", name="Components", exact=True).first.click()
        page.wait_for_timeout(200)
        current = nav.locator('[aria-current="page"]')
        check(current.count() == 1 and current.first.inner_text().strip() == "Components",
              "navbar: aria-current follows navigation")
        # disabled is a non-interactive span, not a link
        disabled = nav.get_by_text("Enterprise", exact=True)
        check(disabled.evaluate("el => el.tagName") == "SPAN", "navbar: disabled item is a span")
        check(disabled.get_attribute("aria-disabled") == "true", "navbar: disabled item aria-disabled")
        check(disabled.evaluate("el => el.closest('a') === null"), "navbar: disabled item not wrapped in a link")
        # external link
        gh = nav.locator('a[target="_blank"]').first
        check(gh.inner_text().strip().find("GitHub") > -1, "navbar: external GitHub link")
        check(gh.get_attribute("target") == "_blank", "navbar: external target=_blank")
        check(gh.get_attribute("rel") == "noreferrer", "navbar: external rel=noreferrer")
        # focus-visible ring on keyboard focus
        nav.get_by_role("link", name="Forge").first.focus()
        page.keyboard.press("Tab")
        page.wait_for_timeout(120)
        outline = page.evaluate("getComputedStyle(document.activeElement).outlineWidth")
        check(outline == "2px", f"navbar: focus-visible 2px outline (got {outline})")
        # mobile: link activation closes the menu and moves the route
        toggle, region = open_mobile(page, "navbar")
        region.get_by_role("link", name="Templates", exact=True).click()
        page.wait_for_timeout(250)
        check(toggle.get_attribute("aria-expanded") == "false", "navbar: link activation closes the mobile menu")
        check(page.evaluate("window.location.hash") == "#/templates", "navbar: mobile link navigates (hash)")
        # outside pointer closes
        toggle.click()
        page.wait_for_timeout(200)
        page.mouse.click(190, 700)
        page.wait_for_timeout(200)
        check(toggle.get_attribute("aria-expanded") == "false", "navbar: outside pointer closes the mobile menu")
        page.close()

        # ---------------- navbar-with-actions -----------------------------
        print("== navbar-with-actions ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-with-actions")
        nav = page.locator("#ds-root nav").first
        nav.get_by_role("button", name="Sign in").first.click()
        page.wait_for_timeout(150)
        check(nav.get_by_text("Signed in as ada@forge.dev").count() == 1, "actions: sign-in state appears")
        check(nav.get_by_role("button", name="Sign out").count() == 1, "actions: sign-out action appears")
        nav.get_by_role("button", name="Sign out").click()
        page.wait_for_timeout(150)
        check(nav.get_by_role("button", name="Sign in").count() == 1, "actions: sign-out restores sign-in")
        gs = nav.get_by_role("link", name="Get started").first
        check(gs.evaluate("el => el.tagName") == "A", "actions: Get started is an anchor")
        page.close()

        # ---------------- navbar-centered ---------------------------------
        print("== navbar-centered ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-centered")
        centered = page.evaluate("""() => {
          const nav = document.querySelector('#ds-root nav');
          const brand = nav.querySelector('a[href="#/overview"]');
          const n = nav.getBoundingClientRect(), b = brand.getBoundingClientRect();
          return { navCenter: n.left + n.width / 2, brandCenter: b.left + b.width / 2 };
        }""")
        check(abs(centered["navCenter"] - centered["brandCenter"]) <= 2,
              f"centered: brand centered at 1280 (delta {abs(centered['navCenter'] - centered['brandCenter']):.1f}px)")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(200)
        brand_left = page.evaluate("document.querySelector('#ds-root nav a[href=\\\"#/overview\\\"]').getBoundingClientRect().left")
        check(brand_left <= 20, f"centered: brand back in flow at 375 (left {brand_left})")
        page.close()

        # ---------------- navbar-with-dropdown ----------------------------
        print("== navbar-with-dropdown ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-with-dropdown")
        trig = page.get_by_role("button", name="Components").first
        check(trig.get_attribute("aria-haspopup") == "true", "dropdown: trigger aria-haspopup")
        check(trig.get_attribute("aria-expanded") == "false", "dropdown: aria-expanded=false closed")
        controls = trig.get_attribute("aria-controls")
        trig.press("ArrowDown")
        page.wait_for_timeout(250)
        check(trig.get_attribute("aria-expanded") == "true", "dropdown: ArrowDown opens")
        panel = page.locator(f'[id="{controls}"]')
        check(panel.count() == 1 and panel.is_visible(), "dropdown: panel rendered (aria-controls target)")
        check(panel.get_attribute("aria-labelledby") == trig.get_attribute("id"),
              "dropdown: panel labelled by trigger")
        check(panel.locator("a[href]").count() >= 5, "dropdown: panel items are anchors")
        active = page.evaluate("document.activeElement && document.activeElement.textContent")
        check(active == "Buttons", f"dropdown: first item focused on ArrowDown open (got {active!r})")
        # arrow cycling skips the disabled span
        for expected in ["Inputs", "Dialogs", "Navbar", "All components"]:
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(80)
            active = page.evaluate("document.activeElement && document.activeElement.textContent")
            check(active == expected, f"dropdown: ArrowDown -> {expected} (got {active!r})")
        page.keyboard.press("ArrowDown")  # wraps to first
        page.wait_for_timeout(80)
        active = page.evaluate("document.activeElement && document.activeElement.textContent")
        check(active == "Buttons", f"dropdown: ArrowDown wraps to first (got {active!r})")
        page.keyboard.press("End")
        page.wait_for_timeout(80)
        active = page.evaluate("document.activeElement && document.activeElement.textContent")
        check(active == "All components", f"dropdown: End focuses last (got {active!r})")
        page.keyboard.press("Home")
        page.wait_for_timeout(80)
        active = page.evaluate("document.activeElement && document.activeElement.textContent")
        check(active == "Buttons", f"dropdown: Home focuses first (got {active!r})")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(trig.get_attribute("aria-expanded") == "false", "dropdown: Escape closes")
        check(page.evaluate("document.activeElement === document.querySelector('[aria-haspopup]')"),
              "dropdown: focus restored to trigger on Escape")
        # ArrowUp opens with the LAST item focused
        trig.press("ArrowUp")
        page.wait_for_timeout(250)
        active = page.evaluate("document.activeElement && document.activeElement.textContent")
        check(active == "All components", f"dropdown: ArrowUp opens with last item (got {active!r})")
        # outside pointer closes without stealing focus
        page.mouse.click(600, 700)
        page.wait_for_timeout(200)
        check(trig.get_attribute("aria-expanded") == "false", "dropdown: outside pointer closes")
        # Tab closes and moves on naturally
        trig.press("Enter")
        page.wait_for_timeout(250)
        check(trig.get_attribute("aria-expanded") == "true", "dropdown: Enter opens")
        page.keyboard.press("Tab")
        page.wait_for_timeout(200)
        check(trig.get_attribute("aria-expanded") == "false", "dropdown: Tab closes")
        check(page.evaluate("document.activeElement && document.activeElement.textContent") != "Buttons",
              "dropdown: Tab moved focus forward (not stranded in the closed panel)")
        # Resources panel (bottom-end) stays inside the viewport
        res = page.get_by_role("button", name="Resources").first
        res.click()
        page.wait_for_timeout(250)
        inside = page.evaluate("""() => {
          const el = document.querySelector('[data-ds-navbar-dropdown-content]');
          const r = el.getBoundingClientRect();
          return r.left >= -1 && r.right <= window.innerWidth + 1 && r.bottom <= window.innerHeight + 1;
        }""")
        check(inside, "dropdown: bottom-end panel inside the viewport")
        check(page.locator("[data-ds-navbar-dropdown-content]").evaluate("el => el.className.includes('right-0')"),
              "dropdown: bottom-end uses end alignment")
        page.keyboard.press("Escape")
        # activating an item closes and navigates
        trig.click()
        page.wait_for_timeout(250)
        panel.get_by_role("link", name="Navbar", exact=True).click()
        page.wait_for_timeout(250)
        check(trig.get_attribute("aria-expanded") == "false", "dropdown: item activation closes")
        check(page.evaluate("window.location.hash") == "#/components/navbar", "dropdown: item navigates (hash)")
        page.close()

        # ---------------- navbar-with-mobile-menu -------------------------
        print("== navbar-with-mobile-menu ==")
        page = browser.new_page(viewport={"width": 375, "height": 900})
        open_preview(page, "navbar-with-mobile-menu", width=375)
        navs = page.locator("#ds-root nav")
        check(navs.count() == 2, "mobile-menu: two demo navbars rendered")
        labels = page.eval_on_selector_all("#ds-root nav", "els => els.map(e => e.getAttribute('aria-label'))")
        check("Main" in labels and "Controlled demo" in labels, "mobile-menu: distinct landmark labels")
        # controlled: state readout tracks every path
        controlled = page.locator('nav[aria-label="Controlled demo"]')
        toggle = controlled.get_by_role("button", name="Open navigation menu")
        check(page.evaluate("document.body.innerText.includes('the mobile menu is closed')"),
              "mobile-menu: controlled readout starts closed")
        toggle.click()
        page.wait_for_timeout(200)
        check(page.evaluate("document.body.innerText.includes('the mobile menu is open')"),
              "mobile-menu: onOpenChange fired (readout open)")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.evaluate("document.body.innerText.includes('the mobile menu is closed')"),
              "mobile-menu: Escape closes through the parent handler")
        # uncontrolled nav on the same page unaffected
        main_nav = page.locator('nav[aria-label="Main"]')
        check(main_nav.get_by_role("button", name="Open navigation menu").get_attribute("aria-expanded") == "false",
              "mobile-menu: uncontrolled navbar unaffected by controlled state")
        page.close()

        # ---------------- navbar-with-mega-menu ---------------------------
        print("== navbar-with-mega-menu ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-with-mega-menu")
        trig = page.get_by_role("button", name="Platform").first
        trig.press("ArrowDown")
        page.wait_for_timeout(250)
        panel = page.locator("[data-ds-navbar-dropdown-content]")
        check(panel.is_visible(), "mega: panel open")
        groups = panel.locator('[role="group"]')
        check(groups.count() == 3, f"mega: three labelled groups (got {groups.count()})")
        for gid in ["mm-product", "mm-resources", "mm-company"]:
            labelled = panel.locator(f'[role="group"][aria-labelledby="{gid}"]').count()
            check(labelled == 1 and panel.locator(f"#{gid}").count() == 1,
                  f"mega: group labelled by #{gid}")
        width = panel.bounding_box()["width"]
        check(width >= 500, f"mega: wide panel at 1280 (got {width})")
        inside = page.evaluate("""() => {
          const r = document.querySelector('[data-ds-navbar-dropdown-content]').getBoundingClientRect();
          return r.left >= -1 && r.right <= window.innerWidth + 1;
        }""")
        check(inside, "mega: panel inside the viewport")
        # arrows traverse every enabled item, skipping the disabled Press kit
        seen = [page.evaluate("document.activeElement && document.activeElement.textContent")]
        for _ in range(8):
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(60)
            seen.append(page.evaluate("document.activeElement && document.activeElement.textContent"))
        check(seen[0] == "Analytics", f"mega: first item focused (got {seen[0]!r})")
        check("Press kit" not in seen, "mega: disabled item skipped by arrows")
        check("Blog" in seen and seen[-1] == "Analytics",
              f"mega: traversal covers groups and wraps (got {seen})")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.evaluate("document.activeElement === document.querySelector('[aria-haspopup]')"),
              "mega: Escape restores focus to the trigger")
        page.close()

        # ---------------- navbar-sticky -----------------------------------
        print("== navbar-sticky ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-sticky")
        nav = page.locator("#ds-root nav").first
        position = nav.evaluate("el => getComputedStyle(el).position")
        check(position == "sticky", f"sticky: nav uses position sticky (got {position})")
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(250)
        top = nav.evaluate("el => el.getBoundingClientRect().top")
        check(abs(top) <= 1, f"sticky: bar pinned at viewport top while scrolled (top {top})")
        page.close()

        # ---------------- navbar-transparent ------------------------------
        print("== navbar-transparent ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-transparent")
        nav = page.locator("#ds-root nav").first
        bg = nav.evaluate("el => getComputedStyle(el).backgroundColor")
        check(bg == "rgba(0, 0, 0, 0)", f"transparent: nav surface transparent (got {bg})")
        border = nav.evaluate("el => getComputedStyle(el).borderBottomColor")
        check(border == "rgba(0, 0, 0, 0)", f"transparent: nav border transparent (got {border})")
        overlaps = page.evaluate("""() => {
          const nav = document.querySelector('#ds-root nav');
          const hero = document.querySelector('#ds-root header');
          const n = nav.getBoundingClientRect(), h = hero.getBoundingClientRect();
          return n.top >= h.top - 1 && n.bottom <= h.bottom + 1;
        }""")
        check(overlaps, "transparent: navbar overlays the page header")
        # the mobile panel stays SOLID even though the bar is transparent
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(200)
        toggle = page.get_by_role("button", name=re.compile("navigation menu")).first
        toggle.click()
        page.wait_for_timeout(250)
        region_id = toggle.get_attribute("aria-controls")
        panel_bg = page.locator(f'[id="{region_id}"]').evaluate("el => getComputedStyle(el).backgroundColor")
        check(panel_bg != "rgba(0, 0, 0, 0)", f"transparent: mobile panel keeps a solid surface (got {panel_bg})")
        page.close()

        # ---------------- navbar-with-sidebar-mobile ----------------------
        print("== navbar-with-sidebar-mobile ==")
        page = browser.new_page(viewport={"width": 375, "height": 900})
        open_preview(page, "navbar-with-sidebar-mobile", width=375)
        toggle = page.get_by_role("button", name=re.compile("navigation menu")).first
        scroll_before = page.evaluate("document.documentElement.scrollHeight")
        toggle.click()
        page.wait_for_timeout(300)
        region = page.locator(f"[id=\"{toggle.get_attribute('aria-controls')}\"]")
        check(region.is_visible(), "sidebar: side panel visible")
        check(page.locator("[data-ds-navbar-overlay]").count() == 1, "sidebar: overlay rendered")
        check(page.locator("[data-ds-navbar-overlay]").evaluate("el => getComputedStyle(el).position") == "fixed",
              "sidebar: overlay is fixed")
        inside = page.evaluate("""() => {
          const r = document.querySelector('[id^="ds-navbar-mobile"]');
          return r.contains(document.activeElement);
        }""")
        check(inside, "sidebar: focus moved into the panel on open")
        check(page.evaluate("document.body.style.overflow") == "hidden", "sidebar: body scroll locked")
        check(page.evaluate("document.documentElement.scrollHeight") == scroll_before,
              "sidebar: no layout shift with scroll lock")
        # panel never covers the full viewport (overlay strip remains)
        pw = region.bounding_box()["width"]
        check(pw <= 375 - 40, f"sidebar: panel leaves an overlay strip (width {pw})")
        # Escape closes, focus returns to the bar toggle, scroll unlocks
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        check(toggle.get_attribute("aria-expanded") == "false", "sidebar: Escape closes")
        check(page.evaluate("document.body.style.overflow") == "", "sidebar: scroll lock released")
        check(page.evaluate("document.activeElement && document.activeElement.getAttribute('aria-label')") == "Open navigation menu",
              "sidebar: focus restored to the bar toggle after Escape")
        # the panel's own close toggle works and restores focus to the bar toggle
        toggle.click()
        page.wait_for_timeout(300)
        check(page.evaluate("document.querySelectorAll('[aria-label=\\\"Close navigation menu\\\"]').length") == 2,
              "sidebar: both toggles share state (two expanded toggles while open)")
        page.get_by_role("button", name="Close navigation menu").last.click()
        page.wait_for_timeout(250)
        check(toggle.get_attribute("aria-expanded") == "false", "sidebar: panel close toggle closes")
        check(page.evaluate("document.activeElement && document.activeElement.getAttribute('aria-label')") == "Open navigation menu",
              "sidebar: focus restored to the bar toggle after panel-close")
        # overlay pointer closes
        toggle.click()
        page.wait_for_timeout(300)
        page.locator("[data-ds-navbar-overlay]").click(position={"x": 355, "y": 450})
        page.wait_for_timeout(250)
        check(toggle.get_attribute("aria-expanded") == "false", "sidebar: overlay click closes")
        page.close()

        # ---------------- navbar-with-user-menu ---------------------------
        print("== navbar-with-user-menu ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar-with-user-menu")
        trig = page.get_by_role("button", name="Account menu for Ada Rivers")
        check(trig.count() == 1, "user-menu: accessible trigger name")
        trig.press("ArrowDown")
        page.wait_for_timeout(250)
        panel = page.locator("[data-ds-navbar-dropdown-content]")
        check(panel.is_visible(), "user-menu: panel open")
        check(panel.get_by_role("link", name="Profile").count() == 1,
              "user-menu: profile link is an anchor")
        usage = panel.locator('span[aria-disabled="true"]')
        check(usage.count() == 1 and "Usage (unavailable)" in usage.first.inner_text(),
              "user-menu: disabled entry is an aria-disabled span")
        check(panel.locator('[role="separator"]').count() == 1, "user-menu: separator rendered")
        signout = panel.get_by_role("button", name="Sign out")
        check(signout.count() == 1, "user-menu: sign-out is a real button")
        # keyboard: arrows skip the disabled entry (Profile -> Settings -> Sign out)
        seq = []
        for _ in range(3):
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(60)
            seq.append(page.evaluate("document.activeElement && document.activeElement.textContent"))
        check(seq == ["Settings", "Sign out", "Profile"], f"user-menu: arrow cycle skips disabled (got {seq})")
        signout.click()
        page.wait_for_timeout(250)
        check(trig.count() == 0, "user-menu: sign out swaps the trigger for a Sign in action")
        nav = page.locator("#ds-root nav").first
        check(nav.get_by_role("button", name="Sign in").count() == 1, "user-menu: signed-out state shows Sign in")
        nav.get_by_role("button", name="Sign in").click()
        page.wait_for_timeout(200)
        trig2 = page.get_by_role("button", name="Account menu for Ada Rivers")
        check(trig2.count() == 1, "user-menu: sign in restores the account trigger")
        # focus restoration on Escape
        trig2.press("Enter")
        page.wait_for_timeout(250)
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.evaluate("document.activeElement === document.querySelector('[aria-haspopup]')"),
              "user-menu: Escape restores focus to the trigger")
        # outside pointer closes
        trig2.click()
        page.wait_for_timeout(250)
        page.mouse.click(600, 700)
        page.wait_for_timeout(200)
        check(trig2.get_attribute("aria-expanded") == "false", "user-menu: outside pointer closes")
        page.close()

        # ---------------- theme + reduced motion (reference preview) ------
        print("== theme + reduced motion ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "navbar")
        light_body = page.evaluate("getComputedStyle(document.body).backgroundColor")
        light_nav = page.locator("#ds-root nav").first.evaluate("el => getComputedStyle(el).backgroundColor")
        page.locator("#ds-theme-toggle").click()
        page.wait_for_timeout(300)
        dark_body = page.evaluate("getComputedStyle(document.body).backgroundColor")
        dark_nav = page.locator("#ds-root nav").first.evaluate("el => getComputedStyle(el).backgroundColor")
        check(light_body != dark_body, f"theme: body flips ({light_body} -> {dark_body})")
        check(light_nav != dark_nav, f"theme: nav surface flips ({light_nav} -> {dark_nav})")
        page.emulate_media(reduced_motion="reduce")
        page.wait_for_timeout(300)
        prop = page.locator("#ds-root nav a[href='#/components']").first.evaluate(
            "el => getComputedStyle(el).transitionProperty")
        check(prop == "none", f"motion: transitions removed under reduced-motion (got {prop})")
        page.close()

        browser.close()


def main():
    static_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        for f in failures:
            print("  FAIL:", f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
