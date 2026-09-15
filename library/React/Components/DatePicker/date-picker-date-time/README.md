# Date Picker — Date + Time

Combined date and time selection: the day grid plus real hour/minute `<select>` controls (disabled until a date exists), a Done commit, and a form value serialized as `yyyy-mm-ddThh:mm`.

## Installation

Copy `code.tsx` into your project (or `code.jsx` for plain-JavaScript builds — same API, types stripped). The only runtime dependency is React 18+; there is **no date library and no positioning library** — the component ships its own small, typed date utilities (`addDays`, `addMonths`, `compareDays`, `isSameDay`, `daysInMonth`, `isLeapYear`, `buildMonthWeeks`, `startOfMonth`, `endOfMonth`, `formatISODate`, `formatISODateTime`), which are also exported for reuse.

The component consumes DevSnips `--ds-*` design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme per [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) — no component-specific CSS file is required.

## Usage

```tsx
<DatePicker withTime timeStep={15} name="checkin" value={dt} onChange={setDt}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent>
    <DatePickerHeader />
    <DatePickerCalendar />
    <DatePickerTime />
    <DatePickerFooter>
      <DatePickerClear />
      <DatePickerApply />
    </DatePickerFooter>
  </DatePickerContent>
</DatePicker>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
<DatePicker withTime timeStep={15} name="checkin" value={dt} onChange={setDt}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent>
    <DatePickerHeader />
    <DatePickerCalendar />
    <DatePickerTime />
    <DatePickerFooter>
      <DatePickerClear />
      <DatePickerApply />
    </DatePickerFooter>
  </DatePickerContent>
</DatePicker>
```

## Props

### `<DatePicker>`

| Name | Type | Default | Description |
|---|---|---|---|
| `mode` | `"single" \| "range"` | `"single"` | Selection mode. Determines the shape of `value` / `defaultValue` / `onChange` (discriminated union). |
| `value` | `Date \| null` · `DateRange \| null` | — | The committed value (controlled). Shape follows `mode`. |
| `defaultValue` | same as `value` | `null` | Initial value (uncontrolled). |
| `onChange` | `(date) => void` · `(range) => void` | — | Called on every committed change. With `requireApply`, only Apply/Clear/Today/presets commit. |
| `open` | `boolean` | — | Popover open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled). Never steals focus on mount. |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the popover opens or closes. |
| `minDate` | `Date` | — | Earliest selectable calendar day (inclusive). |
| `maxDate` | `Date` | — | Latest selectable calendar day (inclusive). |
| `disabledDates` | `(date: Date) => boolean` | — | Matcher for individual disabled dates; composes with `minDate` / `maxDate`. |
| `locale` | `string` | `"en-US"` | BCP-47 tag for calendar labels and the default display format (`Intl.DateTimeFormat`). |
| `weekStartsOn` | `0 \| 1 \| 2 \| 3 \| 4 \| 5 \| 6` | `0` | First weekday column (0 = Sunday, 1 = Monday, …). |
| `formatDate` | `(date: Date) => string` | `Intl` medium (+ short time) | Display formatter for the committed value in the input. |
| `placeholder` | `string` | `"Select date"` / `"Select date range"` | Input placeholder. |
| `disabled` | `boolean` | `false` | Disables the control: no popover, not focusable, not form-submitted. |
| `readOnly` | `boolean` | `false` | Freezes the value: focusable + submitted, but the popover cannot open. |
| `required` | `boolean` | `false` | `aria-required` + required marker on the root-rendered label. |
| `name` | `string` | — | Form field name: a hidden input submits the ISO value (`yyyy-mm-dd`, `yyyy-mm-ddThh:mm` with `withTime`, `from/to` for ranges). |
| `label` | `string` | — | Label rendered by the root, associated via `htmlFor` + `id`. |
| `description` | `string` | — | Description above the control, referenced via `aria-describedby`. |
| `helperText` | `string` | — | Helper below the control (hidden while `error` is set), referenced via `aria-describedby`. |
| `error` | `string` | — | Error message: `role="alert"`, `aria-invalid` on the input, referenced via `aria-describedby`. |
| `triggerLabel` | `string` | `"Open calendar"` | Accessible name of the trigger button. |
| `inputAriaLabel` | `string` | `"Date"` / `"Date range"` | Accessible name of the input when no `label` is rendered. |
| `requireApply` | `boolean` | `false` | Stage selection as a draft; only `<DatePickerApply>` commits it. |
| `withTime` | `boolean` | `false` | Adds hour/minute selection; the popover stays open until Apply/Done. |
| `timeStep` | `number` | `5` | Minute step for the time controls (clamped to 1–60; the current value is always offered). |
| `defaultMonth` | `Date` | selection month, else today | Initial visible month (uncontrolled). |
| `numberOfMonths` | `number` | `1` | Consecutive month grids in the popover (stack below `sm`). |
| `defaultView` | `"days" \| "months" \| "years"` | `"days"` | Initial picker view. The heading button cycles days → months → years regardless. |
| `size` | `"md" \| "lg"` | `"md"` | 36px cells (`md`) or 44px touch targets (`lg`). |
| `className` | `string` | — | Extra classes on the field / wrapper. |
| `children` | `ReactNode` | — | The composed parts (input, trigger, content). |

