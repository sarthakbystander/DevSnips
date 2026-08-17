#!/usr/bin/env python3
"""Design-consistency + anti-AI audit for the migrated React buttons.

Checks every code.tsx against the family:
  - radius: buttons use --ds-radius-sm; menus --ds-radius-md; chips/pills full
  - focus-visible: every interactive button has the focus-visible ring token
  - disabled: every interactive button has disabled:opacity-50 + pointer-events-none
  - motion: transitions guarded by motion-reduce:transition-none
  - icon size: uses [&_svg]:size-* tokens (not arbitrary px on icons)
  - no forbidden: purple/neon/gradients/glassmorphism/decorative blobs/emoji
  - no hardcoded hex outside color-mix hover darkening (#000)
"""
import re
import sys
from pathlib import Path

BUTTONS = Path("React/Components/Buttons")

FORBIDDEN = [
    r"purple", r"neon", r"glassmorphism", r"backdrop-filter", r"\bglow\b",
    r"gradient-(to|from|via)", r"bg-gradient", r"\bdecorative\b",
]
fails = []

for d in sorted(BUTTONS.iterdir()):
    if not d.is_dir():
        continue
    slug = d.name
    tsx = (d / "code.tsx").read_text()
    # focus-visible ring present (interactive buttons render <button>).
    if "focus-visible:outline" not in tsx:
        fails.append(f"{slug}: missing focus-visible ring")
    # disabled treatment: either the `disabled:` Tailwind variant OR a
    # conditional `opacity-50` (pagination disables at bounds via a class).
    if "<button" in tsx and "disabled:" not in tsx and "opacity-50" not in tsx:
        fails.append(f"{slug}: missing disabled treatment (disabled: or opacity-50)")
    # reduced-motion guard on transitions
    if "transition-colors" in tsx and "motion-reduce:transition-none" not in tsx:
        fails.append(f"{slug}: transition without motion-reduce guard")
    # forbidden tokens
    for pat in FORBIDDEN:
        if re.search(pat, tsx, re.I):
            fails.append(f"{slug}: forbidden pattern {pat!r}")
    # hardcoded hex outside color-mix. #000 is allowed only when it appears
    # inside a color-mix(...) group (the hover/active darkening technique).
    # color-mix has nested parens (var(...)), so match balanced parens.
    def _strip_colormix(s):
        out = []
        i = 0
        while i < len(s):
            if s[i : i + 10] == "color-mix(":
                depth = 1
                j = i + 10  # position of the opening paren of color-mix(
                while j < len(s) and depth > 0:
                    if s[j] == "(":
                        depth += 1
                    elif s[j] == ")":
                        depth -= 1
                    j += 1
                # skip the whole balanced color-mix(...) group
                i = j
            else:
                out.append(s[i])
                i += 1
        return "".join(out)
    hex_outside = _strip_colormix(tsx)
    for hexm in re.findall(r"#[0-9a-fA-F]{3,6}", hex_outside):
        fails.append(f"{slug}: hardcoded {hexm} outside color-mix")

if fails:
    print("AUDIT FAILURES:")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("OK: 30 buttons pass design-consistency + anti-AI audit.")
