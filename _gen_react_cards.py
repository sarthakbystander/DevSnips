#!/usr/bin/env python3
"""DevSnips React Cards generator.

For every card variant in ``React/Components/Cards/`` this generator:
  - reads the authored reference ``card/code.tsx`` (the primary, fully-typed
    implementation of the shared compound core),
  - derives every other variant's ``code.tsx`` from it (identical shared
    core, only the header doc comment differs — registered as ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports +
    the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture (the
    actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped in an
    IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Cards is a multi-export compound family (`Card`, `CardHeader`, `CardTitle`,
`CardDescription`, `CardAction`, `CardContent`, `CardFooter`, `CardMedia`,
`SelectableCard`, `SelectableCardGroup`, `InteractiveCard`, `CardSkeleton`),
so it reuses the dialogs multi-export esbuild parity conversion.

Author the reference ``card/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_cards_registry.py``, then run:

    python3 _gen_react_cards.py            # write everything
    python3 _gen_react_cards.py --check    # report drift, no writes

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
CARDS = ROOT / "React/Components/Cards"
REFERENCE = "card"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base icon set + the dropdowns glyphs + the dialog glyphs, plus the card
# glyphs the showcases use (stats, media, layout).
import _gen_react_dialogs as _dialogs
_EXTRA_ICON_CASES = (
    '    case "trending-up": return (<svg {...common}><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
    '<polyline points="16 7 22 7 22 13"/></svg>);\n'
    '    case "trending-down": return (<svg {...common}><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/>'
    '<polyline points="16 17 22 17 22 11"/></svg>);\n'
    '    case "image": return (<svg {...common}><rect width="18" height="18" x="3" y="3" rx="2"/>'
    '<circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>);\n'
    '    case "layers": return (<svg {...common}><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.57 3.91a2 2 0 0 0 1.66 0l8.57-3.91a1 1 0 0 0 0-1.83z"/>'
    '<path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/></svg>);\n'
)
ICON_JS = _dialogs.ICON_JS.replace(
    "    default: return null;",
    _EXTRA_ICON_CASES + "    default: return null;",
)
assert _EXTRA_ICON_CASES.strip().splitlines()[0] in ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             composition_note, logic_doc, keyboard_doc, behavior_doc,
             a11y_doc, responsive_doc, notes_doc, tsx_header, showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, composition_note=composition_note,
        logic_doc=logic_doc, keyboard_doc=keyboard_doc,
        behavior_doc=behavior_doc, a11y_doc=a11y_doc,
        responsive_doc=responsive_doc, notes_doc=notes_doc,
        tsx_header=tsx_header, showcase=showcase,
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


def read_reference_tsx() -> str:
    return (CARDS / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


def render_code_tsx(slug: str, spec: dict) -> str:
    """The reference variant keeps its authored code.tsx; every other variant
    is derived: reference core with the header doc comment swapped for the
    variant's registered ``tsx_header``."""
    if slug == REFERENCE:
        return read_reference_tsx()
    reference = read_reference_tsx()
    m = re.search(r"/\*\*.*?\*/", reference, flags=re.S)
    if not m:
        raise RuntimeError("reference code.tsx is missing its header doc comment")
    header = spec["tsx_header"].strip("\n")
    return reference[: m.start()] + header + reference[m.end():]


def render_code_jsx(tsx: str) -> str:
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


def render_preview(tsx: str, slug: str, spec: dict) -> str:
    names = _export_names(tsx)
    if not names:
        raise RuntimeError(f"no `export function` in code.tsx for {slug}")
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Cards / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Cards · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
// Preview demonstration environment. The shared Icon set is inlined so the
// preview is fully standalone.
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
        "component": "card",
        "family": "cards",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Cards",
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