### Parts

| Part | Props | Renders |
|---|---|---|
| `DatePickerInput` | native input attrs (forwarded) | The read-only display input (`aria-haspopup="dialog"`). |
| `DatePickerTrigger` | native button attrs (forwarded) | The icon toggle button. |
| `DatePickerContent` | `mobileSheet`, native div attrs | The `role="dialog"` popover panel; default chrome = header + calendar. |
| `DatePickerHeader` | native div attrs | Previous / heading (view cycle) / next navigation row. |
| `DatePickerCalendar` | native div attrs | One `role="grid"` per visible month, or the month/year picker panel. |
| `DatePickerFooter` | native div attrs | Hairline-separated action region. |
| `DatePickerPresets` | `presets: DatePickerPreset[]`, `label` | Real-button preset group; active preset tracked with `aria-current="date"`. |
| `DatePickerToday` / `DatePickerClear` / `DatePickerApply` | native button attrs | Footer actions (auto-disabled when unusable). |
| `DatePickerTime` | native div attrs | Hour/minute `<select>` section (disabled until a date exists). |

`useDatePicker()` returns the root context for composed children — value (`committedValue`, `stagedValue`), `formatValue`, `open`, actions (`clearValue`, `applyDraft`, `selectToday`, `applyPreset`), calendar helpers (`isDisabled`, `goToPrevious`/`goToNext`, …).

### Date utilities

`daysInMonth(year, month)`, `isLeapYear(year)`, `addDays(date, n)`, `addMonths(date, n)` (day clamped to the target month), `startOfMonth(date)`, `endOfMonth(date)`, `compareDays(a, b)`, `isSameDay(a, b)`, `buildMonthWeeks(month, weekStartsOn)`, `formatISODate(date)`, `formatISODateTime(date)` — small, typed, local-calendar-date helpers (the same model the Calendar family ships), exported for reuse.

## Compound Components

- `DatePicker` — the root provider. Owns the value (controlled `value` + `onChange`, or uncontrolled `defaultValue`), the open state (controlled `open` + `onOpenChange`, or uncontrolled `defaultOpen`), the visible month (uncontrolled, seeded by `defaultMonth`), the picker view, the roving focus key, the constraints (`minDate`, `maxDate`, `disabledDates`), the locale/format, and the staged draft under `requireApply`. Renders the field chrome (label / description / helper / error) when those props are set.
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

`useDatePicker()` exposes the context to composed children (for example a staged-value readout in the footer).

## Controlled Usage

Pass `value` (+ `onChange`) to own the value, and/or `open` (+ `onOpenChange`) to own the popover:

```tsx
const [date, setDate] = useState<Date | null>(null);
const [open, setOpen] = useState(false);

<DatePicker value={date} onChange={setDate} open={open} onOpenChange={setOpen}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>
```

