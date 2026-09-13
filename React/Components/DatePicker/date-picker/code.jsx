/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useLayoutEffect,
  useMemo,
  useRef,
  useState
} from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
function daysInMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}
function isLeapYear(year) {
  return new Date(year, 1, 29).getMonth() === 1;
}
function dayKey(date) {
  return date.getFullYear() * 1e4 + (date.getMonth() + 1) * 100 + date.getDate();
}
function dateFromKey(key) {
  const year = Math.floor(key / 1e4);
  const month = Math.floor(key % 1e4 / 100) - 1;
  return new Date(year, month, key % 100);
}
function compareDays(a, b) {
  const diff = dayKey(a) - dayKey(b);
  return diff === 0 ? 0 : diff < 0 ? -1 : 1;
}
function isSameDay(a, b) {
  return dayKey(a) === dayKey(b);
}
function addDays(date, amount) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + amount);
}
function addMonths(date, amount) {
  const first = new Date(date.getFullYear(), date.getMonth() + amount, 1);
  const day = Math.min(date.getDate(), daysInMonth(first.getFullYear(), first.getMonth()));
  return new Date(first.getFullYear(), first.getMonth(), day);
}
function startOfMonth(date) {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}
function endOfMonth(date) {
  const year = date.getFullYear();
  const month = date.getMonth();
  return new Date(year, month, daysInMonth(year, month));
}
function buildMonthWeeks(month, weekStartsOn) {
  const first = startOfMonth(month);
  const leading = (first.getDay() - weekStartsOn + 7) % 7;
  const gridStart = addDays(first, -leading);
  const weeks = [];
  for (let w = 0; w < 6; w += 1) {
    const row = [];
    for (let d = 0; d < 7; d += 1) row.push(addDays(gridStart, w * 7 + d));
    weeks.push(row);
  }
  return weeks;
}
function formatISODate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}
function formatISODateTime(date) {
  const hh = String(date.getHours()).padStart(2, "0");
  const mm = String(date.getMinutes()).padStart(2, "0");
  return `${formatISODate(date)}T${hh}:${mm}`;
}
function monthYearLabel(date, locale) {
  return new Intl.DateTimeFormat(locale, { month: "long", year: "numeric" }).format(date);
}
function monthName(date, locale) {
  return new Intl.DateTimeFormat(locale, { month: "long" }).format(date);
}
function yearLabel(year, locale) {
  return new Intl.DateTimeFormat(locale, { year: "numeric" }).format(new Date(year, 0, 1));
}
function fullDateLabel(date, locale) {
  return new Intl.DateTimeFormat(locale, {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric"
  }).format(date);
}
function monthNames(locale) {
  const fmt = new Intl.DateTimeFormat(locale, { month: "long" });
  return Array.from({ length: 12 }, (_, m) => fmt.format(new Date(2024, m, 1)));
}
function weekdayNames(locale, weekStartsOn) {
  const base = new Date(2024, 0, 7);
  const shortFmt = new Intl.DateTimeFormat(locale, { weekday: "short" });
  const longFmt = new Intl.DateTimeFormat(locale, { weekday: "long" });
  return Array.from({ length: 7 }, (_, i) => {
    const day = addDays(base, (weekStartsOn + i) % 7);
    return { short: shortFmt.format(day), long: longFmt.format(day) };
  });
}
function useControllableState(controlled, defaultValue, onChange) {
  const [internal, setInternal] = useState(defaultValue);
  const isControlled = controlled !== undefined;
  const value = isControlled ? controlled : internal;
  const set = useCallback(
    (next) => {
      if (!isControlled) setInternal(next);
      if (onChange) onChange(next);
    },
    [isControlled, onChange]
  );
  return [value, set];
}
const DatePickerContext = createContext(null);
function useDatePicker() {
  const ctx = useContext(DatePickerContext);
  if (!ctx) throw new Error("DatePicker components must be composed inside <DatePicker>.");
  return ctx;
}
const DatePickerRefsContext = createContext({
  inputRef: { current: null },
  triggerRef: { current: null },
  panelRef: { current: null }
});
const INPUT_CLASSES = "h-9 w-full cursor-default rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none";
const INPUT_ERROR_CLASSES = "border-[var(--ds-color-destructive)] hover:border-[var(--ds-color-destructive)]";
const TRIGGER_CLASSES = "inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const PANEL_CLASSES = "absolute z-50 w-max max-w-[calc(100vw-1rem)] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-3 shadow-[var(--ds-shadow-md)]";
const PANEL_SHEET_CLASSES = "max-sm:fixed max-sm:inset-x-3 max-sm:bottom-3 max-sm:top-auto max-sm:mt-0 max-sm:w-auto max-sm:max-w-none max-sm:max-h-[75dvh] max-sm:overflow-y-auto";
const SHEET_OVERLAY_CLASSES = "fixed inset-0 z-40 bg-[var(--ds-color-overlay)] sm:hidden";
const NAV_BUTTON_CLASSES = TRIGGER_CLASSES;
const HEADING_CLASSES = "m-0 text-sm font-semibold leading-9 text-[var(--ds-color-foreground)]";
const HEADING_BUTTON_CLASSES = "-mx-1.5 rounded-[var(--ds-radius-sm)] px-1.5 transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const DAY_BASE_CLASSES = "inline-flex items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent leading-5 tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none";
const PICKER_BUTTON_CLASSES = "flex h-9 flex-1 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent px-2 text-sm leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none";
const FOOTER_CLASSES = "mt-2 flex flex-wrap items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-2";
const PRESET_CLASSES = "inline-flex h-8 w-full items-center justify-start rounded-[var(--ds-radius-sm)] px-2 text-left text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const PRESET_ACTIVE_CLASSES = "bg-[var(--ds-color-surface-active)] font-medium";
const ACTION_BUTTON_CLASSES = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-2.5 text-xs font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const APPLY_BUTTON_CLASSES = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-2.5 text-xs font-medium leading-4 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const TIME_SELECT_CLASSES = "h-9 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-2 text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none";
const SELECTED_DAY_CLASSES = "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)]";
const RANGE_MIDDLE_CLASSES = "rounded-none bg-[var(--ds-color-surface-active)] text-[var(--ds-color-foreground)]";
const PREVIEW_MIDDLE_CLASSES = "rounded-none bg-[var(--ds-color-surface-hover)] text-[var(--ds-color-foreground)]";
const PICKER_SELECTED_CLASSES = "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)]";
const SIZE_CLASSES = {
  md: { cell: "size-9", text: "text-sm", weekday: "text-[11px]" },
  lg: { cell: "size-11", text: "text-sm", weekday: "text-xs" }
};
function CalendarGlyphIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
      <line x1="16" x2="16" y1="2" y2="6" />
      <line x1="8" x2="8" y1="2" y2="6" />
      <line x1="3" x2="21" y1="10" y2="10" />
    </svg>;
}
function ChevronLeftIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <path d="m15 18-6-6 6-6" />
    </svg>;
}
function ChevronRightIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      <path d="m9 18 6-6-6-6" />
    </svg>;
}
function firstDateOf(value) {
  if (!value) return null;
  return value instanceof Date ? value : value.from;
}
function DatePicker(props) {
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
  const mode = _mode ?? "single";
  const singleSlice = props;
  const rangeSlice = props;
  const [singleValue, setSingleValue] = useControllableState(
    mode === "single" ? singleSlice.value : undefined,
    (mode === "single" ? singleSlice.defaultValue : null) ?? null,
    mode === "single" ? singleSlice.onChange : undefined
  );
  const [rangeValue, setRangeValue] = useControllableState(
    mode === "range" ? rangeSlice.value : undefined,
    (mode === "range" ? rangeSlice.defaultValue : undefined) ?? null,
    mode === "range" ? rangeSlice.onChange : undefined
  );
  const committedValue = mode === "single" ? singleValue : rangeValue;
  const commitValue = useCallback(
    (next) => {
      if (mode === "single") setSingleValue(next === null || next instanceof Date ? next : next.from);
      else setRangeValue(next instanceof Date ? { from: next, to: null } : next);
    },
    [mode, setSingleValue, setRangeValue]
  );
  const [open, setOpen] = useControllableState(controlledOpen, defaultOpen, onOpenChange);
  const [today] = useState(() => /* @__PURE__ */ new Date());
  const formatDate = useCallback(
    (date) => {
      if (formatDateProp) return formatDateProp(date);
      return new Intl.DateTimeFormat(
        locale,
        withTime ? { dateStyle: "medium", timeStyle: "short", hourCycle: "h23" } : { dateStyle: "medium" }
      ).format(date);
    },
    [formatDateProp, locale, withTime]
  );
  const formatValue = useCallback(
    (value) => {
      if (!value) return "";
      if (value instanceof Date) return formatDate(value);
      if (!value.to) return `${formatDate(value.from)} \u2013 \u2026`;
      return `${formatDate(value.from)} \u2013 ${formatDate(value.to)}`;
    },
    [formatDate]
  );
  const placeholder = placeholderProp ?? (mode === "range" ? "Select date range" : "Select date");
  const resolvedInputAriaLabel = inputAriaLabel ?? (mode === "range" ? "Date range" : "Date");
  const [monthState, setMonthState] = useState(
    () => startOfMonth(defaultMonth ?? firstDateOf(committedValue) ?? today)
  );
  const monthKey = monthState.getFullYear() * 12 + monthState.getMonth();
  const month = useMemo(() => startOfMonth(monthState), [monthKey]);
  const [view, setView] = useState(defaultView);
  const [focusKey, setFocusKey] = useState(null);
  const focusIntentRef = useRef(null);
  const [hoveredDate, setHoveredDate] = useState(null);
  const inputRef = useRef(null);
  const triggerRef = useRef(null);
  const panelRef = useRef(null);
  const restoreTargetRef = useRef(null);
  const restoreRequestedRef = useRef(false);
  const isDisabled = useCallback(
    (date) => {
      if (minDate && compareDays(date, minDate) < 0) return true;
      if (maxDate && compareDays(date, maxDate) > 0) return true;
      return disabledDates ? disabledDates(date) : false;
    },
    [minDate, maxDate, disabledDates]
  );
  const monthEnabled = useCallback(
    (year, monthIndex) => {
      if (minDate && compareDays(endOfMonth(new Date(year, monthIndex, 1)), minDate) < 0) return false;
      if (maxDate && compareDays(new Date(year, monthIndex, 1), maxDate) > 0) return false;
      return true;
    },
    [minDate, maxDate]
  );
  const yearEnabled = useCallback(
    (year) => {
      if (minDate && compareDays(new Date(year, 11, 31), minDate) < 0) return false;
      if (maxDate && compareDays(new Date(year, 0, 1), maxDate) > 0) return false;
      return true;
    },
    [minDate, maxDate]
  );
  const lastVisibleMonth = useMemo(
    () => startOfMonth(addMonths(month, numberOfMonths - 1)),
    [month, numberOfMonths]
  );
  const isRenderedDate = useCallback(
    (date) => compareDays(date, month) >= 0 && compareDays(date, endOfMonth(lastVisibleMonth)) <= 0,
    [month, lastVisibleMonth]
  );
  const goToMonth = useCallback(
    (target) => {
      let t = startOfMonth(target);
      if (maxDate) {
        const latest = startOfMonth(addMonths(maxDate, -(numberOfMonths - 1)));
        if (compareDays(t, latest) > 0) t = latest;
      }
      if (minDate && compareDays(t, startOfMonth(minDate)) < 0) t = startOfMonth(minDate);
      setMonthState(t);
    },
    [minDate, maxDate, numberOfMonths]
  );
  const monthToReveal = useCallback(
    (date) => {
      if (compareDays(date, month) < 0) return startOfMonth(date);
      if (compareDays(date, endOfMonth(lastVisibleMonth)) > 0) {
        return startOfMonth(addMonths(date, -(numberOfMonths - 1)));
      }
      return month;
    },
    [month, lastVisibleMonth, numberOfMonths]
  );
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
  const previousLabel = view === "days" ? "Go to previous month" : view === "months" ? "Go to previous year" : "Go to previous 12 years";
  const nextLabel = view === "days" ? "Go to next month" : view === "months" ? "Go to next year" : "Go to next 12 years";
  const headingLabel = useMemo(() => {
    if (view === "months") return yearLabel(month.getFullYear(), locale);
    if (view === "years") {
      const pageStart = Math.floor(month.getFullYear() / 12) * 12;
      return `${yearLabel(pageStart, locale)} \u2013 ${yearLabel(pageStart + 11, locale)}`;
    }
    if (numberOfMonths === 1) return monthYearLabel(month, locale);
    const last = addMonths(month, numberOfMonths - 1);
    if (month.getFullYear() === last.getFullYear()) {
      return `${monthName(month, locale)} \u2013 ${monthYearLabel(last, locale)}`;
    }
    return `${monthYearLabel(month, locale)} \u2013 ${monthYearLabel(last, locale)}`;
  }, [view, month, numberOfMonths, locale]);
  const yearPage = useMemo(() => {
    const pageStart = Math.floor(month.getFullYear() / 12) * 12;
    return Array.from({ length: 12 }, (_, i) => pageStart + i);
  }, [month]);
  const requestOpen = useCallback(
    (_origin) => {
      if (disabled || readOnly || open) return;
      restoreTargetRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
      setOpen(true);
    },
    [disabled, readOnly, open, setOpen]
  );
  const requestClose = useCallback(
    (restoreFocus) => {
      if (!open) return;
      if (restoreFocus) restoreRequestedRef.current = true;
      setOpen(false);
    },
    [open, setOpen]
  );
  const toggleOpen = useCallback(
    (origin) => {
      if (open) requestClose(true);
      else requestOpen(origin);
    },
    [open, requestOpen, requestClose]
  );
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
    if (defaultView === "months") {
      requestFocus(`m${reveal.getMonth()}`);
      return;
    }
    if (defaultView === "years") {
      requestFocus(`y${reveal.getFullYear()}`);
      return;
    }
    const renderedEnd = endOfMonth(startOfMonth(addMonths(reveal, numberOfMonths - 1)));
    const rendered = (d) => compareDays(d, reveal) >= 0 && compareDays(d, renderedEnd) <= 0;
    let target = null;
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
  }, [open]);
  useEffect(() => {
    if (open || !restoreRequestedRef.current) return;
    restoreRequestedRef.current = false;
    const target = restoreTargetRef.current;
    restoreTargetRef.current = null;
    if (target && target.isConnected) target.focus();
  }, [open]);
  const [draft, setDraft] = useState(committedValue);
  useEffect(() => {
    if (!open) setDraft(committedValue);
  }, [open, committedValue]);
  const stagedValue = requireApply ? draft : committedValue;
  const rangeCrossesDisabled = useCallback(
    (from, to) => {
      let cursor = addDays(from, 1);
      for (let i = 0; i < 3700 && compareDays(cursor, to) < 0; i += 1) {
        if (isDisabled(cursor)) return true;
        cursor = addDays(cursor, 1);
      }
      return false;
    },
    [isDisabled]
  );
  const withCurrentTime = useCallback(
    (day) => {
      if (!withTime) return day;
      const base = firstDateOf(stagedValue);
      const hours = base ? base.getHours() : 12;
      const minutes = base ? base.getMinutes() : 0;
      return new Date(day.getFullYear(), day.getMonth(), day.getDate(), hours, minutes);
    },
    [withTime, stagedValue]
  );
  const selectDate = useCallback(
    (date) => {
      if (isDisabled(date)) return;
      const day = withCurrentTime(date);
      if (mode === "single") {
        if (requireApply) {
          setDraft(day);
          return;
        }
        if (singleValue && isSameDay(singleValue, day)) {
          if (!withTime) requestClose(true);
          return;
        }
        commitValue(day);
        if (!withTime) requestClose(true);
        return;
      }
      const current = stagedValue instanceof Date || stagedValue === null ? null : stagedValue;
      let next;
      if (!current || current.to) {
        next = { from: day, to: null };
      } else if (isSameDay(day, current.from)) {
        next = { from: current.from, to: current.from };
      } else if (compareDays(day, current.from) < 0 || rangeCrossesDisabled(current.from, day)) {
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
      rangeCrossesDisabled
    ]
  );
  const clearValue = useCallback(() => {
    commitValue(null);
    setDraft(null);
    setHoveredDate(null);
  }, [commitValue]);
  const canApply = mode === "single" || stagedValue === null || stagedValue instanceof Date || stagedValue.to !== null;
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
    (preset) => {
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
    [today, mode, requireApply, commitValue, goToMonth, monthToReveal, requestClose]
  );
  const isPresetActive = useCallback(
    (preset) => {
      const value = preset.getValue(today);
      const current = stagedValue;
      if (value instanceof Date) return current instanceof Date && isSameDay(value, current);
      if (current === null || current instanceof Date || current.to === null) return false;
      return isSameDay(value.from, current.from) && isSameDay(value.to ?? value.from, current.to);
    },
    [today, stagedValue]
  );
  const time = useMemo(() => {
    if (!withTime) return null;
    const base = firstDateOf(stagedValue);
    return base ? { hours: base.getHours(), minutes: base.getMinutes() } : null;
  }, [withTime, stagedValue]);
  const setTime = useCallback(
    (hours, minutes) => {
      if (!withTime) return;
      const base = stagedValue;
      if (!base) return;
      const merge = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), hours, minutes);
      const next = base instanceof Date ? merge(base) : { from: merge(base.from), to: base.to ? merge(base.to) : null };
      if (requireApply) setDraft(next);
      else commitValue(next);
    },
    [withTime, stagedValue, requireApply, commitValue]
  );
  const rangeState = stagedValue instanceof Date || stagedValue === null ? null : stagedValue;
  const isRangeStart = useCallback(
    (date) => mode === "range" && rangeState !== null && rangeState.to !== null && !isSameDay(rangeState.from, rangeState.to) && isSameDay(rangeState.from, date),
    [mode, rangeState]
  );
  const isRangeEnd = useCallback(
    (date) => mode === "range" && rangeState !== null && rangeState.to !== null && !isSameDay(rangeState.from, rangeState.to) && isSameDay(rangeState.to, date),
    [mode, rangeState]
  );
  const isRangeMiddle = useCallback(
    (date) => mode === "range" && rangeState !== null && rangeState.to !== null && compareDays(date, rangeState.from) > 0 && compareDays(date, rangeState.to) < 0,
    [mode, rangeState]
  );
  const isPreviewMiddle = useCallback(
    (date) => {
      if (mode !== "range" || !rangeState || rangeState.to !== null || !hoveredDate) return false;
      if (compareDays(hoveredDate, rangeState.from) <= 0) return false;
      return compareDays(date, rangeState.from) > 0 && compareDays(date, hoveredDate) < 0;
    },
    [mode, rangeState, hoveredDate]
  );
  const isSelected = useCallback(
    (date) => {
      if (mode === "single") return stagedValue instanceof Date && isSameDay(stagedValue, date);
      return rangeState !== null && (isSameDay(rangeState.from, date) || rangeState.to !== null && compareDays(date, rangeState.from) > 0 && compareDays(date, rangeState.to) <= 0);
    },
    [mode, stagedValue, rangeState]
  );
  const handleDayClick = useCallback((date) => selectDate(date), [selectDate]);
  const handleDayPointerEnter = useCallback(
    (date) => {
      if (mode === "range" && rangeState && rangeState.to === null) setHoveredDate(date);
    },
    [mode, rangeState]
  );
  const handleDayPointerLeave = useCallback(() => setHoveredDate(null), []);
  const focusedDay = useMemo(() => {
    if (focusKey && /^\d{8}$/.test(focusKey)) return dateFromKey(Number(focusKey));
    return null;
  }, [focusKey]);
  const firstStagedDate = firstDateOf(stagedValue);
  const tabbableDayKey = useMemo(() => {
    const candidates = [focusedDay, firstStagedDate, today];
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
  const monthActiveKey = useMemo(() => {
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
  const yearActiveKey = useMemo(() => {
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
  const requestFocus = useCallback((key) => {
    focusIntentRef.current = key;
    setFocusKey(key);
  }, []);
  useEffect(() => {
    if (!open || focusKey == null) return;
    const panel = panelRef.current;
    if (!panel) return;
    const intent = focusIntentRef.current;
    focusIntentRef.current = null;
    if (!intent && !panel.contains(document.activeElement)) return;
    const el = panel.querySelector(`[data-dp-focus="${intent ?? focusKey}"]`);
    if (el && el !== document.activeElement) el.focus();
  }, [open, focusKey, monthKey, view]);
  const stepToEnabled = useCallback(
    (start, step) => {
      let cursor = start;
      for (let i = 0; i < 732; i += 1) {
        if (!isDisabled(cursor)) return cursor;
        cursor = step(cursor);
      }
      return null;
    },
    [isDisabled]
  );
  const handleDayKeyDown = useCallback(
    (event, date) => {
      let target;
      let step;
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
          target = addDays(date, 6 - (date.getDay() - weekStartsOn + 7) % 7);
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
    [weekStartsOn, stepToEnabled, isRenderedDate, goToMonth, monthToReveal, requestFocus]
  );
  const handleMonthKeyDown = useCallback(
    (event, monthIndex) => {
      const year = month.getFullYear();
      const norm = (y, m) => ({
        y: y + Math.floor(m / 12),
        m: (m % 12 + 12) % 12
      });
      let target;
      let step;
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
    [month, monthEnabled, goToMonth, requestFocus]
  );
  const handleYearKeyDown = useCallback(
    (event, year) => {
      let target;
      let step;
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
    [month, yearPage, yearEnabled, goToMonth, requestFocus]
  );
  const selectMonth = useCallback(
    (monthIndex) => {
      const year = month.getFullYear();
      const anchor = focusedDay ?? firstStagedDate ?? today;
      const day = Math.min(anchor.getDate(), daysInMonth(year, monthIndex));
      let target = new Date(year, monthIndex, day);
      if (isDisabled(target)) {
        target = stepToEnabled(target, (d) => addDays(d, 1)) ?? stepToEnabled(target, (d) => addDays(d, -1)) ?? new Date(year, monthIndex, 1);
      }
      goToMonth(new Date(year, monthIndex, 1));
      setView("days");
      requestFocus(String(dayKey(target)));
    },
    [month, focusedDay, firstStagedDate, today, isDisabled, stepToEnabled, goToMonth, requestFocus]
  );
  const selectYear = useCallback(
    (year) => {
      goToMonth(new Date(year, month.getMonth(), 1));
      setView("months");
      requestFocus(`m${month.getMonth()}`);
    },
    [month, goToMonth, requestFocus]
  );
  const baseId = useId().replace(/:/g, "");
  const inputId = `${baseId}-input`;
  const panelId = `${baseId}-panel`;
  const descriptionId = description !== undefined ? `${baseId}-description` : null;
  const hasError = typeof error === "string" && error.length > 0;
  const messageId = hasError ? `${baseId}-error` : helperText !== undefined ? `${baseId}-helper` : null;
  const describedBy = [descriptionId, messageId].filter(Boolean).join(" ") || undefined;
  const isoValue = useMemo(() => {
    if (!committedValue) return "";
    if (committedValue instanceof Date) {
      return withTime ? formatISODateTime(committedValue) : formatISODate(committedValue);
    }
    const from = formatISODate(committedValue.from);
    const to = committedValue.to ? formatISODate(committedValue.to) : "";
    return `${from}/${to}`;
  }, [committedValue, withTime]);
  const displayValue = formatValue(committedValue);
  const contextValue = {
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
    timeStep
  };
  const refsValue = useMemo(
    () => ({ inputRef, triggerRef, panelRef }),
    []
  );
  const hasFieldChrome = label !== undefined || description !== undefined || helperText !== undefined || hasError;
  const hiddenInput = name !== undefined && <input type="hidden" name={name} value={isoValue} disabled={disabled} readOnly />;
  return <DatePickerContext.Provider value={contextValue}>
      <DatePickerRefsContext.Provider value={refsValue}>
        {hasFieldChrome ? <div className={cx("w-full max-w-xs space-y-1.5", className)} {...rest}>
            {label !== undefined && <label
    htmlFor={inputId}
    className="block text-sm font-medium leading-5 text-[var(--ds-color-foreground)]"
  >
                {label}
                {required && <span aria-hidden="true" className="text-[var(--ds-color-destructive)]">
                    {" *"}
                  </span>}
              </label>}
            {description !== undefined && <p
    id={descriptionId ?? undefined}
    className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
  >
                {description}
              </p>}
            <div className="relative flex items-center gap-1">
              {children}
              {hiddenInput}
            </div>
            {hasError ? <p
    id={messageId ?? undefined}
    role="alert"
    className="m-0 text-xs font-medium leading-4 text-[var(--ds-color-destructive)]"
  >
                {error}
              </p> : helperText !== undefined && <p
    id={messageId ?? undefined}
    className="m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
  >
                  {helperText}
                </p>}
          </div> : <div className={cx("relative flex w-full max-w-xs items-center gap-1", className)} {...rest}>
            {children}
            {hiddenInput}
          </div>}
      </DatePickerRefsContext.Provider>
    </DatePickerContext.Provider>;
}
function DatePickerInput({
  className,
  id,
  onClick,
  onKeyDown,
  "aria-label": ariaLabel,
  "aria-describedby": ariaDescribedBy,
  ...rest
}) {
  const ctx = useDatePicker();
  const refs = useContext(DatePickerRefsContext);
  return <input
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
      if (!ctx.open && (event.key === "ArrowDown" || event.key === "ArrowUp" || event.key === "Enter" || event.key === " ")) {
        event.preventDefault();
        ctx.requestOpen("input");
      }
      onKeyDown?.(event);
    }}
    className={cx(INPUT_CLASSES, ctx.hasError && INPUT_ERROR_CLASSES, className)}
    {...rest}
  />;
}
function DatePickerTrigger({
  className,
  children,
  onClick,
  "aria-label": ariaLabel,
  ...rest
}) {
  const ctx = useDatePicker();
  const refs = useContext(DatePickerRefsContext);
  return <button
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
    </button>;
}
function DatePickerContent({
  mobileSheet = false,
  className,
  children,
  onKeyDown,
  ...rest
}) {
  const ctx = useDatePicker();
  const refs = useContext(DatePickerRefsContext);
  const [side, setSide] = useState("bottom");
  const [align, setAlign] = useState("start");
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
  const requestClose = ctx.requestClose;
  const open = ctx.open;
  useEffect(() => {
    if (!open) return;
    const onKey = (event) => {
      if (event.key === "Escape") requestClose(true);
    };
    const onPointerDown = (event) => {
      const target = event.target;
      if (!target) return;
      const panel = refs.panelRef.current;
      const input = refs.inputRef.current;
      const trigger = refs.triggerRef.current;
      if (panel && panel.contains(target)) return;
      if (input && input.contains(target)) return;
      if (trigger && trigger.contains(target)) return;
      const focusable = target instanceof Element ? target.closest("button, a, input, select, textarea, [tabindex]") : null;
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
  const dialogLabel = ctx.mode === "range" ? ctx.withTime ? "Choose date and time range" : "Choose date range" : ctx.withTime ? "Choose date and time" : "Choose date";
  const handleTab = (event) => {
    if (event.key !== "Tab") return;
    const panel = refs.panelRef.current;
    if (!panel) return;
    const focusables = Array.from(
      panel.querySelectorAll(
        'button:not([disabled]), select:not([disabled]), input:not([disabled]), [tabindex="0"]'
      )
    ).filter((el) => el.getClientRects().length > 0);
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (!first || !last) return;
    if (event.shiftKey && document.activeElement === first) requestClose(false);
    else if (!event.shiftKey && document.activeElement === last) requestClose(false);
  };
  return <>
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
      className
    )}
    {...rest}
  >
        {children ?? <>
            <DatePickerHeader />
            <DatePickerCalendar />
          </>}
      </div>
    </>;
}
function DatePickerHeader({ className, children, ...rest }) {
  const ctx = useDatePicker();
  return <div className={cx("mb-1 flex items-center justify-between gap-1", className)} {...rest}>
      {children ?? <>
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
            {ctx.view === "years" ? ctx.headingLabel : <button
    type="button"
    onClick={() => ctx.setView(ctx.view === "days" ? "months" : "years")}
    aria-label={ctx.view === "days" ? `${ctx.headingLabel} \u2014 activate to choose a month` : `${ctx.headingLabel} \u2014 activate to choose a year`}
    className={HEADING_BUTTON_CLASSES}
  >
                {ctx.headingLabel}
              </button>}
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
        </>}
    </div>;
}
function DatePickerCalendar({ className, ...rest }) {
  const ctx = useDatePicker();
  if (ctx.view === "months") return <MonthsPanel className={className} />;
  if (ctx.view === "years") return <YearsPanel className={className} />;
  const months = Array.from(
    { length: ctx.numberOfMonths },
    (_, i) => startOfMonth(addMonths(ctx.month, i))
  );
  return <div className={cx("flex flex-col gap-4 sm:flex-row", className)} {...rest}>
      {months.map((gridMonth) => <MonthGrid key={dayKey(gridMonth)} gridMonth={gridMonth} />)}
    </div>;
}
function MonthGrid({ gridMonth }) {
  const ctx = useDatePicker();
  const sizeClasses = SIZE_CLASSES[ctx.size];
  const weeks = buildMonthWeeks(gridMonth, ctx.weekStartsOn);
  const weekdays = weekdayNames(ctx.locale, ctx.weekStartsOn);
  return <div role="grid" aria-label={monthYearLabel(gridMonth, ctx.locale)}>
      <div role="row" className="flex">
        {weekdays.map((day, i) => <div
    role="columnheader"
    key={i}
    aria-label={day.long}
    className={cx(
      "flex items-center justify-center font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]",
      sizeClasses.cell,
      sizeClasses.weekday
    )}
  >
            {day.short}
          </div>)}
      </div>
      {weeks.map((week, rowIndex) => <div role="row" className="flex" key={rowIndex}>
          {week.map((date) => <DayCell key={dayKey(date)} date={date} gridMonth={gridMonth} />)}
        </div>)}
    </div>;
}
function DayCell({ date, gridMonth }) {
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
  const filled = ctx.mode !== "range" && selected || rangeStart || rangeEnd || ctx.mode === "range" && selected && !rangeMiddle;
  const isToday = isSameDay(date, ctx.today);
  return <div role="gridcell" aria-selected={selected} className={sizeClasses.cell}>
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
      !rangeMiddle && !previewMiddle && !filled && (outside ? "text-[var(--ds-color-muted-foreground)]" : "text-[var(--ds-color-foreground)]"),
      !rangeMiddle && !previewMiddle && !filled && "hover:bg-[var(--ds-color-surface-hover)]",
      rangeStart && "rounded-r-none",
      rangeEnd && "rounded-l-none",
      isToday && "border-[var(--ds-color-border-strong)] font-semibold",
      isDisabledDay && "opacity-40"
    )}
  >
        {date.getDate()}
      </button>
    </div>;
}
function MonthsPanel({ className }) {
  const ctx = useDatePicker();
  const year = ctx.month.getFullYear();
  const names = monthNames(ctx.locale);
  const rows = [];
  for (let r = 0; r < 4; r += 1) rows.push([r * 3, r * 3 + 1, r * 3 + 2]);
  return <div className={className}>
      <div role="grid" aria-label={`Choose a month in ${yearLabel(year, ctx.locale)}`}>
        {rows.map((row, r) => <div role="row" className="flex gap-1" key={r}>
            {row.map((m) => {
    const key = `m${m}`;
    const enabled = ctx.monthEnabled(year, m);
    const isCurrent = m === ctx.month.getMonth();
    return <div role="gridcell" aria-selected={isCurrent} className="flex-1" key={m}>
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
        isCurrent ? PICKER_SELECTED_CLASSES : "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]"
      )}
    >
                    {names[m]}
                  </button>
                </div>;
  })}
          </div>)}
      </div>
    </div>;
}
function YearsPanel({ className }) {
  const ctx = useDatePicker();
  const rows = [];
  for (let r = 0; r < 4; r += 1) rows.push(ctx.yearPage.slice(r * 3, r * 3 + 3));
  return <div className={className}>
      <div role="grid" aria-label="Choose a year">
        {rows.map((row, r) => <div role="row" className="flex gap-1" key={r}>
            {row.map((year) => {
    const key = `y${year}`;
    const enabled = ctx.yearEnabled(year);
    const isCurrent = year === ctx.month.getFullYear();
    return <div role="gridcell" aria-selected={isCurrent} className="flex-1" key={year}>
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
        isCurrent ? PICKER_SELECTED_CLASSES : "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]"
      )}
    >
                    {yearLabel(year, ctx.locale)}
                  </button>
                </div>;
  })}
          </div>)}
      </div>
    </div>;
}
function DatePickerFooter({ className, children, ...rest }) {
  return <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function DatePickerToday({
  className,
  children,
  onClick,
  ...rest
}) {
  const ctx = useDatePicker();
  return <button
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
    </button>;
}
function DatePickerClear({
  className,
  children,
  onClick,
  ...rest
}) {
  const ctx = useDatePicker();
  return <button
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
    </button>;
}
function DatePickerApply({
  className,
  children,
  onClick,
  ...rest
}) {
  const ctx = useDatePicker();
  return <button
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
    </button>;
}
function DatePickerPresets({
  presets,
  label = "Date presets",
  className,
  ...rest
}) {
  const ctx = useDatePicker();
  return <div
    role="group"
    aria-label={label}
    className={cx("flex flex-row flex-wrap gap-1 sm:w-36 sm:flex-col", className)}
    {...rest}
  >
      {presets.map((preset) => <button
    key={preset.label}
    type="button"
    title={preset.description}
    aria-current={ctx.isPresetActive(preset) ? "date" : undefined}
    onClick={() => ctx.applyPreset(preset)}
    className={cx(PRESET_CLASSES, ctx.isPresetActive(preset) && PRESET_ACTIVE_CLASSES)}
  >
          {preset.label}
        </button>)}
    </div>;
}
function DatePickerTime({ className, ...rest }) {
  const ctx = useDatePicker();
  const step = Math.max(1, Math.min(60, ctx.timeStep));
  const minuteOptions = [];
  for (let m = 0; m < 60; m += step) minuteOptions.push(m);
  if (ctx.time && !minuteOptions.includes(ctx.time.minutes)) {
    minuteOptions.push(ctx.time.minutes);
    minuteOptions.sort((a, b) => a - b);
  }
  const noDate = ctx.time === null;
  return <div className={cx("mt-2 border-t border-[var(--ds-color-border-subtle)] pt-3", className)} {...rest}>
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
            {Array.from({ length: 24 }, (_, h) => <option key={h} value={h}>
                {String(h).padStart(2, "0")}
              </option>)}
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
            {minuteOptions.map((m) => <option key={m} value={m}>
                {String(m).padStart(2, "0")}
              </option>)}
          </select>
        </label>
        {noDate && <p className="m-0 pb-2 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
            Select a date to set the time.
          </p>}
      </div>
    </div>;
}

export { daysInMonth, isLeapYear, compareDays, isSameDay, addDays, addMonths, startOfMonth, endOfMonth, buildMonthWeeks, formatISODate, formatISODateTime, useDatePicker, DatePicker, DatePickerInput, DatePickerTrigger, DatePickerContent, DatePickerHeader, DatePickerCalendar, DatePickerFooter, DatePickerToday, DatePickerClear, DatePickerApply, DatePickerPresets, DatePickerTime };

export default DatePicker;
