import type { KeyboardEvent, ReactNode, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface LanguageOption {
  value: string;
  label: string;
  nativeName?: string;
  disabled?: boolean;
}

export interface LanguageSelectProps {
  label?: string;
  options: LanguageOption[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: LanguageOption) => void;
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

function GlobeIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18" />
    </svg>
  );
}

/**
 * Language single-select. Options may carry a `nativeName` (e.g. "中文" for a
 * spoken language, or a short locale code) which is shown next to the label as
 * muted text. The trigger shows the selected label (plus its native name when
 * present). Full WAI-ARIA combobox/listbox pattern: ArrowUp/Down/Home/End move
 * the active option, Enter/Space selects, Escape closes; outside-click closes.
 * Controlled (value/onChange) and uncontrolled (defaultValue) both supported.
 */
export function LanguageSelect({
  label = "Language",
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Select a language",
  id,
  name,
  className,
}: LanguageSelectProps) {
  const generatedId = useId();
  const triggerId = id ?? `language-select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;

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

  function choose(option: LanguageOption) {
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
          onClick={() => (open ? setOpen(false) : openListbox())}
          onKeyDown={onKeyDown}
          className={cx(
            "inline-flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] pl-3 pr-2.5 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 motion-reduce:transition-none",
            "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]",
            SIZES[size],
            className,
          )}
        >
          <GlobeIcon className="shrink-0 text-[var(--ds-color-muted-foreground)]" />
          <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
            {selected ? (
              <span className="inline-flex items-center gap-2">
                <span className="truncate">{selected.label}</span>
                {selected.nativeName ? (
                  <span className="truncate text-[var(--ds-color-muted-foreground)]">{selected.nativeName}</span>
                ) : null}
              </span>
            ) : placeholder}
          </span>
          <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? (
          <LanguagePanel
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

export default LanguageSelect;

function LanguagePanel({
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
  options: LanguageOption[];
  activeIndex: number;
  selectedIndex: number;
  triggerId: string;
  onChoose: (o: LanguageOption) => void;
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
          <span className="flex min-w-0 items-baseline gap-2">
            <span className="truncate">{option.label}</span>
            {option.nativeName ? (
              <span className="truncate text-[var(--ds-color-muted-foreground)]">{option.nativeName}</span>
            ) : null}
          </span>
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
