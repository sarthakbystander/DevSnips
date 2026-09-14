"""Deterministic quality-bar auto-fixer for Vanilla components.

Applies the two universally-safe fixes that account for the majority of QA
failures, without changing component behavior:

  1. reduced-motion guard  — if the component animates (transition/animation/
     @keyframes) but has no `prefers-reduced-motion` rule, inject a global
     `@media (prefers-reduced-motion: reduce) { * { animation-duration:0s
     !important; transition-duration:0s !important; animation-iteration-count:
     1 !important; scroll-behavior:auto !important; } }` block. This is the
     recommended reduced-motion baseline.
  2. focus-visible ring — if the component has no `:focus-visible` styles,
     inject a `:focus-visible { outline: 2px solid #2563eb; outline-offset:
     2px; }` rule so keyboard users always see a focus indicator.

Both are injected into the component's existing `<style>` block (before
</style>), or as a new trailing <style> block for fragment-style components.
Full <!DOCTYPE> pages inject before </head> when no <style> exists.

Does NOT touch aria/role or keyboard operability — those require per-component
judgment and are handled manually for interactive families.

Idempotent: re-running is a no-op on already-fixed files.

Run:  DRY_RUN=1 python3 -m _gen.fix_quality_bar   (preview)
      python3 -m _gen.fix_quality_bar              (apply)
Then: python3 scripts/qa_vanilla.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMP = ROOT / "Vanilla" / "Components"

REDUCED_GUARD = (
    "@media (prefers-reduced-motion: reduce){*{"
    "animation-duration:0.01ms !important;"
    "animation-iteration-count:1 !important;"
    "transition-duration:0.01ms !important;"
    "scroll-behavior:auto !important;}}"
)
FOCUS_VISIBLE = (
    ":focus-visible{outline:2px solid #2563eb;outline-offset:2px;}"
)
MARKER = "/* devsnips-qa:quality-bar */"


def has_reduced(low):
    return "prefers-reduced-motion" in low


def has_focus_visible(low):
    return "focus-visible" in low


def has_animation(low):
    return bool(re.search(r"transition\s*:|animation\s*:|@keyframes", low))


def inject(html: Path):
    txt = html.read_text(encoding="utf-8")
    low = txt.lower()
    need_reduced = has_animation(low) and not has_reduced(low)
    need_focus = not has_focus_visible(low)
    if not (need_reduced or need_focus):
        return False, "ok"
    parts = []
    if need_reduced:
        parts.append(REDUCED_GUARD)
    if need_focus:
        parts.append(FOCUS_VISIBLE)
    block = "\n" + MARKER + "\n" + "\n".join(parts) + "\n"

    # 1. existing <style> ... </style> -> insert before the last </style>
    m = list(re.finditer(r"</style\s*>", low))
    if m:
        pos = m[-1].start()
        # translate to original text position
        new = txt[:pos] + block + txt[pos:]
        html.write_text(new, encoding="utf-8")
        return True, ("reduced+focus" if (need_reduced and need_focus)
                      else "reduced" if need_reduced else "focus")
    # 2. full doctype page with </head>
    m = re.search(r"</head\s*>", low)
    if m:
        pos = m.start()
        inject_block = "<style>" + block + "</style>\n"
        new = txt[:pos] + inject_block + txt[pos:]
        html.write_text(new, encoding="utf-8")
        return True, "head-style"
    # 3. fragment with no <style> -> append a <style> block at end
    html.write_text(txt.rstrip() + "\n<style>" + block + "</style>\n",
                    encoding="utf-8")
    return True, "appended-style"


def main():
    dry = os.environ.get("DRY_RUN") == "1"
    print("DevSnips quality-bar auto-fixer"
          + ("  [DRY RUN]" if dry else "  [LIVE]"))
    fixed = 0
    for mf in sorted(COMP.rglob("metadata.json")):
        leaf = mf.parent
        html = None
        for f in leaf.iterdir():
            if f.is_file() and f.suffix == ".html":
                html = f
                break
        if not html:
            continue
        low = html.read_text(encoding="utf-8").lower()
        need_reduced = has_animation(low) and not has_reduced(low)
        need_focus = not has_focus_visible(low)
        if not (need_reduced or need_focus):
            continue
        tags = []
        if need_reduced:
            tags.append("reduced-motion")
        if need_focus:
            tags.append("focus-visible")
        print("  %-68s %s" % (html.relative_to(ROOT), "+".join(tags)))
        if not dry:
            ok, _ = inject(html)
            if ok:
                fixed += 1
    print("\n%s files %s." % (fixed, "would fix" if dry else "fixed"))


if __name__ == "__main__":
    main()
