#!/usr/bin/env python3
"""Consistency + anti-AI audit for the React Tables family.

Checks every variant's code.tsx:
  - one shared compound core: the non-header parts of every code.tsx are
    byte-identical across all 12 variants (only the header doc comment —
    registered per variant as ``tsx_header`` — may differ)
  - exports: the 15 compound primitives + 4 typed helpers everywhere,
    TSX/JSX named-export parity, default export = Table
  - semantics: real table elements + scope attributes + aria-sort /
    aria-selected / aria-expanded / aria-controls / aria-busy /
    indeterminate wiring present; no ARIA grid re-declaration
  - focus-visible ring token; disabled treatment; motion-reduce guards
  - no `any`, no raw hex, no inline styles, no forbidden AI-slop patterns
"""
import re
import sys
from pathlib import Path

TABLES = Path("React/Components/Tables")

CORE_EXPORTS = sorted([
    "Table", "TableCaption", "TableHeader", "TableBody", "TableFooter",
    "TableRow", "TableHead", "TableCell", "TableEmpty", "TableLoading",
    "TableActions", "TableToolbar", "TablePagination", "TableSelection",
    "TableExpand", "sortRows", "useRowSelection", "clampPage", "pageRange",
])

FORBIDDEN = [
    r"purple", r"neon", r"glassmorphism", r"backdrop-filter", r"\bglow\b",
    r"gradient-(to|from|via)", r"bg-gradient", r"\blorem\b", r"emoji",
]

fails = []

dirs = sorted(d for d in TABLES.iterdir() if d.is_dir())
if not dirs:
    print("no tables found")
    sys.exit(1)

cores = {}

for d in dirs:
    slug = d.name
    tsx = (d / "code.tsx").read_text()
    jsx = (d / "code.jsx").read_text()

    # -- exports ---------------------------------------------------------
    tsx_names = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
    jsx_names = re.findall(r"export \{ ([^}]*) \};", jsx)
    jsx_named = sorted(x.strip() for x in jsx_names[0].split(",")) if jsx_names else []

    if tsx_names != CORE_EXPORTS:
        fails.append(f"{slug}: exports wrong: {tsx_names}")
    if tsx_names != jsx_named:
        fails.append(f"{slug}: TSX/JSX named-export parity drift: tsx={tsx_names} jsx={jsx_named}")
    if "export default Table;" not in jsx:
        fails.append(f"{slug}: code.jsx missing default export")

    # -- semantics -------------------------------------------------------
    for needle in ("<table", "<caption", "<thead", "<tbody", "<tfoot",
                   "<th", "<td", "<tr", 'scope ?? "col"', "aria-sort",
                   "aria-selected", "aria-expanded", "aria-controls",
                   "aria-busy", "aria-current", "indeterminate",
                   "aria-live"):
        if needle not in tsx:
            fails.append(f"{slug}: missing {needle}")
    for bad in ('role="grid"', 'role="table"', 'role="row"', 'role="cell"'):
        if bad in tsx:
            fails.append(f"{slug}: ARIA re-declaration of native table semantics: {bad}")

    # -- shared quality bar ---------------------------------------------
    if "focus-visible:outline-2" not in tsx:
        fails.append(f"{slug}: missing focus-visible ring")
    if "disabled:pointer-events-none" not in tsx or "disabled:opacity-50" not in tsx:
        fails.append(f"{slug}: missing disabled treatment")
    if "transition-colors" in tsx and "motion-reduce:transition-none" not in tsx:
        fails.append(f"{slug}: transition without motion-reduce guard")
    if "animate-pulse" in tsx and "motion-reduce:animate-none" not in tsx:
        fails.append(f"{slug}: skeleton pulse without reduced-motion guard")
    for pat in FORBIDDEN:
        if re.search(pat, tsx, re.I):
            fails.append(f"{slug}: forbidden pattern {pat!r}")
    if re.search(r"#[0-9a-fA-F]{3,8}\b", tsx):
        fails.append(f"{slug}: raw hex color found (tokens only)")
    if re.search(r":\s*any\b|as\s+any\b|<any>|Array<any>", tsx):
        fails.append(f"{slug}: `any` usage found")
    if "style=" in tsx or "style={" in tsx:
        fails.append(f"{slug}: inline style found (classes only)")

    # -- shared core (only the header doc comment may differ) ------------
    stripped = re.sub(r"/\*\*.*?\*/", "", tsx, count=1, flags=re.S).rstrip()
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
print(f"OK: {len(dirs)} table variants share one compound core; all checks pass.")
