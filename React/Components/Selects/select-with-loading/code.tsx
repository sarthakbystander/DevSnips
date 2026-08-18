import type { KeyboardEvent, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectWithLoadingProps {
  label?: string;
  helperText?: string;
  error?: string;
  options: SelectOption[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: SelectOption) => void;
  size?: SelectSize;
  placeholder?: string;
  loading?: boolean;
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

function Spinner({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeOpacity={0.25} strokeWidth={2.5} />
      <path d="M21 12a9 9 0 0 1-9 9" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" />
    </svg>
  );
}

/**
 * Accessible custom select demonstrating the LOADING state. While `loading`
 * is true the trigger is non-interactive (`aria-busy="true"`,
 * `pointer-events-none`) and a Spinner SVG replaces the chevron — animated
 * with `animate-spin` and guarded by `motion-reduce:animate-none`. When not
 * loading, the full WAI-ARIA combobox/listbox pattern is active: trigger
 * button with `aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`,
 * `aria-activedescendant`; panel with `role="listbox"` of `role="option"` rows
 * carrying `aria-selected`. Keyboard: ArrowUp/Down/Home/End/Enter/Space/
 * Escape/Tab. Outside-click + Escape close. Controlled (value/onChange) and
 * uncontrolled (defaultValue) both supported.
 */
export function SelectWithLoading({
  label = "Select",
  helperText,
  error,
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Select an option",
  loading = false,
  id,
  name,
  className,
}: SelectWithLoadingProps) {
  const generatedId = useId();
  const triggerId = id ?? `select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;
  const messageId = `${triggerId}-message`;
  const message = error ?? helperText;

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
    if (loading) return;
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
      {message ? (
        <p id={messageId} className={cx("mb-2 text-xs", error ? "text-[var(--ds-color-destructive)]" : "text-[var(--ds-color-muted-foreground)]")}>
          {error ? `Error: ${error}` : helperText}
        </p>
      ) : null}
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValue} readOnly /> : null}
        <button
          ref={triggerRef}
          id={triggerId}
          type="button"
          disabled={loading || undefined}
          aria-busy={loading || undefined}
          aria-haspopup="listbox"
          aria-expanded={open}
          aria-controls={open ? listboxId : undefined}
          aria-activedescendant={open ? `${triggerId}-opt-${activeIndex}` : undefined}
          aria-invalid={error ? true : undefined}
          aria-describedby={message ? messageId : undefined}
          onClick={() => (loading ? undefined : open ? setOpen(false) : openListbox())}
          onKeyDown={onKeyDown}
          className={cx(
            "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
            loading ? "pointer-events-none cursor-wait border-[var(--ds-color-border)] opacity-70" : cx(error ? "border-[var(--ds-color-destructive)]" : "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]"),
            SIZES[size],
            className,
          )}
        >
          <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
            {loading ? "Loading…" : selected ? selected.label : placeholder}
          </span>
          {loading ? (
            <Spinner className="shrink-0 size-4 animate-spin text-[var(--ds-color-muted-foreground)] motion-reduce:animate-none" />
          ) : (
            <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
          )}
        </button>
        {open && !loading ? (
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

export default SelectWithLoading;

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
      {options.map((option, i) => (
        <button
          key={option.value}
          id={`${triggerId}-opt-${i}`}
          type="button"
          data-i={i}
          role="option"
          aria-selected={i === selectedIndex}
          aria-disabled={option.disabled || undefined}
          disabled={option.disabled}
          onMouseEnter={() => onHover(i)}
          onClick={() => onChoose(option)}
          className={cx(
            "flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
            i === activeIndex ? "bg-[var(--ds-color-surface-hover)]" : "",
            i === selectedIndex ? "font-medium" : "",
            option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : "",
          )}
        >
          <span className="truncate">{option.label}</span>
          {i === selectedIndex ? (
            <svg className="shrink-0 text-[var(--ds-color-primary)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="M20 6 9 17l-5-5" />
            </svg>
          ) : null}
        </button>
      ))}
    </div>
  );
}
