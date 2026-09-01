#!/usr/bin/env python3
"""Generate Team section previews from the authored code.tsx sources.

Each `React/Sections/Team/<variant>/code.tsx` is the sole authored source of
truth. This generator derives the self-contained showcase preview from it,
using the same Tailwind + React 18 UMD + Babel preview shell and canonical
--ds-* token block as the existing React section generators.

Usage:
    python3 _gen_react_sections_team.py
    python3 _gen_react_sections_team.py --check
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from _gen_react_buttons import PREVIEW_CSS, TAILWIND_CONFIG, TOKEN_BLOCK

ROOT = Path(__file__).resolve().parent
TEAM_DIR = ROOT / "React" / "Sections" / "Team"
VARIANTS = {
    "minimal": ("Team — Minimal", "Editorial profile list with restrained dividers and typography-led hierarchy."),
    "dark-premium": ("Team — Dark Premium", "Asymmetric dark composition with one featured profile and supporting identities."),
    "bento": ("Team — Bento", "12-column modular composition with unequal profile cells and a team-philosophy row."),
    "neo-brutalist": ("Team — Neo-Brutalist", "Rigid structured panels with 2px borders, hard offsets, and press-down interaction."),
}


def transform_tsx(tsx: str) -> str:
    """Strip only module/type syntax; Babel Standalone handles TSX at preview runtime."""
    source = re.sub(r'^\s*import\s+\*\s+as\s+React\s+from\s+["\']react["\'];\s*$', "", tsx, flags=re.M)
    source = re.sub(r'\bexport\s+type\s+TeamMember\s*=.*?;\n\n', "", source, flags=re.S)
    source = re.sub(r'\bexport\s+interface\s+TeamSectionProps\s*\{.*?\}\n\n', "", source, flags=re.S)
    source = source.replace('export function TeamSection', 'function TeamSection')
    return source


def minify_css(css: str) -> str:
    css = re.sub(r'/\*.*?\*/', "", css, flags=re.S)
    css = re.sub(r'\s+', " ", css).replace("; }", ";}").replace("{ ", "{").replace(" }", "}")
    return css.strip()


def render_preview(slug: str, tsx: str) -> str:
    title, lede = VARIANTS[slug]
    js = transform_tsx(tsx)
    return f'''<!DOCTYPE html>
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
{minify_css(TOKEN_BLOCK)}
{minify_css(PREVIEW_CSS)}
.ds-intro{{max-width:980px;margin:0 auto;padding:32px 24px 40px;}}
.ds-stage{{width:100%;}}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sections / Team / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false"><span id="ds-theme-label">Dark</span></button>
  </header>
  <div class="ds-intro">
    <p class="ds-eyebrow">React Sections · Team</p>
    <h1 class="ds-title">{html.escape(title)}</h1>
    <p class="ds-lede">{html.escape(lede)}</p>
  </div>
  <main class="ds-stage"><div id="ds-root"></div></main>
  <footer class="ds-footer">DevSnips React · Sections · Team · <code>{slug}</code> · live render of code.tsx</footer>
</div>
<script>
(function(){{
  var root = document.documentElement;
  function apply(t){{
    root.setAttribute("data-theme", t);
    try{{ localStorage.setItem("ds-react-theme", t); }}catch(e){{}}
    var b=document.getElementById("ds-theme-toggle");
    var l=document.getElementById("ds-theme-label");
    if(b) b.setAttribute("aria-pressed", t==="dark"?"true":"false");
    if(l) l.textContent=t==="dark"?"Light":"Dark";
  }}
  var saved=null;
  try{{saved=localStorage.getItem("ds-react-theme");}}catch(e){{}}
  if(!saved) saved=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";
  apply(saved);
  document.getElementById("ds-theme-toggle").addEventListener("click",function(){{
    apply(root.getAttribute("data-theme")==="dark"?"light":"dark");
  }});
}})();
</script>
<script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
<script type="text/babel" data-presets="typescript,react">
{js}
window.TeamSection = TeamSection;
</script>
<script type="text/javascript">
ReactDOM.createRoot(document.getElementById("ds-root")).render(React.createElement(window.TeamSection));
</script>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="detect generated-preview drift")
    args = parser.parse_args()
    drift: list[str] = []
    for slug in VARIANTS:
        folder = TEAM_DIR / slug
        source = folder / "code.tsx"
        preview = folder / "preview.html"
        if not source.exists():
            print(f"ERROR: missing {source}", file=sys.stderr)
            return 1
        expected = render_preview(slug, source.read_text(encoding="utf-8"))
        if args.check:
            if not preview.exists() or preview.read_text(encoding="utf-8") != expected:
                drift.append(slug)
        else:
            preview.write_text(expected, encoding="utf-8")
            print(f"wrote {preview.relative_to(ROOT)}")
    if drift:
        print("Drift detected in: " + ", ".join(drift))
        print("Run: python3 _gen_react_sections_team.py")
        return 1
    print("All Team previews are up to date." if args.check else "Team previews generated.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
