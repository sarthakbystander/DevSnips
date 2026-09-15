#!/usr/bin/env python3
"""QA harness for the DevSnips React Tooltips family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx, no `<div onClick`, no inline `style=`, no hex colors
  - TSX/JSX export parity (same exported component names + default export)
    and prop-name parity for every exported component signature
  - shared-core equality across all 7 variants (header-comment-neutralized)

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors
  - 0 horizontal overflow at 375 / 768 / 1280 (closed and open)
  - trigger: aria-describedby points at the role=tooltip content id
  - hover opens after delayDuration (not instantly); focus opens immediately
  - pointer leave / blur / Escape dismiss; focus stays on the trigger
  - adjacent tooltips: only one open at a time
  - arrow element rendered (aria-hidden), w-max bubble sizing
  - placement: side geometry for the full 12-cell matrix, align edges,
    viewport containment at 375 + 1280, edge flip (side=right -> left @375)
  - long content: readable measure (<= 258px incl. border), wrapped lines
  - rich content: title + metadata + kbd chip, aria-hidden status dot
  - disabled trigger: focusable span wrapper opens on hover AND keyboard
    focus; the disabled prop suppresses hover/focus and closes an open one
  - controlled: parent ignores hover (logged via onOpenChange), click forces
    open + auto-close, external toggle pins open
  - focus-visible 2px outline; dark-mode token flip (body + bubble);
    reduced-motion transition-none; open bubble inside the viewport

Run: python3 scripts/_qa_react_tooltips.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLTIPS = ROOT / "React/Components/Tooltips"
SLUGS = [
    "tooltip",
    "tooltip-placement",
    "tooltip-with-icon",
    "tooltip-with-long-content",
    "tooltip-rich-content",
    "tooltip-disabled-trigger",
    "tooltip-controlled",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = ["Tooltip", "TooltipTrigger", "TooltipContent"]

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
    props = []
    for raw in block.split(","):
        seg = raw.strip().strip("(){}").strip()
        if not seg or seg.startswith("..."):
            continue
        seg = re.sub(r"\s*=.*$", "", seg)
        seg = re.sub(r"\?:.*$", "", seg)
        seg = re.sub(r":.*$", "", seg)
        seg = seg.strip()
        if seg:
            props.append(seg)
    return sorted(set(props))


def static_checks():
    print("static checks")
    cores = {}
    for slug in SLUGS:
        folder = TOOLTIPS / slug
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
        check(meta["category"] == "Tooltips", f"{slug}: category Tooltips")
        check(meta["component"] == "tooltip", f"{slug}: component tooltip")
        check(meta["family"] == "tooltips", f"{slug}: family tooltips")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        check('role="tooltip"' in tsx, f"{slug}: role=tooltip present")
        check("aria-describedby" in tsx, f"{slug}: aria-describedby wiring")
        check("pointer-events-none" in tsx, f"{slug}: non-interactive content")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("var(--ds-color-surface-elevated)" in tsx, f"{slug}: elevated surface token")
        check("var(--ds-color-focus-ring)" in tsx or "focus-ring" not in tsx,
              f"{slug}: no off-token focus ring")
        check("style=" not in tsx, f"{slug}: no inline style attribute")
        check(re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx) == [],
              f"{slug}: no hex color literals")
        tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
        for name in CORE_EXPORTS:
            check(name in tsx_exports, f"{slug}: exports {name}")
        m = re.search(r"\nexport \{([^}]*)\};", jsx)
        jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(tsx_exports == jsx_exports, f"{slug}: export parity {tsx_exports} vs {jsx_exports}")
        check("export default Tooltip;" in jsx, f"{slug}: JSX default export")
        check("useTooltip" in jsx, f"{slug}: JSX keeps context hook")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        for name in CORE_EXPORTS:
            tp, jp = prop_signature(tsx, name), prop_signature(jsx, name)
            check(tp == jp, f"{slug}: {name} prop parity {tp} vs {jp}")
        cores[slug] = neutralize_core(tsx)
    ref = cores["tooltip"]
    for slug in SLUGS[1:]:
        check(cores[slug] == ref, f"{slug}: shared core identical to reference")


def open_preview(page, slug):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((TOOLTIPS / slug / "preview.html").as_uri())
    page.wait_for_selector("#ds-root *", timeout=15000)
    page.wait_for_timeout(400)
    return errors


def hover_open(page, trigger, slug, label, wait=550):
    """Hover a trigger and wait for the delayed open; return the tooltip."""
    trigger.hover()
    page.wait_for_timeout(wait)
    tip = page.locator('[role="tooltip"]')
    check(tip.count() == 1, f"{slug}: {label} — hover opens the tooltip")
    return tip


def close_all(page):
    page.mouse.move(2, 2)
    page.wait_for_timeout(200)


def tab_to(page, predicate_js, label, max_tabs=14):
    """Tab forward until activeElement satisfies the JS predicate."""
    for _ in range(max_tabs):
        page.keyboard.press("Tab")
        if page.evaluate(predicate_js):
            return True
    check(False, label)
    return False


def no_overflow(page, slug, state):
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(120)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"{slug}: no horizontal overflow ({state}) @ {w} (got {overflow})")
    page.set_viewport_size({"width": 1280, "height": 900})


def bubble_inside_viewport(page, slug, label):
    inside = page.evaluate("""() => {
      const el = document.querySelector('[role="tooltip"]');
      if (!el) return false;
      const r = el.getBoundingClientRect();
      return r.left >= -1 && r.right <= window.innerWidth + 1 && r.top >= -1 && r.bottom <= window.innerHeight + 1;
    }""")
    check(inside, f"{slug}: {label} — bubble inside viewport")


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
            check(page.locator('[role="tooltip"]').count() == 0, f"{slug}: no tooltip rendered initially")
            no_overflow(page, slug, "closed")
            page.close()

        # ---------------- tooltip (reference) ------------------------------
        print("== tooltip ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip")
        trig = page.get_by_role("button", name="About the retention period")
        describedby = trig.get_attribute("aria-describedby")
        check(bool(describedby), "tooltip: trigger has aria-describedby")

        # hover: delayed open (not instant), then visible
        trig.hover()
        check(page.locator('[role="tooltip"]').count() == 0,
              "tooltip: hover respects delayDuration (not open instantly)")
        page.wait_for_timeout(500)
        tip = page.locator('[role="tooltip"]')
        check(tip.count() == 1, "tooltip: hover opens after the delay")
        check(tip.get_attribute("id") == describedby, "tooltip: aria-describedby -> content id")
        check("recoverable" in tip.text_content(), "tooltip: content text")
        check(tip.locator("span[aria-hidden='true']").count() == 1, "tooltip: arrow rendered (aria-hidden)")
        tb, cb = trig.bounding_box(), tip.bounding_box()
        check(cb["y"] + cb["height"] <= tb["y"] + 2, "tooltip: default placement above the trigger")
        check(cb["width"] <= 258, f"tooltip: bubble capped at the 16rem measure (got {cb['width']})")
        check(cb["width"] > 150, f"tooltip: w-max bubble not squeezed to the trigger width (got {cb['width']})")
        bubble_inside_viewport(page, "tooltip", "reference")

        # Escape dismisses, focus behavior unaffected
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip: Escape dismisses")

        # pointer leave closes
        trig.hover()
        page.wait_for_timeout(500)
        page.mouse.move(2, 2)
        page.wait_for_timeout(200)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip: pointer leave dismisses")

        # keyboard focus opens immediately (no hover delay) + focus ring
        ok = tab_to(page, 'document.activeElement.getAttribute("aria-label") === "About the retention period"',
                    "tooltip: Tab reaches the info trigger")
        if ok:
            check(page.locator('[role="tooltip"]').count() == 1,
                  "tooltip: focus opens immediately (no hover delay)")
            style = page.evaluate("""() => {
              const cs = getComputedStyle(document.activeElement);
              return [cs.outlineWidth, cs.outlineStyle];
            }""")
            check(style[0] == "2px" and style[1] in ("auto", "solid"),
                  f"tooltip: focus-visible ring on trigger (2px {style[1]})")
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)
            check(page.locator('[role="tooltip"]').count() == 0, "tooltip: Escape dismisses the focus-opened tooltip")
            check(page.evaluate('document.activeElement.getAttribute("aria-label")') == "About the retention period",
                  "tooltip: focus stays on the trigger after Escape")
            # blur closes
            tab_to(page, 'document.activeElement.getAttribute("aria-label") === "About the retention period"',
                   "tooltip: re-focus the info trigger")
            page.keyboard.press("Tab")
            page.wait_for_timeout(150)
            check(page.locator('[role="tooltip"]').count() == 0, "tooltip: blur dismisses")

        # adjacent tooltips: only one open at a time
        refresh = page.get_by_role("button", name="Refresh report")
        download = page.get_by_role("button", name="Download report")
        refresh.hover()
        page.wait_for_timeout(500)
        check(page.locator('[role="tooltip"]').count() == 1, "tooltip: first toolbar tooltip open")
        download.hover()
        page.wait_for_timeout(500)
        check(page.locator('[role="tooltip"]').count() == 1, "tooltip: exactly one tooltip with adjacent triggers")
        check("CSV" in page.locator('[role="tooltip"]').text_content(),
              "tooltip: second tooltip replaced the first")
        close_all(page)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip: toolbar tooltips close on pointer leave")

        # open-state overflow + containment across widths (re-hover at each
        # width: resizing moves the trigger out from under the pointer, which
        # legitimately dismisses a hover-opened tooltip)
        for w in WIDTHS:
            page.set_viewport_size({"width": w, "height": 900})
            page.wait_for_timeout(150)
            trig.hover()
            page.wait_for_timeout(500)
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(overflow <= 0, f"tooltip: no horizontal overflow (open) @ {w} (got {overflow})")
            bubble_inside_viewport(page, "tooltip", f"open @ {w}")
            page.keyboard.press("Escape")
            page.wait_for_timeout(120)
            page.mouse.move(2, 2)
        page.set_viewport_size({"width": 1280, "height": 900})
        close_all(page)

        # dark mode token flip (body + bubble) — open fresh in each theme so
        # the pointer never has to leave the trigger to reach the toggle
        trig.hover()
        page.wait_for_timeout(500)
        light_body = page.evaluate("getComputedStyle(document.body).backgroundColor")
        light_tip = page.evaluate("getComputedStyle(document.querySelector('[role=tooltip]')).backgroundColor")
        page.keyboard.press("Escape")
        page.mouse.move(2, 2)
        page.wait_for_timeout(150)
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(200)
        dark_body = page.evaluate("getComputedStyle(document.body).backgroundColor")
        trig.hover()
        page.wait_for_timeout(500)
        dark_tip = page.evaluate("getComputedStyle(document.querySelector('[role=tooltip]')).backgroundColor")
        check(light_body != dark_body, f"tooltip: dark-mode body token flip ({light_body} -> {dark_body})")
        check(light_tip != dark_tip, f"tooltip: dark-mode bubble token flip ({light_tip} -> {dark_tip})")
        page.keyboard.press("Escape")
        page.mouse.move(2, 2)
        page.wait_for_timeout(120)
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(120)

        # reduced motion: the fade transition is disabled
        page.emulate_media(reduced_motion="reduce")
        trig.hover()
        page.wait_for_timeout(500)
        tp = page.evaluate("getComputedStyle(document.querySelector('[role=tooltip]')).transitionProperty")
        check(tp == "none", f"tooltip: reduced-motion transition-none (got {tp})")
        page.emulate_media(reduced_motion="no-preference")
        close_all(page)
        page.close()

        # ---------------- tooltip-placement --------------------------------
        print("== tooltip-placement ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip-placement")
        for side in ("top", "right", "bottom", "left"):
            for align in ("start", "center", "end"):
                name = f"{side} · {align}"
                trig = page.get_by_role("button", name=name, exact=True)
                tip = hover_open(page, trig, "tooltip-placement", name)
                if tip.count() != 1:
                    continue
                check(f"side={side}" in tip.text_content() and f"align={align}" in tip.text_content(),
                      f"tooltip-placement: {name} content")
                tb, cb = trig.bounding_box(), tip.bounding_box()
                tol = 3
                if side == "top":
                    check(cb["y"] + cb["height"] <= tb["y"] + tol, f"tooltip-placement: {name} above trigger")
                elif side == "bottom":
                    check(cb["y"] >= tb["y"] + tb["height"] - tol, f"tooltip-placement: {name} below trigger")
                elif side == "left":
                    check(cb["x"] + cb["width"] <= tb["x"] + tol, f"tooltip-placement: {name} left of trigger")
                else:
                    check(cb["x"] >= tb["x"] + tb["width"] - tol, f"tooltip-placement: {name} right of trigger")
                if side in ("top", "bottom"):
                    if align == "start":
                        check(abs(cb["x"] - tb["x"]) <= tol, f"tooltip-placement: {name} align=start edges")
                    elif align == "end":
                        check(abs(cb["x"] + cb["width"] - tb["x"] - tb["width"]) <= tol,
                              f"tooltip-placement: {name} align=end edges")
                    else:
                        check(abs(cb["x"] + cb["width"] / 2 - tb["x"] - tb["width"] / 2) <= tol + 2,
                              f"tooltip-placement: {name} align=center centers")
                else:
                    if align == "start":
                        check(abs(cb["y"] - tb["y"]) <= tol, f"tooltip-placement: {name} align=start edges")
                    elif align == "end":
                        check(abs(cb["y"] + cb["height"] - tb["y"] - tb["height"]) <= tol,
                              f"tooltip-placement: {name} align=end edges")
                    else:
                        check(abs(cb["y"] + cb["height"] / 2 - tb["y"] - tb["height"] / 2) <= tol + 2,
                              f"tooltip-placement: {name} align=center centers")
                bubble_inside_viewport(page, "tooltip-placement", f"{name} @ 1280")
        # matrix containment at 375 (placement may flip/shift — never overflow)
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(150)
        for side, align in (("top", "start"), ("right", "center"), ("bottom", "end"), ("left", "center")):
            trig = page.get_by_role("button", name=f"{side} · {align}", exact=True)
            tip = hover_open(page, trig, "tooltip-placement", f"{side}/{align} @375")
            if tip.count() == 1:
                bubble_inside_viewport(page, "tooltip-placement", f"{side} · {align} @ 375")
        close_all(page)

        # edge flip: side=right fits at 1280, flips left at 375
        page.set_viewport_size({"width": 1280, "height": 900})
        page.wait_for_timeout(150)
        edge = page.get_by_role("button", name="Publish site")
        tip = hover_open(page, edge, "tooltip-placement", "edge @1280")
        tb, cb = edge.bounding_box(), tip.bounding_box()
        check(cb["x"] >= tb["x"] + tb["width"] - 3, "tooltip-placement: edge trigger keeps side=right @1280")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(150)
        tip = hover_open(page, edge, "tooltip-placement", "edge @375")
        tb, cb = edge.bounding_box(), tip.bounding_box()
        check(cb["x"] + cb["width"] <= tb["x"] + 3, "tooltip-placement: edge trigger flips right -> left @375")
        bubble_inside_viewport(page, "tooltip-placement", "edge flip @ 375")
        close_all(page)
        page.close()

        # ---------------- tooltip-with-icon --------------------------------
        print("== tooltip-with-icon ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip-with-icon")
        for label in ("Copy link", "Download report", "Share dashboard", "Report settings", "Delete report"):
            trig = page.get_by_role("button", name=label)
            check(trig.count() == 1, f"tooltip-with-icon: '{label}' trigger exists with accessible name")
            tip = hover_open(page, trig, "tooltip-with-icon", label)
            if tip.count() == 1:
                check(tip.text_content().strip() == label,
                      f"tooltip-with-icon: tooltip matches the aria-label ('{label}')")
        # keyboard: Tab through the toolbar opens each tooltip
        close_all(page)
        ok = tab_to(page, 'document.activeElement.getAttribute("aria-label") === "Copy link"',
                    "tooltip-with-icon: Tab reaches the toolbar")
        if ok:
            check(page.locator('[role="tooltip"]').count() == 1, "tooltip-with-icon: focus opens the icon tooltip")
            page.keyboard.press("Tab")
            page.wait_for_timeout(150)
            check(page.evaluate('document.activeElement.getAttribute("aria-label")') == "Download report",
                  "tooltip-with-icon: Tab moves to the next action")
            check(page.locator('[role="tooltip"]').count() == 1,
                  "tooltip-with-icon: next action's tooltip open after blur handoff")
        close_all(page)
        page.close()

        # ---------------- tooltip-with-long-content -------------------------
        print("== tooltip-with-long-content ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip-with-long-content")
        trig = page.get_by_role("button", name="About data residency")
        tip = hover_open(page, trig, "tooltip-with-long-content", "residency")
        cb = tip.bounding_box()
        check(150 < cb["width"] <= 258, f"tooltip-with-long-content: wrapped at the measure (got {cb['width']})")
        check(cb["height"] >= 60, f"tooltip-with-long-content: multi-line wrapping (got height {cb['height']})")
        bubble_inside_viewport(page, "tooltip-with-long-content", "residency")
        close_all(page)
        trig = page.get_by_role("button", name="What is included?")
        tip = hover_open(page, trig, "tooltip-with-long-content", "billing")
        cb = tip.bounding_box()
        check(150 < cb["width"] <= 258, f"tooltip-with-long-content: billing wrapped (got {cb['width']})")
        page.set_viewport_size({"width": 375, "height": 900})
        page.wait_for_timeout(150)
        tip = hover_open(page, trig, "tooltip-with-long-content", "billing @375")
        bubble_inside_viewport(page, "tooltip-with-long-content", "billing @ 375")
        close_all(page)
        page.set_viewport_size({"width": 1280, "height": 900})
        page.close()

        # ---------------- tooltip-rich-content ------------------------------
        print("== tooltip-rich-content ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip-rich-content")
        trig = page.get_by_role("button", name="Operational")
        tip = hover_open(page, trig, "tooltip-rich-content", "status")
        check("All systems operational" in tip.text_content(), "tooltip-rich-content: title row")
        check("Checked 2 minutes ago" in tip.text_content(), "tooltip-rich-content: metadata row")
        close_all(page)
        trig = page.get_by_role("button", name="Command palette")
        tip = hover_open(page, trig, "tooltip-rich-content", "command")
        check(tip.locator("kbd").count() == 1, "tooltip-rich-content: kbd chip rendered")
        check("⌘K" in tip.text_content(), "tooltip-rich-content: shortcut glyph")
        # nothing interactive inside the bubble
        check(tip.locator("a, button, input, select, textarea").count() == 0,
              "tooltip-rich-content: no interactive elements inside the tooltip")
        close_all(page)
        page.close()

        # ---------------- tooltip-disabled-trigger --------------------------
        print("== tooltip-disabled-trigger ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip-disabled-trigger")
        export_btn = page.get_by_role("button", name="Export CSV")
        check(export_btn.get_attribute("disabled") is not None, "tooltip-disabled-trigger: inner control natively disabled")
        wrapper = page.locator("span.cursor-not-allowed", has=export_btn).first
        check(wrapper.get_attribute("tabindex") == "0", "tooltip-disabled-trigger: wrapper is focusable (tabIndex=0)")
        tip = hover_open(page, wrapper, "tooltip-disabled-trigger", "wrapper hover")
        check("Team plan" in tip.text_content(), "tooltip-disabled-trigger: explanation on hover")
        close_all(page)
        ok = tab_to(page, 'document.activeElement.tagName === "SPAN" && document.activeElement.tabIndex === 0',
                    "tooltip-disabled-trigger: Tab reaches the wrapper")
        if ok:
            check(page.locator('[role="tooltip"]').count() == 1,
                  "tooltip-disabled-trigger: keyboard focus opens the explanation")
            style = page.evaluate("""() => {
              const cs = getComputedStyle(document.activeElement);
              return [cs.outlineWidth, cs.outlineStyle];
            }""")
            check(style[0] == "2px" and style[1] in ("auto", "solid"),
                  f"tooltip-disabled-trigger: focus-visible ring on wrapper (2px {style[1]})")
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)
        # the disabled prop suppresses hover + focus, and closes an open one
        delete_btn = page.get_by_role("button", name="Delete project")
        delete_btn.hover()
        page.wait_for_timeout(500)
        check(page.locator('[role="tooltip"]').count() == 1, "tooltip-disabled-trigger: hint opens while enabled")
        page.get_by_label("Enable action hints").uncheck()
        page.wait_for_timeout(200)
        check(page.locator('[role="tooltip"]').count() == 0,
              "tooltip-disabled-trigger: becoming disabled closes an open tooltip")
        page.mouse.move(2, 2)
        delete_btn.hover()
        page.wait_for_timeout(500)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip-disabled-trigger: disabled prop suppresses hover")
        delete_btn.focus()
        page.wait_for_timeout(150)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip-disabled-trigger: disabled prop suppresses focus")
        page.get_by_label("Enable action hints").check()
        page.wait_for_timeout(100)
        delete_btn.hover()
        page.wait_for_timeout(500)
        check(page.locator('[role="tooltip"]').count() == 1, "tooltip-disabled-trigger: re-enabling restores the hint")
        close_all(page)
        page.close()

        # ---------------- tooltip-controlled --------------------------------
        print("== tooltip-controlled ==")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        open_preview(page, "tooltip-controlled")
        copy_btn = page.get_by_role("button", name="Copy link")
        # hover requests are logged but the parent ignores them
        copy_btn.hover()
        page.wait_for_timeout(500)
        check(page.locator('[role="tooltip"]').count() == 0,
              "tooltip-controlled: parent ignores the hover request (fully controlled)")
        log = page.locator("p", has_text="onOpenChange log")
        check("open requested" in log.text_content(), "tooltip-controlled: hover request logged via onOpenChange")
        page.mouse.move(2, 2)
        page.wait_for_timeout(200)
        # click forces the confirmation open, then it auto-closes
        copy_btn.click()
        page.wait_for_timeout(200)
        tip = page.locator('[role="tooltip"]')
        check(tip.count() == 1 and "Copied to clipboard" in tip.text_content(),
              "tooltip-controlled: click forces the confirmation tooltip open")
        page.wait_for_timeout(1800)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip-controlled: confirmation auto-closes")
        # external toggle pins the hint open without hover/focus
        toggle = page.get_by_role("button", name="Show hint")
        toggle.click()
        page.wait_for_timeout(150)
        tip = page.locator('[role="tooltip"]')
        check(tip.count() == 1 and "reviewers" in tip.text_content(),
              "tooltip-controlled: external toggle opens the tooltip")
        page.get_by_role("button", name="Hide hint").click()
        page.wait_for_timeout(150)
        check(page.locator('[role="tooltip"]').count() == 0, "tooltip-controlled: external toggle closes the tooltip")
        close_all(page)
        page.close()

        browser.close()


def main():
    static_checks()
    browser_checks()
    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL PASSED")


if __name__ == "__main__":
    main()
