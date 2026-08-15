"""Make each Tailwind Section code.html self-contained.

Problem: code.html (the copy-paste snippet) references style-helper CSS classes
(f-disp, f-mono, f-sans, neu, eg-glass, ft-glow, vc-panel, nb-shadow, cy-clip, ...)
that are only defined in preview.html's <style> block. A user who copies code.html
without also copying those definitions gets unstyled helper classes.

Fix: extract the style-helper CSS (the contents of preview.html's first <style>
block) and inject it into code.html as a <style> block immediately after the
snippet comment header. If code.html already has an inline <style> (e.g. the
404 terminal blink keyframes), merge into it.

Idempotent: skips files that already contain the helper CSS (detected via the
marker comment). Does not touch preview.html.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEC = ROOT / "Tailwind" / "Sections"

MARKER = "/* DevSnips style-helper classes (self-contained snippet) */"

# 10-style categories only (the multi-concept saas/developer/etc. sections are
# already self-contained — their helper classes are defined inline or via the
# sg-mesh/nb/vc token system embedded in preview body, and their code.html
# uses only Tailwind utilities + the scope attrs).
SKIP_CATS = {"ai-product", "app-ui", "developer", "marketing", "premium-visual", "saas"}


def extract_preview_style(prev_text):
    """Return the CSS text from preview.html's first <style> block, or ''."""
    m = re.search(r"<style>(.*?)</style>", prev_text, re.S)
    if not m:
        return ""
    css = m.group(1).strip()
    # Drop @import / @font-face lines (fonts are loaded via <link> in preview;
    # a self-contained snippet should rely on the page's own fonts or the
    # f-sans/f-mono/f-disp fallbacks which we keep).
    css = "\n".join(
        line for line in css.splitlines()
        if not line.strip().startswith("@import") and not line.strip().startswith("@font-face")
    )
    return css.strip()


def inject(code_text, css):
    """Inject the helper CSS into code.html after the comment header."""
    if not css:
        return code_text, False
    if MARKER in code_text:
        return code_text, False  # already done

    style_block = f"<style>\n  {MARKER}\n  {css}\n</style>"

    # If code.html already has an inline <style> (e.g. 404 terminal keyframes),
    # prepend our helpers into it rather than adding a second block.
    existing = re.search(r"<style>(.*?)</style>", code_text, re.S)
    if existing:
        inner = existing.group(1).strip()
        merged = f"<style>\n  {MARKER}\n  {css}\n  {inner}\n</style>"
        return code_text.replace(existing.group(0), merged, 1), True

    # Otherwise, inject after the snippet comment header (<!-- ... -->).
    # The header is the first HTML comment at the top of the file.
    hdr = re.match(r"^(\s*<!--.*?-->)\s*", code_text, re.S)
    if hdr:
        insert_at = hdr.end()
        return code_text[:insert_at] + "\n" + style_block + "\n" + code_text[insert_at:], True
    # No header: prepend.
    return style_block + "\n" + code_text, True


def main():
    fixed = 0
    skipped = 0
    for cat_dir in sorted(SEC.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name in SKIP_CATS:
            continue
        for style_dir in sorted(cat_dir.iterdir()):
            if not style_dir.is_dir():
                continue
            code_p = style_dir / "code.html"
            prev_p = style_dir / "preview.html"
            if not code_p.exists() or not prev_p.exists():
                continue
            code_text = code_p.read_text(encoding="utf-8")
            if MARKER in code_text:
                skipped += 1
                continue
            css = extract_preview_style(prev_p.read_text(encoding="utf-8"))
            if not css:
                skipped += 1
                continue
            new_text, changed = inject(code_text, css)
            if changed:
                code_p.write_text(new_text, encoding="utf-8")
                fixed += 1
    print(f"Injected self-contained style-helper CSS into {fixed} code.html files.")
    print(f"Skipped {skipped} (already done or no preview <style>).")

    # Verification: sample a few and confirm the helper classes are now defined in code.html
    print("\n--- verification (sample) ---")
    samples = [
        "Testimonials/vercel", "Stats/futuristic", "Logos/neo-brutalism",
        "Team/soft-ui", "Footer/cyber", "404/edge-glassmorphism",
    ]
    for s in samples:
        p = SEC / s / "code.html"
        t = p.read_text(encoding="utf-8")
        has = MARKER in t
        # check a representative helper is defined
        representative = {
            "Testimonials/vercel": ".vc-panel",
            "Stats/futuristic": ".ft-glow",
            "Logos/neo-brutalism": ".nb-shadow",
            "Team/soft-ui": ".neu",
            "Footer/cyber": ".cy-clip",
            "404/edge-glassmorphism": "@keyframes blink",
        }[s]
        defined = representative in t
        print(f"  {s}: marker={has} | defines {representative!r}: {defined}")


if __name__ == "__main__":
    main()
