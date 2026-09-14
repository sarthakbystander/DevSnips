/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState
} from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const WEEK_MS = 6048e5;
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
function isoWeekNumber(date) {
  const noon = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 12);
  const thursday = addDays(noon, 3 - (noon.getDay() + 6) % 7);
  const jan4 = new Date(thursday.getFullYear(), 0, 4, 12);
  const weekOneThursday = addDays(jan4, 3 - (jan4.getDay() + 6) % 7);
  return 1 + Math.round((thursday.getTime() - weekOneThursday.getTime()) / WEEK_MS);
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
const CalendarContext = createContext(null);
function useCalendar() {
  const ctx = useContext(CalendarContext);
  if (!ctx) throw new Error("Calendar components must be composed inside <Calendar>.");
  return ctx;
}
const ROOT_CLASSES = "w-max max-w-full rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-3 shadow-[var(--ds-shadow-xs)]";
const HEADER_CLASSES = "mb-1 flex items-center justify-between gap-1";
const NAV_BUTTON_CLASSES = "inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const HEADING_CLASSES = "m-0 text-sm font-semibold leading-9 text-[var(--ds-color-foreground)]";
const HEADING_BUTTON_CLASSES = "-mx-1.5 rounded-[var(--ds-radius-sm)] px-1.5 transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const WEEKDAY_CLASSES = "flex size-9 items-center justify-center text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const WEEKNUM_CLASSES = "flex size-9 items-center justify-center font-mono text-[11px] tabular-nums text-[var(--ds-color-muted-foreground)]";
const DAY_CLASSES = "inline-flex size-9 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent text-sm leading-5 tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none";
const PICKER_BUTTON_CLASSES = "flex h-9 flex-1 items-center justify-center rounded-[var(--ds-radius-sm)] border border-transparent px-2 text-sm leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none";
const FOOTER_CLASSES = "mt-2 flex items-center justify-between gap-2 border-t border-[var(--ds-color-border-subtle)] pt-2 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const SELECTED_DAY_CLASSES = "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)]";
const RANGE_MIDDLE_CLASSES = "rounded-none bg-[var(--ds-color-surface-active)] text-[var(--ds-color-foreground)]";
const PICKER_SELECTED_CLASSES = "bg-[var(--ds-color-primary)] font-medium text-[var(--ds-color-primary-foreground)]";
function ChevronLeftIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false"><path d="m15 18-6-6 6-6" /></svg>;
}
function ChevronRightIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false"><path d="m9 18 6-6-6-6" /></svg>;
}
function Calendar(props) {
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
  const mode = _mode ?? "single";
  const singleSlice = props;
  const multipleSlice = props;
  const rangeSlice = props;
  const [singleSelection, setSingleSelection] = useControllableState(
    mode === "single" ? singleSlice.selected : undefined,
    (mode === "single" ? singleSlice.defaultSelected : null) ?? null,
    mode === "single" ? singleSlice.onSelect : undefined
  );
  const [multipleSelection, setMultipleSelection] = useControllableState(
    mode === "multiple" ? multipleSlice.selected : undefined,
    (mode === "multiple" ? multipleSlice.defaultSelected : undefined) ?? [],
    mode === "multiple" ? multipleSlice.onSelect : undefined
  );
  const [rangeSelection, setRangeSelection] = useControllableState(
    mode === "range" ? rangeSlice.selected : undefined,
    (mode === "range" ? rangeSlice.defaultSelected : undefined) ?? null,
    mode === "range" ? rangeSlice.onSelect : undefined
  );
  const [today] = useState(() => /* @__PURE__ */ new Date());
  const firstSelected = mode === "single" ? singleSelection : mode === "multiple" ? multipleSelection[0] ?? null : rangeSelection?.from ?? null;
  const [monthState, setMonthState] = useControllableState(
    controlledMonth !== undefined ? startOfMonth(controlledMonth) : undefined,
    startOfMonth(defaultMonth ?? firstSelected ?? today),
    onMonthChange
  );
  const monthKey = monthState.getFullYear() * 12 + monthState.getMonth();
  const month = useMemo(() => startOfMonth(monthState), [monthKey]);
  const [view, setView] = useState(defaultView);
  const [focusKey, setFocusKey] = useState(null);
  const focusIntentRef = useRef(false);
  const rootRef = useRef(null);
  const isDisabled = useCallback(
    (date) => {
      if (minDate && compareDays(date, minDate) < 0) return true;
      if (maxDate && compareDays(date, maxDate) > 0) return true;
      return disabled ? disabled(date) : false;
    },
    [minDate, maxDate, disabled]
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
  const [renderedStart, renderedEnd] = useMemo(() => {
    if (!showOutsideDays) return [month, endOfMonth(lastVisibleMonth)];
    const firstWeeks = buildMonthWeeks(month, weekStartsOn);
    const lastWeeks = buildMonthWeeks(lastVisibleMonth, weekStartsOn);
    const start = firstWeeks[0]?.[0] ?? month;
    const end = lastWeeks[lastWeeks.length - 1]?.[6] ?? endOfMonth(lastVisibleMonth);
    return [start, end];
  }, [month, lastVisibleMonth, weekStartsOn, showOutsideDays]);
  const isRenderedDate = useCallback(
    (date) => compareDays(date, renderedStart) >= 0 && compareDays(date, renderedEnd) <= 0,
    [renderedStart, renderedEnd]
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
    [minDate, maxDate, numberOfMonths, setMonthState]
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
  const selectDate = useCallback(
    (date) => {
      if (isDisabled(date)) return;
      if (mode === "single") {
        if (singleSelection && isSameDay(singleSelection, date)) return;
        setSingleSelection(date);
        return;
      }
      if (mode === "multiple") {
        const exists = multipleSelection.some((d) => isSameDay(d, date));
        setMultipleSelection(
          exists ? multipleSelection.filter((d) => !isSameDay(d, date)) : [...multipleSelection, date]
        );
        return;
      }
      if (!rangeSelection || rangeSelection.to) {
        setRangeSelection({ from: date, to: null });
        return;
      }
      const from = rangeSelection.from;
      if (isSameDay(date, from)) {
        setRangeSelection({ from, to: from });
      } else if (compareDays(date, from) < 0 || rangeCrossesDisabled(from, date)) {
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
      rangeCrossesDisabled
    ]
  );
  const clearSelection = useCallback(() => {
    if (mode === "single") setSingleSelection(null);
    else if (mode === "multiple") setMultipleSelection([]);
    else setRangeSelection(null);
  }, [mode, setSingleSelection, setMultipleSelection, setRangeSelection]);
  const isRangeStart = useCallback(
    (date) => mode === "range" && rangeSelection !== null && rangeSelection.to !== null && !isSameDay(rangeSelection.from, rangeSelection.to) && isSameDay(rangeSelection.from, date),
    [mode, rangeSelection]
  );
  const isRangeEnd = useCallback(
    (date) => mode === "range" && rangeSelection !== null && rangeSelection.to !== null && !isSameDay(rangeSelection.from, rangeSelection.to) && isSameDay(rangeSelection.to, date),
    [mode, rangeSelection]
  );
  const isRangeMiddle = useCallback(
    (date) => mode === "range" && rangeSelection !== null && rangeSelection.to !== null && compareDays(date, rangeSelection.from) > 0 && compareDays(date, rangeSelection.to) < 0,
    [mode, rangeSelection]
  );
  const isSelected = useCallback(
    (date) => {
      if (mode === "single") return singleSelection !== null && isSameDay(singleSelection, date);
      if (mode === "multiple") return multipleSelection.some((d) => isSameDay(d, date));
      return rangeSelection !== null && (isSameDay(rangeSelection.from, date) || rangeSelection.to !== null && compareDays(date, rangeSelection.from) > 0 && compareDays(date, rangeSelection.to) <= 0);
    },
    [mode, singleSelection, multipleSelection, rangeSelection]
  );
  const focusedDay = useMemo(() => {
    if (focusKey && /^\d{8}$/.test(focusKey)) return dateFromKey(Number(focusKey));
    return null;
  }, [focusKey]);
  const tabbableDayKey = useMemo(() => {
    const candidates = [focusedDay, firstSelected, today];
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
    focusIntentRef.current = true;
    setFocusKey(key);
  }, []);
  useEffect(() => {
    if (focusKey == null) return;
    const root = rootRef.current;
    if (!root) return;
    const intentional = focusIntentRef.current;
    focusIntentRef.current = false;
    if (!intentional && !root.contains(document.activeElement)) return;
    const el = root.querySelector(`[data-cal-focus="${focusKey}"]`);
    if (el && el !== document.activeElement) el.focus();
  }, [focusKey, monthKey, view]);
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
  const handleDayClick = useCallback(
    (date, outside) => {
      if (outside) {
        goToMonth(monthToReveal(date));
        requestFocus(String(dayKey(date)));
      }
      selectDate(date);
    },
    [goToMonth, monthToReveal, requestFocus, selectDate]
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
      const anchor = focusedDay ?? firstSelected ?? today;
      const day = Math.min(anchor.getDate(), daysInMonth(year, monthIndex));
      let target = new Date(year, monthIndex, day);
      if (isDisabled(target)) {
        target = stepToEnabled(target, (d) => addDays(d, 1)) ?? stepToEnabled(target, (d) => addDays(d, -1)) ?? new Date(year, monthIndex, 1);
      }
      goToMonth(new Date(year, monthIndex, 1));
      setView("days");
      requestFocus(String(dayKey(target)));
    },
    [month, focusedDay, firstSelected, today, isDisabled, stepToEnabled, goToMonth, requestFocus]
  );
  const selectYear = useCallback(
    (year) => {
      goToMonth(new Date(year, month.getMonth(), 1));
      setView("months");
      requestFocus(`m${month.getMonth()}`);
    },
    [month, goToMonth, requestFocus]
  );
  const contextValue = {
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
    setFocusKey
  };
  return <CalendarContext.Provider value={contextValue}><div ref={rootRef} className={cx(ROOT_CLASSES, className)} {...rest}>{children}</div></CalendarContext.Provider>;
}
function CalendarHeader({ className, children, ...rest }) {
  return <div className={cx(HEADER_CLASSES, className)} {...rest}>{children}</div>;
}
function CalendarPrevious({ className, ...rest }) {
  const ctx = useCalendar();
  return <button
    type="button"
    aria-label={ctx.previousLabel}
    disabled={!ctx.canGoPrevious}
    onClick={ctx.goToPrevious}
    className={cx(NAV_BUTTON_CLASSES, className)}
    {...rest}
  ><ChevronLeftIcon /></button>;
}
function CalendarNext({ className, ...rest }) {
  const ctx = useCalendar();
  return <button
    type="button"
    aria-label={ctx.nextLabel}
    disabled={!ctx.canGoNext}
    onClick={ctx.goToNext}
    className={cx(NAV_BUTTON_CLASSES, className)}
    {...rest}
  ><ChevronRightIcon /></button>;
}
function CalendarHeading({ className, ...rest }) {
  const ctx = useCalendar();
  if (ctx.view === "years") {
    return <h2 aria-live="polite" aria-atomic="true" className={cx(HEADING_CLASSES, className)} {...rest}>{ctx.headingLabel}</h2>;
  }
  return <h2 aria-live="polite" aria-atomic="true" className={cx(HEADING_CLASSES, className)} {...rest}><button
    type="button"
    onClick={() => ctx.setView(ctx.view === "days" ? "months" : "years")}
    aria-label={ctx.view === "days" ? `${ctx.headingLabel} \u2014 activate to choose a month` : `${ctx.headingLabel} \u2014 activate to choose a year`}
    className={HEADING_BUTTON_CLASSES}
  >{ctx.headingLabel}</button></h2>;
}
function CalendarGrid({ monthOffset = 0, className, ...rest }) {
  const ctx = useCalendar();
  if (ctx.view === "months") return monthOffset === 0 ? <MonthsPanel className={className} /> : null;
  if (ctx.view === "years") return monthOffset === 0 ? <YearsPanel className={className} /> : null;
  const gridMonth = startOfMonth(addMonths(ctx.month, monthOffset));
  const weeks = buildMonthWeeks(gridMonth, ctx.weekStartsOn);
  const weekdays = weekdayNames(ctx.locale, ctx.weekStartsOn);
  const weekNumberOf = (row) => isoWeekNumber(addDays(row[0] ?? gridMonth, (4 - ctx.weekStartsOn + 7) % 7));
  return <div className={className} {...rest}><div role="grid" aria-label={monthYearLabel(gridMonth, ctx.locale)}><div role="row" className="flex">{ctx.showWeekNumbers && <div role="columnheader" aria-label="Week number" className={WEEKNUM_CLASSES}>
              Wk
            </div>}{weekdays.map((day, i) => <div role="columnheader" key={i} aria-label={day.long} className={WEEKDAY_CLASSES}>{day.short}</div>)}</div>{weeks.map((week, rowIndex) => <div role="row" className="flex" key={rowIndex}>{ctx.showWeekNumbers && <div role="rowheader" className={WEEKNUM_CLASSES}>{weekNumberOf(week)}</div>}{week.map((date) => <DayCell key={dayKey(date)} date={date} gridMonth={gridMonth} monthOffset={monthOffset} />)}</div>)}</div></div>;
}
function DayCell({
  date,
  gridMonth,
  monthOffset
}) {
  const ctx = useCalendar();
  const outside = date.getMonth() !== gridMonth.getMonth();
  if (outside) {
    const isLeading = compareDays(date, gridMonth) < 0;
    const renderOutside = ctx.showOutsideDays && (isLeading ? monthOffset === 0 : monthOffset === ctx.numberOfMonths - 1);
    if (!renderOutside) return <div role="gridcell" className="size-9" />;
  }
  const key = String(dayKey(date));
  const isDisabledDay = ctx.isDisabled(date);
  const selected = ctx.isSelected(date);
  const rangeStart = ctx.isRangeStart(date);
  const rangeEnd = ctx.isRangeEnd(date);
  const rangeMiddle = ctx.isRangeMiddle(date);
  const filled = ctx.mode !== "range" && selected || rangeStart || rangeEnd || ctx.mode === "range" && selected && !rangeMiddle;
  const isToday = isSameDay(date, ctx.today);
  return <div role="gridcell" aria-selected={selected} className="size-9"><button
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
      !rangeMiddle && !filled && (outside ? "text-[var(--ds-color-muted-foreground)]" : "text-[var(--ds-color-foreground)]"),
      !rangeMiddle && !filled && "hover:bg-[var(--ds-color-surface-hover)]",
      rangeStart && "rounded-r-none",
      rangeEnd && "rounded-l-none",
      isToday && "border-[var(--ds-color-border-strong)] font-semibold",
      isDisabledDay && "opacity-40"
    )}
  >{date.getDate()}</button></div>;
}
function MonthsPanel({ className }) {
  const ctx = useCalendar();
  const year = ctx.month.getFullYear();
  const names = monthNames(ctx.locale);
  const rows = [];
  for (let r = 0; r < 4; r += 1) rows.push([r * 3, r * 3 + 1, r * 3 + 2]);
  return <div className={className}><div role="grid" aria-label={`Choose a month in ${yearLabel(year, ctx.locale)}`}>{rows.map((row, r) => <div role="row" className="flex gap-1" key={r}>{row.map((m) => {
    const key = `m${m}`;
    const enabled = ctx.monthEnabled(year, m);
    const isCurrent = m === ctx.month.getMonth();
    return <div role="gridcell" aria-selected={isCurrent} className="flex-1" key={m}><button
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
        isCurrent ? PICKER_SELECTED_CLASSES : "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]"
      )}
    >{names[m]}</button></div>;
  })}</div>)}</div></div>;
}
function YearsPanel({ className }) {
  const ctx = useCalendar();
  const rows = [];
  for (let r = 0; r < 4; r += 1) rows.push(ctx.yearPage.slice(r * 3, r * 3 + 3));
  return <div className={className}><div role="grid" aria-label="Choose a year">{rows.map((row, r) => <div role="row" className="flex gap-1" key={r}>{row.map((year) => {
    const key = `y${year}`;
    const enabled = ctx.yearEnabled(year);
    const isCurrent = year === ctx.month.getFullYear();
    return <div role="gridcell" aria-selected={isCurrent} className="flex-1" key={year}><button
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
        isCurrent ? PICKER_SELECTED_CLASSES : "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]"
      )}
    >{yearLabel(year, ctx.locale)}</button></div>;
  })}</div>)}</div></div>;
}
function CalendarFooter({ className, children, ...rest }) {
  return <div className={cx(FOOTER_CLASSES, className)} {...rest}>{children}</div>;
}

export { daysInMonth, isLeapYear, compareDays, isSameDay, addDays, addMonths, startOfMonth, endOfMonth, isoWeekNumber, buildMonthWeeks, useCalendar, Calendar, CalendarHeader, CalendarPrevious, CalendarNext, CalendarHeading, CalendarGrid, CalendarFooter };

export default Calendar;