A component never mixes controlled and uncontrolled halves of one state: pass `value` to control it, `defaultValue` to seed it. The range mode's `value` is always a `DateRange | null` (`{ from: Date; to: Date | null }`) — never an ambiguous string.

## Uncontrolled Usage

Pass `defaultValue` / `defaultOpen` / `defaultMonth` to seed without owning state:

```tsx
<DatePicker defaultValue={new Date(2026, 7, 15)} onChange={logChange}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>
```

Selection still reports through `onChange` — uncontrolled only changes who stores the value.

## Date and Value Representation

The value model is a discriminated union on `mode` — TypeScript rejects a `value` shape that does not match the mode.

| Mode | `value` / `defaultValue` | `onChange` | Display |
|---|---|---|---|
| `single` (default) | `Date \| null` | `(date: Date \| null) => void` | One formatted date ("Aug 15, 2026"). Clicking the selected date is a no-op — never an accidental deselect; clearing is the explicit `DatePickerClear` / parent action. |
| `range` | `DateRange \| null` (`{ from: Date; to: Date \| null }`) | `(range: DateRange \| null) => void` | "from – to"; while incomplete (pointer or keyboard has only picked `from`) it reads "from – …". |

Dates are **local calendar dates**, never UTC timestamps. Identity and ordering use the numeric `dayKey` (`year*10000 + (month+1)*100 + day`), arithmetic uses `new Date(y, m, d + n)` constructor normalization — deterministic across DST transitions, leap years, and month/year boundaries. `Date` objects are never mutated. The form value (`name` prop) is a `yyyy-mm-dd` string built from local parts via `formatISODate` — `toISOString()` is never used anywhere (it converts to UTC and can shift the day). Range form values serialize as `from/to` (the `to` side empty while the range is incomplete); `withTime` values serialize as `yyyy-mm-ddThh:mm`.

`withTime` upgrades the single value to date+time: picking a day preserves the current time (defaulting to 12:00 when empty), the selects rewrite hours/minutes on the committed value, and the display format includes `timeStyle: "short"` (24-hour). The hidden form input serializes `yyyy-mm-ddThh:mm` from local parts. Minute options follow `timeStep` (15 here), but an off-step current value is always offered so nothing is silently lost.

## Validation

Constraint and validation behavior:

- `minDate` / `maxDate` are inclusive calendar-day boundaries. They disable day cells (native `disabled` — not focusable, not activatable), the navigation buttons when the target month/year/page holds no selectable day, the month/year picker options outside the range, and keyboard movement (arrows / PageUp / PageDown skip disabled dates and never land on one).
- `disabledDates` is a matcher `(date: Date) => boolean` composing with `minDate` / `maxDate` — a date is disabled when any rule rejects it. Disabled days stay visible with reduced opacity; they are genuinely non-selectable, not merely muted. Range completion across a disabled day is rejected (the click restarts the range instead of producing a range spanning an unselectable day).
- `error` sets `aria-invalid="true"` on the input and renders the message with `role="alert"`, referenced through `aria-describedby`. Clear the error when the user resolves it (the demos clear on change).
- `required` sets `aria-required="true"` and renders a required marker (visual only, `aria-hidden`) on the root-rendered label. Native `required` form validation does not apply — the display input is `readOnly` (barred from constraint validation) and the hidden input carries the ISO value — so validate in the form's submit handler, as the `date-picker-with-error` demo does.
- Selection can never bypass constraints: every selection path (click, Enter/Space, Today, presets) goes through the same `isDisabled` guard.

Until a date exists the time section is genuinely disabled (native `disabled` — not focusable) with a visible explanation; that ordering guard holds across clear/reset too. `DatePickerApply` is a "Done" here — without `requireApply` it simply closes with focus restored.

## Popover Behavior

The popover is a non-modal `role="dialog"` panel (no focus trap, no scroll lock):

