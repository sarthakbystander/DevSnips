import type { KeyboardEvent, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectWithCheckboxesProps {
  label?: string;
  helperText?: string;
  options: SelectOption[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: SelectOption) => void;
  size?: SelectSize;
  placeholder?: string;
  id?: string;
  name?: string;
  className?: string;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const SIZES: Record<SelectSize, string> = {
  sm: "h-8 text-[13px]",
  md: "h-9 text-sm",
  lg: "h-11 text-sm",
};

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

/**
 * Custom accessible single-select listbox that emphasizes a checkbox
 * affordance. Each option row carries a 16px checkbox indicator (`size-4`,
 * `rounded-[var(--ds-radius-xs)]`, 1px `color.border` outline) that fills
 * and shows a check glyph exactly when the row is `aria-selected`. This is
 * SINGLE-select — selecting one option checks it and clears the others, so
 * the checkbox always reflects the currently selected value (mirroring the
 * listbox `aria-selected` state). Click, Enter, or Space selects and
 * closes. Full WAI-ARIA combobox/listbox pattern: trigger button with
 * `aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`,
 * `aria-activedescendant`; panel with `role="listbox"` of `role="option"`
 * rows carrying `aria-selected`. Keyboard: ArrowUp/Down/Home/End/Enter/
 * Space/Escape/Tab. Outside-click + Escape close. Controlled (value/
 * onChange) and uncontrolled (defaultValue) both supported.
 */
export function SelectWithCheckboxes({
  label = "Select",
  helperText,
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Select an option",
  id,
  name,
  className,
}: SelectWithCheckboxesProps) {
  const generatedId = useId();
  const triggerId = id ?? `select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;
  const messageId = `${triggerId}-message`;

  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;

  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(() => {
    const enabled = options.findIndex((o) => !o.disabled);
    return enabled === -1 ? 0 : enabled;
  });
  const triggerRef = useRef<HTMLButtonElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);

  function openListbox(nextActive?: number) {
    setOpen(true);
    const cur = selected ? options.indexOf(selected) : -1;
    const fallback = options.findIndex((o) => !o.disabled);
    const start = nextActive ?? (cur >= 0 ? cur : fallback);
    setActiveIndex(Math.max(0, Math.min(options.length - 1, start < 0 ? 0 : start)));
  }

  function choose(option: SelectOption) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
    setOpen(false);
    triggerRef.current?.focus();
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
        if (open) choose(options[activeIndex]);
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

  const selectedIndex = selected ? options.indexOf(selected) : -1;

  return (
    <div className="w-full">
      <label htmlFor={triggerId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      {helperText ? (
        <p id={messageId} className="mb-2 text-xs text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p>
      ) : null}
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValue} readOnly /> : null}
        <button
          ref={triggerRef}
          id={triggerId}
          type="button"
          aria-haspopup="listbox"
          aria-expanded={open}
          aria-controls={open ? listboxId : undefined}
          aria-activedescendant={open ? `${triggerId}-opt-${activeIndex}` : undefined}
          aria-describedby={helperText ? messageId : undefined}
          onClick={() => (open ? setOpen(false) : openListbox())}
          onKeyDown={onKeyDown}
          className={cx(
            "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
            SIZES[size],
            className,
          )}
        >
          <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
            {selected ? selected.label : placeholder}
          </span>
          <ChevronDown className={cx("shrink-0 size-4 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? (
          <ListboxPanel
            ref={listboxRef}
            id={listboxId}
            labelledby={triggerId}
            options={options}
            activeIndex={activeIndex}
            selectedIndex={selectedIndex}
            triggerId={triggerId}
            onChoose={choose}
            onHover={setActiveIndex}
            onOutside={() => setOpen(false)}
          />
        ) : null}
      </div>
    </div>
  );
}

export default SelectWithCheckboxes;

function ListboxPanel({
  ref,
  id,
  labelledby,
  options,
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
  options: SelectOption[];
  activeIndex: number;
  selectedIndex: number;
  triggerId: string;
  onChoose: (o: SelectOption) => void;
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
      {options.map((option, i) => {
        const checked = i === selectedIndex;
        return (
          <button
            key={option.value}
            id={`${triggerId}-opt-${i}`}
            type="button"
            data-i={i}
            role="option"
            aria-selected={checked}
            aria-disabled={option.disabled || undefined}
            disabled={option.disabled}
            onMouseEnter={() => onHover(i)}
            onClick={() => onChoose(option)}
            className={cx(
              "flex w-full items-center gap-2.5 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
              i === activeIndex ? "bg-[var(--ds-color-surface-hover)]" : "",
              checked ? "font-medium" : "",
              option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : "",
            )}
          >
            <span
              aria-hidden="true"
              className={cx(
                "flex size-4 shrink-0 items-center justify-center rounded-[var(--ds-radius-xs)] border transition-colors motion-reduce:transition-none",
                checked
                  ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]"
                  : "border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)]",
                i === activeIndex && !checked ? "border-[var(--ds-color-border-strong)]" : "",
                option.disabled && checked ? "opacity-60" : "",
              )}
            >
              {checked ? (
                <svg className="size-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M20 6 9 17l-5-5" />
                </svg>
              ) : null}
            </span>
            <span className="flex-1 truncate">{option.label}</span>
          </button>
        );
      })}
    </div>
  );
}
