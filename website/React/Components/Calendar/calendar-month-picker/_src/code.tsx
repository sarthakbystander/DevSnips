import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type {
  HTMLAttributes,
  KeyboardEvent as ReactKeyboardEvent,
  ReactElement,
  ReactNode,
} from "react";

/**
 * DevSnips React Calendar — month picker.
 *
 * The shared compound Calendar opened in the months view
 * (`defaultView="months"`): pick a month to page the day grid there.
 * Implementation identical to the reference `calendar/code.tsx`.
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/* ------------------------------------------------------------------------ */
/* Date utilities — local calendar-date semantics                           */
/* ------------------------------------------------------------------------ */

export type WeekDay = 0 | 1 | 2 | 3 | 4 | 5 | 6;

const WEEK_MS = 604800000;

/** Days in a (year, month); `month` is 0-based. Handles leap years. */
export function daysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate();
}

/** Whether a Gregorian year is a leap year. */
export function isLeapYear(year: number): boolean {
  return new Date(year, 1, 29).getMonth() === 1;
}

/**
 * Numeric identity of a local calendar date:
 * `year * 10000 + (month + 1) * 100 + day`. Strictly monotonic with calendar
 * order, so keys compare directly — no string comparison and no timestamp
 * comparison (both break across DST / UTC boundaries).
 */
function dayKey(date: Date): number {
  return date.getFullYear() * 10000 + (date.getMonth() + 1) * 100 + date.getDate();
}

/** Rebuild a local calendar date from its `dayKey`. */
function dateFromKey(key: number): Date {
  const year = Math.floor(key / 10000);
  const month = Math.floor((key % 10000) / 100) - 1;
  return new Date(year, month, key % 100);
}

/** -1 / 0 / 1 comparison by calendar day; time-of-day is ignored. */
export function compareDays(a: Date, b: Date): number {
  const diff = dayKey(a) - dayKey(b);
  return diff === 0 ? 0 : diff < 0 ? -1 : 1;
}

/** Whether two Dates fall on the same local calendar day. */
export function isSameDay(a: Date, b: Date): boolean {
  return dayKey(a) === dayKey(b);
}

/**
 * Add calendar days using local constructor arithmetic. This is DST-safe:
 * `new Date(y, m, d + n)` normalizes month/year overflow itself, unlike
 * timestamp math (`date.getTime() + n * 86400000`), which skips or repeats
 * an hour across DST transitions and can shift the calendar day.
 */
export function addDays(date: Date, amount: number): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + amount);
}

/**
 * Add calendar months, clamping the day-of-month to the target month
 * (`Jan 31 + 1 month` lands on `Feb 28/29`, not `Mar 2/3`). Handles
 * December ↔ January year rollover via constructor normalization.
 */
export function addMonths(date: Date, amount: number): Date {
  const first = new Date(date.getFullYear(), date.getMonth() + amount, 1);
  const day = Math.min(date.getDate(), daysInMonth(first.getFullYear(), first.getMonth()));
  return new Date(first.getFullYear(), first.getMonth(), day);
}

/** The first day of the month containing `date`. */
export function startOfMonth(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

/** The last day of the month containing `date`. */
export function endOfMonth(date: Date): Date {
  const year = date.getFullYear();
  const month = date.getMonth();
  return new Date(year, month, daysInMonth(year, month));
}

/**
 * ISO-8601 week number (weeks start Monday; week 1 contains the year's
 * first Thursday). Computed on local-noon copies so the Thursday shift is
 * never affected by a midnight DST transition.
 */
export function isoWeekNumber(date: Date): number {
  const noon = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 12);
  const thursday = addDays(noon, 3 - ((noon.getDay() + 6) % 7));
  const jan4 = new Date(thursday.getFullYear(), 0, 4, 12);
  const weekOneThursday = addDays(jan4, 3 - ((jan4.getDay() + 6) % 7));
  return 1 + Math.round((thursday.getTime() - weekOneThursday.getTime()) / WEEK_MS);
}

/**
 * The 6 × 7 day matrix covering `month`, aligned to `weekStartsOn`.
 * Always exactly six rows so the grid never changes height between months.
 * Leading / trailing cells hold adjacent-month dates.
 */
export function buildMonthWeeks(month: Date, weekStartsOn: WeekDay): Date[][] {
  const first = startOfMonth(month);
  const leading = (first.getDay() - weekStartsOn + 7) % 7;
  const gridStart = addDays(first, -leading);
  const weeks: Date[][] = [];
  for (let w = 0; w < 6; w += 1) {
    const row: Date[] = [];
    for (let d = 0; d < 7; d += 1) row.push(addDays(gridStart, w * 7 + d));
    weeks.push(row);
  }
  return weeks;
}

/* ------------------------------------------------------------------------ */
/* Locale-aware formatting (Intl — no hardcoded month / weekday names)      */
/* ------------------------------------------------------------------------ */

function monthYearLabel(date: Date, locale: string): string {
  return new Intl.DateTimeFormat(locale, { month: "long", year: "numeric" }).format(date);
}

function monthName(date: Date, locale: string): string {
  return new Intl.DateTimeFormat(locale, { month: "long" }).format(date);
}

function yearLabel(year: number, locale: string): string {
  return new Intl.DateTimeFormat(locale, { year: "numeric" }).format(new Date(year, 0, 1));
}

function fullDateLabel(date: Date, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
}

function monthNames(locale: string): string[] {
  const fmt = new Intl.DateTimeFormat(locale, { month: "long" });
  return Array.from({ length: 12 }, (_, m) => fmt.format(new Date(2024, m, 1)));
}

/** Short + long weekday names in grid order for a given week start. */
function weekdayNames(locale: string, weekStartsOn: WeekDay): Array<{ short: string; long: string }> {
  // 2024-01-07 was a Sunday — a fixed reference week, independent of today.
  const base = new Date(2024, 0, 7);
  const shortFmt = new Intl.DateTimeFormat(locale, { weekday: "short" });
  const longFmt = new Intl.DateTimeFormat(locale, { weekday: "long" });
  return Array.from({ length: 7 }, (_, i) => {
    const day = addDays(base, (weekStartsOn + i) % 7);
    return { short: shortFmt.format(day), long: longFmt.format(day) };
  });
}

