import type { KeyboardEvent, ReactNode, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface SelectOption {
  value: string;
  label: string;
  avatar?: ReactNode;
  description?: string;
  disabled?: boolean;
}

export interface SelectWithAvatarProps {
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

function CheckGlyph() {
  return (
    <svg className="shrink-0 size-4 text-[var(--ds-color-primary)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 6 9 17l-5-5" />
    </svg>
  );
}

function initialsOf(label: string): string {
  const parts = label.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function AvatarSlot({ option, className }: { option?: SelectOption | null; className?: string }) {
  if (option?.avatar) {
    return <span className={cx("size-5 shrink-0 overflow-hidden rounded-full", className)}>{option.avatar}</span>;
  }
  return (
    <span
      className={cx(
        "flex size-5 shrink-0 items-center justify-center rounded-full bg-[var(--ds-color-muted)] text-[10px] font-semibold leading-none text-[var(--ds-color-muted-foreground)]",
        className,
      )}
      aria-hidden="true"
    >
      {option ? initialsOf(option.label) : "?"}
    </span>
  );
}

/**
 * Custom accessible single-select listbox where each option carries an
 * optional `avatar` (ReactNode) and `description`. The selected option's
 * avatar is mirrored in the trigger alongside the label, vertically
 * centered. When no avatar is supplied, a 20px (`size-5`) circle fallback
 * showing the option's initials is rendered instead. Implements the full
 * WAI-ARIA combobox/listbox pattern: trigger button with
 * `aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`,
 * `aria-activedescendant`; panel with `role="listbox"` of `role="option"`
 * rows carrying `aria-selected`. Keyboard: ArrowUp/Down/Home/End/Enter/
 * Space/Escape/Tab. Outside-click + Escape close. Controlled
 * (value/onChange) and uncontrolled (defaultValue) both supported.
 */
export function SelectWithAvatar({
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
}: SelectWithAvatarProps) {
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
          <span className="flex min-w-0 flex-1 items-center gap-2">
            <AvatarSlot option={selected} />
            <span className="flex min-w-0 flex-col leading-tight">
              <span className={cx("truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
                {selected ? selected.label : placeholder}
              </span>
            </span>
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

export default SelectWithAvatar;

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
            "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
            i === activeIndex ? "bg-[var(--ds-color-surface-hover)]" : "",
            i === selectedIndex ? "font-medium" : "",
            option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : "",
          )}
        >
          <AvatarSlot option={option} />
          <span className="flex min-w-0 flex-1 flex-col leading-tight">
            <span className="truncate">{option.label}</span>
            {option.description ? (
              <span className="truncate text-[11px] text-[var(--ds-color-muted-foreground)]">{option.description}</span>
            ) : null}
          </span>
          {i === selectedIndex ? <CheckGlyph /> : null}
        </button>
      ))}
    </div>
  );
}
