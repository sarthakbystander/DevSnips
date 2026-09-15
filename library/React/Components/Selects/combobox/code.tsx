import type { KeyboardEvent, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface ComboboxOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface ComboboxProps {
  label?: string;
  options: ComboboxOption[];
  /** The selected option's value. */
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: ComboboxOption) => void;
  /** Fires whenever the text input value changes (the typed query). */
  onInputChange?: (query: string) => void;
  size?: SelectSize;
  placeholder?: string;
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

/**
 * A true WAI-ARIA combobox: a single text INPUT is both the trigger and the
 * editable value. You can type a value OR pick from the listbox below — the
 * input has `role="combobox" aria-expanded aria-controls aria-activedescendant
 * aria-autocomplete="list"`. Typing filters options by label (case-insensitive
 * substring). ArrowDown opens the listbox and moves the active option down,
 * ArrowUp moves up, Enter selects (sets the input value to the option label
 * and the selected value to the option value), Escape closes, Home/End jump.
 * Distinct from searchable-select: here the INPUT IS the trigger (no button).
 *
 * Selected value follows `value`/`defaultValue`/`onChange` (controlled +
 * uncontrolled). The input text mirrors the selected option's label when not
 * being edited, and reflects the typed query while the listbox is open.
 */
export function Combobox({
  label = "Combobox",
  options,
  value,
  defaultValue = "",
  onChange,
  onInputChange,
  size = "md",
  placeholder = "Search or select…",
  disabled,
  id,
  name,
  className,
}: ComboboxProps) {
  const generatedId = useId();
  const inputId = id ?? `combobox-${generatedId}`;
  const listboxId = `${inputId}-listbox`;

  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;

  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);

  const normalized = query.trim().toLowerCase();
  const filtered = normalized === ""
    ? options
    : options.filter((o) => o.label.toLowerCase().includes(normalized));

  // When closed (and not focused), show the selected option's label.
  const displayText = open ? query : (selected ? selected.label : query);

  useEffect(() => {
    if (!open) return;
    const start = selected
      ? filtered.findIndex((o) => o.value === selected.value)
      : filtered.findIndex((o) => !o.disabled);
    setActiveIndex(start === -1 ? (filtered.findIndex((o) => !o.disabled) === -1 ? 0 : filtered.findIndex((o) => !o.disabled)) : start);
  }, [open, query]);

  function openListbox() {
    setOpen(true);
  }

  function closeListbox() {
    setOpen(false);
    // Restore the input text to the selected label (clear stray query).
    setQuery(selected ? selected.label : "");
  }

  function choose(option: ComboboxOption) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
    setQuery(option.label);
    setOpen(false);
    inputRef.current?.focus();
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
        if (!open) openListbox();
        else moveActive(1);
        break;
      case "ArrowUp":
        event.preventDefault();
        if (!open) openListbox();
        else moveActive(-1);
        break;
      case "Home":
        if (open) {
          event.preventDefault();
          jumpTo("first");
        }
        break;
      case "End":
        if (open) {
          event.preventDefault();
          jumpTo("last");
        }
        break;
      case "Enter":
        if (open && filtered[activeIndex]) {
          event.preventDefault();
          choose(filtered[activeIndex]);
        }
        break;
      case "Escape":
        if (open) {
          event.preventDefault();
          closeListbox();
        }
        break;
      case "Tab":
        if (open) closeListbox();
        break;
    }
  }

  function handleInputChange(e: { target: { value: string } }) {
    const v = e.target.value;
    setQuery(v);
    if (!open) openListbox();
    onInputChange?.(v);
  }

  const activeId = open && filtered[activeIndex] ? `${inputId}-opt-${activeIndex}` : undefined;
  const selectedIndex = selected ? filtered.findIndex((o) => o.value === selected.value) : -1;

  return (
    <div className="w-full">
      <label htmlFor={inputId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValue} disabled={disabled} readOnly /> : null}
        <input
          ref={inputRef}
          id={inputId}
          type="text"
          role="combobox"
          aria-expanded={open}
          aria-haspopup="listbox"
          aria-controls={open ? listboxId : undefined}
          aria-activedescendant={activeId}
          aria-autocomplete="list"
          aria-label={label}
          autoComplete="off"
          spellCheck={false}
          value={displayText}
          disabled={disabled}
          placeholder={selected ? selected.label : placeholder}
          onChange={handleInputChange}
          onFocus={() => { if (!open && filtered.length > 0) openListbox(); }}
          onKeyDown={onInputKeyDown}
          className={cx(
            "inline-flex w-full items-center rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 motion-reduce:transition-none placeholder:text-[var(--ds-color-muted-foreground)]",
            "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)] pr-9",
            SIZES[size],
            className,
          )}
        />
        <button
          type="button"
          tabIndex={-1}
          aria-hidden="true"
          disabled={disabled}
          onClick={() => (open ? closeListbox() : (inputRef.current?.focus(), openListbox()))}
          className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center justify-center text-[var(--ds-color-muted-foreground)] focus-visible:outline-none"
        >
          <ChevronDown className={cx("transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? (
          <ComboboxPanel
            ref={listboxRef}
            id={listboxId}
            labelledby={inputId}
            filtered={filtered}
            activeIndex={activeIndex}
            selectedIndex={selectedIndex}
            triggerId={inputId}
            onChoose={choose}
            onHover={setActiveIndex}
            onOutside={closeListbox}
          />
        ) : null}
      </div>
    </div>
  );
}

export default Combobox;

function ComboboxPanel({
  ref,
  id,
  labelledby,
  filtered,
  activeIndex,
  selectedIndex,
  triggerId,
  onChoose,
  onHover,
  onOutside,
}: {
  ref: RefObject<HTMLDivElement>;
  id: string;
  labelledby: string;
  filtered: ComboboxOption[];
  activeIndex: number;
  selectedIndex: number;
  triggerId: string;
  onChoose: (o: ComboboxOption) => void;
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
    const el = ref.current?.querySelector(`[data-i="${activeIndex}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex, ref]);

  return (
    <div
      ref={ref}
      id={id}
      role="listbox"
      aria-labelledby={labelledby}
      className="absolute z-20 mt-1.5 max-h-60 w-full overflow-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]"
    >
      {filtered.length === 0 ? (
        <div className="px-2.5 py-2 text-[13px] text-[var(--ds-color-muted-foreground)]">No matches</div>
      ) : (
        filtered.map((option, i) => {
          const isSelected = i === selectedIndex;
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
                <svg className="shrink-0 text-[var(--ds-color-primary)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M20 6 9 17l-5-5" />
                </svg>
              ) : null}
            </button>
          );
        })
      )}
    </div>
  );
}
