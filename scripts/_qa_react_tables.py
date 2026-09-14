#!/usr/bin/env python3
"""Playwright QA for the React Tables previews.

Verifies behavior-critical guarantees (not cosmetics):
  - every variant: renders, zero console errors, zero horizontal overflow at
    375/768/1280
  - static: exactly the 5 required files per variant, metadata schema, no
    `any` in code.tsx, no hardcoded hex, no inline style=, no
    component-specific CSS files
  - shared core: every derived code.tsx is identical to the reference except
    its header doc comment; TSX/JSX export sets + per-component prop
    signatures match
  - generator: `_gen_react_tables.py --check` reports no drift;
    `scripts/validate.py` passes
  - semantics: real table elements everywhere (table/caption/thead/tbody/
    tfoot/tr/th[scope=col]/td), no role=grid re-declaration, no div-based
    fake tables, no nested interactive elements
  - table: caption + totals footer derived from the row data, right-aligned
    tabular numeric columns
  - table-with-actions: real View link + Edit button, menu opens/closes,
    menuitem activates + focus restores, full menu keyboard model, bottom
    rows flip the menu upward
  - table-sortable: asc/desc/unsorted cycle actually reorders rows, aria-sort
    tracks the active column, keyboard sorting works
  - table-selectable: row selection, select-all, true .indeterminate IDL
    tri-state, selected count, disabled row excluded, bulk remove, keyboard
  - table-with-pagination: next/previous/numbered pages change the visible
    rows, boundary disabling, aria-current, page-size resets to page 1,
    aria-live range status
  - table-expandable: expand/collapse, aria-expanded + aria-controls wiring,
    multiple open rows, keyboard toggle, focus stays on the trigger
  - table-grouped: one tbody per group, th scope=rowgroup, collapse removes
    rows, aria-expanded toggles
  - table-compact: compact padding + 13px text, truncation with title, right
    alignment preserved
  - table-responsive: desktop table <-> mobile card list swap at 640px, the
    hidden presentation is display:none, cards keep every field
  - table-loading: aria-busy + skeleton rows + sr-only announcement, data
    returns, reduced-motion kills the pulse
  - table-empty: one real row (no fake rows), action creates a row, clear
    returns to empty
  - table-status: text+tint badges, real progressbar semantics, avatar
    aria-hidden, retry action works
  - table-with-header: sticky top-0 header cells, scope=col, capped vertical
    scroll region, header stays pinned while the body scrolls
  - table-with-footer: tfoot totals derive from the visible rows and
    recompute when the toolbar filter narrows the dataset, polite status
  - table-striped: token-based nth-child(even) striping, consistent across
    rows, reuses the header's subtle surface, hover still reads on top
  - table-hover: full-row hover surface shift, restores on pointer move,
    color-only transition
  - table-with-search: labelled type=search, live filtering, role=status
    count, honest empty state, Clear search restores the dataset
  - table-with-filters: two labelled selects compose (AND), Clear filters
    resets + self-disables, empty combination renders one real row
  - focus-visible 2px outline on controls
  - dark mode flips computed table surface + text colors
  - reduced motion kills transitions

Run from the repo root with a static server on :8765:

    python3 -m http.server 8765 &
    python3 scripts/_qa_react_tables.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/React/Components/Tables/"

VARIANTS = [
    "table", "table-with-actions", "table-sortable", "table-selectable",
    "table-with-pagination", "table-expandable", "table-grouped",
    "table-compact", "table-responsive", "table-loading", "table-empty",
    "table-status", "table-with-header", "table-with-footer",
    "table-striped", "table-hover", "table-with-search", "table-with-filters",
]

COMPONENT_EXPORTS = [
    "Table", "TableCaption", "TableHeader", "TableBody", "TableFooter",
    "TableRow", "TableHead", "TableCell", "TableEmpty", "TableLoading",
    "TableActions", "TableToolbar", "TablePagination", "TableSelection",
    "TableExpand",
]
HELPER_EXPORTS = ["sortRows", "useRowSelection", "clampPage", "pageRange"]
EXPORTS = COMPONENT_EXPORTS + HELPER_EXPORTS

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
        folder = ROOT / "React/Components/Tables" / slug
        files = sorted(p.name for p in folder.iterdir() if p.is_file())
        check(
            files == ["README.md", "code.jsx", "code.tsx", "metadata.json", "preview.html"],
            f"{slug}: exactly the 5 required files",
        )
        meta = json.loads((folder / "metadata.json").read_text())
        check(
            meta["technology"] == "react"
            and meta["type"] == "component"
            and meta["category"] == "Tables"
            and meta["styling"] == "Tailwind CSS"
            and meta["languages"] == ["JSX", "TSX"]
            and meta["framework"] == "React"
            and meta["language"] == "TSX"
            and meta["component"] == "table"
            and meta["family"] == "tables",
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
        check("<table" in tsx and "<thead" in tsx and "<tbody" in tsx,
              f"{slug}: real table elements in code.tsx")
        check('role="grid"' not in tsx and 'role="table"' not in tsx,
              f"{slug}: no ARIA grid/table re-declaration")
    css = list((ROOT / "React/Components/Tables").rglob("*.css"))
    check(css == [], "no component-specific CSS files in the family")
    # derived-code.tsx parity: identical shared core except the header comment
    reference = (ROOT / "React/Components/Tables/table/code.tsx").read_text()
    ref_body = re.sub(r"/\*\*.*?\*/", "", reference, count=1, flags=re.S)
    for slug in VARIANTS[1:]:
        tsx = (ROOT / "React/Components/Tables" / slug / "code.tsx").read_text()
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
        folder = ROOT / "React/Components/Tables" / slug
        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        te = sorted(set(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx)))
        m = re.search(r"export \{ ([^}]*) \};", jsx)
        je = sorted(x.strip() for x in m.group(1).split(",")) if m else []
        check(te == je == sorted(EXPORTS), f"{slug}: TSX/JSX named-export parity")
        check("export default Table;" in jsx, f"{slug}: JSX default export = Table")
        for name in COMPONENT_EXPORTS:
            tp = _props_of(tsx, name)
            jp = _props_of(jsx, name)
            check(tp is not None and tp == jp, f"{slug}: {name} prop-signature parity")


def generator_checks():
    print("== generator + repo validation ==")
    r = subprocess.run(
        [sys.executable, "_gen_react_tables.py", "--check"],
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
    rendered = page.evaluate("document.querySelectorAll('#ds-root table').length")
    check(rendered >= 1, f"{slug}: a real <table> renders")
    for w in (375, 768, 1280):
        check(overflow(page, w) == 0, f"{slug}: no horizontal overflow at {w}px")
    check(errs == [], f"{slug}: zero console errors")


def semantics_checks(page):
    print("== table semantics ==")
    for slug in VARIANTS:
        open_preview(page, slug)
        info = page.evaluate(
            """(() => {
              const root = document.getElementById('ds-root');
              const table = root.querySelector('table');
              return {
                caption: table.querySelector('caption') !== null,
                thead: table.querySelector('thead') !== null,
                tbody: table.querySelector('tbody') !== null,
                scopedHeaders: table.querySelectorAll('th[scope]').length,
                gridRoles: root.querySelectorAll('[role="grid"], [role="table"], [role="row"], [role="cell"]').length,
                divTables: root.querySelectorAll('div > [role="rowgroup"]').length,
              };
            })()"""
        )
        check(info["caption"], f"{slug}: <caption> present")
        check(info["thead"] and info["tbody"], f"{slug}: thead + tbody present")
        check(info["scopedHeaders"] > 0, f"{slug}: th elements carry scope")
        check(info["gridRoles"] == 0 and info["divTables"] == 0,
              f"{slug}: no ARIA-grid re-declaration / div-based fake table")
        bad = page.evaluate(
            """(() => {
              const controls = Array.from(document.querySelectorAll('#ds-root table button, #ds-root table a, #ds-root table input, #ds-root table select'));
              return controls.filter(c => c.querySelector('button, a, input, select') !== null).length;
            })()"""
        )
        check(bad == 0, f"{slug}: no nested interactive elements")


def reference_checks(page):
    print("== table (reference) ==")
    open_preview(page, "table")
    caption = page.evaluate("document.querySelector('#ds-root caption').textContent")
    check("Invoices for the 2026 billing year" in caption, "table: caption names the dataset")
    check(page.evaluate("document.querySelectorAll('#ds-root tfoot').length") == 1,
          "table: tfoot present")
    totals = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root tfoot td')).map(td => td.textContent.trim())"
    )
    check(totals == ["Total", "$7,265.00", "$172.50"],
          f"table: footer totals derive from the row data (got {totals})")
    align = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td:nth-child(3)')).textAlign"
    )
    check(align == "right", f"table: numeric column is right-aligned (got {align})")
    fvn = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td:nth-child(3)')).fontVariantNumeric"
    )
    check("tabular-nums" in fvn, f"table: numeric column uses tabular figures (got {fvn})")
    rows = page.evaluate("document.querySelectorAll('#ds-root tbody tr').length")
    check(rows == 6, f"table: 6 invoice rows (got {rows})")


def actions_checks(page):
    print("== table-with-actions ==")
    open_preview(page, "table-with-actions")
    href = page.evaluate("document.querySelector('#ds-root tbody tr td a').getAttribute('href')")
    check(href == "#/tokens/tok_1", f"table-with-actions: View is a real link (href {href})")
    page.click("#ds-root button[aria-label='Edit CI deploy key']")
    log = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("Editing CI deploy key." in log, "table-with-actions: Edit button fires its action")
    # menu: click opens, item activates, focus restores
    trigger = "#ds-root button[aria-label='More actions for CI deploy key']"
    page.click(trigger)
    page.wait_for_timeout(150)
    check(page.evaluate(f"document.querySelector(\"{trigger}\").getAttribute('aria-expanded')") == "true",
          "table-with-actions: trigger aria-expanded=true while open")
    items = page.evaluate("document.querySelectorAll('#ds-root [role=\"menu\"] [role=\"menuitem\"]').length")
    check(items == 3, f"table-with-actions: menu renders 3 real menuitems (got {items})")
    page.click("#ds-root [role='menu'] [role='menuitem']:has-text('Duplicate')")
    page.wait_for_timeout(150)
    log = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("Duplicated CI deploy key." in log, "table-with-actions: menuitem activates its action")
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"menu\"]').length") == 0,
          "table-with-actions: menu closes after selection")
    refocused = page.evaluate(f"document.activeElement === document.querySelector(\"{trigger}\")")
    check(refocused, "table-with-actions: focus restores to the trigger after selection")
    # keyboard model: ArrowDown opens + focuses first item, arrows cycle, Escape closes + refocuses
    page.locator(trigger).focus()
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(150)
    first_focused = page.evaluate(
        "document.activeElement && document.activeElement.getAttribute('role') === 'menuitem' && document.activeElement.textContent === 'Duplicate'"
    )
    check(first_focused, "table-with-actions: ArrowDown opens the menu and focuses the first item")
    page.keyboard.press("ArrowDown")
    second = page.evaluate("document.activeElement.textContent")
    check(second == "Rotate token", f"table-with-actions: arrows cycle menu items (got {second!r})")
    page.keyboard.press("ArrowUp")
    back = page.evaluate("document.activeElement.textContent")
    check(back == "Duplicate", "table-with-actions: ArrowUp cycles back")
    page.keyboard.press("End")
    last = page.evaluate("document.activeElement.textContent")
    check(last == "Revoke", "table-with-actions: End jumps to the last item")
    page.keyboard.press("Escape")
    page.wait_for_timeout(150)
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"menu\"]').length") == 0,
          "table-with-actions: Escape closes the menu")
    check(page.evaluate(f"document.activeElement === document.querySelector(\"{trigger}\")"),
          "table-with-actions: Escape restores focus to the trigger")
    # bottom rows flip the menu upward so it is never clipped by the container
    last_trigger = "#ds-root button[aria-label='More actions for Legacy importer']"
    page.click(last_trigger)
    page.wait_for_timeout(150)
    menu_cls = page.evaluate("document.querySelector('#ds-root [role=\"menu\"]').className")
    check("bottom-full" in menu_cls, "table-with-actions: last-row menu opens upward")
    # outside pointer closes
    page.click("#ds-root")
    page.wait_for_timeout(150)
    check(page.evaluate("document.querySelectorAll('#ds-root [role=\"menu\"]').length") == 0,
          "table-with-actions: outside pointer-down closes the menu")


def sorting_checks(page):
    print("== table-sortable ==")
    open_preview(page, "table-sortable")
    sorts = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root th[aria-sort]')).map(th => th.getAttribute('aria-sort'))"
    )
    check(sorts == ["none", "none", "none", "none"],
          f"table-sortable: all sortable headers start aria-sort=none (got {sorts})")
    second_service = "document.querySelectorAll('#ds-root tbody tr')[1].querySelector('td').textContent"
    check(page.evaluate(second_service) == "billing-service",
          "table-sortable: initial order is the original data order")
    page.click("#ds-root th button:has-text('Service')")
    page.wait_for_timeout(150)
    check(page.evaluate(second_service) == "auth-service",
          "table-sortable: first click sorts ascending (real reorder)")
    active = page.evaluate("document.querySelector('#ds-root th[aria-sort=\"ascending\"] button').textContent")
    check("Service" in active, "table-sortable: aria-sort=ascending lands on the active column")
    page.click("#ds-root th button:has-text('Service')")
    page.wait_for_timeout(150)
    first_service = "document.querySelector('#ds-root tbody tr td').textContent"
    check(page.evaluate(first_service) == "search-indexer",
          "table-sortable: second click sorts descending")
    check(page.evaluate("document.querySelectorAll('#ds-root th[aria-sort=\"descending\"]').length") == 1,
          "table-sortable: aria-sort=descending on the active column")
    page.click("#ds-root th button:has-text('Service')")
    page.wait_for_timeout(150)
    check(page.evaluate(second_service) == "billing-service",
          "table-sortable: third click restores the original order (real reset)")
    check(page.evaluate("document.querySelectorAll('#ds-root th[aria-sort=\"none\"]').length") == 4,
          "table-sortable: unsorted reset returns every header to aria-sort=none")
    # numeric column sorts numerically (34 < 61 < 77 …), not lexicographically
    page.click("#ds-root th button:has-text('Duration')")
    page.wait_for_timeout(150)
    first_duration = page.evaluate(
        "document.querySelector('#ds-root tbody tr td:nth-child(3)').textContent"
    )
    check(first_duration == "34s", f"table-sortable: numeric column sorts numerically (got {first_duration})")
    # keyboard sorting: focus the Region sort button and press Enter
    page.locator("#ds-root th button:has-text('Region')").focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(150)
    first_region = page.evaluate(
        "document.querySelector('#ds-root tbody tr td:nth-child(2)').textContent"
    )
    check(first_region == "ap-south-1",
          f"table-sortable: Enter on a focused sort button sorts (got {first_region})")
    status = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("Sorted by Region (ascending)." in status,
          "table-sortable: sort state is announced in the live region")


def selection_checks(page):
    print("== table-selectable ==")
    open_preview(page, "table-selectable")
    header_box = "#ds-root thead input[aria-label='Select all members']"
    state = page.evaluate(
        f"""(() => {{
          const box = document.querySelector("{header_box}");
          return {{ checked: box.checked, indeterminate: box.indeterminate }};
        }})()"""
    )
    check(state == {"checked": False, "indeterminate": False},
          "table-selectable: header checkbox starts unchecked + not indeterminate")
    ada = "#ds-root input[aria-label='Select Ada Lovelace']"
    page.click(ada)
    page.wait_for_timeout(150)
    state = page.evaluate(
        f"""(() => {{
          const box = document.querySelector("{header_box}");
          return {{ checked: box.checked, indeterminate: box.indeterminate }};
        }})()"""
    )
    check(state == {"checked": False, "indeterminate": True},
          "table-selectable: one row selected -> header shows the true indeterminate IDL state")
    count = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("1 of 5 selected" in count, f"table-selectable: live selected count (got {count!r})")
    selected = page.evaluate(
        "document.querySelector('#ds-root tbody tr[aria-selected=\"true\"] td:nth-child(2)').textContent"
    )
    check("Ada Lovelace" in selected, "table-selectable: selected row carries aria-selected=true")
    # select-all
    page.click(header_box)
    page.wait_for_timeout(150)
    state = page.evaluate(
        f"""(() => {{
          const box = document.querySelector("{header_box}");
          const rows = Array.from(document.querySelectorAll('#ds-root tbody input[type="checkbox"]'));
          return {{
            checked: box.checked,
            indeterminate: box.indeterminate,
            rowStates: rows.map(r => ({{ checked: r.checked, disabled: r.disabled }})),
          }};
        }})()"""
    )
    check(state["checked"] and not state["indeterminate"],
          "table-selectable: select-all checks the header checkbox (no indeterminate)")
    check(all(r["checked"] for r in state["rowStates"] if not r["disabled"]),
          "table-selectable: select-all selects every enabled row")
    suspended = [r for r in state["rowStates"] if r["disabled"]]
    check(len(suspended) == 1 and not suspended[0]["checked"],
          "table-selectable: the suspended row stays disabled + unselected")
    count = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("5 of 5 selected" in count, "table-selectable: count reads 5 of 5 (disabled row excluded)")
    # clear all via header
    page.click(header_box)
    page.wait_for_timeout(150)
    count = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("0 of 5 selected" in count, "table-selectable: header toggle clears all rows")
    # keyboard: Space toggles a row checkbox
    page.locator(ada).focus()
    page.keyboard.press("Space")
    page.wait_for_timeout(150)
    check(page.evaluate(f"document.querySelector(\"{ada}\").checked"),
          "table-selectable: Space toggles a row checkbox from the keyboard")
    # bulk remove genuinely removes rows
    page.click("#ds-root input[aria-label='Select Grace Hopper']")
    page.wait_for_timeout(100)
    page.click("#ds-root button:has-text('Remove selected')")
    page.wait_for_timeout(150)
    rows = page.evaluate("document.querySelectorAll('#ds-root tbody tr').length")
    count = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check(rows == 4, f"table-selectable: Remove selected removes the rows (got {rows} rows)")
    check("0 of 3 selected" in count,
          f"table-selectable: count recomputes against the remaining selectable rows (got {count!r})")


def pagination_checks(page):
    print("== table-with-pagination ==")
    open_preview(page, "table-with-pagination")
    status = "document.querySelector('#ds-root nav p').textContent"
    check("1" in page.evaluate(status) and "8" in page.evaluate(status) and "42" in page.evaluate(status),
          f"table-with-pagination: initial range status (got {page.evaluate(status)!r})")
    check(page.evaluate("document.querySelector('#ds-root button[aria-label=\"Go to previous page\"]').disabled"),
          "table-with-pagination: Previous is natively disabled on page 1")
    first_event = "document.querySelector('#ds-root tbody tr td').textContent"
    check(page.evaluate(first_event) == "evt_1000", "table-with-pagination: page 1 shows the first events")
    page.click("#ds-root button[aria-label='Go to next page']")
    page.wait_for_timeout(150)
    check(page.evaluate(first_event) == "evt_1008",
          "table-with-pagination: Next changes the visible rows")
    check(page.evaluate(status).replace("–", "-").find("9") >= 0,
          "table-with-pagination: range status advances")
    current = page.evaluate(
        "document.querySelector('#ds-root nav [aria-current=\"page\"]').textContent"
    )
    check(current == "2", f"table-with-pagination: aria-current=page tracks the page (got {current})")
    check(not page.evaluate("document.querySelector('#ds-root button[aria-label=\"Go to previous page\"]').disabled"),
          "table-with-pagination: Previous enables after leaving page 1")
    # numbered page button
    page.click("#ds-root nav button[aria-label='Go to page 6']")
    page.wait_for_timeout(150)
    check(page.evaluate(first_event) == "evt_1040",
          "table-with-pagination: numbered page button jumps to the page")
    check(page.evaluate("document.querySelector('#ds-root button[aria-label=\"Go to next page\"]').disabled"),
          "table-with-pagination: Next is natively disabled on the last page")
    last_status = page.evaluate(status)
    check("42" in last_status and "41" in last_status,
          f"table-with-pagination: last page shows the final partial range (got {last_status!r})")
    # keyboard: Enter on Previous
    page.locator("#ds-root button[aria-label='Go to previous page']").focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(150)
    check(page.evaluate(first_event) == "evt_1032",
          "table-with-pagination: keyboard activation changes the page")
    # page size: changing it resets to page 1 and re-slices
    page.select_option("#ds-root nav select", "20")
    page.wait_for_timeout(150)
    rows = page.evaluate("document.querySelectorAll('#ds-root tbody tr').length")
    check(rows == 20, f"table-with-pagination: page-size select changes the visible row count (got {rows})")
    check(page.evaluate("document.querySelector('#ds-root nav [aria-current=\"page\"]').textContent") == "1",
          "table-with-pagination: page-size change resets to page 1")
    check(page.evaluate("document.querySelectorAll('#ds-root nav ul li button[aria-label^=\"Go to page\"]').length") == 2,
          "table-with-pagination: page list re-windows for the new page count")


def expansion_checks(page):
    print("== table-expandable ==")
    open_preview(page, "table-expandable")
    # the trigger's aria-label flips Expand/Collapse with state, so select by
    # the stable aria-controls wiring instead
    trig = "#ds-root button[aria-controls='order-ORD-5201-details']"
    check(page.evaluate(f"document.querySelector(\"{trig}\").getAttribute('aria-expanded')") == "false",
          "table-expandable: trigger starts aria-expanded=false")
    check(page.evaluate(f"document.querySelector(\"{trig}\").getAttribute('aria-label')") == "Expand details for order ORD-5201",
          "table-expandable: trigger accessible name describes the action + target")
    page.click(trig)
    page.wait_for_timeout(150)
    check(page.evaluate(f"document.querySelector(\"{trig}\").getAttribute('aria-expanded')") == "true",
          "table-expandable: click sets aria-expanded=true")
    wiring = page.evaluate(
        f"""(() => {{
          const t = document.querySelector("{trig}");
          const panel = document.getElementById(t.getAttribute('aria-controls'));
          return {{ controls: t.getAttribute('aria-controls'), found: panel !== null,
                   text: panel ? panel.textContent.slice(0, 40) : null }};
        }})()"""
    )
    check(wiring["found"] and wiring["controls"] == "order-ORD-5201-details",
          "table-expandable: aria-controls points at the rendered panel")
    check("Desk lamp" in wiring["text"], "table-expandable: panel shows the order's line items")
    # multiple rows open at once
    trig2 = "#ds-root button[aria-controls='order-ORD-5203-details']"
    page.click(trig2)
    page.wait_for_timeout(150)
    open_panels = page.evaluate("document.querySelectorAll('#ds-root [aria-expanded=\"true\"]').length")
    check(open_panels == 2, f"table-expandable: multiple rows can be open (got {open_panels})")
    # keyboard toggle + focus stays on the trigger
    page.locator(trig).focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(150)
    check(page.evaluate(f"document.querySelector(\"{trig}\").getAttribute('aria-expanded')") == "false",
          "table-expandable: Enter collapses the row from the keyboard")
    check(page.evaluate(f"document.activeElement === document.querySelector(\"{trig}\")"),
          "table-expandable: focus stays on the trigger after toggling")
    check(page.evaluate("document.getElementById('order-ORD-5201-details') === null"),
          "table-expandable: collapsed panel is removed from the DOM")


def grouped_checks(page):
    print("== table-grouped ==")
    open_preview(page, "table-grouped")
    bodies = page.evaluate("document.querySelectorAll('#ds-root tbody').length")
    check(bodies == 3, f"table-grouped: one tbody per group (got {bodies})")
    scopes = page.evaluate("document.querySelectorAll('#ds-root th[scope=\"rowgroup\"]').length")
    check(scopes == 3, f"table-grouped: th scope=rowgroup per group (got {scopes})")
    labels = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root th[scope=\"rowgroup\"]')).map(th => th.textContent.replace(/\\s+/g, ' ').trim().slice(0, 20))"
    )
    check(any("Engineering" in l for l in labels) and any("Design" in l for l in labels) and any("Operations" in l for l in labels),
          f"table-grouped: group headers label the departments (got {labels})")
    eng_rows = "document.querySelectorAll('#ds-root tbody#group-engineering-rows tr').length"
    check(page.evaluate(eng_rows) == 4, "table-grouped: Engineering renders its header + 3 members")
    page.click("#ds-root button[aria-label='Collapse Engineering group']")
    page.wait_for_timeout(150)
    check(page.evaluate(eng_rows) == 1, "table-grouped: collapsing removes the member rows")
    expanded = page.evaluate(
        "document.querySelector('#ds-root button[aria-label=\"Expand Engineering group\"]') !== null"
    )
    check(expanded, "table-grouped: the toggle now offers to expand (aria-expanded=false)")
    controls = page.evaluate(
        "document.querySelector('#ds-root button[aria-label=\"Expand Engineering group\"]').getAttribute('aria-controls')"
    )
    check(controls == "group-engineering-rows",
          "table-grouped: aria-controls points at the group tbody id")
    page.click("#ds-root button[aria-label='Expand Engineering group']")
    page.wait_for_timeout(150)
    check(page.evaluate(eng_rows) == 4, "table-grouped: expanding restores the member rows")


def compact_checks(page):
    print("== table-compact ==")
    open_preview(page, "table-compact")
    padding = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td')).paddingTop"
    )
    check(padding == "6px", f"table-compact: compact cell padding applied (got {padding})")
    size = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td')).fontSize"
    )
    check(size == "13px", f"table-compact: compact text size applied (got {size})")
    rows = page.evaluate("document.querySelectorAll('#ds-root tbody tr').length")
    check(rows == 12, f"table-compact: 12 dense rows render (got {rows})")
    trunc = page.evaluate(
        """(() => {
          const el = document.querySelector('#ds-root tbody tr:nth-child(3) td span');
          return { cls: el.className.includes('truncate'), title: el.getAttribute('title') };
        })()"""
    )
    check(trunc["cls"] and trunc["title"] == "/v1/workspaces/{workspaceId}/deployments/{deploymentId}/logs/stream",
          "table-compact: long values truncate with the full value in title")
    align = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td:nth-child(5)')).textAlign"
    )
    check(align == "right", "table-compact: numeric columns stay right-aligned")


def responsive_checks(page):
    print("== table-responsive ==")
    open_preview(page, "table-responsive", width=1280)
    desktop = page.evaluate(
        """(() => {
          const wrap = document.querySelector('#ds-root div.hidden');
          const cards = document.querySelector('#ds-root ul');
          return { tableVisible: getComputedStyle(wrap).display !== 'none',
                   cardsVisible: getComputedStyle(cards).display !== 'none' };
        })()"""
    )
    check(desktop["tableVisible"] and not desktop["cardsVisible"],
          "table-responsive: desktop shows the table, cards are display:none")
    page.set_viewport_size({"width": 375, "height": 900})
    page.wait_for_timeout(200)
    mobile = page.evaluate(
        """(() => {
          const wrap = document.querySelector('#ds-root div.hidden');
          const cards = document.querySelector('#ds-root ul');
          return { tableVisible: getComputedStyle(wrap).display !== 'none',
                   cardsVisible: getComputedStyle(cards).display !== 'none',
                   cardCount: cards.querySelectorAll('li').length,
                   text: cards.textContent };
        })()"""
    )
    check(not mobile["tableVisible"] and mobile["cardsVisible"],
          "table-responsive: mobile shows the card list, table is display:none")
    check(mobile["cardCount"] == 4, f"table-responsive: every project becomes a card (got {mobile['cardCount']})")
    check("Atlas Analytics" in mobile["text"] and "Owner" in mobile["text"] and "$12,400.00" in mobile["text"],
          "table-responsive: cards keep every field (name, label/value pairs, budget)")
    check(overflow(page, 375) == 0, "table-responsive: no horizontal overflow at 375px in card mode")
    page.set_viewport_size({"width": 768, "height": 900})
    page.wait_for_timeout(200)
    check(page.evaluate("getComputedStyle(document.querySelector('#ds-root div.hidden')).display") != "none",
          "table-responsive: 768px is back to the table presentation")


def loading_checks(page, browser):
    print("== table-loading ==")
    open_preview(page, "table-loading")
    check(page.evaluate("document.querySelector('#ds-root table').getAttribute('aria-busy')") is None,
          "table-loading: no aria-busy while idle")
    check(page.evaluate("document.querySelectorAll('#ds-root tbody tr').length") == 5,
          "table-loading: data rows render initially")
    page.click("#ds-root button:has-text('Reload')")
    page.wait_for_timeout(200)
    check(page.evaluate("document.querySelector('#ds-root table').getAttribute('aria-busy')") == "true",
          "table-loading: aria-busy=true while loading")
    skeleton = page.evaluate(
        """(() => {
          const rows = Array.from(document.querySelectorAll('#ds-root tbody tr[aria-hidden="true"]'));
          const sr = document.querySelector('#ds-root tbody tr.sr-only td');
          return { skeletonRows: rows.length, announcement: sr ? sr.textContent : null };
        })()"""
    )
    check(skeleton["skeletonRows"] == 5, f"table-loading: skeleton rows render (got {skeleton['skeletonRows']})")
    check(skeleton["announcement"] == "Loading data",
          "table-loading: visually hidden announcement while loading")
    check(page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root button')).find(b => b.textContent === 'Loading…').disabled"
    ), "table-loading: Reload disables while loading (no double-fire)")
    page.wait_for_timeout(1600)
    check(page.evaluate("document.querySelector('#ds-root table').getAttribute('aria-busy')") is None,
          "table-loading: aria-busy clears when data returns")
    check(page.evaluate("document.querySelectorAll('#ds-root tbody tr').length") == 5,
          "table-loading: real data rows return after the load")
    # reduced motion kills the skeleton pulse
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, "table-loading")
    p.click("#ds-root button:has-text('Reload')")
    p.wait_for_timeout(200)
    anim = p.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr[aria-hidden=\"true\"] td span')).animationName"
    )
    check(anim == "none", f"table-loading: reduced motion disables the skeleton pulse (got {anim})")
    context.close()


def empty_checks(page):
    print("== table-empty ==")
    open_preview(page, "table-empty")
    rows = page.evaluate("document.querySelectorAll('#ds-root tbody tr').length")
    check(rows == 1, f"table-empty: exactly one real row (no fake placeholder rows, got {rows})")
    check(page.evaluate("document.querySelectorAll('#ds-root tbody td').length") == 1,
          "table-empty: the empty state is a single spanning cell")
    title = page.evaluate("document.querySelector('#ds-root tbody td p').textContent")
    check(title == "No saved views", f"table-empty: zero-data message renders (got {title!r})")
    page.click("#ds-root button:has-text('Create a view')")
    page.wait_for_timeout(150)
    rows = page.evaluate("document.querySelectorAll('#ds-root tbody tr').length")
    check(rows == 1 and "Untitled view 1" in page.evaluate("document.querySelector('#ds-root tbody').textContent"),
          "table-empty: the action genuinely creates a row")
    note = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("1 saved view." in note, f"table-empty: toolbar count updates (got {note!r})")
    page.click("#ds-root button:has-text('Clear all')")
    page.wait_for_timeout(150)
    check(page.evaluate("document.querySelector('#ds-root tbody td p').textContent") == "No saved views",
          "table-empty: Clear all returns to the empty state")


def status_checks(page):
    print("== table-status ==")
    open_preview(page, "table-status")
    badges = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root tbody tr td:nth-child(2) > span')).map(b => b.textContent.trim())"
    )
    check(sorted(set(badges)) == ["Complete", "Failed", "Queued", "Running"],
          f"table-status: four semantic statuses render as text (got {sorted(set(badges))})")
    prog = page.evaluate(
        """(() => {
          const bar = document.querySelector('#ds-root [role="progressbar"]');
          return { now: bar.getAttribute('aria-valuenow'), min: bar.getAttribute('aria-valuemin'),
                   max: bar.getAttribute('aria-valuemax'), label: bar.getAttribute('aria-label') };
        })()"""
    )
    check(prog == {"now": "45", "min": "0", "max": "100", "label": "Rollout of api-gateway"},
          f"table-status: progressbar exposes real values (got {prog})")
    avatar_hidden = page.evaluate(
        "document.querySelector('#ds-root tbody tr td:nth-child(3) span').getAttribute('aria-hidden') === 'true'"
    )
    check(avatar_hidden, "table-status: avatar initials are aria-hidden (the name is the content)")
    duration = page.evaluate(
        "document.querySelector('#ds-root tbody tr td:nth-child(5)').textContent"
    )
    check(duration == "3m 32s", f"table-status: duration formats realistically (got {duration!r})")
    page.click("#ds-root button[aria-label='Retry api-gateway']")
    page.wait_for_timeout(150)
    log = page.evaluate("document.querySelector('#ds-root [aria-live]').textContent")
    check("Retried api-gateway." in log, "table-status: row action fires")
    dot = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td:nth-child(2) span span')).backgroundColor"
    )
    text = page.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr td:nth-child(2) > span')).color"
    )
    check(dot == text, "table-status: badge dot + text share the semantic token color")


def header_checks(page):
    print("== table-with-header ==")
    open_preview(page, "table-with-header")
    info = page.evaluate(
        """(() => {
          const th = document.querySelector('#ds-root thead th');
          const cs = getComputedStyle(th);
          const container = document.querySelector('#ds-root table').parentElement;
          return {
            position: cs.position, top: cs.top,
            scope: th.getAttribute('scope'),
            scopedCount: document.querySelectorAll('#ds-root thead th[scope="col"]').length,
            containerMaxH: getComputedStyle(container).maxHeight,
            containerOverflowY: getComputedStyle(container).overflowY,
            thBg: cs.backgroundColor,
            rows: document.querySelectorAll('#ds-root tbody tr').length,
          };
        })()"""
    )
    check(info["position"] == "sticky" and info["top"] == "0px",
          f"table-with-header: header cells are sticky top-0 (got {info['position']} {info['top']})")
    check(info["scope"] == "col" and info["scopedCount"] == 4,
          f"table-with-header: every header is th scope=col (got {info['scopedCount']})")
    check(info["containerMaxH"] == "288px" and info["containerOverflowY"] == "auto",
          f"table-with-header: container is a capped vertical scroll region (got {info['containerMaxH']} / {info['containerOverflowY']})")
    check(info["thBg"] != "rgba(0, 0, 0, 0)" and info["thBg"] != "transparent",
          "table-with-header: pinned header keeps an opaque surface")
    check(info["rows"] == 16, f"table-with-header: 16 release rows render (got {info['rows']})")
    pin = page.evaluate(
        """(() => {
          const container = document.querySelector('#ds-root table').parentElement;
          container.scrollTop = 400;
          const th = document.querySelector('#ds-root thead th');
          const cr = container.getBoundingClientRect();
          const hr = th.getBoundingClientRect();
          return { delta: Math.abs(hr.top - cr.top), visible: hr.bottom > cr.top };
        })()"""
    )
    check(pin["delta"] <= 2 and pin["visible"],
          f"table-with-header: header stays pinned at the container top while scrolled (delta {pin['delta']}px)")


def footer_checks(page):
    print("== table-with-footer ==")
    open_preview(page, "table-with-footer")
    totals = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root tfoot td')).map(td => td.textContent.trim())"
    )
    check(totals == ["Total — 6 invoices", "$12,260.00"],
          f"table-with-footer: initial footer totals derive from all rows (got {totals})")
    status = page.evaluate(
        """(() => {
          const el = document.querySelector('#ds-root [aria-live]');
          return { text: el.textContent, live: el.getAttribute('aria-live') };
        })()"""
    )
    check(status["text"] == "Showing 6 of 6 invoices" and status["live"] == "polite",
          f"table-with-footer: polite result status (got '{status['text']}')")
    page.select_option("#ds-root select[aria-label='Filter invoices by status']", "open")
    page.wait_for_timeout(150)
    open_state = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          totals: Array.from(document.querySelectorAll('#ds-root tfoot td')).map(td => td.textContent.trim()),
          status: document.querySelector('#ds-root [aria-live]').textContent,
        }))()"""
    )
    check(open_state["rows"] == 3, f"table-with-footer: Open only narrows to 3 rows (got {open_state['rows']})")
    check(open_state["totals"] == ["Total — 3 invoices", "$3,050.00"],
          f"table-with-footer: footer recomputes from the visible rows (got {open_state['totals']})")
    check(open_state["status"] == "Showing 3 of 6 invoices",
          f"table-with-footer: status announces the filtered count (got '{open_state['status']}')")
    page.select_option("#ds-root select[aria-label='Filter invoices by status']", "paid")
    page.wait_for_timeout(150)
    paid_total = page.evaluate(
        "document.querySelector('#ds-root tfoot td:last-child').textContent.trim()"
    )
    check(paid_total == "$9,210.00", f"table-with-footer: Paid only recomputes to $9,210.00 (got {paid_total})")
    page.select_option("#ds-root select[aria-label='Filter invoices by status']", "all")
    page.wait_for_timeout(150)
    check(page.evaluate("document.querySelectorAll('#ds-root tbody tr').length") == 6,
          "table-with-footer: clearing the filter restores all 6 rows")


