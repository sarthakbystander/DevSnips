#!/usr/bin/env python3
"""DevSnips React Tooltips generator.

For every tooltip variant in ``React/Components/Tooltips/`` this generator:
  - reads the authored reference ``tooltip/code.tsx`` (the primary, fully-typed
    implementation),
  - derives every other variant's ``code.tsx`` from it (identical shared core,
    only the header doc comment differs — registered as ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    + the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Tooltips is a multi-export compound family (`Tooltip`, `TooltipTrigger`,
`TooltipContent`), so it reuses the dialogs/dropdowns multi-export esbuild
parity conversion. Placement is resolved inside the component (no portal,
no positioning library).

Author the reference ``tooltip/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_tooltips_registry.py``, then run:

    python3 _gen_react_tooltips.py            # write everything
    python3 _gen_react_tooltips.py --check    # report drift, no writes

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
TOOLTIPS = ROOT / "React/Components/Tooltips"
REFERENCE = "tooltip"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base Icon set + the breadcrumb/menu/dialog glyphs, plus the tooltip glyphs
# the showcases use (lock, database).
import _gen_react_dialogs as _dialogs
_EXTRA_ICON_CASES = (
    '    case "lock": return (<svg {...common}><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
    '<path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>);\n'
    '    case "database": return (<svg {...common}><ellipse cx="12" cy="5" rx="9" ry="3"/>'
    '<path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>);\n'
)
ICON_JS = _dialogs.ICON_JS.replace(
    "    default: return null;",
    _EXTRA_ICON_CASES + "    default: return null;",
)
assert _EXTRA_ICON_CASES.strip().splitlines()[0] in ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             composition_note, logic_doc, positioning_doc, keyboard_doc,
             behavior_doc, a11y_doc, responsive_doc, notes_doc, tsx_header,
             showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, composition_note=composition_note,
        logic_doc=logic_doc, positioning_doc=positioning_doc,
        keyboard_doc=keyboard_doc, behavior_doc=behavior_doc,
        a11y_doc=a11y_doc, responsive_doc=responsive_doc,
        notes_doc=notes_doc, tsx_header=tsx_header, showcase=showcase,
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
    return (TOOLTIPS / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


def render_code_tsx(folder: Path, slug: str, spec: dict) -> str:
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Tooltips / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Tooltips · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "tooltip",
        "family": "tooltips",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Tooltips",
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


COMPOSITION = """- `Tooltip` — the root provider. Owns the open state (controlled `open` + `onOpenChange`, or uncontrolled `defaultOpen`), the placement config (`side`, `align`, `sideOffset`), the hover `delayDuration`, the `disabled` switch, and the generated tooltip id. Renders a `relative inline-flex` wrapper the content is positioned against.
- `TooltipTrigger` — clones its single child element (a real focusable element, or a `<span tabIndex={0}>` around a disabled control) to attach the trigger ref, the pointer/focus handlers, and `aria-describedby` pointing at the tooltip.
- `TooltipContent` — the `role="tooltip"` bubble plus its pointing arrow. Rendered only while open, `pointer-events-none` (a tooltip never carries interactive content), measured against the viewport before paint and flipped/shifted when the preferred placement would overflow."""

LOGIC_BASE = """The root `<Tooltip>` owns the open state. Both modes are supported:

- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultOpen`; the component owns the state.

Hover opens the tooltip after `delayDuration` (default 300 ms, so passing cursors do not flash it); keyboard focus opens it **immediately** — keyboard users never wait for a hover delay. The component tracks *what* opened it: a pointer-opened tooltip closes on pointer leave, a focus-opened tooltip closes on blur. If focus leaves while the pointer still hovers, ownership hands over to the pointer so the tooltip closes on pointer leave instead — the two gestures never fight.

Escape dismisses the open tooltip (focus stays on the trigger). The `disabled` prop suppresses opening entirely — and a tooltip that becomes disabled while open closes. A pending hover-open timer is cancelled on pointer leave and on unmount, so a tooltip never opens after its trigger is gone.

On touch devices there is no hover: tapping the trigger fires the same pointer path, so the tooltip appears on tap and dismisses on the next outside interaction. Touch users get the same content as pointer users."""

POSITIONING_BASE = """Placement is prop-driven — `side` (`top` / `right` / `bottom` / `left`) × `align` (`start` / `center` / `end`), with `sideOffset` (pixels, default 6) for the trigger gap. `center` aligns the tooltip's center with the trigger's center; `start` / `end` align the leading / trailing edges.

Before paint, `TooltipContent` measures itself and the trigger against the viewport (an 8px margin) and corrects the placement when it would overflow: `top` ↔ `bottom` and `left` ↔ `right` flip when the preferred side lacks room and the opposite side has more, and an `align` that would overflow an edge shifts toward the side with room (`center` degrades to `start` / `end` first). The correction runs in a layout effect while the content is still transparent, so the flip never flashes. `sideOffset` is applied after the flip, so the gap always points the right way.

The content is absolutely positioned inside the root's `relative inline-flex` wrapper — there is no portal and no positioning library. The bubble is capped at `min(16rem, 100vw - 2rem)` wide, so even long content stays inside a 375px viewport. One honest constraint of the no-portal approach: an ancestor with `overflow: hidden` (and a stacking trap) can clip the bubble — place the `<Tooltip>` outside clipping containers."""

KEYBOARD_BASE = """| Key | Behavior |
|---|---|
| `Tab` | Moves focus to the trigger; a focused trigger opens its tooltip immediately (no hover delay) |
| `Shift+Tab` / `Tab` away | Blur dismisses the tooltip |
| `Escape` | Dismiss the open tooltip; focus stays on the trigger |

The trigger is a real focusable element (a `<button>`, `<a>`, or — for a disabled control — a `<span tabIndex={0}>`), so Enter/Space activation and tab order follow normal browser behavior. The tooltip itself is not focusable and contains no interactive elements — it is announced through the trigger's `aria-describedby`."""

STATES_BASE = """- **Trigger** — the wrapped element keeps its own styling and its visible `:focus-visible` ring (`--ds-color-focus-ring`); the tooltip adds no visual state to the trigger.
- **Content** — `surface-elevated` with a 1px `--ds-color-border` and a restrained `--ds-shadow-sm`, radius-md, 13px/20px text, per the Dropdown / Popover / Tooltip token rules.
- **Arrow** — a rotated square sharing the content's surface and border, notched toward the trigger; follows the resolved placement (including after a flip).
- **Open transition** — a subtle 150ms opacity fade-in that doubles as the pre-measurement guard; `motion-reduce:transition-none` disables it.
- **Disabled** — the `disabled` prop suppresses opening; a natively `disabled` trigger cannot receive hover/focus, so the tooltip pattern for disabled controls is the focusable `<span tabIndex={0}>` wrapper (see `tooltip-disabled-trigger`)."""

A11Y_BASE = """The structure follows the WAI-ARIA tooltip pattern.

- The trigger is a real focusable element — a tooltip must never depend on hover alone. Keyboard focus opens the tooltip exactly like pointer hover.
- The tooltip is `role="tooltip"`, and the trigger carries `aria-describedby` pointing at the tooltip's id, so assistive technology announces the tooltip text as the trigger's description when it appears.
- The tooltip is `pointer-events-none` and never contains interactive content (links, buttons, inputs). Content that must be interacted with belongs in a popover or dialog, not a tooltip.
- A tooltip is **supplementary**: it must never be the only way to reach essential information. Everything it says is either repeated in the visible UI or genuinely optional detail.
- A natively `disabled` control does not receive hover or focus events, so a tooltip explaining *why* it is disabled must wrap it in a focusable `<span tabIndex={0}>` (the inner control gets `pointer-events-none`) — see `tooltip-disabled-trigger`."""

RESPONSIVE_BASE = """The bubble is capped at `min(16rem, 100vw - 2rem)` wide, wraps its text, and is measured against the viewport before paint — flipping sides or shifting alignment when it would overflow. The trigger keeps its own size (36px controls in the demos — a comfortable touch target). On touch devices the tooltip appears on tap, since there is no hover. Every demo is verified overflow-free at 375 / 768 / 1280px with the tooltip open and closed."""


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

## Tooltip Behavior

{spec["logic_doc"]}

## Positioning

{spec["positioning_doc"]}

## Keyboard Interaction

{keyboard}

## Accessibility

{A11Y_BASE}

{spec["a11y_doc"]}

## States

{spec["behavior_doc"]}

## Responsive Behavior

{spec["responsive_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This tooltip variant uses the semantic color, radius, shadow, typography, and motion tokens — per the Dropdown / Popover / Tooltip row of the component token rules (radius-md, shadow-sm–md, 1px subtle border, body-sm text).

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_tooltips_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_tooltips_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_tooltips"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = TOOLTIPS / slug
        folder.mkdir(parents=True, exist_ok=True)
        tsx = render_code_tsx(folder, slug, spec)
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
        print(f"OK: {len(COMPONENTS)} tooltip variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} tooltip variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