/* ------------------------------------------------------------------------ */
/* Public types                                                             */
/* ------------------------------------------------------------------------ */

export interface DateRange {
  from: Date;
  to: Date | null;
}

export type CalendarMode = "single" | "multiple" | "range";
export type CalendarView = "days" | "months" | "years";

export interface CalendarBaseProps {
  /** Visible month (controlled). Any Date inside the month; normalized to the 1st. */
  month?: Date;
  /** Initial visible month (uncontrolled). Defaults to the month of the initial selection, else today. */
  defaultMonth?: Date;
  /** Called whenever the visible month changes (navigation, keyboard, outside-day click, picker selection). */
  onMonthChange?: (month: Date) => void;
  /** Initial picker view. The heading button cycles days → months → years. */
  defaultView?: CalendarView;
  /** Earliest selectable date (inclusive). Earlier dates and earlier navigation are disabled. */
  minDate?: Date;
  /** Latest selectable date (inclusive). Later dates and later navigation are disabled. */
  maxDate?: Date;
  /** Matcher for individual disabled dates; combined with `minDate` / `maxDate`. */
  disabled?: (date: Date) => boolean;
  /** BCP-47 locale tag for month / weekday / day labels. Default `"en-US"`. */
  locale?: string;
  /** First weekday column: 0 = Sunday … 6 = Saturday. Default 0. */
  weekStartsOn?: WeekDay;
  /** Render adjacent-month days at the grid edges (they select + navigate on click). Default false. */
  showOutsideDays?: boolean;
  /** Render a leading ISO-8601 week-number column (non-interactive). Default false. */
  showWeekNumbers?: boolean;
  /** Number of consecutive month grids. Render one `<CalendarGrid monthOffset={i}>` per month. Default 1. */
  numberOfMonths?: number;
  className?: string;
  children?: ReactNode;
}

export interface CalendarSingleSelectionProps {
  mode?: "single";
  selected?: Date | null;
  defaultSelected?: Date | null;
  onSelect?: (date: Date | null) => void;
}

export interface CalendarMultipleSelectionProps {
  mode: "multiple";
  selected?: Date[];
  defaultSelected?: Date[];
  onSelect?: (dates: Date[]) => void;
}

export interface CalendarRangeSelectionProps {
  mode: "range";
  selected?: DateRange | null;
  defaultSelected?: DateRange | null;
  onSelect?: (range: DateRange | null) => void;
}

export type CalendarProps = CalendarBaseProps &
  (CalendarSingleSelectionProps | CalendarMultipleSelectionProps | CalendarRangeSelectionProps);

/* ------------------------------------------------------------------------ */
/* Controlled / uncontrolled state                                          */
/* ------------------------------------------------------------------------ */

function useControllableState<T>(
  controlled: T | undefined,
  defaultValue: T,
  onChange: ((value: T) => void) | undefined,
): [T, (value: T) => void] {
  const [internal, setInternal] = useState<T>(defaultValue);
  const isControlled = controlled !== undefined;
  const value = isControlled ? (controlled as T) : internal;
  const set = useCallback(
    (next: T) => {
      if (!isControlled) setInternal(next);
      if (onChange) onChange(next);
    },
    [isControlled, onChange],
  );
  return [value, set];
}

/* ------------------------------------------------------------------------ */
/* Context                                                                  */
/* ------------------------------------------------------------------------ */

export interface CalendarContextValue {
  mode: CalendarMode;
  locale: string;
  weekStartsOn: WeekDay;
  showOutsideDays: boolean;
  showWeekNumbers: boolean;
  numberOfMonths: number;
  view: CalendarView;
  setView: (view: CalendarView) => void;
  /** First visible month (normalized to its 1st day). */
  month: Date;
  today: Date;
  headingLabel: string;
  goToMonth: (month: Date) => void;
  goToPrevious: () => void;
  goToNext: () => void;
  canGoPrevious: boolean;
  canGoNext: boolean;
  previousLabel: string;
  nextLabel: string;
  isDisabled: (date: Date) => boolean;
  isSelected: (date: Date) => boolean;
  isRangeStart: (date: Date) => boolean;
  isRangeEnd: (date: Date) => boolean;
  isRangeMiddle: (date: Date) => boolean;
  selectDate: (date: Date) => void;
  clearSelection: () => void;
  handleDayClick: (date: Date, outside: boolean) => void;
  handleDayKeyDown: (event: ReactKeyboardEvent<HTMLButtonElement>, date: Date) => void;
  tabbableDayKey: number | null;
  monthEnabled: (year: number, monthIndex: number) => boolean;
  yearEnabled: (year: number) => boolean;
  monthActiveKey: string | null;
  yearActiveKey: string | null;
  yearPage: number[];
  selectMonth: (monthIndex: number) => void;
  selectYear: (year: number) => void;
  handleMonthKeyDown: (event: ReactKeyboardEvent<HTMLButtonElement>, monthIndex: number) => void;
  handleYearKeyDown: (event: ReactKeyboardEvent<HTMLButtonElement>, year: number) => void;
  focusKey: string | null;
  setFocusKey: (key: string) => void;
}

const CalendarContext = createContext<CalendarContextValue | null>(null);

/** Access the nearest `<Calendar>` context (for composed children such as footer actions). */
export function useCalendar(): CalendarContextValue {
  const ctx = useContext(CalendarContext);
  if (!ctx) throw new Error("Calendar components must be composed inside <Calendar>.");
  return ctx;
}

/* ------------------------------------------------------------------------ */
/* Shared class constants (token-driven)                                    */
/* ------------------------------------------------------------------------ */

const ROOT_CLASSES =
  "w-max max-w-full rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-3 shadow-[var(--ds-shadow-xs)]";