def striped_checks(page):
    print("== table-striped ==")
    open_preview(page, "table-striped")
    bg = page.evaluate(
        """(() => {
          const rows = document.querySelectorAll('#ds-root tbody tr');
          return {
            odd: getComputedStyle(rows[0]).backgroundColor,
            even: getComputedStyle(rows[1]).backgroundColor,
            even2: getComputedStyle(rows[3]).backgroundColor,
            headBg: getComputedStyle(document.querySelector('#ds-root thead')).backgroundColor,
            rows: rows.length,
          };
        })()"""
    )
    check(bg["rows"] == 8, f"table-striped: 8 product rows render (got {bg['rows']})")
    check(bg["odd"] != bg["even"], "table-striped: even rows differ from odd rows")
    check(bg["even"] == bg["even2"], "table-striped: striping is consistent across even rows")
    check(bg["even"] == bg["headBg"], "table-striped: stripe reuses the header's subtle surface token")
    before = page.evaluate("getComputedStyle(document.querySelectorAll('#ds-root tbody tr')[2]).backgroundColor")
    page.hover("#ds-root tbody tr:nth-child(3)")
    page.wait_for_timeout(250)
    after = page.evaluate("getComputedStyle(document.querySelectorAll('#ds-root tbody tr')[2]).backgroundColor")
    check(before != after, "table-striped: hover affordance still reads over the stripe")


