# Calendar — Month Picker

The month-selection view: a 12-month grid opened from the heading (or seeded with defaultView), with year paging, min/max-aware options, and full keyboard navigation — choosing a month lands in its day grid.

## Installation

Copy `code.tsx` into your project (or `code.jsx` for plain-JavaScript builds — same API, types stripped). The only runtime dependency is React 18+; there is **no date library** — the component ships its own small, typed date utilities (`addDays`, `addMonths`, `compareDays`, `isSameDay`, `daysInMonth`, `isLeapYear`, `isoWeekNumber`, `buildMonthWeeks`, `startOfMonth`, `endOfMonth`), which are also exported for reuse.

The component consumes DevSnips `--ds-*` design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme per [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) — no component-specific CSS file is required.

## Usage

```tsx
// Open directly in the months view:
<Calendar defaultView="months" defaultMonth={new Date(2026, 7, 1)} onMonthChange={setMonth}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>

// …or from any calendar: activate the heading ("August 2026 — activate to
// choose a month") to switch the grid to the month picker.
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
// Open directly in the months view:
<Calendar defaultView="months" defaultMonth={new Date(2026, 7, 1)} onMonthChange={setMonth}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>

// …or from any calendar: activate the heading ("August 2026 — activate to
// choose a month") to switch the grid to the month picker.
```

## Props

### `<Calendar>`

| Name | Type | Default | Description |
|---|---|---|---|
| `mode` | `"single" \| "multiple" \| "range"` | `"single"` | Selection mode. Determines the shape of `selected` / `defaultSelected` / `onSelect` (discriminated union). |
| `selected` | `Date \| null` · `Date[]` · `DateRange \| null` | — | Selection (controlled). Shape follows `mode`. |
| `defaultSelected` | same as `selected` | `null` / `[]` | Initial selection (uncontrolled). |
| `onSelect` | `(date) => void` · `(dates) => void` · `(range) => void` | — | Called on every selection change, including in-progress range steps (`{ from, to: null }`). |
| `month` | `Date` | — | Visible month (controlled); any day inside it, normalized to the 1st. |
| `defaultMonth` | `Date` | selection month, else today | Initial visible month (uncontrolled). |
| `onMonthChange` | `(month: Date) => void` | — | Called whenever the visible month changes (navigation, keyboard paging, outside-day click, picker selection). |
| `defaultView` | `"days" \| "months" \| "years"` | `"days"` | Initial picker view. The heading button cycles days → months → years regardless. |
| `minDate` | `Date` | — | Earliest selectable calendar day (inclusive). |
| `maxDate` | `Date` | — | Latest selectable calendar day (inclusive). |
| `disabled` | `(date: Date) => boolean` | — | Matcher for individual disabled dates; composes with `minDate` / `maxDate`. |
| `locale` | `string` | `"en-US"` | BCP-47 tag for month, weekday, and day accessible names (via `Intl.DateTimeFormat`). |
| `weekStartsOn` | `0 \| 1 \| 2 \| 3 \| 4 \| 5 \| 6` | `0` | First weekday column (0 = Sunday, 1 = Monday, …). Headers and rows stay consistent. |
| `showOutsideDays` | `boolean` | `false` | Render adjacent-month days at the layout's outer edges. |
| `showWeekNumbers` | `boolean` | `false` | Render the non-interactive ISO-8601 week-number column. |
| `numberOfMonths` | `number` | `1` | Consecutive months shown; render one `<CalendarGrid monthOffset={i}>` per month. |
| `className` | `string` | — | Extra classes on the panel. |
| `children` | `ReactNode` | — | The composed parts (header, grid(s), footer). |

### Parts

| Part | Props | Renders |
|---|---|---|
| `CalendarHeader` | `className`, native div attrs | The navigation row. |
| `CalendarPrevious` / `CalendarNext` | `className`, native button attrs | View-aware nav buttons (month / year / 12-year page). Auto-disabled at `minDate` / `maxDate`. |
| `CalendarHeading` | `className`, native heading attrs | `aria-live` month/year label; a button that opens the month / year picker. |
| `CalendarGrid` | `monthOffset` (0-based), `className`, native div attrs | One `role="grid"` month matrix — or the picker panel in the months/years views (`monthOffset={0}` only). |
| `CalendarFooter` | `className`, native div attrs | A hairline-separated summary / action region. |

`useCalendar()` returns the root context for composed children (footer actions, custom cells) — selection helpers (`selectDate`, `clearSelection`), navigation (`goToMonth`, `goToPrevious`, `goToNext`), and state (`month`, `view`, `isDisabled`, …).

### Date utilities