- Opens from the input (click, `ArrowDown`, `Enter`, `Space`) or the trigger button; closing restores focus to the element that opened it.
- `Escape` closes and restores focus. Outside pointer interaction closes — when the click landed on a non-focusable surface, focus returns to the opener; when it landed on another control, focus follows the click naturally.
- `Tab` / `Shift+Tab` leave the panel from either end and close it — focus is never trapped and the natural order continues.
- In `single` mode the popover closes after selection; in `range` mode it stays open until the range completes; with `requireApply` / `withTime` it stays open until Apply/Done.
- The panel flips above the field when the space below runs out, and pins to the field's right edge when it would overflow the right viewport edge (pre-paint measurement, class-driven — no positioning library, no inline styles). `mobileSheet` docks it as a full-width bottom sheet below the `sm` breakpoint with a dimmed overlay, purely with `max-sm:` Tailwind variants — no JavaScript viewport detection.

## Keyboard Interaction

Same as the base table; the hour/minute `<select>` controls are native and fully keyboard-operable (arrows / typing / Home / End inside the open listbox). Tab reaches them after the grid.

## Accessibility

The popover follows the WAI-ARIA date-picker dialog pattern (a non-modal dialog containing a date grid — NOT the menu pattern):

- The input is a real `<input type="text">` (textually read-only) with `aria-haspopup="dialog"`, `aria-expanded`, and `aria-controls` (referenced only while open). The trigger is a real `<button>`. There are no clickable divs and no nested interactive elements.
- The panel is `role="dialog"` with an accessible name ("Choose date" / "Choose date range" / "Choose date and time"), containing a `role="grid"` day matrix (`role="row"`, `role="columnheader"` weekday labels with full names in `aria-label`, `role="gridcell"` carrying `aria-selected`).
- Every day is a real `<button>` with a full locale-aware accessible name ("Friday, August 15, 2026") — never a bare number.
- Today carries `aria-current="date"` — distinguishable from the *selected* date (`aria-selected` + filled treatment), and today is never auto-selected.
- Disabled dates use native `disabled`; the month/year heading is `aria-live="polite"`. Selected / hover / today / range start / range middle / range end / range hover preview / disabled are distinguished by more than color alone (fill + weight, squared range edges, border + weight, opacity).
- Field wiring is real: root-rendered `label` uses `htmlFor` + `id`; `description` / `helperText` / `error` register their generated ids in the input's `aria-describedby`; the error uses `role="alert"`; `required` uses `aria-required`; `aria-invalid` tracks the error state. State is never communicated by color alone.

Each select is wrapped by a real `<label>` (visible "Hours" / "Minutes") — implicit association, not aria gymnastics — and the group sits after the calendar in reading order. The disable-until-date state is conveyed natively.

## Responsive Behavior

A single month grid is 252px wide at the default `md` size (7 × 36px cells; 308px at `lg` 44px cells) and fits a 375px viewport. The panel's width is `max-w-[calc(100vw-1rem)]` and long localized dates wrap in the input instead of breaking the layout. With `numberOfMonths: 2` (and with presets) the popover content stacks vertically below `sm` instead of overflowing. The `mobileSheet` presentation docks the panel full-width at the bottom of the viewport below `sm`. Every variant is verified overflow-free at 375 / 768 / 1280px, open and closed.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. The date picker follows the Calendar / Date Picker token rules: neutral surfaces, strong typography, thin borders, restrained radius (`radius-sm` controls, `radius-md` panel), compact 36px controls (44px at `size="lg"`), a clear selected state, a 2px `focus-ring` ring, `surface-elevated` + `shadow-md` for the floating panel, `color.overlay` for the mobile sheet backdrop, and light/dark parity.

## Notes

The time section composes between the calendar and the footer, as shown. Model: minutes/hours live on the same `Date` as the day; there is no separate second state to keep in sync.

## Limitations

`withTime` covers hour/minute selection in 24-hour presentation; seconds, 12-hour dials, and timezone selection are out of scope. Range + time is supported by the core (applied to both endpoints) but is not a shipped variant.
