#!/usr/bin/env python3
"""DevSnips React Accordion generator.

For every accordion variant in ``React/Components/Accordion/`` this
generator:
  - reads the authored reference ``accordion/code.tsx`` (the primary,
    fully-typed implementation of the shared compound core),
  - derives every other variant's ``code.tsx`` from it (identical shared
    core, only the header doc comment differs — registered as
    ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports +
    the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture (the
    actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped in an
    IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Accordion is a multi-export compound family (`Accordion`, `AccordionItem`,
`AccordionTrigger`, `AccordionContent`), so it reuses the alerts/dialogs
multi-export esbuild parity conversion.

Author the reference ``accordion/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_accordion_registry.py``, then run:

    python3 _gen_react_accordion.py            # write everything
    python3 _gen_react_accordion.py --check    # report drift, no writes

esbuild (build-time-only, not committed) must be at /tmp/dsbuild.
"""
from __future__ import annotations
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ACCORDION = ROOT / "React/Components/Accordion"
REFERENCE = "accordion"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base icon set + the breadcrumb/menu/dialog glyphs + the alert status
# glyphs; the accordion showcases need no extra icons beyond those.
import _gen_react_alerts as _alerts
ICON_JS = _alerts.ICON_JS

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
    return (ACCORDION / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


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
    # Registry text is markdown-ish prose; escape it before injecting into HTML
    # so component-like substrings (e.g. `<Accordion>`) never parse as tags.
    title = html.escape(spec["title"])
    description = html.escape(spec["description"])
    subcategory = html.escape(spec["subcategory"])
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Accordion / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <main class="ds-main">
    <p class="ds-eyebrow">React Component · {subcategory}</p>
    <h1 class="ds-title">{title}</h1>
    <p class="ds-lede">{description}</p>
    <div id="ds-root" class="ds-pos-wrap"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Accordion · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "accordion",
        "family": "accordion",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Accordion",
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


COMPOSITION = """- `Accordion` — the root provider: owns the open-item state (controlled `value` + `onValueChange`, or uncontrolled `defaultValue`), picks the expansion mode (`type="single"` default, `type="multiple"`), and derives the stable per-instance id base every trigger/region pair is built from.
- `AccordionItem` — one entry in the divided list (`border-b`, removed on the last item). Requires a unique id-safe `value`; computes its own open state from the root and derives the trigger/region ids.
- `AccordionTrigger` — the disclosure control: a real `<button type="button">` inside an `<h3>` heading, with `aria-expanded` + `aria-controls`, an optional leading `icon` (`aria-hidden`), an optional trailing `badge` pill, an optional `description` line, and the rotating chevron (also `aria-hidden`).
- `AccordionContent` — the collapsible region: `role="region"` labelled by its trigger, animated with the CSS grid-rows trick (no JavaScript measurement), hidden from the accessibility tree and tab order while closed.

Compose only what an entry needs — a bare trigger + content pair is valid; so is the full icon + description + badge composition."""


ACCORDION_PROPS = r"""### `<Accordion>`

| Name | Type | Default | Description |
|---|---|---|---|
| `type` | `"single" \| "multiple"` | `"single"` | Expansion mode: `single` keeps at most one item open; `multiple` lets any number stay open. |
| `collapsible` | `boolean` | `false` | Single mode only: allow the open item to be closed by activating its trigger again. When `false`, the open item's trigger is a no-op. Ignored in multiple mode. |
| `value` | single: `string \| null` · multiple: `string[]` | — | Controlled open value(s). The TypeScript type is discriminated by `type`, so it always matches the mode. |
| `defaultValue` | single: `string \| null` · multiple: `string[]` | — | Initial open value(s) when uncontrolled. |
| `onValueChange` | single: `(value: string \| null) => void` · multiple: `(value: string[]) => void` | — | Called with the next open value(s) whenever a trigger toggles an item. |
| `className` | `string` | — | Extra classes on the root div (for example the bordered-container treatment). |
| `children` | `ReactNode` | — | `AccordionItem` entries. |

Every other attribute of a plain `<div>` (`aria-*`, `data-*`, …) is forwarded to the root."""

ITEM_PROPS = r"""### `<AccordionItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | required | Unique, id-safe identifier for the item within the accordion. It keys the open state and derives the trigger/region ids, so keep it stable and free of whitespace. |
| `disabled` | `boolean` | `false` | Disable the item: the trigger becomes natively `disabled` — unfocusable, not activatable, exposed as disabled to assistive technology. |
| `className` | `string` | — | Extra classes on the item div. |
| `children` | `ReactNode` | — | One `AccordionTrigger` + one `AccordionContent`. |

Every other attribute of a plain `<div>` is forwarded."""

TRIGGER_PROPS = r"""### `<AccordionTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Leading visual affordance, rendered `aria-hidden` — it supplements the trigger text, never replaces it. |
| `badge` | `ReactNode` | — | Short status/count content rendered as a neutral pill before the chevron. It is plain text inside the button, so it joins the accessible name — keep it short and meaningful. |
| `description` | `ReactNode` | — | A short supporting line under the title. Also part of the accessible name — keep it brief. |
| `onClick` | `(event) => void` | — | Runs before the toggle; call `event.preventDefault()` to veto it. |
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | The trigger title (required — it is the accessible name). |

The rendered element is a real `<button type="button">` wrapped in an `<h3>`; every other button attribute (`aria-*`, `data-*`, …) is forwarded. `disabled` is set on `<AccordionItem>`, not here."""

CONTENT_PROPS = r"""### `<AccordionContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the inner content div (padding, typography overrides). |
| `children` | `ReactNode` | — | Region content — paragraphs, lists, real controls. |

The region element is `role="region"` with `aria-labelledby` pointing at its trigger; `className` and forwarded attributes (for example `aria-busy`) land on the inner content div. Content stays mounted while closed so state inside it survives a close/reopen cycle."""


def props_table():
    return "\n\n".join([ACCORDION_PROPS, ITEM_PROPS, TRIGGER_PROPS, CONTENT_PROPS])


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

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`); no component-specific values are invented. Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This accordion follows the token system rules: 1px `color.border` dividers, `color.surface-hover` trigger feedback, body-sm text, the `color.focus-ring` token for keyboard focus (drawn inset so bordered containers never clip it), and `color.muted-foreground` for supporting text, icons, and badges.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_accordion_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_accordion_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_accordion"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = ACCORDION / slug
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
        print(f"OK: {len(COMPONENTS)} accordion variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} accordion variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