const HEADER_CLASSES = "mb-1 flex items-center justify-between gap-1";
const NAV_BUTTON_CLASSES =
  "inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const HEADING_CLASSES = "m-0 text-sm font-semibold leading-9 text-[var(--ds-color-foreground)]";
const HEADING_BUTTON_CLASSES =
  "-mx-1.5 rounded-[var(--ds-radius-sm)] px-1.5 transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const WEEKDAY_CLASSES =
  "flex size-9 items-center justify-center text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const WEEKNUM_CLASSES =
  "flex size-9 items-center justify-center font-mono text-[11px] tabular-nums text-[var(--ds-color-muted-foreground)]";
const DAY_CLASSES =
  "inline-flex size-9 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent text-sm leading-5 tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none";
const PICKER_BUTTON_CLASSES =
  "flex h-9 flex-1 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent px-2 text-sm leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none";
const FOOTER_CLASSES =
  "mt-2 flex items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-2 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";

const SELECTED_DAY_CLASSES =
  "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)]";
const RANGE_MIDDLE_CLASSES = "rounded-none bg-[var(--ds-color-surface-active)] text-[var(--ds-color-foreground)]";
const PICKER_SELECTED_CLASSES = "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)]";

/* ------------------------------------------------------------------------ */
/* Icons (inline SVG — consistent stroke with the DevSnips icon set)        */
/* ------------------------------------------------------------------------ */

function ChevronLeftIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <path d="m15 18-6-6 6-6" />
    </svg>
  );
}

function ChevronRightIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <path d="m9 18 6-6-6-6" />
    </svg>
  );
}

/* ------------------------------------------------------------------------ */
/* Root                                                                     */
/* ------------------------------------------------------------------------ */

