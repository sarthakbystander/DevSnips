#!/usr/bin/env python3
"""DevSnips React Breadcrumbs generator.

For every breadcrumb variant in ``React/Components/Breadcrumbs/`` this
generator:
  - reads the authored ``code.tsx`` (the primary, fully-typed implementation),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    + the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Breadcrumbs is a multi-export compound family (`Breadcrumbs`, `BreadcrumbList`,
`BreadcrumbItem`, `BreadcrumbLink`, `BreadcrumbCurrent`, `BreadcrumbSeparator`,
plus `BreadcrumbDropdown` on the dropdown variant and `BreadcrumbEllipsis` on
the collapsed variant), so it reuses the tabs multi-export esbuild parity
conversion.

Author ``code.tsx`` per variant, register metadata in
``_gen_react_breadcrumbs_registry.py``, then run:

    python3 _gen_react_breadcrumbs.py            # write everything
    python3 _gen_react_breadcrumbs.py --check    # report drift, no writes

esbuild (build-time-only, not committed) must be at /tmp/dsbuild.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BREADCRUMBS = ROOT / "React/Components/Breadcrumbs"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# The shared preview Icon set grows a few navigation glyphs the breadcrumb
# showcases need (home, docs, components, products, folder).
_EXTRA_ICON_CASES = (
    '    case "home": return (<svg {...common}><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
    '<path d="M9 22V12h6v10"/></svg>);\n'
    '    case "folder": return (<svg {...common}><path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/></svg>);\n'
    '    case "book": return (<svg {...common}><path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/></svg>);\n'
    '    case "grid": return (<svg {...common}><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>);\n'
    '    case "package": return (<svg {...common}><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>);\n'
)
ICON_JS = _buttons.ICON_JS.replace(
    "    default: return null;",
    _EXTRA_ICON_CASES + "    default: return null;",
)
assert _EXTRA_ICON_CASES.strip().splitlines()[0] in ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             composition_note, keyboard_doc, behavior_doc, a11y_doc,
             responsive_doc, notes_doc, showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, composition_note=composition_note,
        keyboard_doc=keyboard_doc, behavior_doc=behavior_doc,
        a11y_doc=a11y_doc, responsive_doc=responsive_doc,
        notes_doc=notes_doc, showcase=showcase,
    )


def _esbuild_run(tsx_text: str) -> str:
    """Run a tsx body through esbuild, returning ESM JavaScript (types
    stripped, JSX preserved)."""
    with tempfile.NamedTemporaryFile("w", suffix=".tsx", delete=False) as f:
        f.write(tsx_text)
        path = f.name
    try:
        return subprocess.run(
            [ESBUILD, path, "--jsx=preserve", "--format=esm"],
            capture_output=True, text=True, check=True,
        ).stdout
    finally:
        Path(path).unlink(missing_ok=True)


def _export_names(tsx_text: str) -> list[str]:
    """All `export function <Name>` declarations in the tsx source."""
    return re.findall(r"export function ([A-Za-z_$][\w$]*)", tsx_text)


def _default_export(tsx_text: str) -> str | None:
    m = re.search(r"export default ([A-Za-z_$][\w$]*)\s*;", tsx_text)
    return m.group(1) if m else None


def render_code_tsx(folder: Path) -> str:
    return (folder / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


def render_code_jsx(folder: Path) -> str:
    tsx = render_code_tsx(folder)
    names = _export_names(tsx)
    default = _default_export(tsx)
    body = _esbuild_run(tsx).replace("void 0", "undefined")
    # esbuild hoists exports to a trailing block; replace it with a clean,
    # human-readable export statement that preserves every named export.
    body = re.sub(r"\nvar [a-z0-9_]+_default = [A-Za-z_$][\w$]*;\n", "\n", body)
    body = re.sub(r"\nexport \{[^}]*\};?\s*$", "\n", body)
    exports = ""
    if names:
        exports += "export { " + ", ".join(names) + " };\n"
    if default:
        exports += f"\nexport default {default};\n"
    header = (
        "/* DevSnips React — JavaScript parity build.\n"
        " * Same API, behavior, and classes as code.tsx; TypeScript types removed.\n"
        " * Regenerated from code.tsx — edit code.tsx and re-run the generator.\n"
        " */\n\n"
    )
    return header + body.rstrip() + "\n\n" + exports


def _tsx_to_babel_component(tsx_text: str) -> str:
    tsx, names = tsx_text, _export_names(tsx_text)
    body = _esbuild_run(tsx)
    body = re.sub(r"\nvar [a-z0-9_]+_default = [A-Za-z_$][\w$]*;\n", "\n", body)
    body = re.sub(r"\nexport \{[^}]*\};?\s*$", "\n", body)
    body = re.sub(r"\bexport (function|const|class|let|var)\b", r"\1", body)
    body = re.sub(r"\nexport default [A-Za-z_$][\w$]*;\s*$", "\n", body)
    body = re.sub(
        r'(?m)^import \{([^}]+)\} from "react";',
        lambda m: f"const {{ {m.group(1)} }} = React;",
        body,
    )
    body = re.sub(r'(?m)^import [^;]+;\n', "", body)
    indented = "\n".join("  " + ln if ln else ln for ln in body.rstrip().splitlines())
    assigns = "".join(f"\n  window.{name} = {name};" for name in names)
    return "(function() {\n" + indented + assigns + "\n})();\n"


def render_preview(folder: Path, slug: str, spec: dict) -> str:
    tsx = render_code_tsx(folder)
    names = _export_names(tsx)
    if not names:
        raise RuntimeError(f"no `export function` in {folder/'code.tsx'}")
    component_js = _tsx_to_babel_component(tsx)
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Breadcrumbs / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Breadcrumbs · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "breadcrumbs",
        "family": "breadcrumbs",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Breadcrumbs",
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


COMPOSITION = """Breadcrumbs is a compound component. Six primitives compose the pattern:

