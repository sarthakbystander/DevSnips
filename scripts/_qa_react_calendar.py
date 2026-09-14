#!/usr/bin/env python3
"""QA harness for the DevSnips React Calendar family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx, no `<div onClick`, no inline `style=`, no hex colors
    (except `#000` inside `color-mix` hover darkening)
  - date-model guards: no `toISOString`, no `Date.UTC`, no `.setDate()` /
    `.setMonth()` / `.setFullYear()` mutation, no `Date.parse`
  - TSX/JSX export parity (same exported names + default export) and
    prop-name parity for every exported component signature
  - shared-core equality across all 12 variants (header-comment-neutralized)

Date-unit checks (Node, when the esbuild toolchain is available):
  - the exported date utilities are bundled from the actual reference
    code.tsx and driven through leap years, month lengths, month/year
    boundaries, clamping, ISO-8601 week edges, and DST-transition timezones

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors; 0 horizontal overflow @ 375/768/1280
  - grid/row/columnheader/gridcell roles; one tabbable day (roving tabindex)
  - full locale-aware day labels; aria-selected; aria-current="date"
  - no nested interactive elements; native disabled on disabled days
  - selection (single / multiple / range incl. same-day, reversed, crossing),
    month/year navigation + boundaries, leap years via the controlled demo,
    week numbers, outside days, month/year pickers, footer actions,
    controlled state + locale switching, min/max day + navigation constraints
  - full keyboard model (arrows, Home/End, PageUp/PageDown, Shift+Page*)
  - focus-visible ring; dark-mode token flip; reduced-motion guard

Run: python3 scripts/_qa_react_calendar.py
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALENDAR = ROOT / "React/Components/Calendar"
ESBUILD = Path("/tmp/dsbuild/node_modules/.bin/esbuild")
DSBUILD = Path("/tmp/dsbuild")
SLUGS = [
    "calendar",
    "calendar-single",
    "calendar-range",
    "calendar-multiple",
    "calendar-disabled-dates",
    "calendar-min-max",
    "calendar-week-numbers",
    "calendar-outside-days",
    "calendar-month-picker",
    "calendar-year-picker",
    "calendar-with-footer",
    "calendar-controlled",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = [
    "daysInMonth", "isLeapYear", "compareDays", "isSameDay", "addDays",
    "addMonths", "startOfMonth", "endOfMonth", "isoWeekNumber",
    "buildMonthWeeks", "useCalendar", "Calendar", "CalendarHeader",
    "CalendarPrevious", "CalendarNext", "CalendarHeading", "CalendarGrid",
    "CalendarFooter",
]

failures: list[str] = []
skips: list[str] = []
checks = 0


def check(ok: bool, label: str):
    global checks
    checks += 1
    if not ok:
        failures.append(label)
        print(f"  FAIL {label}")


def skip(label: str):
    skips.append(label)
    print(f"  SKIP {label}")


def neutralize_core(tsx: str) -> str:
    """Shared core of a variant: the header doc comment removed, blank runs
    collapsed — everything else must be identical across the family."""
    tsx = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S)
    tsx = re.sub(r"\n{3,}", "\n\n", tsx)
    return tsx.rstrip()


def prop_signature(src: str, name: str) -> list[str]:
    """Destructured prop names of `export function <name>(...)` (TSX) or the
    plain `function <name>(...)` (JSX, exports hoisted to a trailing block).
    Parameter lists end at the first `)` at paren depth 0 — a destructured
    object pattern is skipped past braces, and a bare `props`/`event`
    parameter counts as itself. Defaults and types are stripped."""
    m = re.search(rf"export\s+function\s+{name}\s*\(", src) \
        or re.search(rf"(?<![\w$])function\s+{name}\s*\(", src)
    if not m:
        return []
    start = m.end() - 1  # index of the opening paren
    depth, end = 0, None
    for i in range(start, len(src)):
        c = src[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                end = i
                break
    block = src[start + 1 : end if end else len(src)]
    props = []
    for raw in block.split(","):
        seg = raw.strip().strip("()").strip()
        if seg.startswith("{") and seg.endswith("}"):
            seg = seg[1:-1]
        if not seg or seg.startswith("..."):
            continue
        seg = re.sub(r"\s*=.*$", "", seg, flags=re.S)
        seg = re.sub(r"\s*:.*$", "", seg, flags=re.S)
        seg = seg.strip()
        if seg:
            props.append(seg)
    return sorted(set(props))


def static_checks():
    print("static checks")
    cores: dict[str, str] = {}
    for slug in SLUGS:
        folder = CALENDAR / slug
        check(folder.is_dir(), f"{slug}: folder exists")
        for name in FILES:
            check((folder / name).is_file(), f"{slug}: {name} exists")

        meta = json.loads((folder / "metadata.json").read_text())
        for key in ("id", "name", "slug", "component", "family", "variant", "description",
                    "framework", "language", "languages", "technology", "type", "category",
                    "subcategory", "styling", "tags", "features", "responsive", "darkMode",
                    "accessibility", "interactive", "dependencies", "source", "related"):
            check(key in meta, f"{slug}: metadata has {key}")
        check(meta["technology"] == "react", f"{slug}: technology react")
        check(meta["type"] == "component", f"{slug}: type component")
        check(meta["category"] == "Calendar", f"{slug}: category Calendar")
        check(meta["component"] == "calendar", f"{slug}: component calendar")
        check(meta["family"] == "calendar", f"{slug}: family calendar")
        check(meta["styling"] == "Tailwind CSS", f"{slug}: styling Tailwind CSS")
        check(meta["languages"] == ["JSX", "TSX"], f"{slug}: languages JSX+TSX")
        check(meta["slug"] == slug, f"{slug}: metadata slug matches folder")
        check(meta["dependencies"] == [], f"{slug}: no dependencies")

        tsx = (folder / "code.tsx").read_text()
        jsx = (folder / "code.jsx").read_text()
        check(not re.search(r"\bany\b", tsx), f"{slug}: no any in code.tsx")
        check("<div onClick" not in tsx, f"{slug}: no div onClick")
        check("style=" not in tsx, f"{slug}: no inline style attribute")
        hexes = [h for h in re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx) if h != "#000"]
        check(hexes == [], f"{slug}: no hex colors besides color-mix #000 {hexes}")
        # date-model guards: local calendar dates only
        check("toISOString" not in tsx, f"{slug}: no toISOString (UTC conversion)")
        check("Date.UTC" not in tsx, f"{slug}: no Date.UTC")
        check("Date.parse" not in tsx, f"{slug}: no Date.parse")
        for mutator in (".setDate(", ".setMonth(", ".setFullYear(", ".setHours(", ".setMinutes("):
            check(mutator not in tsx, f"{slug}: no Date mutation {mutator}")
        check('role="grid"' in tsx, f"{slug}: role=grid present")
        check('role="row"' in tsx, f"{slug}: role=row present")
        check('role="gridcell"' in tsx, f"{slug}: role=gridcell present")
        check('role="columnheader"' in tsx, f"{slug}: role=columnheader present")
        check("aria-selected" in tsx, f"{slug}: aria-selected present")
        check('aria-current={isToday ? "date" : undefined}' in tsx, f"{slug}: aria-current=date for today")
        check('aria-live="polite"' in tsx, f"{slug}: aria-live heading")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("tabIndex=" in tsx, f"{slug}: roving tabindex")
        check("Intl.DateTimeFormat" in tsx, f"{slug}: locale-aware Intl formatting")

        tsx_exports = re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx)
        jsx_exports = re.findall(r"export \{([^}]*)\}", jsx)
        jsx_names = [n.strip() for n in jsx_exports[0].split(",")] if jsx_exports else []
        for name in CORE_EXPORTS:
            check(name in tsx_exports, f"{slug}: exports {name}")
        check(sorted(tsx_exports) == sorted(jsx_names),
              f"{slug}: export parity {len(tsx_exports)} vs {len(jsx_names)}")
        check("export default Calendar;" in jsx, f"{slug}: JSX default export")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        for name in ("Calendar", "CalendarHeader", "CalendarPrevious", "CalendarNext",
                     "CalendarHeading", "CalendarGrid", "CalendarFooter", "useCalendar"):
            tp, jp = prop_signature(tsx, name), prop_signature(jsx, name)
            check(tp == jp, f"{slug}: {name} prop parity {tp} vs {jp}")

        cores[slug] = neutralize_core(tsx)

    ref = cores[SLUGS[0]]
    for slug, core in cores.items():
        check(core == ref, f"{slug}: shared core identical to reference")


NODE_TEST = r'''
import {
  daysInMonth, isLeapYear, addDays, addMonths, startOfMonth, endOfMonth,
  compareDays, isSameDay, isoWeekNumber, buildMonthWeeks,
} from "./qa-cal.mjs";
let pass = 0, fail = 0;
const t = (n, c) => { if (c) pass++; else { fail++; console.log("FAIL", n); } };
const d = (y, m, day) => new Date(y, m, day);

// leap years + month lengths
t("leap 2024", isLeapYear(2024) === true);
t("non-leap 2026", isLeapYear(2026) === false);
t("leap 2000 (div 400)", isLeapYear(2000) === true);
t("non-leap 1900 (div 100)", isLeapYear(1900) === false);
t("Feb 2024 = 29", daysInMonth(2024, 1) === 29);
t("Feb 2026 = 28", daysInMonth(2026, 1) === 28);
t("Feb 1900 = 28", daysInMonth(1900, 1) === 28);
t("Apr = 30", daysInMonth(2026, 3) === 30);
t("Jan = 31", daysInMonth(2026, 0) === 31);
t("Dec = 31", daysInMonth(2026, 11) === 31);
// day arithmetic across month/year boundaries
t("Jan 31 + 1d = Feb 1", isSameDay(addDays(d(2026,0,31),1), d(2026,1,1)));
t("Dec 31 + 1d = Jan 1 next year", (() => { const r = addDays(d(2026,11,31),1); return r.getFullYear()===2027 && r.getMonth()===0 && r.getDate()===1; })());
t("Jan 1 - 1d = Dec 31 prev year", (() => { const r = addDays(d(2026,0,1),-1); return r.getFullYear()===2025 && r.getMonth()===11 && r.getDate()===31; })());
t("Feb 28 2026 + 1 = Mar 1", isSameDay(addDays(d(2026,1,28),1), d(2026,2,1)));
t("Feb 28 2024 + 1 = Feb 29", isSameDay(addDays(d(2024,1,28),1), d(2024,1,29)));
t("Feb 29 2024 + 1 = Mar 1", isSameDay(addDays(d(2024,1,29),1), d(2024,2,1)));
// month arithmetic with clamping
t("Jan 31 + 1mo = Feb 28 (2026)", isSameDay(addMonths(d(2026,0,31),1), d(2026,1,28)));
t("Jan 31 + 1mo = Feb 29 (2024)", isSameDay(addMonths(d(2024,0,31),1), d(2024,1,29)));
t("Mar 31 - 1mo = Feb 28", isSameDay(addMonths(d(2026,2,31),-1), d(2026,1,28)));
t("Dec 15 + 1mo = Jan 15 next", (() => { const r = addMonths(d(2026,11,15),1); return r.getFullYear()===2027 && r.getMonth()===0; })());
t("Jan 15 - 1mo = Dec 15 prev", (() => { const r = addMonths(d(2026,0,15),-1); return r.getFullYear()===2025 && r.getMonth()===11; })());
t("Aug 31 + 6mo = Feb 28 2027", isSameDay(addMonths(d(2026,7,31),6), d(2027,1,28)));
// comparison ignores time-of-day
t("compare ignores time", compareDays(d(2026,7,22), new Date(2026,7,22,23,59)) === 0);
t("compare lt", compareDays(d(2026,7,21), d(2026,7,22)) === -1);
t("compare gt across year", compareDays(d(2027,0,1), d(2026,11,31)) === 1);
// ISO-8601 week numbers
t("ISO 2026-01-01 = w1", isoWeekNumber(d(2026,0,1)) === 1);
t("ISO 2025-12-29 = 2026 w1", isoWeekNumber(d(2025,11,29)) === 1);
t("ISO 2026-08-03 = w32", isoWeekNumber(d(2026,7,3)) === 32);
t("ISO 2024-02-29 = w9", isoWeekNumber(d(2024,1,29)) === 9);
t("ISO 2020-12-31 = w53", isoWeekNumber(d(2020,11,31)) === 53);
t("ISO 2021-01-01 = 2020 w53", isoWeekNumber(d(2021,0,1)) === 53);
t("ISO Mon-Sun share a week across DST", [9,10,11,12,13,14,15].every(day => isoWeekNumber(d(2026,2,day)) === 11));
// grid building
const aug = buildMonthWeeks(d(2026,7,1), 0);
t("6x7 grid", aug.length === 6 && aug.every(r => r.length === 7));
t("Aug 2026 Sun-start first = Jul 26", isSameDay(aug[0][0], d(2026,6,26)));
t("Aug 2026 Sun-start last = Sep 5", isSameDay(aug[5][6], d(2026,8,5)));
t("Aug 2026 Mon-start first = Jul 27", isSameDay(buildMonthWeeks(d(2026,7,1), 1)[0][0], d(2026,6,27)));
t("Feb 2026 Sun-start first = Feb 1", isSameDay(buildMonthWeeks(d(2026,1,1), 0)[0][0], d(2026,1,1)));
t("endOfMonth Feb 2024 = 29", endOfMonth(d(2024,1,10)).getDate() === 29);
t("startOfMonth", isSameDay(startOfMonth(d(2026,7,22)), d(2026,7,1)));
// grid integrity across 5 years: unique, consecutive, correct in-month count
let ok = true;
for (let y = 2024; y <= 2028; y++) for (let m = 0; m < 12; m++) {
  const cells = buildMonthWeeks(new Date(y, m, 1), 0).flat();
  const keys = new Set(cells.map(c => c.getFullYear()*10000 + (c.getMonth()+1)*100 + c.getDate()));
  if (keys.size !== 42) ok = false;
  for (let i = 1; i < 42; i++) if (!isSameDay(cells[i], addDays(cells[i-1], 1))) ok = false;
  if (cells.filter(c => c.getMonth() === m && c.getFullYear() === y).length !== daysInMonth(y, m)) ok = false;
}
t("5yr grid integrity", ok);
console.log(JSON.stringify({ pass, fail }));
process.exit(fail ? 1 : 0);
'''

UNIT_TIMEZONES = ["UTC", "America/New_York", "America/Santiago", "Australia/Lord_Howe", "Pacific/Apia", "Europe/Berlin"]


def unit_checks():
    """Run the exported date utilities (bundled from the real code.tsx)
    through edge cases in Node, across DST-relevant timezones."""
    global checks
    print("date unit checks (node)")
    if not ESBUILD.exists():
        skip("esbuild toolchain missing — date unit tests not executed")
        return
    import os
    bundle = DSBUILD / "qa-cal.mjs"
    test = DSBUILD / "qa-cal-test.mjs"
    try:
        subprocess.run(
            [str(ESBUILD), str(CALENDAR / "calendar/code.tsx"), "--format=esm",
             "--bundle", "--external:react", "--external:react-dom", "--external:react/*",
             f"--outfile={bundle}"],
            capture_output=True, text=True, check=True,
        )
        test.write_text(NODE_TEST, encoding="utf-8")
        for tz in UNIT_TIMEZONES:
            env = dict(os.environ, TZ=tz)
            result = subprocess.run(
                ["node", str(test)], capture_output=True, text=True,
                cwd=str(DSBUILD), env=env,
            )
            line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "{}"
            try:
                counts = json.loads(line)
            except json.JSONDecodeError:
                counts = {"pass": 0, "fail": -1}
            ok = result.returncode == 0 and counts.get("fail") == 0
            check(ok, f"date utils unit tests pass in TZ={tz} ({line.strip()} {result.stderr.strip()[:120]})")
            checks += counts.get("pass", 0) - 1
    finally:
        bundle.unlink(missing_ok=True)
        test.unlink(missing_ok=True)


PICKER_SLUGS = {"calendar-month-picker", "calendar-year-picker"}
NESTED_JS = """() => {
  let bad = 0;
  document.querySelectorAll('#ds-root button, #ds-root a, #ds-root select').forEach((el) => {
    if (el.querySelector('button, a, input, select, textarea')) bad += 1;
  });
  return bad === 0;
}"""
LABELS_JS = """() => Array.from(document.querySelectorAll('[role="gridcell"] button'))
  .every((b) => /\\b\\d{4}\\b/.test(b.getAttribute('aria-label') || ''))"""


def open_preview(page, slug):
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto((CALENDAR / slug / "preview.html").as_uri())
    page.wait_for_selector("#ds-root *", timeout=15000)
    page.wait_for_timeout(500)
    return errors


def no_overflow(page, slug, state):
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(120)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"{slug}: no horizontal overflow ({state}) @ {w} (got {overflow})")
    page.set_viewport_size({"width": 1280, "height": 900})


def focus_key(page) -> str:
    return page.evaluate(
        "(document.activeElement && document.activeElement.dataset && document.activeElement.dataset.calFocus) || ''"
    )


def heading_text(page) -> str:
    return page.locator("#ds-root h2").first.text_content().strip()


def selected_count(page) -> int:
    return page.locator('[role="gridcell"][aria-selected="true"]').count()


def generic_browser_checks(browser):
    print("generic browser checks (per variant)")
    for slug in SLUGS:
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = open_preview(page, slug)
        check(not errors, f"{slug}: no console/page errors {errors[:3]}")

        # Scope to the first calendar demo (some showcases mount two).
        demo = page.locator("#ds-root > div > div").first
        grids = demo.locator('[role="grid"]')
        check(grids.count() >= 1, f"{slug}: at least one role=grid")
        if slug in PICKER_SLUGS:
            check(grids.first.locator("button").count() == 12,
                  f"{slug}: picker view renders 12 options")
        else:
            expected_grids = 2 if slug == "calendar-range" else 1
            check(grids.count() == expected_grids, f"{slug}: {expected_grids} day grid(s)")
            check(demo.locator('[role="gridcell"]').count() == 42 * expected_grids,
                  f"{slug}: fixed 6x7 grid structure ({42 * expected_grids} cells)")
            check(demo.locator('[role="columnheader"]').count() >= 7, f"{slug}: 7 weekday columnheaders")
            check(demo.evaluate(LABELS_JS), f"{slug}: full locale-aware day labels")
        # roving tabindex: exactly one tabbable control in the grid(s)
        check(demo.locator('[role="grid"] button[tabindex="0"]').count() == 1,
              f"{slug}: exactly one tabbable grid control")
        # no nested interactive elements
        check(page.evaluate(NESTED_JS), f"{slug}: no nested interactive elements")
        # navigation buttons with accessible names
        check(demo.locator('button[aria-label^="Go to previous"]').count() == 1,
              f"{slug}: previous nav button labelled")
        check(demo.locator('button[aria-label^="Go to next"]').count() == 1,
              f"{slug}: next nav button labelled")
        # live heading
        check(demo.locator('h2[aria-live="polite"]').count() >= 1, f"{slug}: aria-live heading")
        no_overflow(page, slug, "initial")
        page.close()


def check_reference(browser):
    slug = "calendar"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    check(heading_text(page) == "August 2026", f"{slug}: opens on August 2026")
    check(page.locator('[role="gridcell"] button').count() == 31, f"{slug}: 31 day buttons in August")
    # today is marked but not auto-selected
    today_state = page.evaluate("""() => {
      const now = new Date();
      const inView = now.getFullYear() === 2026 && now.getMonth() === 7;
      const marked = document.querySelectorAll('[aria-current="date"]').length;
      const sel = document.querySelectorAll('[role="gridcell"][aria-selected="true"]').length;
      return { inView, marked, sel };
    }""")
    check(today_state["marked"] == (1 if today_state["inView"] else 0),
          f"{slug}: aria-current=date present iff today is in the visible month")
    check(today_state["sel"] == 0, f"{slug}: today is not auto-selected")

    # single selection, no accidental deselect
    page.locator('[data-cal-focus="20260814"]').click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 1, f"{slug}: selecting a day marks one cell")
    check("Aug 14, 2026" in page.locator("#cal-readout").text_content(), f"{slug}: selection announced")
    page.locator('[data-cal-focus="20260814"]').click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 1, f"{slug}: re-clicking the selected day does not deselect")

    # selection persists across navigation
    page.get_by_role("button", name="Go to next month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "September 2026", f"{slug}: next month navigates")
    check(selected_count(page) == 0, f"{slug}: no selected cell in the new month")
    page.get_by_role("button", name="Go to previous month").click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 1, f"{slug}: selection survives navigation")

    # keyboard: roving focus + arrows
    page.locator('[data-cal-focus="20260814"]').click()
    page.wait_for_timeout(150)
    check(focus_key(page) == "20260814", f"{slug}: clicked day receives focus")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(100)
    check(focus_key(page) == "20260815", f"{slug}: ArrowRight moves to next day")
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(100)
    check(focus_key(page) == "20260822", f"{slug}: ArrowDown moves a week down")
    page.keyboard.press("ArrowLeft")
    page.wait_for_timeout(100)
    check(focus_key(page) == "20260821", f"{slug}: ArrowLeft moves to previous day")
    page.keyboard.press("ArrowUp")
    page.wait_for_timeout(100)
    check(focus_key(page) == "20260814", f"{slug}: ArrowUp moves a week up")
    page.keyboard.press("Home")
    page.wait_for_timeout(100)
    check(focus_key(page) == "20260809", f"{slug}: Home moves to week start (Sunday)")
    page.keyboard.press("End")
    page.wait_for_timeout(100)
    check(focus_key(page) == "20260815", f"{slug}: End moves to week end (Saturday)")

    # keyboard paging across month/year boundaries (never selects)
    page.keyboard.press("PageDown")
    page.wait_for_timeout(250)
    check(heading_text(page) == "September 2026", f"{slug}: PageDown pages the month")
    check(focus_key(page) == "20260915", f"{slug}: PageDown moves focus with the month")
    check(selected_count(page) == 0, f"{slug}: keyboard navigation never selects")
    page.keyboard.press("PageUp")
    page.wait_for_timeout(250)
    check(heading_text(page) == "August 2026", f"{slug}: PageUp pages back")
    page.keyboard.press("Shift+PageDown")
    page.wait_for_timeout(250)
    check(heading_text(page) == "August 2027", f"{slug}: Shift+PageDown pages a year")
    page.keyboard.press("Shift+PageUp")
    page.wait_for_timeout(250)
    check(heading_text(page) == "August 2026", f"{slug}: Shift+PageUp pages a year back")

    # Dec -> Jan boundary via nav buttons
    for _ in range(4):
        page.get_by_role("button", name="Go to next month").click()
        page.wait_for_timeout(80)
    check(heading_text(page) == "December 2026", f"{slug}: December 2026 reached")
    page.get_by_role("button", name="Go to next month").click()
    page.wait_for_timeout(120)
    check(heading_text(page) == "January 2027", f"{slug}: December rolls into January of the next year")
    page.get_by_role("button", name="Go to previous month").click()
    page.wait_for_timeout(120)
    check(heading_text(page) == "December 2026", f"{slug}: January rolls back into December")
    page.close()


def check_single(browser):
    slug = "calendar-single"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")
    check(selected_count(page) == 1, f"{slug}: controlled initial selection rendered")
    check("Milestone: Aug 12, 2026" in page.locator("#single-readout").text_content(),
          f"{slug}: controlled initial selection shown")
    page.locator('[data-cal-focus="20260818"]').click()
    page.wait_for_timeout(150)
    check("Milestone: Aug 18, 2026" in page.locator("#single-readout").text_content(),
          f"{slug}: click updates controlled selection")
    page.locator('[data-cal-focus="20260818"]').click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 1, f"{slug}: repeat click is a no-op (no deselect)")
    page.get_by_role("button", name="Clear").click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 0, f"{slug}: explicit clear empties the selection")
    check("No milestone date set." in page.locator("#single-readout").text_content(),
          f"{slug}: cleared state announced")
    page.close()


def check_range(browser):
    slug = "calendar-range"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    grids = page.locator('[role="grid"]')
    check(grids.nth(0).get_attribute("aria-label") == "August 2026", f"{slug}: first grid is August 2026")
    check(grids.nth(1).get_attribute("aria-label") == "September 2026", f"{slug}: second grid is September 2026")
    check(heading_text(page) == "August – September 2026", f"{slug}: multi-month heading")

    # basic range with band: Aug 17 -> Aug 24 — a clean week that does not
    # cross the Aug 15 hold.
    page.locator('[data-cal-focus="20260817"]').click()
    page.wait_for_timeout(150)
    check("Arriving Aug 17, 2026" in page.locator("#range-readout").text_content(),
          f"{slug}: first click starts the range")
    check(selected_count(page) == 1, f"{slug}: pending range marks the start day")
    page.locator('[data-cal-focus="20260824"]').click()
    page.wait_for_timeout(300)
    check("Aug 17, 2026 – Aug 24, 2026 · 7 nights" in page.locator("#range-readout").text_content(),
          f"{slug}: range completes with correct length")
    check(selected_count(page) == 8, f"{slug}: all 8 in-range cells marked")
    start_cls = page.locator('[data-cal-focus="20260817"]').get_attribute("class") or ""
    mid_cls = page.locator('[data-cal-focus="20260819"]').get_attribute("class") or ""
    end_cls = page.locator('[data-cal-focus="20260824"]').get_attribute("class") or ""
    check("rounded-r-none" in start_cls, f"{slug}: range start squared toward the band")
    check("rounded-none" in mid_cls, f"{slug}: range middle is a continuous band")
    check("rounded-l-none" in end_cls, f"{slug}: range end squared toward the band")

    # same-day range
    page.locator('[data-cal-focus="20260820"]').click()
    page.wait_for_timeout(120)
    page.locator('[data-cal-focus="20260820"]').click()
    page.wait_for_timeout(150)
    check("Aug 20, 2026 – Aug 20, 2026 · 0 nights" in page.locator("#range-readout").text_content(),
          f"{slug}: same-day range completes")

    # reversed click restarts (no silent swap)
    page.locator('[data-cal-focus="20260825"]').click()
    page.wait_for_timeout(120)
    page.locator('[data-cal-focus="20260821"]').click()
    page.wait_for_timeout(150)
    check("Arriving Aug 21, 2026" in page.locator("#range-readout").text_content(),
          f"{slug}: earlier second click restarts the range")

    # completion across the disabled hold day restarts instead of crossing
    page.locator('[data-cal-focus="20260812"]').click()
    page.wait_for_timeout(120)
    page.locator('[data-cal-focus="20260818"]').click()
    page.wait_for_timeout(150)
    check("Arriving Aug 18, 2026" in page.locator("#range-readout").text_content(),
          f"{slug}: range may not cross the disabled hold day")
    check(selected_count(page) == 1, f"{slug}: crossing attempt leaves only the new start")

    # complete the pending range, then build a fresh one across the month
    # boundary (September days live in the second grid)
    page.locator('[data-cal-focus="20260826"]').click()
    page.wait_for_timeout(200)
    check("Aug 18, 2026 – Aug 26, 2026" in page.locator("#range-readout").text_content(),
          f"{slug}: pending range completes")
    page.locator('[data-cal-focus="20260828"]').click()
    page.wait_for_timeout(120)
    page.locator('[data-cal-focus="20260903"]').click()
    page.wait_for_timeout(300)
    check("Aug 28, 2026 – Sep 3, 2026 · 6 nights" in page.locator("#range-readout").text_content(),
          f"{slug}: range across a month boundary")
    check(selected_count(page) == 7, f"{slug}: cross-month range marks 7 cells across both grids")
    page.close()


def check_multiple(browser):
    slug = "calendar-multiple"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")
    check(selected_count(page) == 3, f"{slug}: three seeded days selected")
    page.locator('[data-cal-focus="20260805"]').click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 2, f"{slug}: clicking a selected day toggles it off")
    check("2 days:" in page.locator("#multiple-readout").text_content(), f"{slug}: summary tracks toggles")
    page.locator('[data-cal-focus="20260820"]').click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 3, f"{slug}: clicking an unselected day toggles it on")
    page.get_by_role("button", name="Clear all").click()
    page.wait_for_timeout(150)
    check(selected_count(page) == 0, f"{slug}: parent can clear the whole set")
    page.close()


def check_disabled(browser):
    slug = "calendar-disabled-dates"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    check(page.locator('[data-cal-focus="20260808"]').is_disabled(), f"{slug}: weekend day disabled (Aug 8)")
    check(page.locator('[data-cal-focus="20260810"]').is_disabled(), f"{slug}: blackout day disabled (Aug 10)")
    check(not page.locator('[data-cal-focus="20260813"]').is_disabled(), f"{slug}: Aug 13 stays enabled")
    # disabled days cannot be selected even via a programmatic click
    page.evaluate("document.querySelector('[data-cal-focus=\\'20260810\\']').click()")
    page.wait_for_timeout(120)
    check("Select an open date." in page.locator("#disabled-readout").text_content(),
          f"{slug}: disabled day cannot be selected")
    # keyboard navigation skips disabled days
    page.locator('[data-cal-focus="20260807"]').click()
    page.wait_for_timeout(150)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(120)
    check(focus_key(page) == "20260813", f"{slug}: ArrowRight skips weekend + blackout days")
    # tabbable follows focus; on a fresh calendar it lands on the first enabled day (Aug 3)
    check(page.locator('[role="grid"] button[tabindex="0"]').get_attribute("data-cal-focus") == "20260813",
          f"{slug}: roving tabindex follows the moved focus")
    page.locator('[data-cal-focus="20260813"]').click()
    page.wait_for_timeout(150)
    check("Booked for Aug 13, 2026." in page.locator("#disabled-readout").text_content(),
          f"{slug}: enabled day selects normally")
    page.close()


def check_min_max(browser):
    slug = "calendar-min-max"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    card1 = page.locator('[role="grid"][aria-label="August 2026"]').first
    check(page.locator('[data-cal-focus="20260804"]').first.is_disabled(), f"{slug}: day before minDate disabled")
    check(not page.locator('[data-cal-focus="20260805"]').first.is_disabled(), f"{slug}: minDate itself enabled")
    check(not page.locator('[data-cal-focus="20260826"]').first.is_disabled(), f"{slug}: maxDate itself enabled")
    check(page.locator('[data-cal-focus="20260827"]').first.is_disabled(), f"{slug}: day after maxDate disabled")
    prev1 = page.get_by_role("button", name="Go to previous month").nth(0)
    next1 = page.get_by_role("button", name="Go to next month").nth(0)
    check(prev1.is_disabled(), f"{slug}: previous disabled when the prior month is fully outside")
    check(next1.is_disabled(), f"{slug}: next disabled when the following month is fully outside")
    # selection cannot bypass the window (programmatic click on a disabled day)
    page.evaluate("document.querySelector('[data-cal-focus=\\'20260804\\']').click()")
    page.wait_for_timeout(120)
    check("Select a date inside the window." in page.locator("#minmax-readout").text_content(),
          f"{slug}: selection cannot bypass minDate")
    # keyboard cannot escape the window
    page.locator('[data-cal-focus="20260805"]').first.click()
    page.wait_for_timeout(150)
    page.keyboard.press("ArrowLeft")
    page.wait_for_timeout(150)
    check(focus_key(page) == "20260805", f"{slug}: ArrowLeft cannot escape before minDate")
    page.locator('[data-cal-focus="20260826"]').first.click()
    page.wait_for_timeout(150)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(150)
    check(focus_key(page) == "20260826", f"{slug}: ArrowRight cannot escape past maxDate")

    # cross-year window: prev disabled, next walks Dec 2026 -> Feb 2027, then disables
    grids = page.locator('[role="grid"]')
    check(grids.nth(1).get_attribute("aria-label") == "November 2026", f"{slug}: second demo opens November 2026")
    prev2 = page.get_by_role("button", name="Go to previous month").nth(1)
    next2 = page.get_by_role("button", name="Go to next month").nth(1)
    check(prev2.is_disabled(), f"{slug}: cross-year window disables previous")
    check(not next2.is_disabled(), f"{slug}: cross-year window allows next")
    next2.click(); page.wait_for_timeout(120)
    check(grids.nth(1).get_attribute("aria-label") == "December 2026", f"{slug}: November -> December")
    next2.click(); page.wait_for_timeout(120)
    check(grids.nth(1).get_attribute("aria-label") == "January 2027", f"{slug}: December rolls into January 2027")
    next2.click(); page.wait_for_timeout(120)
    check(grids.nth(1).get_attribute("aria-label") == "February 2027", f"{slug}: January -> February 2027")
    check(next2.is_disabled(), f"{slug}: next disabled at the window end")
    check(not prev2.is_disabled(), f"{slug}: previous re-enabled inside the window")
    page.close()


def check_week_numbers(browser):
    slug = "calendar-week-numbers"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    headers = page.locator('[role="columnheader"]')
    check(headers.count() == 8, f"{slug}: week-number column + 7 weekday headers")
    check(headers.nth(0).get_attribute("aria-label") == "Week number", f"{slug}: week column labelled")
    check(headers.nth(1).get_attribute("aria-label") == "Monday", f"{slug}: weekStartsOn=1 starts on Monday")
    weeks = page.locator('[role="rowheader"]')
    check(weeks.count() == 6, f"{slug}: one week number per row")
    got = [weeks.nth(i).text_content().strip() for i in range(6)]
    check(got == ["31", "32", "33", "34", "35", "36"], f"{slug}: ISO week numbers 31-36 (got {got})")
    check(weeks.first.locator("button").count() == 0, f"{slug}: week numbers are not interactive")
    # headers and rows agree: Aug 1 2026 is a Saturday -> column index 5 of the first week row
    first_row = page.locator('[role="row"]').nth(1)
    cell = first_row.locator('[role="gridcell"]').nth(5)
    check(cell.locator("button").get_attribute("aria-label") == "Saturday, August 1, 2026",
          f"{slug}: Monday-start headers align with the dates")
    page.locator('[data-cal-focus="20260813"]').click()
    page.wait_for_timeout(150)
    check("ISO week 33" in page.locator("#weeknum-readout").text_content(),
          f"{slug}: exported isoWeekNumber agrees with the column")
    page.close()


def check_outside_days(browser):
    slug = "calendar-outside-days"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    outside = page.locator("[data-outside]")
    check(outside.count() == 11, f"{slug}: 6 leading + 5 trailing outside days rendered")
    first = page.locator('[data-cal-focus="20260726"]')
    check(first.get_attribute("aria-label") == "Sunday, July 26, 2026",
          f"{slug}: outside day keeps its real month in the label")
    trailing = page.locator('[data-cal-focus="20260901"]')
    check(trailing.get_attribute("aria-label") == "Tuesday, September 1, 2026",
          f"{slug}: trailing outside day labelled with September")
    trailing.click()
    page.wait_for_timeout(200)
    check(heading_text(page) == "September 2026", f"{slug}: selecting an outside day pages to its month")
    check(selected_count(page) == 1, f"{slug}: outside day selection lands in the new month")
    check(focus_key(page) == "20260901", f"{slug}: focus follows the outside-day selection")
    # grid structure is stable: still exactly 42 cells after the month change
    check(page.locator('[role="gridcell"]').count() == 42, f"{slug}: 6x7 grid stays stable")
    page.close()


def check_month_picker(browser):
    slug = "calendar-month-picker"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    check(page.locator('[role="grid"]').get_attribute("aria-label") == "Choose a month in 2026",
          f"{slug}: opens in the months view")
    check(heading_text(page) == "2026", f"{slug}: months view heading shows the year")
    check(page.locator('button[aria-label="Go to previous year"]').count() == 1,
          f"{slug}: nav buttons are year-aware")
    check(page.locator('[role="gridcell"][aria-selected="true"] button').text_content().strip() == "August",
          f"{slug}: current month marked")
    page.locator('button[aria-label="March 2026"]').click()
    page.wait_for_timeout(200)
    check(heading_text(page) == "March 2026", f"{slug}: choosing a month opens its day grid")
    check(page.locator('[role="gridcell"] button').count() == 31, f"{slug}: March renders 31 days")
    # heading cycles days -> months -> years
    page.locator("h2 button").click()
    page.wait_for_timeout(150)
    check(page.locator('[role="grid"]').get_attribute("aria-label") == "Choose a month in 2026",
          f"{slug}: heading re-opens the months view")
    page.get_by_role("button", name="Go to previous year").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "2025", f"{slug}: previous year paging")
    page.close()


def check_year_picker(browser):
    slug = "calendar-year-picker"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    check(page.locator('[role="grid"]').get_attribute("aria-label") == "Choose a year",
          f"{slug}: opens in the years view")
    check(heading_text(page) == "2016 – 2027", f"{slug}: 12-year page heading")
    check(page.locator('button[aria-label="Go to previous 12 years"]').count() == 1,
          f"{slug}: nav buttons are decade-aware")
    check(page.locator('[role="gridcell"][aria-selected="true"] button').text_content().strip() == "2026",
          f"{slug}: current year marked")
    page.locator('[role="gridcell"] button', has_text="2024").first.click()
    page.wait_for_timeout(200)
    check(page.locator('[role="grid"]').get_attribute("aria-label") == "Choose a month in 2024",
          f"{slug}: choosing a year continues to the month picker")
    page.locator('button[aria-label="February 2024"]').click()
    page.wait_for_timeout(200)
    check(heading_text(page) == "February 2024", f"{slug}: February 2024 opens")
    check(page.locator('[data-cal-focus="20240229"]').count() == 1, f"{slug}: Feb 29 exists in a leap year")
    check(page.locator('[role="gridcell"] button').count() == 29, f"{slug}: 29 day buttons in Feb 2024")
    page.close()


def check_footer(browser):
    slug = "calendar-with-footer"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    check("No date selected" in page.locator("#footer-readout").text_content(),
          f"{slug}: empty summary initially")
    page.locator('[data-cal-focus="20260814"]').click()
    page.wait_for_timeout(150)
    check(page.locator("#footer-readout").text_content().strip() == "Aug 14, 2026",
          f"{slug}: summary tracks the selection")
    page.get_by_role("button", name="Clear").click()
    page.wait_for_timeout(150)
    check("No date selected" in page.locator("#footer-readout").text_content(),
          f"{slug}: Clear empties the selection")
    page.get_by_role("button", name="Today").click()
    page.wait_for_timeout(200)
    expected = page.evaluate(
        "() => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date())"
    )
    check(page.locator("#footer-readout").text_content().strip() == expected,
          f"{slug}: Today selects the current local date")
    expected_heading = page.evaluate(
        "() => new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(new Date())"
    )
    check(heading_text(page) == expected_heading, f"{slug}: Today navigates to the current month")
    page.close()


def check_controlled(browser):
    slug = "calendar-controlled"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    check(heading_text(page) == "August 2026", f"{slug}: controlled initial month")
    check("Selected: Aug 14, 2026" in page.locator("#controlled-readout").text_content(),
          f"{slug}: controlled initial selection")
    # internal navigation flows through onMonthChange
    page.get_by_role("button", name="Go to previous month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "July 2026", f"{slug}: internal nav updates the controlled month")
    check("month → July 2026" in page.locator("#controlled-log").text_content(),
          f"{slug}: onMonthChange fired and logged")
    # external month/year jump (leap-year probe)
    page.select_option("#ctl-month", "1")
    page.wait_for_timeout(150)
    check(heading_text(page) == "February 2026", f"{slug}: external month select drives the calendar")
    page.select_option("#ctl-year", "2024")
    page.wait_for_timeout(150)
    check(heading_text(page) == "February 2024", f"{slug}: external year select drives the calendar")
    check(page.locator('[role="gridcell"] button').count() == 29, f"{slug}: leap February renders 29 days")
    page.select_option("#ctl-year", "2026")
    page.wait_for_timeout(150)
    check(page.locator('[role="gridcell"] button').count() == 28, f"{slug}: non-leap February renders 28 days")
    # controlled selection still works after the jumps
    page.locator('[data-cal-focus="20260210"]').click()
    page.wait_for_timeout(150)
    check("Selected: Feb 10, 2026" in page.locator("#controlled-readout").text_content(),
          f"{slug}: selection flows through onSelect")
    check("select → Feb 10, 2026" in page.locator("#controlled-log").text_content(),
          f"{slug}: onSelect fired and logged")
    # locale switching re-renders labels via Intl
    page.select_option("#ctl-locale", "fr-FR")
    page.wait_for_timeout(200)
    check(heading_text(page) == "février 2026", f"{slug}: fr-FR heading")
    check(page.locator('[data-cal-focus="20260210"]').get_attribute("aria-label") == "mardi 10 février 2026",
          f"{slug}: fr-FR day labels")
    page.select_option("#ctl-locale", "ja-JP")
    page.wait_for_timeout(200)
    check(heading_text(page) == "2026年2月", f"{slug}: ja-JP heading")
    # jump button
    page.select_option("#ctl-locale", "en-US")
    page.get_by_role("button", name="Jump to Feb 2024").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "February 2024", f"{slug}: external jump button")
    page.close()


def check_theme_focus_motion(browser):
    slug = "calendar"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    open_preview(page, slug)

    # focus-visible ring on a keyboard-focused day
    page.locator('[data-cal-focus="20260814"]').click()
    page.wait_for_timeout(150)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(150)
    ring = page.evaluate("""() => {
      const s = getComputedStyle(document.activeElement);
      return { w: s.outlineWidth, style: s.outlineStyle };
    }""")
    check(focus_key(page) == "20260815", "focus-visible: keyboard focus on the moved day")
    check(ring["w"] == "2px" and ring["style"] in ("solid", "auto"),
          f"focus-visible: 2px outline ring (got {ring})")

    # dark-mode token flip (body surface + selected-day fill)
    page.locator('[data-cal-focus="20260815"]').click()
    page.wait_for_timeout(150)
    light = page.evaluate("""() => ({
      body: getComputedStyle(document.body).backgroundColor,
      sel: getComputedStyle(document.querySelector('[role=\\'gridcell\\'][aria-selected=\\'true\\'] button')).backgroundColor,
    })""")
    page.locator("#ds-theme-toggle").click()
    page.wait_for_timeout(300)
    dark = page.evaluate("""() => ({
      body: getComputedStyle(document.body).backgroundColor,
      sel: getComputedStyle(document.querySelector('[role=\\'gridcell\\'][aria-selected=\\'true\\'] button')).backgroundColor,
    })""")
    check(light["body"] != dark["body"], "dark mode: body background flips")
    check(light["sel"] != dark["sel"], "dark mode: selected-day fill flips")
    check(dark["sel"] == "rgb(250, 250, 250)", f"dark mode: selected fill uses dark primary ({dark['sel']})")
    page.locator("#ds-theme-toggle").click()
    page.wait_for_timeout(200)

    # reduced motion collapses the state transitions
    page.emulate_media(reduced_motion="reduce")
    page.wait_for_timeout(100)
    tp = page.evaluate("getComputedStyle(document.querySelector('[role=\\'gridcell\\'] button')).transitionProperty")
    check(tp == "none", f"reduced motion: day transitions collapse (got {tp})")
    page.close()


def browser_checks():
    from playwright.sync_api import sync_playwright

    print("browser checks")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        generic_browser_checks(browser)
        check_reference(browser)
        check_single(browser)
        check_range(browser)
        check_multiple(browser)
        check_disabled(browser)
        check_min_max(browser)
        check_week_numbers(browser)
        check_outside_days(browser)
        check_month_picker(browser)
        check_year_picker(browser)
        check_footer(browser)
        check_controlled(browser)
        check_theme_focus_motion(browser)
        browser.close()


def process_checks():
    print("process checks")
    gen = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_calendar.py"), "--check"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    check(gen.returncode == 0, f"generator --check drift-free ({gen.stdout.strip()} {gen.stderr.strip()[:200]})")
    val = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate.py")],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    check(val.returncode == 0, f"scripts/validate.py passes ({val.stdout.strip()[-200:]} {val.stderr.strip()[-200:]})")


def main():
    static_checks()
    unit_checks()
    browser_checks()
    process_checks()
    print(f"\n{checks} checks, {len(failures)} failures, {len(skips)} skipped")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("ALL PASSED")


if __name__ == "__main__":
    main()
