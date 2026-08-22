#!/usr/bin/env python3
"""DevSnips React Date Picker generator.

For every date-picker variant in ``React/Components/DatePicker/`` this
generator:
  - reads the authored reference ``date-picker/code.tsx`` (the primary,
    fully-typed implementation of the compound date picker system),
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

DatePicker is a multi-export compound family (`DatePicker`,
`DatePickerInput`, `DatePickerTrigger`, `DatePickerContent`,
`DatePickerHeader`, `DatePickerCalendar`, `DatePickerFooter`,
`DatePickerPresets`, `DatePickerToday`, `DatePickerClear`,
`DatePickerApply`, `DatePickerTime`, `useDatePicker`, plus the typed date
utilities), so it reuses the calendar/tooltips multi-export esbuild parity
conversion. Every variant shares the same core implementation; variants
differ in how the showcase composes it (single/range mode, presets,
constraints, footer/apply flow, time section, mobile sheet).

Author the reference ``date-picker/code.tsx``, register metadata + showcase
+ ``tsx_header`` in ``_gen_react_datepicker_registry.py``, then run:

    python3 _gen_react_datepicker.py            # write everything
    python3 _gen_react_datepicker.py --check    # report drift, no writes

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
DATEPICKER = ROOT / "React/Components/DatePicker"
REFERENCE = "date-picker"
ESBUILD = "/tmp/dsbuild/node_modules/.bin/esbuild"

import _gen_react_buttons as _buttons
TAILWIND_CONFIG = _buttons.TAILWIND_CONFIG
TOKEN_BLOCK = _buttons.TOKEN_BLOCK
PREVIEW_CSS = _buttons.PREVIEW_CSS

# The calendar family icon set (base + breadcrumbs + dropdowns + dialogs
# glyphs, plus the calendar glyph). The date-picker showcases reuse it.
import _gen_react_calendar as _calendar
ICON_JS = _calendar.ICON_JS

COMPONENTS: dict[str, dict] = {}


def register(slug, *, title, subcategory, description, tags, features,
             accessibility, interactive, related, usage, props_doc,
             value_doc, validation_doc, keyboard_doc, a11y_doc,
             responsive_doc, notes_doc, limitations_doc, tsx_header, showcase):
    COMPONENTS[slug] = dict(
        title=title, subcategory=subcategory, description=description,
        tags=tags, features=features, accessibility=accessibility,
        interactive=interactive, related=related, usage=usage,
        props_doc=props_doc, value_doc=value_doc,
        validation_doc=validation_doc, keyboard_doc=keyboard_doc,
        a11y_doc=a11y_doc, responsive_doc=responsive_doc,
        notes_doc=notes_doc, limitations_doc=limitations_doc,
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
    return (DATEPICKER / REFERENCE / "code.tsx").read_text(encoding="utf-8").strip("\n") + "\n"


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
    <div class="ds-brand"><span class="ds-mark" aria-hidden="true">D</span><span>DevSnips</span><span class="ds-crumb" aria-hidden="true">/ <b>React</b> / DatePicker / {slug}</span></div>
    <button class="ds-theme-toggle" id="ds-theme-toggle" type="button" aria-pressed="false">
      <span id="ds-theme-label">Dark</span>
    </button>
  </header>
  <main class="ds-main">
    <p class="ds-eyebrow">React Component · {spec["subcategory"]}</p>
    <h1 class="ds-title">{spec["title"]}</h1>
    <p class="ds-lede">{html.escape(spec["description"])}</p>
    <div id="ds-root" class="ds-pos-wrap"></div>
  </main>
  <footer class="ds-footer">DevSnips React · DatePicker · <code>{slug}</code> · preview demonstration of code.tsx</footer>
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
        "component": "date-picker",
        "family": "datepicker",
        "variant": slug,
        "description": spec["description"],
        "framework": "React",
        "language": "TSX",
        "languages": ["JSX", "TSX"],
        "technology": "react",
        "type": "component",
        "category": "DatePicker",
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


INSTALLATION = """Copy `code.tsx` into your project (or `code.jsx` for plain-JavaScript builds — same API, types stripped). The only runtime dependency is React 18+; there is **no date library and no positioning library** — the component ships its own small, typed date utilities (`addDays`, `addMonths`, `compareDays`, `isSameDay`, `daysInMonth`, `isLeapYear`, `buildMonthWeeks`, `startOfMonth`, `endOfMonth`, `formatISODate`, `formatISODateTime`), which are also exported for reuse.

