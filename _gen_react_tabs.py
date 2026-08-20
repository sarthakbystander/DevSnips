#!/usr/bin/env python3
"""DevSnips React Tabs generator.

For every tab variant in ``React/Components/Tabs/`` this generator:
  - reads the authored ``code.tsx`` (the primary, fully-typed implementation),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    + the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Tabs is the first multi-export family (`Tabs`, `TabsList`, `TabsTrigger`,
`TabsContent`, plus `TabsAddAction` on the add-action variant), so it has its
own esbuild parity conversion — the buttons converter assumes one export.

Author ``code.tsx`` per variant, register metadata in
``_gen_react_tabs_registry.py``, then run:

    python3 _gen_react_tabs.py            # write everything
    python3 _gen_react_tabs.py --check    # report drift, no writes

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
TABS = ROOT / "React/Components/Tabs"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS
ICON_JS = _buttons.ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, props_doc, composition_note,
             behavior_doc, a11y_doc, notes_doc, showcase, extra=None):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, props_doc=props_doc,
        composition_note=composition_note, behavior_doc=behavior_doc,
        a11y_doc=a11y_doc, notes_doc=notes_doc, showcase=showcase,
        extra=extra or [],
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
    extra_js = ""
    for dep_slug in spec.get("extra", []):
        if dep_slug in COMPONENTS and dep_slug != slug:
            dep_folder = TABS / dep_slug
            dep_tsx = render_code_tsx(dep_folder)
            extra_js += "\n// sibling component: " + dep_slug + "\n"
            extra_js += _tsx_to_babel_component(dep_tsx)
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Tabs / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Tabs · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "tabs",
        "family": "tabs",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Tabs",
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


COMPOSITION = """Tabs is a compound component. Four primitives compose the pattern:

```tsx
<Tabs defaultValue="overview">
  <TabsList aria-label="Project navigation">
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="activity">Activity</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">…</TabsContent>
  <TabsContent value="activity">…</TabsContent>
</Tabs>
```

- `Tabs` — the root provider. Owns the selected value (controlled via `value` + `onValueChange`, uncontrolled via `defaultValue`) and the `orientation` (`"horizontal"` | `"vertical"`).
- `TabsList` — renders `role="tablist"` and owns arrow-key / Home / End navigation with automatic activation.
- `TabsTrigger` — renders a native `<button role="tab">` with roving `tabIndex`, plus the optional `icon` / `badge` / `count` content props.
- `TabsContent` — renders the `role="tabpanel"`. Every panel stays mounted; inactive panels carry the `hidden` attribute, so form and input state inside a panel is preserved."""

KEYBOARD = """| Key | Horizontal tabs | Vertical tabs |
|---|---|---|
| `ArrowRight` | Move focus + activate the next tab | — |
| `ArrowLeft` | Move focus + activate the previous tab | — |
| `ArrowDown` | — | Move focus + activate the next tab |
| `ArrowUp` | — | Move focus + activate the previous tab |
| `Home` | Activate the first tab | Activate the first tab |
| `End` | Activate the last tab | Activate the last tab |

Navigation wraps around the ends. Automatic activation is used: focus and selection move together through the tablist. Disabled tabs are skipped by arrow keys and removed from the tab order. Only the selected tab sits in the tab order (roving `tabIndex`)."""

A11Y_STRUCTURE = """The structure follows the W3C Tabs pattern: one `role="tablist"` containing native `<button role="tab">` triggers, with `role="tabpanel"` content regions.

- Trigger → panel association: `aria-controls` points at the panel id; the panel answers with `aria-labelledby` pointing back at the trigger id.
- `aria-selected` mirrors the current selection on every trigger.
- Panels stay focusable (`tabIndex={0}`) so keyboard users can read into scrollable content."""


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

## Composition

{COMPOSITION}

{spec["composition_note"]}

## Keyboard Interaction

{KEYBOARD}

## Accessibility

{A11Y_STRUCTURE}

{spec["a11y_doc"]}

## States

{spec["behavior_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-active)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This tabs variant uses the semantic color, radius, spacing, and motion tokens.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_tabs_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_tabs_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_tabs"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = TABS / slug
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
        print(f"OK: {len(COMPONENTS)} tabs up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} tabs.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
