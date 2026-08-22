#!/usr/bin/env python3
"""Consistency + anti-AI audit for the React Navbar family.

Checks every variant's code.tsx / code.jsx:
  - one shared compound core: the header doc comment is the ONLY difference
    between variants (header-neutralized, the 10 code.tsx files are
    byte-identical)
  - exports: all 15 primitives everywhere, TSX/JSX export parity
  - semantics: semantic <nav> + aria-label, real anchors, aria-current,
    aria-expanded/aria-controls on the toggle, aria-haspopup on dropdown
    triggers, aria-disabled spans for disabled items — and NO ARIA menu
    pattern (role="menu"/menuitem) on navigation
  - focus-visible ring token; motion-reduce guards; overlay token
  - no `any`, no raw hex, no inline style=, no forbidden AI-slop patterns
    (gradients, glassmorphism, neon/purple, decorative blob vocabulary)
"""
import re
import sys
from pathlib import Path

NAVBAR = Path("React/Components/Navbar")

CORE_EXPORTS = sorted([
    "Navbar", "NavbarBrand", "NavbarContent", "NavbarSection", "NavbarItem",
    "NavbarLink", "NavbarAction", "NavbarToggle", "NavbarMobile",
    "NavbarMobileContent", "NavbarDropdown", "NavbarDropdownTrigger",
    "NavbarDropdownContent", "NavbarDropdownItem", "NavbarDivider",
])

FORBIDDEN = [
    r"purple", r"neon", r"glassmorphism", r"backdrop-blur", r"backdrop-filter",
    r"\bglow\b", r"gradient-(to|from|via)", r"bg-gradient", r"\blorem\b",
    r"\bblob\b", r"font-awesome", r"material-icons",
]

fails = []


def header_neutralized(src: str) -> str:
    """Blank the header doc comment so the shared core can be compared
    byte-for-byte across variants."""
    out = re.sub(r"/\*\*.*?\*/", "/* <HEADER> */", src, count=1, flags=re.S)
    return out.rstrip()


dirs = sorted(d for d in NAVBAR.iterdir() if d.is_dir())
if not dirs:
    print("no navbar variants found")
    sys.exit(1)

cores = {}

for d in dirs:
    slug = d.name
    tsx_path = d / "code.tsx"
    jsx_path = d / "code.jsx"
    if not tsx_path.is_file() or not jsx_path.is_file():
        fails.append(f"{slug}: missing code.tsx/code.jsx")
        continue
    tsx = tsx_path.read_text(encoding="utf-8")
    jsx = jsx_path.read_text(encoding="utf-8")
    # comment-stripped view (header docs legitimately discuss avoided patterns)
    code = re.sub(r"/\*.*?\*/", "", tsx, flags=re.S)

    if re.search(r"\bany\b", tsx):
        fails.append(f"{slug}: `any` type")
    if re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", tsx):
        fails.append(f"{slug}: raw hex color")
    if "style=" in tsx:
        fails.append(f"{slug}: inline style attribute")
    for pat in FORBIDDEN:
        if re.search(pat, code, flags=re.IGNORECASE):
            fails.append(f"{slug}: forbidden pattern {pat!r}")
    for needle, label in [
        ("<nav", "semantic <nav>"),
        ("aria-label", "landmark label"),
        ('aria-current={active ? "page" : undefined}', "aria-current wiring"),
        ("aria-expanded", "aria-expanded"),
        ("aria-controls", "aria-controls"),
        ('aria-haspopup="true"', "aria-haspopup trigger"),
        ('aria-disabled="true"', "aria-disabled spans"),
        ("focus-visible:outline-2", "focus-visible ring"),
        ("var(--ds-color-focus-ring)", "focus-ring token"),
        ("motion-reduce:transition-none", "reduced-motion guard"),
        ("var(--ds-color-overlay)", "overlay token"),
    ]:
        if needle not in tsx:
            fails.append(f"{slug}: missing {label}")
    if 'role="menu"' in code or "menuitem" in code:
        fails.append(f"{slug}: ARIA menu pattern on navigation (must stay disclosure)")
    if "<div onClick" in code:
        fails.append(f"{slug}: clickable div")

    tsx_exports = sorted(re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx))
    if tsx_exports != CORE_EXPORTS:
        fails.append(f"{slug}: exports {tsx_exports} != {CORE_EXPORTS}")
    m = re.search(r"\nexport \{([^}]*)\};", jsx)
    jsx_exports = sorted(x.strip() for x in m.group(1).split(",")) if m else []
    if jsx_exports != tsx_exports:
        fails.append(f"{slug}: TSX/JSX export mismatch")

    cores[slug] = header_neutralized(tsx)

ref = cores.get("navbar")
if ref is None:
    print("reference variant 'navbar' missing")
    sys.exit(1)
for slug, core in cores.items():
    if core != ref:
        fails.append(f"{slug}: shared core diverges from the reference")

if fails:
    print(f"NAVBAR AUDIT: {len(fails)} problem(s)")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print(f"NAVBAR AUDIT: {len(dirs)} variants, shared core identical, all checks clean")