The component consumes DevSnips `--ds-*` design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme per [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) — no component-specific CSS file is required."""

COMPOSITION = """- `DatePicker` — the root provider. Owns the value (controlled `value` + `onChange`, or uncontrolled `defaultValue`), the open state (controlled `open` + `onOpenChange`, or uncontrolled `defaultOpen`), the visible month (uncontrolled, seeded by `defaultMonth`), the picker view, the roving focus key, the constraints (`minDate`, `maxDate`, `disabledDates`), the locale/format, and the staged draft under `requireApply`. Renders the field chrome (label / description / helper / error) when those props are set.
- `DatePickerInput` — the real text input (textually `readOnly`, so it stays keyboard-focusable and form-submittable without free-text parsing). Opens the popover on click / ArrowDown / Enter / Space. Carries `aria-haspopup="dialog"`, `aria-expanded`, `aria-controls`, `aria-required`, `aria-invalid`, `aria-describedby`.
- `DatePickerTrigger` — the real icon button toggling the popover ("Open calendar", `aria-haspopup="dialog"` + `aria-expanded`).
- `DatePickerContent` — the popover panel (`role="dialog"`, non-modal). Handles Escape, outside pointer interaction, Tab leave, and the pre-paint viewport flip. Without children it renders the default `DatePickerHeader` + `DatePickerCalendar` chrome; pass children to compose presets / footer / time sections. `mobileSheet` docks it as a bottom sheet below `sm` (pure CSS).
- `DatePickerHeader` — the navigation row: previous / heading / next. The heading button cycles the days → months → years picker views.
- `DatePickerCalendar` — one `role="grid"` month matrix per visible month (`numberOfMonths`), or the month / year picker panel in those views.
- `DatePickerFooter` — a hairline-separated action / summary region.
- `DatePickerPresets` — a real-button preset group. Clicking a preset sets the actual value (staged under `requireApply`, committed otherwise).
- `DatePickerToday` — moves to and selects today (respecting constraints).
- `DatePickerClear` — clears the value AND the staged draft immediately.
- `DatePickerApply` — commits the staged draft and closes ("Apply"; without `requireApply` it is a "Done" button that just closes). Disabled while a range is incomplete.
- `DatePickerTime` — the hour/minute section (`withTime` only). Two real labelled `<select>` controls, disabled until a date exists.

`useDatePicker()` exposes the context to composed children (for example a staged-value readout in the footer)."""

CONTROLLED_BASE = """Pass `value` (+ `onChange`) to own the value, and/or `open` (+ `onOpenChange`) to own the popover:

```tsx
const [date, setDate] = useState<Date | null>(null);
const [open, setOpen] = useState(false);

<DatePicker value={date} onChange={setDate} open={open} onOpenChange={setOpen}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>
```

A component never mixes controlled and uncontrolled halves of one state: pass `value` to control it, `defaultValue` to seed it. The range mode's `value` is always a `DateRange | null` (`{ from: Date; to: Date | null }`) — never an ambiguous string."""

UNCONTROLLED_BASE = """Pass `defaultValue` / `defaultOpen` / `defaultMonth` to seed without owning state:

```tsx
<DatePicker defaultValue={new Date(2026, 7, 15)} onChange={logChange}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>
```

Selection still reports through `onChange` — uncontrolled only changes who stores the value."""

VALUE_BASE = """The value model is a discriminated union on `mode` — TypeScript rejects a `value` shape that does not match the mode.

| Mode | `value` / `defaultValue` | `onChange` | Display |
|---|---|---|---|
| `single` (default) | `Date \\| null` | `(date: Date \\| null) => void` | One formatted date ("Aug 15, 2026"). Clicking the selected date is a no-op — never an accidental deselect; clearing is the explicit `DatePickerClear` / parent action. |
| `range` | `DateRange \\| null` (`{ from: Date; to: Date \\| null }`) | `(range: DateRange \\| null) => void` | "from – to"; while incomplete (pointer or keyboard has only picked `from`) it reads "from – …". |

Dates are **local calendar dates**, never UTC timestamps. Identity and ordering use the numeric `dayKey` (`year*10000 + (month+1)*100 + day`), arithmetic uses `new Date(y, m, d + n)` constructor normalization — deterministic across DST transitions, leap years, and month/year boundaries. `Date` objects are never mutated. The form value (`name` prop) is a `yyyy-mm-dd` string built from local parts via `formatISODate` — `toISOString()` is never used anywhere (it converts to UTC and can shift the day). Range form values serialize as `from/to` (the `to` side empty while the range is incomplete); `withTime` values serialize as `yyyy-mm-ddThh:mm`."""

