#!/usr/bin/env python3
"""Consistency + anti-AI audit for the React Tabs family.

Checks every variant's code.tsx:
  - one shared compound core: the non-treatment parts of every code.tsx are
    byte-identical across all 11 variants (treatment constants + orientation
    default + the optional TabsAddAction export may differ)
  - exports: Tabs/TabsList/TabsTrigger/TabsContent everywhere,
    TabsAddAction only on tabs-with-add-action
  - semantics: role=tablist/tab/tabpanel + aria-selected/aria-controls/
    aria-labelledby + roving tabIndex present
  - focus-visible ring token; disabled treatment; motion-reduce guards
  - TSX/JSX export parity (named exports + default match between code.tsx
    and code.jsx)
  - no `any`, no raw hex, no forbidden AI-slop patterns
"""
import re
import sys
from pathlib import Path

TABS = Path("React/Components/Tabs")

CORE_EXPORTS = ["Tabs", "TabsContent", "TabsList", "TabsTrigger"]  # sorted

FORBIDDEN = [
    r"purple", r"neon", r"glassmorphism", r"backdrop-filter", r"\bglow\b",
    r"gradient-(to|from|via)", r"bg-gradient", r"\blorem\b",
]

fails = []


def treatment_neutralized(src: str) -> str:
    """Blank the treatment-specific values so the shared core can be
    compared byte-for-byte across variants."""
    out = src
    for name in ("LIST_HORIZONTAL_CLASSES", "TRIGGER_TREATMENT_CLASSES",
                 "TRIGGER_SELECTED_CLASSES", "TRIGGER_IDLE_CLASSES"):
        out = re.sub(
            rf'const {name} =\s*\n?\s*"[^"]*";',
            f'const {name} = "<X>";', out)
    out = re.sub(r'orientation = "(horizontal|vertical)"',
                 'orientation = "<ORIENT>"', out)
    # the treatment-description line differs per variant
    out = re.sub(r"\* Treatment: [^\n]*", "* Treatment: <T>", out)
    # the add-action variant carries one extra type import
    out = out.replace('import type { ButtonHTMLAttributes } from "react";\n', "")
    # the default export sits in a different position on the add-action variant
    out = out.replace("export default Tabs;\n", "")
    return out.rstrip()


dirs = sorted(d for d in TABS.iterdir() if d.is_dir())
if not dirs:
    print("no tabs found")
    sys.exit(1)

cores = {}

for d in dirs:
    slug = d.name
    tsx = (d / "code.tsx").read_text()
    jsx = (d / "code.jsx").read_text()

    # -- exports ---------------------------------------------------------
    tsx_names = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
    jsx_names = sorted(re.findall(r"export \{ ([^}]*) \};", jsx))
    jsx_named = sorted(x.strip() for x in (jsx_names[0] or "").split(",")) if jsx_names else []

    if tsx_names[: len(CORE_EXPORTS)] != CORE_EXPORTS and set(CORE_EXPORTS) - set(tsx_names):
        fails.append(f"{slug}: core exports wrong: {tsx_names}")
    if ("tabs-with-add-action" == slug) != ("TabsAddAction" in tsx_names):
        fails.append(f"{slug}: TabsAddAction export mismatch")
    if tsx_names != jsx_named:
        fails.append(f"{slug}: TSX/JSX named-export parity drift: tsx={tsx_names} jsx={jsx_named}")
    if "export default Tabs;" not in jsx:
        fails.append(f"{slug}: code.jsx missing default export")

    # -- semantics -------------------------------------------------------
    for needle in ('role="tablist"', 'role="tab"', 'role="tabpanel"',
                   "aria-selected", "aria-controls", "aria-labelledby",
                   "tabIndex", "onKeyDown", "ArrowLeft", "Home", "End"):
        if needle not in tsx:
            fails.append(f"{slug}: missing {needle}")
    if '-tab-${value}' not in tsx or '-panel-${value}' not in tsx:
        fails.append(f"{slug}: id/panel association naming missing")
    if "tab.disabled" not in tsx:
        fails.append(f"{slug}: keyboard nav does not skip disabled tabs")

    # -- shared quality bar ---------------------------------------------
    if "focus-visible:outline-2" not in tsx:
        fails.append(f"{slug}: missing focus-visible ring")
    if "disabled:opacity-50" not in tsx or "disabled:pointer-events-none" not in tsx:
        fails.append(f"{slug}: missing disabled treatment")
    if "transition-colors" in tsx and "motion-reduce:transition-none" not in tsx:
        fails.append(f"{slug}: transition without motion-reduce guard")
    for pat in FORBIDDEN:
        if re.search(pat, tsx, re.I):
            fails.append(f"{slug}: forbidden pattern {pat!r}")
    if re.search(r"#[0-9a-fA-F]{3,8}\b", tsx):
        fails.append(f"{slug}: raw hex color found (tokens only)")
    if re.search(r":\s*any\b|as\s+any\b|<any>|Array<any>", tsx):
        fails.append(f"{slug}: `any` usage found")

    # -- shared core -----------------------------------------------------
    stripped = treatment_neutralized(tsx)
    # the add-action variant only appends its extra export
    stripped = stripped.split("export interface TabsAddActionProps")[0].rstrip()
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
print(f"OK: {len(dirs)} tabs variants share one compound core; all checks pass.")