`daysInMonth(year, month)`, `isLeapYear(year)`, `addDays(date, n)`, `addMonths(date, n)` (day clamped to the target month), `startOfMonth(date)`, `endOfMonth(date)`, `compareDays(a, b)`, `isSameDay(a, b)`, `isoWeekNumber(date)`, `buildMonthWeeks(month, weekStartsOn)` — small, typed, local-calendar-date helpers used internally and exported for reuse (they are the foundation of the DatePicker family).

## Composition

- `Calendar` — the root provider. Owns the selection state (per `mode`), the visible month (controlled `month` + `onMonthChange`, or uncontrolled `defaultMonth`), the picker view (`days` / `months` / `years`, seeded by `defaultView`), the roving focus key, and the constraints (`minDate`, `maxDate`, `disabled`). Renders the bordered panel.
- `CalendarHeader` — the navigation row. Compose `CalendarPrevious` + `CalendarHeading` + `CalendarNext` inside it.
- `CalendarPrevious` / `CalendarNext` — real buttons with view-aware accessible names ("Go to previous month" / "year" / "12 years"). They disable themselves when `minDate` / `maxDate` make that direction impossible.
- `CalendarHeading` — an `aria-live="polite"` `<h2>` announcing the visible month/year. In the days and months views the label is a button that switches to the month / year picker.
- `CalendarGrid` — one month matrix (`role="grid"`). Render `<CalendarGrid monthOffset={i} />` once per visible month when using `numberOfMonths`. In the `months` / `years` views the first grid renders the picker panel and the others render nothing.
- `CalendarFooter` — an optional summary / action region separated by a hairline.

`useCalendar()` exposes the context to composed children (for example a footer "Today" action that calls `goToMonth` + `selectDate`).

## Selection Modes

The selection API is a discriminated union on `mode` — TypeScript rejects a `selected` shape that does not match the mode.

| Mode | `selected` | `onSelect` | Behavior |
|---|---|---|---|
| `single` (default) | `Date \| null` | `(date: Date \| null) => void` | One date. Clicking the selected date is a no-op — there is no accidental deselection. |
| `multiple` | `Date[]` | `(dates: Date[]) => void` | Click toggles a date in/out of the set. Updates are immutable — caller arrays are never mutated. |
| `range` | `DateRange \| null` (`{ from: Date; to: Date \| null }`) | `(range: DateRange \| null) => void` | First click starts (`to: null`); second click completes. See the range rules below. |

Range rules (predictable by design):

1. Clicking any date with a complete range (or none) starts a new range at that date.
2. Clicking the pending `from` date completes a **same-day range** (`from === to`).
3. Clicking a date **earlier** than `from` restarts the range at that date (no silent swap).
4. A completion that would **cross a disabled date** is rejected — the click restarts the range at the clicked date instead of producing a range that spans an unselectable day.

Every mode works controlled (`selected` + `onSelect`) or uncontrolled (`defaultSelected`). A component never mixes the two: pass `selected` to control it, `defaultSelected` to seed it.

The months view is a navigation aid, not a separate selection granularity: choosing a month pages the calendar to that month and returns to the day grid, where the actual date selection happens. The currently displayed month is marked with `aria-selected`. Months outside `minDate` / `maxDate` are disabled.

## Date Model and Timezones

Calendar dates are **local calendar dates**, never UTC timestamps.

