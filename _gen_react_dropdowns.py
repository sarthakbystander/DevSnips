#!/usr/bin/env python3
"""DevSnips React Dropdowns generator.

For every dropdown-menu variant in ``React/Components/Dropdowns/`` this
generator:
  - reads the authored ``code.tsx`` (the primary, fully-typed implementation),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    + the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing every compound component on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Dropdowns is a multi-export compound family (`DropdownMenu`,
`DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuItem`,
`DropdownMenuLabel`, `DropdownMenuGroup`, `DropdownMenuSeparator`, plus
`DropdownMenuCheckboxItem` on the checkboxes variant,
`DropdownMenuRadioGroup` + `DropdownMenuRadioItem` on the radio variant, and
`DropdownMenuSub` + `DropdownMenuSubTrigger` + `DropdownMenuSubContent` on the
submenu variant), so it reuses the tabs/breadcrumbs/pagination multi-export
esbuild parity conversion.

Author ``code.tsx`` per variant, register metadata in
``_gen_react_dropdowns_registry.py``, then run:

    python3 _gen_react_dropdowns.py            # write everything
    python3 _gen_react_dropdowns.py --check    # report drift, no writes

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
DROPDOWNS = ROOT / "React/Components/Dropdowns"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base Icon set + the breadcrumb navigation glyphs, plus the menu glyphs the
# dropdown showcases use (members, email, links, theme, sign out, files).
import _gen_react_breadcrumbs as _breadcrumbs
_EXTRA_ICON_CASES = (
    '    case "users": return (<svg {...common}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
    '<circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>);\n'
    '    case "mail": return (<svg {...common}><rect width="20" height="16" x="2" y="4" rx="2"/>'
    '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>);\n'
    '    case "link": return (<svg {...common}><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>'
    '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>);\n'
    '    case "monitor": return (<svg {...common}><rect width="20" height="14" x="2" y="3" rx="2"/>'
    '<path d="M8 21h8"/><path d="M12 17v4"/></svg>);\n'
    '    case "sun": return (<svg {...common}><circle cx="12" cy="12" r="4"/>'
    '<path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/>'
    '<path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>);\n'
    '    case "moon": return (<svg {...common}><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>);\n'
    '    case "logout": return (<svg {...common}><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>'
    '<path d="m16 17 5-5-5-5"/><path d="M21 12H9"/></svg>);\n'
    '    case "file": return (<svg {...common}><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
    '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>);\n'
    '    case "eye": return (<svg {...common}><path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/>'
    '<circle cx="12" cy="12" r="3"/></svg>);\n'
)
ICON_JS = _breadcrumbs.ICON_JS.replace(
    "    default: return null;",
    _EXTRA_ICON_CASES + "    default: return null;",
)
assert _EXTRA_ICON_CASES.strip().splitlines()[0] in ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             composition_note, logic_doc, keyboard_doc, behavior_doc,
             a11y_doc, responsive_doc, notes_doc, showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, composition_note=composition_note,
        logic_doc=logic_doc, keyboard_doc=keyboard_doc,
        behavior_doc=behavior_doc, a11y_doc=a11y_doc,
        responsive_doc=responsive_doc, notes_doc=notes_doc, showcase=showcase,
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Dropdowns / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Dropdowns · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "dropdown-menu",
        "family": "dropdowns",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Dropdowns",
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


COMPOSITION = """Dropdown Menu is a compound component. Seven primitives compose the pattern:

```tsx
<DropdownMenu>
  <DropdownMenuTrigger>Actions</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>Project</DropdownMenuLabel>
    <DropdownMenuGroup>
      <DropdownMenuItem>Edit</DropdownMenuItem>
      <DropdownMenuItem>Duplicate</DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuSeparator />
    <DropdownMenuItem destructive>Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

- `DropdownMenu` — the root. Owns the open state (controlled via `open` + `onOpenChange`, or uncontrolled via `defaultOpen`), the trigger/content id wiring, the placement preference, and outside-pointer closing. Renders a `relative inline-flex` wrapper the menu panel anchors to.
- `DropdownMenuTrigger` — a real `<button type="button">` with `aria-haspopup="menu"` + `aria-expanded`. Click toggles; ArrowDown opens with the first item focused, ArrowUp with the last. The trailing chevron rotates while open.
- `DropdownMenuContent` — the `role="menu"` panel, labelled by the trigger. Rendered only while open; measures itself before paint and flips placement to stay in the viewport.
- `DropdownMenuItem` — one action: a real `<button>` with `role="menuitem"`. Optional `icon`, `shortcut`, `destructive`, `disabled`, `closeOnSelect`, and `onSelect` props.
- `DropdownMenuLabel` — a non-interactive section heading (uppercase, tracked, smaller type).
- `DropdownMenuGroup` — a `role="group"` wrapper; associate it with its label via `aria-labelledby`.
- `DropdownMenuSeparator` — a `role="separator"` horizontal rule between groups."""

LOGIC_BASE = """The root `<DropdownMenu>` owns the open state. Both modes are supported:

- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultOpen`; the component owns the state.

