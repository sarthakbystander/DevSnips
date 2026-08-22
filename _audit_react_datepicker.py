#!/usr/bin/env python3
"""Consistency + anti-AI audit for the React DatePicker family.

Checks every variant's code.tsx:
  - one shared compound core: everything except the header doc comment is
    byte-identical across all 10 variants
  - exports: the full primitive set (DatePicker + input/trigger/content +
    header/calendar/footer + presets + today/clear/apply + time +
    useDatePicker + date utilities) everywhere
  - semantics: role=dialog/grid, aria-haspopup/expanded/controls, selected
    markers, field wiring, roving tabIndex, keyboard keys, focus restore
  - date logic kept central: the exported local-calendar-date utilities are
    the only date arithmetic (no getTime()+86400000 hacks, no mutation)
  - focus-visible ring token; disabled treatment; motion-reduce guards
  - TSX/JSX export parity (named exports + default match between code.tsx
    and code.jsx)
  - no `any`, no raw hex (except the `#000` color-mix hover derivation), no
    forbidden AI-slop patterns
"""
import re
import sys
from pathlib import Path

DATEPICKER = Path("React/Components/DatePicker")

CORE_EXPORTS = sorted([
    "daysInMonth", "isLeapYear", "compareDays", "isSameDay", "addDays",
    "addMonths", "startOfMonth", "endOfMonth", "buildMonthWeeks",
    "formatISODate", "formatISODateTime", "useDatePicker", "DatePicker",
    "DatePickerInput", "DatePickerTrigger", "DatePickerContent",
    "DatePickerHeader", "DatePickerCalendar", "DatePickerFooter",
    "DatePickerPresets", "DatePickerToday", "DatePickerClear",
    "DatePickerApply", "DatePickerTime",
])

FORBIDDEN = [
    r"purple", r"neon", r"glassmorphism", r"backdrop-filter", r"\bglow\b",
    r"gradient-(to|from|via)", r"bg-gradient", r"\blorem\b", r"style=",
]

fails = []


def header_neutralized(src: str) -> str:
    """Blank the variant's header doc comment so the shared core can be
    compared byte-for-byte across variants."""
    out = re.sub(r"/\*\*.*?\*/", "", src, count=1, flags=re.S)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.rstrip()


dirs = sorted(d for d in DATEPICKER.iterdir() if d.is_dir())
if not dirs:
    print("no date pickers found")
    sys.exit(1)

cores = {}

for d in dirs:
    slug = d.name
    tsx = (d / "code.tsx").read_text()
    jsx = (d / "code.jsx").read_text()

    # -- exports ---------------------------------------------------------
    tsx_names = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
    jsxm = re.findall(r"export \{ ([^}]*) \};", jsx)
    jsx_named = sorted(x.strip() for x in (jsxm[0] or "").split(",")) if jsx else []

    missing = [n for n in CORE_EXPORTS if n not in tsx_names]
    if missing:
        fails.append(f"{slug}: core exports missing: {missing}")
    if tsx_names != jsx_named:
        fails.append(f"{slug}: TSX/JSX named-export parity drift: tsx={tsx_names} jsx={jsx_named}")
    if "export default DatePicker;" not in jsx:
        fails.append(f"{slug}: code.jsx missing default export")

    # -- semantics -------------------------------------------------------
    for needle in ('role="dialog"', 'role="grid"', 'role="gridcell"',
                   'aria-haspopup="dialog"', "aria-expanded", "aria-controls",
                   "aria-selected", 'aria-current={isToday ? "date" : undefined}',
                   "aria-invalid", "aria-required", "aria-describedby",
                   "tabIndex", "onKeyDown", "ArrowLeft", "ArrowRight",
                   "ArrowUp", "ArrowDown", "Home", "End", "PageUp", "PageDown",
                   "Escape", "requestClose", "restoreTargetRef"):
        if needle not in tsx:
            fails.append(f"{slug}: missing {needle}")
    for primitive in ("DatePickerInput", "DatePickerTrigger", "DatePickerContent",
                      "DatePickerHeader", "DatePickerCalendar", "DatePickerFooter",
                      "DatePickerPresets", "DatePickerToday", "DatePickerClear",
                      "DatePickerApply", "DatePickerTime"):
        if f"export function {primitive}" not in tsx:
            fails.append(f"{slug}: missing primitive {primitive}")

    # -- date logic kept central ------------------------------------------
    for util in ("addDays", "addMonths", "compareDays", "isSameDay",
                 "daysInMonth", "buildMonthWeeks", "dayKey"):
        if not re.search(rf"\b{util}\b", tsx):
            fails.append(f"{slug}: central date utility {util} missing")
    no_comments = re.sub(r"//[^\n]*", "", re.sub(r"/\*.*?\*/", "", tsx, flags=re.S))
    if (re.search(r"getTime\(\)\s*[+-]", no_comments) or ".setDate(" in no_comments
            or ".setMonth(" in no_comments):
        fails.append(f"{slug}: timestamp arithmetic or Date mutation found")

    # -- quality bar ------------------------------------------------------
    if "focus-visible:outline-2" not in tsx:
        fails.append(f"{slug}: missing focus-visible ring")
    if "disabled:opacity-50" not in tsx and "disabled:opacity-40" not in tsx:
        fails.append(f"{slug}: missing disabled treatment")
    if "transition-colors" in tsx and "motion-reduce:transition-none" not in tsx:
        fails.append(f"{slug}: transition without motion-reduce guard")
    for pat in FORBIDDEN:
        if re.search(pat, tsx, re.I):
            fails.append(f"{slug}: forbidden pattern {pat!r}")
    hexes = [h for h in re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx) if h != "#000"]
    if hexes:
        fails.append(f"{slug}: raw hex color found (tokens only) {hexes}")
    if re.search(r":\s*any\b|as\s+any\b|<any>|Array<any>", tsx):
        fails.append(f"{slug}: `any` usage found")
    if "<div onClick" in tsx:
        fails.append(f"{slug}: clickable div found")

    # -- shared core -------------------------------------------------------
    stripped = header_neutralized(tsx)
    cores.setdefault(stripped, []).append(slug)

if len(cores) != 1:
    fails.append(
        "shared compound core diverged across variants: " +
        ", ".join(f"{i}: {v}" for i, v in enumerate(cores.values())))

if fails:
    print("AUDIT FAILURES:")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print(f"OK: {len(dirs)} date-picker variants share one compound core; all checks pass.")
