#!/usr/bin/env python3
"""DevSnips React Calendar generator.

For every calendar variant in ``React/Components/Calendar/`` this generator:
  - reads the authored reference ``calendar/code.tsx`` (the primary,
    fully-typed implementation of the compound calendar system),
  - derives every other variant's ``code.tsx`` from it (identical shared
    core, only the header doc comment differs — registered as
    ``tsx_header``),
  - derives ``code.jsx`` via esbuild (TS types stripped, ALL named exports
    + the default export preserved),
  - builds ``preview.html`` via the buttons-family preview architecture
    (the actual ``code.tsx`` inlined, auto-transformed to Babel JSX, wrapped
    in an IIFE exposing every compound component + the date utilities on
    ``window``),
  - writes ``metadata.json`` + ``README.md`` from a lightweight registry.

Calendar is a multi-export compound family (`Calendar`, `CalendarHeader`,
`CalendarPrevious`, `CalendarNext`, `CalendarHeading`, `CalendarGrid`,
`CalendarFooter`, `useCalendar`, plus the typed date utilities), so it
reuses the tooltips/dialogs multi-export esbuild parity conversion. Every
variant shares the same core implementation; variants differ in how the
showcase composes it (selection mode, constraints, views, week numbers,
outside days, controlled state).

Author the reference ``calendar/code.tsx``, register metadata + showcase +
``tsx_header`` in ``_gen_react_calendar_registry.py``, then run:

    python3 _gen_react_calendar.py            # write everything
    python3 _gen_react_calendar.py --check    # report drift, no writes

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
CALENDAR = ROOT / "React/Components/Calendar"
REFERENCE = "calendar"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# Base Icon set + the breadcrumb/menu/dialog glyphs, plus a calendar glyph
# the showcases use.
import _gen_react_dialogs as _dialogs
_EXTRA_ICON_CASES = (
    '    case "calendar": return (<svg {...common}><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>'
    '<line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/>'
    '<line x1="3" x2="21" y1="10" y2="10"/></svg>);\n'
)
ICON_JS = _dialogs.ICON_JS.replace(
    "    default: return null;",
    _EXTRA_ICON_CASES + "    default: return null;",
)
assert _EXTRA_ICON_CASES.strip().splitlines()[0] in ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             selection_doc, keyboard_doc, a11y_doc, responsive_doc,
             notes_doc, tsx_header, showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, selection_doc=selection_doc,
        keyboard_doc=keyboard_doc, a11y_doc=a11y_doc,
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
    return (CALENDAR / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


def render_code_tsx(slug: str, spec: dict) -> str:
    """The reference variant keeps its authored code.tsx; every other variant
    is derived: reference core with the header doc comment swapped for the
    variant's registered ``tsx_header``."""
    reference = read_reference_tsx()
    if slug == REFERENCE:
        return reference
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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / Calendar / {slug}</span></div>
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
  <footer class="ds-footer">DevSnips React · Calendar · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "calendar",
        "family": "calendar",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "Calendar",
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


INSTALLATION = """Copy `code.tsx` into your project (or `code.jsx` for plain-JavaScript builds — same API, types stripped). The only runtime dependency is React 18+; there is **no date library** — the component ships its own small, typed date utilities (`addDays`, `addMonths`, `compareDays`, `isSameDay`, `daysInMonth`, `isLeapYear`, `isoWeekNumber`, `buildMonthWeeks`, `startOfMonth`, `endOfMonth`), which are also exported for reuse.

The component consumes DevSnips `--ds-*` design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme per [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) — no component-specific CSS file is required."""

COMPOSITION = """- `Calendar` — the root provider. Owns the selection state (per `mode`), the visible month (controlled `month` + `onMonthChange`, or uncontrolled `defaultMonth`), the picker view (`days` / `months` / `years`, seeded by `defaultView`), the roving focus key, and the constraints (`minDate`, `maxDate`, `disabled`). Renders the bordered panel.
- `CalendarHeader` — the navigation row. Compose `CalendarPrevious` + `CalendarHeading` + `CalendarNext` inside it.
- `CalendarPrevious` / `CalendarNext` — real buttons with view-aware accessible names ("Go to previous month" / "year" / "12 years"). They disable themselves when `minDate` / `maxDate` make that direction impossible.
- `CalendarHeading` — an `aria-live="polite"` `<h2>` announcing the visible month/year. In the days and months views the label is a button that switches to the month / year picker.
- `CalendarGrid` — one month matrix (`role="grid"`). Render `<CalendarGrid monthOffset={i} />` once per visible month when using `numberOfMonths`. In the `months` / `years` views the first grid renders the picker panel and the others render nothing.
- `CalendarFooter` — an optional summary / action region separated by a hairline.

`useCalendar()` exposes the context to composed children (for example a footer "Today" action that calls `goToMonth` + `selectDate`)."""

