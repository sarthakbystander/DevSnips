import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  InputHTMLAttributes,
  KeyboardEvent as ReactKeyboardEvent,
  ReactElement,
  ReactNode,
  RefObject,
} from "react";

/**
 * DevSnips React Date Picker — label / description / helper wiring.
 *
 * The shared compound DatePicker composed with the root-rendered field
 * chrome: a real `<label htmlFor>`, a description, helper text, and the
 * required marker, associated through generated `id` + `aria-describedby`.
 * Implementation identical to the reference `date-picker/code.tsx`.
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/* ------------------------------------------------------------------------ */
/* Date utilities — local calendar-date semantics (Calendar family model)   */
/* ------------------------------------------------------------------------ */

export type WeekDay = 0 | 1 | 2 | 3 | 4 | 5 | 6;

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

/**
 * `yyyy-mm-dd` built from LOCAL date parts — never the built-in ISO
 * conversion (which goes through UTC and can shift the calendar day). This
 * is the value the hidden form input submits.
 */
export function formatISODate(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

/** `yyyy-mm-ddThh:mm` from local parts (the date-time mode form value). */
export function formatISODateTime(date: Date): string {
  const hh = String(date.getHours()).padStart(2, "0");
  const mm = String(date.getMinutes()).padStart(2, "0");
  return `${formatISODate(date)}T${hh}:${mm}`;
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

export type DatePickerMode = "single" | "range";
export type DatePickerView = "days" | "months" | "years";
export type DatePickerSize = "md" | "lg";
export type DatePickerOpenOrigin = "input" | "trigger" | "programmatic";

/**
 * A preset option for `<DatePickerPresets>`. `getValue` receives today so
 * relative presets ("Last 7 days") stay correct without a clock dependency
 * inside the component. The returned shape must match the picker's `mode`
 * (`Date` for `single`, `DateRange` for `range`).
 */
export interface DatePickerPreset {
  label: string;
  description?: string;
  getValue: (today: Date) => Date | DateRange;
}

export interface DatePickerBaseProps {
  /** Open state (controlled). */
  open?: boolean;
  /** Initial open state (uncontrolled). */
  defaultOpen?: boolean;
  /** Called whenever the popover opens or closes. */
  onOpenChange?: (open: boolean) => void;
  /** Earliest selectable date (inclusive). Earlier dates and earlier navigation are disabled. */
  minDate?: Date;
  /** Latest selectable date (inclusive). Later dates and later navigation are disabled. */
  maxDate?: Date;
  /** Matcher for individual disabled dates; composes with `minDate` / `maxDate`. */
  disabledDates?: (date: Date) => boolean;
  /** BCP-47 locale tag for the calendar labels and the default date format. Default `"en-US"`. */
  locale?: string;
  /** First weekday column: 0 = Sunday … 6 = Saturday. Default 0. */
  weekStartsOn?: WeekDay;
  /**
   * Display formatter for the committed value shown in the input. Defaults to
   * `Intl.DateTimeFormat(locale, { dateStyle: "medium" })` (plus
   * `timeStyle: "short"` when `withTime`).
   */
  formatDate?: (date: Date) => string;
  /** Input placeholder. Defaults to "Select date" / "Select date range". */
  placeholder?: string;
  /** Disables the control: no popover, not focusable, not submitted. */
  disabled?: boolean;
  /** Freezes the value: the input stays focusable + submittable but the popover cannot open. */
  readOnly?: boolean;
  /** Marks the control required: `aria-required` + a required marker on the root-rendered label. */
  required?: boolean;
  /**
   * Form field name. When set, a hidden input submits the value as
   * `yyyy-mm-dd` (`yyyy-mm-ddThh:mm` with `withTime`; `from/to` for ranges,
   * `to` empty while the range is incomplete).
   */
  name?: string;
  /** Label text rendered by the root and associated with the input via `htmlFor` + `id`. */
  label?: string;
  /** Description text rendered above the control and referenced via `aria-describedby`. */
  description?: string;
  /** Helper text rendered below the control (hidden while `error` is set) and referenced via `aria-describedby`. */
  helperText?: string;
  /** Error message: renders with `role="alert"`, sets `aria-invalid` on the input, and is referenced via `aria-describedby`. */
  error?: string;
  /** Accessible name for the trigger button. Default "Open calendar". */
  triggerLabel?: string;
  /** Accessible name for the input when no `label` is rendered. Default "Date" / "Date range". */
  inputAriaLabel?: string;
  /**
   * When true, calendar interaction stages a draft value: the input keeps
   * showing the committed value until `<DatePickerApply>` commits the draft
   * (Escape / outside close discards it). `<DatePickerClear>` always clears
   * both immediately.
   */
  requireApply?: boolean;
  /** Adds the `<DatePickerTime>` hour/minute section to the value and keeps the popover open after day selection. */
  withTime?: boolean;
  /** Minute step for the time controls. Default 5. The current value is always offered even when off-step. */
  timeStep?: number;
  /** Initial visible month (uncontrolled). Defaults to the committed selection's month, else today. Any Date inside the month; normalized to the 1st. */
  defaultMonth?: Date;
  /** Consecutive month grids in the popover. Default 1. Grids stack vertically on narrow screens. */
  numberOfMonths?: number;
  /** Initial picker view. The heading button cycles days → months → years regardless. */
  defaultView?: DatePickerView;
  /** Control size: `md` = 36px cells (default), `lg` = 44px cells (touch-friendly). */
  size?: DatePickerSize;
  className?: string;
  children?: ReactNode;
}

export interface DatePickerSingleValueProps {
  mode?: "single";
  value?: Date | null;
  defaultValue?: Date | null;
  onChange?: (date: Date | null) => void;
}

export interface DatePickerRangeValueProps {
  mode: "range";
  value?: DateRange | null;
  defaultValue?: DateRange | null;
  onChange?: (range: DateRange | null) => void;
}

export type DatePickerProps = DatePickerBaseProps &
  (DatePickerSingleValueProps | DatePickerRangeValueProps);

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

export interface DatePickerContextValue {
  mode: DatePickerMode;
  locale: string;
  weekStartsOn: WeekDay;
  size: DatePickerSize;
  numberOfMonths: number;
  withTime: boolean;
  requireApply: boolean;
  open: boolean;
  requestOpen: (origin: DatePickerOpenOrigin) => void;
  requestClose: (restoreFocus: boolean) => void;
  toggleOpen: (origin: DatePickerOpenOrigin) => void;
  inputId: string;
  panelId: string;
  describedBy: string | undefined;
  hasError: boolean;
  disabled: boolean;
  readOnly: boolean;
  required: boolean;
  placeholder: string;
  triggerLabel: string;
  /** Resolved accessible name for the input (root `inputAriaLabel` or the mode default). */
  inputAriaLabel: string;
  /** The committed value shown in the input (`Date | DateRange | null`). */
  committedValue: Date | DateRange | null;
  /** The value the calendar displays — the staged draft with `requireApply`, else the committed value. */
  stagedValue: Date | DateRange | null;
  displayValue: string;
  /** Locale-aware display string for the value shapes (used by composed readouts). */
  formatValue: (value: Date | DateRange | null) => string;
  /** View state. */
  view: DatePickerView;
  setView: (view: DatePickerView) => void;
  month: Date;
  today: Date;
  headingLabel: string;
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
  isPreviewMiddle: (date: Date) => boolean;
  handleDayClick: (date: Date) => void;
  handleDayKeyDown: (event: ReactKeyboardEvent<HTMLButtonElement>, date: Date) => void;
  handleDayPointerEnter: (date: Date) => void;
  handleDayPointerLeave: () => void;
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
  setFocusKey: (key: string) => void;
  /** Footer / preset actions. */
  clearValue: () => void;
  applyDraft: () => void;
  canApply: boolean;
  selectToday: () => void;
  todayDisabled: boolean;
  applyPreset: (preset: DatePickerPreset) => void;
  isPresetActive: (preset: DatePickerPreset) => boolean;
  /** Time section state (`withTime`). Null until a date is staged/committed. */
  time: { hours: number; minutes: number } | null;
  setTime: (hours: number, minutes: number) => void;
  timeStep: number;
}

const DatePickerContext = createContext<DatePickerContextValue | null>(null);

/** Access the nearest `<DatePicker>` context (for composed children such as footer readouts). */
export function useDatePicker(): DatePickerContextValue {
  const ctx = useContext(DatePickerContext);
  if (!ctx) throw new Error("DatePicker components must be composed inside <DatePicker>.");
  return ctx;
}

/* Refs shared with the field primitives (input / trigger / content) without
 * widening the public context surface. */
interface InternalRefs {
  inputRef: RefObject<HTMLInputElement>;
  triggerRef: RefObject<HTMLButtonElement>;
  panelRef: RefObject<HTMLDivElement>;
}
const DatePickerRefsContext = createContext<InternalRefs>({
  inputRef: { current: null },
  triggerRef: { current: null },
  panelRef: { current: null },
});

/* ------------------------------------------------------------------------ */
/* Shared class constants (token-driven)                                    */
/* ------------------------------------------------------------------------ */

const INPUT_CLASSES =
  "h-9 w-full cursor-default rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none";
const INPUT_ERROR_CLASSES = "border-[var(--ds-color-destructive)] hover:border-[var(--ds-color-destructive)]";
const TRIGGER_CLASSES =
  "inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const PANEL_CLASSES =
  "absolute z-50 w-max max-w-[calc(100vw-1rem)] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-3 shadow-[var(--ds-shadow-md)]";
const PANEL_SHEET_CLASSES =
  "max-sm:fixed max-sm:inset-x-3 max-sm:bottom-3 max-sm:top-auto max-sm:mt-0 max-sm:w-auto max-sm:max-w-none max-sm:max-h-[75dvh] max-sm:overflow-y-auto";
const SHEET_OVERLAY_CLASSES = "fixed inset-0 z-40 bg-[var(--ds-color-overlay)] sm:hidden";
const NAV_BUTTON_CLASSES = TRIGGER_CLASSES;
const HEADING_CLASSES = "m-0 text-sm font-semibold leading-9 text-[var(--ds-color-foreground)]";
const HEADING_BUTTON_CLASSES =
  "-mx-1.5 rounded-[var(--ds-radius-sm)] px-1.5 transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const DAY_BASE_CLASSES =
  "inline-flex items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent leading-5 tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none";
const PICKER_BUTTON_CLASSES =
  "flex h-9 flex-1 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent px-2 text-sm leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none";
const FOOTER_CLASSES =
  "mt-2 flex flex-wrap items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-2";
const PRESET_CLASSES =
  "inline-flex h-8 w-full items-center justify-start rounded-[var(--ds-radius-sm)] px-2 text-left text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const PRESET_ACTIVE_CLASSES = "bg-[var(--ds-color-surface-active)] font-medium";
const ACTION_BUTTON_CLASSES =
  "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-2.5 text-xs font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const APPLY_BUTTON_CLASSES =
  "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-2.5 text-xs font-medium leading-4 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const TIME_SELECT_CLASSES =
  "h-9 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-2 text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none";

const SELECTED_DAY_CLASSES =
  "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)]";
const RANGE_MIDDLE_CLASSES = "rounded-none bg-[var(--ds-color-surface-active)] text-[var(--ds-color-foreground)]";
const PREVIEW_MIDDLE_CLASSES = "rounded-none bg-[var(--ds-color-surface-hover)] text-[var(--ds-color-foreground)]";
const PICKER_SELECTED_CLASSES = "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)]";

/** Size scale: md = the family's default 36px controls; lg = 44px touch targets. */
const SIZE_CLASSES: Record<DatePickerSize, { cell: string; text: string; weekday: string }> = {
  md: { cell: "size-9", text: "text-sm", weekday: "text-[11px]" },
  lg: { cell: "size-11", text: "text-sm", weekday: "text-xs" },
};

/* ------------------------------------------------------------------------ */
/* Icons (inline SVG — consistent stroke with the DevSnips icon set)        */
/* ------------------------------------------------------------------------ */

function CalendarGlyphIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
      <line x1="16" x2="16" y1="2" y2="6" />
      <line x1="8" x2="8" y1="2" y2="6" />
      <line x1="3" x2="21" y1="10" y2="10" />
    </svg>
  );
}

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