COMPOSITION = """- `Card` — the root surface (radius-md, 1px border, surface color, shadow-xs). A plain `<div>` that only carries structure — it adds no fake interactivity.
- `CardHeader` — the header grid: title + description in a text column, an optional `CardAction` slot at the top right.
- `CardTitle` — a real `<h3>` heading (cards are page regions, so titles are headings).
- `CardDescription` — a `<p>` of muted supporting text.
- `CardAction` — the header action slot (icon buttons, a menu trigger).
- `CardContent` — the padded body region between header and footer.
- `CardFooter` — the action row; buttons stack full-width below `sm` and lay out inline from `sm` up (same recipe as the dialog footer).
- `CardMedia` — an image framed in a crop box (`video` 16:9 / `square` 1:1 / `none` natural) with graceful fallback when `src` is omitted.
- `SelectableCard` — a native `<input type="radio">` / `type="checkbox">` whose whole card is its `<label>`; controlled and uncontrolled.
- `SelectableCardGroup` — a `<fieldset>`/`<legend>` radio group owning the single selection for single-choice card pickers.
- `InteractiveCard` — a real `<a href>` when `href` is set (navigation), otherwise a real `<button type="button">` (actions).
- `CardSkeleton` — the loading placeholder: `aria-busy` + visually hidden label, reduced-motion-safe pulse.

Compose only the primitives a card actually needs — a plain `Card` with `CardContent` and no header or footer is valid."""

BASE_PROPS = r"""### `<Card>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the surface. |
| `children` | `ReactNode` | — | Header, content, footer, and/or media regions. |

Every attribute of a plain `<div>` (`id`, `aria-*`, `data-*`, …) is forwarded. The card itself is non-interactive — use `InteractiveCard` or `SelectableCard` for click targets."""

HEADER_PROPS = r"""### `<CardHeader>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the header grid. |
| `children` | `ReactNode` | — | `CardTitle`, `CardDescription`, and optionally `CardAction`. |

A `grid-cols-[1fr_auto]`: title + description stack in the text column; an optional `CardAction` sits at the top of the auto-sized action column."""

TITLE_PROPS = r"""### `<CardTitle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the heading. |
| `children` | `ReactNode` | — | Title text. |

A real `<h3>` — if the page outline needs a different rank, pass the heading element semantics via your page structure (the visual style stays the same)."""

DESCRIPTION_PROPS = r"""### `<CardDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the paragraph. |
| `children` | `ReactNode` | — | Supporting description text. |"""

ACTION_PROPS = r"""### `<CardAction>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the action slot. |
| `children` | `ReactNode` | — | Icon buttons / a menu trigger (compose the DevSnips Buttons/Dropdowns families). |"""

CONTENT_PROPS = r"""### `<CardContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the body region. |
| `children` | `ReactNode` | — | The main card content. |"""

FOOTER_PROPS = r"""### `<CardFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the footer row (alignment: `sm:justify-end` / `sm:justify-between`). |
| `children` | `ReactNode` | — | Footer actions and metadata. |

Actions stack full-width below `sm` (primary last in DOM lands on top) and lay out inline from `sm` up. No baked-in justify utility, so alignment overrides never conflict."""

MEDIA_PROPS = r"""### `<CardMedia>`

| Name | Type | Default | Description |
|---|---|---|---|
| `src` | `string` | — | Image URL. Omit it to render the decorative `aria-hidden` placeholder (the layout never collapses). |
| `alt` | `string` | `""` | Alternative text; `""` marks decorative images — meaningful images must pass real alt text. |
| `aspect` | `"video" \| "square" \| "none"` | `"video"` | Crop box: 16:9, 1:1, or natural height (for fixed-size layouts like horizontal cards). |
| `className` | `string` | — | Extra classes on the media frame; the image fills it with `object-cover`. |

Every attribute of a plain `<img>` (`loading`, `sizes`, `srcSet`, …) is forwarded."""