SELECTION_MODES_BASE = """The selection API is a discriminated union on `mode` — TypeScript rejects a `selected` shape that does not match the mode.

| Mode | `selected` | `onSelect` | Behavior |
|---|---|---|---|
| `single` (default) | `Date \\| null` | `(date: Date \\| null) => void` | One date. Clicking the selected date is a no-op — there is no accidental deselection. |
| `multiple` | `Date[]` | `(dates: Date[]) => void` | Click toggles a date in/out of the set. Updates are immutable — caller arrays are never mutated. |
| `range` | `DateRange \\| null` (`{ from: Date; to: Date \\| null }`) | `(range: DateRange \\| null) => void` | First click starts (`to: null`); second click completes. See the range rules below. |

Range rules (predictable by design):

1. Clicking any date with a complete range (or none) starts a new range at that date.
2. Clicking the pending `from` date completes a **same-day range** (`from === to`).
3. Clicking a date **earlier** than `from` restarts the range at that date (no silent swap).
4. A completion that would **cross a disabled date** is rejected — the click restarts the range at the clicked date instead of producing a range that spans an unselectable day.

Every mode works controlled (`selected` + `onSelect`) or uncontrolled (`defaultSelected`). A component never mixes the two: pass `selected` to control it, `defaultSelected` to seed it."""

DATE_MODEL_BASE = """Calendar dates are **local calendar dates**, never UTC timestamps.

- All arithmetic uses `new Date(year, month, day)` constructor normalization (`addDays`, `addMonths`) — never timestamp math (`getTime() + 86400000`), which shifts a day across DST transitions, and never string comparison.
- Day identity and ordering use a numeric key (`year * 10000 + (month+1) * 100 + day`), which is strictly monotonic with calendar order.
- `toISOString()` is never used (it converts to UTC and would shift the calendar day for most timezones).
- A selected date's *calendar* meaning is preserved: March 10 stays March 10 in the user's local calendar. The returned `Date` objects are local dates; compare them with `isSameDay` / `compareDays`, not `getTime()`.
- `minDate` / `maxDate` / `disabled(date)` are compared by calendar day — the time-of-day on the `Date` objects you pass is ignored.
- Week numbers follow ISO 8601 (weeks start Monday; week 1 contains the year's first Thursday), computed on local-noon copies so the Thursday shift is immune to midnight DST transitions."""

CONSTRAINTS_BASE = """`minDate` and `maxDate` are inclusive calendar-day boundaries. They disable:

- day cells outside the range (native `disabled` — not focusable, not activatable, announced as unavailable),
- the previous/next navigation buttons when the target month / year / 12-year page would hold no selectable day,
- month and year picker options that fall entirely outside the range,
- keyboard navigation — arrow/PageUp/PageDown movement skips disabled dates and never lands on one,
- range completion across the boundary (the range restarts instead of crossing).

Selection can never bypass constraints: every selection path (click, Enter/Space, footer actions) goes through the same `isDisabled` guard. The `disabled` matcher composes with `minDate` / `maxDate` (a date is disabled if any rule rejects it)."""

