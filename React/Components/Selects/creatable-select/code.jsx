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
function PlusIcon({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 5v14M5 12h14" />
    </svg>;
}
export function CreatableSelect({
  label = "Select",
  options,
  value,
  defaultValue = "",
  onChange,
  onCreateOption,
  size = "md",
  placeholder = "Select an option",
  searchPlaceholder = "Search options",
  createLabel = "Create",
  disabled,
  id,
  name,
  className
}) {
  const generatedId = useId();
  const triggerId = id ?? `creatable-select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;
  const comboboxId = `${triggerId}-combobox`;
  const [created, setCreated] = useState([]);
  const allOptions = [...created, ...options];
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
  const trimmed = query.trim();
  const filtered = normalized === "" ? allOptions : allOptions.filter((o) => o.label.toLowerCase().includes(normalized));
  const exactMatch = normalized !== "" && allOptions.some((o) => o.label.toLowerCase() === normalized || o.value.toLowerCase() === normalized);
  const canCreate = trimmed !== "" && !exactMatch;
  const rowCount = filtered.length + (canCreate ? 1 : 0);
  useEffect(() => {
    if (!open) return;
    setActiveIndex(canCreate ? 0 : 0);
  }, [open, query, canCreate]);
  function openPanel() {
    setOpen(true);
    setQuery("");
  }
  function closePanel() {
    setOpen(false);
    setQuery("");
    triggerRef.current?.focus();
  }
  function chooseOption(option) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
    closePanel();
  }
  function createOption() {
    const text = trimmed;
    if (text === "") return;
    const newOption = { value: text, label: text };
    setCreated((prev) => [...prev, newOption]);
    if (value === undefined) setInternalValue(newOption.value);
    onCreateOption?.(text);
    onChange?.(newOption.value, newOption);
    closePanel();
  }
  function chooseRow(index) {
    if (canCreate && index === 0) {
      createOption();
      return;
    }
    const optIndex = canCreate ? index - 1 : index;
    const option = filtered[optIndex];
    if (option) chooseOption(option);
  }
  function moveActive(step) {
    setActiveIndex((cur) => {
      if (rowCount === 0) return cur;
      let next = cur;
      for (let i = 0; i < rowCount; i++) {
        next = (next + step + rowCount) % rowCount;
        if (canCreate && next === 0) return next;
        const optIndex = canCreate ? next - 1 : next;
        const option = filtered[optIndex];
        if (option && !option.disabled) return next;
      }
      return cur;
    });
  }
  function jumpTo(edge) {
    if (rowCount === 0) return;
    if (edge === "first") {
      if (canCreate) {
        setActiveIndex(0);
        return;
      }
      const hit = filtered.findIndex((o) => !o.disabled);
      if (hit !== -1) setActiveIndex(hit);
      return;
    }
    for (let i = filtered.length - 1; i >= 0; i--) {
      if (!filtered[i].disabled) {
        setActiveIndex(canCreate ? i + 1 : i);
        return;
      }
    }
    if (canCreate) setActiveIndex(0);
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
        chooseRow(activeIndex);
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
  let activeId;
  if (canCreate && activeIndex === 0) {
    activeId = `${triggerId}-create`;
  } else {
    const optIndex = canCreate ? activeIndex - 1 : activeIndex;
    if (filtered[optIndex]) activeId = `${triggerId}-opt-${optIndex}`;
  }
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
        {open ? <CreatablePanel
    ref={listboxRef}
    listboxId={listboxId}
    comboboxId={comboboxId}
    labelledby={triggerId}
    inputRef={inputRef}
    searchPlaceholder={searchPlaceholder}
    query={query}
    onQuery={setQuery}
    onInputKeyDown={onInputKeyDown}
    filtered={filtered}
    selectedValue={selectedValue}
    triggerId={triggerId}
    activeId={activeId}
    activeIndex={activeIndex}
    canCreate={canCreate}
    createLabel={createLabel}
    createText={trimmed}
    onChooseRow={chooseRow}
    onHover={setActiveIndex}
    onOutside={closePanel}
  /> : null}
      </div>
    </div>;
}
function CreatablePanel({
  ref,
  listboxId,
  comboboxId,
  labelledby,
  inputRef,
  searchPlaceholder,
  query,
  onQuery,
  onInputKeyDown,
  filtered,
  selectedValue,
  triggerId,
  activeId,
  activeIndex,
  canCreate,
  createLabel,
  createText,
  onChooseRow,
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
  const empty = filtered.length === 0 && !canCreate;
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
        {empty ? <div className="px-2.5 py-2 text-[13px] text-[var(--ds-color-muted-foreground)]">No matches</div> : <>
            {canCreate ? <button
    key="__create__"
    id={`${triggerId}-create`}
    type="button"
    data-i={0}
    role="option"
    aria-selected={false}
    onMouseEnter={() => onHover(0)}
    onClick={() => onChooseRow(0)}
    className={cx(
      "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
      activeIndex === 0 ? "bg-[var(--ds-color-surface-hover)]" : ""
    )}
  >
                <PlusIcon className="shrink-0 text-[var(--ds-color-primary)]" />
                <span className="truncate">
                  {createLabel} <span className="font-medium">&ldquo;{createText}&rdquo;</span>
                </span>
              </button> : null}
            {filtered.map((option, i) => {
    const row = canCreate ? i + 1 : i;
    const isSelected = option.value === selectedValue;
    return <button
      key={option.value}
      id={`${triggerId}-opt-${i}`}
      type="button"
      data-i={row}
      role="option"
      aria-selected={isSelected}
      aria-disabled={option.disabled || undefined}
      disabled={option.disabled}
      onMouseEnter={() => onHover(row)}
      onClick={() => onChooseRow(row)}
      className={cx(
        "flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
        row === activeIndex ? "bg-[var(--ds-color-surface-hover)]" : "",
        isSelected ? "font-medium" : "",
        option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : ""
      )}
    >
                  <span className="truncate">{option.label}</span>
                  {isSelected ? <CheckIcon className="shrink-0 text-[var(--ds-color-primary)]" /> : null}
                </button>;
  })}
          </>}
      </div>
    </div>;
}

export default CreatableSelect;
