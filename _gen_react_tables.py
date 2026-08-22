#!/usr/bin/env python3
"""DevSnips React Tables generator.

For every table variant in ``React/Components/Tables/`` this generator:
  - reads the authored reference ``table/code.tsx`` (the primary, fully-typed
    implementation of the shared compound core),
  - derives every other variant's ``code.tsx`` from it (identical shared
    core, only the header doc comment differs — registered as ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports +
    the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture (the
    actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped in an
    IIFE exposing every compound component + helper on ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Tables is a multi-export compound family (`Table`, `TableCaption`,
`TableHeader`, `TableBody`, `TableFooter`, `TableRow`, `TableHead`,
`TableCell`, `TableEmpty`, `TableLoading`, `TableActions`, `TableToolbar`,
`TablePagination`, `TableSelection`, `TableExpand` + the typed helpers
`sortRows`, `useRowSelection`, `clampPage`, `pageRange`), so it reuses the
alerts/dialogs multi-export esbuild parity conversion.

Author the reference ``table/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_tables_registry.py``, then run:

    python3 _gen_react_tables.py            # write everything
    python3 _gen_react_tables.py --check    # report drift, no writes

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
TABLES = ROOT / "React/Components/Tables"
REFERENCE = "table"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base icon set + the breadcrumb/menu/dialog glyphs, plus the glyphs the
# table showcases use (chevron-up for sort/collapse, inbox for the empty
# state, building for group headers).
import _gen_react_dialogs as _dialogs
_EXTRA_ICON_CASES = (
    '    case "chevron-up": return (<svg {...common}><path d="m18 15-6-6-6 6"/></svg>);\n'
    '    case "inbox": return (<svg {...common}><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/>'
    '<path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>);\n'
    '    case "building": return (<svg {...common}><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/>'
    '<path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/>'
    '<path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/>'
    '<path d="M8 10h.01"/><path d="M8 14h.01"/></svg>);\n'
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
    return (TABLES / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Tables / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Tables · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "table",
        "family": "tables",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Tables",
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


# ---------------------------------------------------------------------------
# Shared README content
# ---------------------------------------------------------------------------

COMPOSITION = """The family is a compound component over real table semantics. Compose only the regions a table needs:

```tsx
<Table>
  <TableCaption />
  <TableHeader>
    <TableRow>
      <TableHead />
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell />
    </TableRow>
  </TableBody>
  <TableFooter />
</Table>
```

| Primitive | Element | Purpose |
|---|---|---|
| `<Table>` | bordered container + `<table>` | Root; provides the `density` context and the deliberate `overflow-x-auto` scroll region; `loading` sets `aria-busy`. |
| `<TableCaption>` | `<caption>` | The table's accessible name/description, rendered above the table. |
| `<TableHeader>` | `<thead>` | Column-header section (subtle surface, bottom rule). |
| `<TableBody>` | `<tbody>` | Data rows; the last row's divider is removed. |
| `<TableFooter>` | `<tfoot>` | Totals/summaries (subtle surface, top rule). |
| `<TableRow>` | `<tr>` | Hover affordance; `selected` (`aria-selected` + accent tint) and `disabled` (`aria-disabled` + reduced opacity) states. |
| `<TableHead>` | `<th scope="col">` | Column header; `sortable` renders a real sort button and manages `aria-sort`. |
| `<TableCell>` | `<td>` | Data cell; `align` + `numeric` (tabular figures); `colSpan` forwards natively. |
| `<TableEmpty>` | `<tr>` + spanning `<td>` | Honest zero-data state (title, description, optional real action). |
| `<TableLoading>` | skeleton `<tr>`s | Geometry-preserving skeleton rows (pair with `<Table loading>`). |
| `<TableActions>` | `<div>` in a cell | End-aligned cluster of real controls. |
| `<TableToolbar>` | `<div>` above the table | Selection counts, filters, primary actions (layout only). |
| `<TablePagination>` | `<nav aria-label>` | Self-contained pagination bar (status, windowed pages, Previous/Next, optional page-size select). |
| `<TableSelection>` | native `<input type="checkbox">` | Row / select-all selection with a true `.indeterminate` tri-state. |
| `<TableExpand>` | `<button>` | Row expand/collapse trigger (`aria-expanded` / `aria-controls`). |

