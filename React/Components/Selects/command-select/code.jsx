/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useEffect, useId, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  sm: "h-8 text-[13px] [&_svg]:size-[14px]",
  md: "h-9 text-sm [&_svg]:size-4",
  lg: "h-11 text-sm [&_svg]:size-[18px]"
};
function ChevronDown({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m6 9 6 6 6-6" />
    </svg>;
}
function CheckIcon({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 6 9 17l-5-5" />
    </svg>;
}
function SearchIcon({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="11" cy="11" r="7" />
      <path d="m21 21-4.3-4.3" />
    </svg>;
}
export function CommandSelect({
  label = "Select",
  groups,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Select a command",
  searchPlaceholder = "Search commands",
  disabled,
  id,
  name,
  className
}) {
  const generatedId = useId();
  const triggerId = id ?? `command-select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;
  const comboboxId = `${triggerId}-combobox`;
  const allOptions = groups.flatMap((g) => g.options);
  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = allOptions.find((o) => o.value === selectedValue) ?? null;
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const triggerRef = useRef(null);
  const inputRef = useRef(null);
  const listboxRef = useRef(null);
  const normalized = query.trim().toLowerCase();
  const rows = [];
  let optionGlobalIndex = 0;
  for (const group of groups) {
    const matched = normalized === "" ? group.options : group.options.filter((o) => o.label.toLowerCase().includes(normalized));
    if (matched.length === 0) continue;
    rows.push({ type: "group", groupLabel: group.label, optionIndex: -1, optionGlobalIndex: -1 });
    for (let i = 0; i < matched.length; i++) {
      rows.push({
        type: "option",
        groupLabel: group.label,
        option: matched[i],
        optionIndex: i,
        optionGlobalIndex: allOptions.indexOf(matched[i])
      });
    }
    optionGlobalIndex += matched.length;
  }
  const optionRows = rows.filter((r) => r.type === "option");
  useEffect(() => {
    if (!open) return;
    const start = selected ? optionRows.findIndex((r) => r.option && r.option.value === selected.value) : optionRows.findIndex((r) => r.option && !r.option.disabled);
    const fallback = optionRows.findIndex((r) => r.option && !r.option.disabled);
    setActiveIndex(start === -1 ? fallback === -1 ? 0 : fallback : start);
  }, [open, query]);
  function openPanel() {
    setOpen(true);
    setQuery("");
  }
  function closePanel() {
    setOpen(false);
    setQuery("");
    triggerRef.current?.focus();
  }
  function choose(option) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
    closePanel();
  }
  function moveActive(step) {
    setActiveIndex((cur) => {
      const n = optionRows.length;
      if (n === 0) return cur;
      let next = cur;
      for (let i = 0; i < n; i++) {
        next = (next + step + n) % n;
        const o = optionRows[next].option;
        if (o && !o.disabled) return next;
      }
      return cur;
    });
  }
  function jumpTo(edge) {
    const n = optionRows.length;
    if (n === 0) return;
    const range = edge === "first" ? optionRows : [...optionRows].reverse();
    const hit = range.findIndex((r) => r.option && !r.option.disabled);
    if (hit === -1) return;
    const idx = edge === "first" ? hit : n - 1 - hit;
    setActiveIndex(Math.max(0, Math.min(n - 1, idx)));
  }
  function onInputKeyDown(event) {
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        moveActive(1);
        break;
      case "ArrowUp":
        event.preventDefault();
        moveActive(-1);
        break;
      case "Home":
        event.preventDefault();
        jumpTo("first");
        break;
      case "End":
        event.preventDefault();
        jumpTo("last");
        break;
      case "Enter":
        event.preventDefault();
        {
          const o = optionRows[activeIndex]?.option;
          if (o) choose(o);
        }
        break;
      case "Escape":
        event.preventDefault();
        if (query !== "") setQuery("");
        else closePanel();
        break;
      case "Tab":
        if (open) closePanel();
        break;
    }
  }
  const activeRow = optionRows[activeIndex];
  const activeId = activeRow && activeRow.option ? `${triggerId}-opt-${activeRow.optionGlobalIndex}` : undefined;
  return <div className="w-full">
      <label htmlFor={triggerId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValue} disabled={disabled} readOnly /> : null}
        <button
    ref={triggerRef}
    id={triggerId}
    type="button"
    disabled={disabled}
    aria-haspopup="listbox"
    aria-expanded={open}
    aria-controls={open ? listboxId : undefined}
    onClick={() => open ? closePanel() : openPanel()}
    className={cx(
      "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 motion-reduce:transition-none",
      "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]",
      SIZES[size],
      className
    )}
  >
          <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
            {selected ? selected.label : placeholder}
          </span>
          {selected ? <CheckIcon className="shrink-0 text-[var(--ds-color-primary)]" /> : null}
          <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? <CommandPanel
    ref={listboxRef}
    listboxId={listboxId}
    comboboxId={comboboxId}
    labelledby={triggerId}
    inputRef={inputRef}
    searchPlaceholder={searchPlaceholder}
    query={query}
    onQuery={setQuery}
    onInputKeyDown={onInputKeyDown}
    rows={rows}
    optionRows={optionRows}
    activeIndex={activeIndex}
    selectedValue={selectedValue}
    triggerId={triggerId}
    activeId={activeId}
    onChoose={choose}
    onHover={setActiveIndex}
    onOutside={closePanel}
  /> : null}
      </div>
    </div>;
}
function CommandPanel({
  ref,
  listboxId,
  comboboxId,
  labelledby,
  inputRef,
  searchPlaceholder,
  query,
  onQuery,
  onInputKeyDown,
  rows,
  optionRows,
  activeIndex,
  selectedValue,
  triggerId,
  activeId,
  onChoose,
  onHover,
  onOutside
}) {
  useEffect(() => {
    function onDown(e) {
      if (ref.current && !ref.current.contains(e.target)) onOutside();
    }
    document.addEventListener("mousedown", onDown);
    return () => document.removeEventListener("mousedown", onDown);
  }, [onOutside, ref]);
  useEffect(() => {
    inputRef.current?.focus();
  }, [inputRef]);
  useEffect(() => {
    const el = ref.current?.querySelector(`[data-i="${activeIndex}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex, ref]);
  const empty = optionRows.length === 0;
  return <div
    ref={ref}
    className="absolute z-20 mt-1.5 w-full overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] shadow-[var(--ds-shadow-md)]"
  >
      <div className="flex items-center gap-2 border-b border-[var(--ds-color-border-subtle)] px-2.5 py-2">
        <SearchIcon className="shrink-0 text-[var(--ds-color-muted-foreground)]" />
        <input
    ref={inputRef}
    id={comboboxId}
    type="text"
    role="combobox"
    aria-expanded={true}
    aria-haspopup="listbox"
    aria-controls={listboxId}
    aria-activedescendant={activeId}
    aria-autocomplete="list"
    value={query}
    onChange={(e) => onQuery(e.target.value)}
    onKeyDown={onInputKeyDown}
    placeholder={searchPlaceholder}
    className="w-full bg-transparent text-sm text-[var(--ds-color-foreground)] placeholder:text-[var(--ds-color-muted-foreground)] focus-visible:outline-none"
  />
      </div>
      <div
    id={listboxId}
    role="listbox"
    aria-labelledby={labelledby}
    className="max-h-60 overflow-auto p-1"
  >
        {empty ? <div className="px-2.5 py-2 text-[13px] text-[var(--ds-color-muted-foreground)]">No matches</div> : rows.map((row, i) => {
    if (row.type === "group") {
      return <div
        key={`g-${row.groupLabel}`}
        className="px-2.5 pb-1 pt-2 text-[11px] font-medium uppercase tracking-wide text-[var(--ds-color-muted-foreground)]"
      >
                  {row.groupLabel}
                </div>;
    }
    const option = row.option;
    const optionRowIndex = optionRows.indexOf(row);
    const isSelected = option.value === selectedValue;
    const isActive = optionRowIndex === activeIndex;
    return <button
      key={`o-${option.value}`}
      id={`${triggerId}-opt-${row.optionGlobalIndex}`}
      type="button"
      data-i={optionRowIndex}
      role="option"
      aria-selected={isSelected}
      aria-disabled={option.disabled || undefined}
      disabled={option.disabled}
      onMouseEnter={() => onHover(optionRowIndex)}
      onClick={() => onChoose(option)}
      className={cx(
        "flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
        isActive ? "bg-[var(--ds-color-surface-hover)]" : "",
        isSelected ? "font-medium" : "",
        option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : ""
      )}
    >
                <span className="truncate">{option.label}</span>
                {isSelected ? <CheckIcon className="shrink-0 text-[var(--ds-color-primary)]" /> : null}
              </button>;
  })}
      </div>
    </div>;
}

export default CommandSelect;
