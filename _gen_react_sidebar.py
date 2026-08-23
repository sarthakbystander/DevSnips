#!/usr/bin/env python3
"""DevSnips React Sidebar generator.

The Sidebar family is a 19-export compound application-navigation system
(`SidebarProvider`, `Sidebar`, `SidebarHeader`, `SidebarContent`,
`SidebarFooter`, `SidebarGroup`, `SidebarGroupLabel`, `SidebarMenu`,
`SidebarMenuItem`, `SidebarMenuButton`, `SidebarMenuCollapsible`,
`SidebarMenuSub`, `SidebarMenuSubItem`, `SidebarMenuSubButton`,
`SidebarTrigger`, `SidebarRail`, `SidebarSearch`, `SidebarNav`,
`useSidebar`). Every variant shares the SAME implementation core — the
variants are distinct navigation *patterns* (collapsed rail, mobile drawer,
groups, nesting, active state, badges, user area, footer actions, search,
collapsible groups, full dashboard) expressed through composition,
documented per variant.

For every sidebar variant in ``React/Components/Sidebar/`` this generator:
  - reads the authored reference ``sidebar/code.tsx`` (the primary,
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

Author the reference ``sidebar/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_sidebar_registry.py``, then run:

    python3 _gen_react_sidebar.py            # write everything
    python3 _gen_react_sidebar.py --check    # report drift, no writes

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
SIDEBAR = ROOT / "React/Components/Sidebar"
REFERENCE = "sidebar"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# The fullest shared Icon set (buttons base + breadcrumbs + dropdowns/menu
# glyphs) extended with the navigation glyphs the sidebar showcases use.
import _gen_react_dropdowns as _dropdowns
_EXTRA_ICON_CASES = r"""    case "bar-chart": return (<svg {...common}><path d="M3 3v18h18"/><path d="M8 17V9"/><path d="M13 17V5"/><path d="M18 17v-6"/></svg>);
    case "inbox": return (<svg {...common}><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>);
    case "message-square": return (<svg {...common}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>);
    case "help-circle": return (<svg {...common}><circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>);
    case "layers": return (<svg {...common}><path d="m12 2 8.5 4.5L12 11 3.5 6.5 12 2z"/><path d="m3.5 12 8.5 4.5 8.5-4.5"/><path d="m3.5 17 8.5 4.5 8.5-4.5"/></svg>);
    case "globe": return (<svg {...common}><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"/></svg>);
"""
ICON_JS = _dropdowns.ICON_JS.replace(
    "    default: return null;",
    _EXTRA_ICON_CASES + "    default: return null;",
)
assert _EXTRA_ICON_CASES.strip().splitlines()[0] in ICON_JS

# Sidebar previews are full-width app shells: the preview shell's own topbar
# becomes static and the main column loses its max-width so the persistent
# sidebar / mobile drawer patterns render in a realistic application layout.
SIDEBAR_PREVIEW_CSS = r"""  .ds-topbar{position:static;}
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
    return (SIDEBAR / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


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
{SIDEBAR_PREVIEW_CSS}
</style>
</head>
<body>
<div class="ds-page">
  <header class="ds-topbar">
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Sidebar / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Sidebar · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "sidebar",
        "family": "sidebar",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Sidebar",
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

## Navigation Data

{NAV_DATA}

## Responsive Behavior

{RESPONSIVE_BASE}

{spec["responsive_doc"]}

## Accessibility

{A11Y_BASE}

{spec["a11y_doc"]}

## Keyboard Interaction

{spec["keyboard_doc"]}

## Active Navigation

{ACTIVE_BASE}

{spec["behavior_doc"]}

## Controlled and Uncontrolled State

{CONTROLLED_BASE}

{spec["controlled_doc"]}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This sidebar variant uses the semantic color, radius, shadow, typography, and motion tokens, and follows the navigation rules (sidebar width 240–280px, clear active state, quiet state changes, mobile navigation as an accessible drawer).

## Notes and Limitations

{spec["notes_doc"]}
"""


COMPOSITION = """Sidebar is a compound component. Nineteen exports compose the pattern:

```tsx
<SidebarProvider>
  <Sidebar label="Main">
    <SidebarHeader>
      <a href="/" className="brand">Acme</a>
    </SidebarHeader>
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Platform</SidebarGroupLabel>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton href="/overview" active icon={<GridIcon />}>Overview</SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuCollapsible label="Projects" icon={<FolderIcon />}>
              <SidebarMenuSub>
                <SidebarMenuSubItem><SidebarMenuSubButton href="/projects/active">Active sprint</SidebarMenuSubButton></SidebarMenuSubItem>
              </SidebarMenuSub>
            </SidebarMenuCollapsible>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter>
      <SidebarMenuButton onClick={signOut}>Sign out</SidebarMenuButton>
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
  <main>
    <SidebarTrigger />
    …page content…
  </main>
</SidebarProvider>
```

- `SidebarProvider` — the state root (renders no DOM of its own). Owns the desktop `collapsed` state (controlled via `collapsed` + `onCollapsedChange`, or uncontrolled via `defaultCollapsed`), the mobile drawer state (`mobileOpen` + `onMobileOpenChange`, or `defaultMobileOpen`), and the responsive `breakpoint` (`sm` / `md` / `lg`, default `md`). Also owns the single `matchMedia` listener, drawer Escape handling, scroll-lock bookkeeping, and focus restoration.
- `Sidebar` — renders the navigation surface TWICE from the same children: a persistent desktop `<aside>` landmark (visible at and above the breakpoint; `w-64` expanded, `w-16` collapsed) and a mobile modal drawer (`role="dialog" aria-modal="true"`, overlay, focus trap, close button) rendered only while open below the breakpoint. Only one is exposed at a time.
- `SidebarHeader` — the 56px header region (brand, workspace switcher); centers its content in the collapsed rail.
- `SidebarContent` — the scrollable navigation region (`overflow-y-auto`).
- `SidebarFooter` — the bottom-pinned region separated by a top border (user area, settings/help/logout actions).
- `SidebarGroup` — one navigation section; `SidebarGroupLabel` — its uppercase eyebrow label (kept in the accessibility tree as sr-only when collapsed).
- `SidebarMenu` / `SidebarMenuItem` — the `<ul>` / `<li>` list structure for navigation rows.
- `SidebarMenuButton` — the primary row control: a real `<a href>` when `href` is passed, a real `<button type="button">` otherwise, and a non-interactive `aria-disabled` span when `disabled`. Supports `active` (`aria-current="page"` + surface treatment + inset indicator bar), `icon`, `badge`, and `tooltip` (collapsed-rail label).
- `SidebarMenuCollapsible` — an expandable parent row (`aria-expanded` + `aria-controls`, rotating chevron, `active` descendant indication). Controlled (`open` + `onOpenChange`) or uncontrolled (`defaultOpen`). In the collapsed rail, activating it expands the sidebar and opens the group.
- `SidebarMenuSub` / `SidebarMenuSubItem` / `SidebarMenuSubButton` — the nested level: a border-guided `<ul>` with smaller rows (13px), same active/disabled semantics as top-level rows.
- `SidebarTrigger` — the 36px mode control for page headers: opens/closes the drawer below the breakpoint, toggles collapse at/above it (`aria-expanded` + `aria-controls` reflect the active mode).
- `SidebarRail` — a thin edge hit area on the desktop sidebar border that toggles collapse (desktop only; renders nothing in the drawer).
- `SidebarSearch` — a labelled `type="search"` field with a clear button; Escape clears the query without closing the drawer. Hidden in the collapsed rail.
- `SidebarNav` — the typed data-driven renderer (see *Navigation Data*): renders sections/groups/collapsibles from `SidebarNavSection[]`, auto-expands parents with an active descendant, and filters by `query` with a status-message empty state.
- `useSidebar()` — the context escape hatch for custom content (e.g. adapting a brand wordmark or user card to the collapsed state)."""


NAV_DATA = """`SidebarNav` renders navigation from typed data instead of hand composition:

```tsx
export interface SidebarNavItem {
  id: string;                  // stable id (expansion bookkeeping)
  label: string;               // visible + accessible label
  href?: string;               // navigation target
  icon?: ReactNode;            // leading icon (aria-hidden)
  badge?: ReactNode;           // trailing count/status badge
  disabled?: boolean;          // non-interactive aria-disabled row
  active?: boolean;            // current page (aria-current="page")
  children?: SidebarNavItem[]; // nested level (up to three levels render)
}

export interface SidebarNavSection {
  id: string;
  label?: string;              // group eyebrow label
  items: SidebarNavItem[];
}

<SidebarContent>
  <SidebarNav sections={SECTIONS} query={query} emptyMessage="Nothing found" />
</SidebarContent>
```

Rendering rules:

- Items with `children` render as `SidebarMenuCollapsible` parents; leaf items render as `SidebarMenuButton` links/actions. Nested children render as `SidebarMenuSubButton` rows (three levels of indentation maximum — deeper trees belong in a different navigation pattern).
- A parent with an active descendant opens automatically and shows the parent-indication treatment; manual toggles are remembered per session (`overrides` map keyed by item `id`).
- `query` filters case-insensitively by label. A matching child keeps its parent chain visible (and expanded); a matching parent keeps its whole subtree. When nothing matches, a `role="status"` empty message renders instead of the tree.

The data model is framework-neutral: `href` values are plain URLs. In a routed app, derive `active` from the current route when building the sections."""


A11Y_BASE = """The structure follows the WAI-ARIA disclosure navigation pattern, plus the modal-dialog pattern for the mobile drawer.

- The desktop sidebar is a real `<aside>` containing a `<nav aria-label>` landmark; the mobile drawer is `role="dialog" aria-modal="true"` with the same labelled `<nav>` inside. Only one is exposed at a time (the desktop landmark is `display: none` below the breakpoint; the drawer is only mounted while open).
- Navigation rows are real `<a href>` elements (normal browser navigation, middle-click, screen-reader link semantics); toggles and actions are real `<button type="button">` elements. No `div` click handlers, no nested interactive elements.
- Disabled rows render as non-interactive spans with `aria-disabled="true"` — never dead anchors or focusable-but-inert controls.
- Collapsed-rail rows keep their full label in the accessibility tree (sr-only text) and expose a measured, fixed-position tooltip on hover/focus — the tooltip never takes pointer events and is hidden from assistive technology because the sr-only label already names the control.
- The mobile drawer moves focus to its first navigation control on open, traps Tab/Shift+Tab at its boundaries, closes on Escape and outside pointer down, locks body scroll with scrollbar-width compensation, and returns focus to the `SidebarTrigger` on close. A built-in close button ("Close navigation") is the last tab stop.
- Group labels remain available to screen readers when the rail is collapsed (sr-only), and collapsible parents expose `aria-expanded` + `aria-controls` pointing at the nested list.
- Every interactive element has a visible `focus-visible` ring via the `--ds-color-focus-ring` token, and all transitions are disabled under `prefers-reduced-motion`."""


ACTIVE_BASE = """Pass `active` to the `SidebarMenuButton` / `SidebarMenuSubButton` that represents the current page (or set `active: true` in the `SidebarNavItem` data). The current item renders with the active surface, foreground text, medium weight, AND a 2px inset indicator bar — never color alone — and exposes `aria-current="page"` to assistive technology. In a routed app, derive `active` from the current route:

```tsx
<SidebarMenuButton href="/analytics" active={pathname.startsWith("/analytics")}>Analytics</SidebarMenuButton>
```

Exactly one item in the navigation should be current at a time. A collapsible parent with an active descendant receives the parent-indication treatment (medium-weight foreground text, no surface fill) via its own `active` prop — `aria-current` stays on the actual page link."""


RESPONSIVE_BASE = """The family switches modes by breakpoint, driven by one `matchMedia` listener in the provider plus Tailwind responsive utilities — no resize handlers per component:

- **At and above the breakpoint** (`md` = 768px by default): the persistent `<aside>` renders as a 256px navigation column; `SidebarTrigger` / `SidebarRail` toggle it to a 64px icon rail (labels become sr-only, badges become dots, rows expose measured tooltips, `SidebarSearch` hides, group labels stay in the accessibility tree).
- **Below the breakpoint**: the desktop landmark is `display: none` and the sidebar becomes a modal drawer (`w-72`, capped at `100vw - 3rem`) with an overlay, scroll lock, focus trap, Escape / outside-pointer close, and focus restoration. A resize to desktop while the drawer is open closes it cleanly.
- Activating any navigation link inside the drawer closes it (navigation proceeds).
- Long labels truncate with `min-w-0` + `truncate` instead of forcing overflow; the rail keeps a fixed 64px width so it never overflows the layout."""


CONTROLLED_BASE = """Both state slices support controlled and uncontrolled usage:

- **Collapsed (desktop)** — uncontrolled via `defaultCollapsed`, or controlled via `collapsed` + `onCollapsedChange`. Every internal toggle point (`SidebarTrigger`, `SidebarRail`, a collapsed `SidebarMenuCollapsible` activation) flows through `onCollapsedChange`.
- **Mobile drawer** — uncontrolled via `defaultMobileOpen`, or controlled via `mobileOpen` + `onMobileOpenChange`. Trigger clicks, Escape, overlay pointer downs, drawer close-button clicks, and in-drawer navigation all flow through `onMobileOpenChange`.

```tsx
const [collapsed, setCollapsed] = useState(false);
const [mobileOpen, setMobileOpen] = useState(false);
<SidebarProvider collapsed={collapsed} onCollapsedChange={setCollapsed}
                 mobileOpen={mobileOpen} onMobileOpenChange={setMobileOpen}>
  …
</SidebarProvider>
```

`SidebarMenuCollapsible` manages its own expansion (uncontrolled `defaultOpen` or controlled `open` + `onOpenChange`); `SidebarNav` keeps a per-item override map on top of the active-descendant default. The collapsed state is intentionally NOT persisted — persistence belongs to the application shell (store the controlled value in `localStorage` or a cookie if you need it)."""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_sidebar_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_sidebar_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_sidebar"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = SIDEBAR / slug
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
        print(f"OK: {len(COMPONENTS)} sidebar variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} sidebar variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