function firstDateOf(value: Date | DateRange | null): Date | null {
  if (!value) return null;
  return value instanceof Date ? value : value.from;
}

export function DatePicker(props: DatePickerProps): ReactElement {
  const {
    open: controlledOpen,
    defaultOpen = false,
    onOpenChange,
    minDate,
    maxDate,
    disabledDates,
    locale = "en-US",
    weekStartsOn = 0,
    formatDate: formatDateProp,
    placeholder: placeholderProp,
    disabled = false,
    readOnly = false,
    required = false,
    name,
    label,
    description,
    helperText,
    error,
    triggerLabel = "Open calendar",
    inputAriaLabel,
    requireApply = false,
    withTime = false,
    timeStep = 5,
    defaultMonth,
    numberOfMonths = 1,
    defaultView = "days",
    size = "md",
    className,
    children,
    // Value props are consumed through the typed slices below — destructured
    // here so they never leak onto the DOM via `...rest` (`onChange` also
    // collides with the native React event handler).
    mode: _mode,
    value: _value,
    defaultValue: _defaultValue,
    onChange: _onChange,
    ...rest
  } = props;
  const mode: DatePickerMode = _mode ?? "single";

  // The discriminated union guarantees each value slice matches `mode`; the
  // casts re-associate the union member with its own props. A slice is only
  // ever read or written when `mode` selects it.
  const singleSlice = props as DatePickerBaseProps & DatePickerSingleValueProps;
  const rangeSlice = props as DatePickerBaseProps & DatePickerRangeValueProps;

  const [singleValue, setSingleValue] = useControllableState<Date | null>(
    mode === "single" ? singleSlice.value : undefined,
    (mode === "single" ? singleSlice.defaultValue : null) ?? null,
    mode === "single" ? singleSlice.onChange : undefined,
  );
  const [rangeValue, setRangeValue] = useControllableState<DateRange | null>(
    mode === "range" ? rangeSlice.value : undefined,
    (mode === "range" ? rangeSlice.defaultValue : undefined) ?? null,
    mode === "range" ? rangeSlice.onChange : undefined,
  );

  const committedValue: Date | DateRange | null = mode === "single" ? singleValue : rangeValue;
  const commitValue = useCallback(
    (next: Date | DateRange | null) => {
      if (mode === "single") setSingleValue(next === null || next instanceof Date ? next : next.from);
      else setRangeValue(next instanceof Date ? { from: next, to: null } : next);
    },
    [mode, setSingleValue, setRangeValue],
  );

  const [open, setOpen] = useControllableState<boolean>(controlledOpen, defaultOpen, onOpenChange);

  const [today] = useState(() => new Date());

  /* ----- formatting ------------------------------------------------------- */

  const formatDate = useCallback(
    (date: Date): string => {
      if (formatDateProp) return formatDateProp(date);
      return new Intl.DateTimeFormat(
        locale,
        withTime
          ? { dateStyle: "medium", timeStyle: "short", hourCycle: "h23" }
          : { dateStyle: "medium" },
      ).format(date);
    },
    [formatDateProp, locale, withTime],
  );

  const formatValue = useCallback(
    (value: Date | DateRange | null): string => {
      if (!value) return "";
      if (value instanceof Date) return formatDate(value);
      if (!value.to) return `${formatDate(value.from)} – …`;
      return `${formatDate(value.from)} – ${formatDate(value.to)}`;
    },
    [formatDate],
  );

  const placeholder =
    placeholderProp ?? (mode === "range" ? "Select date range" : "Select date");
  const resolvedInputAriaLabel =
    inputAriaLabel ?? (mode === "range" ? "Date range" : "Date");

  /* ----- visible month ---------------------------------------------------- */

  const [monthState, setMonthState] = useState<Date>(() =>
    startOfMonth(defaultMonth ?? firstDateOf(committedValue) ?? today),
  );
  const monthKey = monthState.getFullYear() * 12 + monthState.getMonth();
  const month = useMemo(() => startOfMonth(monthState), [monthKey]); // eslint-disable-line react-hooks/exhaustive-deps

  const [view, setView] = useState<DatePickerView>(defaultView);
  const [focusKey, setFocusKey] = useState<string | null>(null);
  const focusIntentRef = useRef<string | null>(null);
  const [hoveredDate, setHoveredDate] = useState<Date | null>(null);

  const inputRef = useRef<HTMLInputElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const restoreTargetRef = useRef<HTMLElement | null>(null);
  const restoreRequestedRef = useRef(false);

  /* ----- constraints ------------------------------------------------------ */

  const isDisabled = useCallback(
    (date: Date): boolean => {
      if (minDate && compareDays(date, minDate) < 0) return true;
      if (maxDate && compareDays(date, maxDate) > 0) return true;
      return disabledDates ? disabledDates(date) : false;
    },
    [minDate, maxDate, disabledDates],
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

  const lastVisibleMonth = useMemo(
    () => startOfMonth(addMonths(month, numberOfMonths - 1)),
    [month, numberOfMonths],
  );

  const isRenderedDate = useCallback(
    (date: Date): boolean =>
      compareDays(date, month) >= 0 && compareDays(date, endOfMonth(lastVisibleMonth)) <= 0,
    [month, lastVisibleMonth],
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
    [minDate, maxDate, numberOfMonths],
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

  /* ----- navigation -------------------------------------------------------- */

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

  /* ----- open / close ------------------------------------------------------ */

  // The focus-restore target is captured at request time (not in the open
  // effect): child effects run before the root's, so by effect time focus has
  // already moved into the panel.
  const requestOpen = useCallback(
    (_origin: DatePickerOpenOrigin) => {
      if (disabled || readOnly || open) return;
      restoreTargetRef.current =
        document.activeElement instanceof HTMLElement ? document.activeElement : null;
      setOpen(true);
    },
    [disabled, readOnly, open, setOpen],
  );

  const requestClose = useCallback(
    (restoreFocus: boolean) => {
      if (!open) return;
      if (restoreFocus) restoreRequestedRef.current = true;
      setOpen(false);
    },
    [open, setOpen],
  );

  const toggleOpen = useCallback(
    (origin: DatePickerOpenOrigin) => {
      if (open) requestClose(true);
      else requestOpen(origin);
    },
    [open, requestOpen, requestClose],
  );

  // Opening: reset to the default view and reveal the selected date's month.
  // Focus moves into the grid only when the open was user-initiated (a
  // restore target was captured) — a programmatic `defaultOpen` / controlled
  // `open` never steals focus on mount.
  const committedRef = useRef(committedValue);
  committedRef.current = committedValue;
  useEffect(() => {
    if (!open) return;
    setHoveredDate(null);
    setView(defaultView);
    const selected = firstDateOf(committedRef.current);
    const reveal = selected ? monthToReveal(selected) : month;
    if (selected) goToMonth(reveal);
    if (!restoreTargetRef.current) return;
    // Picker entry views focus the matching picker option, not a day.
    if (defaultView === "months") {
      requestFocus(`m${reveal.getMonth()}`);
      return;
    }
    if (defaultView === "years") {
      requestFocus(`y${reveal.getFullYear()}`);
      return;
    }
    // Focus target: the selected day, else today (when rendered), else the
    // first enabled day of the visible months — computed against the revealed
    // month, which applies in the same commit as the focus request.
    const renderedEnd = endOfMonth(startOfMonth(addMonths(reveal, numberOfMonths - 1)));
    const rendered = (d: Date) => compareDays(d, reveal) >= 0 && compareDays(d, renderedEnd) <= 0;
    let target: Date | null = null;
    if (selected && rendered(selected) && !isDisabled(selected)) target = selected;
    else if (rendered(today) && !isDisabled(today)) target = today;
    else {
      for (let i = 0; i < numberOfMonths && !target; i += 1) {
        const gridMonth = startOfMonth(addMonths(reveal, i));
        const count = daysInMonth(gridMonth.getFullYear(), gridMonth.getMonth());
        for (let d = 0; d < count && !target; d += 1) {
          const candidate = addDays(gridMonth, d);
          if (!isDisabled(candidate)) target = candidate;
        }
      }
    }
    if (target) requestFocus(String(dayKey(target)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Closing: restore focus to the element that opened the popover, but never
  // to an unmounted one.
  useEffect(() => {
    if (open || !restoreRequestedRef.current) return;
    restoreRequestedRef.current = false;
    const target = restoreTargetRef.current;
    restoreTargetRef.current = null;
    if (target && target.isConnected) target.focus();
  }, [open]);

  /* ----- draft (staged selection for requireApply) ------------------------- */

  const [draft, setDraft] = useState<Date | DateRange | null>(committedValue);
  // The draft tracks the committed value while the popover is closed, so
  // reopening starts from the committed value and a discarded draft never
  // lingers.
  useEffect(() => {
    if (!open) setDraft(committedValue);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, committedValue]);

  const stagedValue: Date | DateRange | null = requireApply ? draft : committedValue;

  /* ----- selection --------------------------------------------------------- */

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

  /** Preserve the current time on a newly picked day (withTime); 12:00 when empty. */
  const withCurrentTime = useCallback(
    (day: Date): Date => {
      if (!withTime) return day;
      const base = firstDateOf(stagedValue);
      const hours = base ? base.getHours() : 12;
      const minutes = base ? base.getMinutes() : 0;
      return new Date(day.getFullYear(), day.getMonth(), day.getDate(), hours, minutes);
    },
    [withTime, stagedValue],
  );

  const selectDate = useCallback(
    (date: Date) => {
      if (isDisabled(date)) return;
      const day = withCurrentTime(date);
      if (mode === "single") {
        if (requireApply) {
          setDraft(day);
          return;
        }
        if (singleValue && isSameDay(singleValue, day)) {
          // Re-clicking the committed date: never an accidental deselect —
          // just dismiss the popover.
          if (!withTime) requestClose(true);
          return;
        }
        commitValue(day);
        if (!withTime) requestClose(true);
        return;
      }
      // range
      const current = stagedValue instanceof Date || stagedValue === null ? null : stagedValue;
      let next: DateRange;
      if (!current || current.to) {
        next = { from: day, to: null };
      } else if (isSameDay(day, current.from)) {
        next = { from: current.from, to: current.from };
      } else if (compareDays(day, current.from) < 0 || rangeCrossesDisabled(current.from, day)) {
        // Earlier-than-start or crossing a disabled day: restart, predictably.
        next = { from: day, to: null };
      } else {
        next = { from: current.from, to: day };
      }
      if (requireApply) setDraft(next);
      else commitValue(next);
      setHoveredDate(null);
      if (next.to && !requireApply && !withTime) requestClose(true);
    },
    [
      isDisabled,
      withCurrentTime,
      mode,
      requireApply,
      singleValue,
      withTime,
      requestClose,
      commitValue,
      stagedValue,
      rangeCrossesDisabled,
    ],
  );

  const clearValue = useCallback(() => {
    // Clear is an explicit action: it commits immediately even under
    // requireApply, and resets the draft so a reopened popover stays empty.
    commitValue(null);
    setDraft(null);
    setHoveredDate(null);
  }, [commitValue]);

  const canApply =
    mode === "single" ||
    stagedValue === null ||
    stagedValue instanceof Date ||
    stagedValue.to !== null;

  const applyDraft = useCallback(() => {
    if (!canApply) return;
    if (requireApply) commitValue(stagedValue);
    requestClose(true);
  }, [canApply, requireApply, commitValue, stagedValue, requestClose]);

  const todayDisabled = isDisabled(today);

  const selectToday = useCallback(() => {
    if (todayDisabled) return;
    goToMonth(monthToReveal(today));
    requestFocus(String(dayKey(today)));
    selectDate(today);
  }, [todayDisabled, goToMonth, monthToReveal, today, selectDate]);

  const applyPreset = useCallback(
    (preset: DatePickerPreset) => {
      const value = preset.getValue(today);
      const anchor = value instanceof Date ? value : value.from;
      const matches = mode === "single" ? value instanceof Date : !(value instanceof Date);
      if (!matches) return;
      if (requireApply) setDraft(value);
      else commitValue(value);
      goToMonth(monthToReveal(anchor));
      requestFocus(String(dayKey(anchor)));
      if (!requireApply) requestClose(true);
    },
    [today, mode, requireApply, commitValue, goToMonth, monthToReveal, requestClose],
  );

  const isPresetActive = useCallback(
    (preset: DatePickerPreset): boolean => {
      const value = preset.getValue(today);
      const current = stagedValue;
      if (value instanceof Date) return current instanceof Date && isSameDay(value, current);
      if (current === null || current instanceof Date || current.to === null) return false;
      return isSameDay(value.from, current.from) && isSameDay(value.to ?? value.from, current.to);
    },
    [today, stagedValue],
  );

  /* ----- time (withTime) ---------------------------------------------------- */

  const time = useMemo((): { hours: number; minutes: number } | null => {
    if (!withTime) return null;
    const base = firstDateOf(stagedValue);
    return base ? { hours: base.getHours(), minutes: base.getMinutes() } : null;
  }, [withTime, stagedValue]);

  const setTime = useCallback(
    (hours: number, minutes: number) => {
      if (!withTime) return;
      const base = stagedValue;
      if (!base) return;
      const merge = (d: Date) =>
        new Date(d.getFullYear(), d.getMonth(), d.getDate(), hours, minutes);
      const next =
        base instanceof Date
          ? merge(base)
          : { from: merge(base.from), to: base.to ? merge(base.to) : null };
      if (requireApply) setDraft(next);
      else commitValue(next);
    },
    [withTime, stagedValue, requireApply, commitValue],
  );

  /* ----- range / preview state ---------------------------------------------- */

  const rangeState = stagedValue instanceof Date || stagedValue === null ? null : stagedValue;

  const isRangeStart = useCallback(
    (date: Date) =>
      mode === "range" &&
      rangeState !== null &&
      rangeState.to !== null &&
      !isSameDay(rangeState.from, rangeState.to) &&
      isSameDay(rangeState.from, date),
    [mode, rangeState],
  );
  const isRangeEnd = useCallback(
    (date: Date) =>
      mode === "range" &&
      rangeState !== null &&
      rangeState.to !== null &&
      !isSameDay(rangeState.from, rangeState.to) &&
      isSameDay(rangeState.to, date),
    [mode, rangeState],
  );
  const isRangeMiddle = useCallback(
    (date: Date) =>
      mode === "range" &&
      rangeState !== null &&
      rangeState.to !== null &&
      compareDays(date, rangeState.from) > 0 &&
      compareDays(date, rangeState.to) < 0,
    [mode, rangeState],
  );
  const isPreviewMiddle = useCallback(
    (date: Date): boolean => {
      if (mode !== "range" || !rangeState || rangeState.to !== null || !hoveredDate) return false;
      if (compareDays(hoveredDate, rangeState.from) <= 0) return false;
      return compareDays(date, rangeState.from) > 0 && compareDays(date, hoveredDate) < 0;
    },
    [mode, rangeState, hoveredDate],
  );
  const isSelected = useCallback(
    (date: Date): boolean => {
      if (mode === "single") return stagedValue instanceof Date && isSameDay(stagedValue, date);
      return (
        rangeState !== null &&
        (isSameDay(rangeState.from, date) ||
          (rangeState.to !== null &&
            compareDays(date, rangeState.from) > 0 &&
            compareDays(date, rangeState.to) <= 0))
      );
    },
    [mode, stagedValue, rangeState],
  );

  const handleDayClick = useCallback((date: Date) => selectDate(date), [selectDate]);
  const handleDayPointerEnter = useCallback(
    (date: Date) => {
      if (mode === "range" && rangeState && rangeState.to === null) setHoveredDate(date);
    },
    [mode, rangeState],
  );
  const handleDayPointerLeave = useCallback(() => setHoveredDate(null), []);

  /* ----- focus model (roving tabindex) -------------------------------------- */

  const focusedDay = useMemo((): Date | null => {
    if (focusKey && /^\d{8}$/.test(focusKey)) return dateFromKey(Number(focusKey));
    return null;
  }, [focusKey]);

  const firstStagedDate = firstDateOf(stagedValue);

  const tabbableDayKey = useMemo((): number | null => {
    const candidates: Array<Date | null> = [focusedDay, firstStagedDate, today];
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
  }, [focusedDay, firstStagedDate, today, isRenderedDate, isDisabled, numberOfMonths, month]);

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

  /**
   * Move focus to `key`; used by keyboard handlers and activations. The key
   * is parked on a ref so the focus effect can always read the LATEST
   * request — even from a commit whose `focusKey` closure is still stale.
   */
  const requestFocus = useCallback((key: string) => {
    focusIntentRef.current = key;
    setFocusKey(key);
  }, []);

  // Focus follows the roving key. Without an explicit intent the effect only
  // refocuses while focus already lives inside the panel, so pointer users
  // are never focus-napped.
  useEffect(() => {
    if (!open || focusKey == null) return;
    const panel = panelRef.current;
    if (!panel) return;
    const intent = focusIntentRef.current;
    focusIntentRef.current = null;
    if (!intent && !panel.contains(document.activeElement)) return;
    const el = panel.querySelector<HTMLElement>(`[data-dp-focus="${intent ?? focusKey}"]`);
    if (el && el !== document.activeElement) el.focus();
  }, [open, focusKey, monthKey, view]);

  /* ----- keyboard: day grid -------------------------------------------------- */

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

  /* ----- keyboard: month / year pickers -------------------------------------- */

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
      const anchor = focusedDay ?? firstStagedDate ?? today;
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
    [month, focusedDay, firstStagedDate, today, isDisabled, stepToEnabled, goToMonth, requestFocus],
  );

  const selectYear = useCallback(
    (year: number) => {
      goToMonth(new Date(year, month.getMonth(), 1));
      setView("months");
      requestFocus(`m${month.getMonth()}`);
    },
    [month, goToMonth, requestFocus],
  );

  /* ----- ids + field wiring --------------------------------------------------- */

  const baseId = useId().replace(/:/g, "");
  const inputId = `${baseId}-input`;
  const panelId = `${baseId}-panel`;
  const descriptionId = description !== undefined ? `${baseId}-description` : null;
  const hasError = typeof error === "string" && error.length > 0;
  const messageId = hasError ? `${baseId}-error` : helperText !== undefined ? `${baseId}-helper` : null;
  const describedBy = [descriptionId, messageId].filter(Boolean).join(" ") || undefined;

  /* ----- form value ------------------------------------------------------------ */

  const isoValue = useMemo((): string => {
    if (!committedValue) return "";
    if (committedValue instanceof Date) {
      return withTime ? formatISODateTime(committedValue) : formatISODate(committedValue);
    }
    const from = formatISODate(committedValue.from);
    const to = committedValue.to ? formatISODate(committedValue.to) : "";
    return `${from}/${to}`;
  }, [committedValue, withTime]);

  const displayValue = formatValue(committedValue);

  const contextValue: DatePickerContextValue = {
    mode,
    locale,
    weekStartsOn,
    size,
    numberOfMonths,
    withTime,
    requireApply,
    open,
    requestOpen,
    requestClose,
    toggleOpen,
    inputId,
    panelId,
    describedBy,
    hasError,
    disabled,
    readOnly,
    required,
    placeholder,
    triggerLabel,
    inputAriaLabel: resolvedInputAriaLabel,
    committedValue,
    stagedValue,
    displayValue,
    formatValue,
    view,
    setView,
    month,
    today,
    headingLabel,
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
    isPreviewMiddle,
    handleDayClick,
    handleDayKeyDown,
    handleDayPointerEnter,
    handleDayPointerLeave,
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
    setFocusKey,
    clearValue,
    applyDraft,
    canApply,
    selectToday,
    todayDisabled,
    applyPreset,
    isPresetActive,
    time,
    setTime,
    timeStep,
  };

  const refsValue = useMemo<InternalRefs>(
    () => ({ inputRef, triggerRef, panelRef }),
    [],
  );
  const hasFieldChrome =
    label !== undefined || description !== undefined || helperText !== undefined || hasError;

  const hiddenInput = name !== undefined && (
    <input type="hidden" name={name} value={isoValue} disabled={disabled} readOnly />
  );

  return (
    <DatePickerContext.Provider value={contextValue}>
      <DatePickerRefsContext.Provider value={refsValue}>
        {hasFieldChrome ? (
          <div className={cx("w-full max-w-xs space-y-1.5", className)} {...rest}>
            {label !== undefined && (
              <label
                htmlFor={inputId}
                className="block text-sm font-medium leading-5 text-[var(--ds-color-foreground)]"
              >
                {label}
                {required && (
                  <span aria-hidden="true" className="text-[var(--ds-color-destructive)]">
                    {" *"}
                  </span>
                )}
              </label>
            )}
            {description !== undefined && (
              <p
                id={descriptionId ?? undefined}
                className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
              >
                {description}
              </p>
            )}
            <div className="relative flex items-center gap-1">
              {children}
              {hiddenInput}
            </div>
            {hasError ? (
              <p
                id={messageId ?? undefined}
                role="alert"
                className="m-0 text-xs font-medium leading-4 text-[var(--ds-color-destructive)]"
              >
                {error}
              </p>
            ) : (
              helperText !== undefined && (
                <p
                  id={messageId ?? undefined}
                  className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
                >
                  {helperText}
                </p>
              )
            )}
          </div>
        ) : (
          <div className={cx("relative flex w-full max-w-xs items-center gap-1", className)} {...rest}>
            {children}
            {hiddenInput}
          </div>
        )}
      </DatePickerRefsContext.Provider>
    </DatePickerContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* Field: input + trigger                                                    */
/* ------------------------------------------------------------------------ */

export type DatePickerInputProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  "value" | "defaultValue" | "onChange" | "onSelect" | "size"
>;

export function DatePickerInput({
  className,
  id,
  onClick,
  onKeyDown,
  "aria-label": ariaLabel,
  "aria-describedby": ariaDescribedBy,
  ...rest
}: DatePickerInputProps): ReactElement {
  const ctx = useDatePicker();
  const refs = useContext(DatePickerRefsContext);
  return (
    <input
      ref={refs.inputRef}
      type="text"
      readOnly
      id={id ?? ctx.inputId}
      value={ctx.displayValue}
      placeholder={ctx.placeholder}
      disabled={ctx.disabled}
      aria-label={ariaLabel ?? ctx.inputAriaLabel}
      aria-haspopup="dialog"
      aria-expanded={ctx.open}
      aria-controls={ctx.open ? ctx.panelId : undefined}
      aria-required={ctx.required || undefined}
      aria-invalid={ctx.hasError || undefined}
      aria-describedby={cx(ariaDescribedBy, ctx.describedBy) || undefined}
      onClick={(event) => {
        if (!ctx.open) ctx.requestOpen("input");
        onClick?.(event);
      }}
      onKeyDown={(event) => {
        if (
          !ctx.open &&
          (event.key === "ArrowDown" || event.key === "ArrowUp" || event.key === "Enter" || event.key === " ")
        ) {
          event.preventDefault();
          ctx.requestOpen("input");
        }
        onKeyDown?.(event);
      }}
      className={cx(INPUT_CLASSES, ctx.hasError && INPUT_ERROR_CLASSES, className)}
      {...rest}
    />
  );
}

export function DatePickerTrigger({
  className,
  children,
  onClick,
  "aria-label": ariaLabel,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement>): ReactElement {
  const ctx = useDatePicker();
  const refs = useContext(DatePickerRefsContext);
  return (
    <button
      ref={refs.triggerRef}
      type="button"
      aria-label={ariaLabel ?? ctx.triggerLabel}
      aria-haspopup="dialog"
      aria-expanded={ctx.open}
      aria-controls={ctx.open ? ctx.panelId : undefined}
      disabled={ctx.disabled || ctx.readOnly}
      onClick={(event) => {
        ctx.toggleOpen("trigger");
        onClick?.(event);
      }}
      className={cx(TRIGGER_CLASSES, className)}
      {...rest}
    >
      {children ?? <CalendarGlyphIcon />}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* Popover content                                                           */
/* ------------------------------------------------------------------------ */

export interface DatePickerContentProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Mobile presentation: below the `sm` breakpoint the panel docks as a
   * full-width bottom sheet over a dimmed overlay (pure CSS — no viewport
   * JavaScript). At `sm` and up it stays a popover.
   */
  mobileSheet?: boolean;
}

export function DatePickerContent({
  mobileSheet = false,
  className,
  children,
  onKeyDown,
  ...rest
}: DatePickerContentProps): ReactElement | null {
  const ctx = useDatePicker();
  const refs = useContext(DatePickerRefsContext);
  const [side, setSide] = useState<"bottom" | "top">("bottom");
  const [align, setAlign] = useState<"start" | "end">("start");

  // Viewport correction: flip above the field when the space below runs out,
  // and pin to the field's right edge when the panel would overflow the
  // viewport's right edge. Class-driven (no inline styles). Placement is
  // computed from the field rect + the panel's own size only — never from
  // the panel's current placement — so the result is stable. Two passes: the
  // layout effect catches the common case pre-paint; the setTimeout pass
  // re-measures after runtime-injected CSS (e.g. a Tailwind CDN build) has
  // settled — with compiled CSS the second pass is a no-op.
  useLayoutEffect(() => {
    if (!ctx.open) return;
    const measure = () => {
      const panel = refs.panelRef.current;
      const box = panel?.parentElement;
      if (!panel || !box) return;
      const field = box.getBoundingClientRect();
      const panelHeight = panel.offsetHeight;
      const panelWidth = panel.offsetWidth;
      const margin = 8;
      const fitsBelow = field.bottom + panelHeight + margin <= window.innerHeight;
      const fitsAbove = field.top - panelHeight - margin >= 0;
      setSide(!fitsBelow && fitsAbove ? "top" : "bottom");
      setAlign(field.left + panelWidth + margin > window.innerWidth ? "end" : "start");
    };
    measure();
    const refine = window.setTimeout(measure, 0);
    return () => window.clearTimeout(refine);
  }, [ctx.open, ctx.month, ctx.view]);

  // Dismissal: Escape anywhere closes and restores focus; pointer interaction
  // outside the panel + field closes (restoring focus when the click landed
  // somewhere non-focusable, so focus is never stranded on <body>).
  const requestClose = ctx.requestClose;
  const open = ctx.open;
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") requestClose(true);
    };
    const onPointerDown = (event: PointerEvent) => {
      const target = event.target as Node | null;
      if (!target) return;
      const panel = refs.panelRef.current;
      const input = refs.inputRef.current;
      const trigger = refs.triggerRef.current;
      if (panel && panel.contains(target)) return;
      if (input && input.contains(target)) return;
      if (trigger && trigger.contains(target)) return;
      const focusable =
        target instanceof Element
          ? target.closest("button, a, input, select, textarea, [tabindex]")
          : null;
      if (!focusable) event.preventDefault();
      requestClose(!focusable);
    };
    document.addEventListener("keydown", onKey);
    document.addEventListener("pointerdown", onPointerDown);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("pointerdown", onPointerDown);
    };
  }, [open, requestClose, refs]);

  if (!open) return null;

  const dialogLabel =
    ctx.mode === "range"
      ? ctx.withTime
        ? "Choose date and time range"
        : "Choose date range"
      : ctx.withTime
        ? "Choose date and time"
        : "Choose date";

  const handleTab = (event: ReactKeyboardEvent<HTMLDivElement>) => {
    // Tab is never trapped: leaving the panel in either direction closes it
    // and lets the browser continue the natural focus order.
    if (event.key !== "Tab") return;
    const panel = refs.panelRef.current;
    if (!panel) return;
    const focusables = Array.from(
      panel.querySelectorAll<HTMLElement>(
        'button:not([disabled]), select:not([disabled]), input:not([disabled]), [tabindex="0"]',
      ),
    ).filter((el) => el.getClientRects().length > 0);
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (!first || !last) return;
    if (event.shiftKey && document.activeElement === first) requestClose(false);
    else if (!event.shiftKey && document.activeElement === last) requestClose(false);
  };

  return (
    <>
      {mobileSheet && <div aria-hidden="true" className={SHEET_OVERLAY_CLASSES} />}
      <div
        ref={refs.panelRef}
        role="dialog"
        aria-label={dialogLabel}
        id={ctx.panelId}
        onKeyDown={(event) => {
          handleTab(event);
          onKeyDown?.(event);
        }}
        className={cx(
          PANEL_CLASSES,
          side === "top" ? "bottom-full mb-1" : "top-full mt-1",
          align === "end" ? "right-0" : "left-0",
          mobileSheet && PANEL_SHEET_CLASSES,
          className,
        )}
        {...rest}
      >
        {children ?? (
          <>
            <DatePickerHeader />
            <DatePickerCalendar />
          </>
        )}
      </div>
    </>
  );
}

/* ------------------------------------------------------------------------ */
/* Header (month / year navigation)                                          */
/* ------------------------------------------------------------------------ */

export type DatePickerPartProps = HTMLAttributes<HTMLDivElement>;

export function DatePickerHeader({ className, children, ...rest }: DatePickerPartProps): ReactElement {
  const ctx = useDatePicker();
  return (
    <div className={cx("mb-1 flex items-center justify-between gap-1", className)} {...rest}>
      {children ?? (
        <>
          <button
            type="button"
            aria-label={ctx.previousLabel}
            disabled={!ctx.canGoPrevious}
            onClick={ctx.goToPrevious}
            className={NAV_BUTTON_CLASSES}
          >
            <ChevronLeftIcon />
          </button>
          <h2 aria-live="polite" aria-atomic="true" className={cx(HEADING_CLASSES, "flex-1 text-center")}>
            {ctx.view === "years" ? (
              ctx.headingLabel
            ) : (
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
            )}
          </h2>
          <button
            type="button"
            aria-label={ctx.nextLabel}
            disabled={!ctx.canGoNext}
            onClick={ctx.goToNext}
            className={NAV_BUTTON_CLASSES}
          >
            <ChevronRightIcon />
          </button>
        </>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* Calendar (day matrix + month / year pickers)                              */
/* ------------------------------------------------------------------------ */

export type DatePickerCalendarProps = HTMLAttributes<HTMLDivElement>;

export function DatePickerCalendar({ className, ...rest }: DatePickerCalendarProps): ReactElement {
  const ctx = useDatePicker();
  if (ctx.view === "months") return <MonthsPanel className={className} />;
  if (ctx.view === "years") return <YearsPanel className={className} />;

  const months = Array.from({ length: ctx.numberOfMonths }, (_, i) =>
    startOfMonth(addMonths(ctx.month, i)),
  );

  return (
    <div className={cx("flex flex-col gap-4 sm:flex-row", className)} {...rest}>
      {months.map((gridMonth) => (
        <MonthGrid key={dayKey(gridMonth)} gridMonth={gridMonth} />
      ))}
    </div>
  );
}

function MonthGrid({ gridMonth }: { gridMonth: Date }): ReactElement {
  const ctx = useDatePicker();
  const sizeClasses = SIZE_CLASSES[ctx.size];
  const weeks = buildMonthWeeks(gridMonth, ctx.weekStartsOn);
  const weekdays = weekdayNames(ctx.locale, ctx.weekStartsOn);

  return (
    <div role="grid" aria-label={monthYearLabel(gridMonth, ctx.locale)}>
      <div role="row" className="flex">
        {weekdays.map((day, i) => (
          <div
            role="columnheader"
            key={i}
            aria-label={day.long}
            className={cx(
              "flex items-center justify-center font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]",
              sizeClasses.cell,
              sizeClasses.weekday,
            )}
          >
            {day.short}
          </div>
        ))}
      </div>
      {weeks.map((week, rowIndex) => (
        <div role="row" className="flex" key={rowIndex}>
          {week.map((date) => (
            <DayCell key={dayKey(date)} date={date} gridMonth={gridMonth} />
          ))}
        </div>
      ))}
    </div>
  );
}

function DayCell({ date, gridMonth }: { date: Date; gridMonth: Date }): ReactElement {
  const ctx = useDatePicker();
  const sizeClasses = SIZE_CLASSES[ctx.size];
  const outside = date.getMonth() !== gridMonth.getMonth();
  const key = String(dayKey(date));
  const isDisabledDay = ctx.isDisabled(date);
  const selected = ctx.isSelected(date);
  const rangeStart = ctx.isRangeStart(date);
  const rangeEnd = ctx.isRangeEnd(date);
  const rangeMiddle = ctx.isRangeMiddle(date);
  const previewMiddle = ctx.isPreviewMiddle(date);
  const filled =
    (ctx.mode !== "range" && selected) ||
    rangeStart ||
    rangeEnd ||
    (ctx.mode === "range" && selected && !rangeMiddle);
  const isToday = isSameDay(date, ctx.today);

  return (
    <div role="gridcell" aria-selected={selected} className={sizeClasses.cell}>
      <button
        type="button"
        disabled={isDisabledDay}
        tabIndex={ctx.tabbableDayKey === dayKey(date) ? 0 : -1}
        data-dp-focus={key}
        aria-label={fullDateLabel(date, ctx.locale)}
        aria-current={isToday ? "date" : undefined}
        onClick={() => ctx.handleDayClick(date)}
        onPointerEnter={() => ctx.handleDayPointerEnter(date)}
        onPointerLeave={ctx.handleDayPointerLeave}
        onFocus={() => ctx.setFocusKey(key)}
        onKeyDown={(event) => ctx.handleDayKeyDown(event, date)}
        className={cx(
          DAY_BASE_CLASSES,
          sizeClasses.cell,
          sizeClasses.text,
          rangeMiddle && RANGE_MIDDLE_CLASSES,
          !rangeMiddle && previewMiddle && PREVIEW_MIDDLE_CLASSES,
          !rangeMiddle && !previewMiddle && filled && SELECTED_DAY_CLASSES,
          !rangeMiddle && !previewMiddle && !filled &&
            (outside ? "text-[var(--ds-color-muted-foreground)]" : "text-[var(--ds-color-foreground)]"),
          !rangeMiddle && !previewMiddle && !filled && "hover:bg-[var(--ds-color-surface-hover)]",
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

function MonthsPanel({ className }: { className?: string }): ReactElement {
  const ctx = useDatePicker();
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
                    data-dp-focus={key}
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
  const ctx = useDatePicker();
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
                    data-dp-focus={key}
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
/* Footer + actions                                                          */
/* ------------------------------------------------------------------------ */

export function DatePickerFooter({ className, children, ...rest }: DatePickerPartProps): ReactElement {
  return (
    <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export function DatePickerToday({
  className,
  children,
  onClick,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement>): ReactElement {
  const ctx = useDatePicker();
  return (
    <button
      type="button"
      disabled={ctx.todayDisabled}
      onClick={(event) => {
        ctx.selectToday();
        onClick?.(event);
      }}
      className={cx(ACTION_BUTTON_CLASSES, className)}
      {...rest}
    >
      {children ?? "Today"}
    </button>
  );
}

export function DatePickerClear({
  className,
  children,
  onClick,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement>): ReactElement {
  const ctx = useDatePicker();
  return (
    <button
      type="button"
      disabled={ctx.committedValue === null && ctx.stagedValue === null}
      onClick={(event) => {
        ctx.clearValue();
        onClick?.(event);
      }}
      className={cx(ACTION_BUTTON_CLASSES, className)}
      {...rest}
    >
      {children ?? "Clear"}
    </button>
  );
}

export function DatePickerApply({
  className,
  children,
  onClick,
  ...rest
}: ButtonHTMLAttributes<HTMLButtonElement>): ReactElement {
  const ctx = useDatePicker();
  return (
    <button
      type="button"
      disabled={!ctx.canApply}
      onClick={(event) => {
        ctx.applyDraft();
        onClick?.(event);
      }}
      className={cx(APPLY_BUTTON_CLASSES, className)}
      {...rest}
    >
      {children ?? (ctx.requireApply ? "Apply" : "Done")}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* Presets                                                                   */
/* ------------------------------------------------------------------------ */

export interface DatePickerPresetsProps extends HTMLAttributes<HTMLDivElement> {
  /** The preset options. Each `getValue(today)` must match the picker's `mode`. */
  presets: DatePickerPreset[];
  /** Accessible group label. Default "Date presets". */
  label?: string;
}

export function DatePickerPresets({
  presets,
  label = "Date presets",
  className,
  ...rest
}: DatePickerPresetsProps): ReactElement {
  const ctx = useDatePicker();
  return (
    <div
      role="group"
      aria-label={label}
      className={cx("flex flex-row flex-wrap gap-1 sm:w-36 sm:flex-col", className)}
      {...rest}
    >
      {presets.map((preset) => (
        <button
          key={preset.label}
          type="button"
          title={preset.description}
          aria-current={ctx.isPresetActive(preset) ? "date" : undefined}
          onClick={() => ctx.applyPreset(preset)}
          className={cx(PRESET_CLASSES, ctx.isPresetActive(preset) && PRESET_ACTIVE_CLASSES)}
        >
          {preset.label}
        </button>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* Time section (withTime)                                                   */
/* ------------------------------------------------------------------------ */

export function DatePickerTime({ className, ...rest }: HTMLAttributes<HTMLDivElement>): ReactElement {
  const ctx = useDatePicker();
  const step = Math.max(1, Math.min(60, ctx.timeStep));
  const minuteOptions: number[] = [];
  for (let m = 0; m < 60; m += step) minuteOptions.push(m);
  if (ctx.time && !minuteOptions.includes(ctx.time.minutes)) {
    minuteOptions.push(ctx.time.minutes);
    minuteOptions.sort((a, b) => a - b);
  }
  const noDate = ctx.time === null;

  return (
    <div className={cx("mt-2 border-t border-[var(--ds-color-border-subtle)] pt-3", className)} {...rest}>
      <div className="flex items-end gap-2">
        <label className="flex flex-col gap-1">
          <span className="text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]">
            Hours
          </span>
          <select
            value={ctx.time ? String(ctx.time.hours) : "12"}
            disabled={noDate}
            onChange={(event) => ctx.setTime(Number(event.target.value), ctx.time?.minutes ?? 0)}
            className={TIME_SELECT_CLASSES}
          >
            {Array.from({ length: 24 }, (_, h) => (
              <option key={h} value={h}>
                {String(h).padStart(2, "0")}
              </option>
            ))}
          </select>
        </label>
        <span aria-hidden="true" className="pb-2 text-sm text-[var(--ds-color-muted-foreground)]">
          :
        </span>
        <label className="flex flex-col gap-1">
          <span className="text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]">
            Minutes
          </span>
          <select
            value={ctx.time ? String(ctx.time.minutes) : "0"}
            disabled={noDate}
            onChange={(event) => ctx.setTime(ctx.time?.hours ?? 12, Number(event.target.value))}
            className={TIME_SELECT_CLASSES}
          >
            {minuteOptions.map((m) => (
              <option key={m} value={m}>
                {String(m).padStart(2, "0")}
              </option>
            ))}
          </select>
        </label>
        {noDate && (
          <p className="m-0 pb-2 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
            Select a date to set the time.
          </p>
        )}
      </div>
    </div>
  );
}

export default DatePicker;
