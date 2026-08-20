#!/usr/bin/env python3
"""DevSnips React Dialogs generator.

For every dialog variant in ``React/Components/Dialogs/`` this generator:
  - reads the authored reference ``dialog/code.tsx`` (the primary, fully-typed
    implementation),
  - derives every other variant's ``code.tsx`` from it (identical shared core,
    only the header doc comment differs — registered as ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    + the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Dialogs is a multi-export compound family (`Dialog`, `DialogTrigger`,
`DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`,
`DialogFooter`, `DialogClose`), so it reuses the
tabs/breadcrumbs/pagination/dropdowns multi-export esbuild parity conversion.
The content renders through `createPortal`, so the preview transform also
maps `react-dom` imports onto the global `ReactDOM` UMD build.

Author the reference ``dialog/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_dialogs_registry.py``, then run:

    python3 _gen_react_dialogs.py            # write everything
    python3 _gen_react_dialogs.py --check    # report drift, no writes

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
DIALOGS = ROOT / "React/Components/Dialogs"
REFERENCE = "dialog"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base Icon set + the breadcrumb navigation glyphs + the menu glyphs, plus the
# dialog glyphs the showcases use (warning, info, invite, history).
import _gen_react_dropdowns as _dropdowns
_EXTRA_ICON_CASES = (
    '    case "alert-triangle": return (<svg {...common}><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
    '<path d="M12 9v4"/><path d="M12 17h.01"/></svg>);\n'
    '    case "info": return (<svg {...common}><circle cx="12" cy="12" r="10"/>'
    '<path d="M12 16v-4"/><path d="M12 8h.01"/></svg>);\n'
    '    case "user-plus": return (<svg {...common}><path d="M2 21a8 8 0 0 1 13.292-6"/>'
    '<circle cx="10" cy="8" r="5"/><path d="M19 16v6"/><path d="M22 19h-6"/></svg>);\n'
    '    case "clock": return (<svg {...common}><circle cx="12" cy="12" r="10"/>'
    '<polyline points="12 6 12 12 16 14"/></svg>);\n'
    '    case "keyboard": return (<svg {...common}><rect width="20" height="16" x="2" y="4" rx="2"/>'
    '<path d="M6 8h.01"/><path d="M10 8h.01"/><path d="M14 8h.01"/><path d="M18 8h.01"/>'
    '<path d="M6 12h.01"/><path d="M10 12h.01"/><path d="M14 12h.01"/><path d="M18 12h.01"/>'
    '<path d="M7 16h10"/></svg>);\n'
)
ICON_JS = _dropdowns.ICON_JS.replace(
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
    return (DIALOGS / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


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
    body = re.sub(
        r'(?m)^import \{([^}]+)\} from "react-dom";',
        lambda m: f"const {{ {m.group(1)} }} = ReactDOM;",
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Dialogs / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Dialogs · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "dialog",
        "family": "dialogs",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Dialogs",
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


COMPOSITION = """- `Dialog` — the root provider. Owns the open state (controlled `open` + `onOpenChange`, or uncontrolled `defaultOpen`), the `modal` behavior switch, the generated ids, and the focus-restore memory.
- `DialogTrigger` — a real `<button type="button">` with `aria-haspopup="dialog"` + `aria-expanded`. Click toggles the dialog.
- `DialogContent` — the portaled `role="dialog"` panel (`aria-modal` when modal) plus, in modal mode, the overlay that blocks the background. Rendered only while open; moves focus inside on open and traps Tab while modal.
- `DialogHeader` — the header layout slot (`DialogTitle` + `DialogDescription`).
- `DialogTitle` — an `<h2>` that registers itself so the panel is labelled by it.
- `DialogDescription` — a `<p>` that registers itself so the panel is described by it.
- `DialogFooter` — the action row; buttons go full-width stacked on small screens, right-aligned inline from `sm` up.
- `DialogClose` — a real `<button>` that closes the dialog (footer cancel actions, or the header close with `variant="ghost"`)."""

LOGIC_BASE = """The root `<Dialog>` owns the open state. Both modes are supported:

- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultOpen`; the component owns the state.

`DialogContent` renders through `createPortal` into `document.body` and only while open, so the panel never fights page stacking contexts or `overflow` clipping. Opening remembers the currently focused element (usually the trigger), moves focus to the first focusable element inside the panel (or the panel itself), registers the dialog on a module-level open stack, and — in modal mode — locks body scroll (compensating for the removed scrollbar width so the page does not shift). Closing returns focus to the remembered element, removes the stack entry, and releases the scroll lock only when no other dialog is still open, so nested dialogs never unlock the page early.

Modal dialogs close on Escape and on overlay pointer down, and trap Tab focus inside the panel. `modal={false}` renders a non-modal floating panel instead: no overlay, no scroll lock, no focus trap, and the page stays interactive — it closes on Escape or on a pointer down outside the panel.

Nesting is supported: Escape closes only the top-most open dialog (tracked by the module-level stack), and each dialog restores focus to whatever was focused when it opened — so a nested confirmation returns focus into the parent dialog, and the parent later returns focus to the page trigger. No positioning or overlay library is involved."""

KEYBOARD_BASE = """| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the dialog, focus the first focusable element inside |
| `Tab` (modal dialog) | Move to the next focusable element; wraps from the last element back to the first |
| `Shift+Tab` (modal dialog) | Move to the previous focusable element; wraps from the first element to the last |
| `Escape` | Close the top-most open dialog and restore focus to its trigger |
| `Tab` (non-modal dialog) | Moves forward naturally — the page stays reachable |

The trigger and every action are native `<button>` elements, so Enter/Space activation follows normal browser behavior. Disabled actions use the native `disabled` attribute: they are skipped by Tab and cannot be activated."""

STATES_BASE = """- **Trigger (idle)** — bordered surface button per the shared control system (36px, radius-sm, `shadow-xs`).
- **Trigger (open)** — `aria-expanded="true"`; keeps the hover surface.
- **Overlay (modal)** — `var(--ds-color-overlay)` backdrop covering the viewport; pointer down on it closes the dialog.
- **Panel** — `--ds-color-surface-elevated` with a 1px `--ds-color-border` and the `--ds-shadow-lg` elevation, radius-md, centered, capped at `100dvh - 2rem` with internal column layout, per the Dialog token rules.
- **Title / description** — heading-md (18px, 600) on foreground; body-sm on `--ds-color-muted-foreground`.
- **Footer actions** — full-width stacked below `sm`, right-aligned inline from `sm` up.
- **Disabled actions** — native `disabled`: 50% opacity, no pointer events, out of the tab order."""

A11Y_BASE = """The structure follows the WAI-ARIA dialog (modal) pattern.

- The trigger is a native `<button>` with `aria-haspopup="dialog"`, `aria-expanded`, and `aria-controls` pointing at the panel.
- The panel is `role="dialog"` with `aria-modal="true"` in modal mode. `DialogTitle` / `DialogDescription` register themselves, and the panel wires `aria-labelledby` / `aria-describedby` only when they are present — a dialog without a visible title must pass `aria-label` to `DialogContent` (the attributes are omitted, never left pointing at nothing). Confirmation-style dialogs can pass `role="alertdialog"` through `DialogContent`.
- Focus is real DOM focus: opening moves focus into the dialog, Tab is trapped while modal, and closing restores focus to the trigger — focus is never left on an unmounted element (the restore target is checked against `isConnected`).
- The background is unreachable while modal: the overlay blocks pointer interaction, the focus trap blocks keyboard access, and `aria-modal` tells assistive technology the rest of the page is inert.
- Disabled actions carry the native `disabled` attribute, which assistive technology announces as unavailable."""

RESPONSIVE_BASE = """The panel is `width: calc(100vw - 2rem)` up to `max-w-lg` (512px, inside the 400–640px dialog token range) and capped at `max-height: calc(100dvh - 2rem)`, so it stays inside the viewport at every width from 375px up — including small landscape screens — without page overflow. Long content scrolls inside a `min-h-0 flex-1 overflow-y-auto` body region while the header and footer stay pinned (see `dialog-scrollable`). Footer actions stack full-width below `sm` and lay out inline from `sm` up. The trigger keeps the shared 36px control height — a comfortable touch target — at every breakpoint."""


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

## Dialog Behavior

{spec["logic_doc"]}

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

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This dialog variant uses the semantic color, radius, shadow, typography, and motion tokens — including `color.overlay` for the backdrop and the Dialog row of the component token rules (radius-md, shadow-lg).

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_dialogs_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_dialogs_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_dialogs"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = DIALOGS / slug
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
        print(f"OK: {len(COMPONENTS)} dialog variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} dialog variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
