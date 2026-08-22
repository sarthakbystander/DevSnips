"""Registry for the DevSnips React Date Picker generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference
``date-picker/code.tsx``). The generator (``_gen_react_datepicker.py``)
combines these with the reference ``code.tsx`` on disk to write ``code.tsx``
(derived), ``code.jsx``, ``preview.html``, ``metadata.json``, and
``README.md``.

Every variant is the SAME compound date picker; variants differ in how the
showcase composes it (single/range mode, label/error field chrome, presets,
constraints, footer/apply flow, time section, mobile sheet). Showcases use
fixed August 2026 anchors where possible so QA is deterministic. Realistic,
product-oriented demo content only (bookings, sprints, reporting windows).
No lorem ipsum, no marketing buzzwords.
"""
from _gen_react_datepicker import register

TAGS_BASE = ["date-picker", "date", "react", "tailwind", "accessible", "keyboard", "popover", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "WAI-ARIA dialog + grid", "roving tabindex", "controlled/uncontrolled", "locale-aware", "local calendar dates"]
A11Y_BASE = ['role="dialog" popover', 'role="grid" day matrix', "full locale-aware day labels", 'aria-selected on gridcells', 'aria-current="date" for today', "native disabled day buttons", "aria-live month/year heading", "aria-haspopup + aria-expanded field semantics", "focus restoration on close"]

# Shared props table — every variant exposes the same compound API.
PROPS_DOC = r"""### `<DatePicker>`

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

`daysInMonth(year, month)`, `isLeapYear(year)`, `addDays(date, n)`, `addMonths(date, n)` (day clamped to the target month), `startOfMonth(date)`, `endOfMonth(date)`, `compareDays(a, b)`, `isSameDay(a, b)`, `buildMonthWeeks(month, weekStartsOn)`, `formatISODate(date)`, `formatISODateTime(date)` — small, typed, local-calendar-date helpers (the same model the Calendar family ships), exported for reuse."""

# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = """const CARD = "rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const ROW_NAME = "m-0 text-sm font-medium text-[var(--ds-color-foreground)]";
const BTN_SMALL = "inline-flex h-7 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-2 text-xs font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const AUG_2026 = new Date(2026, 7, 1);
const fmtDay = (d) => (d ? new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric" }).format(d) : "");
"""


# 1. date-picker (reference)
register(
    "date-picker",
    title="Date Picker",
    subcategory="Core",
    description="The canonical compound date picker: a read-only display input + calendar trigger opening a non-modal dialog with the WAI-ARIA day grid — controlled and uncontrolled demos, full keyboard model, and focus restoration built in.",
    tags=TAGS_BASE + ["single-date", "controlled", "uncontrolled", "keyboard"],
    features=FEAT_BASE + ["single selection", "popover viewport flip", "focus restoration", "input + trigger semantics"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["date-picker-with-label", "date-picker-range", "date-picker-with-footer", "date-picker-month-year"],
    usage='''import DatePicker, {
  DatePickerInput, DatePickerTrigger, DatePickerContent,
} from "./date-picker";

<DatePicker value={date} onChange={setDate}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="This reference shows both halves of the state contract side by side: the release-date picker is fully **controlled** (`value` + `onChange` — the parent owns the date and can clear it externally), the visit picker is **uncontrolled** (no `defaultValue` — it seeds empty and reports through `onChange`). Both reuse the exact same composition.",
    validation_doc="No constraints here — the reference variant documents the unconstrained behavior. Selection still passes through the same `isDisabled` guard (which is trivially permissive without `minDate` / `maxDate` / `disabledDates`).",
    keyboard_doc=None,
    a11y_doc="The demos' readouts are `role=status` regions, so selection changes are announced without moving focus. After selection, focus returns to the input that opened the popover; the grid respects the roving-tabindex model throughout.",
    responsive_doc=None,
    notes_doc="Reference implementation for the DatePicker family. It establishes the compound API (`DatePicker` + input/trigger/content + header/calendar/footer/actions), the commit-vs-draft value model behind `requireApply`, the popover dismissal/restore behavior, and the self-contained derivation of the Calendar family's date grid.",
    limitations_doc=None,
    tsx_header="",
    showcase=DEMO_HELPERS + '''
function ReleaseDate() {
  const [date, setDate] = React.useState(new Date(2026, 7, 14));
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Release planning</p>
        <p className={ROW_NAME}>Code freeze date</p>
        <p className={NOTE}>Controlled: the parent owns the date and renders the summary.</p>
      </div>
      <DatePicker value={date} onChange={setDate}>
        <DatePickerInput id="dp-ref-input" />
        <DatePickerTrigger />
        <DatePickerContent />
      </DatePicker>
      <p className={NOTE} id="dp-ref-readout" role="status">
        {date ? "Freeze set for " + fmtDay(date) + "." : "No freeze date set."}
      </p>
      <button type="button" className={BTN_SMALL} id="dp-ref-clear" onClick={() => setDate(null)}>
        Clear externally
      </button>
    </div>
  );
}

function VisitDate() {
  const [reported, setReported] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Facilities</p>
        <p className={ROW_NAME}>Site visit</p>
        <p className={NOTE}>Uncontrolled: seeded empty, reported through onChange.</p>
      </div>
      <DatePicker onChange={setReported}>
        <DatePickerInput id="dp-ref-uncontrolled" />
        <DatePickerTrigger />
        <DatePickerContent />
      </DatePicker>
      <p className={NOTE} id="dp-ref-uncontrolled-readout" role="status">
        {reported ? "Visit requested for " + fmtDay(reported) + "." : "No date selected yet."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ReleaseDate />
      <VisitDate />
    </div>
  );
}
''',
)

# 2. date-picker-with-label
register(
    "date-picker-with-label",
    title="Date Picker — with Label",
    subcategory="Labeling",
    description="A date picker with the root-rendered field chrome: label, description, and helper text wired to the control with real `htmlFor` + `id` and `aria-describedby` associations — never visual proximity.",
    tags=TAGS_BASE + ["label", "description", "helper-text", "form"],
    features=FEAT_BASE + ["real label association", "aria-describedby wiring", "required marker"],
    accessibility=A11Y_BASE + ["htmlFor label association", "describedby description + helper ids"],
    interactive=True,
    related=["date-picker", "date-picker-with-error"],
    usage='''<DatePicker
  label="Appointment date"
  description="Bring your documents; the visit takes about 20 minutes."
  helperText="Slots open daily from 08:00."
  required
  value={date}
  onChange={setDate}
>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="The field chrome props (`label`, `description`, `helperText`, `error`) are optional; when any of them is present the root renders the field wrapper (label above, helper/error below) instead of a bare control row. Without them the composition renders inline with no chrome — both shapes are shown throughout the family.",
    validation_doc="`required` is set on this demo: the label gets a visual marker (`aria-hidden` asterisk) and the input carries `aria-required=\"true\"`. Form-level validation is the submit handler's job (see the error variant).",
    keyboard_doc=None,
    a11y_doc="The label is a real `<label htmlFor>` pointing at the input's generated id — clicking it focuses the control. The description and helper paragraphs register their ids in the input's `aria-describedby` (description + helper, in reading order). Required: `aria-required=\"true\"` on the input; the asterisk is presentation-only.",
    responsive_doc=None,
    notes_doc="Demonstrates the root-rendered field chrome in a vanilla form context. Contrast with `date-picker-with-error`, where the same wiring carries a validation message. The ids are auto-generated from `useId` and are always registered before they are referenced.",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — label / description / helper wiring.
 *
 * The shared compound DatePicker composed with the root-rendered field
 * chrome: a real `<label htmlFor>`, a description, helper text, and the
 * required marker, associated through generated `id` + `aria-describedby`.
 * Implementation identical to the reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function AppointmentField() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Registry office</p>
        <p className={ROW_NAME}>Book an appointment</p>
      </div>
      <DatePicker
        label="Appointment date"
        description="Bring your documents; the visit takes about 20 minutes."
        helperText="Slots open daily from 08:00."
        required
        value={date}
        onChange={setDate}
      >
        <DatePickerInput />
        <DatePickerTrigger />
        <DatePickerContent />
      </DatePicker>
      <p className={NOTE} id="dp-label-readout" role="status">
        {date ? "Booked for " + fmtDay(date) + "." : "No appointment yet."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <AppointmentField />
    </div>
  );
}
''',
)

# 3. date-picker-range
register(
    "date-picker-range",
    title="Date Picker — Range",
    subcategory="Selection",
    description="Two-month date range selection with a typed `DateRange` value (`{ from, to }`), live hover preview while the range is incomplete, an incomplete-range summary, and range clear — never an ambiguous string.",
    tags=TAGS_BASE + ["range", "hover-preview", "multi-month", "clear"],
    features=FEAT_BASE + ["range selection", "hover preview band", "2-month popover", "incomplete-range summary", "range clear"],
    accessibility=A11Y_BASE + ["range start/middle/end treatments", "hover preview (surface-hover) distinct from committed middle (surface-active)"],
    interactive=True,
    related=["date-picker", "date-picker-with-presets", "date-picker-with-disabled-dates"],
    usage='''const [range, setRange] = useState<DateRange | null>(null);

<DatePicker mode="range" numberOfMonths={2} value={range} onChange={setRange}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent>
    <DatePickerHeader />
    <DatePickerCalendar />
    <DatePickerFooter>
      <DatePickerClear />
    </DatePickerFooter>
  </DatePickerContent>
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="Range rules (predictable by design): the first pick starts a range (`to: null`); picking the pending `from` completes a same-day range; picking an earlier date restarts at that date; picking a date across a disabled day restarts (never a range spanning an unselectable day). The summary tracks the in-progress step readably (\"from – …\").",
    validation_doc="The incomplete state is explicit — the parent receives `{ from, to: null }` through `onChange` on the first pick and can render the pending summary. Apply-style committing of incomplete ranges is prevented globally (Apply would be disabled); here commits are immediate, so every `onChange` payload is a well-typed `DateRange`.",
    keyboard_doc=None,
    a11y_doc="During the incomplete step, pointer movement previews the would-be range with a distinct `surface-hover` band (committed middle uses `surface-active`) — the committed start stays filled. The two grids are labelled with their own month/year; there is still exactly one tabbable day cell across both months.",
    responsive_doc="`numberOfMonths: 2` renders both months below `sm` stacked vertically (the shared `flex-col sm:flex-row` container), so the popover stays fully inside the viewport at 375px.",
    notes_doc="The canonical range composition: multi-month grid, hover preview, footer clear. Presets and disabled dates compose the same way (see those variants).",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — range selection.
 *
 * The shared compound DatePicker in `mode="range"`: typed `DateRange`
 * values, two-month popover, live hover preview while the range is
 * incomplete, and a footer clear action. Implementation identical to the
 * reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function TripPlanner() {
  const [range, setRange] = React.useState(null);
  const from = range ? range.from : null;
  const to = range && range.to ? range.to : null;
  const nights = from && to ? Math.round((to - from) / 86400000) : 0;
  return (
    <div className={CARD + " w-full max-w-md space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Travel desk</p>
        <p className={ROW_NAME}>Trip dates</p>
        <p className={NOTE}>Pick start and end. Hover previews the range before you commit.</p>
      </div>
      <DatePicker mode="range" numberOfMonths={2} defaultMonth={AUG_2026} value={range} onChange={setRange}>
        <DatePickerInput id="dp-range-input" />
        <DatePickerTrigger />
        <DatePickerContent>
          <DatePickerHeader />
          <DatePickerCalendar />
          <DatePickerFooter>
            <p className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]" id="dp-range-summary">
              {from ? (to ? nights + " nights" : "Select an end date.") : "Start with the outbound day."}
            </p>
            <DatePickerClear />
          </DatePickerFooter>
        </DatePickerContent>
      </DatePicker>
      <p className={NOTE} id="dp-range-readout" role="status">
        {from ? (to ? "Trip: " + fmtDay(from) + " to " + fmtDay(to) + "." : "Trip starts " + fmtDay(from) + " — end pending.") : "No trip dates selected."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <TripPlanner />
    </div>
  );
}
''',
)

# 4. date-picker-with-presets
register(
    "date-picker-with-presets",
    title="Date Picker — with Presets",
    subcategory="Composite",
    description="A range date picker with a configurable preset panel (Today, Yesterday, Last 7 days, Last 30 days, This month): choosing a preset sets the actual typed range value and tracks the active preset with `aria-current`.",
    tags=TAGS_BASE + ["presets", "range", "reporting"],
    features=FEAT_BASE + ["configurable presets", "active-preset tracking", "range presets", "preset panel composition"],
    accessibility=A11Y_BASE + ['role="group" preset panel', 'aria-current="date" on the active preset'],
    interactive=True,
    related=["date-picker-range", "date-picker-with-footer"],
    usage='''const PRESETS = [
  { label: "Today", getValue: (today) => ({ from: today, to: today }) },
  { label: "Last 7 days", getValue: (today) => ({ from: addDays(today, -6), to: today }) },
  { label: "Last 30 days", getValue: (today) => ({ from: addDays(today, -29), to: today }) },
  { label: "This month", getValue: (today) => ({ from: startOfMonth(today), to: endOfMonth(today) }) },
];

<DatePicker mode="range" value={range} onChange={setRange}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent>
    <div className="flex flex-col gap-3 sm:flex-row">
      <DatePickerPresets presets={PRESETS} className="sm:border-r sm:border-[var(--ds-color-border-subtle)] sm:pr-3" />
      <div>
        <DatePickerHeader />
        <DatePickerCalendar />
      </div>
    </div>
  </DatePickerContent>
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="Each preset's `getValue(today)` returns a `Date` (single mode) or a `DateRange` (range mode) — mismatched shapes are ignored, so presets stay honest. Single-date presets like \"Today\" work as same-day ranges here (`{ from: today, to: today }`). The active preset (its value equal to the current value) is marked `aria-current=\"date\"` and shown with medium weight.",
    validation_doc="Presets pass through the same selection guard as manual picks (a preset whose days fall entirely inside `minDate`–`maxDate` still applies; constraints normally remain unset in preset demos).",
    keyboard_doc="Same as the base table. Preset buttons are ordinary tab stops; activating one behaves exactly like a manual completed pick (close + focus restore).",
    a11y_doc="The preset panel is a real `role=\"group\"` of buttons with an accessible group label — not a detachable decorative list. `aria-current=\"date\"` marks the option matching the current value.",
    responsive_doc="The preset column wraps horizontally below `sm` (shared `flex-col sm:flex-row` layout), so the popover never overflows at 375px.",
    notes_doc="Presets are a plain prop-driven list — a product registers exactly the entries it needs (they are not hard-coded inside the component). Ordering is stable; the active marker follows the value.",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — preset panel.
 *
 * The shared compound DatePicker in `mode="range"` with a `DatePickerPresets`
 * panel: configurable relative presets (Today, Yesterday, Last 7/30 days,
 * This month) that set the actual typed range value. Implementation
 * identical to the reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
const RANGE_PRESETS = [
  { label: "Today", getValue: (today) => ({ from: today, to: today }) },
  { label: "Yesterday", getValue: (today) => { const y = addDays(today, -1); return { from: y, to: y }; } },
  { label: "Last 7 days", getValue: (today) => ({ from: addDays(today, -6), to: today }) },
  { label: "Last 30 days", getValue: (today) => ({ from: addDays(today, -29), to: today }) },
  { label: "This month", getValue: (today) => ({ from: startOfMonth(today), to: endOfMonth(today) }) },
];

function ReportWindow() {
  const [range, setRange] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-md space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Usage report</p>
        <p className={ROW_NAME}>Reporting window</p>
        <p className={NOTE}>Common windows on the left; fine-tune on the grid.</p>
      </div>
      <DatePicker mode="range" value={range} onChange={setRange}>
        <DatePickerInput id="dp-preset-input" />
        <DatePickerTrigger />
        <DatePickerContent>
          <div className="flex flex-col gap-3 sm:flex-row">
            <DatePickerPresets presets={RANGE_PRESETS} className="sm:border-r sm:border-[var(--ds-color-border-subtle)] sm:pr-3" />
            <div>
              <DatePickerHeader />
              <DatePickerCalendar />
            </div>
          </div>
        </DatePickerContent>
      </DatePicker>
      <p className={NOTE} id="dp-preset-readout" role="status">
        {range && range.from ? (range.to ? "Window: " + fmtDay(range.from) + " to " + fmtDay(range.to) + "." : "Window starts " + fmtDay(range.from) + " — end pending.") : "No window selected."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ReportWindow />
    </div>
  );
}
''',
)

# 5. date-picker-with-disabled-dates
register(
    "date-picker-with-disabled-dates",
    title="Date Picker — with Disabled Dates",
    subcategory="Constraints",
    description="Constraint enforcement end to end: disabled weekends + a holiday hold + a min/max booking window. Disabled days are genuinely non-selectable — pointer, keyboard, and range completion all respect them.",
    tags=TAGS_BASE + ["disabled-dates", "min-max", "constraints"],
    features=FEAT_BASE + ["disabled matcher", "min/max window", "range-crossing guard", "nav button clamping"],
    accessibility=A11Y_BASE + ["native disabled on constrained days", "keyboard movement skips disabled constraints"],
    interactive=True,
    related=["date-picker-range", "date-picker-month-year"],
    usage='''const MIN = new Date(2026, 7, 3);
const MAX = new Date(2026, 8, 25);
const HOLD = new Date(2026, 7, 15);
const isWeekend = (d) => d.getDay() === 0 || d.getDay() === 6;
const disabledDates = (d) => isWeekend(d) || isSameDay(d, HOLD);

<DatePicker
  minDate={MIN}
  maxDate={MAX}
  disabledDates={disabledDates}
  value={date}
  onChange={setDate}
>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent>
    <DatePickerHeader />
    <DatePickerCalendar />
    <DatePickerFooter>
      <p className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">Weekdays only.</p>
      <DatePickerClear />
    </DatePickerFooter>
  </DatePickerContent>
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="The demo anchors a booking window (`minDate` = Aug 3, `maxDate` = Sep 25, 2026) plus a matcher that rejects weekends and the Aug 15 hold. Constraints are evaluated on every render — nothing is pre-filtered or string-compared.",
    validation_doc="This variant is the constraint showcase: weekends + hold via `disabledDates`, outer window via `minDate` / `maxDate`. The navigation clamps at the window edges (the previous button disables at the earliest month), the month/year pickers disable out-of-window options, and keyboard movement skips disabled days automatically. Range-crossing guard: completing a range over a disabled day restarts the range.",
    keyboard_doc=None,
    a11y_doc="Disabled days remain visible with reduced opacity and carry native `disabled` — assistive technology reports them as unavailable, and they leave the tab order entirely. Constraints are never communicated by color alone (opacity + cursor + native semantics).",
    responsive_doc=None,
    notes_doc="Composability matters: a single `isDisabled` predicate merges `minDate`, `maxDate`, and the matcher, and every selection path (click, keyboard, Today, presets) consults it. Matchers receive local `Date` objects — decide with `getDay()` / `isSameDay`, not string parsing.",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — disabled dates and constraints.
 *
 * The shared compound DatePicker with a `disabledDates` matcher (weekends
 * plus a holiday hold) inside a `minDate` / `maxDate` booking window.
 * Disabled days are genuinely non-selectable across pointer, keyboard, and
 * range completion. Implementation identical to the reference
 * `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
const BOOK_MIN = new Date(2026, 7, 3);
const BOOK_MAX = new Date(2026, 8, 25);
const BOOK_HOLD = new Date(2026, 7, 15);
const bookWeekend = (d) => d.getDay() === 0 || d.getDay() === 6;
const bookBlocked = (d) => bookWeekend(d) || isSameDay(d, BOOK_HOLD);

function ClinicBooking() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Clinic scheduling</p>
        <p className={ROW_NAME}>Book an exam slot</p>
        <p className={NOTE}>Weekdays only, inside the term window. August 15 is a staff hold.</p>
      </div>
      <DatePicker
        minDate={BOOK_MIN}
        maxDate={BOOK_MAX}
        disabledDates={bookBlocked}
        defaultMonth={AUG_2026}
        value={date}
        onChange={setDate}
      >
        <DatePickerInput id="dp-disabled-input" />
        <DatePickerTrigger />
        <DatePickerContent>
          <DatePickerHeader />
          <DatePickerCalendar />
          <DatePickerFooter>
            <p className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">Weekdays only.</p>
            <DatePickerClear />
          </DatePickerFooter>
        </DatePickerContent>
      </DatePicker>
      <p className={NOTE} id="dp-disabled-readout" role="status">
        {date ? "Exam on " + fmtDay(date) + "." : "No slot selected."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ClinicBooking />
    </div>
  );
}
''',
)

# 6. date-picker-with-error
register(
    "date-picker-with-error",
    title="Date Picker — with Error",
    subcategory="Validation",
    description="Real form validation: a required date picker that surfaces an `aria-invalid` error with `role=\"alert\"` on submit, resolves it on selection, and is connected to the control through `aria-describedby` — demonstrated in a working form.",
    tags=TAGS_BASE + ["error", "validation", "aria-invalid", "form"],
    features=FEAT_BASE + ["error message wiring", "aria-invalid tracking", "real form demo", "required"],
    accessibility=A11Y_BASE + ['role="alert" error message', "aria-invalid on the input", "error id in aria-describedby"],
    interactive=True,
    related=["date-picker-with-label", "date-picker"],
    usage='''const [date, setDate] = useState<Date | null>(null);
const [error, setError] = useState("");

<form onSubmit={handleSubmit}>
  <DatePicker
    label="Departure date"
    helperText="We hold your seat for 15 minutes."
    error={error}
    required
    name="departure"
    value={date}
    onChange={(d) => { setDate(d); if (d) setError(""); }}
  >
    <DatePickerInput />
    <DatePickerTrigger />
    <DatePickerContent />
  </DatePicker>
  <button type="submit">Request booking</button>
</form>

// handleSubmit: if (!date) setError("Select a departure date.")''',
    props_doc=PROPS_DOC,
    value_doc="The `error` string is the whole validation contract: while it is non-empty the input carries `aria-invalid=\"true\"` and the message renders with `role=\"alert\"`; the helper text hides so exactly one message region owns the `aria-describedby` slot (description + error, in order).",
    validation_doc="The demo is a real `<form>`: submitting empty sets the error, picking a date clears it (change handler), and a valid submit confirms the booking through a `role=\"status\"` region. The hidden `name=\"departure\"` input carries the ISO value for real submission. `required` conveys the semantics; the actual gate runs in the submit handler because native validation is barred for the read-only display input (documented, not faked).",
    keyboard_doc=None,
    a11y_doc="The error message is referenced by the input's `aria-describedby` and announces with `role=\"alert\"`; `aria-invalid` flips while the error is non-empty and clears on a successful pick. Contrast with `date-picker-with-label`, where the helper owns the message slot.",
    responsive_doc=None,
    notes_doc="The pattern stays valid without the form demo: `error` can be driven by any validator. The destructive border tracks the error state (border + message + aria — never color alone).",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — error / validation wiring.
 *
 * The shared compound DatePicker with the root-rendered error message:
 * `role="alert"`, `aria-invalid` on the input, and the error id registered
 * in `aria-describedby` — exercised by a real form submit handler.
 * Implementation identical to the reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function BookingForm() {
  const [date, setDate] = React.useState(null);
  const [error, setError] = React.useState("");
  const [sent, setSent] = React.useState("");
  const submit = (e) => {
    e.preventDefault();
    if (!date) {
      setError("Select a departure date.");
      setSent("");
      return;
    }
    setError("");
    setSent("Booking requested for " + fmtDay(date) + ".");
  };
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Rail desk</p>
        <p className={ROW_NAME}>Request a booking</p>
      </div>
      <form onSubmit={submit} noValidate className="space-y-3">
        <DatePicker
          label="Departure date"
          helperText="We hold your seat for 15 minutes."
          error={error}
          required
          name="departure"
          defaultMonth={AUG_2026}
          value={date}
          onChange={(d) => { setDate(d); if (d) setError(""); }}
        >
          <DatePickerInput id="dp-error-input" />
          <DatePickerTrigger />
          <DatePickerContent />
        </DatePicker>
        <button
          type="submit"
          id="dp-error-submit"
          className="inline-flex h-9 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none"
        >
          Request booking
        </button>
        <p className={NOTE} id="dp-error-sent" role="status">{sent}</p>
      </form>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <BookingForm />
    </div>
  );
}
''',
)

# 7. date-picker-month-year
register(
    "date-picker-month-year",
    title="Date Picker — Month + Year Pickers",
    subcategory="Navigation",
    description="Efficient long-range selection: the popover opens directly in the month picker, the heading cycles days → months → years, and the year pager covers decades without an unusable dropdown — full keyboard support throughout.",
    tags=TAGS_BASE + ["month-picker", "year-picker", "navigation"],
    features=FEAT_BASE + ["month picker view", "year picker view", "view cycle", "paged year spans"],
    accessibility=A11Y_BASE + ["picker grid semantics", "picker keyboard model"],
    interactive=True,
    related=["date-picker", "date-picker-with-disabled-dates"],
    usage='''<DatePicker defaultView="months" value={date} onChange={setDate}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent />
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="Useful when dates commonly sit months or years away (expiry, graduation, historic periods). The picker views never select — they only navigate; selection still happens on the day grid (`defaultView=\"months\"` just chooses the entry view).",
    validation_doc="Constraints clamp the pickers too: month and year options outside `minDate` / `maxDate` are native-disabled, and the previous/next pager buttons disable at the span edges — the paged 12-year spans stay finite and understandable instead of an endless scroll.",
    keyboard_doc="The picker grids get their own keyboard model (see the base table): arrows move by row, PageUp/PageDown by year / 12-year page, Home/End by span edge, and choosing a month or year returns to the day grid with focus placed on the same day clamped into the target month.",
    a11y_doc="Month and year pickers are real `role=\"grid\"` panels with `aria-selected` on the current option and native disabled on constrained options. The heading's `aria-label` explains the cycle (\"… — activate to choose a month/year\").",
    responsive_doc=None,
    notes_doc="`defaultView=\"months\"` is the one-line configuration; the heading button always exposes the full cycle days → months → years → back to days once a year is chosen. The pager spans 12 years per page, so decades never materialize as a long dropdown.",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — month + year pickers.
 *
 * The shared compound DatePicker opening directly in the month picker
 * (`defaultView="months"`), with the heading cycle and paged 12-year spans
 * for efficient long-range navigation. Implementation identical to the
 * reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function GraduationYear() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Registrar</p>
        <p className={ROW_NAME}>Expected graduation</p>
        <p className={NOTE}>Opens in month view; the heading also reaches the year pager.</p>
      </div>
      <DatePicker defaultView="months" defaultMonth={AUG_2026} value={date} onChange={setDate}>
        <DatePickerInput id="dp-my-input" />
        <DatePickerTrigger />
        <DatePickerContent />
      </DatePicker>
      <p className={NOTE} id="dp-my-readout" role="status">
        {date ? "Graduation: " + fmtDay(date) + "." : "No date selected."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <GraduationYear />
    </div>
  );
}
''',
)

# 8. date-picker-with-footer
register(
    "date-picker-with-footer",
    title="Date Picker — with Footer (Apply Flow)",
    subcategory="Behavior",
    description="Staged selection with an explicit commit: the footer carries Today / Clear / Apply, the input keeps showing the committed value while the calendar stages a draft, and a live staged readout shows what Applying would set.",
    tags=TAGS_BASE + ["footer", "apply", "today", "staged-selection"],
    features=FEAT_BASE + ["staged draft", "apply commit", "today action", "clear action", "staged readout"],
    accessibility=A11Y_BASE + ["staged value read via useDatePicker", "discard on Escape / outside"],
    interactive=True,
    related=["date-picker", "date-picker-with-presets"],
    usage='''<DatePicker requireApply value={date} onChange={setDate}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent>
    <DatePickerHeader />
    <DatePickerCalendar />
    <DatePickerFooter>
      <StagedReadout />
      <div className="flex gap-1">
        <DatePickerToday />
        <DatePickerClear />
        <DatePickerApply />
      </div>
    </DatePickerFooter>
  </DatePickerContent>
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="`requireApply` splits the value into a committed outer value and a staged draft: picking days updates only the draft (`onChange` does not fire), `DatePickerApply` commits it (with `onChange`), and closing any other way (Escape, outside) discards the draft — reopening restarts from the committed value. `DatePickerClear` is the deliberate exception: it empties both immediately. `DatePickerToday` stages today (respecting constraints).",
    validation_doc="Apply is disabled while a range is incomplete (single-mode demo always able to apply here). The parent still uses ordinary `value`/`onChange` — the distinction is entirely interaction semantics.",
    keyboard_doc=None,
    a11y_doc="The staged readout is a composed child (`useDatePicker()` reads `stagedValue` + `formatValue`) in a `role=\"status\"` region, so staging is announced without focus moves. Apply restores focus to the opener on commit.",
    responsive_doc=None,
    notes_doc="This is the correct pattern when picking a date has consequences (recalculating prices, re-fetching a report): intermediate picks no longer fire effects. Contrast with the reference variant, where every pick commits immediately.",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — footer with Today / Clear / Apply.
 *
 * The shared compound DatePicker with `requireApply`: picking stages a draft,
 * `DatePickerApply` commits it, Escape / outside close discards it, and
 * `DatePickerClear` empties both immediately. Implementation identical to
 * the reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function StagedNote() {
  const ctx = useDatePicker();
  return (
    <p className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]" id="dp-footer-staged" role="status">
      {ctx.formatValue(ctx.stagedValue) || "Nothing staged."}
    </p>
  );
}

function ApprovalDate() {
  const [date, setDate] = React.useState(new Date(2026, 7, 20));
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Approvals</p>
        <p className={ROW_NAME}>Effective date</p>
        <p className={NOTE}>Nothing changes until you Apply — Escape discards the draft.</p>
      </div>
      <DatePicker requireApply value={date} onChange={setDate}>
        <DatePickerInput id="dp-footer-input" />
        <DatePickerTrigger />
        <DatePickerContent>
          <DatePickerHeader />
          <DatePickerCalendar />
          <DatePickerFooter>
            <StagedNote />
            <div className="flex gap-1">
              <DatePickerToday />
              <DatePickerClear />
              <DatePickerApply />
            </div>
          </DatePickerFooter>
        </DatePickerContent>
      </DatePicker>
      <p className={NOTE} id="dp-footer-readout" role="status">
        {date ? "Effective from " + fmtDay(date) + "." : "No effective date."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ApprovalDate />
    </div>
  );
}
''',
)

# 9. date-picker-date-time
register(
    "date-picker-date-time",
    title="Date Picker — Date + Time",
    subcategory="Composite",
    description="Combined date and time selection: the day grid plus real hour/minute `<select>` controls (disabled until a date exists), a Done commit, and a form value serialized as `yyyy-mm-ddThh:mm`.",
    tags=TAGS_BASE + ["date-time", "time-select", "form"],
    features=FEAT_BASE + ["hour/minute selects", "off-step values preserved", "ISO datetime form value", "time default 12:00"],
    accessibility=A11Y_BASE + ["labelled time selects", "disabled-until-date time section"],
    interactive=True,
    related=["date-picker", "date-picker-with-footer"],
    usage='''<DatePicker withTime timeStep={15} name="checkin" value={dt} onChange={setDt}>
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
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="`withTime` upgrades the single value to date+time: picking a day preserves the current time (defaulting to 12:00 when empty), the selects rewrite hours/minutes on the committed value, and the display format includes `timeStyle: \"short\"` (24-hour). The hidden form input serializes `yyyy-mm-ddThh:mm` from local parts. Minute options follow `timeStep` (15 here), but an off-step current value is always offered so nothing is silently lost.",
    validation_doc="Until a date exists the time section is genuinely disabled (native `disabled` — not focusable) with a visible explanation; that ordering guard holds across clear/reset too. `DatePickerApply` is a \"Done\" here — without `requireApply` it simply closes with focus restored.",
    keyboard_doc="Same as the base table; the hour/minute `<select>` controls are native and fully keyboard-operable (arrows / typing / Home / End inside the open listbox). Tab reaches them after the grid.",
    a11y_doc="Each select is wrapped by a real `<label>` (visible \"Hours\" / \"Minutes\") — implicit association, not aria gymnastics — and the group sits after the calendar in reading order. The disable-until-date state is conveyed natively.",
    responsive_doc=None,
    notes_doc="The time section composes between the calendar and the footer, as shown. Model: minutes/hours live on the same `Date` as the day; there is no separate second state to keep in sync.",
    limitations_doc="`withTime` covers hour/minute selection in 24-hour presentation; seconds, 12-hour dials, and timezone selection are out of scope. Range + time is supported by the core (applied to both endpoints) but is not a shipped variant.",
    tsx_header='''/**
 * DevSnips React Date Picker — date + time.
 *
 * The shared compound DatePicker with `withTime`: the day grid plus real
 * hour/minute `<select>` controls (disabled until a date exists), Done
 * commit, and `yyyy-mm-ddThh:mm` form serialization. Implementation
 * identical to the reference `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function CheckIn() {
  const [dt, setDt] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Equipment desk</p>
        <p className={ROW_NAME}>Check-in window</p>
        <p className={NOTE}>Pick the day, then set the time. Saved as ISO datetime.</p>
      </div>
      <DatePicker withTime timeStep={15} name="checkin" defaultMonth={AUG_2026} value={dt} onChange={setDt}>
        <DatePickerInput id="dp-dt-input" />
        <DatePickerTrigger />
        <DatePickerContent>
          <DatePickerHeader />
          <DatePickerCalendar />
          <DatePickerTime />
          <DatePickerFooter>
            <p className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]" id="dp-dt-iso">
              {dt ? formatISODateTime(dt) : "No value."}
            </p>
            <div className="flex gap-1">
              <DatePickerClear />
              <DatePickerApply />
            </div>
          </DatePickerFooter>
        </DatePickerContent>
      </DatePicker>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <CheckIn />
    </div>
  );
}
''',
)

# 10. date-picker-mobile
register(
    "date-picker-mobile",
    title="Date Picker — Mobile",
    subcategory="Layout",
    description="Mobile-first presentation: below `sm` the panel docks as a full-width bottom sheet over a dimmed overlay with 44px touch targets (`size=\"lg\"`); at desktop it stays a normal popover — pure CSS breakpoint behavior, zero viewport JavaScript.",
    tags=TAGS_BASE + ["mobile", "bottom-sheet", "touch-targets"],
    features=FEAT_BASE + ["mobile bottom sheet", "44px cells", "CSS-only breakpoint behavior", "overlay dismissal"],
    accessibility=A11Y_BASE + ["overlay is aria-hidden + below sm only", "touch sizes honored"],
    interactive=True,
    related=["date-picker", "date-picker-range"],
    usage='''<DatePicker size="lg" value={date} onChange={setDate}>
  <DatePickerInput />
  <DatePickerTrigger />
  <DatePickerContent mobileSheet>
    <DatePickerHeader />
    <DatePickerCalendar />
    <DatePickerFooter>
      <DatePickerClear />
      <DatePickerApply />
    </DatePickerFooter>
  </DatePickerContent>
</DatePicker>''',
    props_doc=PROPS_DOC,
    value_doc="`DatePickerContent mobileSheet` + `size=\"lg\"` on the root is the whole recipe. The same composition works at every breakpoint — the breakpoint logic lives in `max-sm:` / `sm:` Tailwind variants, so narrowing the browser (or emulating a phone) docks the sheet without any media query in JavaScript.",
    validation_doc="The sheet closes through the overlay (outside pointer interaction) — the same dismissal path as the desktop popover — and Apply/Done keeps focus restoration.",
    keyboard_doc=None,
    a11y_doc="The dimmed overlay is `aria-hidden` and visually under the panel (`z-40` vs panel `z-50`); it exists below `sm` only (`sm:hidden`). Content order stays identical between breakpoints, so screen readers see one structure.",
    responsive_doc="This variant IS the responsive showcase: at 375px the sheet spans the viewport width docked to the bottom, 44px cells keep touch targets comfortable, and tall content scrolls inside the capped sheet (`max-h-[75dvh]`). At ≥768px it is a normal anchored popover.",
    notes_doc="Prefer this composition for app-like flows (check-in, field service, booking) where the sheet reads better than a floating popover on phones. `size=\"lg\"` enlarges cells, nav buttons, and picker buttons together.",
    limitations_doc=None,
    tsx_header='''/**
 * DevSnips React Date Picker — mobile bottom sheet.
 *
 * The shared compound DatePicker with `DatePickerContent mobileSheet` and
 * `size="lg"`: below `sm` the panel docks full-width over a dimmed overlay
 * with 44px touch targets; at desktop it stays a popover. Pure CSS
 * breakpoint behavior. Implementation identical to the reference
 * `date-picker/code.tsx`.
 */''',
    showcase=DEMO_HELPERS + '''
function FieldCheckIn() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-3"}>
      <div className="space-y-1">
        <p className={LABEL}>Field service</p>
        <p className={ROW_NAME}>Technician visit</p>
        <p className={NOTE}>On a phone the panel docks as a bottom sheet; on desktop it pops over.</p>
      </div>
      <DatePicker size="lg" value={date} onChange={setDate}>
        <DatePickerInput id="dp-mobile-input" />
        <DatePickerTrigger />
        <DatePickerContent mobileSheet>
          <DatePickerHeader />
          <DatePickerCalendar />
          <DatePickerFooter>
            <p className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">Same picker at every width.</p>
            <div className="flex gap-1">
              <DatePickerClear />
              <DatePickerApply />
            </div>
          </DatePickerFooter>
        </DatePickerContent>
      </DatePicker>
      <p className={NOTE} id="dp-mobile-readout" role="status">
        {date ? "Visit on " + fmtDay(date) + "." : "No visit scheduled."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <FieldCheckIn />
    </div>
  );
}
''',
)