- All arithmetic uses `new Date(year, month, day)` constructor normalization (`addDays`, `addMonths`) — never timestamp math (`getTime() + 86400000`), which shifts a day across DST transitions, and never string comparison.
- Day identity and ordering use a numeric key (`year * 10000 + (month+1) * 100 + day`), which is strictly monotonic with calendar order.
- `toISOString()` is never used (it converts to UTC and would shift the calendar day for most timezones).
- A selected date's *calendar* meaning is preserved: March 10 stays March 10 in the user's local calendar. The returned `Date` objects are local dates; compare them with `isSameDay` / `compareDays`, not `getTime()`.
- `minDate` / `maxDate` / `disabled(date)` are compared by calendar day — the time-of-day on the `Date` objects you pass is ignored.
- Week numbers follow ISO 8601 (weeks start Monday; week 1 contains the year's first Thursday), computed on local-noon copies so the Thursday shift is immune to midnight DST transitions.

## Date Constraints

`minDate` and `maxDate` are inclusive calendar-day boundaries. They disable:

- day cells outside the range (native `disabled` — not focusable, not activatable, announced as unavailable),
- the previous/next navigation buttons when the target month / year / 12-year page would hold no selectable day,
- month and year picker options that fall entirely outside the range,
- keyboard navigation — arrow/PageUp/PageDown movement skips disabled dates and never lands on one,
- range completion across the boundary (the range restarts instead of crossing).

Selection can never bypass constraints: every selection path (click, Enter/Space, footer actions) goes through the same `isDisabled` guard. The `disabled` matcher composes with `minDate` / `maxDate` (a date is disabled if any rule rejects it).

## Keyboard Interaction

| Key | Day grid | Month picker | Year picker |
|---|---|---|---|
| `ArrowLeft` / `ArrowRight` | Previous / next day | Previous / next month | Previous / next year |
| `ArrowUp` / `ArrowDown` | Same weekday, previous / next week | Same month ± 1 year-quarter row (± 3) | ± 3 years |
| `Home` / `End` | First / last day of the current week row (respects `weekStartsOn`) | January / December | First / last year of the page |
| `PageUp` / `PageDown` | Previous / next month (day clamped, e.g. Jan 31 → Feb 28) | Previous / next year | Previous / next 12-year page |
| `Shift+PageUp` / `Shift+PageDown` | Previous / next year | — | — |
| `Enter` / `Space` | Select the focused date (native button activation) | Choose the month | Choose the year |
| `Tab` / `Shift+Tab` | Moves into / out of the calendar — exactly one tabbable cell (roving tabindex) | same | same |

Focus model: roving `tabIndex` — only one cell in the calendar is tabbable at a time (the focused date, else the selected date, else today, else the first enabled day). Arrow movement skips disabled dates automatically, and moving past a month edge pages the visible month so focus is never lost. There are no keyboard traps: Tab always leaves the calendar. The previous/next buttons and the heading button are ordinary tab stops with visible focus rings.

## Accessibility

The day matrix follows the WAI-ARIA date-picker grid pattern:

- `role="grid"` per month (labelled with the month + year), `role="row"` per week, `role="columnheader"` for weekday labels (short text visible, full name in `aria-label`), `role="rowheader"` for ISO week numbers, `role="gridcell"` per day carrying `aria-selected`.
- Every day is a real `<button>` with a full locale-aware accessible name ("Friday, August 22, 2026") — never a bare number, never a clickable div.
- Today carries `aria-current="date"` — it is distinguishable from the *selected* date (which uses `aria-selected` + a filled treatment), and today is never auto-selected.
- Disabled dates use native `disabled` (exposed as unavailable, skipped by keyboard) and stay visible with reduced opacity — never hidden, never color-only.
- The month/year heading is `aria-live="polite"`, so navigation is announced.
- The previous/next buttons have view-aware accessible names; the heading button's `aria-label` explains that it opens the month/year picker.
- Selected vs. hover vs. today vs. disabled are distinguished by more than color alone (fill + weight, border + weight, opacity).

The months view is a `role="grid"` labelled 'Choose a month in 2026' with a 3-column roving-tabindex layout. Every option's accessible name includes the year ('March 2026'), so the target is unambiguous. The heading stays `aria-live` and announces the year being browsed; the previous/next buttons announce 'Go to previous/next year'.

## States

- **Default** — foreground text on the surface; hover shifts to `surface-hover`.
- **Selected** — solid `primary` fill with `primary-foreground` text and medium weight (fill + weight, not color alone). Hover darkens via `color-mix`.
- **Range start / end** — the same primary fill, squared toward the range interior; the **range middle** is a continuous `surface-active` band (squared corners).
- **Today** — a `border-strong` outline + semibold text; combined with the fill when today is also selected.
- **Focused** — the roving cell; keyboard focus shows a 2px `focus-ring` outline (`:focus-visible`).
- **Disabled** — native `disabled` + 40% opacity + `cursor-not-allowed`; skipped by pointer and keyboard.
- **Outside days** — muted-foreground text (with `showOutsideDays`); selecting one pages to its month.

All state transitions are 150ms `ease-out` color transitions and collapse to nothing under `prefers-reduced-motion`.

## Responsive Behavior

A single month grid is 252px wide (7 × 36px cells; 288px with week numbers) and fits a 375px viewport without scaling. Day cells are 36×36px — the family's default control size. With `numberOfMonths > 1`, wrap the grids in a `flex-col sm:flex-row` container (see `calendar-range`) so the months stack on narrow screens instead of overflowing. The month/year pickers use the same width and a 3-column layout. Every variant is verified overflow-free at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. The calendar follows the Calendar / Date Picker token rules: neutral surfaces, strong typography, thin borders, restrained radius (`radius-sm` cells, `radius-md` panel), compact 36px controls, a clear selected state, and light/dark parity.

## Notes

The heading button cycles days → months → years. This variant simply starts in the months view (`defaultView="months"`). PageUp/PageDown and the header chevrons page by year.
