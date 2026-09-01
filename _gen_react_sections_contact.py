#!/usr/bin/env python3
"""Generate preview.html for the React Sections Contact family.

Reads the authored `React/Sections/Contact/<slug>/code.tsx` (the single
source of truth — do NOT edit it here) and renders a self-contained
runnable `preview.html` per variant, following the exact preview
architecture of the React Components (`_gen_react_buttons.py`) and the
Hero/Features/Testimonials/Pricing/Stats/Logo-Cloud/Newsletter/CTA
sections generators:

  - Tailwind CDN + React 18 UMD + Babel standalone
  - the canonical `--ds-*` token block (light + dark) imported from
    `_gen_react_buttons.TOKEN_BLOCK`
  -the actual component transformed from code.tsx via esbuild
    (`_tsx_to_babel_component`), exposed on `window.ContactSection`
  - a persisted, no-flash light/dark page toggle

Sections render full-bleed between the topbar and footer (a section is a
full-width page region, not a showcase column. The Dark Premium variant
(`dark-premium`) pins `data-theme="dark"` on its own root, so the page
toggle demonstrates it holding its theme mapping in both page themes.

The family ships exactly the four DevSnips visual directions: `minimal`,
`dark-premium`, `bento`, `neo-brutalist`.

esbuild (build-time-only tool, NOT committed) must be installed at
/tmp/dsbuild — same requirement as the other `_gen_react_*` generators.


Usage:
    python3 _gen_react_sections_contact.py          # write all 4 previews
    python3 _gen_react_sections_contact.py --check  # detect drift, exit 1
"""

import argparse
import html
import sys
from pathlib import Path

from _gen_react_buttons import (
    PREVIEW_CSS,
    TAILWIND_CONFIG,
    TOKEN_BLOCK,
    _tsx_to_babel_component,
)

ROOT = Path(__file__).resolve().parent
CONTACT_DIR = ROOT / "React" / "Sections" / "Contact"

# slug -> (display title, preview lede). Keyed by folder name so the
# generator refuses to proceed if a folder disappears. One folder per
# design direction, like the other section families. The ledes describe the
# ACTUAL composition of each variant — not a generic "contact section".
VARIANTS = {
    "minimal": (
        "Contact — Minimal",
        "The reference composition: an editorial 6/6 split — the left "
        "column carries the compact eyebrow, headline, lede,the primary "
        "email address, a ruled contact-information list (email, location,"
        " hours,response time),and a small supporting note; the right "
        "column carries the accessible 4-field contact form (Name,Email,"
        " Company optional,Message,with a primary send action). Separation "
        "comes from whitespace,typography,and hairline rules — no cards. "
        "The only accent is the send button, the email link,and error states. "
        "Try submitting the empty form, then a malformed address,then a "
        "complete inquiry — validation and success are announced, never shown "
        "by color alone,and the page never reloads or sends data anywhere.",
    ),
    "dark-premium": (
        "Contact — Dark Premium",
        "An editorial contact funnel on a pinned dark canvas:the left 5/7"
        " column carries a large four-line statement headline (the framed "
        "question stays on its own line),a lede,the primary email, a ruled "
        "metadata list (response time,location),and a quiet intake "
        "statement;the right column carries one refined form panel — "
        "one elevation step above the canvas with a thin border,and product-"
        "surface metadata (panel caption,index mark)so it reads as part "
        "of a product interface, not a generic form card. Thin borders, "
        "restrained accent (the send action only), tight tracking, subtle "
        "metadata. The section pins the dark theme mapping on its own root — "
        "toggle the page theme to see it hold. Form validation:empty "
        "required fields and malformed email show per-field accessible errors,"
        "values are preserved,and a valid submit resolves an announced success.",
    ),
    "bento": (
        "Contact — Bento",
        "A genuine 12-column bento contact composition:one large 7-column"
        " hero cell (span 7) carries the headline,lede,and the primary four-"
        "field contact form; a 5-column direct-emai/office cell (span 5) "
        "sits beside it;three smaller fact cells (span 4 each) carry "
        "response time,location,and build-slot availability as labels and "
        "values;and a full-width supporting strip (span 12) carries the "
        "response promise. Varied cell weights, uniform gap, one radius, "
        "border-only hover lift, one accent (the send button). Collapse:"
        " authored spans at lg, paired columns at sm, one column below. "
        "The only interactive element is the form — the fact cells are real "
        "content, never fake buttons.",
    ),
    "neo-brutalist": (
        "Contact — Neo-Brutalist",
        "The expressive ceiling, kept disciplined: an oversized 'CONTACT' "
        "statement headline, a large bordered form block with oversized "
        "controls and hard offset shadows, anda rigid contact-information "
        "matrix beneath — one flat warning-fill response block, one status/email "
        "block(the availability reads in words,never color alone),and a "
        "2-column contact-information `<dl>`. Square geometry, uniform 2px "
        "borders, mono uppercase labels, press-down buttons and inputs,restrained "
        "flat fills — one primary CTA fill plus one supporting warning fill. "
        "Everything is real and interactive:try submitting empty fields or a "
        "malformed email,then a complete inquiry — errors and success are "
        "announced,values survive validation failures,and nothing reloads.",
    ),
}