Every region primitive throws a descriptive error when rendered outside `<Table>` (except `TableToolbar` and `TablePagination`, which live next to the table)."""

DATA_MODELING = """Tables are data-driven but unopinionated about your data shape. The conventions that keep them sound:

- **Row keys** — give every `<TableRow>` a stable, unique React `key` (an id from your data, never the array index of a sorted/filtered list).
- **Column definitions** — for data-driven tables, describe columns once (`key`, `label`, `accessor`, optional `align` / `numeric` / `format`) and map them to `<TableHead>` / `<TableCell>`; the sortable variant shows the pattern.
- **Custom cell rendering** — cells are just `<td>`s: render links, badges, avatars, progress bars, or controls inside `<TableCell>`; use `<TableActions>` for the trailing actions column.
- **Custom header rendering** — `<TableHead>` accepts any `children`; pass `sortable` + `sortDirection` + `onSort` only for columns that genuinely sort.
- **Alignment** — text columns stay `left`; numeric columns use `align="right"` + `numeric` (tabular figures) on BOTH the header and the cells so digits line up.
- **Column sizing** — the table is `w-full` with automatic layout; constrain a column with a `max-w-*` + `truncate` class on its cells (keep the full value available via `title` or an expansion panel), or size the whole table with `containerClassName`."""

SORTING_DOC = """Sorting is primitive-driven and real — there is no fake "sorted-looking" state:

1. Mark the column `<TableHead sortable sortDirection={direction} onSort={cycle}>`. The head renders a visible `<button type="button">` (click, Enter, and Space all work) and the `<th>` carries `aria-sort` — `"ascending"` / `"descending"` on the active column, `"none"` on sortable-but-inactive columns.
2. Track `{ key, direction }` in state. The recommended cycle is **ascending → descending → unsorted** (unsorted restores the original data order — a real reset, not a third sort).
3. Order the data with the typed `sortRows(rows, accessor, direction)` helper: it returns a sorted COPY (strings via `localeCompare`, numbers numerically) and immutably leaves the source array alone.

Only one column sorts at a time in this system — that keeps `aria-sort` honest (exactly one column announces a direction) and the model understandable. Multi-column sorting is deliberately out of scope (see Limitations)."""

SELECTION_DOC = """Selection uses REAL native checkboxes — never div fakes:

- Each selectable row renders `<TableSelection checked={...} onCheckedChange={...} label="Select <row name>" />` in its first cell; the header renders a `<TableSelection>` for select-all.
- The typed `useRowSelection(selectableKeys)` hook tracks the selected key set and derives `count`, `allSelected`, and `someSelected`. Pass `allSelected` to the header checkbox's `checked` and `someSelected` to its `indeterminate` — the tri-state is the true `.indeterminate` IDL property set imperatively on the DOM node (no HTML attribute exists), so it renders a dash distinct from the check mark.
- Disabled rows keep their checkbox `disabled`, are excluded from the selectable key list, and therefore never count toward select-all.
- Selected rows get `selected` on `<TableRow>`: `aria-selected="true"` plus an accent-tinted surface derived from tokens via `color-mix` — strong, and never color alone (the checkbox state carries the same information)."""

EXPANSION_DOC = """Row expansion uses a real toggle button and a real content row:

- The trigger is `<TableExpand expanded={...} controls={panelId} label="details for <row>" onClick={toggle} />` — a `<button type="button">` with `aria-expanded` and `aria-controls`, operable from the keyboard.
- The expanded content is a real `<TableRow>` whose `<TableCell colSpan={columnCount} id={panelId}>` holds the panel (a description list, text, or any composition — avoid nested tables unless the data genuinely is tabular).
- Expansion toggles instantly (no height animation), so there is no layout thrash and nothing is ever hidden from keyboard users in a half-open state; focus stays on the trigger when a row opens or closes.
- Track the open rows as a `Set` of keys — multiple rows can be open at once unless you deliberately close siblings."""

PAGINATION_DOC = """`<TablePagination>` is a self-contained pagination bar that follows the DevSnips Pagination family's semantics. It reports and changes the current page; the parent slices the dataset:

