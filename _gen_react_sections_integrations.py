#!/usr/bin/env python3
"""Generate preview.html for the React Sections Integrations family.

Reads the authored `React/Sections/Integrations/<slug>/code.tsx` (the
single source of truth - do NOT edit it here) and renders a self-contained
runnable `preview.html` per variant, following the exact preview
architecture of the React Components (`_gen_react_buttons.py`) and the
Hero/Features/Testimonials/Logo-Cloud sections generators:

  - Tailwind CDN + React 18 UMD + Babel standalone
  - the canonical `--ds-*` token block( light + dark) imported from
    `_gen_react_buttons.TOKEN_BLOCK`
  -the actual component transformed from code.tsx via esbuild
    (`_tsx_to_babel_component`), exposed on `window.tegrationsSection`
  - a persisted, no-flash light/dark page toggle

Sections render full-bleed between the topbar and footer (a section is a
full-width page region, not a showcase column). The Dark Premium variant
(`dark-premium`) pins `data-theme="dark"` on its own root, so the page
toggle demonstrates it holding its theme mapping in both page themes.

The family ships exactly the four DevSnips visual directions:
 `minimal`,
`dark-premium`, `bento`, `neo-brutalist`.

esbuild (build-time-only tool, NOT committed) must be installed at
/tmp/dsbuild - same requirement as the other `_gen_react_*` generators.



Usage:
    python3 _gen_react_sections_integrations.py          # write all 4 previews
    python3 _gen_react_sections_integrations.py --check  # detect drift, exit 1
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
INTEGRATIONS_DIR = ROOT / "React" / "Sections" / "Integrations"

# slug ->( display title, preview lede). Keyed by folder name so the
# generator refuses to proceed if a folder disappears. Each lede describes
# the actual composition of its variant (used asthe preview's introduction).
VARIANTS = {
    "minimal": (
        "Integrations - Minimal",
        "The reference direction: a restrained, documentation-style integration "
        "directory. A tight header block names the ecosystem, then a ruled "
        "list of integrations sits below - hairline rules, whitespace,and "
        "typography carry the hierarchy, never cards. Each row carries a "
        "compact invented identity mark, a mono category label,andonelining "
        "description. One accent for the directory link only.",
    ),
    "dark-premium": (
        "Integrations - Dark Premium",
        "A connected-ecosystem composition on a pinned dark canvas: a "
        "central product node names the product, and six integration nodes "
        "orbit it in two ruled rings. Hairline SVG connection lines fan out "
        "from the center toward the section edges - purely decorative and "
        "aria-hidden-and never overlap the named nodes. One raised panel,"
        "one elevation step, anda single accent action.",
    ),
    "bento": (
        "Integrations - Bento",
        "An ecosystem composition in a modular 12-column cell grid: onelarge "
        "featured integration cell with a product-ecosystem anchor, a five-"
        "tool showcase cell, three category cells (Development, Design,"
        "Communication,) and a full-width connection strip tying the count "
        "to the integration directory. Nice radius, uniform gap, and "
        "border-only hover lift. Intentionally not a logo-card gallery.",
    ),
    "neo-brutalist": (
        "Integrations - Neo-Brutalist",
        "The expressive ceiling, kept disciplined: an oversized bold heading, "
        "a large flat-accent central system block, anda rigid rack of module "
        "blocks with 2px borders, hard offset shadows, mono index "
        "numbers, uppercase mono names, LINKED connection tags,and a "
        "press-down Connect-your-stack action.",
    ),
}

# Sections-preview shell additions on top of the shared PREVIEW_CSS:
#he section renders full-bleed, so its mount point escapes the .ds-main's
# 980px column. This is the shared sections shell (identical to the
# Hero/Features/Testimonials/Logo-Cloud generators).
SECTIONS_PREVIEW_CSS = """
  .ds-intro{max-width:980px;margin:0 auto;padding:32px 24px 40px;}
  .ds-stage{width:100%;}
"""


def render_preview(slug: str, tsx: str) -> str:
    title, lede = VARIANTS[slug]
    component_js = _tsx_to_babel_component(tsx, expose_name="IntegrationsSection")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)} - DevSnips React Sections</title>
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sections / Integrations / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <div class="ds-intro">
    <p class="ds-eyebrow">React Sections - Integrations</p>
    <h1 class="ds-title">{html.escape(title)}</h1>
    <p class="ds-lede">{html.escape(lede)}</p>
  </div>
  <main class="ds-stage">
    <div id="ds-root"></div>
  </main>
  <footer class="ds-footer">DevSnips React - Sections - Integrations - <code>{slug}</code> - live render of code.tsx</footer>
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
// Mount the section full-bleed, as it would sit on a real page.
ReactDOM.createRoot(document.getElementById("ds-root")).render(<IntegrationsSection />);
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
        folder = INTEGRATIONS_DIR / slug
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
        print("Run: python3 _gen_react_sections_integrations.py")
        return 1
    if args.check:
        print("All Integrations previews are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())