# Sections-preview shell additions on top of the shared PREVIEW_CSS:
#the section renders full-bleed, so its mount point escapes .ds-main's
# 980px column.
SECTIONS_PREVIEW_CSS = """
  .ds-intro{max-width:980px;margin:0 auto;padding:32px 24px 40px;}
  .ds-stage{width:100%;}
"""


def render_preview(slug: str, tsx: str) -> str:
    title, lede = VARIANTS[slug]
    component_js = _tsx_to_babel_component(tsx, expose_name="ContactSection")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)} — DevSnips React Sections</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<script src="https://cdn.tailwindcss.com"></script>
<script>
{TAILWIND_CONFIG}
</script>
<style>
{TOKEN_BLOCK}
{PREVIEW_CSS}
{SECTIONS_PREVIEW_CSS}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sections / Contact / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <div class="ds-intro">
    <p class="ds-eyebrow">React Sections · Contact</p>
    <h1 class="ds-title">{html.escape(title)}</h1>
    <p class="ds-lede">{html.escape(lede)}</p>
  </div>
  <main class="ds-stage">
    <div id="ds-root"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Sections · Contact · <code>{slug}</code> · live render of code.tsx</footer>
</div>
<script>
(function(){{
  var root = document.documentElement;
  function apply(t){{ root.setAttribute("data-theme", t); try{{ localStorage.setItem("ds-react-theme", t); }}catch(e){{}} var b=document.getElementById("ds-theme-toggle"); var l=document.getElementById("ds-theme-label"); if(b){{b.setAttribute("aria-pressed", t==="dark"?"true":"false");}} if(l){{l.textContent = t==="dark"?"Light":"Dark";}} }}
  var saved = null; try{{ saved = localStorage.getItem("ds-react-theme"); }}catch(e){{}}
  if(!saved){{ saved = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark":"light"; }}
  apply(saved);
  document.getElementById("ds-theme-toggle").addEventListener("click", function(){{ var cur = root.getAttribute("data-theme") === "dark" ? "light":"dark"; apply(cur); }});
}})();
</script>
<script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
<script type="text/babel" data-presets="react">
// The section below is the actual code.tsx implementation, transformed to
// JSX (types removed, exports stripped) so Babel standalone can run it. It
// is identical in behavior and classes to code.tsx.
{component_js}
</script>
<script type="text/babel" data-presets="react">
// Mount the section full-bleed, as it would sit on a real page. The preview
// demonstrates the real form interaction: empty required fields and malformed
// email show per-field accessible errors, a valid inquiry resolves an
// announced success state,and the page never reloads or sends data anywhere..
ReactDOM.createRoot(document.getElementById("ds-root")).render(<ContactSection />);
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit 1 if any preview.html is out of date",
    )
    args = parser.parse_args()

    drift = []
    for slug in VARIANTS:
        folder = CONTACT_DIR / slug
        tsx_path = folder / "code.tsx"
        if not tsx_path.exists():
            print(f"ERROR: missing {tsx_path}", file=sys.stderr)
            return 1
        expected = render_preview(slug, tsx_path.read_text())
        preview_path = folder / "preview.html"
        if args.check:
            if not preview_path.exists() or preview_path.read_text() != expected:
                drift.append(slug)
        else:
            preview_path.write_text(expected)
            print(f"wrote {preview_path.relative_to(ROOT)}")

    if drift:
        print("Drift detected in: " + ", ".join(drift))
        print("Run: python3 _gen_react_sections_contact.py")
        return 1
    if args.check:
        print("All Contact previews are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())