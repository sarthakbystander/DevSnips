#!/usr/bin/env python3
"""DevSnips React Radios generator.

For every radio in ``React/Components/Radios/`` this generator:
  - reads the authored ``code.tsx`` (the primary, fully-typed implementation),
  - derives ``code.jsx`` via esbuild (TS types stripped, ``export`` restored),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing the component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Author ``code.tsx`` per variant, register metadata in
``_gen_react_checkboxes_radios_registry.py``, then run:

    python3 _gen_react_radios.py            # write everything
    python3 _gen_react_radios.py --check    # report drift, no writes

esbuild (build-time-only, not committed) must be at /tmp/dsbuild.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RADIOS = ROOT / "React/Components/Radios"

import _gen_react_buttons as _buttons
_ts_to_jsx = _buttons._ts_to_jsx
_tsx_to_babel_component = _buttons._tsx_to_babel_component
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS
ICON_JS = _buttons.ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, props_doc, behavior_doc,
             a11y_doc, notes_doc, showcase, extra=None):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, props_doc=props_doc,
        behavior_doc=behavior_doc, a11y_doc=a11y_doc, notes_doc=notes_doc,
        showcase=showcase, extra=extra or [],
    )


def _export_name_from_tsx(tsx_text: str) -> str | None:
    m = re.search(r"export function ([A-Za-z_$][\w$]*)", tsx_text)
    return m.group(1) if m else None


def render_code_tsx(folder: Path) -> str:
    return (folder / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


def render_code_jsx(folder: Path) -> str:
    tsx = render_code_tsx(folder)
    name = _export_name_from_tsx(tsx)
    body = _ts_to_jsx(tsx, export_name=name)
    header = (
        "/* DevSnips React — JavaScript parity build.\n"
        " * Same API, behavior, and classes as code.tsx; TypeScript types removed.\n"
        " * Regenerated from code.tsx — edit code.tsx and re-run the generator.\n"
        " */\n\n"
    )
    return header + body


def render_preview(folder: Path, slug: str, spec: dict) -> str:
    tsx = render_code_tsx(folder)
    main_name = _export_name_from_tsx(tsx)
    if not main_name:
        raise RuntimeError(f"no `export function` in {folder/'code.tsx'}")
    component_js = _tsx_to_babel_component(tsx, expose_name=main_name)
    extra_js = ""
    for dep_slug in spec.get("extra", []):
        if dep_slug in COMPONENTS and dep_slug != slug:
            dep_folder = RADIOS / dep_slug
            dep_tsx = render_code_tsx(dep_folder)
            dep_name = _export_name_from_tsx(dep_tsx) or ""
            if dep_name:
                extra_js += "\n// sibling component: " + dep_slug + "\n"
                extra_js += _tsx_to_babel_component(dep_tsx, expose_name=dep_name)
    showcase = spec["showcase"].strip("\n")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{spec["title"]} — DevSnips React</title>
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Radios / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <main class="ds-main">
    <p class="ds-eyebrow">React Component · {spec["subcategory"]}</p>
    <h1 class="ds-title">{spec["title"]}</h1>
    <p class="ds-lede">{spec["description"]}</p>
    <div id="ds-root" class="ds-pos-wrap"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Radios · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
// so the preview is fully standalone.
{ICON_JS}
</script>
<script type="text/babel" data-presets="react">
// The component below is the actual code.tsx implementation, transformed to
// JSX (types removed) so Babel standalone can run it. It is identical in
// behavior to code.tsx/code.jsx.
{component_js}
{extra_js}
</script>
<script type="text/babel" data-presets="react">
{showcase}
ReactDOM.createRoot(document.getElementById("ds-root")).render(<Showcase />);
</script>
</body>
</html>
"""


def render_metadata(spec, slug) -> str:
    return json.dumps({
        "id": f"{slug}-react-001",
        "name": spec["title"],
        "slug": slug,
        "component": "radio",
        "family": "radios",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Radios",
        "subcategory": spec["subcategory"],
        "styling": "Tailwind CSS",
        "tags": spec["tags"],
        "features": spec["features"],
        "responsive": True,
        "darkMode": True,
        "accessibility": spec["accessibility"],
        "interactive": spec["interactive"],
        "dependencies": [],
        "source": "DevSnips",
        "related": spec["related"],
    }, indent=2) + "\n"


def render_readme(spec, slug) -> str:
    return f"""# {spec["title"]}

{spec["description"]}

## Usage

```tsx
{spec["props_doc"]["usage"]}
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
{spec["props_doc"]["usage"]}
```

## Props

{spec["props_doc"]["table"]}

## States

{spec["behavior_doc"]}

## Accessibility

{spec["a11y_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This radio uses the semantic color, radius, spacing, and motion tokens.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_checkboxes_radios_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_checkboxes_radios_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        import sys as _s
        _s.modules["_gen_react_radios"] = _s.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = RADIOS / slug
        folder.mkdir(parents=True, exist_ok=True)
        files = {
            "code.jsx": render_code_jsx(folder),
            "preview.html": render_preview(folder, slug, spec),
            "metadata.json": render_metadata(spec, slug),
            "README.md": render_readme(spec, slug),
        }
        for name, content in files.items():
            p = folder / name
            if check:
                if not p.exists() or p.read_text(encoding="utf-8") != content:
                    drift.append(str(p))
            else:
                p.write_text(content, encoding="utf-8")
    if check:
        if drift:
            print("DRIFT detected in:")
            for d in drift:
                print("  " + d)
            sys.exit(1)
        print(f"OK: {len(COMPONENTS)} radios up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} radios.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
