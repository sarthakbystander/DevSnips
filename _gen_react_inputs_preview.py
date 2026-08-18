#!/usr/bin/env python3
"""DevSnips React Inputs preview rebuilder.

Rebuilds a working ``preview.html`` for every input in
``React/Components/Inputs/`` from its ``code.tsx`` + the Showcase already
authored in the existing preview. Mirrors the buttons generator
(``_gen_react_buttons.py``): the component is the actual code.tsx
implementation, auto-transformed to Babel-compatible JSX (TypeScript types
stripped, ``import``/``export`` removed, wrapped in an IIFE that exposes it on
``window``), and the preview loads React 18 UMD + Babel standalone + Tailwind
CDN + the shared ``--ds-*`` token block with a persisted no-flash light/dark
toggle.

The original previews used a broken pattern (a single ``<script type="text/babel">``
block with ES ``import`` statements, no ``data-presets="react"``, and no
``window`` exposure), so Babel standalone could not run them. This script
fixes that by reusing the exact preview architecture the buttons family uses.

    python3 _gen_react_inputs_preview.py            # rewrite all previews
    python3 _gen_react_inputs_preview.py --check    # report drift, no writes

esbuild (build-time-only, not committed) must be at /tmp/dsbuild, same as the
buttons generator.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "React/Components/Inputs"

# Reuse the proven transform + shared blocks from the buttons generator so the
# two React families stay architecturally identical.
import _gen_react_buttons as _buttons
_tsx_to_babel_component = _buttons._tsx_to_babel_component
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS
ICON_JS = _buttons.ICON_JS


def _export_name_from_tsx(tsx_text: str) -> str | None:
    m = re.search(r"export function ([A-Za-z_$][\w$]*)", tsx_text)
    return m.group(1) if m else None


def _extract_showcase(preview_text: str) -> str:
    """Pull the authored ``function Showcase() { ... }`` body out of an
    existing preview so the demonstrations are preserved verbatim.

    The Showcase is the demonstration JSX; everything else (the component
    body, the broken import, the render line, the theme listener) is replaced
    by the generated shell. The Showcase always renders into a single root,
    so it carries no dependency on the old container id.
    """
    m = re.search(r"function Showcase\(\)\s*\{.*?\n\}", preview_text, re.S)
    if not m:
        raise RuntimeError("could not find function Showcase() in preview")
    return m.group(0).strip() + "\n"


def render_preview(folder: Path, slug: str) -> str:
    tsx = (folder / "code.tsx").read_text(encoding="utf-8")
    main_name = _export_name_from_tsx(tsx)
    if not main_name:
        raise RuntimeError(f"no `export function` found in {folder/'code.tsx'}")
    component_js = _tsx_to_babel_component(tsx, expose_name=main_name)

    # Preserve the authored Showcase from the current preview.
    preview_text = (folder / "preview.html").read_text(encoding="utf-8")
    showcase = _extract_showcase(preview_text)

    meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    title = meta.get("name", slug.replace("-", " ").title())
    lede = meta.get("description", "")
    eyebrow = f"React Component · {meta.get('subcategory', 'Inputs')}"

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — DevSnips React</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<script src="https://cdn.tailwindcss.com"></script>
<script>
{TAILWIND_CONFIG}
  // Apply token CSS variables before paint to avoid a flash in dark mode.
</script>
<style>
{TOKEN_BLOCK}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Inputs / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <main class="ds-main">
    <p class="ds-eyebrow">{eyebrow}</p>
    <h1 class="ds-title">{title}</h1>
    <p class="ds-lede">{lede}</p>
    <div id="ds-root" class="ds-pos-wrap"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Inputs · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
// Preview demonstration environment. The shared Icon set + hooks are inlined
// so the preview is fully standalone (unused hooks are tree-shaken by the
// browser at runtime; they add no behavior).
{ICON_JS}
</script>
<script type="text/babel" data-presets="react">
// The component below is the actual code.tsx implementation, transformed to
// JSX (types removed) so Babel standalone can run it. It is identical in
// behavior to code.tsx/code.jsx.
{component_js}
</script>
<script type="text/babel" data-presets="react">
{showcase}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
</script>
</body>
</html>
"""


def main(check: bool = False) -> None:
    folders = sorted(d for d in INPUTS.iterdir() if (d / "code.tsx").exists())
    if not folders:
        print("No input folders with code.tsx found under", INPUTS)
        sys.exit(1)
    drift = []
    wrote = 0
    for folder in folders:
        slug = folder.name
        try:
            content = render_preview(folder, slug)
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR building {slug}: {exc}")
            drift.append(str(folder / "preview.html"))
            continue
        p = folder / "preview.html"
        if check:
            if not p.exists() or p.read_text(encoding="utf-8") != content:
                drift.append(str(p))
        else:
            p.write_text(content, encoding="utf-8")
            wrote += 1
    if check:
        if drift:
            print("DRIFT detected in:")
            for d in drift:
                print("  " + d)
            sys.exit(1)
        print(f"OK: {len(folders)} input previews up to date.")
    else:
        print(f"Wrote {wrote} input previews.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
