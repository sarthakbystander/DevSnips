import type { KeyboardEvent, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface MultiOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface MultiSelectProps {
  label?: string;
  options: MultiOption[];
  value?: string[];
  defaultValue?: string[];
  onChange?: (values: string[], options: MultiOption[]) => void;
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

function CheckIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 6 9 17l-5-5" />
    </svg>
  );
}

/**
 * Custom multi-selection listbox. The trigger shows a restrained summary:
 * 0 selected → placeholder; 1–2 → labels joined by ", "; 3+ → "N selected".
 * The panel is a listbox where each option has role="option" aria-selected +
 * a box glyph reflecting state. Click / Enter / Space toggles selection and
 * the panel STAYS OPEN (multi-select). ArrowUp/Down/Home/End navigate,
 * Escape closes. Selected rows use bg-surface-selected + a check.
 * Outside-click closes. Controlled (value/onChange) + uncontrolled.
 */
export function MultiSelect({
  label = "Select options",
  options,
  value,
  defaultValue = [],
  onChange,
  size = "md",
  placeholder = "Select options",
  disabled,
  id,
  name,
  className,
}: MultiSelectProps) {
  const generatedId = useId();
  const triggerId = id ?? `multi-select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;

  const [internalValue, setInternalValue] = useState<string[]>(defaultValue);
  const selectedValues = value ?? internalValue;

  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(() => {
    const enabled = options.findIndex((o) => !o.disabled);
    return enabled === -1 ? 0 : enabled;
  });
  const triggerRef = useRef<HTMLButtonElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);

  const selectedSet = new Set(selectedValues);
  const selectedOptions = options.filter((o) => selectedSet.has(o.value));

  const summary = selectedValues.length === 0
    ? placeholder
    : selectedValues.length <= 2
      ? selectedOptions.map((o) => o.label).join(", ")
      : `${selectedValues.length} selected`;

  function toggle(option: MultiOption) {
    if (option.disabled) return;
    const next = selectedSet.has(option.value)
      ? selectedValues.filter((v) => v !== option.value)
      : [...selectedValues, option.value];
    if (value === undefined) setInternalValue(next);
    const nextOptions = options.filter((o) => next.includes(o.value));
    onChange?.(next, nextOptions);
  }

  function openListbox(nextActive?: number) {
    setOpen(true);
    const firstSelected = options.findIndex((o) => selectedSet.has(o.value));
    const enabled = options.findIndex((o) => !o.disabled);
    const start = nextActive ?? (firstSelected >= 0 ? firstSelected : enabled);
    setActiveIndex(Math.max(0, Math.min(options.length - 1, start < 0 ? 0 : start)));
  }

  function moveActive(step: number) {
    setActiveIndex((cur) => {
      let next = cur;
      for (let i = 0; i < options.length; i++) {
        next = (next + step + options.length) % options.length;
        if (!options[next].disabled) return next;
      }
      return cur;
    });
  }

  function onKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (disabled) return;
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        if (!open) openListbox();
        else moveActive(1);
        break;
      case "ArrowUp":
        event.preventDefault();
        if (!open) openListbox(options.length - 1);
        else moveActive(-1);
        break;
      case "Home":
        if (open) { event.preventDefault(); for (let i = 0; i < options.length; i++) if (!options[i].disabled) { setActiveIndex(i); break; } }
        break;
      case "End":
        if (open) { event.preventDefault(); for (let i = options.length - 1; i >= 0; i--) if (!options[i].disabled) { setActiveIndex(i); break; } }
        break;
      case "Enter":
      case " ":
      case "Spacebar":
        event.preventDefault();
        if (open) toggle(options[activeIndex]);
        else openListbox();
        break;
      case "Escape":
        if (open) { event.preventDefault(); setOpen(false); }
        break;
      case "Tab":
        if (open) setOpen(false);
        break;
    }
  }

  return (
    <div className="w-full">
      <label htmlFor={triggerId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValues.join(",")} disabled={disabled} readOnly /> : null}
        <button
          ref={triggerRef}
          id={triggerId}
          type="button"
          disabled={disabled}
          aria-haspopup="listbox"
          aria-expanded={open}
          aria-controls={open ? listboxId : undefined}
          aria-activedescendant={open ? `${triggerId}-opt-${activeIndex}` : undefined}
          onClick={() => (open ? setOpen(false) : openListbox())}
          onKeyDown={onKeyDown}
          className={cx(
            "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 motion-reduce:transition-none",
            "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]",
            SIZES[size],
            className,
          )}
        >
          <span className={cx("flex-1 truncate", selectedValues.length === 0 && "text-[var(--ds-color-muted-foreground)]")}>
            {summary}
          </span>
          <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? (
          <MultiPanel
            ref={listboxRef}
            id={listboxId}
            labelledby={triggerId}
            options={options}
            activeIndex={activeIndex}
            selectedSet={selectedSet}
            triggerId={triggerId}
            onToggle={toggle}
            onHover={setActiveIndex}
            onOutside={() => setOpen(false)}
          />
        ) : null}
      </div>
    </div>
  );
}

export default MultiSelect;

function MultiPanel({
  ref,
  id,
  labelledby,
  options,
  activeIndex,
  selectedSet,
  triggerId,
  onToggle,
  onHover,
  onOutside,
}: {
  ref: RefObject<HTMLDivElement>;
  id: string;
  labelledby: string;
  options: MultiOption[];
  activeIndex: number;
  selectedSet: Set<string>;
  triggerId: string;
  onToggle: (o: MultiOption) => void;
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
      aria-multiselectable="true"
      className="absolute z-20 mt-1.5 max-h-60 w-full overflow-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]"
    >
      {options.map((option, i) => {
        const isSelected = selectedSet.has(option.value);
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
            onClick={() => onToggle(option)}
            className={cx(
              "flex w-full items-center gap-2.5 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
              i === activeIndex ? "bg-[var(--ds-color-surface-hover)]" : "",
              isSelected ? "bg-[var(--ds-color-surface-selected)] font-medium" : "",
              option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : "",
            )}
          >
            <span className={cx(
              "flex size-[16px] shrink-0 items-center justify-center rounded-[var(--ds-radius-xs)] border transition-colors motion-reduce:transition-none",
              isSelected
                ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]"
                : "border-[var(--ds-color-border-strong)] bg-[var(--ds-color-input)]",
            )}>
              {isSelected ? <CheckIcon className="size-[12px]" /> : null}
            </span>
            <span className="truncate">{option.label}</span>
          </button>
        );
      })}
    </div>
  );
}