def hover_checks(page):
    print("== table-hover ==")
    open_preview(page, "table-hover")
    base = page.evaluate(
        """(() => {
          const rows = document.querySelectorAll('#ds-root tbody tr');
          return { r1: getComputedStyle(rows[0]).backgroundColor, r2: getComputedStyle(rows[1]).backgroundColor };
        })()"""
    )
    check(base["r1"] == base["r2"], "table-hover: resting rows share the base surface (no striping)")
    page.hover("#ds-root tbody tr:nth-child(2)")
    page.wait_for_timeout(250)
    hovered = page.evaluate("getComputedStyle(document.querySelectorAll('#ds-root tbody tr')[1]).backgroundColor")
    check(hovered != base["r2"], "table-hover: hovered row shifts to the hover surface")
    page.hover("#ds-root tbody tr:nth-child(3)")
    page.wait_for_timeout(250)
    moved = page.evaluate(
        """(() => {
          const rows = document.querySelectorAll('#ds-root tbody tr');
          return { prev: getComputedStyle(rows[1]).backgroundColor, now: getComputedStyle(rows[2]).backgroundColor };
        })()"""
    )
    check(moved["prev"] == base["r2"] and moved["now"] != base["r2"],
          "table-hover: hover tracks the pointer and restores the previous row")
    transition = page.evaluate("getComputedStyle(document.querySelector('#ds-root tbody tr')).transitionProperty")
    check("background-color" in transition, f"table-hover: hover shift is a color transition (got {transition})")


