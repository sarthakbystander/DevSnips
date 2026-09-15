import type { KeyboardEvent, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface SearchableOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SearchableSelectProps {
  label?: string;
  options: SearchableOption[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: SearchableOption) => void;
  size?: SelectSize;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  id?: string;
  name?: string;
  className?: string;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const SIZES: Record<SelectSize, string> = {
  sm: "h-8 text-[13px] [&_svg]:size-[14px]",
  md: "h-9 text-sm [&_svg]:size-4",
  lg: "h-11 text-sm [&_svg]:size-[18px]",
};

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 6 9 17l-5-5" />
    </svg>
  );
}

function SearchIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="11" cy="11" r="7" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}

/**
 * Custom searchable combobox. Trigger opens a panel with a search INPUT at the
 * top and a filtered list of options below. Typing filters options by label
 * (case-insensitive substring). Keyboard: ArrowDown/Up moves the active option
 * among FILTERED options, Enter selects, Escape closes + clears search,
 * Home/End jump to first/last. Empty-results state ("No matches"). Selected
 * option is shown in the trigger with a check. Outside-click closes.
 *
 * ARIA: trigger `aria-haspopup="listbox" aria-expanded aria-controls`; the
 * search input is `role="combobox"` with `aria-controls` (listbox) +
 * `aria-activedescendant`; listbox `role="listbox"`, options `role="option"
 * aria-selected`. Controlled (value/onChange) + uncontrolled (defaultValue).
 */
export function SearchableSelect({
  label = "Search",
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Search…",
  searchPlaceholder = "Search options",
  disabled,
  id,
  name,
  className,
}: SearchableSelectProps) {
  const generatedId = useId();
  const triggerId = id ?? `searchable-select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;
  const comboboxId = `${triggerId}-combobox`;

  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;

  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);

  const normalized = query.trim().toLowerCase();
  const filtered = normalized === ""
    ? options
    : options.filter((o) => o.label.toLowerCase().includes(normalized));

  useEffect(() => {
    if (!open) return;
    const enabled = filtered.findIndex((o) => !o.disabled);
    setActiveIndex(enabled === -1 ? 0 : enabled);
  }, [open, query, filtered]);

  function openPanel() {
    setOpen(true);
    setQuery("");
  }

  function closePanel() {
    setOpen(false);
    setQuery("");
    triggerRef.current?.focus();
  }

  function choose(option: SearchableOption) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
    closePanel();
  }

  function moveActive(step: number) {
    setActiveIndex((cur) => {
      const n = filtered.length;
      if (n === 0) return cur;
      let next = cur;
      for (let i = 0; i < n; i++) {
        next = (next + step + n) % n;
        if (!filtered[next].disabled) return next;
      }
      return cur;
    });
  }

  function jumpTo(edge: "first" | "last") {
    const n = filtered.length;
    if (n === 0) return;
    const range = edge === "first" ? filtered : [...filtered].reverse();
    const hit = range.findIndex((o) => !o.disabled);
    if (hit === -1) return;
    const idx = edge === "first" ? hit : n - 1 - hit;
    setActiveIndex(Math.max(0, Math.min(n - 1, idx)));
  }

  function onInputKeyDown(event: KeyboardEvent<HTMLInputElement>) {
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
        if (filtered[activeIndex]) choose(filtered[activeIndex]);
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

  const activeId = filtered[activeIndex] ? `${triggerId}-opt-${activeIndex}` : undefined;

  return (
    <div className="w-full">
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
          onClick={() => (open ? closePanel() : openPanel())}
          className={cx(
            "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 motion-reduce:transition-none",
            "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]",
            SIZES[size],
            className,
          )}
        >
          <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
            {selected ? selected.label : placeholder}
          </span>
          {selected ? (
            <CheckIcon className="shrink-0 text-[var(--ds-color-primary)]" />
          ) : null}
          <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? (
          <SearchPanel
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
            activeIndex={activeIndex}
            selectedValue={selectedValue}
            triggerId={triggerId}
            activeId={activeId}
            onChoose={choose}
            onHover={setActiveIndex}
            onOutside={closePanel}
          />
        ) : null}
      </div>
    </div>
  );
}

export default SearchableSelect;

function SearchPanel({
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
  activeIndex,
  selectedValue,
  triggerId,
  activeId,
  onChoose,
  onHover,
  onOutside,
}: {
  ref: RefObject<HTMLDivElement>;
  listboxId: string;
  comboboxId: string;
  labelledby: string;
  inputRef: RefObject<HTMLInputElement>;
  searchPlaceholder: string;
  query: string;
  onQuery: (q: string) => void;
  onInputKeyDown: (e: KeyboardEvent<HTMLInputElement>) => void;
  filtered: SearchableOption[];
  activeIndex: number;
  selectedValue: string;
  triggerId: string;
  activeId: string | undefined;
  onChoose: (o: SearchableOption) => void;
  onHover: (i: number) => void;
  onOutside: () => void;
}) {
  useEffect(() => {
    function onDown(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) onOutside();
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

  return (
    <div
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
        {filtered.length === 0 ? (
          <div className="px-2.5 py-2 text-[13px] text-[var(--ds-color-muted-foreground)]">No matches</div>
        ) : (
          filtered.map((option, i) => {
            const isSelected = option.value === selectedValue;
            return (
              <button
                key={option.value}
                id={`${triggerId}-opt-${i}`}
                type="button"
                data-i={i}
                role="option"
                aria-selected={isSelected}
                aria-disabled={option.disabled || undefined}
                disabled={option.disabled}
                onMouseEnter={() => onHover(i)}
                onClick={() => onChoose(option)}
                className={cx(
                  "flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
                  i === activeIndex ? "bg-[var(--ds-color-surface-hover)]" : "",
                  isSelected ? "font-medium" : "",
                  option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : "",
                )}
              >
                <span className="truncate">{option.label}</span>
                {isSelected ? (
                  <CheckIcon className="shrink-0 text-[var(--ds-color-primary)]" />
                ) : null}
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}