export function Calendar(props: CalendarProps): ReactElement {
  const {
    month: controlledMonth,
    defaultMonth,
    onMonthChange,
    defaultView = "days",
    minDate,
    maxDate,
    disabled,
    locale = "en-US",
    weekStartsOn = 0,
    showOutsideDays = false,
    showWeekNumbers = false,
    numberOfMonths = 1,
    className,
    children,
    // Selection props are consumed through the typed slices below — they are
    // destructured here so they never leak onto the DOM via `...rest`
    // (`onSelect` also collides with the native React event handler).
    mode: _mode,
    selected: _selected,
    defaultSelected: _defaultSelected,
    onSelect: _onSelect,
    ...rest
  } = props;
  const mode: CalendarMode = _mode ?? "single";

  // The discriminated union guarantees each selection slice matches `mode`;
  // the casts re-associate the union member with its own props. A slice is
  // only ever read or written when `mode` selects it — the other two stay
  // dormant for the life of the component.
  const singleSlice = props as CalendarBaseProps & CalendarSingleSelectionProps;
  const multipleSlice = props as CalendarBaseProps & CalendarMultipleSelectionProps;
  const rangeSlice = props as CalendarBaseProps & CalendarRangeSelectionProps;

  const [singleSelection, setSingleSelection] = useControllableState<Date | null>(
    mode === "single" ? singleSlice.selected : undefined,
    (mode === "single" ? singleSlice.defaultSelected : null) ?? null,
    mode === "single" ? singleSlice.onSelect : undefined,
  );
  const [multipleSelection, setMultipleSelection] = useControllableState<Date[]>(
    mode === "multiple" ? multipleSlice.selected : undefined,
    (mode === "multiple" ? multipleSlice.defaultSelected : undefined) ?? [],
    mode === "multiple" ? multipleSlice.onSelect : undefined,
  );
  const [rangeSelection, setRangeSelection] = useControllableState<DateRange | null>(
    mode === "range" ? rangeSlice.selected : undefined,
    (mode === "range" ? rangeSlice.defaultSelected : undefined) ?? null,
    mode === "range" ? rangeSlice.onSelect : undefined,
  );

  const [today] = useState(() => new Date());

  const firstSelected =
    mode === "single"
      ? singleSelection
      : mode === "multiple"
        ? (multipleSelection[0] ?? null)
        : (rangeSelection?.from ?? null);

  // Visible month — controlled (`month`) or uncontrolled (`defaultMonth`).
  // Normalized to the 1st; the numeric key stabilizes the memo below across
  // fresh Date identities from a controlled parent.
  const [monthState, setMonthState] = useControllableState<Date>(
    controlledMonth !== undefined ? startOfMonth(controlledMonth) : undefined,
    startOfMonth(defaultMonth ?? firstSelected ?? today),
    onMonthChange,
  );
  const monthKey = monthState.getFullYear() * 12 + monthState.getMonth();
  const month = useMemo(() => startOfMonth(monthState), [monthKey]); // eslint-disable-line react-hooks/exhaustive-deps

  const [view, setView] = useState<CalendarView>(defaultView);
  const [focusKey, setFocusKey] = useState<string | null>(null);
  const focusIntentRef = useRef(false);
  const rootRef = useRef<HTMLDivElement>(null);

  /* ----- constraints ----------------------------------------------------- */

  const isDisabled = useCallback(
    (date: Date): boolean => {
      if (minDate && compareDays(date, minDate) < 0) return true;
      if (maxDate && compareDays(date, maxDate) > 0) return true;
      return disabled ? disabled(date) : false;
    },
    [minDate, maxDate, disabled],
  );

  const monthEnabled = useCallback(
    (year: number, monthIndex: number): boolean => {
      if (minDate && compareDays(endOfMonth(new Date(year, monthIndex, 1)), minDate) < 0) return false;
      if (maxDate && compareDays(new Date(year, monthIndex, 1), maxDate) > 0) return false;
      return true;
    },
    [minDate, maxDate],
  );

  const yearEnabled = useCallback(
    (year: number): boolean => {
      if (minDate && compareDays(new Date(year, 11, 31), minDate) < 0) return false;
      if (maxDate && compareDays(new Date(year, 0, 1), maxDate) > 0) return false;
      return true;
    },
    [minDate, maxDate],
  );

  /* ----- visible range ---------------------------------------------------- */

  const lastVisibleMonth = useMemo(
    () => startOfMonth(addMonths(month, numberOfMonths - 1)),
    [month, numberOfMonths],
  );

  // Range of day cells actually rendered (in-month cells of every visible
  // month, plus the edge outside cells when `showOutsideDays` is on). The
  // range is continuous — interior outside cells of multi-month layouts are
  // not rendered (they would duplicate the neighbouring grid's in-month
  // cells), but every date in between exists as an in-month cell.
  const [renderedStart, renderedEnd] = useMemo((): [Date, Date] => {
    if (!showOutsideDays) return [month, endOfMonth(lastVisibleMonth)];
    const firstWeeks = buildMonthWeeks(month, weekStartsOn);
    const lastWeeks = buildMonthWeeks(lastVisibleMonth, weekStartsOn);
    const start = firstWeeks[0]?.[0] ?? month;
    const end = lastWeeks[lastWeeks.length - 1]?.[6] ?? endOfMonth(lastVisibleMonth);
    return [start, end];
  }, [month, lastVisibleMonth, weekStartsOn, showOutsideDays]);

  const isRenderedDate = useCallback(
    (date: Date): boolean =>
      compareDays(date, renderedStart) >= 0 && compareDays(date, renderedEnd) <= 0,
    [renderedStart, renderedEnd],
  );

  const goToMonth = useCallback(
    (target: Date) => {
      let t = startOfMonth(target);
      if (maxDate) {
        const latest = startOfMonth(addMonths(maxDate, -(numberOfMonths - 1)));
        if (compareDays(t, latest) > 0) t = latest;
      }
      if (minDate && compareDays(t, startOfMonth(minDate)) < 0) t = startOfMonth(minDate);
      setMonthState(t);
    },
    [minDate, maxDate, numberOfMonths, setMonthState],
  );

  /** The first visible month that reveals `date` (unchanged when already visible). */
  const monthToReveal = useCallback(
    (date: Date): Date => {
      if (compareDays(date, month) < 0) return startOfMonth(date);
      if (compareDays(date, endOfMonth(lastVisibleMonth)) > 0) {
        return startOfMonth(addMonths(date, -(numberOfMonths - 1)));
      }
      return month;
    },
    [month, lastVisibleMonth, numberOfMonths],
  );

  /* ----- navigation ------------------------------------------------------- */

  const navStep = view === "days" ? 1 : view === "months" ? 12 : 144;
  let canGoPrevious = true;
  let canGoNext = true;
  if (view === "days") {
    canGoPrevious = !minDate || compareDays(endOfMonth(addMonths(month, -1)), minDate) >= 0;
    canGoNext = !maxDate || compareDays(startOfMonth(addMonths(month, numberOfMonths)), maxDate) <= 0;
  } else if (view === "months") {
    const y = month.getFullYear();
    canGoPrevious = !minDate || compareDays(new Date(y - 1, 11, 31), minDate) >= 0;
    canGoNext = !maxDate || compareDays(new Date(y + 1, 0, 1), maxDate) <= 0;
  } else {
    const pageStart = Math.floor(month.getFullYear() / 12) * 12;
    canGoPrevious = !minDate || compareDays(new Date(pageStart - 1, 11, 31), minDate) >= 0;
    canGoNext = !maxDate || compareDays(new Date(pageStart + 12, 0, 1), maxDate) <= 0;
  }
  const goToPrevious = useCallback(() => {
    if (canGoPrevious) goToMonth(addMonths(month, -navStep));
  }, [canGoPrevious, goToMonth, month, navStep]);
  const goToNext = useCallback(() => {
    if (canGoNext) goToMonth(addMonths(month, navStep));
  }, [canGoNext, goToMonth, month, navStep]);

  const previousLabel =
    view === "days" ? "Go to previous month" : view === "months" ? "Go to previous year" : "Go to previous 12 years";
  const nextLabel =
    view === "days" ? "Go to next month" : view === "months" ? "Go to next year" : "Go to next 12 years";

  const headingLabel = useMemo(() => {
    if (view === "months") return yearLabel(month.getFullYear(), locale);
    if (view === "years") {
      const pageStart = Math.floor(month.getFullYear() / 12) * 12;
      return `${yearLabel(pageStart, locale)} – ${yearLabel(pageStart + 11, locale)}`;
    }
    if (numberOfMonths === 1) return monthYearLabel(month, locale);
    const last = addMonths(month, numberOfMonths - 1);
    if (month.getFullYear() === last.getFullYear()) {
      return `${monthName(month, locale)} – ${monthYearLabel(last, locale)}`;
    }
    return `${monthYearLabel(month, locale)} – ${monthYearLabel(last, locale)}`;
  }, [view, month, numberOfMonths, locale]);

  const yearPage = useMemo(() => {
    const pageStart = Math.floor(month.getFullYear() / 12) * 12;
    return Array.from({ length: 12 }, (_, i) => pageStart + i);
  }, [month]);

  /* ----- selection -------------------------------------------------------- */

  // A range may never silently cross a disabled date (disabled includes the
  // min/max boundaries). Checked on completion; endpoints themselves can
  // never be disabled because disabled day buttons cannot be activated.
  const rangeCrossesDisabled = useCallback(
    (from: Date, to: Date): boolean => {
      let cursor = addDays(from, 1);
      for (let i = 0; i < 3700 && compareDays(cursor, to) < 0; i += 1) {
        if (isDisabled(cursor)) return true;
        cursor = addDays(cursor, 1);
      }
      return false;
    },
    [isDisabled],
  );

  const selectDate = useCallback(
    (date: Date) => {
      if (isDisabled(date)) return;
      if (mode === "single") {
        // Clicking the selected day is a no-op — never an accidental deselect.
        if (singleSelection && isSameDay(singleSelection, date)) return;
        setSingleSelection(date);
        return;
      }
      if (mode === "multiple") {
        const exists = multipleSelection.some((d) => isSameDay(d, date));
        // Immutable updates — caller-owned arrays are never mutated.
        setMultipleSelection(
          exists ? multipleSelection.filter((d) => !isSameDay(d, date)) : [...multipleSelection, date],
        );
        return;
      }
      // range
      if (!rangeSelection || rangeSelection.to) {
        setRangeSelection({ from: date, to: null });
        return;
      }
      const from = rangeSelection.from;
      if (isSameDay(date, from)) {
        setRangeSelection({ from, to: from });
      } else if (compareDays(date, from) < 0 || rangeCrossesDisabled(from, date)) {
        // Earlier-than-start or crossing a disabled day: restart, predictably.
        setRangeSelection({ from: date, to: null });
      } else {
        setRangeSelection({ from, to: date });
      }
    },
    [
      isDisabled,
      mode,
      singleSelection,
      multipleSelection,
      rangeSelection,
      setSingleSelection,
      setMultipleSelection,
      setRangeSelection,
      rangeCrossesDisabled,
    ],
  );

  const clearSelection = useCallback(() => {
    if (mode === "single") setSingleSelection(null);
    else if (mode === "multiple") setMultipleSelection([]);
    else setRangeSelection(null);
  }, [mode, setSingleSelection, setMultipleSelection, setRangeSelection]);

  const isRangeStart = useCallback(
    (date: Date) =>
      mode === "range" &&
      rangeSelection !== null &&
      rangeSelection.to !== null &&
      !isSameDay(rangeSelection.from, rangeSelection.to) &&
      isSameDay(rangeSelection.from, date),
    [mode, rangeSelection],
  );
  const isRangeEnd = useCallback(
    (date: Date) =>
      mode === "range" &&
      rangeSelection !== null &&
      rangeSelection.to !== null &&
      !isSameDay(rangeSelection.from, rangeSelection.to) &&
      isSameDay(rangeSelection.to, date),
    [mode, rangeSelection],
  );
  const isRangeMiddle = useCallback(
    (date: Date) =>
      mode === "range" &&
      rangeSelection !== null &&
      rangeSelection.to !== null &&
      compareDays(date, rangeSelection.from) > 0 &&
      compareDays(date, rangeSelection.to) < 0,
    [mode, rangeSelection],
  );
  const isSelected = useCallback(
    (date: Date): boolean => {
      if (mode === "single") return singleSelection !== null && isSameDay(singleSelection, date);
      if (mode === "multiple") return multipleSelection.some((d) => isSameDay(d, date));
      return (
        rangeSelection !== null &&
        (isSameDay(rangeSelection.from, date) ||
          (rangeSelection.to !== null &&
            compareDays(date, rangeSelection.from) > 0 &&
            compareDays(date, rangeSelection.to) <= 0))
      );
    },
    [mode, singleSelection, multipleSelection, rangeSelection],
  );

  /* ----- focus model (roving tabindex) ------------------------------------ */

  const focusedDay = useMemo((): Date | null => {
    if (focusKey && /^\d{8}$/.test(focusKey)) return dateFromKey(Number(focusKey));
    return null;
  }, [focusKey]);

  const tabbableDayKey = useMemo((): number | null => {
    const candidates: Array<Date | null> = [focusedDay, firstSelected, today];
    for (const candidate of candidates) {
      if (candidate && isRenderedDate(candidate) && !isDisabled(candidate)) return dayKey(candidate);
    }
    for (let i = 0; i < numberOfMonths; i += 1) {
      const gridMonth = startOfMonth(addMonths(month, i));
      const count = daysInMonth(gridMonth.getFullYear(), gridMonth.getMonth());
      for (let d = 0; d < count; d += 1) {
        const date = addDays(gridMonth, d);
        if (!isDisabled(date)) return dayKey(date);
      }
    }
    return null;
  }, [focusedDay, firstSelected, today, isRenderedDate, isDisabled, numberOfMonths, month]);

  const monthActiveKey = useMemo((): string | null => {
    const y = month.getFullYear();
    const fromFocus = focusKey ? /^m(\d{1,2})$/.exec(focusKey) : null;
    if (fromFocus) {
      const m = Number(fromFocus[1]);
      if (m < 12 && monthEnabled(y, m)) return `m${m}`;
    }
    if (monthEnabled(y, month.getMonth())) return `m${month.getMonth()}`;
    for (let m = 0; m < 12; m += 1) if (monthEnabled(y, m)) return `m${m}`;
    return null;
  }, [focusKey, month, monthEnabled]);

  const yearActiveKey = useMemo((): string | null => {
    const fromFocus = focusKey ? /^y(\d+)$/.exec(focusKey) : null;
    if (fromFocus) {
      const y = Number(fromFocus[1]);
      if (yearPage.includes(y) && yearEnabled(y)) return `y${y}`;
    }
    const current = month.getFullYear();
    if (yearPage.includes(current) && yearEnabled(current)) return `y${current}`;
    for (const y of yearPage) if (yearEnabled(y)) return `y${y}`;
    return null;
  }, [focusKey, month, yearPage, yearEnabled]);

  /** Move focus to `key`; used by keyboard handlers and month-changing activations. */
  const requestFocus = useCallback((key: string) => {
    focusIntentRef.current = true;
    setFocusKey(key);
  }, []);

  // Focus follows the roving key: after keyboard navigation (or a
  // month-changing activation such as an outside-day click) the newly
  // rendered target cell receives focus. Without an explicit intent the
  // effect only refocuses while focus already lives inside the calendar, so
  // pointer users are never focus-napped.
  useEffect(() => {
    if (focusKey == null) return;
    const root = rootRef.current;
    if (!root) return;
    const intentional = focusIntentRef.current;
    focusIntentRef.current = false;
    if (!intentional && !root.contains(document.activeElement)) return;
    const el = root.querySelector<HTMLElement>(`[data-cal-focus="${focusKey}"]`);
    if (el && el !== document.activeElement) el.focus();
  }, [focusKey, monthKey, view]);

  /* ----- keyboard: day grid ------------------------------------------------ */

  const stepToEnabled = useCallback(
    (start: Date, step: (d: Date) => Date): Date | null => {
      let cursor = start;
      for (let i = 0; i < 732; i += 1) {
        if (!isDisabled(cursor)) return cursor;
        cursor = step(cursor);
      }
      return null;
    },
    [isDisabled],
  );

  const handleDayKeyDown = useCallback(
    (event: ReactKeyboardEvent<HTMLButtonElement>, date: Date) => {
      let target: Date;
      let step: (d: Date) => Date;
      switch (event.key) {
        case "ArrowLeft":
          target = addDays(date, -1);
          step = (d) => addDays(d, -1);
          break;
        case "ArrowRight":
          target = addDays(date, 1);
          step = (d) => addDays(d, 1);
          break;
        case "ArrowUp":
          target = addDays(date, -7);
          step = (d) => addDays(d, -7);
          break;
        case "ArrowDown":
          target = addDays(date, 7);
          step = (d) => addDays(d, 7);
          break;
        case "Home":
          // Start of the current week row (respects weekStartsOn).
          target = addDays(date, -((date.getDay() - weekStartsOn + 7) % 7));
          step = (d) => addDays(d, 1);
          break;
        case "End":
          target = addDays(date, 6 - ((date.getDay() - weekStartsOn + 7) % 7));
          step = (d) => addDays(d, -1);
          break;
        case "PageUp": {
          const amount = event.shiftKey ? -12 : -1;
          target = addMonths(date, amount);
          step = (d) => addMonths(d, amount);
          break;
        }
        case "PageDown": {
          const amount = event.shiftKey ? 12 : 1;
          target = addMonths(date, amount);
          step = (d) => addMonths(d, amount);
          break;
        }
        default:
          return;
      }
      event.preventDefault();
      const next = stepToEnabled(target, step);
      if (!next) return;
      if (!isRenderedDate(next)) goToMonth(monthToReveal(next));
      requestFocus(String(dayKey(next)));
    },
    [weekStartsOn, stepToEnabled, isRenderedDate, goToMonth, monthToReveal, requestFocus],
  );

  const handleDayClick = useCallback(
    (date: Date, outside: boolean) => {
      if (outside) {
        goToMonth(monthToReveal(date));
        requestFocus(String(dayKey(date)));
      }
      selectDate(date);
    },
    [goToMonth, monthToReveal, requestFocus, selectDate],
  );

  /* ----- keyboard: month / year pickers ------------------------------------- */

  const handleMonthKeyDown = useCallback(
    (event: ReactKeyboardEvent<HTMLButtonElement>, monthIndex: number) => {
      const year = month.getFullYear();
      const norm = (y: number, m: number): { y: number; m: number } => ({
        y: y + Math.floor(m / 12),
        m: ((m % 12) + 12) % 12,
      });
      let target: { y: number; m: number };
      let step: (c: { y: number; m: number }) => { y: number; m: number };
      switch (event.key) {
        case "ArrowLeft":
          target = norm(year, monthIndex - 1);
          step = (c) => norm(c.y, c.m - 1);
          break;
        case "ArrowRight":
          target = norm(year, monthIndex + 1);
          step = (c) => norm(c.y, c.m + 1);
          break;
        case "ArrowUp":
          target = norm(year, monthIndex - 3);
          step = (c) => norm(c.y, c.m - 3);
          break;
        case "ArrowDown":
          target = norm(year, monthIndex + 3);
          step = (c) => norm(c.y, c.m + 3);
          break;
        case "Home":
          target = { y: year, m: 0 };
          step = (c) => norm(c.y, c.m + 1);
          break;
        case "End":
          target = { y: year, m: 11 };
          step = (c) => norm(c.y, c.m - 1);
          break;
        case "PageUp":
          target = { y: year - 1, m: monthIndex };
          step = (c) => ({ y: c.y - 1, m: c.m });
          break;
        case "PageDown":
          target = { y: year + 1, m: monthIndex };
          step = (c) => ({ y: c.y + 1, m: c.m });
          break;
        default:
          return;
      }
      event.preventDefault();
      let cursor = target;
      for (let i = 0; i < 240 && !monthEnabled(cursor.y, cursor.m); i += 1) cursor = step(cursor);
      if (!monthEnabled(cursor.y, cursor.m)) return;
      if (cursor.y !== year) goToMonth(new Date(cursor.y, month.getMonth(), 1));
      requestFocus(`m${cursor.m}`);
    },
    [month, monthEnabled, goToMonth, requestFocus],
  );

  const handleYearKeyDown = useCallback(
    (event: ReactKeyboardEvent<HTMLButtonElement>, year: number) => {
      let target: number;
      let step: (y: number) => number;
      switch (event.key) {
        case "ArrowLeft":
          target = year - 1;
          step = (y) => y - 1;
          break;
        case "ArrowRight":
          target = year + 1;
          step = (y) => y + 1;
          break;
        case "ArrowUp":
          target = year - 3;
          step = (y) => y - 3;
          break;
        case "ArrowDown":
          target = year + 3;
          step = (y) => y + 3;
          break;
        case "Home":
          target = yearPage[0] ?? year;
          step = (y) => y + 1;
          break;
        case "End":
          target = yearPage[yearPage.length - 1] ?? year;
          step = (y) => y - 1;
          break;
        case "PageUp":
          target = year - 12;
          step = (y) => y - 12;
          break;
        case "PageDown":
          target = year + 12;
          step = (y) => y + 12;
          break;
        default:
          return;
      }
      event.preventDefault();
      let cursor = target;
      for (let i = 0; i < 240 && !yearEnabled(cursor); i += 1) cursor = step(cursor);
      if (!yearEnabled(cursor)) return;
      if (!yearPage.includes(cursor)) goToMonth(new Date(cursor, month.getMonth(), 1));
      requestFocus(`y${cursor}`);
    },
    [month, yearPage, yearEnabled, goToMonth, requestFocus],
  );

  const selectMonth = useCallback(
    (monthIndex: number) => {
      const year = month.getFullYear();
      const anchor = focusedDay ?? firstSelected ?? today;
      const day = Math.min(anchor.getDate(), daysInMonth(year, monthIndex));
      let target = new Date(year, monthIndex, day);
      if (isDisabled(target)) {
        target =
          stepToEnabled(target, (d) => addDays(d, 1)) ??
          stepToEnabled(target, (d) => addDays(d, -1)) ??
          new Date(year, monthIndex, 1);
      }
      goToMonth(new Date(year, monthIndex, 1));
      setView("days");
      requestFocus(String(dayKey(target)));
    },
    [month, focusedDay, firstSelected, today, isDisabled, stepToEnabled, goToMonth, requestFocus],
  );

  const selectYear = useCallback(
    (year: number) => {
      goToMonth(new Date(year, month.getMonth(), 1));
      setView("months");
      requestFocus(`m${month.getMonth()}`);
    },
    [month, goToMonth, requestFocus],
  );

  const contextValue: CalendarContextValue = {
    mode,
    locale,
    weekStartsOn,
    showOutsideDays,
    showWeekNumbers,
    numberOfMonths,
    view,
    setView,
    month,
    today,
    headingLabel,
    goToMonth,
    goToPrevious,
    goToNext,
    canGoPrevious,
    canGoNext,
    previousLabel,
    nextLabel,
    isDisabled,
    isSelected,
    isRangeStart,
    isRangeEnd,
    isRangeMiddle,
    selectDate,
    clearSelection,
    handleDayClick,
    handleDayKeyDown,
    tabbableDayKey,
    monthEnabled,
    yearEnabled,
    monthActiveKey,
    yearActiveKey,
    yearPage,
    selectMonth,
    selectYear,
    handleMonthKeyDown,
    handleYearKeyDown,
    focusKey,
    setFocusKey,
  };

  return (
    <CalendarContext.Provider value={contextValue}>
      <div ref={rootRef} className={cx(ROOT_CLASSES, className)} {...rest}>
        {children}
      </div>
    </CalendarContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* Header parts                                                             */
/* ------------------------------------------------------------------------ */

export type CalendarPartProps = HTMLAttributes<HTMLDivElement>;

export function CalendarHeader({ className, children, ...rest }: CalendarPartProps): ReactElement {
  return (
    <div className={cx(HEADER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export function CalendarPrevious({ className, ...rest }: HTMLAttributes<HTMLButtonElement>): ReactElement {
  const ctx = useCalendar();
  return (
    <button
      type="button"
      aria-label={ctx.previousLabel}
      disabled={!ctx.canGoPrevious}
      onClick={ctx.goToPrevious}
      className={cx(NAV_BUTTON_CLASSES, className)}
      {...rest}
    >
      <ChevronLeftIcon />
    </button>
  );
}

export function CalendarNext({ className, ...rest }: HTMLAttributes<HTMLButtonElement>): ReactElement {
  const ctx = useCalendar();
  return (
    <button
      type="button"
      aria-label={ctx.nextLabel}
      disabled={!ctx.canGoNext}
      onClick={ctx.goToNext}
      className={cx(NAV_BUTTON_CLASSES, className)}
      {...rest}
    >
      <ChevronRightIcon />
    </button>
  );
}

export function CalendarHeading({ className, ...rest }: HTMLAttributes<HTMLHeadingElement>): ReactElement {
  const ctx = useCalendar();
  if (ctx.view === "years") {
    return (
      <h2 aria-live="polite" aria-atomic="true" className={cx(HEADING_CLASSES, className)} {...rest}>
        {ctx.headingLabel}
      </h2>
    );
  }
  return (
    <h2 aria-live="polite" aria-atomic="true" className={cx(HEADING_CLASSES, className)} {...rest}>
      <button
        type="button"
        onClick={() => ctx.setView(ctx.view === "days" ? "months" : "years")}
        aria-label={
          ctx.view === "days"
            ? `${ctx.headingLabel} — activate to choose a month`
            : `${ctx.headingLabel} — activate to choose a year`
        }
        className={HEADING_BUTTON_CLASSES}
      >
        {ctx.headingLabel}
      </button>
    </h2>
  );
}

/* ------------------------------------------------------------------------ */
/* Day grid                                                                 */
/* ------------------------------------------------------------------------ */

export interface CalendarGridProps extends HTMLAttributes<HTMLDivElement> {
  /** Which visible month this grid renders (0-based). Must be < `numberOfMonths`. */
  monthOffset?: number;
}

export function CalendarGrid({ monthOffset = 0, className, ...rest }: CalendarGridProps): ReactElement | null {
  const ctx = useCalendar();
  if (ctx.view === "months") return monthOffset === 0 ? <MonthsPanel className={className} /> : null;
  if (ctx.view === "years") return monthOffset === 0 ? <YearsPanel className={className} /> : null;

  const gridMonth = startOfMonth(addMonths(ctx.month, monthOffset));
  const weeks = buildMonthWeeks(gridMonth, ctx.weekStartsOn);
  const weekdays = weekdayNames(ctx.locale, ctx.weekStartsOn);
  // ISO weeks belong to their Thursday — the row's week number is computed
  // from the Thursday of the row regardless of the configured week start.
  const weekNumberOf = (row: Date[]): number =>
    isoWeekNumber(addDays(row[0] ?? gridMonth, (4 - ctx.weekStartsOn + 7) % 7));

  return (
    <div className={className} {...rest}>
      <div role="grid" aria-label={monthYearLabel(gridMonth, ctx.locale)}>
        <div role="row" className="flex">
          {ctx.showWeekNumbers && (
            <div role="columnheader" aria-label="Week number" className={WEEKNUM_CLASSES}>
              Wk
            </div>
          )}
          {weekdays.map((day, i) => (
            <div role="columnheader" key={i} aria-label={day.long} className={WEEKDAY_CLASSES}>
              {day.short}
            </div>
          ))}
        </div>
        {weeks.map((week, rowIndex) => (
          <div role="row" className="flex" key={rowIndex}>
            {ctx.showWeekNumbers && (
              <div role="rowheader" className={WEEKNUM_CLASSES}>
                {weekNumberOf(week)}
              </div>
            )}
            {week.map((date) => (
              <DayCell key={dayKey(date)} date={date} gridMonth={gridMonth} monthOffset={monthOffset} />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

function DayCell({
  date,
  gridMonth,
  monthOffset,
}: {
  date: Date;
  gridMonth: Date;
  monthOffset: number;
}): ReactElement {
  const ctx = useCalendar();
  const outside = date.getMonth() !== gridMonth.getMonth();

  if (outside) {
    // Outside cells render only at the layout's outer edges — with several
    // months, interior outside cells would duplicate the neighbouring grid's
    // in-month buttons (double focus targets, duplicate accessible names).
    const isLeading = compareDays(date, gridMonth) < 0;
    const renderOutside =
      ctx.showOutsideDays && (isLeading ? monthOffset === 0 : monthOffset === ctx.numberOfMonths - 1);
    if (!renderOutside) return <div role="gridcell" className="size-9" />;
  }

  const key = String(dayKey(date));
  const isDisabledDay = ctx.isDisabled(date);
  const selected = ctx.isSelected(date);
  const rangeStart = ctx.isRangeStart(date);
  const rangeEnd = ctx.isRangeEnd(date);
  const rangeMiddle = ctx.isRangeMiddle(date);
  const filled =
    (ctx.mode !== "range" && selected) ||
    rangeStart ||
    rangeEnd ||
    (ctx.mode === "range" && selected && !rangeMiddle);
  const isToday = isSameDay(date, ctx.today);

  return (
    <div role="gridcell" aria-selected={selected} className="size-9">
      <button
        type="button"
        disabled={isDisabledDay}
        tabIndex={ctx.tabbableDayKey === dayKey(date) ? 0 : -1}
        data-cal-focus={key}
        data-outside={outside || undefined}
        aria-label={fullDateLabel(date, ctx.locale)}
        aria-current={isToday ? "date" : undefined}
        onClick={() => ctx.handleDayClick(date, outside)}
        onFocus={() => ctx.setFocusKey(key)}
        onKeyDown={(event) => ctx.handleDayKeyDown(event, date)}
        className={cx(
          DAY_CLASSES,
          rangeMiddle && RANGE_MIDDLE_CLASSES,
          !rangeMiddle && filled && SELECTED_DAY_CLASSES,
          !rangeMiddle && !filled &&
            (outside ? "text-[var(--ds-color-muted-foreground)]" : "text-[var(--ds-color-foreground)]"),
          !rangeMiddle && !filled && "hover:bg-[var(--ds-color-surface-hover)]",
          rangeStart && "rounded-r-none",
          rangeEnd && "rounded-l-none",
          isToday && "border-[var(--ds-color-border-strong)] font-semibold",
          isDisabledDay && "opacity-40",
        )}
      >
        {date.getDate()}
      </button>
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* Month / year picker panels                                               */
/* ------------------------------------------------------------------------ */

function MonthsPanel({ className }: { className?: string }): ReactElement {
  const ctx = useCalendar();
  const year = ctx.month.getFullYear();
  const names = monthNames(ctx.locale);
  const rows: number[][] = [];
  for (let r = 0; r < 4; r += 1) rows.push([r * 3, r * 3 + 1, r * 3 + 2]);

  return (
    <div className={className}>
      <div role="grid" aria-label={`Choose a month in ${yearLabel(year, ctx.locale)}`}>
        {rows.map((row, r) => (
          <div role="row" className="flex gap-1" key={r}>
            {row.map((m) => {
              const key = `m${m}`;
              const enabled = ctx.monthEnabled(year, m);
              const isCurrent = m === ctx.month.getMonth();
              return (
                <div role="gridcell" aria-selected={isCurrent} className="flex-1" key={m}>
                  <button
                    type="button"
                    disabled={!enabled}
                    tabIndex={ctx.monthActiveKey === key ? 0 : -1}
                    data-cal-focus={key}
                    aria-label={`${names[m]} ${yearLabel(year, ctx.locale)}`}
                    onClick={() => ctx.selectMonth(m)}
                    onFocus={() => ctx.setFocusKey(key)}
                    onKeyDown={(event) => ctx.handleMonthKeyDown(event, m)}
                    className={cx(
                      PICKER_BUTTON_CLASSES,
                      "w-full",
                      isCurrent
                        ? PICKER_SELECTED_CLASSES
                        : "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]",
                    )}
                  >
                    {names[m]}
                  </button>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

function YearsPanel({ className }: { className?: string }): ReactElement {
  const ctx = useCalendar();
  const rows: number[][] = [];
  for (let r = 0; r < 4; r += 1) rows.push(ctx.yearPage.slice(r * 3, r * 3 + 3));

  return (
    <div className={className}>
      <div role="grid" aria-label="Choose a year">
        {rows.map((row, r) => (
          <div role="row" className="flex gap-1" key={r}>
            {row.map((year) => {
              const key = `y${year}`;
              const enabled = ctx.yearEnabled(year);
              const isCurrent = year === ctx.month.getFullYear();
              return (
                <div role="gridcell" aria-selected={isCurrent} className="flex-1" key={year}>
                  <button
                    type="button"
                    disabled={!enabled}
                    tabIndex={ctx.yearActiveKey === key ? 0 : -1}
                    data-cal-focus={key}
                    onClick={() => ctx.selectYear(year)}
                    onFocus={() => ctx.setFocusKey(key)}
                    onKeyDown={(event) => ctx.handleYearKeyDown(event, year)}
                    className={cx(
                      PICKER_BUTTON_CLASSES,
                      "w-full tabular-nums",
                      isCurrent
                        ? PICKER_SELECTED_CLASSES
                        : "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]",
                    )}
                  >
                    {yearLabel(year, ctx.locale)}
                  </button>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* Footer                                                                   */
/* ------------------------------------------------------------------------ */

export function CalendarFooter({ className, children, ...rest }: CalendarPartProps): ReactElement {
  return (
    <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export default Calendar;
