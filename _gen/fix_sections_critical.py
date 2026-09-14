"""Targeted fixes for Tailwind Sections critical defects (read-then-edit on generated files).

Applies to BOTH code.html and preview.html (they share the section markup):
  1. Testimonials: replace literal `>heart<` inside badge <svg> with a real heart path.
  2. Testimonials: fill the unfilled `%s` template placeholders in
     bento-grid (ratings), dark-premium (split), vercel (carousel).

Does NOT regenerate files. Only patches the specific broken substrings, so all
other content is preserved exactly. Idempotent: re-running is a no-op once fixed.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "Tailwind" / "Sections" / "Testimonials"

HEART_OLD = 'aria-hidden="true">heart</svg>'
# Also catch the previously-patched path so re-running syncs to the canonical ICONS["heart"].
HEART_PREV = 'aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z"/></svg>'
HEART_NEW = (
    'aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/></svg>'
)


def patch_heart(text):
    if HEART_OLD in text:
        text = text.replace(HEART_OLD, HEART_NEW)
    elif HEART_PREV in text:
        text = text.replace(HEART_PREV, HEART_NEW)
    return text


def patch_bento_grid(text):
    """ratings key: 4 unfilled %s in the featured rating panel."""
    s = "bento-grid"
    from _gen.helpers import TOKENS, star_row
    b = TOKENS[s]
    old = (
        '<div class="%s p-8"><div class="flex items-end gap-3">'
        '<span class="f-disp text-5xl font-bold">4.9</span>'
        '<span class="text-sm %s pb-1">/ 5.0</span></div>'
        '<div class="mt-3">%s</div>'
        '<p class="mt-3 text-sm %s">Based on 2,847 verified reviews</p>'
    )
    new = (
        f'<div class="{b["surface"]} p-8"><div class="flex items-end gap-3">'
        '<span class="f-disp text-5xl font-bold">4.9</span>'
        f'<span class="text-sm {b["text_muted"]} pb-1">/ 5.0</span></div>'
        f'<div class="mt-3">{star_row(5, s)}</div>'
        f'<p class="mt-3 text-sm {b["text_muted"]}">Based on 2,847 verified reviews</p>'
    )
    return text.replace(old, new) if old in text else text


def patch_dark_premium(text):
    """split key: 8 unfilled %s in the featured spotlight panel."""
    s = "dark-premium"
    from _gen.helpers import TOKENS, star_row, avatar
    b = TOKENS[s]
    persons = [
        ("Maya Chen", "Head of Design", "Northbeam"),
        ("Daniel Reyes", "CTO", "Loop Labs"),
        ("Aisha Karim", "Product Lead", "Pulumi"),
        ("Tom Bradley", "Founder", "Myria Co."),
        ("Sofia Rossi", "Eng Lead", "Vela"),
        ("Jordan Fields", "Dev Advocate", "Cal.com"),
        ("Priya Nair", "VP Product", "Resend"),
        ("Ethan Park", "COO", "Flowbase"),
    ]
    quotes = [
        "The fastest onboarding we have ever shipped. Live in two days.",
        "Replaced four separate tools. Our team finally has breathing room.",
        "Reliable, fast, and beautifully designed. An absolute no-brainer.",
        "Our median reply time dropped 70% in the first week alone.",
        "The automation suite paid for itself within a single month.",
        "It genuinely feels built by people who care about the craft.",
        "Onboarding 200 contractors took an afternoon, not a quarter.",
        "Support that treats our customers like we do. Rare and welcome.",
        "Dashboards our execs actually open. The data just makes sense.",
        "We cut churn 18% by acting on insights we finally could see.",
    ]
    P = lambda n: persons[n % len(persons)]
    Q = lambda n: quotes[n % len(quotes)]
    pr = P(3)
    old = (
        '<div class="%s p-8 sm:p-12"><div class="mb-5">%s</div>'
        '<blockquote class="f-disp text-2xl sm:text-3xl font-medium leading-snug">"%s"</blockquote>'
        '<div class="mt-8 flex items-center gap-4">%s<div>'
        '<p class="font-semibold">%s</p><p class="text-sm %s">%s, %s</p></div></div></div>'
    )
    new = (
        f'<div class="{b["surface"]} p-8 sm:p-12"><div class="mb-5">{star_row(5, s)}</div>'
        f'<blockquote class="f-disp text-2xl sm:text-3xl font-medium leading-snug">"{Q(3)}"</blockquote>'
        f'<div class="mt-8 flex items-center gap-4">{avatar(pr[0], 3)}<div>'
        f'<p class="font-semibold">{pr[0]}</p><p class="text-sm {b["text_muted"]}">{pr[1]}, {pr[2]}</p></div></div></div>'
    )
    return text.replace(old, new) if old in text else text


def patch_vercel(text):
    """carousel key: 2 unfilled %s in the outer carousel panel."""
    s = "vercel"
    from _gen.helpers import TOKENS
    b = TOKENS[s]
    old = '<div class="%s %s overflow-hidden p-8 sm:p-12">'
    new = f'<div class="{b["surface"]} {b["hover_card"]} overflow-hidden p-8 sm:p-12">'
    return text.replace(old, new) if old in text else text


def fix_dir(style, patchers):
    d = T / style
    changed = []
    for fname in ("code.html", "preview.html"):
        p = d / fname
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for patch in patchers:
            text = patch(text)
        text = patch_heart(text)
        if text != orig:
            p.write_text(text, encoding="utf-8")
            changed.append(fname)
    return changed


def main():
    sys.path.insert(0, str(ROOT))
    fixes = [
        ("bento-grid", [patch_bento_grid]),
        ("dark-premium", [patch_dark_premium]),
        ("vercel", [patch_vercel]),
    ]
    # heart applies to all 15
    all_styles = sorted(p.name for p in T.iterdir() if p.is_dir())
    total = 0
    for style in all_styles:
        ch = fix_dir(style, [])
        if ch:
            total += len(ch)
            print(f"[heart] {style}: {', '.join(ch)}")
    for style, patchers in fixes:
        ch = fix_dir(style, patchers)
        if ch:
            total += len(ch)
            print(f"[%s] {style}: {', '.join(ch)}")
    print(f"\nDone. {total} file writes across {len(all_styles)} styles.")
    # verify no %s or heart remains
    leaks = []
    for style in all_styles:
        for fname in ("code.html", "preview.html"):
            p = T / style / fname
            txt = p.read_text(encoding="utf-8")
            if ">heart<" in txt:
                leaks.append(f"{style}/{fname}: heart")
            if "%s" in txt:
                leaks.append(f"{style}/{fname}: %s")
    if leaks:
        print("REMAINING LEAKS:")
        for l in leaks:
            print("  -", l)
        sys.exit(1)
    else:
        print("Verification: no `>heart<` or `%s` remains in any Testimonials file.")


if __name__ == "__main__":
    main()
