#!/usr/bin/env python3
"""DevSnips React Navbar generator.

The Navbar family is a 15-primitive compound system (`Navbar`,
`NavbarBrand`, `NavbarContent`, `NavbarSection`, `NavbarItem`, `NavbarLink`,
`NavbarAction`, `NavbarToggle`, `NavbarMobile`, `NavbarMobileContent`,
`NavbarDropdown`, `NavbarDropdownTrigger`, `NavbarDropdownContent`,
`NavbarDropdownItem`, `NavbarDivider`). Every variant shares the SAME
implementation core — the variants are distinct navigation *patterns*
(actions, centered, dropdown, mobile, mega-menu, sticky, transparent,
sidebar, user menu) expressed through composition, documented per variant.

For every navbar variant in ``React/Components/Navbar/`` this generator:
  - reads the authored reference ``navbar/code.tsx`` (the primary,
    fully-typed implementation),
  - derives every other variant's ``code.tsx`` from it (identical shared
    core, only the header doc comment differs — registered as
    ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    preserved),
  - builds a full-width ``preview.html`` via the buttons-family preview
    architecture (the actual ``code.tsx`` inlined, auto-transformed to
    Babel JSX, wrapped in an IIFE exposing every primitive on ``window``),
  - writes ``metadata.json`` + ``README.md`` from the registry.

Author the reference ``navbar/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_navbar_registry.py``, then run:

    python3 _gen_react_navbar.py            # write everything
    python3 _gen_react_navbar.py --check    # report drift, no writes

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
NAVBAR = ROOT / "React/Components/Navbar"
REFERENCE = "navbar"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# The fullest shared Icon set (buttons base + breadcrumbs + dropdowns/menu
# glyphs). The navbar showcases additionally use no family-specific glyphs —
# the component itself ships its own chevron/menu/close/external icons.
import _gen_react_dropdowns as _dropdowns
ICON_JS = _dropdowns.ICON_JS

# Navbar previews are full-width: the preview shell's own topbar becomes
# static (so the demo navbar is the only sticky element) and the main column
# loses its max-width so sticky/transparent/mobile patterns can be evaluated
# in a realistic page context.
NAVBAR_PREVIEW_CSS = r"""  .ds-topbar{position:static;}
  .ds-main{max-width:none;padding:0 0 64px;}
  .ds-intro{max-width:980px;margin:0 auto;padding:32px 24px 24px;}
"""

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             composition_note, behavior_doc, keyboard_doc, a11y_doc,
             responsive_doc, controlled_doc, notes_doc, tsx_header,
             showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, composition_note=composition_note,
        behavior_doc=behavior_doc, keyboard_doc=keyboard_doc,
        a11y_doc=a11y_doc, responsive_doc=responsive_doc,
        controlled_doc=controlled_doc, notes_doc=notes_doc,
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


def read_reference_tsx() -> str:
    return (NAVBAR / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


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
    return reference[: m.start()] + header + "\n\n" + reference[m.end():].lstrip("\n")


def render_code_jsx(tsx: str) -> str:
    names = _export_names(tsx)
    body = _esbuild_run(tsx).replace("void 0", "undefined")
    # esbuild hoists exports to a trailing block; replace it with a clean,
    # human-readable export statement that preserves every named export.
    body = re.sub(r"\nexport \{[^}]*\};?\s*$", "\n", body)
    exports = ""
    if names:
        exports += "export { " + ", ".join(names) + " };\n"
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
{NAVBAR_PREVIEW_CSS}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Navbar / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <main class="ds-main">
    <div class="ds-intro">
      <p class="ds-eyebrow">React Component · {spec["subcategory"]}</p>
      <h1 class="ds-title">{spec["title"]}</h1>
      <p class="ds-lede">{spec["description"]}</p>
    </div>
    <div id="ds-root"></div>
  </main>
  <footer class="ds-footer">DevSnips React · Navbar · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "navbar",
        "family": "navbar",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Navbar",
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

## Installation

Copy `code.tsx` (TypeScript) or `code.jsx` (plain JavaScript) into your project — it is a single self-contained module with no dependencies beyond React. Make sure your app loads Tailwind CSS and the DevSnips `--ds-*` design tokens (see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md)); the component consumes the tokens through Tailwind arbitrary values such as `bg-[var(--ds-color-surface)]`. No component-specific CSS file is required.

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

## Compound Components

{COMPOSITION}

{spec["composition_note"]}

## Navigation Behavior

{spec["behavior_doc"]}

## Keyboard Interaction

{spec["keyboard_doc"]}

## Accessibility

{A11Y_BASE}

{spec["a11y_doc"]}

## Active Navigation

{ACTIVE_BASE}

## Responsive Behavior

{RESPONSIVE_BASE}

{spec["responsive_doc"]}

## Controlled and Uncontrolled State

{CONTROLLED_BASE}

{spec["controlled_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This navbar variant uses the semantic color, radius, shadow, typography, and motion tokens, and follows the navigation rules (48–56px top-nav height, subtle bottom border, quiet state changes).

## Notes and Limitations

{spec["notes_doc"]}
"""