VALIDATION_BASE = """Constraint and validation behavior:

- `minDate` / `maxDate` are inclusive calendar-day boundaries. They disable day cells (native `disabled` — not focusable, not activatable), the navigation buttons when the target month/year/page holds no selectable day, the month/year picker options outside the range, and keyboard movement (arrows / PageUp / PageDown skip disabled dates and never land on one).
- `disabledDates` is a matcher `(date: Date) => boolean` composing with `minDate` / `maxDate` — a date is disabled when any rule rejects it. Disabled days stay visible with reduced opacity; they are genuinely non-selectable, not merely muted. Range completion across a disabled day is rejected (the click restarts the range instead of producing a range spanning an unselectable day).
- `error` sets `aria-invalid="true"` on the input and renders the message with `role="alert"`, referenced through `aria-describedby`. Clear the error when the user resolves it (the demos clear on change).
- `required` sets `aria-required="true"` and renders a required marker (visual only, `aria-hidden`) on the root-rendered label. Native `required` form validation does not apply — the display input is `readOnly` (barred from constraint validation) and the hidden input carries the ISO value — so validate in the form's submit handler, as the `date-picker-with-error` demo does.
- Selection can never bypass constraints: every selection path (click, Enter/Space, Today, presets) goes through the same `isDisabled` guard."""

POPOVER_BASE = """The popover is a non-modal `role="dialog"` panel (no focus trap, no scroll lock):

- Opens from the input (click, `ArrowDown`, `Enter`, `Space`) or the trigger button; closing restores focus to the element that opened it.
- `Escape` closes and restores focus. Outside pointer interaction closes — when the click landed on a non-focusable surface, focus returns to the opener; when it landed on another control, focus follows the click naturally.
- `Tab` / `Shift+Tab` leave the panel from either end and close it — focus is never trapped and the natural order continues.
- In `single` mode the popover closes after selection; in `range` mode it stays open until the range completes; with `requireApply` / `withTime` it stays open until Apply/Done.
- The panel flips above the field when the space below runs out, and pins to the field's right edge when it would overflow the right viewport edge (pre-paint measurement, class-driven — no positioning library, no inline styles). `mobileSheet` docks it as a full-width bottom sheet below the `sm` breakpoint with a dimmed overlay, purely with `max-sm:` Tailwind variants — no JavaScript viewport detection."""

KEYBOARD_BASE = """| Key | Input (closed) | Day grid | Month picker | Year picker |
|---|---|---|---|---|
| `ArrowDown` / `ArrowUp` | Opens the popover | Same weekday, previous / next week | Same month ± 1 year-quarter row (± 3) | ± 3 years |
| `ArrowLeft` / `ArrowRight` | — | Previous / next day | Previous / next month | Previous / next year |
| `Enter` / `Space` | Opens the popover | Select the focused date | Choose the month | Choose the year |
| `Home` / `End` | — | First / last day of the current week row (respects `weekStartsOn`) | January / December | First / last year of the page |
| `PageUp` / `PageDown` | — | Previous / next month (day clamped, e.g. Jan 31 → Feb 28) | Previous / next year | Previous / next 12-year page |
| `Shift+PageUp` / `Shift+PageDown` | — | Previous / next year | — | — |
| `Escape` | — | Close the popover, restore focus to the opener | same | same |
| `Tab` / `Shift+Tab` | Natural order | Leaves / closes the popover — exactly one tabbable day cell (roving tabindex) | same | same |

Focus model: roving `tabIndex` — only one cell in the grid is tabbable at a time (the focused date, else the staged/selected date, else today, else the first enabled day). Arrow movement skips disabled dates automatically, and moving past a month edge pages the visible month so focus is never lost. The previous/next buttons, the heading button, footer actions, and preset buttons are ordinary tab stops with visible focus rings."""

