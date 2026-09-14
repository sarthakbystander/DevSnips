#!/usr/bin/env python3
"""QA harness for the DevSnips React DatePicker family.

Static checks (per variant):
  - 5-file shape (code.tsx, code.jsx, preview.html, metadata.json, README.md)
  - metadata.json valid + required schema fields
  - no `any` in code.tsx, no `<div onClick`, no inline `style=`, no hex colors
    (except `#000` inside `color-mix` hover darkening)
  - date-model guards: no `toISOString`, no `Date.UTC`, no `.setDate()` /
    `.setMonth()` / `.setFullYear()` / `.setHours()` mutation, no `Date.parse`
  - dialog + grid semantics markers, roving tabindex, Intl formatting
  - TSX/JSX export parity (same exported names + default export) and
    prop-name parity for every exported component signature
  - shared-core equality across all 10 variants (header-comment-neutralized)

Date-unit checks (Node, when the esbuild toolchain is available):
  - the exported date utilities are bundled from the actual reference
    code.tsx and driven through leap years, month lengths, month/year
    boundaries, clamping, ISO formatting, and DST-transition timezones

Browser checks (Playwright, per preview):
  - 0 console errors, 0 page errors; 0 horizontal overflow @ 375/768/1280
  - dialog semantics (role, aria-haspopup, aria-expanded, aria-controls)
  - grid semantics, roving tabindex, locale labels, aria-current="date"
  - selection + close-on-select, focus restoration, Escape, outside click
  - range: start/end/incomplete/same-day/hover preview/clear
  - presets: value mutation + active tracking
  - constraints: disabled days, min/max nav clamping, keyboard skipping
  - form: label/describedby/aria-invalid/required/hidden ISO value
  - footer apply flow: staged vs committed, Apply/Clear/Today/Escape
  - date-time: selects disabled-until-date, time mutation, ISO, clear
  - month/year pickers: entry view, view cycle, leap year, year paging
  - mobile: bottom sheet at 375 (overlay + full-width + 44px cells), popover at desktop
  - focus-visible ring; dark-mode token flip; reduced-motion guard

Run: python3 scripts/_qa_react_datepicker.py
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATEPICKER = ROOT / "React/Components/DatePicker"
ESBUILD = Path("/tmp/dsbuild/node_modules/.bin/esbuild")
DSBUILD = Path("/tmp/dsbuild")
SLUGS = [
    "date-picker",
    "date-picker-with-label",
    "date-picker-range",
    "date-picker-with-presets",
    "date-picker-with-disabled-dates",
    "date-picker-with-error",
    "date-picker-month-year",
    "date-picker-with-footer",
    "date-picker-date-time",
    "date-picker-mobile",
]
FILES = ["code.tsx", "code.jsx", "preview.html", "metadata.json", "README.md"]
WIDTHS = [375, 768, 1280]
CORE_EXPORTS = [
    "daysInMonth", "isLeapYear", "compareDays", "isSameDay", "addDays",
    "addMonths", "startOfMonth", "endOfMonth", "buildMonthWeeks",
    "formatISODate", "formatISODateTime", "useDatePicker", "DatePicker",
    "DatePickerInput", "DatePickerTrigger", "DatePickerContent",
    "DatePickerHeader", "DatePickerCalendar", "DatePickerFooter",
    "DatePickerPresets", "DatePickerToday", "DatePickerClear",
    "DatePickerApply", "DatePickerTime",
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
    start = m.end() - 1
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
        folder = DATEPICKER / slug
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
        check(meta["category"] == "DatePicker", f"{slug}: category DatePicker")
        check(meta["component"] == "date-picker", f"{slug}: component date-picker")
        check(meta["family"] == "datepicker", f"{slug}: family datepicker")
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
        check('role="dialog"' in tsx, f"{slug}: role=dialog present")
        check('role="grid"' in tsx, f"{slug}: role=grid present")
        check('role="gridcell"' in tsx, f"{slug}: role=gridcell present")
        check("aria-selected" in tsx, f"{slug}: aria-selected present")
        check('aria-haspopup="dialog"' in tsx, f"{slug}: aria-haspopup=dialog on controls")
        check("aria-expanded" in tsx, f"{slug}: aria-expanded on controls")
        check('aria-current={isToday ? "date" : undefined}' in tsx, f"{slug}: aria-current=date for today")
        check('aria-live="polite"' in tsx, f"{slug}: aria-live heading")
        check("motion-reduce:transition-none" in tsx, f"{slug}: reduced-motion guard")
        check("tabIndex=" in tsx, f"{slug}: roving tabindex")
        check("Intl.DateTimeFormat" in tsx, f"{slug}: locale-aware Intl formatting")
        check("requireApply" in tsx, f"{slug}: staged-draft support")
        check("mobileSheet" in tsx, f"{slug}: mobile sheet support")

        tsx_exports = re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx)
        jsx_exports = re.findall(r"export \{([^}]*)\}", jsx)
        jsx_names = [n.strip() for n in jsx_exports[0].split(",")] if jsx_exports else []
        for name in CORE_EXPORTS:
            check(name in tsx_exports, f"{slug}: exports {name}")
        check(sorted(tsx_exports) == sorted(jsx_names),
              f"{slug}: export parity {len(tsx_exports)} vs {len(jsx_names)}")
        check("export default DatePicker;" in jsx, f"{slug}: JSX default export")
        check("interface " not in jsx and ": string" not in jsx, f"{slug}: JSX types stripped")
        for name in ("DatePicker", "DatePickerInput", "DatePickerTrigger", "DatePickerContent",
                     "DatePickerHeader", "DatePickerCalendar", "DatePickerFooter",
                     "DatePickerPresets", "DatePickerToday", "DatePickerClear",
                     "DatePickerApply", "DatePickerTime", "useDatePicker"):
            tp, jp = prop_signature(tsx, name), prop_signature(jsx, name)
            check(tp == jp, f"{slug}: {name} prop parity {tp} vs {jp}")

        readme = (folder / "README.md").read_text()
        for section in ("## Installation", "## Usage", "## Props", "## Compound Components",
                        "## Controlled Usage", "## Uncontrolled Usage",
                        "## Date and Value Representation", "## Validation",
                        "## Keyboard Interaction", "## Accessibility",
                        "## Responsive Behavior", "## Styling", "## Design Tokens",
                        "## Notes", "## Limitations"):
            check(section in readme, f"{slug}: README section {section}")

        cores[slug] = neutralize_core(tsx)

    ref = cores[SLUGS[0]]
    for slug, core in cores.items():
        check(core == ref, f"{slug}: shared core identical to reference")


NODE_TEST = r'''
import {
  daysInMonth, isLeapYear, addDays, addMonths, startOfMonth, endOfMonth,
  compareDays, isSameDay, buildMonthWeeks, formatISODate, formatISODateTime,
} from "./qa-dp.mjs";
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
// day arithmetic across month/year boundaries
t("Jan 31 + 1d = Feb 1", isSameDay(addDays(d(2026,0,31),1), d(2026,1,1)));
t("Dec 31 + 1d = Jan 1 next year", (() => { const r = addDays(d(2026,11,31),1); return r.getFullYear()===2027 && r.getMonth()===0 && r.getDate()===1; })());
t("Jan 1 - 1d = Dec 31 prev year", (() => { const r = addDays(d(2026,0,1),-1); return r.getFullYear()===2025 && r.getMonth()===11 && r.getDate()===31; })());
t("Feb 28 2024 + 1 = Feb 29", isSameDay(addDays(d(2024,1,28),1), d(2024,1,29)));
t("Feb 29 2024 + 1 = Mar 1", isSameDay(addDays(d(2024,1,29),1), d(2024,2,1)));
// month arithmetic with clamping
t("Jan 31 + 1mo = Feb 28 (2026)", isSameDay(addMonths(d(2026,0,31),1), d(2026,1,28)));
t("Jan 31 + 1mo = Feb 29 (2024)", isSameDay(addMonths(d(2024,0,31),1), d(2024,1,29)));
t("Mar 31 - 1mo = Feb 28", isSameDay(addMonths(d(2026,2,31),-1), d(2026,1,28)));
t("Aug 31 + 6mo = Feb 28 2027", isSameDay(addMonths(d(2026,7,31),6), d(2027,1,28)));
// comparison ignores time-of-day
t("compare ignores time", compareDays(d(2026,7,22), new Date(2026,7,22,23,59)) === 0);
t("compare lt", compareDays(d(2026,7,21), d(2026,7,22)) === -1);
t("compare gt across year", compareDays(d(2027,0,1), d(2026,11,31)) === 1);
// grid building
const aug = buildMonthWeeks(d(2026,7,1), 0);
t("6x7 grid", aug.length === 6 && aug.every(r => r.length === 7));
t("Aug 2026 Sun-start first = Jul 26", isSameDay(aug[0][0], d(2026,6,26)));
t("Aug 2026 Sun-start last = Sep 5", isSameDay(aug[5][6], d(2026,8,5)));
t("Aug 2026 Mon-start first = Jul 27", isSameDay(buildMonthWeeks(d(2026,7,1), 1)[0][0], d(2026,6,27)));
// ISO formatting is local-parts based (no UTC shift)
t("ISO basic", formatISODate(d(2026,7,5)) === "2026-08-05");
t("ISO pads", formatISODate(d(2026,0,3)) === "2026-01-03");
t("ISO year edge", formatISODate(d(2026,11,31)) === "2026-12-31");
t("ISO datetime", formatISODateTime(new Date(2026,7,20,9,30)) === "2026-08-20T09:30");
t("ISO datetime pads", formatISODateTime(new Date(2026,0,2,0,5)) === "2026-01-02T00:05");
t("ISO leap", formatISODate(d(2024,1,29)) === "2024-02-29");
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
    bundle = DSBUILD / "qa-dp.mjs"
    test = DSBUILD / "qa-dp-test.mjs"
    try:
        subprocess.run(
            [str(ESBUILD), str(DATEPICKER / "date-picker/code.tsx"), "--format=esm",
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
    page.goto((DATEPICKER / slug / "preview.html").as_uri())
    page.wait_for_selector("#ds-root *", timeout=15000)
    page.wait_for_timeout(500)
    return errors


def no_overflow(page, slug, state):
    for w in WIDTHS:
        page.set_viewport_size({"width": w, "height": 900})
        page.wait_for_timeout(150)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(overflow <= 0, f"{slug}: no horizontal overflow ({state}) @ {w} (got {overflow})")
    page.set_viewport_size({"width": 1280, "height": 900})


def focus_key(page) -> str:
    return page.evaluate(
        "(document.activeElement && document.activeElement.dataset && document.activeElement.dataset.dpFocus) || ''"
    )


def heading_text(page) -> str:
    return page.locator("#ds-root [role='dialog'] h2").first.text_content().strip()


def open_first_picker(page, slug):
    """Open the first date picker on the page via its trigger."""
    page.get_by_role("button", name="Open calendar").first.click()
    page.wait_for_selector('[role="dialog"]', timeout=5000)
    page.wait_for_timeout(250)


def generic_browser_checks(browser):
    print("generic browser checks (per variant)")
    for slug in SLUGS:
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = open_preview(page, slug)
        check(not errors, f"{slug}: no console/page errors {errors[:3]}")
        # field semantics before opening
        check(page.locator('#ds-root input[aria-haspopup="dialog"]').count() >= 1,
              f"{slug}: input carries aria-haspopup=dialog")
        first_input = page.locator('#ds-root input[aria-haspopup="dialog"]').first
        check(first_input.get_attribute("aria-expanded") == "false",
              f"{slug}: input aria-expanded=false while closed")
        check(first_input.get_attribute("readonly") is not None,
              f"{slug}: display input is read-only")
        # no nested interactive elements
        check(page.evaluate(NESTED_JS), f"{slug}: no nested interactive elements")
        no_overflow(page, slug, "closed")

        # open + dialog semantics
        open_first_picker(page, slug)
        dialog = page.get_by_role("dialog")
        check(dialog.count() == 1, f"{slug}: one role=dialog while open")
        check(dialog.first.get_attribute("aria-label") is not None and
              dialog.first.get_attribute("aria-label").startswith("Choose"),
              f"{slug}: dialog has an accessible name")
        check(page.locator('#ds-root input[aria-haspopup="dialog"]').first.get_attribute("aria-expanded") == "true",
              f"{slug}: input aria-expanded=true while open")
        expanded_id = page.locator('#ds-root input[aria-haspopup="dialog"]').first.get_attribute("aria-controls")
        check(expanded_id == dialog.first.get_attribute("id"),
              f"{slug}: aria-controls points at the dialog id")
        grids = page.locator('[role="dialog"] [role="grid"]')
        check(grids.count() >= 1, f"{slug}: at least one role=grid in dialog")
        # roving tabindex: exactly one tabbable control in the dialog grid(s)
        check(page.locator('[role="dialog"] [role="grid"] button[tabindex="0"]').count() == 1,
              f"{slug}: exactly one tabbable grid control")
        # day grid variants check full labels (skip picker-entry variant)
        if slug != "date-picker-month-year":
            check(page.evaluate(LABELS_JS), f"{slug}: full locale-aware day labels")
        # Escape closes and restores focus to a field control
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        check(page.get_by_role("dialog").count() == 0, f"{slug}: Escape closes the dialog")
        active = page.evaluate("document.activeElement && document.activeElement.tagName")
        check(active in ("INPUT", "BUTTON"), f"{slug}: focus restored to a field control (got {active})")
        page.close()


def check_reference(browser):
    slug = "date-picker"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    # controlled demo: initial value + external clear
    inp = page.locator("#dp-ref-input")
    check(inp.input_value() == "Aug 14, 2026", f"{slug}: controlled value displayed")

    # open via trigger, pick a day, auto-close, readout, focus restore
    page.get_by_role("button", name="Open calendar").first.click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    check(heading_text(page) == "August 2026", f"{slug}: opens on the selection's month")
    page.locator('[data-dp-focus="20260820"]').click()
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 0, f"{slug}: closes after single selection")
    check(inp.input_value() == "Aug 20, 2026", f"{slug}: input shows the picked date")
    check("Aug 20, 2026" in page.locator("#dp-ref-readout").text_content(), f"{slug}: readout updates")
    check(page.locator('[role="dialog"]').count() == 0, f"{slug}: dialog unmounted after close")
    active = page.evaluate("document.activeElement && document.activeElement.getAttribute('aria-label')")
    check(active == "Open calendar", f"{slug}: focus restored to the trigger (got {active})")

    # re-click selected day: no deselect (closes, value kept)
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.locator('[data-dp-focus="20260820"]').click()
    page.wait_for_timeout(250)
    check(inp.input_value() == "Aug 20, 2026", f"{slug}: re-clicking the selected day never deselects")

    # external clear (controlled parent)
    page.locator("#dp-ref-clear").click()
    page.wait_for_timeout(150)
    check(inp.input_value() == "", f"{slug}: controlled parent clears the value")

    # month navigation via nav buttons
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.get_by_role("button", name="Go to next month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "September 2026", f"{slug}: next month navigates")
    page.get_by_role("button", name="Go to previous month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "August 2026", f"{slug}: previous month navigates")

    # full keyboard model on the grid (anchors relative to today, which the
    # opening focus follows when nothing is selected)
    today_key = page.evaluate(
        "(() => { const n = new Date(); return n.getFullYear() * 10000 + (n.getMonth() + 1) * 100 + n.getDate(); })()"
    )
    check(focus_key(page) == str(today_key), f"{slug}: opening focuses today (got {focus_key(page)})")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(100)
    check(int(focus_key(page)) == today_key + 1, f"{slug}: ArrowRight moves to next day")
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(100)
    check(int(focus_key(page)) == today_key + 8, f"{slug}: ArrowDown moves a week down")
    page.keyboard.press("ArrowLeft")
    page.wait_for_timeout(100)
    check(int(focus_key(page)) == today_key + 7, f"{slug}: ArrowLeft moves to previous day")
    page.keyboard.press("ArrowUp")
    page.wait_for_timeout(100)
    check(focus_key(page) == str(today_key), f"{slug}: ArrowUp moves a week up")
    home_key = page.evaluate(
        "(key) => { const y = Math.floor(key / 10000), m = Math.floor((key % 10000) / 100) - 1, d = key % 100; const dt = new Date(y, m, d); const back = new Date(y, m, d - dt.getDay()); return back.getFullYear() * 10000 + (back.getMonth() + 1) * 100 + back.getDate(); }",
        today_key,
    )
    page.keyboard.press("Home")
    page.wait_for_timeout(100)
    check(focus_key(page) == str(home_key), f"{slug}: Home moves to week start")
    page.keyboard.press("End")
    page.wait_for_timeout(100)
    check(focus_key(page) == str(today_key), f"{slug}: End moves to week end")
    page.keyboard.press("PageDown")
    page.wait_for_timeout(200)
    check(heading_text(page) == "September 2026", f"{slug}: PageDown pages the month")
    page.keyboard.press("Shift+PageDown")
    page.wait_for_timeout(200)
    check(heading_text(page) == "September 2027", f"{slug}: Shift+PageDown pages a year")
    page.keyboard.press("Shift+PageUp")
    page.wait_for_timeout(200)
    check(heading_text(page) == "September 2026", f"{slug}: Shift+PageUp pages a year back")
    # Enter selects
    page.keyboard.press("Enter")
    page.wait_for_timeout(250)
    check(inp.input_value().startswith("Sep "), f"{slug}: Enter selects the focused day")
    check(page.get_by_role("dialog").count() == 0, f"{slug}: keyboard selection closes")
    check(page.evaluate("document.activeElement.id") == "dp-ref-input",
          f"{slug}: focus restored to the input after keyboard selection")

    # today is marked, not auto-selected
    today_state = page.evaluate("""() => ({
      marked: document.querySelectorAll('[aria-current="date"]').length,
    })""")
    check(today_state["marked"] <= 1, f"{slug}: at most one aria-current=date")

    # uncontrolled demo: opens on today's month, keyboard select works
    page.locator("#dp-ref-uncontrolled").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    now = page.evaluate("(() => { const n = new Date(); return { y: n.getFullYear(), m: n.getMonth() }; })()")
    expected = page.evaluate(
        "(n) => new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(new Date(n.y, n.m, 1))",
        now,
    )
    check(heading_text(page) == expected, f"{slug}: uncontrolled opens on today's month")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(100)
    page.keyboard.press("Enter")
    page.wait_for_timeout(250)
    uinp = page.locator("#dp-ref-uncontrolled")
    check(uinp.input_value() != "", f"{slug}: uncontrolled selection commits")
    check("requested" in page.locator("#dp-ref-uncontrolled-readout").text_content(),
          f"{slug}: uncontrolled readout updates")

    # open dialog overflow at all widths
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    no_overflow(page, slug, "dialog open")
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    page.close()


def check_with_label(browser):
    slug = "date-picker-with-label"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    inp = page.locator('#ds-root input[aria-haspopup="dialog"]').first
    # real label association: htmlFor -> id, clicking the label focuses the input
    label = page.locator("label", has_text="Appointment date")
    check(label.count() == 1, f"{slug}: label element rendered")
    check(label.first.get_attribute("for") == inp.get_attribute("id"),
          f"{slug}: label htmlFor matches the input id")
    check(inp.get_attribute("aria-required") == "true", f"{slug}: aria-required on the input")
    # description + helper registered in aria-describedby, pointing at real nodes
    described = (inp.get_attribute("aria-describedby") or "").split()
    check(len(described) == 2, f"{slug}: aria-describedby carries description + helper ids {described}")
    resolved = page.evaluate(
        "(ids) => ids.every((id) => !!document.getElementById(id))", described
    )
    check(resolved, f"{slug}: every describedby id resolves to a real node")
    texts = page.evaluate(
        "(ids) => ids.map((id) => document.getElementById(id).textContent)", described
    )
    check(any("documents" in t for t in texts), f"{slug}: description text is associated")
    check(any("08:00" in t for t in texts), f"{slug}: helper text is associated")
    label.first.click()
    page.wait_for_timeout(250)
    # clicking the label activates the associated control — which opens the
    # picker and moves focus into the grid (the dialog pattern)
    check(page.get_by_role("dialog").count() == 1,
          f"{slug}: clicking the label activates the associated control (opens the picker)")
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    # required marker is presentation-only
    marker = page.evaluate(
        "document.querySelector('label span[aria-hidden=\"true\"]') !== null"
    )
    check(marker, f"{slug}: required marker is aria-hidden")
    # select through the field
    page.locator('#ds-root input[aria-haspopup="dialog"]').first.click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.get_by_role("button", name="Go to next month").click()
    page.wait_for_timeout(150)
    page.locator('[data-dp-focus="20260910"]').click()
    page.wait_for_timeout(250)
    check("Sep 10, 2026" in page.locator("#dp-label-readout").text_content(),
          f"{slug}: labelled picker selects + announces")
    page.close()


def check_range(browser):
    slug = "date-picker-range"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    inp = page.locator("#dp-range-input")
    check(inp.input_value() == "", f"{slug}: starts empty")
    open_first_picker(page, slug)
    check(page.locator('[role="dialog"] [role="grid"]').count() == 2,
          f"{slug}: two month grids rendered")
    check(heading_text(page) == "August – September 2026", f"{slug}: two-month heading")

    # incomplete range
    page.locator('[data-dp-focus="20260810"]').click()
    page.wait_for_timeout(200)
    check(page.get_by_role("dialog").count() == 1, f"{slug}: stays open while the range is incomplete")
    check("Select an end date." in page.locator("#dp-range-summary").text_content(),
          f"{slug}: incomplete state summarized")
    check("end pending" in page.locator("#dp-range-readout").text_content(),
          f"{slug}: readout shows the pending range")
    check(page.locator('[role="gridcell"][aria-selected="true"]').count() == 1,
          f"{slug}: only the start day is selected mid-range")

    # hover preview: middle cells between from and hovered, distinct from committed middle
    page.locator('[data-dp-focus="20260817"]').hover()
    page.wait_for_timeout(150)
    preview_count = page.evaluate(
        """() => Array.from(document.querySelectorAll('[role="gridcell"] button'))
          .filter((b) => b.className.includes('surface-hover') && b.className.includes('rounded-none')).length"""
    )
    check(preview_count == 6, f"{slug}: hover preview paints 6 middle cells (got {preview_count})")
    check(page.locator('[role="gridcell"][aria-selected="true"]').count() == 1,
          f"{slug}: hover preview does not fake selection")

    # complete the range -> closes, display + summary
    page.locator('[data-dp-focus="20260817"]').click()
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 0, f"{slug}: closes when the range completes")
    check(inp.input_value() == "Aug 10, 2026 – Aug 17, 2026",
          f"{slug}: input shows the completed range (got {inp.input_value()!r})")
    check("Trip: Aug 10, 2026 to Aug 17, 2026." in page.locator("#dp-range-readout").text_content(),
          f"{slug}: readout shows the completed trip")

    # range treatments: start/end filled, middle is a band (reopen to inspect)
    page.locator("#dp-range-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    check("7 nights" in page.locator("#dp-range-summary").text_content(),
          f"{slug}: summary computes nights")
    start_cls = page.locator('[data-dp-focus="20260810"]').get_attribute("class") or ""
    mid_cls = page.locator('[data-dp-focus="20260812"]').get_attribute("class") or ""
    end_cls = page.locator('[data-dp-focus="20260817"]').get_attribute("class") or ""
    check("primary" in start_cls and "primary" in end_cls, f"{slug}: range endpoints filled")
    check("surface-active" in mid_cls and "rounded-none" in mid_cls, f"{slug}: range middle band")
    check(page.locator('[role="gridcell"][aria-selected="true"]').count() == 8,
          f"{slug}: all 8 range days selected")

    # same-day range
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    page.locator("#dp-range-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.locator('[data-dp-focus="20260824"]').click()
    page.wait_for_timeout(200)
    page.locator('[data-dp-focus="20260824"]').click()
    page.wait_for_timeout(250)
    check(inp.input_value() == "Aug 24, 2026 – Aug 24, 2026",
          f"{slug}: same-day range completes (got {inp.input_value()!r})")

    # clear range
    page.locator("#dp-range-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.get_by_role("button", name="Clear").click()
    page.wait_for_timeout(200)
    check(inp.input_value() == "", f"{slug}: clear empties the range")
    check("No trip dates" in page.locator("#dp-range-readout").text_content(),
          f"{slug}: readout resets after clear")
    page.close()


def check_presets(browser):
    slug = "date-picker-with-presets"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    open_first_picker(page, slug)
    group = page.locator('[role="group"][aria-label="Date presets"]')
    check(group.count() == 1, f"{slug}: preset group rendered with accessible label")
    check(group.first.locator("button").count() == 5, f"{slug}: 5 preset buttons")

    # Today preset: same-day range of today, popover closes, input updated
    today_fmt = page.evaluate(
        "new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date())"
    )
    group.first.get_by_role("button", name="Today").click()
    page.wait_for_timeout(250)
    inp = page.locator("#dp-preset-input")
    check(inp.input_value() == f"{today_fmt} – {today_fmt}",
          f"{slug}: Today preset sets a same-day range (got {inp.input_value()!r})")
    check(page.get_by_role("dialog").count() == 0, f"{slug}: preset closes the popover")

    # active tracking: reopen, Today carries aria-current=date
    open_first_picker(page, slug)
    active = group.first.locator('button[aria-current="date"]')
    check(active.count() == 1 and active.first.text_content().strip() == "Today",
          f"{slug}: active preset tracked with aria-current=date")

    # Last 7 days: from = today - 6
    group.first.get_by_role("button", name="Last 7 days").click()
    page.wait_for_timeout(250)
    expected = page.evaluate(
        """() => {
          const f = (d) => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(d);
          const now = new Date();
          const from = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 6);
          return f(from) + " – " + f(now);
        }"""
    )
    check(inp.input_value() == expected,
          f"{slug}: Last 7 days preset sets the real range (got {inp.input_value()!r})")
    check("Window:" in page.locator("#dp-preset-readout").text_content(),
          f"{slug}: readout follows the preset value")

    # This month: from = 1st, to = last of the current month
    open_first_picker(page, slug)
    group.first.get_by_role("button", name="This month").click()
    page.wait_for_timeout(250)
    expected_month = page.evaluate(
        """() => {
          const f = (d) => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(d);
          const now = new Date();
          const first = new Date(now.getFullYear(), now.getMonth(), 1);
          const last = new Date(now.getFullYear(), now.getMonth() + 1, 0);
          return f(first) + " – " + f(last);
        }"""
    )
    check(inp.input_value() == expected_month,
          f"{slug}: This month preset spans the month (got {inp.input_value()!r})")
    page.close()


def check_disabled(browser):
    slug = "date-picker-with-disabled-dates"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    open_first_picker(page, slug)
    check(heading_text(page) == "August 2026", f"{slug}: opens on the default month")

    # min/max clamping: previous month (July) entirely before minDate=Aug 3
    check(page.get_by_role("button", name="Go to previous month").is_disabled(),
          f"{slug}: previous nav disabled at the min boundary")
    check(not page.get_by_role("button", name="Go to next month").is_disabled(),
          f"{slug}: next nav enabled inside the window")

    # weekend + hold disabled natively (Aug 8 2026 = Saturday, Aug 15 = hold)
    for key, why in (("20260808", "weekend"), ("20260815", "holiday hold"), ("20260816", "weekend")):
        btn = page.locator(f'[data-dp-focus="{key}"]')
        check(btn.is_disabled(), f"{slug}: {key} disabled ({why})")
    # weekday selectable
    page.locator('[data-dp-focus="20260817"]').click()
    page.wait_for_timeout(250)
    check(page.locator("#dp-disabled-input").input_value() == "Aug 17, 2026",
          f"{slug}: weekday inside the window selects")
    check("Exam on Aug 17, 2026." in page.locator("#dp-disabled-readout").text_content(),
          f"{slug}: readout follows selection")

    # keyboard skipping: from Friday Aug 14, ArrowRight skips the disabled 15th (hold) + 16th (Sun)
    page.locator("#dp-disabled-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.locator('[data-dp-focus="20260814"]').focus()
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(150)
    check(focus_key(page) == "20260817", f"{slug}: ArrowRight skips disabled days (got {focus_key(page)})")

    # max boundary: nav to September, next becomes disabled when only out-of-window months remain
    page.get_by_role("button", name="Go to next month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "September 2026", f"{slug}: navigates to the max month")
    check(page.get_by_role("button", name="Go to next month").is_disabled(),
          f"{slug}: next nav disabled at the max boundary")
    # out-of-window day disabled (Sep 26 > maxDate Sep 25)
    check(page.locator('[data-dp-focus="20260926"]').count() == 0 or
          page.locator('[data-dp-focus="20260926"]').is_disabled(),
          f"{slug}: out-of-window days disabled")
    page.close()


def check_with_error(browser):
    slug = "date-picker-with-error"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    inp = page.locator("#dp-error-input")
    check(inp.get_attribute("aria-required") == "true", f"{slug}: aria-required present")
    check(inp.get_attribute("aria-invalid") is None, f"{slug}: no aria-invalid before validation")
    check(page.locator('[role="alert"]').count() == 0, f"{slug}: no error before submit")
    # helper initially owns the message slot
    check("hold your seat" in (page.locator(f'#{inp.get_attribute("aria-describedby")}').text_content()),
          f"{slug}: helper wired via aria-describedby initially")

    # empty submit -> error
    page.locator("#dp-error-submit").click()
    page.wait_for_timeout(200)
    check(page.locator('[role="alert"]').count() == 1, f"{slug}: error renders with role=alert")
    check("Select a departure date." in page.locator('[role="alert"]').text_content(),
          f"{slug}: error message content")
    check(inp.get_attribute("aria-invalid") == "true", f"{slug}: aria-invalid=true with error")
    err_described = (inp.get_attribute("aria-describedby") or "").split()
    check(len(err_described) == 1 and "alert" in page.locator(f'#{err_described[0]}').get_attribute("role"),
          f"{slug}: error id owns the describedby slot")

    # destructive border on the input while invalid
    border = inp.evaluate("(el) => getComputedStyle(el).borderColor")
    check(border == "rgb(194, 38, 27)", f"{slug}: destructive border while invalid (got {border})")

    # hidden input carries the form name and is empty
    hidden = page.locator('input[name="departure"]')
    check(hidden.count() == 1, f"{slug}: hidden form input rendered")
    check(hidden.first.get_attribute("value") == "", f"{slug}: hidden value empty before selection")

    # pick a date -> error resolves, helper returns, hidden ISO value
    page.locator("#dp-error-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.locator('[data-dp-focus="20260821"]').click()
    page.wait_for_timeout(250)
    check(page.locator('[role="alert"]').count() == 0, f"{slug}: error clears on selection")
    check(inp.get_attribute("aria-invalid") is None, f"{slug}: aria-invalid clears on selection")
    check("hold your seat" in (page.locator(f'#{inp.get_attribute("aria-describedby")}').text_content()),
          f"{slug}: helper returns after the error clears")
    check(hidden.first.get_attribute("value") == "2026-08-21", f"{slug}: hidden input carries the ISO date")

    # valid submit -> confirmation announced
    page.locator("#dp-error-submit").click()
    page.wait_for_timeout(200)
    check("Booking requested for Aug 21, 2026." in page.locator("#dp-error-sent").text_content(),
          f"{slug}: valid submit confirms via role=status")
    page.close()


def check_month_year(browser):
    slug = "date-picker-month-year"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    open_first_picker(page, slug)
    # entry view: month picker
    months_grid = page.locator('[role="dialog"] [role="grid"]')
    check(months_grid.first.get_attribute("aria-label") == "Choose a month in 2026",
          f"{slug}: opens directly in the month picker")
    check(months_grid.first.locator("button").count() == 12, f"{slug}: 12 month options")
    check(heading_text(page) == "2026", f"{slug}: heading shows the year")

    # keyboard: arrows + PageUp/PageDown in the month picker
    check(focus_key(page) == "m7", f"{slug}: current month focused (got {focus_key(page)})")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(100)
    check(focus_key(page) == "m8", f"{slug}: ArrowRight moves to the next month")
    page.keyboard.press("PageDown")
    page.wait_for_timeout(200)
    check(heading_text(page) == "2027", f"{slug}: PageDown pages a year in the picker")
    page.keyboard.press("PageUp")
    page.wait_for_timeout(200)
    check(heading_text(page) == "2026", f"{slug}: PageUp pages back")

    # pick February 2026 -> day grid of Feb 2026 (28 in-month days; outside
    # cells belong to neighbouring months)
    page.locator('[data-dp-focus="m1"]').click()
    page.wait_for_timeout(250)
    check(heading_text(page) == "February 2026", f"{slug}: month choice returns to the day grid")
    feb26 = page.evaluate(
        "Array.from(document.querySelectorAll('[role=\\\"gridcell\\\"] button')).filter((b) => (b.getAttribute('aria-label') || '').includes('February') && (b.getAttribute('aria-label') || '').includes('2026')).length"
    )
    check(feb26 == 28, f"{slug}: Feb 2026 renders 28 in-month days (got {feb26})")

    # year picker via the heading cycle
    page.get_by_role("button", name="February 2026 — activate to choose a month").click()
    page.wait_for_timeout(200)
    page.get_by_role("button", name="2026 — activate to choose a year").click()
    page.wait_for_timeout(200)
    check(page.locator('[role="dialog"] [role="grid"]').first.get_attribute("aria-label") == "Choose a year",
          f"{slug}: heading cycles to the year picker")
    check(page.locator('[role="dialog"] [role="gridcell"]').count() == 12,
          f"{slug}: 12-year page (no giant year dropdown)")
    # the 2024–2035 page contains 2024 — pick it directly (leap year check)
    page.locator('[data-dp-focus="y2024"]').click()
    page.wait_for_timeout(200)
    check(heading_text(page) == "2024", f"{slug}: year choice returns to the month picker")
    page.locator('[data-dp-focus="m1"]').click()
    page.wait_for_timeout(250)
    check(heading_text(page) == "February 2024", f"{slug}: landed on Feb 2024")
    feb24 = page.evaluate(
        "Array.from(document.querySelectorAll('[role=\\\"gridcell\\\"] button')).filter((b) => (b.getAttribute('aria-label') || '').includes('February') && (b.getAttribute('aria-label') || '').includes('2024')).length"
    )
    check(feb24 == 29, f"{slug}: Feb 2024 renders 29 in-month days (leap year, got {feb24})")
    # leap day selects
    page.locator('[data-dp-focus="20240229"]').click()
    page.wait_for_timeout(250)
    check(page.locator("#dp-my-input").input_value() == "Feb 29, 2024",
          f"{slug}: Feb 29 selectable in a leap year")
    check("Feb 29, 2024" in page.locator("#dp-my-readout").text_content(),
          f"{slug}: readout confirms the leap date")
    # reopening resets to the entry view (months of the selection's year)
    page.locator("#dp-my-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    check(page.locator('[role="dialog"] [role="grid"]').first.get_attribute("aria-label") == "Choose a month in 2024",
          f"{slug}: reopening returns to the month picker entry view")
    # Dec -> Jan year rollover through nav buttons
    page.locator('[data-dp-focus="m11"]').click()
    page.wait_for_timeout(250)
    check(heading_text(page) == "December 2024", f"{slug}: December 2024 day grid")
    page.get_by_role("button", name="Go to next month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "January 2025", f"{slug}: Dec -> Jan year rollover")
    page.get_by_role("button", name="Go to previous month").click()
    page.wait_for_timeout(150)
    check(heading_text(page) == "December 2024", f"{slug}: Jan -> Dec rollover back")
    page.close()


def check_footer(browser):
    slug = "date-picker-with-footer"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    inp = page.locator("#dp-footer-input")
    check(inp.input_value() == "Aug 20, 2026", f"{slug}: committed value displayed")

    # staged selection does NOT touch the committed value
    page.locator("#dp-footer-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    check("Aug 20, 2026" in page.locator("#dp-footer-staged").text_content(),
          f"{slug}: staged readout starts from the committed value")
    page.locator('[data-dp-focus="20260825"]').click()
    page.wait_for_timeout(200)
    check(page.get_by_role("dialog").count() == 1, f"{slug}: staging keeps the popover open")
    check(inp.input_value() == "Aug 20, 2026", f"{slug}: staged pick does not commit")
    check("Aug 25, 2026" in page.locator("#dp-footer-staged").text_content(),
          f"{slug}: staged readout tracks the draft")
    check("Effective from Aug 20, 2026." in page.locator("#dp-footer-readout").text_content(),
          f"{slug}: outer value untouched while staging")

    # Apply commits + closes + restores focus
    page.get_by_role("button", name="Apply").click()
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 0, f"{slug}: Apply closes")
    check(inp.input_value() == "Aug 25, 2026", f"{slug}: Apply commits the draft")
    check("Effective from Aug 25, 2026." in page.locator("#dp-footer-readout").text_content(),
          f"{slug}: readout follows the commit")
    check(page.evaluate("document.activeElement.id") == "dp-footer-input",
          f"{slug}: Apply restores focus to the opener")

    # Escape discards the draft
    page.locator("#dp-footer-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.locator('[data-dp-focus="20260826"]').click()
    page.wait_for_timeout(200)
    check("Aug 26, 2026" in page.locator("#dp-footer-staged").text_content(),
          f"{slug}: draft stages again")
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    check(inp.input_value() == "Aug 25, 2026", f"{slug}: Escape discards the draft")

    # reopening restarts from the committed value
    page.locator("#dp-footer-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    check("Aug 25, 2026" in page.locator("#dp-footer-staged").text_content(),
          f"{slug}: reopening restarts from the committed value")

    # Clear empties committed + staged immediately
    page.get_by_role("button", name="Clear").click()
    page.wait_for_timeout(200)
    check(inp.input_value() == "", f"{slug}: Clear empties the committed value immediately")
    check("Nothing staged." in page.locator("#dp-footer-staged").text_content(),
          f"{slug}: Clear empties the staged draft too")
    check(page.get_by_role("button", name="Clear").is_disabled(),
          f"{slug}: Clear disables itself when empty")

    # Today stages (does not commit), Apply commits it
    page.get_by_role("button", name="Today").click()
    page.wait_for_timeout(200)
    today_fmt = page.evaluate(
        "new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date())"
    )
    check(today_fmt in page.locator("#dp-footer-staged").text_content(),
          f"{slug}: Today stages today")
    check(inp.input_value() == "", f"{slug}: Today does not commit")
    page.get_by_role("button", name="Apply").click()
    page.wait_for_timeout(250)
    check(inp.input_value() == today_fmt, f"{slug}: Apply commits today")
    page.close()


def check_date_time(browser):
    slug = "date-picker-date-time"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    hours = page.locator("label", has_text="Hours").locator("select")
    minutes = page.locator("label", has_text="Minutes").locator("select")
    check(hours.count() == 0 and minutes.count() == 0,
          f"{slug}: time selects live inside the popover (0 while closed)")

    page.locator("#dp-dt-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    hours = page.locator("label", has_text="Hours").locator("select")
    minutes = page.locator("label", has_text="Minutes").locator("select")
    check(hours.count() == 1 and minutes.count() == 1, f"{slug}: hour + minute selects rendered")
    check(hours.first.is_disabled() and minutes.first.is_disabled(),
          f"{slug}: time selects disabled until a date exists")
    check("Select a date to set the time." in page.locator('[role="dialog"]').text_content(),
          f"{slug}: disabled state explained")

    # picking a day keeps the popover open (time pending), enables selects
    page.locator('[data-dp-focus="20260820"]').click()
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 1, f"{slug}: withTime keeps the popover open")
    check(not hours.first.is_disabled(), f"{slug}: selects enable after the day pick")
    inp = page.locator("#dp-dt-input")
    check(inp.input_value() == "Aug 20, 2026, 12:00", f"{slug}: day pick defaults to 12:00 (got {inp.input_value()!r})")
    check("2026-08-20T12:00" in page.locator("#dp-dt-iso").text_content(), f"{slug}: ISO readout follows")

    # time mutation updates the committed value live
    hours.first.select_option("9")
    page.wait_for_timeout(150)
    check(inp.input_value() == "Aug 20, 2026, 09:00", f"{slug}: hour change updates the value")
    minutes.first.select_option("30")
    page.wait_for_timeout(150)
    check(inp.input_value() == "Aug 20, 2026, 09:30", f"{slug}: minute change updates the value")
    check("2026-08-20T09:30" in page.locator("#dp-dt-iso").text_content(), f"{slug}: ISO readout updates")
    hidden = page.locator('input[name="checkin"]')
    check(hidden.count() == 1 and hidden.first.get_attribute("value") == "2026-08-20T09:30",
          f"{slug}: hidden input serializes yyyy-mm-ddThh:mm")

    # picking another day preserves the time
    page.locator('[data-dp-focus="20260824"]').click()
    page.wait_for_timeout(200)
    check(inp.input_value() == "Aug 24, 2026, 09:30", f"{slug}: time preserved across day changes")

    # Done closes with focus restored
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 0, f"{slug}: Done closes")
    check(page.evaluate("document.activeElement.id") == "dp-dt-input", f"{slug}: Done restores focus")

    # persisted on reopen; clear resets date + time controls
    page.locator("#dp-dt-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    check(hours.first.input_value() == "9" and minutes.first.input_value() == "30",
          f"{slug}: time persists on reopen")
    page.get_by_role("button", name="Clear").click()
    page.wait_for_timeout(200)
    check(inp.input_value() == "", f"{slug}: clear empties the value")
    check(hours.first.is_disabled(), f"{slug}: clear disables the time selects again")
    check("No value." in page.locator("#dp-dt-iso").text_content(), f"{slug}: ISO readout resets")
    check(hidden.first.get_attribute("value") == "", f"{slug}: hidden input clears")
    page.close()


def check_mobile(browser):
    slug = "date-picker-mobile"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors = open_preview(page, slug)
    check(not errors, f"{slug}: behavior — no console/page errors {errors[:3]}")

    # desktop: popover presentation (absolute), no visible overlay
    open_first_picker(page, slug)
    panel_style = page.locator('[role="dialog"]').first.evaluate(
        "(el) => ({ pos: getComputedStyle(el).position })"
    )
    check(panel_style["pos"] == "absolute", f"{slug}: desktop uses the popover (absolute)")
    overlay_visible = page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root [aria-hidden=\"true\"].fixed')).some((el) => getComputedStyle(el).display !== 'none')"
    )
    check(not overlay_visible, f"{slug}: sheet overlay hidden at desktop")
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)

    # mobile: bottom sheet presentation
    page.set_viewport_size({"width": 375, "height": 800})
    page.wait_for_timeout(200)
    page.locator("#dp-mobile-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(300)
    panel = page.locator('[role="dialog"]').first
    pm = panel.evaluate(
        """(el) => {
          const s = getComputedStyle(el);
          const r = el.getBoundingClientRect();
          return { pos: s.position, left: r.left, right: r.right, bottom: r.bottom, w: r.width, h: r.height, iw: window.innerWidth, vh: window.innerHeight };
        }"""
    )
    check(pm["pos"] == "fixed", f"{slug}: mobile docks the sheet (fixed)")
    check(pm["left"] >= 0 and pm["right"] <= pm["iw"] + 0.5,
          f"{slug}: sheet inside the viewport horizontally ({pm})")
    check(pm["bottom"] <= pm["vh"] + 0.5, f"{slug}: sheet inside the viewport vertically ({pm})")
    check(pm["w"] >= pm["iw"] - 30, f"{slug}: sheet spans nearly the full width ({pm})")
    check(overlay_visible := page.evaluate(
        "Array.from(document.querySelectorAll('#ds-root [aria-hidden=\"true\"].fixed')).some((el) => getComputedStyle(el).display !== 'none')"
    ), f"{slug}: overlay visible on mobile")
    check(page.evaluate(
        "document.querySelector('#ds-root [aria-hidden=\"true\"].fixed').getAttribute('aria-hidden') === 'true'"
    ), f"{slug}: overlay is aria-hidden")

    # 44px touch targets
    cell = page.locator('[role="dialog"] [role="gridcell"] button').first.evaluate(
        "(el) => ({ w: el.getBoundingClientRect().width, h: el.getBoundingClientRect().height })"
    )
    check(cell["w"] == 44 and cell["h"] == 44, f"{slug}: 44px day cells (got {cell})")

    # pick + readout
    page.locator('[data-dp-focus="20260826"]').click()
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 0, f"{slug}: selection closes the sheet")
    check("Visit on Aug 26, 2026." in page.locator("#dp-mobile-readout").text_content(),
          f"{slug}: readout follows the pick")

    # overlay dismissal closes the sheet
    page.locator("#dp-mobile-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(300)
    page.mouse.click(187, 120)
    page.wait_for_timeout(250)
    check(page.get_by_role("dialog").count() == 0, f"{slug}: overlay tap closes the sheet")

    # no horizontal overflow with the sheet open at 375
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(overflow <= 0, f"{slug}: no overflow with the sheet closed @375 (got {overflow})")
    page.locator("#dp-mobile-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(300)
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(overflow <= 0, f"{slug}: no overflow with the sheet open @375 (got {overflow})")
    page.close()


def check_theme_focus_motion(browser):
    slug = "date-picker"
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    open_preview(page, slug)

    # focus-visible ring on a keyboard-focused day (opens on the selected Aug 14)
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(150)
    ring = page.evaluate("""() => {
      const s = getComputedStyle(document.activeElement);
      return { w: s.outlineWidth, style: s.outlineStyle };
    }""")
    check(focus_key(page) == "20260815", "focus-visible: keyboard focus on the moved day")
    check(ring["w"] == "2px" and ring["style"] in ("solid", "auto"),
          f"focus-visible: 2px outline ring (got {ring})")

    # dark-mode token flip (body surface + selected-day fill + panel surface)
    page.locator('[data-dp-focus="20260815"]').click()
    page.wait_for_timeout(250)
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    light = page.evaluate("""() => ({
      body: getComputedStyle(document.body).backgroundColor,
      sel: getComputedStyle(document.querySelector('[role=\\'gridcell\\'][aria-selected=\\'true\\'] button')).backgroundColor,
      panel: getComputedStyle(document.querySelector('[role=\\'dialog\\']')).backgroundColor,
    })""")
    page.locator("#ds-theme-toggle").click()
    page.wait_for_timeout(300)
    # the theme toggle is an outside pointer interaction (closes the dialog) —
    # reopen to measure the dark panel + selected fill
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    dark = page.evaluate("""() => ({
      body: getComputedStyle(document.body).backgroundColor,
      sel: getComputedStyle(document.querySelector('[role=\\'gridcell\\'][aria-selected=\\'true\\'] button')).backgroundColor,
      panel: getComputedStyle(document.querySelector('[role=\\'dialog\\']')).backgroundColor,
    })""")
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    check(light["body"] != dark["body"], "dark mode: body background flips")
    check(light["sel"] != dark["sel"], "dark mode: selected-day fill flips")
    check(dark["sel"] == "rgb(250, 250, 250)", f"dark mode: selected fill uses dark primary ({dark['sel']})")
    check(light["panel"] != dark["panel"], "dark mode: panel surface flips")
    page.locator("#ds-theme-toggle").click()
    page.wait_for_timeout(200)

    # reduced motion collapses the state transitions (day cells only exist
    # while the dialog is open — reopen before measuring)
    page.emulate_media(reduced_motion="reduce")
    page.wait_for_timeout(100)
    page.locator("#dp-ref-input").click()
    page.wait_for_selector('[role="dialog"]')
    page.wait_for_timeout(250)
    tp = page.evaluate("getComputedStyle(document.querySelector('[role=\\'gridcell\\'] button')).transitionProperty")
    check(tp == "none", f"reduced motion: day transitions collapse (got {tp})")
    inp_tp = page.locator("#dp-ref-input").evaluate("(el) => getComputedStyle(el).transitionProperty")
    check(inp_tp == "none", f"reduced motion: input transitions collapse (got {inp_tp})")
    page.close()


def browser_checks():
    from playwright.sync_api import sync_playwright

    print("browser checks")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        generic_browser_checks(browser)
        check_reference(browser)
        check_with_label(browser)
        check_range(browser)
        check_presets(browser)
        check_disabled(browser)
        check_with_error(browser)
        check_month_year(browser)
        check_footer(browser)
        check_date_time(browser)
        check_mobile(browser)
        check_theme_focus_motion(browser)
        browser.close()


def process_checks():
    print("process checks")
    gen = subprocess.run(
        [sys.executable, str(ROOT / "_gen_react_datepicker.py"), "--check"],
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