```tsx
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>
```

- `Breadcrumbs` — the root `<nav aria-label="Breadcrumb">` landmark. Provides the default `separator` to every separator through context.
- `BreadcrumbList` — the ordered list (`<ol>`). Wraps onto multiple lines instead of scrolling horizontally.
- `BreadcrumbItem` — one level of the trail (`<li>`).
- `BreadcrumbLink` — a real `<a href>` for navigable levels: normal browser navigation, optional leading `icon`.
- `BreadcrumbCurrent` — the current page: plain text with `aria-current="page"`, never a link.
- `BreadcrumbSeparator` — decorative structure between levels (`role="presentation"`, `aria-hidden`); renders its own `children`, else the `separator` given to `<Breadcrumbs>`, else the default chevron."""

A11Y_STRUCTURE = """The structure follows the W3C Breadcrumb pattern: a `<nav aria-label="Breadcrumb">` landmark containing an ordered list (`<ol>`) whose last item is the current page marked with `aria-current="page"`.

- Every navigable level is a real `<a href>` — normal browser navigation, no click handlers faking links.
- The current page is plain text, not a link; assistive technology announces it as the current page.
- Separators are `aria-hidden` `role="presentation"` list items — never announced, never focusable.
- Icons are decorative (`aria-hidden`); the visible label always carries the accessible name."""

KEYBOARD_BASE = """| Key | Behavior |
|---|---|
| `Tab` / `Shift+Tab` | Move focus through the links |
| `Enter` | Follow the focused link |"""

KEYBOARD_MENU = """| Key | Behavior |
|---|---|
| `Enter` / `Space` / `ArrowDown` | Open the menu and focus the first item |
| `ArrowUp` (closed) | Open the menu and focus the last item |
| `ArrowDown` / `ArrowUp` (open) | Move between menu items (wraps around) |
| `Home` / `End` | Jump to the first / last menu item |
| `Enter` | Follow the focused menu link |
| `Escape` | Close the menu and return focus to the trigger |
| `Tab` | Close the menu and continue through the page |"""

STATES = """- **Link** — muted foreground; hover shifts to the foreground color with an underline.
- **Current page** — foreground color at medium weight; not interactive.
- **Separator** — muted decorative glyph, hidden from assistive technology.
- **Focus-visible** — `--ds-color-focus-ring` outline on links and menu triggers in both themes."""

RESPONSIVE_BASE = """The list uses `flex-wrap` with a `min-w-0` flexible item per level, so long trails wrap onto multiple lines instead of forcing page-level horizontal scrolling. From 375px up, prefer intentional reduction over squeezing: collapse middle levels with `breadcrumbs-collapsed` and cap long labels with `breadcrumbs-max-width`."""


def render_readme(spec, slug) -> str:
    keyboard = spec["keyboard_doc"] or KEYBOARD_BASE
    return f"""# {spec["title"]}

{spec["description"]}

## Usage

```tsx
{spec["usage"]}
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
{spec["usage"]}
```

## Props

{spec["props_doc"]}

## Composition

{COMPOSITION}

{spec["composition_note"]}

## Keyboard Interaction

{keyboard}

## Accessibility

{A11Y_STRUCTURE}

{spec["a11y_doc"]}

## States

{spec["behavior_doc"]}

## Responsive Behavior

{spec["responsive_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This breadcrumb variant uses the semantic color, radius, typography, and motion tokens.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_breadcrumbs_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_breadcrumbs_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_breadcrumbs"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = BREADCRUMBS / slug
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
        print(f"OK: {len(COMPONENTS)} breadcrumbs up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} breadcrumbs.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