def search_checks(page):
    print("== table-with-search ==")
    open_preview(page, "table-with-search")
    label = page.evaluate(
        """(() => {
          const input = document.getElementById('user-search');
          const label = document.querySelector('label[for="user-search"]');
          const status = document.querySelector('#ds-root [role="status"]');
          return {
            labelled: label !== null && label.contains(input),
            type: input.getAttribute('type'),
            statusText: status.textContent,
          };
        })()"""
    )
    check(label["labelled"] and label["type"] == "search",
          "table-with-search: search input is a labelled native type=search")
    check(label["statusText"] == "8 of 8 users",
          f"table-with-search: role=status announces the full count (got '{label['statusText']}')")
    check(page.evaluate("document.querySelectorAll('#ds-root tbody tr').length") == 8,
          "table-with-search: 8 user rows render initially")
    page.fill("#user-search", "engineer")
    page.wait_for_timeout(200)
    filtered = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          status: document.querySelector('#ds-root [role="status"]').textContent,
          text: document.querySelector('#ds-root tbody').textContent,
        }))()"""
    )
    check(filtered["rows"] == 4 and filtered["status"] == "4 of 8 users",
          f"table-with-search: 'engineer' filters to 4 rows with announced count (got {filtered['rows']} / '{filtered['status']}')")
    check("Katherine Johnson" in filtered["text"] and "Alan Turing" not in filtered["text"],
          "table-with-search: filtering matches the role field, not every row")
    page.fill("#user-search", "zzzz")
    page.wait_for_timeout(200)
    empty = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          text: document.querySelector('#ds-root tbody').textContent,
          status: document.querySelector('#ds-root [role="status"]').textContent,
        }))()"""
    )
    check(empty["rows"] == 1 and "No users match" in empty["text"],
          "table-with-search: zero matches render one honest empty row")
    check(empty["status"] == "0 of 8 users",
          f"table-with-search: status announces zero results (got '{empty['status']}')")
    page.click("#ds-root tbody button:has-text('Clear search')")
    page.wait_for_timeout(200)
    restored = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          value: document.getElementById('user-search').value,
          status: document.querySelector('#ds-root [role="status"]').textContent,
        }))()"""
    )
    check(restored["rows"] == 8 and restored["value"] == "" and restored["status"] == "8 of 8 users",
          "table-with-search: Clear search empties the field and restores all 8 rows")


def filters_checks(page):
    print("== table-with-filters ==")
    open_preview(page, "table-with-filters")
    initial = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          count: document.querySelector('#ds-root [aria-live]').textContent,
          clearDisabled: Array.from(document.querySelectorAll('#ds-root button')).find(b => b.textContent === 'Clear filters').disabled,
          selects: document.querySelectorAll('#ds-root select[aria-label]').length,
        }))()"""
    )
    check(initial["selects"] == 2, "table-with-filters: two labelled filter selects render")
    check(initial["rows"] == 10 and initial["count"] == "10 of 10 orders",
          f"table-with-filters: all 10 orders render initially (got {initial['rows']} / '{initial['count']}')")
    check(initial["clearDisabled"] is True, "table-with-filters: Clear filters starts disabled (nothing to clear)")
    page.select_option("#ds-root select[aria-label='Filter by status']", "delivered")
    page.wait_for_timeout(150)
    one = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          count: document.querySelector('#ds-root [aria-live]').textContent,
          clearDisabled: Array.from(document.querySelectorAll('#ds-root button')).find(b => b.textContent === 'Clear filters').disabled,
        }))()"""
    )
    check(one["rows"] == 3 and one["count"] == "3 of 10 orders",
          f"table-with-filters: Delivered narrows to 3 orders with announced count (got {one['rows']})")
    check(one["clearDisabled"] is False, "table-with-filters: Clear filters enables once a filter is active")
    page.select_option("#ds-root select[aria-label='Filter by channel']", "retail")
    page.wait_for_timeout(150)
    empty = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          text: document.querySelector('#ds-root tbody').textContent,
          count: document.querySelector('#ds-root [aria-live]').textContent,
        }))()"""
    )
    check(empty["rows"] == 1 and "No orders match these filters" in empty["text"],
          "table-with-filters: Delivered × Retail renders the empty state (one real row)")
    check(empty["count"] == "0 of 10 orders", f"table-with-filters: count announces zero (got '{empty['count']}')")
    page.click("#ds-root tbody button:has-text('Clear filters')")
    page.wait_for_timeout(150)
    restored = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          status: document.querySelector('#ds-root select[aria-label="Filter by status"]').value,
          channel: document.querySelector('#ds-root select[aria-label="Filter by channel"]').value,
          clearDisabled: Array.from(document.querySelectorAll('#ds-root button')).find(b => b.textContent === 'Clear filters').disabled,
        }))()"""
    )
    check(restored["rows"] == 10 and restored["status"] == "all" and restored["channel"] == "all",
          "table-with-filters: Clear filters resets both selects and restores all 10 orders")
    check(restored["clearDisabled"] is True, "table-with-filters: Clear filters disables itself after reset")
    page.select_option("#ds-root select[aria-label='Filter by status']", "processing")
    page.wait_for_timeout(150)
    page.select_option("#ds-root select[aria-label='Filter by channel']", "partner")
    page.wait_for_timeout(150)
    combo = page.evaluate(
        """(() => ({
          rows: document.querySelectorAll('#ds-root tbody tr').length,
          text: document.querySelector('#ds-root tbody').textContent,
        }))()"""
    )
    check(combo["rows"] == 1 and "ORD-1010" in combo["text"],
          f"table-with-filters: filters compose with AND (Processing × Partner = ORD-1010 only, got {combo['rows']})")


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


def dark_mode_check(page):
    print("== dark mode ==")
    for slug in ("table", "table-sortable", "table-selectable", "table-status", "table-striped"):
        open_preview(page, slug)
        # the surface lives on the bordered container; the <table> itself is transparent
        light_bg = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root table').parentElement).backgroundColor"
        )
        light_fg = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root table')).color"
        )
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(200)
        dark_bg = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root table').parentElement).backgroundColor"
        )
        dark_fg = page.evaluate(
            "getComputedStyle(document.querySelector('#ds-root table')).color"
        )
        check(light_bg != dark_bg, f"{slug}: table surface flips between light and dark themes")
        check(light_fg != dark_fg, f"{slug}: table text flips between light and dark themes")
        body_bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
        check(body_bg == "rgb(10, 10, 10)", f"{slug}: dark canvas applied (body bg {body_bg})")
        page.click("#ds-theme-toggle")
        page.wait_for_timeout(150)


def reduced_motion_check(browser):
    context = browser.new_context(reduced_motion="reduce", viewport={"width": 1280, "height": 900})
    p = context.new_page()
    open_preview(p, "table-selectable")
    prop = p.evaluate(
        "getComputedStyle(document.querySelector('#ds-root tbody tr')).transitionProperty"
    )
    check(prop == "none", f"table-selectable: reduced motion disables row transitions (got {prop})")
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
        actions_checks(page)
        sorting_checks(page)
        selection_checks(page)
        pagination_checks(page)
        expansion_checks(page)
        grouped_checks(page)
        compact_checks(page)
        responsive_checks(page)
        loading_checks(page, browser)
        empty_checks(page)
        status_checks(page)
        header_checks(page)
        footer_checks(page)
        striped_checks(page)
        hover_checks(page)
        search_checks(page)
        filters_checks(page)

        print("== focus / theme / motion ==")
        focus_ring_check(page, "table-sortable", "#ds-root th button:has-text('Service')")
        focus_ring_check(page, "table-selectable", "#ds-root input[aria-label='Select Ada Lovelace']")
        focus_ring_check(page, "table-expandable", "#ds-root button[aria-controls='order-ORD-5201-details']")
        focus_ring_check(page, "table-with-pagination", "#ds-root button[aria-label='Go to next page']")
        focus_ring_check(page, "table-with-search", "#ds-root #user-search")
        focus_ring_check(page, "table-with-filters", "#ds-root select[aria-label='Filter by status']")
        focus_ring_check(page, "table-with-footer", "#ds-root select[aria-label='Filter invoices by status']")
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