A11Y_BASE = """The popover follows the WAI-ARIA date-picker dialog pattern (a non-modal dialog containing a date grid — NOT the menu pattern):

- The input is a real `<input type="text">` (textually read-only) with `aria-haspopup="dialog"`, `aria-expanded`, and `aria-controls` (referenced only while open). The trigger is a real `<button>`. There are no clickable divs and no nested interactive elements.
- The panel is `role="dialog"` with an accessible name ("Choose date" / "Choose date range" / "Choose date and time"), containing a `role="grid"` day matrix (`role="row"`, `role="columnheader"` weekday labels with full names in `aria-label`, `role="gridcell"` carrying `aria-selected`).
- Every day is a real `<button>` with a full locale-aware accessible name ("Friday, August 15, 2026") — never a bare number.
- Today carries `aria-current="date"` — distinguishable from the *selected* date (`aria-selected` + filled treatment), and today is never auto-selected.
- Disabled dates use native `disabled`; the month/year heading is `aria-live="polite"`. Selected / hover / today / range start / range middle / range end / range hover preview / disabled are distinguished by more than color alone (fill + weight, squared range edges, border + weight, opacity).
- Field wiring is real: root-rendered `label` uses `htmlFor` + `id`; `description` / `helperText` / `error` register their generated ids in the input's `aria-describedby`; the error uses `role="alert"`; `required` uses `aria-required`; `aria-invalid` tracks the error state. State is never communicated by color alone."""

RESPONSIVE_BASE = """A single month grid is 252px wide at the default `md` size (7 × 36px cells; 308px at `lg` 44px cells) and fits a 375px viewport. The panel's width is `max-w-[calc(100vw-1rem)]` and long localized dates wrap in the input instead of breaking the layout. With `numberOfMonths: 2` (and with presets) the popover content stacks vertically below `sm` instead of overflowing. The `mobileSheet` presentation docks the panel full-width at the bottom of the viewport below `sm`. Every variant is verified overflow-free at 375 / 768 / 1280px, open and closed."""

STYLING_BASE = """Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required."""

TOKENS_BASE = """See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. The date picker follows the Calendar / Date Picker token rules: neutral surfaces, strong typography, thin borders, restrained radius (`radius-sm` controls, `radius-md` panel), compact 36px controls (44px at `size="lg"`), a clear selected state, a 2px `focus-ring` ring, `surface-elevated` + `shadow-md` for the floating panel, `color.overlay` for the mobile sheet backdrop, and light/dark parity."""

LIMITATIONS_BASE = """- The display input is intentionally read-only: there is no free-text date parsing (locale ambiguity and invalid-date handling belong to a dedicated masked-input component). Pick from the grid, the month/year pickers, Today, or presets.
- The visible month is uncontrolled (`defaultMonth` seeds it); there is no controlled `month` prop — month navigation is internal and resets to reveal the selection on each open.
- `withTime` covers hour/minute selection in 24-hour presentation (`hourCycle: "h23"`); seconds, 12-hour dials, and timezone selection are out of scope.
- `required` is conveyed accessibly (`aria-required` + marker) but native `required` constraint validation does not apply to the read-only display input — validate in the form submit handler (see the error variant).
- Range + `withTime` is supported by the core (time applies to both endpoints) but is not a shipped variant; the presets variant demonstrates the canonical range + presets composition."""


def render_readme(spec, slug) -> str:
    keyboard = spec["keyboard_doc"] or KEYBOARD_BASE
    responsive = spec["responsive_doc"] or RESPONSIVE_BASE
    limitations = spec["limitations_doc"] or LIMITATIONS_BASE
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

## Compound Components

{COMPOSITION}

## Controlled Usage

{CONTROLLED_BASE}

## Uncontrolled Usage

{UNCONTROLLED_BASE}

## Date and Value Representation

{VALUE_BASE}

{spec["value_doc"]}

## Validation

{VALIDATION_BASE}

{spec["validation_doc"]}

## Popover Behavior

{POPOVER_BASE}

## Keyboard Interaction

{keyboard}

## Accessibility

{A11Y_BASE}

{spec["a11y_doc"]}

## Responsive Behavior

{responsive}

## Styling

{STYLING_BASE}

## Design Tokens

{TOKENS_BASE}

## Notes

{spec["notes_doc"]}

## Limitations

{limitations}
"""


def main(check=False):
    if not COMPONENTS:
        import importlib.util
        reg = ROOT / "_gen_react_datepicker_registry.py"
        spec = importlib.util.spec_from_file_location("_gen_react_datepicker_registry", reg)
        mod = importlib.util.module_from_spec(spec)
        _sys = sys
        _sys.modules["_gen_react_datepicker"] = _sys.modules[__name__]
        spec.loader.exec_module(mod)
    drift = []
    for slug, spec in COMPONENTS.items():
        folder = DATEPICKER / slug
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
        print(f"OK: {len(COMPONENTS)} date-picker variants up to date.")
    else:
        print(f"Wrote {len(COMPONENTS)} date-picker variants.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        main(check=True)
    else:
        main()
