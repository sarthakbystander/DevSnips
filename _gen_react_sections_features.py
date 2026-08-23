#!/usr/bin/env python3
"""Generate preview.html for the React Sections Features family.

Reads the authored `React/Sections/Features/<slug>/code.tsx` (the single
source of truth — do NOT edit it here) and renders a self-contained
runnable `preview.html` per variant, following the exact preview
architecture of the React Components (`_gen_react_buttons.py`) and the
Hero sections generator (`_gen_react_sections_hero.py`):

  - Tailwind CDN + React 18 UMD + Babel standalone
  - the canonical `--ds-*` token block (light + dark) imported from
    `_gen_react_buttons.TOKEN_BLOCK`
  - the actual component transformed from code.tsx via esbuild
    (`_tsx_to_babel_component`), exposed on `window.FeaturesSection`
  - a persisted, no-flash light/dark page toggle

Sections render full-bleed between the topbar and footer (a section is a
full-width page region, not a showcase column). The Dark Premium variant
(`split`) pins `data-theme="dark"` on its own root, so the page toggle
demonstrates it holding its theme mapping in both page themes.

esbuild (build-time-only tool, NOT committed) must be installed at
/tmp/dsbuild — same requirement as the other `_gen_react_*` generators.

Usage:
    python3 _gen_react_sections_features.py          # write all 8 previews
    python3 _gen_react_sections_features.py --check  # detect drift, exit 1
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
FEATURES_DIR = ROOT / "React" / "Sections" / "Features"

# slug -> (display title, preview lede). Keyed by folder name so the
# generator refuses to proceed if a folder disappears.
VARIANTS = {
    "grid": (
        "Features — Grid",
        "The reference composition (Minimal): a left-aligned header block "
        "above an even six-item grid — icon, title, one sentence — "
        "separated by whitespace alone, never cards.",
    ),
    "bento": (
        "Features — Bento",
        "A modular 12-column cell grid: one hero cell with a routing "
        "diagram, one stat cell, and four single-idea supporting cells. "
        "Uniform gap, one radius, border-only hover lift.",
    ),
    "alternating": (
        "Features — Alternating",
        "An editorial walk through three features: 5/7 splits with copy on "
        "one side and a bordered product artifact (waterfall, chart, log "
        "tail) on the other, alternating sides per row.",
    ),
    "editorial": (
        "Features — Editorial",
        "Asymmetric 4/8 split: a quiet heading block beside a numbered "
        "feature list. Mono index numbers, semibold titles, and 1px "
        "hairline dividers carry the whole design.",
    ),
    "split": (
        "Features — Split",
        "A product-focused 6/6 split (Dark Premium): feature copy with "
        "icon-marked rows beside a queue-depth panel. The section pins the "
        "dark theme mapping on its own root — toggle the page theme to "
        "see it hold.",
    ),
    "spotlight": (
        "Features — Spotlight",
        "One large featured capability (with a real query-plan artifact) "
        "plus a quieter row of three supporting features below a single "
        "hairline. Hierarchy by weight, not decoration.",
    ),
    "tabs": (
        "Features — Tabs",
        "An interactive showcase: four lenses on one platform behind real "
        "tab semantics — roving tabindex, arrow-key navigation, automatic "
        "activation — each panel pairing copy with a real CLI artifact.",
    ),
    "neo-brutalist": (
        "Features — Neo-Brutalist",
        "The expressive ceiling, kept disciplined: four square blocks with "
        "uniform 2px borders, hard offset shadows, mono index numbers, one "
        "flat accent fill, and press-down buttons.",
    ),
}

# Sections-preview shell additions on top of the shared PREVIEW_CSS:
# the section renders full-bleed, so its mount point escapes .ds-main's
# 980px column.
SECTIONS_PREVIEW_CSS = """
  .ds-intro{max-width:980px;margin:0 auto;padding:32px 24px 40px;}
  .ds-stage{width:100%;}
"""


def render_preview(slug: str, tsx: str) -> str:
    title, lede = VARIANTS[slug]
    component_js = _tsx_to_babel_component(tsx, expose_name="FeaturesSection")
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sections / Features / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <div class="ds-intro">
    <p class="ds-eyebrow">React Sections · Features</p>
    <h1 class="ds-title">{html.escape(title)}</h1>
    <p class="ds-lede">{html.escape(lede)}</p>
  </div>
  <main class="ds-stage">
    <div id="ds-root"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Sections · Features · <code>{slug}</code> · live render of code.tsx</footer>
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
ReactDOM.createRoot(document.getElementById("ds-root")).render(<FeaturesSection />);
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
        folder = FEATURES_DIR / slug
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
        print("Run: python3 _gen_react_sections_features.py")
        return 1
    if args.check:
        print("All Features previews are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
