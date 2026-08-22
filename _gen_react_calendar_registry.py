"""Registry for the DevSnips React Calendar generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``calendar/code.tsx``).
The generator (``_gen_react_calendar.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Every variant is the SAME compound calendar; variants differ in how the
showcase composes it (selection mode, constraints, picker views, week
numbers, outside days, controlled state). Showcases use fixed dates
(August 2026 anchors) so QA is deterministic. Realistic, product-oriented
demo content only (bookings, on-call schedules, reporting periods). No
lorem ipsum, no marketing buzzwords.
"""
from _gen_react_calendar import register

TAGS_BASE = ["calendar", "date", "react", "tailwind", "accessible", "keyboard", "grid", "responsive", "interactive"]
FEAT_BASE = ["responsive", "light/dark", "reduced-motion", "focus-visible", "WAI-ARIA grid", "roving tabindex", "controlled/uncontrolled", "locale-aware", "local calendar dates"]
A11Y_BASE = ['role="grid" day matrix', "full locale-aware day labels", 'aria-selected on gridcells', 'aria-current="date" for today', "native disabled day buttons", "aria-live month/year heading", "roving tabindex keyboard model"]

# Shared props table — every variant exposes the same compound API.
PROPS_DOC = r"""### `<Calendar>`

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

`daysInMonth(year, month)`, `isLeapYear(year)`, `addDays(date, n)`, `addMonths(date, n)` (day clamped to the target month), `startOfMonth(date)`, `endOfMonth(date)`, `compareDays(a, b)`, `isSameDay(a, b)`, `isoWeekNumber(date)`, `buildMonthWeeks(month, weekStartsOn)` — small, typed, local-calendar-date helpers used internally and exported for reuse (they are the foundation of the DatePicker family)."""

# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = """const CARD = "rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const ROW_NAME = "m-0 text-sm font-medium text-[var(--ds-color-foreground)]";
const BTN_PRIMARY = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE = "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_SMALL = "inline-flex h-7 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-2 text-xs font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const SELECT = "h-9 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-2 text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const AUG_2026 = new Date(2026, 7, 1);
const fmtDay = (d) => (d ? new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric" }).format(d) : "");
const fmtMonth = (d) => (d ? new Intl.DateTimeFormat("en-US", { month: "long", year: "numeric" }).format(d) : "");
// The calendar composition every showcase reuses.
const CalendarChrome = ({ children }) => (
  <>
    <CalendarHeader>
      <CalendarPrevious />
      <CalendarHeading className="flex-1 text-center" />
      <CalendarNext />
    </CalendarHeader>
    {children}
  </>
);
"""


# 1. calendar (reference)
register(
    "calendar",
    title="Calendar",
    subcategory="Core",
    description="The canonical compound calendar: a WAI-ARIA grid of real day buttons with roving-tabindex keyboard navigation, month/year picker views, locale-aware labels, and local-calendar-date semantics — shown here as an uncontrolled single-date calendar.",
    tags=TAGS_BASE + ["single-date", "uncontrolled"],
    features=FEAT_BASE + ["single selection", "month/year picker views", "fixed 6-row grid"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["calendar-single", "calendar-range", "calendar-multiple", "calendar-with-footer"],
    usage='''import Calendar, {
  CalendarHeader, CalendarPrevious, CalendarNext, CalendarHeading, CalendarGrid,
} from "./calendar";

<Calendar defaultMonth={new Date(2026, 7, 1)} onSelect={setDate}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="This reference uses the default `single` mode, uncontrolled: the calendar owns its selection and reports it through `onSelect`. The visible month is seeded with `defaultMonth` (it would otherwise open on the selected date's month, or today's).",
    keyboard_doc=None,
    a11y_doc="The demo's readout is a `role=status` region, so selecting a day announces the chosen date without moving focus. Selection persists while navigating months — the visible month and the selection are independent pieces of state.",
    responsive_doc=None,
    notes_doc="Reference implementation for the Calendar family. It establishes the shared date model (local calendar dates, numeric day keys, constructor arithmetic), the compound API (`Calendar` + header parts + `CalendarGrid` + `CalendarFooter`), the days/months/years view cycle, and the roving-tabindex focus model that every other variant reuses.",
    tsx_header="",
    showcase=DEMO_HELPERS + '''
function VisitScheduler() {
  const [picked, setPicked] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Facilities</p>
        <p className={ROW_NAME}>Schedule a site visit</p>
        <p className={NOTE}>Pick a date for the walkthrough. The team confirms within one business day.</p>
      </div>
      <Calendar defaultMonth={AUG_2026} onSelect={setPicked}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="cal-readout" role="status">
        {picked ? "Visit requested for " + fmtDay(picked) + "." : "No date selected yet."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <VisitScheduler />
    </div>
  );
}
''',
)

# 2. calendar-single
register(
    "calendar-single",
    title="Calendar — Single Date",
    subcategory="Selection",
    description="Explicit single-date selection, controlled by the parent: the selected date drives a milestone summary, re-selecting the same day is a no-op, and clearing is only possible through the explicit external action.",
    tags=TAGS_BASE + ["single-date", "controlled"],
    features=FEAT_BASE + ["controlled selection", "no accidental deselect", "external clear"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["calendar", "calendar-with-footer", "calendar-controlled"],
    usage='''const [date, setDate] = useState<Date | null>(new Date(2026, 7, 12));

<Calendar selected={date} onSelect={setDate}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>

// Clearing is explicit — never an accidental second click on the same day:
<button onClick={() => setDate(null)}>Clear</button>''',
    props_doc=PROPS_DOC,
    selection_doc="In `single` mode, clicking the selected date does nothing — a second click is not a toggle. Clearing is possible, but only deliberately: the parent sets `selected` to `null` (controlled) or calls `clearSelection()` from a composed child via `useCalendar()`. This demo is fully controlled: the parent owns the date and renders it in the summary.",
    keyboard_doc=None,
    a11y_doc="Because selection is controlled, the summary text and the grid can never disagree: both render from the same state. The `aria-selected` gridcell, the filled day button, and the `role=status` summary all update together.",
    responsive_doc=None,
    notes_doc="Demonstrates the controlled half of the single-selection API. Contrast with the reference variant (`calendar`), which is uncontrolled. The `Clear` action shows that emptying the selection is a deliberate parent decision — `selected={null}` is a valid controlled state.",
    tsx_header="""/**
 * DevSnips React Calendar — single-date selection.
 *
 * The shared compound Calendar composed for explicit single-date selection:
 * controlled `selected` + `onSelect`, no accidental deselection on a repeat
 * click, clearing only through an explicit action. Implementation identical
 * to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function MilestonePlanner() {
  const [date, setDate] = React.useState(new Date(2026, 7, 12));
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Release planning</p>
        <p className={ROW_NAME}>Milestone date</p>
        <p className={NOTE}>The code freeze is scheduled against this date.</p>
      </div>
      <Calendar defaultMonth={AUG_2026} selected={date} onSelect={setDate}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <div className="flex items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-3">
        <p className={NOTE} id="single-readout" role="status">
          {date ? "Milestone: " + fmtDay(date) : "No milestone date set."}
        </p>
        <button type="button" className={BTN_SMALL} onClick={() => setDate(null)}>
          Clear
        </button>
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <MilestonePlanner />
    </div>
  );
}
''',
)


# 3. calendar-range
register(
    "calendar-range",
    title="Calendar — Range Selection",
    subcategory="Selection",
    description="Two-month range selection with a continuous in-range band: click a start, then an end — earlier clicks and disabled-day crossings restart the range predictably (the demo venue holds Aug 15), same-day ranges are supported, and the selection survives month navigation.",
    tags=TAGS_BASE + ["range", "multi-month"],
    features=FEAT_BASE + ["range selection", "numberOfMonths=2", "same-day ranges", "restart-on-crossing", "responsive stacking"],
    accessibility=A11Y_BASE + ["start/end/middle exposed via aria-selected"],
    interactive=True,
    related=["calendar-single", "calendar-multiple", "calendar-min-max", "calendar-disabled-dates"],
    usage='''const [range, setRange] = useState<DateRange | null>(null);

<Calendar mode="range" numberOfMonths={2} selected={range} onSelect={setRange}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <div className="flex flex-col gap-6 sm:flex-row">
    <CalendarGrid monthOffset={0} />
    <CalendarGrid monthOffset={1} />
  </div>
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="Range selection state is `{ from: Date; to: Date | null }`. The first click starts a range (`to` is `null` — the endpoint is a single filled day); the second completes it. Clicking an earlier date, or a date that would cross a disabled day, restarts the range at the clicked date instead of silently swapping or crossing. Clicking `from` again completes a same-day range. `onSelect` fires on every step, so a controlled parent can render the in-progress state.",
    keyboard_doc=None,
    a11y_doc="The range is not color-only: start and end are solid fills with squared inner corners, the middle is a continuous band, and every in-range gridcell carries `aria-selected=\"true\"`. The `role=status` summary announces the committed range (and the night count) as it changes.",
    responsive_doc="Two months render side by side from `sm` up and stack vertically below that — the grids are wrapped in `flex-col sm:flex-row`, so a 375px viewport gets one column and no horizontal scrolling.",
    notes_doc="The canonical multi-month composition. `numberOfMonths={2}` + one `CalendarGrid` per month; the header navigates both grids together. Outside days are off by default, so interior cells between the two months stay clean. Range math in the summary uses the exported `addDays` / `compareDays` utilities — no timestamp division.",
    tsx_header="""/**
 * DevSnips React Calendar — range selection.
 *
 * The shared compound Calendar in `mode="range"`: start/end/middle range
 * treatment, same-day ranges, restart-on-earlier-click, and no crossing of
 * disabled dates. Shown across two months (`numberOfMonths={2}`).
 * Implementation identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function StayPlanner() {
  const [range, setRange] = React.useState(null);
  let nights = 0;
  if (range && range.to) {
    for (let d = range.from; compareDays(d, range.to) < 0; d = addDays(d, 1)) nights += 1;
  }
  return (
    <div className={CARD + " w-full max-w-2xl space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Offsite</p>
        <p className={ROW_NAME}>Book the team retreat</p>
        <p className={NOTE}>Select the arrival and departure dates. The venue is on hold Aug 15.</p>
      </div>
      <Calendar
        mode="range"
        numberOfMonths={2}
        defaultMonth={AUG_2026}
        selected={range}
        onSelect={setRange}
        disabled={(d) => isSameDay(d, new Date(2026, 7, 15))}
      >
        <CalendarChrome>
          <div className="flex flex-col gap-6 sm:flex-row">
            <CalendarGrid monthOffset={0} />
            <CalendarGrid monthOffset={1} />
          </div>
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="range-readout" role="status">
        {range && range.to
          ? fmtDay(range.from) + " – " + fmtDay(range.to) + " · " + nights + " nights"
          : range
            ? "Arriving " + fmtDay(range.from) + " — select a departure date."
            : "Select an arrival date."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <StayPlanner />
    </div>
  );
}
''',
)

# 4. calendar-multiple
register(
    "calendar-multiple",
    title="Calendar — Multiple Dates",
    subcategory="Selection",
    description="Toggle-style multi-date selection with immutable updates: each click adds or removes one date, the selection is a plain Date array, and a controlled parent can clear or replace the whole set.",
    tags=TAGS_BASE + ["multiple", "toggle", "immutable"],
    features=FEAT_BASE + ["multiple selection", "toggle dates", "immutable array updates"],
    accessibility=A11Y_BASE,
    interactive=True,
    related=["calendar-range", "calendar-single", "calendar-with-footer"],
    usage='''const [days, setDays] = useState<Date[]>([]);

<Calendar mode="multiple" selected={days} onSelect={setDays}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="In `multiple` mode the selection is a `Date[]` and every click toggles one date: absent dates are appended, present dates are removed. Updates are immutable — the calendar always creates a new array (`[...dates, next]` / `filter`) and never mutates the caller's array, so React state comparisons and memoization keep working.",
    keyboard_doc=None,
    a11y_doc="Each selected date's gridcell carries `aria-selected=\"true\"` independently — assistive technology announces every chosen day as selected, not just the most recent one. The summary lists the selected dates in calendar order (sorted with the exported `compareDays`).",
    responsive_doc=None,
    notes_doc="Demonstrates the `multiple` selection mode with a controlled parent (an on-call rotation). The initial value is seeded, dates toggle on click, and the parent can clear the whole set with one action.",
    tsx_header="""/**
 * DevSnips React Calendar — multiple-date selection.
 *
 * The shared compound Calendar in `mode="multiple"`: toggle individual
 * dates in and out of a `Date[]`, with immutable updates. Implementation
 * identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function OnCallPlanner() {
  const [days, setDays] = React.useState([new Date(2026, 7, 5), new Date(2026, 7, 12), new Date(2026, 7, 19)]);
  const ordered = [...days].sort(compareDays);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Engineering</p>
        <p className={ROW_NAME}>On-call Wednesdays</p>
        <p className={NOTE}>Toggle the days this rotation covers.</p>
      </div>
      <Calendar mode="multiple" defaultMonth={AUG_2026} selected={days} onSelect={setDays}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <div className="flex items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-3">
        <p className={NOTE} id="multiple-readout" role="status">
          {days.length === 0
            ? "No on-call days selected."
            : days.length + " days: " + ordered.map((d) => fmtDay(d).replace(", 2026", "")).join(", ")}
        </p>
        <button type="button" className={BTN_SMALL} onClick={() => setDays([])}>
          Clear all
        </button>
      </div>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <OnCallPlanner />
    </div>
  );
}
''',
)


# 5. calendar-disabled-dates
register(
    "calendar-disabled-dates",
    title="Calendar — Disabled Dates",
    subcategory="Constraints",
    description="Individual disabled dates via a typed matcher: weekends plus a three-day maintenance blackout are unselectable, keyboard-skipped, and exposed as disabled — while the rest of the calendar stays fully interactive.",
    tags=TAGS_BASE + ["disabled", "matcher", "constraints"],
    features=FEAT_BASE + ["disabled date matcher", "keyboard skips disabled", "native disabled semantics"],
    accessibility=A11Y_BASE + ["disabled dates announced as unavailable"],
    interactive=True,
    related=["calendar-min-max", "calendar-range", "calendar-single"],
    usage='''const isClosed = (date: Date) =>
  date.getDay() === 0 || date.getDay() === 6 || isSameDay(date, new Date(2026, 7, 10));

<Calendar disabled={isClosed} defaultMonth={new Date(2026, 7, 1)}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="The `disabled` matcher receives each rendered local calendar date and returns whether it is unavailable. Disabled dates cannot be selected by any path — click, Enter/Space, keyboard focus, or range completion (a range that would cross one restarts instead). The matcher composes with `minDate` / `maxDate`.",
    keyboard_doc=None,
    a11y_doc="Disabled days are native `<button disabled>`: they are not focusable, not activatable, announced as unavailable, and arrow-key navigation steps over them automatically. They remain visible (muted text at 40% opacity), so the closure schedule stays readable. Only the matched dates are disabled — the calendar itself is untouched.",
    responsive_doc=None,
    notes_doc="A venue-booking demo: the venue is closed on weekends and for a maintenance blackout (Aug 10–12, 2026). The matcher uses the exported `isSameDay` for the specific dates. Note how `disabled` targets individual dates — for a continuous window of valid dates, prefer `minDate` / `maxDate` (`calendar-min-max`).",
    tsx_header="""/**
 * DevSnips React Calendar — disabled dates.
 *
 * The shared compound Calendar with a `disabled` matcher: individual dates
 * are unselectable, keyboard-skipped, and announced as unavailable.
 * Implementation identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function VenueBooking() {
  const [date, setDate] = React.useState(null);
  const isClosed = (d) => {
    if (d.getDay() === 0 || d.getDay() === 6) return true;
    return isSameDay(d, new Date(2026, 7, 10)) || isSameDay(d, new Date(2026, 7, 11)) || isSameDay(d, new Date(2026, 7, 12));
  };
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Venue</p>
        <p className={ROW_NAME}>Book the workshop room</p>
        <p className={NOTE}>Closed weekends, and Aug 10–12 for maintenance.</p>
      </div>
      <Calendar defaultMonth={AUG_2026} disabled={isClosed} selected={date} onSelect={setDate}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="disabled-readout" role="status">
        {date ? "Booked for " + fmtDay(date) + "." : "Select an open date."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <VenueBooking />
    </div>
  );
}
''',
)

# 6. calendar-min-max
register(
    "calendar-min-max",
    title="Calendar — Min / Max Dates",
    subcategory="Constraints",
    description="Inclusive minimum and maximum selectable dates: out-of-window days, impossible navigation, and out-of-range month/year picker options are all disabled, across same-month and cross-year windows.",
    tags=TAGS_BASE + ["minDate", "maxDate", "constraints", "booking-window"],
    features=FEAT_BASE + ["minDate / maxDate", "constrained navigation", "constrained pickers", "cross-year window"],
    accessibility=A11Y_BASE + ["boundary nav buttons announce + enforce limits"],
    interactive=True,
    related=["calendar-disabled-dates", "calendar-range", "calendar-month-picker"],
    usage='''<Calendar
  minDate={new Date(2026, 7, 5)}
  maxDate={new Date(2026, 7, 26)}
  defaultMonth={new Date(2026, 7, 1)}
>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="`minDate` and `maxDate` are inclusive calendar-day boundaries (time-of-day is ignored). Dates outside the window are disabled; the previous/next buttons disable when the target month, year, or 12-year page would hold no selectable day; the month and year pickers disable out-of-window options; and ranges cannot complete across the boundary. Selection can never bypass the window — every path goes through the same guard.",
    keyboard_doc=None,
    a11y_doc="Out-of-window days use native `disabled` and stay visible at reduced opacity, so the shape of the window is perceivable. Navigation buttons that cannot move are `disabled` with their accessible names intact ('Go to previous month'), so the constraint is announced rather than silent.",
    responsive_doc=None,
    notes_doc="Two demos: a booking window inside a single month (Aug 5–26, 2026 — both navigation directions disabled) and a cross-year window (Nov 20, 2026 – Feb 10, 2027 — next enabled across the year boundary, previous disabled). Keyboard PageUp/PageDown respects the same limits as the buttons.",
    tsx_header="""/**
 * DevSnips React Calendar — minimum / maximum dates.
 *
 * The shared compound Calendar constrained by `minDate` / `maxDate`:
 * out-of-window days, navigation, and picker options are all disabled.
 * Implementation identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function BookingWindow() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Reservations</p>
        <p className={ROW_NAME}>Book a table</p>
        <p className={NOTE}>This seating is open Aug 5 – Aug 26, 2026 only.</p>
      </div>
      <Calendar
        defaultMonth={AUG_2026}
        minDate={new Date(2026, 7, 5)}
        maxDate={new Date(2026, 7, 26)}
        selected={date}
        onSelect={setDate}
      >
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="minmax-readout" role="status">
        {date ? "Reserved for " + fmtDay(date) + "." : "Select a date inside the window."}
      </p>
    </div>
  );
}

function RolloutWindow() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Infrastructure</p>
        <p className={ROW_NAME}>Schedule the migration</p>
        <p className={NOTE}>The change window runs Nov 20, 2026 – Feb 10, 2027.</p>
      </div>
      <Calendar
        defaultMonth={new Date(2026, 10, 1)}
        minDate={new Date(2026, 10, 20)}
        maxDate={new Date(2027, 1, 10)}
        selected={date}
        onSelect={setDate}
      >
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="minmax-cross-readout" role="status">
        {date ? "Migration scheduled for " + fmtDay(date) + "." : "Select a date inside the window."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <BookingWindow />
      <RolloutWindow />
    </div>
  );
}
''',
)


# 7. calendar-week-numbers
register(
    "calendar-week-numbers",
    title="Calendar — Week Numbers",
    subcategory="Content",
    description="ISO-8601 week numbers in a leading, non-interactive rowheader column, paired with a Monday week start — the standard layout for sprint and capacity planning.",
    tags=TAGS_BASE + ["week numbers", "iso-8601", "monday-start"],
    features=FEAT_BASE + ["ISO week numbers", "weekStartsOn=1", "non-interactive week column"],
    accessibility=A11Y_BASE + ["week numbers as rowheaders, never selectable"],
    interactive=True,
    related=["calendar", "calendar-outside-days", "calendar-controlled"],
    usage='''<Calendar
  defaultMonth={new Date(2026, 7, 1)}
  weekStartsOn={1}
  showWeekNumbers
>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="Week numbers are display-only — they never participate in selection. The column adds no tab stops and no click targets; selection behavior is identical to the reference calendar.",
    keyboard_doc=None,
    a11y_doc="Week numbers render as `role=\"rowheader\"` cells (not buttons), and the corner cell is a `role=\"columnheader\"` labelled 'Week number'. The numbers are ISO 8601: weeks start Monday and week 1 contains the year's first Thursday, computed from each row's Thursday so the value is correct for any `weekStartsOn`.",
    responsive_doc="The week-number column adds one 36px cell per row (288px total) — still comfortably inside a 375px viewport.",
    notes_doc="A sprint-planning view: Monday start + ISO weeks. The week number of a row is computed from the row's Thursday (the ISO rule), so it stays correct regardless of the configured week start.",
    tsx_header="""/**
 * DevSnips React Calendar — ISO week numbers.
 *
 * The shared compound Calendar with `showWeekNumbers` + a Monday week
 * start: a non-interactive ISO-8601 week-number column. Implementation
 * identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function SprintPlanner() {
  const [day, setDay] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Planning</p>
        <p className={ROW_NAME}>Sprint 34 kickoff</p>
        <p className={NOTE}>Weeks are ISO 8601, Monday-first.</p>
      </div>
      <Calendar defaultMonth={AUG_2026} weekStartsOn={1} showWeekNumbers selected={day} onSelect={setDay}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="weeknum-readout" role="status">
        {day ? "Kickoff on " + fmtDay(day) + " (ISO week " + isoWeekNumber(day) + ")." : "Select the kickoff day."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <SprintPlanner />
    </div>
  );
}
''',
)

# 8. calendar-outside-days
register(
    "calendar-outside-days",
    title="Calendar — Outside Days",
    subcategory="Layout",
    description="Adjacent-month days rendered at the grid edges: muted but fully interactive, with their real month in the accessible name — selecting one pages the calendar to its month.",
    tags=TAGS_BASE + ["outside days", "grid", "layout"],
    features=FEAT_BASE + ["showOutsideDays", "edge-only rendering", "select-to-navigate"],
    accessibility=A11Y_BASE + ["outside days keep their real month in the label"],
    interactive=True,
    related=["calendar", "calendar-week-numbers", "calendar-range"],
    usage='''<Calendar defaultMonth={new Date(2026, 7, 1)} showOutsideDays>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="Outside days are fully selectable. Selecting one navigates the calendar to that day’s month and selects it there — the visible month follows the selection, so the state is never ambiguous. With `showOutsideDays` off (the default), the same cells render as empty gridcells, keeping the six-row grid stable without duplicate or dead focus targets.",
    keyboard_doc=None,
    a11y_doc="An outside day’s accessible name is its real date — the trailing cell in an August grid announces 'Tuesday, September 1, 2026', so it is never confused with an in-month day. With multiple months, outside days render only at the layout’s outer edges: interior cells would duplicate the neighbouring grid’s in-month buttons (double focus targets, duplicate accessible names), so they stay empty.",
    responsive_doc=None,
    notes_doc="With `numberOfMonths > 1`, outside days appear only before the first month and after the last — the interior boundary between two visible months is never duplicated.",
    tsx_header="""/**
 * DevSnips React Calendar — outside days.
 *
 * The shared compound Calendar with `showOutsideDays`: adjacent-month days
 * fill the grid edges, select-to-navigate, and never duplicate focus
 * targets across multi-month layouts. Implementation identical to the
 * reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function TimelinePicker() {
  const [date, setDate] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Editorial</p>
        <p className={ROW_NAME}>Pick a publish date</p>
        <p className={NOTE}>Faded days belong to the previous or next month — picking one jumps there.</p>
      </div>
      <Calendar defaultMonth={AUG_2026} showOutsideDays selected={date} onSelect={setDate}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="outside-readout" role="status">
        {date ? "Publishes " + fmtDay(date) + "." : "No publish date selected."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <TimelinePicker />
    </div>
  );
}
''',
)


# 9. calendar-month-picker
register(
    "calendar-month-picker",
    title="Calendar — Month Picker",
    subcategory="Navigation",
    description="The month-selection view: a 12-month grid opened from the heading (or seeded with defaultView), with year paging, min/max-aware options, and full keyboard navigation — choosing a month lands in its day grid.",
    tags=TAGS_BASE + ["month picker", "navigation", "view"],
    features=FEAT_BASE + ["months view", "defaultView", "year paging", "constrained options"],
    accessibility=A11Y_BASE + ['months view is a labelled role="grid"'],
    interactive=True,
    related=["calendar-year-picker", "calendar-controlled", "calendar-min-max"],
    usage='''// Open directly in the months view:
<Calendar defaultView="months" defaultMonth={new Date(2026, 7, 1)} onMonthChange={setMonth}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>

// …or from any calendar: activate the heading ("August 2026 — activate to
// choose a month") to switch the grid to the month picker.''',
    props_doc=PROPS_DOC,
    selection_doc="The months view is a navigation aid, not a separate selection granularity: choosing a month pages the calendar to that month and returns to the day grid, where the actual date selection happens. The currently displayed month is marked with `aria-selected`. Months outside `minDate` / `maxDate` are disabled.",
    keyboard_doc=None,
    a11y_doc="The months view is a `role=\"grid\"` labelled 'Choose a month in 2026' with a 3-column roving-tabindex layout. Every option's accessible name includes the year ('March 2026'), so the target is unambiguous. The heading stays `aria-live` and announces the year being browsed; the previous/next buttons announce 'Go to previous/next year'.",
    responsive_doc=None,
    notes_doc="The heading button cycles days → months → years. This variant simply starts in the months view (`defaultView=\"months\"`). PageUp/PageDown and the header chevrons page by year.",
    tsx_header="""/**
 * DevSnips React Calendar — month picker.
 *
 * The shared compound Calendar opened in the months view
 * (`defaultView="months"`): pick a month to page the day grid there.
 * Implementation identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function ReportPeriod() {
  const [viewing, setViewing] = React.useState(AUG_2026);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Analytics</p>
        <p className={ROW_NAME}>Reporting period</p>
        <p className={NOTE}>Choose a month to load its report, then pick the exact day.</p>
      </div>
      <Calendar defaultView="months" defaultMonth={AUG_2026} onMonthChange={setViewing}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="month-readout" role="status">
        {"Viewing " + fmtMonth(viewing) + "."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ReportPeriod />
    </div>
  );
}
''',
)

# 10. calendar-year-picker
register(
    "calendar-year-picker",
    title="Calendar — Year Picker",
    subcategory="Navigation",
    description="The year-selection view: a 12-year page grid with decade paging and min/max-aware options — choosing a year continues to the month picker, then the day grid.",
    tags=TAGS_BASE + ["year picker", "navigation", "view"],
    features=FEAT_BASE + ["years view", "12-year pages", "defaultView", "constrained options"],
    accessibility=A11Y_BASE + ['years view is a labelled role="grid"'],
    interactive=True,
    related=["calendar-month-picker", "calendar-controlled", "calendar-min-max"],
    usage='''// Open directly in the years view:
<Calendar defaultView="years" defaultMonth={new Date(2026, 7, 1)} onMonthChange={setMonth}>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>

// The heading cycles days → months → years; the years view pages in
// 12-year steps with the chevrons or PageUp / PageDown.''',
    props_doc=PROPS_DOC,
    selection_doc="The years view pages years in 12-year blocks aligned to the decade grid. Choosing a year continues to the month picker for that year (not directly to days), so the flow is year → month → day. Years outside `minDate` / `maxDate` are disabled; the chevrons disable when the adjacent page holds no selectable year.",
    keyboard_doc=None,
    a11y_doc="The years view is a `role=\"grid\"` labelled 'Choose a year' with the same roving-tabindex model as the day grid (arrows, Home/End for the page edges, PageUp/PageDown for 12-year jumps). The heading shows the page range (e.g. '2016 – 2027') and is announced via `aria-live` when it changes.",
    responsive_doc=None,
    notes_doc="Reaching the years view from a day grid takes two heading activations (days → months → years); this variant starts there directly. The flow back down is year → months → days, so a full jump from August 2026 to February 2024 is three picks.",
    tsx_header="""/**
 * DevSnips React Calendar — year picker.
 *
 * The shared compound Calendar opened in the years view
 * (`defaultView="years"`): 12-year pages with decade navigation, then on to
 * the month picker. Implementation identical to the reference
 * `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function ArchiveAccess() {
  const [viewing, setViewing] = React.useState(AUG_2026);
  return (
    <div className={CARD + " w-full max-w-sm space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Audit log</p>
        <p className={ROW_NAME}>Jump to an archive year</p>
        <p className={NOTE}>Pick a year, then a month, then the exact day.</p>
      </div>
      <Calendar defaultView="years" defaultMonth={AUG_2026} onMonthChange={setViewing}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <p className={NOTE} id="year-readout" role="status">
        {"Viewing " + fmtMonth(viewing) + "."}
      </p>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ArchiveAccess />
    </div>
  );
}
''',
)


# 11. calendar-with-footer
register(
    "calendar-with-footer",
    title="Calendar — Footer Actions",
    subcategory="Composite",
    description="A calendar with a footer region: a live selected-date summary plus explicit Clear and Today actions, composed with CalendarFooter and the useCalendar hook.",
    tags=TAGS_BASE + ["footer", "actions", "today", "clear"],
    features=FEAT_BASE + ["CalendarFooter", "useCalendar composition", "explicit Today action"],
    accessibility=A11Y_BASE + ["footer summary via role=status"],
    interactive=True,
    related=["calendar-single", "calendar-controlled", "calendar"],
    usage='''function FooterActions() {
  const { goToMonth, selectDate, clearSelection } = useCalendar();
  return (
    <CalendarFooter>
      <span>{selected ? format(selected) : "No date selected"}</span>
      <span className="flex gap-2">
        <button onClick={clearSelection}>Clear</button>
        <button onClick={() => { const t = new Date(); goToMonth(t); selectDate(t); }}>
          Today
        </button>
      </span>
    </CalendarFooter>
  );
}

<Calendar selected={selected} onSelect={setSelected}>
  <CalendarHeader>…</CalendarHeader>
  <CalendarGrid />
  <FooterActions />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="The footer actions are explicit: **Today** navigates to and selects the current local date (the calendar never auto-selects today on its own), and **Clear** empties the selection via the parent's controlled state. Both are ordinary buttons with immediate effect — selection still only happens through the same guarded path.",
    keyboard_doc=None,
    a11y_doc="The summary is a `role=status` region, so footer actions announce their result ('No date selected' → the chosen date). `useCalendar()` gives composed children access to `selectDate` / `clearSelection` / `goToMonth` without prop drilling, and the actions are real buttons in the normal tab order.",
    responsive_doc=None,
    notes_doc="Shows the composition escape hatch: `CalendarFooter` is a plain region, and any child can drive the calendar through `useCalendar()`. Today is an explicit user action here — the calendar itself never assumes the current date is the desired selection.",
    tsx_header="""/**
 * DevSnips React Calendar — footer actions.
 *
 * The shared compound Calendar with a `CalendarFooter`: a selected-date
 * summary plus explicit Clear / Today actions driven by `useCalendar()`.
 * Implementation identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function FooterActions({ selected, onClear }) {
  const cal = useCalendar();
  return (
    <CalendarFooter>
      <span id="footer-readout" role="status">
        {selected ? fmtDay(selected) : "No date selected"}
      </span>
      <span className="flex items-center gap-2">
        <button type="button" className={BTN_SMALL} onClick={onClear}>
          Clear
        </button>
        <button
          type="button"
          className={BTN_SMALL}
          onClick={() => {
            const t = new Date();
            cal.goToMonth(t);
            cal.selectDate(t);
          }}
        >
          Today
        </button>
      </span>
    </CalendarFooter>
  );
}

function AppointmentCard() {
  const [selected, setSelected] = React.useState(null);
  return (
    <div className={CARD + " w-full max-w-sm space-y-1"}>
      <div className="space-y-1 pb-3">
        <p className={LABEL}>Front desk</p>
        <p className={ROW_NAME}>Book an appointment</p>
      </div>
      <Calendar defaultMonth={AUG_2026} selected={selected} onSelect={setSelected}>
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
        <FooterActions selected={selected} onClear={() => setSelected(null)} />
      </Calendar>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <AppointmentCard />
    </div>
  );
}
''',
)

# 12. calendar-controlled
register(
    "calendar-controlled",
    title="Calendar — Controlled State",
    subcategory="State",
    description="A fully parent-controlled calendar: the visible month, the selected date, and even the locale live in parent state, with external month/year/locale selectors and an event log of every callback.",
    tags=TAGS_BASE + ["controlled", "month", "locale", "state"],
    features=FEAT_BASE + ["controlled month + selection", "external month/year jump", "locale switching", "callback log"],
    accessibility=A11Y_BASE + ["locale-aware labels switch live"],
    interactive=True,
    related=["calendar-single", "calendar-month-picker", "calendar-year-picker"],
    usage='''const [month, setMonth] = useState(new Date(2026, 7, 1));
const [selected, setSelected] = useState<Date | null>(null);
const [locale, setLocale] = useState("en-US");

<Calendar
  month={month}
  onMonthChange={setMonth}
  selected={selected}
  onSelect={setSelected}
  locale={locale}
>
  <CalendarHeader>
    <CalendarPrevious />
    <CalendarHeading className="flex-1 text-center" />
    <CalendarNext />
  </CalendarHeader>
  <CalendarGrid />
</Calendar>''',
    props_doc=PROPS_DOC,
    selection_doc="With `month` + `selected` both controlled, the calendar is a pure function of props: every internal navigation or selection request flows out through `onMonthChange` / `onSelect`, and the parent decides the new state. Uncontrolled pieces (the picker view, the roving focus) stay internal.",
    keyboard_doc=None,
    a11y_doc="The month, year, and locale selectors are real labelled `<select>` elements outside the calendar — the calendar itself keeps its full grid semantics. Switching locale re-renders every month name, weekday header, and day accessible name through `Intl.DateTimeFormat`; the `aria-live` heading announces the new label.",
    responsive_doc=None,
    notes_doc="The control-panel pattern: external month/year selects can jump the calendar anywhere (e.g. February 2024 to inspect a leap month), and the calendar's own navigation stays consistent because it reports through the same callbacks. The locale switcher demonstrates that no month or weekday name is hardcoded.",
    tsx_header="""/**
 * DevSnips React Calendar — controlled state.
 *
 * The shared compound Calendar with parent-owned month, selection, and
 * locale: every change flows through `onMonthChange` / `onSelect`.
 * Implementation identical to the reference `calendar/code.tsx`.
 */""",
    showcase=DEMO_HELPERS + '''
function ControlledDemo() {
  const [month, setMonth] = React.useState(new Date(2026, 7, 1));
  const [selected, setSelected] = React.useState(new Date(2026, 7, 14));
  const [locale, setLocale] = React.useState("en-US");
  const [log, setLog] = React.useState([]);
  const addLog = (entry) => setLog((prev) => [entry, ...prev].slice(0, 4));
  const years = [2024, 2025, 2026, 2027, 2028];
  const monthOptions = Array.from({ length: 12 }, (_, i) =>
    new Intl.DateTimeFormat(locale, { month: "long" }).format(new Date(2024, i, 1))
  );
  return (
    <div className={CARD + " w-full max-w-md space-y-4"}>
      <div className="space-y-1">
        <p className={LABEL}>Scheduling console</p>
        <p className={ROW_NAME}>Fully controlled calendar</p>
        <p className={NOTE}>Month, selection, and locale are owned by the parent.</p>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <label className="sr-only" htmlFor="ctl-month">Month</label>
        <select
          id="ctl-month"
          className={SELECT}
          value={month.getMonth()}
          onChange={(e) => setMonth(new Date(month.getFullYear(), Number(e.target.value), 1))}
        >
          {monthOptions.map((name, i) => (
            <option key={i} value={i}>{name}</option>
          ))}
        </select>
        <label className="sr-only" htmlFor="ctl-year">Year</label>
        <select
          id="ctl-year"
          className={SELECT}
          value={month.getFullYear()}
          onChange={(e) => setMonth(new Date(Number(e.target.value), month.getMonth(), 1))}
        >
          {years.map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
        <label className="sr-only" htmlFor="ctl-locale">Locale</label>
        <select id="ctl-locale" className={SELECT} value={locale} onChange={(e) => setLocale(e.target.value)}>
          <option value="en-US">en-US</option>
          <option value="fr-FR">fr-FR</option>
          <option value="de-DE">de-DE</option>
          <option value="ja-JP">ja-JP</option>
        </select>
      </div>
      <Calendar
        month={month}
        onMonthChange={(m) => { setMonth(m); addLog("month → " + fmtMonth(m)); }}
        selected={selected}
        onSelect={(d) => { setSelected(d); addLog("select → " + (d ? fmtDay(d) : "cleared")); }}
        locale={locale}
      >
        <CalendarChrome>
          <CalendarGrid />
        </CalendarChrome>
      </Calendar>
      <div className="flex items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-3">
        <p className={NOTE} id="controlled-readout" role="status">
          {selected ? "Selected: " + fmtDay(selected) : "Nothing selected."}
        </p>
        <button type="button" className={BTN_SMALL} onClick={() => setMonth(new Date(2024, 1, 1))}>
          Jump to Feb 2024
        </button>
      </div>
      <ul className="m-0 list-none space-y-1 p-0 font-mono text-[11px] leading-4 text-[var(--ds-color-muted-foreground)]" id="controlled-log">
        {log.length === 0 ? <li>No events yet.</li> : log.map((entry, i) => <li key={i}>{entry}</li>)}
      </ul>
    </div>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-6">
      <ControlledDemo />
    </div>
  );
}
''',
)