Opening moves focus into the menu: the first item, or the last item when the trigger was invoked with ArrowUp. Activating an item runs its `onSelect` and then closes the menu (set `closeOnSelect={false}` or call `event.preventDefault()` in `onSelect` to keep it open). Closing — via selection, Escape, the trigger, or a pointer down outside — returns focus to the trigger, except on Tab, where focus is allowed to move forward naturally.

The panel opens relative to its trigger at the requested `placement` (`bottom-start` by default) and measures itself in a layout effect before paint: if the preferred side would leave the viewport, it flips to the other side (bottom ↔ top, start ↔ end). The panel also caps its own height (`min(20rem, 100vh - 2rem)` with internal scrolling) and width (`100vw - 1.5rem`), so menus never routinely overflow the viewport. No positioning library is involved."""

KEYBOARD_BASE = """| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the menu, focus the first item |
| `ArrowDown` (trigger) | Open the menu, focus the first item |
| `ArrowUp` (trigger) | Open the menu, focus the last item |
| `ArrowDown` / `ArrowUp` (menu) | Move focus to the next / previous enabled item, wrapping at the ends |
| `Home` / `End` (menu) | Focus the first / last enabled item |
| `Enter` / `Space` (menu) | Activate the focused item (native button behavior) |
| `Escape` | Close the menu and return focus to the trigger |
| `Tab` | Close the menu and move focus forward naturally |

The trigger and items are native `<button>` elements, so Enter/Space activation follows normal browser behavior. Disabled items use the native `disabled` attribute: they are skipped by arrow-key navigation, removed from the tab order, and cannot be activated."""

STATES_BASE = """- **Trigger (idle)** — bordered surface button with a muted chevron; hover shifts to a subtle surface.
- **Trigger (open)** — `aria-expanded="true"`; keeps the hover surface and rotates the chevron 180°.
- **Item (idle)** — foreground text on the elevated menu surface.
- **Item (hover / focus)** — `--ds-color-surface-hover` background; keyboard focus additionally shows the `--ds-color-focus-ring` outline inside the item bounds.
- **Item (disabled)** — native `disabled`: 50% opacity, no pointer events, skipped by arrow keys, out of the tab order.
- **Panel** — `--ds-color-surface-elevated` with a 1px `--ds-color-border` and the restrained `--ds-shadow-md`, per the Dropdown/Popover token rules (radius-md, subtle border, body-sm type)."""

A11Y_BASE = """The structure follows the WAI-ARIA menu button pattern.

- The trigger is a native `<button>` with `aria-haspopup="menu"`, `aria-expanded`, and `aria-controls` pointing at the open panel.
- The panel is `role="menu"` labelled by its trigger (`aria-labelledby`); items are `role="menuitem"` on real `<button>` elements — no `div` click handlers.
- Focus is real DOM focus: opening moves focus into the menu, closing returns it to the trigger, and focus is never left on an unmounted element.
- Disabled items carry the native `disabled` attribute, which assistive technology announces as unavailable.
- `DropdownMenuSeparator` uses `role="separator"`; icons are `aria-hidden` decoration and shortcuts are exposed via `aria-keyshortcuts`, so accessible names stay clean."""

RESPONSIVE_BASE = """The menu panel caps its width at `100vw - 1.5rem` and its height at `min(20rem, 100vh - 2rem)` with internal scrolling, so it stays inside the viewport at every width from 375px up without shrinking the trigger. Placement flips (bottom ↔ top, start ↔ end) keep the panel attached to its trigger near viewport edges. Long item labels truncate within the panel rather than forcing horizontal page overflow; the trigger label truncates within its own `max-w-full` bounds. The trigger keeps the shared 36px (h-9) control height — a comfortable touch target — at every breakpoint."""


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

## Menu Behavior

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

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This dropdown-menu variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_dropdowns_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_dropdowns_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_dropdowns"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = DROPDOWNS / slug
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
        print(f"OK: {len(COMPONENTS)} dropdown variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} dropdown variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