COMPOSITION = """Navbar is a compound component. Fifteen primitives compose the pattern:

```tsx
<Navbar>
  <NavbarBrand href="/">Forge</NavbarBrand>
  <NavbarContent>
    <NavbarSection align="start">
      <NavbarItem><NavbarLink href="/docs" active>Docs</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarSection>
    <NavbarSection align="end">
      <NavbarItem><NavbarAction variant="ghost">Sign in</NavbarAction></NavbarItem>
      <NavbarItem><NavbarAction variant="primary" href="/signup">Get started</NavbarAction></NavbarItem>
    </NavbarSection>
  </NavbarContent>
  <NavbarToggle />
  <NavbarMobile>
    <NavbarMobileContent>
      <NavbarItem><NavbarLink href="/docs" active>Docs</NavbarLink></NavbarItem>
      <NavbarItem><NavbarLink href="/pricing">Pricing</NavbarLink></NavbarItem>
    </NavbarMobileContent>
  </NavbarMobile>
</Navbar>
```

- `Navbar` — the root `<nav>` landmark. Owns the mobile-menu state (controlled via `open` + `onOpenChange`, or uncontrolled via `defaultOpen`), the landmark label, the responsive `breakpoint`, and the `default` / `transparent` surface variant.
- `NavbarBrand` — a real `<a>` home link wrapping any ReactNode brand (logo mark, wordmark, or both).
- `NavbarContent` — the desktop content row, hidden below the breakpoint. Contains `NavbarSection` regions.
- `NavbarSection` — a `<ul>` region aligned `start`, `center`, or `end`; its children are `NavbarItem` list items.
- `NavbarItem` — a `<li>` wrapping one link, action, or dropdown.
- `NavbarLink` — a real `<a>` navigation link with `active` (`aria-current="page"`), `external` (`target="_blank"` + indicator), and `disabled` (non-interactive `aria-disabled` span — never a dead anchor).
- `NavbarAction` — a bar-height action: a real `<button>` by default, a real `<a>` when `href` is passed. `primary` / `outline` / `ghost` variants.
- `NavbarToggle` — the mobile-menu button: `aria-expanded`, `aria-controls` pointing at the mobile region, dynamic accessible name, hamburger/close icon swap.
- `NavbarMobile` — the collapsible mobile region referenced by `aria-controls`. `placement="panel"` (full-width disclosure under the bar) or `placement="side"` (compact side panel with overlay, scroll lock, and focus-on-open).
- `NavbarMobileContent` — the `<ul>` inside the mobile region; links inside it automatically switch to full-width stacked styling.
- `NavbarDropdown` — a navigation dropdown root (disclosure pattern). Owns its open state and panel placement.
- `NavbarDropdownTrigger` — a real `<button>` styled as a nav link, with `aria-haspopup="true"`, `aria-expanded`, `aria-controls`, and a rotating chevron.
- `NavbarDropdownContent` — the absolutely positioned panel, labelled by its trigger. Rendered only while open; flips its alignment to stay in the viewport.
- `NavbarDropdownItem` — one entry: a real `<a>` when `href` is passed, otherwise a real `<button>` action. Supports `active`, `external`, `disabled`, `icon`, and `onSelect`.
- `NavbarDivider` — a `role="separator"` rule between dropdown groups."""