SELECTABLE_PROPS = r"""### `<SelectableCard>`

| Name | Type | Default | Description |
|---|---|---|---|
| `type` | `"checkbox" \| "radio"` | `"checkbox"` | `checkbox` for independent multi-select; `radio` for single choice within a `name` (`SelectableCardGroup` renders this for each option). |
| `label` | `ReactNode` | — | Visible card label; also the input's accessible name. |
| `description` | `ReactNode` | — | Supporting text, wired via `aria-describedby`. |
| `checked` / `defaultChecked` | `boolean` | — | Controlled (with `onChange`) or uncontrolled selection. |
| `onChange` | `(event) => void` | — | Native change event handler. |
| `disabled` / `required` | `boolean` | — | Native input semantics. |
| `name` / `value` | `string` | — | Native form association. |
| `id` | `string` | — | Explicit input id (generated with `useId` otherwise). |

The whole card is the `<label htmlFor>` of a real native input: clicking anywhere on the card toggles it, Space toggles, radio groups keep browser arrow-key navigation, and forms submit the value."""

GROUP_PROPS = r"""### `<SelectableCardGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `legend` | `ReactNode` | — | Visible `<legend>` for the fieldset. |
| `options` | `SelectableCardOption[]` | — | `{ value, label, description?, disabled? }[]`. |
| `value` / `defaultValue` | `string` | — | Controlled (with `onChange`) or uncontrolled selected option value. |
| `onChange` | `(value, event) => void` | — | Called with the newly selected option value. |
| `disabled` / `required` | `boolean` | — | Applied to every option. |
| `name` | `string` | — | Radio group name (generated otherwise). |
| `columns` | `1 \| 2 \| 3` | `1` | Card columns from `sm` up. |

Single choice via `<input type="radio">` cards. The group owns the value and passes controlled `checked` down, so uncontrolled mode stays in sync even though a deselected radio receives no change event of its own — the same group-tracking recipe the radio family uses."""

INTERACTIVE_PROPS = r"""### `<InteractiveCard>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | — | Destination URL; renders a real `<a>`. Omit `href` and the card renders a real `<button type="button">` for actions. |
| `onClick` / `disabled` | — | — | Button-mode props (action cards). `disabled` only exists on the button branch (anchors cannot be disabled natively). |
| `className` | `string` | — | Extra classes on the control. |
| `children` | `ReactNode` | — | `CardHeader` / `CardContent` sections rendered inside the single control. |

The whole card is one real control — anchor for navigation, button for actions. Do not nest other interactive elements inside it; put secondary actions in a sibling `CardAction` slot of a plain `Card`."""

SKELETON_PROPS = r"""### `<CardSkeleton>`

| Name | Type | Default | Description |
|---|---|---|---|
| `media` | `boolean` | `false` | Render a 16:9 media placeholder block. |
| `lines` | `number` | `2` | Number of body placeholder lines (minimum 1). |
| `footer` | `boolean` | `false` | Render an action-row placeholder. |
| `label` | `string` | `"Loading…"` | Visually hidden announcement while the card carries `aria-busy="true"`. |
| `className` | `string` | — | Extra classes on the surface (e.g. width in a grid). |"""


def props_table():
    return "\n\n".join([
        BASE_PROPS, HEADER_PROPS, TITLE_PROPS, DESCRIPTION_PROPS, ACTION_PROPS,
        CONTENT_PROPS, FOOTER_PROPS, MEDIA_PROPS, SELECTABLE_PROPS, GROUP_PROPS,
        INTERACTIVE_PROPS, SKELETON_PROPS,
    ])


def render_readme(spec, slug) -> str:
    return f"""# {spec["title"]}

{spec["description"]}

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

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

## Behavior

{spec["logic_doc"]}

## Keyboard Interaction

{spec["keyboard_doc"]}

## Accessibility

{spec["a11y_doc"]}

## States

{spec["behavior_doc"]}

## Responsive Behavior

{spec["responsive_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_cards_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_cards_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_cards"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = CARDS / slug
        folder.mkdir(parents=True, exist_ok=True)
        tsx = render_code_tsx(slug, spec)
        files = {
            "code.tsx": tsx,
            "code.jsx": render_code_jsx(tsx),
            "preview.html": render_preview(tsx, slug, spec),
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
        print(f"OK: {len(COMPONENTS)} card variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} card variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