KEYBOARD_BASE = """| Key | Day grid | Month picker | Year picker |
|---|---|---|---|
| `ArrowLeft` / `ArrowRight` | Previous / next day | Previous / next month | Previous / next year |
| `ArrowUp` / `ArrowDown` | Same weekday, previous / next week | Same month ± 1 year-quarter row (± 3) | ± 3 years |
| `Home` / `End` | First / last day of the current week row (respects `weekStartsOn`) | January / December | First / last year of the page |
| `PageUp` / `PageDown` | Previous / next month (day clamped, e.g. Jan 31 → Feb 28) | Previous / next year | Previous / next 12-year page |
| `Shift+PageUp` / `Shift+PageDown` | Previous / next year | — | — |
| `Enter` / `Space` | Select the focused date (native button activation) | Choose the month | Choose the year |
| `Tab` / `Shift+Tab` | Moves into / out of the calendar — exactly one tabbable cell (roving tabindex) | same | same |

Focus model: roving `tabIndex` — only one cell in the calendar is tabbable at a time (the focused date, else the selected date, else today, else the first enabled day). Arrow movement skips disabled dates automatically, and moving past a month edge pages the visible month so focus is never lost. There are no keyboard traps: Tab always leaves the calendar. The previous/next buttons and the heading button are ordinary tab stops with visible focus rings."""

A11Y_BASE = """The day matrix follows the WAI-ARIA date-picker grid pattern:

- `role="grid"` per month (labelled with the month + year), `role="row"` per week, `role="columnheader"` for weekday labels (short text visible, full name in `aria-label`), `role="rowheader"` for ISO week numbers, `role="gridcell"` per day carrying `aria-selected`.
- Every day is a real `<button>` with a full locale-aware accessible name ("Friday, August 22, 2026") — never a bare number, never a clickable div.
- Today carries `aria-current="date"` — it is distinguishable from the *selected* date (which uses `aria-selected` + a filled treatment), and today is never auto-selected.
- Disabled dates use native `disabled` (exposed as unavailable, skipped by keyboard) and stay visible with reduced opacity — never hidden, never color-only.
- The month/year heading is `aria-live="polite"`, so navigation is announced.
- The previous/next buttons have view-aware accessible names; the heading button's `aria-label` explains that it opens the month/year picker.
- Selected vs. hover vs. today vs. disabled are distinguished by more than color alone (fill + weight, border + weight, opacity)."""

STATES_BASE = """- **Default** — foreground text on the surface; hover shifts to `surface-hover`.
- **Selected** — solid `primary` fill with `primary-foreground` text and medium weight (fill + weight, not color alone). Hover darkens via `color-mix`.
- **Range start / end** — the same primary fill, squared toward the range interior; the **range middle** is a continuous `surface-active` band (squared corners).
- **Today** — a `border-strong` outline + semibold text; combined with the fill when today is also selected.
- **Focused** — the roving cell; keyboard focus shows a 2px `focus-ring` outline (`:focus-visible`).
- **Disabled** — native `disabled` + 40% opacity + `cursor-not-allowed`; skipped by pointer and keyboard.
- **Outside days** — muted-foreground text (with `showOutsideDays`); selecting one pages to its month.

All state transitions are 150ms `ease-out` color transitions and collapse to nothing under `prefers-reduced-motion`."""

RESPONSIVE_BASE = """A single month grid is 252px wide (7 × 36px cells; 288px with week numbers) and fits a 375px viewport without scaling. Day cells are 36×36px — the family's default control size. With `numberOfMonths > 1`, wrap the grids in a `flex-col sm:flex-row` container (see `calendar-range`) so the months stack on narrow screens instead of overflowing. The month/year pickers use the same width and a 3-column layout. Every variant is verified overflow-free at 375 / 768 / 1280px."""


def render_readme(spec, slug) -> str:
    keyboard = spec["keyboard_doc"] or KEYBOARD_BASE
    responsive = spec["responsive_doc"] or RESPONSIVE_BASE
    return f"""# {spec["title"]}

{spec["description"]}

## Installation

{INSTALLATION}

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

## Selection Modes

{SELECTION_MODES_BASE}

{spec["selection_doc"]}

## Date Model and Timezones

{DATE_MODEL_BASE}

## Date Constraints

{CONSTRAINTS_BASE}

## Keyboard Interaction

{keyboard}

## Accessibility

{A11Y_BASE}

{spec["a11y_doc"]}

## States

{STATES_BASE}

## Responsive Behavior

{responsive}

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. The calendar follows the Calendar / Date Picker token rules: neutral surfaces, strong typography, thin borders, restrained radius (`radius-sm` cells, `radius-md` panel), compact 36px controls, a clear selected state, and light/dark parity.

## Notes

{spec["notes_doc"]}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_calendar_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_calendar_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_calendar"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = CALENDAR / slug
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
        print(f"OK: {len(COMPONENTS)} calendar variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} calendar variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