A11Y_BASE = """The structure follows the WAI-ARIA disclosure navigation pattern.

- The root is a semantic `<nav>` landmark with an accessible name (`label`, default "Main") — pass a distinct label when more than one navbar is on the page.
- Navigation links are real `<a href>` elements (normal browser navigation, middle-click, and screen-reader link semantics); actions and toggles are real `<button>` elements. No `div` click handlers, no nested interactive elements.
- The mobile toggle is a real `<button>` with `aria-expanded` and `aria-controls` pointing at the actual mobile region; its accessible name reflects the state ("Open/Close navigation menu").
- Dropdown triggers carry `aria-haspopup="true"` + `aria-expanded` + `aria-controls`; the panel is labelled by its trigger. Navigation dropdowns intentionally do NOT use `role="menu"`/`role="menuitem"` — the panel contains real links, and the ARIA menu pattern is for action menus, not navigation.
- The mobile navigation is NOT a modal dialog: focus is never trapped. The `side` placement moves focus into the panel on open and restores it to the toggle on close, but Tab always moves forward naturally.
- Disabled links and dropdown items render as non-interactive spans with `aria-disabled="true"` — they are skipped by arrow keys, removed from the tab order, and never presented as followable links.
- External links announce themselves with `target="_blank" rel="noreferrer"`, a visible (aria-hidden) indicator glyph, and screen-reader-only "(opens in a new tab)" text.
- Every interactive element has a visible `focus-visible` ring via the `--ds-color-focus-ring` token, and all transitions are disabled under `prefers-reduced-motion`."""


ACTIVE_BASE = """Pass `active` to the `NavbarLink` or `NavbarDropdownItem` that represents the current page. Active items render with the `--ds-color-surface-active` background and foreground text (background + color, never color alone) and expose `aria-current="page"` to assistive technology. In a routed app, derive `active` from the current route:

```tsx
<NavbarLink href="/docs" active={pathname.startsWith("/docs")}>Docs</NavbarLink>
```

Exactly one item in a navigation region should be current at a time."""


RESPONSIVE_BASE = """The family collapses by breakpoint, not by JavaScript width detection: below the configured `breakpoint` (`sm` / `md` / `lg`, default `md`) `NavbarContent` is hidden with a Tailwind responsive utility and the `NavbarToggle` appears; the `NavbarMobile` region is likewise hidden at and above the breakpoint. No resize listeners are involved.

- The bar is a single 56px row (`h-14`) with `max-w-6xl` content width and fluid horizontal padding (`px-4 sm:px-6`); long link labels truncate (`min-w-0` + `truncate`) instead of forcing overflow.
- The `panel` mobile placement is absolutely positioned under the bar, so opening/closing it never shifts page layout; it caps its height at `100dvh - 4rem` and scrolls internally.
- Dropdown panels cap their width at `100vw - 1.5rem` and height at `min(24rem, 100dvh - 6rem)` with internal scrolling, and flip their horizontal alignment (start ↔ end) to stay inside the viewport.
- All controls keep comfortable touch targets: 36px (h-9) actions/toggles, 32px+ link hit areas."""


CONTROLLED_BASE = """The mobile menu supports both state modes:

- **Uncontrolled** (default) — `<Navbar>` owns the state; optionally seed it with `defaultOpen`.
- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state. Every internal request (toggle click, Escape, outside pointer, link activation) flows through `onOpenChange`.

```tsx
const [open, setOpen] = useState(false);
<Navbar open={open} onOpenChange={setOpen}>…</Navbar>
```

`NavbarDropdown` manages its own open state internally (seed with `defaultOpen`); it closes itself on selection, Escape, Tab, or outside pointer interaction, and restores focus to its trigger."""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_navbar_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_navbar_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_navbar"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = NAVBAR / slug
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
        print(f"OK: {len(COMPONENTS)} navbar variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} navbar variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
