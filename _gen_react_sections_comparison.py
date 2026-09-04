#!/usr/bin/env python3
"""Generate preview.html for the React Sections Comparison family.

Reads the authored `React/Sections/Comparison/<slug>/code.tsx` as the single
source of truth and renders a readable, self-contained `preview.html` per
variant using the same preview architecture as the existing React Sections.

Architecture:
  - Tailwind CDN + React 18 UMD + Babel standalone
  - canonical `--ds-*` token block and shared preview CSS
  - build-time esbuild transform via `_tsx_to_babel_component`
  - transformed component embedded directly in preview.html
  - persisted, no-flash light/dark page toggle
  - full-bleed section mount between the preview chrome

Usage:
    python3 _gen_react_sections_comparison.py
    python3 _gen_react_sections_comparison.py --check
"""

from __future__ import annotations

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
COMPARISON_DIR = ROOT / "React" / "Sections" / "Comparison"

VARIANTS = {
    "minimal": (
        "Comparison — Minimal",
        "A restrained editorial matrix with a clear recommended option.",
    ),
    "dark-premium": (
        "Comparison — Dark Premium",
        "A permanently dark product-decision interface with stacked comparison panels.",
    ),
    "bento": (
        "Comparison — Bento",
        "A genuine 12-column decision map built from varied comparison cells.",
    ),
    "neo-brutalist": (
        "Comparison — Neo-Brutalist",
        "A rigid comparison matrix with hard borders and offset elevation.",
    ),
}

SECTIONS_PREVIEW_CSS = """
  .ds-intro{max-width:980px;margin:0 auto;padding:32px 24px 40px;}
  .ds-stage{width:100%;}
"""


def render_preview(slug: str, tsx: str) -> str:
    title, lede = VARIANTS[slug]
    component_js = _tsx_to_babel_component(tsx, expose_name="ComparisonSection")

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
    <div class="ds-brand">
      <span class="ds-mark" aria-hidden="true">D</span>
      <span>DevSnips</span>
      <span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sections / Comparison / {slug}</span>
    </div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <div class="ds-intro">
    <p class="ds-eyebrow">React Sections · Comparison</p>
    <h1 class="ds-title">{html.escape(title)}</h1>
    <p class="ds-lede">{html.escape(lede)}</p>
  </div>
  <main class="ds-stage">
    <div id="ds-root"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Sections · Comparison · <code>{slug}</code> · live render of code.tsx</footer>
</div>
<script>
(function(){{
  var root = document.documentElement;
  function apply(t){{
    root.setAttribute("data-theme", t);
    try{{ localStorage.setItem("ds-react-theme", t); }}catch(e){{}}
    var b = document.getElementById("ds-theme-toggle");
    var l = document.getElementById("ds-theme-label");
    if(b){{ b.setAttribute("aria-pressed", t === "dark" ? "true" : "false"); }}
    if(l){{ l.textContent = t === "dark" ? "Light" : "Dark"; }}
  }}
  var saved = null;
  try{{ saved = localStorage.getItem("ds-react-theme"); }}catch(e){{}}
  if(!saved){{
    saved = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }}
  apply(saved);
  document.getElementById("ds-theme-toggle").addEventListener("click", function(){{
    var cur = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    apply(cur);
  }});
}})();
</script>
<script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
<script type="text/babel" data-presets="react">
// The section below is generated from the authored code.tsx source.
{component_js}
</script>
<script type="text/babel" data-presets="react">
// Mount the section full-bleed, as it would sit on a real page.
ReactDOM.createRoot(document.getElementById("ds-root")).render(<ComparisonSection />);
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

    drift: list[str] = []
    for slug in VARIANTS:
        folder = COMPARISON_DIR / slug
        tsx_path = folder / "code.tsx"
        preview_path = folder / "preview.html"

        if not tsx_path.exists():
            print(f"ERROR: missing {tsx_path}", file=sys.stderr)
            return 1

        expected = render_preview(slug, tsx_path.read_text())
        if args.check:
            if not preview_path.exists() or preview_path.read_text() != expected:
                drift.append(slug)
        else:
            preview_path.write_text(expected)
            print(f"wrote {preview_path.relative_to(ROOT)}")

    if drift:
        print("Drift detected in: " + ", ".join(drift))
        print("Run: python3 _gen_react_sections_comparison.py")
        return 1

    if args.check:
        print("All Comparison previews are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
