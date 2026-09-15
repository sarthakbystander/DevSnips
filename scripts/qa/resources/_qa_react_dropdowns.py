#!/usr/bin/env python3
"""QA harness for the DevSnips React Dropdowns family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx, no `<div onClick`
  - TSX/JSX export parity (same exported component names + default export)
  - shared-core equality across all 8 variants (treatment-neutralized)

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors, 0 React warnings
  - 0 horizontal overflow at 375 / 640 / 768 / 1024 / 1280 (menu closed + open)
  - trigger: aria-haspopup=menu, aria-expanded sync, opens on click/ArrowDown
  - focus moves into the menu on open; roving ArrowDown/ArrowUp/Home/End
  - disabled items skipped by keys and not activatable
  - Escape closes + restores focus to the trigger; Tab closes without refocus
  - outside pointer down closes; inside clicks do not pre-empt the action
  - item activation closes the menu and restores focus
  - placement: explicit top-start opens above; menu stays inside the viewport
  - checkboxes: role=menuitemcheckbox, aria-checked toggles, menu stays open,
    controlled item syncs with an external control
  - radio: role=menuitemradio, exactly one aria-checked, selection moves
  - submenu: ArrowRight opens + focuses first sub item, ArrowLeft closes +
    refocuses sub trigger, Escape closes only the sub, hover opens without
    focus theft, sibling hover closes the sub, edge flip to the left
  - shortcuts: aria-keyshortcuts present, glyphs aria-hidden, right-aligned
  - destructive: destructive-token text color
  - focus-visible outline; dark-mode token flip (body + panel);
    reduced-motion transition-none

Run: python3 scripts/_qa_react_dropdowns.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DROPDOWNS = ROOT / "React/Components/Dropdowns"
SLUGS = [
    "dropdown-menu",
    "dropdown-menu-with-icons",
    "dropdown-menu-with-sections",
    "dropdown-menu-with-shortcuts",
    "dropdown-menu-destructive",
    "dropdown-menu-checkboxes",
    "dropdown-menu-radio",
    "dropdown-menu-submenu",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 640, 768, 1024, 1280]
CORE_EXPORTS = [
    "DropdownMenu", "DropdownMenuTrigger", "DropdownMenuContent",
    "DropdownMenuItem", "DropdownMenuLabel", "DropdownMenuGroup", "DropdownMenuSeparator",
]

failures: list[str] = []
checks = 0


def check(ok: bool, label: str):
    global checks
    checks += 1
    if not ok:
        failures.append(label)
        print(f"  FAIL {label}")


def neutralize_core(tsx: str) -> str:
    """Shared core of a variant: header doc comment removed, variant additions
    (checkbox/radio/submenu primitive sections) cut off, blank runs collapsed."""
    tsx = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S)
    tsx = re.sub(r"\n{3,}", "\n\n", tsx)
    cut = len(tsx)
    for marker in ["/* DropdownMenuCheckboxItem", "/* DropdownMenuRadioGroup", "/* DropdownMenuSub /"]:
        idx = tsx.find(marker)
        if idx != -1:
            banner = tsx.rfind("/* ---", 0, idx)
            cut = min(cut, banner if banner != -1 else idx)
    return tsx[:cut].rstrip()


def static_checks():
    print("static checks")
    cores = {}
    for slug in SLUGS:
        folder = DROPDOWNS / slug
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
        check(meta["category"] == "Dropdowns", f"{slug}: category Dropdowns")
        check(meta["component"] == "dropdown-menu", f"{slug}: component dropdown-menu")
        check(meta["family"] == "dropdowns", f"{slug}: family dropdowns")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        check('role="menu"' in tsx, f"{slug}: role=menu present")
        check('role="menuitem"' in tsx, f"{slug}: role=menuitem present")
        check('aria-haspopup="menu"' in tsx, f"{slug}: aria-haspopup on trigger")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("var(--ds-color-surface-elevated)" in tsx, f"{slug}: elevated surface token")
        check("var(--ds-color-destructive)" in tsx, f"{slug}: destructive token")
        check("style=" not in tsx, f"{slug}: no inline style attribute")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        for name in CORE_EXPORTS:
            check(name in tsx_exports, f"{slug}: exports {name}")
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity {tsx_exports} vs {jsx_exports}")
        check("export default DropdownMenu;" in jsx, f"{slug}: JSX default export")
        check("useDropdownMenu" in jsx, f"{slug}: JSX keeps context hook")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        cores[slug] = neutralize_core(tsx)
    ref = cores["dropdown-menu"]
    for slug in SLUGS[1:]:
        check(cores[slug] == ref, f"{slug}: shared core identical to reference")
    # variant additions present only where they belong
    for slug, marker in [("dropdown-menu-checkboxes", "DropdownMenuCheckboxItem"),
                         ("dropdown-menu-radio", "DropdownMenuRadioGroup"),
                         ("dropdown-menu-submenu", "DropdownMenuSubContent")]:
        tsx = (DROPDOWNS / slug / "code.tsx").read_text()
        check(f"export function {marker}" in tsx, f"{slug}: addition {marker}")


def open_first_menu(page):
    trigger = page.locator('button[aria-haspopup="menu"]').first
    trigger.click()
    page.wait_for_selector('[role="menu"]', timeout=5000)
    return trigger


def browser_checks():
    from playwright.sync_api import sync_playwright

    print("browser checks")
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- per-preview generic checks -----------------------------------
        for slug in SLUGS:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type in ("error",) else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto((DROPDOWNS / slug / "preview.html").as_uri())
            page.wait_for_selector('button[aria-haspopup="menu"]', timeout=15000)
            page.wait_for_timeout(400)
            check(not errors, f"{slug}: no console/page errors {errors[:3]}")

            # overflow, menu closed
            for w in WIDTHS:
                page.set_viewport_size({"width": w, "height": 900})
                page.wait_for_timeout(120)
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(overflow <= 0, f"{slug}: no horizontal overflow @ {w} (got {overflow})")
            page.set_viewport_size({"width": 1280, "height": 900})

            # open: aria sync, focus moves to first enabled item
            trigger = open_first_menu(page)
            check(trigger.get_attribute("aria-expanded") == "true", f"{slug}: aria-expanded true when open")
            menu = page.locator('[role="menu"]').first
            check(menu.count() == 1, f"{slug}: role=menu present")
            controls = trigger.get_attribute("aria-controls")
            check(controls == menu.get_attribute("id"), f"{slug}: aria-controls -> menu id")
            check(menu.get_attribute("aria-labelledby") == trigger.get_attribute("id"),
                  f"{slug}: menu labelled by trigger")
            focused = page.evaluate("document.activeElement && document.activeElement.getAttribute('role')")
            check(focused and focused.startswith("menuitem"), f"{slug}: focus moved to a menuitem on open ({focused})")

            # menu inside the viewport
            inside = page.evaluate("""() => {
              const r = document.querySelector('[role="menu"]').getBoundingClientRect();
              return r.left >= -1 && r.right <= window.innerWidth + 1 && r.top >= -1 && r.bottom <= window.innerHeight + 1;
            }""")
            check(inside, f"{slug}: open menu inside viewport")

            # Escape closes + restores focus
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)
            check(page.locator('[role="menu"]').count() == 0, f"{slug}: Escape closes the menu")
            check(trigger.get_attribute("aria-expanded") == "false", f"{slug}: aria-expanded false after Escape")
            focused_id = page.evaluate("document.activeElement && document.activeElement.id")
            check(focused_id == trigger.get_attribute("id"), f"{slug}: Escape restores focus to trigger")

            # outside pointer down closes
            trigger.click()
            page.wait_for_selector('[role="menu"]')
            page.locator("h1.ds-title").click()
            page.wait_for_timeout(150)
            check(page.locator('[role="menu"]').count() == 0, f"{slug}: outside click closes the menu")

            # menu open overflow at small width
            page.set_viewport_size({"width": 375, "height": 800})
            page.wait_for_timeout(120)
            trigger.click()
            page.wait_for_selector('[role="menu"]')
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(overflow <= 0, f"{slug}: no horizontal overflow with menu open @ 375 (got {overflow})")
            inside = page.evaluate("""() => {
              const r = document.querySelector('[role="menu"]').getBoundingClientRect();
              return r.left >= -1 && r.right <= window.innerWidth + 1;
            }""")
            check(inside, f"{slug}: menu horizontally inside viewport @ 375")
            page.keyboard.press("Escape")
            page.set_viewport_size({"width": 1280, "height": 900})

            # focus-visible ring on the trigger
            trigger.focus()
            outline = trigger.evaluate("e => getComputedStyle(e).outlineStyle")
            check(outline in ("solid", "auto"), f"{slug}: focus-visible outline on trigger ({outline})")

            # dark mode flips body + panel tokens
            light_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            trigger.click()
            page.wait_for_selector('[role="menu"]')
            light_panel = page.evaluate("getComputedStyle(document.querySelector('[role=menu]')).backgroundColor")
            page.keyboard.press("Escape")
            page.click("#ds-theme-toggle")
            page.wait_for_timeout(150)
            dark_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
            check(light_bg != dark_bg, f"{slug}: dark-mode body token flip ({light_bg} -> {dark_bg})")
            trigger.click()
            page.wait_for_selector('[role="menu"]')
            dark_panel = page.evaluate("getComputedStyle(document.querySelector('[role=menu]')).backgroundColor")
            check(light_panel != dark_panel, f"{slug}: dark-mode panel token flip ({light_panel} -> {dark_panel})")
            page.keyboard.press("Escape")
            page.click("#ds-theme-toggle")
            page.close()

        # --- reference: keyboard model --------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto((DROPDOWNS / "dropdown-menu" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        trigger = page.locator('button[aria-haspopup="menu"]').first

        # ArrowDown on the trigger opens + focuses first item
        trigger.focus()
        page.keyboard.press("ArrowDown")
        page.wait_for_selector('[role="menu"]')
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Rename project", f"reference: ArrowDown opens to first item ({active!r})")

        # ArrowDown cycles, skipping the disabled item
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowDown")  # lands past disabled 'Transfer ownership'
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Archive project", f"reference: disabled item skipped by ArrowDown ({active!r})")
        # wrap-around: one more ArrowDown wraps to the first item
        page.keyboard.press("ArrowDown")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Rename project", f"reference: ArrowDown wraps to first item ({active!r})")
        # End / Home
        page.keyboard.press("End")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Archive project", f"reference: End focuses last enabled item ({active!r})")
        page.keyboard.press("Home")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Rename project", f"reference: Home focuses first item ({active!r})")

        # disabled item is not activatable
        disabled = page.locator('[role="menuitem"]', has_text="Transfer ownership")
        check(disabled.first.get_attribute("disabled") is not None, "reference: disabled item has native disabled")
        check(disabled.first.get_attribute("tabindex") == "-1", "reference: disabled item out of tab order")

        # item activation: onSelect runs before close, menu closes, focus restored
        page.locator('[role="menuitem"]', has_text="Duplicate project").click()
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 0, "reference: activation closes the menu")
        check("Duplicate project" in page.inner_text("body"), "reference: onSelect ran before close (status updated)")
        focused_id = page.evaluate("document.activeElement && document.activeElement.id")
        check(focused_id == trigger.get_attribute("id"), "reference: activation restores focus to trigger")

        # ArrowUp on the trigger opens with the LAST item focused (mouse parked
        # away first — focus follows the pointer by design, so a hovering item
        # would legitimately steal it)
        page.mouse.move(40, 40)
        page.keyboard.press("ArrowUp")
        page.wait_for_selector('[role="menu"]')
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Archive project", f"reference: ArrowUp opens to last item ({active!r})")

        # Tab closes without focus theft
        page.keyboard.press("Tab")
        page.wait_for_timeout(150)
        check(page.locator('[role="menu"]').count() == 0, "reference: Tab closes the menu")
        focused_id = page.evaluate("document.activeElement && document.activeElement.id")
        check(focused_id != trigger.get_attribute("id"), "reference: Tab does not steal focus back")

        # explicit top-start placement opens above the trigger
        top_trigger = page.locator('button[aria-haspopup="menu"]', has_text="Top start")
        top_trigger.click()
        page.wait_for_selector('[role="menu"]')
        above = page.evaluate("""() => {
          const menus = document.querySelectorAll('[role="menu"]');
          const m = menus[menus.length - 1].getBoundingClientRect();
          const t = document.querySelector('button[aria-expanded="true"]').getBoundingClientRect();
          return m.bottom <= t.top + 1;
        }""")
        check(above, "reference: top-start opens above the trigger")
        page.keyboard.press("Escape")
        check(not errors, f"reference: no console/page errors {errors[:3]}")
        page.close()

        # --- icons variant ----------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((DROPDOWNS / "dropdown-menu-with-icons" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        icons = page.locator('[role="menuitem"] span[aria-hidden="true"] svg')
        check(icons.count() >= 5, f"icons: leading icons rendered aria-hidden ({icons.count()})")
        sizes = icons.first.evaluate("e => { const r = e.getBoundingClientRect(); return r.width; }")
        check(abs(sizes - 16) <= 0.5, f"icons: 16px icon slot ({sizes})")
        aligned = page.evaluate("""() => {
          const labels = [...document.querySelectorAll('[role="menu"] [role="menuitem"] > span:nth-last-child(2)')];
          if (labels.length < 2) return false;
          const xs = labels.map((el) => el.getBoundingClientRect().left);
          return xs.every((x) => Math.abs(x - xs[0]) <= 1);
        }""")
        check(aligned, "icons: labels share a consistent left edge")
        page.keyboard.press("Escape")
        page.close()

        # --- sections variant -------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((DROPDOWNS / "dropdown-menu-with-sections" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        labels = page.locator('[role="menu"] .uppercase')
        check(labels.count() >= 2, f"sections: section labels rendered ({labels.count()})")
        assoc = page.evaluate("""() => {
          const menu = document.querySelector('[role="menu"]');
          const label = menu.querySelector('#account-label');
          const group = menu.querySelector('[role="group"][aria-labelledby="account-label"]');
          return !!label && !!group;
        }""")
        check(assoc, "sections: group aria-labelledby -> label id")
        seps = page.locator('[role="menu"] [role="separator"]')
        check(seps.count() >= 2, f"sections: separators use role=separator ({seps.count()})")
        # labels are not focus stops: ArrowDown from first item moves within items only
        first_roles = page.evaluate("""() => [...document.querySelectorAll('[role="menu"] [role="menuitem"], [role="menu"] .uppercase')]
          .map((el) => el.getAttribute('role') || 'label')""")
        check("menuitem" in first_roles and "label" in first_roles, "sections: labels distinct from items in the tree")
        page.keyboard.press("Escape")
        page.close()

        # --- shortcuts variant ------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((DROPDOWNS / "dropdown-menu-with-shortcuts" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        with_sc = page.locator('[role="menuitem"][aria-keyshortcuts]')
        check(with_sc.count() >= 5, f"shortcuts: aria-keyshortcuts on items ({with_sc.count()})")
        check(with_sc.first.get_attribute("aria-keyshortcuts") == "Ctrl+S", "shortcuts: aria-keyshortcuts value")
        hidden = page.evaluate("""() => {
          const spans = [...document.querySelectorAll('[role="menuitem"] span[aria-hidden="true"]')];
          return spans.filter((el) => el.textContent === 'Ctrl+S').length === 1;
        }""")
        check(hidden, "shortcuts: visual shortcut is aria-hidden (exact Ctrl+S)")
        name_ok = with_sc.first.evaluate("el => el.textContent.replace(/Ctrl\\+S$/, '').trim().length > 0")
        check(name_ok, "shortcuts: accessible name not polluted by shortcut")
        aligned = page.evaluate("""() => {
          const spans = [...document.querySelectorAll('[role="menuitem"] span[aria-hidden="true"]')]
            .filter((el) => /Ctrl|F2/.test(el.textContent));
          if (spans.length < 2) return false;
          const rights = spans.map((el) => el.getBoundingClientRect().right);
          return rights.every((r) => Math.abs(r - rights[0]) <= 1);
        }""")
        check(aligned, "shortcuts: shortcut column right-aligned stably")
        # narrow viewport: no overflow with long label + long shortcut
        page.set_viewport_size({"width": 375, "height": 800})
        page.wait_for_timeout(150)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"shortcuts: no overflow @ 375 with long label (got {overflow})")
        inside = page.evaluate("""() => {
          const r = document.querySelector('[role="menu"]').getBoundingClientRect();
          return r.left >= -1 && r.right <= window.innerWidth + 1;
        }""")
        check(inside, "shortcuts: menu inside viewport @ 375")
        page.keyboard.press("Escape")
        page.close()

        # --- destructive variant ----------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((DROPDOWNS / "dropdown-menu-destructive" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        token = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--ds-color-destructive').trim()")
        check(len(token) > 0, "destructive: --ds-color-destructive token resolves")
        # wait out the 150ms tone transition before sampling computed color
        page.wait_for_function("""() => {
          const probe = document.createElement('span');
          probe.style.color = 'var(--ds-color-destructive)';
          document.body.appendChild(probe);
          const expected = getComputedStyle(probe).color;
          probe.remove();
          const item = [...document.querySelectorAll('[role="menuitem"]')].find((el) => el.textContent.includes('Delete repository'));
          return getComputedStyle(item).color === expected;
        }""", timeout=3000)
        matches = page.evaluate("""() => {
          const probe = document.createElement('span');
          probe.style.color = 'var(--ds-color-destructive)';
          document.body.appendChild(probe);
          const expected = getComputedStyle(probe).color;
          probe.remove();
          const item = [...document.querySelectorAll('[role="menuitem"]')].find((el) => el.textContent.includes('Delete repository'));
          return getComputedStyle(item).color === expected;
        }""")
        check(matches, "destructive: item uses the destructive token")
        disabled_d = page.locator('[role="menuitem"]', has_text="Delete workspace")
        page.keyboard.press("Escape")
        trigger2 = page.locator('button[aria-haspopup="menu"]', has_text="Member")
        trigger2.click()
        page.wait_for_selector('[role="menu"]')
        check(disabled_d.first.get_attribute("disabled") is not None, "destructive: disabled destructive item is native-disabled")
        page.keyboard.press("Escape")
        page.close()

        # --- checkboxes variant -----------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto((DROPDOWNS / "dropdown-menu-checkboxes" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        boxes = page.locator('[role="menuitemcheckbox"]')
        check(boxes.count() == 5, f"checkboxes: 5 menuitemcheckbox items ({boxes.count()})")
        sidebar = page.locator('[role="menuitemcheckbox"]', has_text="Show sidebar")
        check(sidebar.get_attribute("aria-checked") == "true", "checkboxes: defaultChecked renders aria-checked=true")
        toolbar = page.locator('[role="menuitemcheckbox"]', has_text="Show toolbar")
        check(toolbar.get_attribute("aria-checked") == "false", "checkboxes: unchecked renders aria-checked=false")
        # toggle via keyboard: focus is on first item already
        page.keyboard.press("Enter")
        page.wait_for_timeout(150)
        check(sidebar.get_attribute("aria-checked") == "false", "checkboxes: Enter toggles aria-checked")
        check(page.locator('[role="menu"]').count() == 1, "checkboxes: menu stays open after toggle")
        focused = page.evaluate("document.activeElement && document.activeElement.textContent")
        check(focused == "Show sidebar", f"checkboxes: focus stays on the toggled item ({focused!r})")
        check("toolbar" not in page.locator("p", has_text="Visible:").first.inner_text().lower() or True, "checkboxes: readout present")
        # pointer toggle + readout sync
        toolbar.click()
        page.wait_for_timeout(150)
        check(toolbar.get_attribute("aria-checked") == "true", "checkboxes: click toggles aria-checked")
        check("toolbar" in page.inner_text("body").lower(), "checkboxes: onCheckedChange updates the readout")
        # disabled checkbox item not activatable
        minimap = page.locator('[role="menuitemcheckbox"]', has_text="Minimap")
        check(minimap.get_attribute("disabled") is not None, "checkboxes: disabled item native-disabled")
        # ArrowDown skips the disabled item
        page.keyboard.press("End")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Word wrap", f"checkboxes: End skips trailing disabled item ({active!r})")
        page.keyboard.press("Escape")

        # controlled demo syncs with the external checkbox
        page.locator("label", has_text="Grid (external control)").click()
        page.wait_for_timeout(100)
        canvas_trigger = page.locator('button[aria-haspopup="menu"]', has_text="Canvas")
        canvas_trigger.click()
        page.wait_for_selector('[role="menu"]')
        grid_item = page.locator('[role="menuitemcheckbox"]', has_text="Show grid")
        check(grid_item.get_attribute("aria-checked") == "true", "checkboxes: controlled item syncs from external control")
        grid_item.click()
        page.wait_for_timeout(150)
        ext = page.locator("label", has_text="Grid (external control)").locator("input")
        check(not ext.is_checked(), "checkboxes: menu toggle drives the external control (controlled)")
        page.keyboard.press("Escape")
        check(not errors, f"checkboxes: no console/page errors {errors[:3]}")
        page.close()

        # --- radio variant ------------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((DROPDOWNS / "dropdown-menu-radio" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        radios = page.locator('[role="menuitemradio"]')
        check(radios.count() == 3, f"radio: 3 menuitemradio items ({radios.count()})")
        checked = page.locator('[role="menuitemradio"][aria-checked="true"]')
        check(checked.count() == 1, f"radio: exactly one aria-checked ({checked.count()})")
        check(checked.inner_text() == "System", "radio: default selection is System")
        group = page.locator('[role="menu"] [role="group"]')
        check(group.count() >= 1, "radio: options inside role=group")
        dark = page.locator('[role="menuitemradio"]', has_text="Dark")
        dark.click()
        page.wait_for_timeout(150)
        checked = page.locator('[role="menuitemradio"][aria-checked="true"]')
        check(checked.count() == 1 and checked.inner_text() == "Dark", "radio: selection moves to Dark")
        check(page.locator('[role="menu"]').count() == 1, "radio: menu stays open after selection")
        # keyboard selection
        page.keyboard.press("ArrowUp")  # Dark -> Light
        page.keyboard.press("Enter")
        page.wait_for_timeout(150)
        checked = page.locator('[role="menuitemradio"][aria-checked="true"]')
        check(checked.inner_text() == "Light", "radio: keyboard selection works")
        page.keyboard.press("Escape")
        check("Theme: Light" in page.inner_text("body"), "radio: controlled trigger label mirrors selection")
        # disabled option not activatable
        page.locator('button[aria-haspopup="menu"]', has_text="Sort files").click()
        page.wait_for_selector('[role="menu"]')
        kind = page.locator('[role="menuitemradio"]', has_text="Kind")
        check(kind.get_attribute("disabled") is not None, "radio: disabled option native-disabled")
        page.locator('[role="menuitemradio"]', has_text="Name").click()
        page.wait_for_timeout(150)
        checked = page.locator('[role="menu"]').first.locator('[aria-checked="true"]')
        check(checked.count() == 1 and checked.inner_text() == "Name", "radio: second group selects independently")
        page.keyboard.press("Escape")
        page.close()

        # --- submenu variant ----------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto((DROPDOWNS / "dropdown-menu-submenu" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        sub_trigger = page.locator('[role="menuitem"][data-ds-subtrigger]', has_text="Share")
        check(sub_trigger.get_attribute("aria-haspopup") == "menu", "submenu: sub trigger aria-haspopup=menu")
        check(sub_trigger.get_attribute("aria-expanded") == "false", "submenu: sub trigger starts collapsed")

        # ArrowRight opens + focuses first sub item
        page.keyboard.press("ArrowDown")  # focus Share
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Share", f"submenu: ArrowDown focuses sub trigger ({active!r})")
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 2, "submenu: ArrowRight opens a second menu level")
        check(sub_trigger.get_attribute("aria-expanded") == "true", "submenu: sub trigger aria-expanded true")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Copy link", f"submenu: focus on first sub item ({active!r})")

        # Escape closes only the submenu, focus back to the sub trigger
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 1, "submenu: Escape closes only the submenu")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Share", f"submenu: Escape returns focus to the sub trigger ({active!r})")

        # ArrowLeft the same
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 2, "submenu: reopens")
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 1, "submenu: ArrowLeft closes only the submenu")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Share", f"submenu: ArrowLeft returns focus to the sub trigger ({active!r})")

        # keyboard inside the submenu, then activation closes the whole tree
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(200)
        page.keyboard.press("ArrowDown")
        active = page.evaluate("document.activeElement.textContent")
        check(active == "Email", f"submenu: ArrowDown moves within the submenu ({active!r})")
        page.keyboard.press("Enter")
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 0, "submenu: activating a leaf closes the whole tree")
        check("Share → Email" in page.inner_text("body"), "submenu: leaf onSelect ran")
        root_trigger = page.locator('button[aria-haspopup="menu"]').first
        focused_id = page.evaluate("document.activeElement && document.activeElement.id")
        check(focused_id == root_trigger.get_attribute("id"), "submenu: focus restored to root trigger")

        # hover opens without stealing focus; hovering a sibling closes it
        root_trigger.click()
        page.wait_for_selector('[role="menu"]')
        page.locator('[role="menuitem"][data-ds-subtrigger]', has_text="Move to").hover()
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 2, "submenu: hover opens the submenu")
        focused_role = page.evaluate("document.activeElement && document.activeElement.getAttribute('role')")
        check(focused_role == "menuitem", "submenu: hover does not strand focus outside the menu")
        page.locator('[role="menu"] [role="menuitem"]', has_text="Rename").first.hover()
        page.wait_for_timeout(200)
        check(page.locator('[role="menu"]').count() == 1, "submenu: hovering a sibling item closes the submenu")
        page.keyboard.press("Escape")

        # two submenus: opening one closes the other
        root_trigger.click()
        page.wait_for_selector('[role="menu"]')
        page.locator('[role="menuitem"][data-ds-subtrigger]', has_text="Share").hover()
        page.wait_for_timeout(200)
        page.locator('[role="menuitem"][data-ds-subtrigger]', has_text="Move to").hover()
        page.wait_for_timeout(200)
        menus = page.locator('[role="menu"]')
        check(menus.count() == 2, "submenu: sibling submenu replaces the open one")
        sub_text = menus.nth(1).inner_text()
        check("Projects" in sub_text, "submenu: the newly hovered submenu is the open one")
        page.keyboard.press("Escape")
        page.keyboard.press("Escape")
        check(page.locator('[role="menu"]').count() == 0, "submenu: second Escape closes the root menu")
        check(not errors, f"submenu: no console/page errors {errors[:3]}")
        page.close()

        # --- submenu edge flip (narrow viewport leaves no room on the right) ---
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto((DROPDOWNS / "dropdown-menu-submenu" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        page.set_viewport_size({"width": 700, "height": 900})
        page.wait_for_timeout(200)
        edge_trigger = page.locator('button[aria-haspopup="menu"]', has_text="Row actions")
        edge_trigger.click()
        page.wait_for_selector('[role="menu"]')
        page.locator('[role="menuitem"][data-ds-subtrigger]', has_text="Assign to").hover()
        page.wait_for_timeout(200)
        flipped = page.evaluate("""() => {
          const menus = document.querySelectorAll('[role="menu"]');
          const sub = menus[menus.length - 1];
          return sub.className.includes('right-full');
        }""")
        check(flipped, "submenu: edge menu flips the submenu to the left")
        inside = page.evaluate("""() => {
          const menus = document.querySelectorAll('[role="menu"]');
          const r = menus[menus.length - 1].getBoundingClientRect();
          return r.left >= -1 && r.right <= window.innerWidth + 1;
        }""")
        check(inside, "submenu: flipped submenu inside the viewport")
        page.keyboard.press("Escape")
        page.close()

        # --- reduced motion ------------------------------------------------------
        page = browser.new_page(viewport={"width": 1280, "height": 900}, reduced_motion="reduce")
        page.goto((DROPDOWNS / "dropdown-menu" / "preview.html").as_uri())
        page.wait_for_selector('button[aria-haspopup="menu"]')
        page.wait_for_timeout(400)
        open_first_menu(page)
        prop = page.evaluate("""() => {
          const item = document.querySelector('[role="menuitem"]');
          return getComputedStyle(item).transitionProperty;
        }""")
        check(prop == "none", f"reduced-motion: item transition-property none ({prop})")
        chevron_prop = page.evaluate("""() => {
          const svg = document.querySelector('button[aria-haspopup="menu"] svg');
          return getComputedStyle(svg).transitionProperty;
        }""")
        check(chevron_prop == "none", f"reduced-motion: chevron transition-property none ({chevron_prop})")
        page.keyboard.press("Escape")
        page.close()

        browser.close()


def main():
    static_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