```tsx
const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));
const safePage = clampPage(page, totalPages);
const visible = rows.slice((safePage - 1) * pageSize, safePage * pageSize);

<TablePagination
  page={safePage}
  onPageChange={setPage}
  totalItems={rows.length}
  pageSize={pageSize}
  pageSizeOptions={[8, 12, 20]}
  onPageSizeChange={(size) => { setPageSize(size); setPage(1); }}
/>
```

- Changing the page changes the visible rows — there is no decorative pagination footer.
- Previous/Next disable natively at the boundaries; the current page carries `aria-current="page"`; the page list windows with non-interactive ellipses for large counts.
- Every page value is clamped with the exported `clampPage`, so an empty page cannot occur through invalid state (for example after the dataset shrinks or the page size grows — reset to page 1 on page-size change, as above).
- The "Showing X–Y of Z" status is an `aria-live="polite"` region so page changes are announced."""

LOADING_EMPTY_DOC = """**Loading.** Set `loading` on `<Table>` (adds `aria-busy="true"`) and render `<TableLoading columns={n} rows={m} />` inside `<TableBody>`. The skeleton rows keep the table's approximate geometry (same column count, near-identical row heights) to minimize layout shift; the bars are `aria-hidden` decorative placeholders with a subtle pulse that is disabled under reduced motion, and a visually hidden row announces "Loading data".

**Empty.** Render `<TableEmpty colSpan={n} title="…" description="…" action={…} />` inside `<TableBody>` when the dataset is empty. It is one real row with one spanning cell — never fake placeholder rows — and the optional action must be a real control that resolves the state (create, clear filters, retry)."""

LIMITATIONS_DOC = """- **Single-column sorting only.** `aria-sort` is only honest when exactly one column is sorted; multi-column sort is deliberately not built in.
- **No virtualized scrolling.** The table renders every row it is given; for very large datasets paginate (see `<TablePagination>`) or window the data yourself.
- **No column resizing or reordering.** Column sizing is class-based (`max-w-*` + `truncate`, `containerClassName`).
- **No ARIA grid mode.** The family intentionally keeps native table semantics; spreadsheet-style cell-to-cell arrow-key navigation would require `role="grid"` and is out of scope.
- **Sticky headers/columns are not built in.** The scroll container is `overflow-x-auto`; sticky positioning can be layered on with classes but is not part of the shipped core.
- **The responsive card presentation is a composition pattern**, not a primitive: the table-responsive variant shows how to render the same data as a card list below `sm` — your app owns that mapping."""

STYLING_DOC = """Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`); the selected-row tint derives from the accent token with `color-mix`, so no component-specific color values are invented. Define the tokens once in your theme — no component-specific CSS file is required."""

TOKENS_DOC = """See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This table follows the token system's Table rules: compact-or-default density, clear header styling (`surface-subtle` header/footer, `label-sm` header type), 1px `color.border` / `color.border-subtle` rules instead of shadows, `surface-hover` row affordance, an accent-tinted selected state, semantic status colors for badges, and the `color.focus-ring` token on every control."""


def render_readme(spec, slug) -> str:
    return f"""# {spec["title"]}

## Overview

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

## Compound components

{COMPOSITION}

{spec["composition_note"]}

## Data modeling

{DATA_MODELING}

## Sorting

{SORTING_DOC}

## Selection

{SELECTION_DOC}

## Expansion

{EXPANSION_DOC}

## Pagination

{PAGINATION_DOC}

## Behavior

{spec["logic_doc"]}

## Responsive behavior

{spec["responsive_doc"]}

## Keyboard interaction

{spec["keyboard_doc"]}

## Accessibility

{spec["a11y_doc"]}

## States

{spec["behavior_doc"]}

## Styling

{STYLING_DOC}

## Design tokens

{TOKENS_DOC}

## Loading and empty states

{LOADING_EMPTY_DOC}

## Notes

{spec["notes_doc"]}

## Limitations

{LIMITATIONS_DOC}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_tables_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_tables_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_tables"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = TABLES / slug
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
        print(f"OK: {len(COMPONENTS)} table variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} table variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
