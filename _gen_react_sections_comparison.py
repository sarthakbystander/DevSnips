#!/usr/bin/env python3
"""Generate standalone previews for the React Sections Comparison family.

`code.tsx` is the authored source of truth. Each generated preview embeds that
source directly and compiles it with Babel standalone in the browser. This
matches the existing React Sections preview contract while avoiding a
runtime dependency on a sibling `code.tsx` file.

    python3 _gen_react_sections_comparison.py
    python3 _gen_react_sections_comparison.py --check
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

from _gen_react_buttons import PREVIEW_CSS, TAILWIND_CONFIG, TOKEN_BLOCK

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "React" / "Sections" / "Comparison"
VARIANTS = {
    "minimal": ("Comparison — Minimal", "Editorial matrix with a recommended option."),
    "dark-premium": ("Comparison — Dark Premium", "Stacked product-decision panels on a permanently dark surface."),
    "bento": ("Comparison — Bento", "A 12-column decision map built from varied comparison cells."),
    "neo-brutalist": ("Comparison — Neo-Brutalist", "Rigid comparison matrix with hard borders and offset elevation."),
}


def render_preview(slug: str, tsx: str) -> str:
    title, lede = VARIANTS[slug]
    source_literal = json.dumps(tsx, ensure_ascii=False).replace("</", "<\\/")
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
{TOKEN_BLOCK}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sections / Comparison / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false"><span id="ds-theme-label">Dark</span></button>
  </header>
  <div class="ds-intro">
    <p class="ds-eyebrow">React Sections · Comparison</p>
    <h1 class="ds-title">{html.escape(title)}</h1>
    <p class="ds-lede">{html.escape(lede)}</p>
  </div>
  <main class="ds-stage"><div id="ds-root"></div></main>
  <footer class="ds-footer">DevSnips React · Sections · Comparison · <code>{slug}</code> · standalone preview of code.tsx</footer>
</div>
<script>
(function(){{
  var root=document.documentElement;
  function apply(t){{
    root.setAttribute("data-theme",t);
    try{{localStorage.setItem("ds-react-theme",t)}}catch(e){{}}
    var b=document.getElementById("ds-theme-toggle"),l=document.getElementById("ds-theme-label");
    if(b)b.setAttribute("aria-pressed",t==="dark"?"true":"false");
    if(l)l.textContent=t==="dark"?"Light":"Dark";
  }}
  var saved=null;try{{saved=localStorage.getItem("ds-react-theme")}}catch(e){{}}
  if(!saved)saved=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";
  apply(saved);
  document.getElementById("ds-theme-toggle").addEventListener("click",function(){{apply(root.getAttribute("data-theme")==="dark"?"light":"dark")}});
}})();
</script>
<script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
<script>
(function(){{
  var source={source_literal};
  try{{
    source=source.replace(/^\\s*import\\s+\\{{\\s*useId\\s*\\}}\\s+from\\s+["']react["'];?\\s*$/m,"const {{ useId }} = React;");
    source=source.replace(/\\bexport\\s+(?=(?:interface|type|function|const|let|var|class)\\b)/g,"");
    var transformed=Babel.transform(source,{{presets:["react"],plugins:["transform-typescript"]}}).code;
    new Function("React","window",transformed+"\\nwindow.ComparisonSection=ComparisonSection;")(React,window);
    ReactDOM.createRoot(document.getElementById("ds-root")).render(React.createElement(window.ComparisonSection));
  }}catch(error){{
    console.error(error);
    document.getElementById("ds-root").textContent="Preview compilation failed.";
  }}
}})();
</script>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="do not write; fail if the embedded source is stale")
    args = parser.parse_args()
    drift: list[str] = []
    for slug in VARIANTS:
        folder = BASE / slug
        source_path = folder / "code.tsx"
        preview_path = folder / "preview.html"
        if not source_path.exists():
            print(f"ERROR: missing {source_path}", file=sys.stderr)
            return 1
        source = source_path.read_text()
        if args.check:
            if not preview_path.exists():
                drift.append(slug)
                continue
            preview = preview_path.read_text()
            embedded = json.dumps(source, ensure_ascii=False).replace("</", "<\\/")
            if embedded not in preview or "fetch(\"./code.tsx\")" in preview:
                drift.append(slug)
        else:
            preview_path.write_text(render_preview(slug, source))
            print(f"wrote {preview_path.relative_to(ROOT)}")
    if drift:
        print("Drift detected in: " + ", ".join(drift))
        print("Run: python3 _gen_react_sections_comparison.py")
        return 1
    if args.check:
        print("All Comparison previews embed current code.tsx sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
