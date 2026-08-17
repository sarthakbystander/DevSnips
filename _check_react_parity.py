#!/usr/bin/env python3
"""Check TSX/JSX API parity for every React button.

Extracts the destructured prop names from the primary component function
signature in both code.tsx and code.jsx and reports any divergence.
"""
import re
from pathlib import Path

BUTTONS = Path("React/Components/Buttons")


def primary_signature(src):
    """Return (component_name, [prop_names]) for the primary exported
    component function, handling destructured multi-line param lists.
    Prefers `export function Name(` over a plain `function` (so the local
    `cx`/helper functions are skipped)."""
    # prefer exported function declarations first
    m = re.search(r"export\s+function\s+([A-Za-z_$][\w$]*)\s*\(", src)
    if not m:
        m = re.search(r"function\s+([A-Za-z_$][\w$]*)\s*\(", src)
    if not m:
        return None, []
    name = m.group(1)
    # capture the balanced { ... } that is the param list right after the (
    start = src.index("(", m.end() - 1)
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
    block = src[start : end + 1 if end else len(src)]
    # strip default values: `size = "md"` -> `size`; strip types after `:`; strip spreads
    props = []
    for raw in block.split(","):
        seg = raw.strip().strip("{}")
        if not seg or seg.startswith("..."):
            continue
        seg = re.sub(r"\s*=.*$", "", seg)      # remove defaults
        seg = re.sub(r"\?:.*$", "", seg)        # remove optional type
        seg = re.sub(r":.*$", "", seg)          # remove type annotation
        seg = seg.strip()
        if seg:
            props.append(seg)
    return name, sorted(set(props))


def main():
    drift = []
    for d in sorted(BUTTONS.iterdir()):
        if not d.is_dir():
            continue
        tsx = (d / "code.tsx").read_text()
        jsx = (d / "code.jsx").read_text()
        tn, tp = primary_signature(tsx)
        jn, jp = primary_signature(jsx)
        if tn != jn:
            drift.append(f"{d.name}: name tsx={tn} jsx={jn}")
            continue
        if tp != jp:
            only_tsx = [p for p in tp if p not in jp]
            only_jsx = [p for p in jp if p not in tp]
            drift.append(f"{d.name}: props differ — tsx-only={only_tsx} jsx-only={only_jsx}")
    if drift:
        print("PARITY DRIFT:")
        for d in drift:
            print("  - " + d)
        raise SystemExit(1)
    print(f"OK: 30 buttons, TSX/JSX prop signatures match.")


if __name__ == "__main__":
    main()
