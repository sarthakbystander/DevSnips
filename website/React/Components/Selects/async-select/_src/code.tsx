import type { KeyboardEvent, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface AsyncSelectProps {
  label?: string;
  loadOptions: (query: string) => Promise<SelectOption[]>;
  defaultOptions?: SelectOption[] | boolean;
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: SelectOption) => void;
  size?: SelectSize;
  placeholder?: string;
  loadingPlaceholder?: string;
  emptyMessage?: string;
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

function AlertGlyph({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 9v4M12 17h.01" />
      <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
    </svg>
  );
}

/**
 * Custom accessible select that loads its options ASYNCHRONOUSLY via the
 * consumer's `loadOptions(query)` promise. On open (and on any future
 * reopen) it calls `loadOptions("")` and renders a loading spinner state
 * (`aria-busy="true"` on the panel), then results. Promise rejection is
 * caught and surfaced as an inline error message inside the panel
 * (`role="alert"`). When `defaultOptions` is an array it is shown
 * immediately (and re-lazily on open); when `true` the panel opens with a
 * loading state until the first load resolves; when omitted the panel
 * loads on open. The component performs NO real network requests — it only
 * invokes the consumer's `loadOptions`. Full WAI-ARIA combobox/listbox
 * pattern: trigger button with `aria-haspopup="listbox"`,
 * `aria-expanded`, `aria-controls`, `aria-activedescendant`; panel with
 * `role="listbox"` of `role="option"` rows carrying `aria-selected`.
 * Keyboard: ArrowUp/Down/Home/End/Enter/Space/Escape/Tab. Outside-click +
 * Escape close. Controlled (value/onChange) and uncontrolled
 * (defaultValue) both supported.
 */
export function AsyncSelect({
  label = "Select",
  loadOptions,
  defaultOptions,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Select an option",
  loadingPlaceholder = "Loading…",
  emptyMessage = "No results",
  id,
  name,
  className,
}: AsyncSelectProps) {
  const generatedId = useId();
  const triggerId = id ?? `select-${generatedId}`;
  const listboxId = `${triggerId}-listbox`;
  const statusId = `${triggerId}-status`;

  const isDefaultArray = Array.isArray(defaultOptions);
  const [options, setOptions] = useState<SelectOption[]>(() => (isDefaultArray ? (defaultOptions as SelectOption[]) : []));
  const [isLoading, setIsLoading] = useState(() => (isDefaultArray ? false : defaultOptions === true));
  const [error, setError] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);

  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;

  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);
  const reqRef = useRef(0);

  function runLoad(query: string) {
    const token = ++reqRef.current;
    setIsLoading(true);
    setError(null);
    Promise.resolve()
      .then(() => loadOptions(query))
      .then((res) => {
        if (token !== reqRef.current) return;
        const next = Array.isArray(res) ? res : [];
        setOptions(next);
        setIsLoading(false);
        setLoaded(true);
        setActiveIndex(() => {
          const enabled = next.findIndex((o) => !o.disabled);
          return enabled === -1 ? 0 : enabled;
        });
      })
      .catch((err: unknown) => {
        if (token !== reqRef.current) return;
        setError(err instanceof Error ? err.message : "Failed to load options");
        setIsLoading(false);
      });
  }

  useEffect(() => {
    if (open && !loaded && !isLoading && !error) {
      runLoad("");
    }
  }, [open, loaded, isLoading, error, loadOptions]);

  useEffect(() => {
    return () => { ++reqRef.current; };
  }, []);

  function openListbox(nextActive?: number) {
    setOpen(true);
    const cur = selected ? options.indexOf(selected) : -1;
    const fallback = options.findIndex((o) => !o.disabled);
    const start = nextActive ?? (cur >= 0 ? cur : fallback);
    setActiveIndex(Math.max(0, Math.min(Math.max(options.length - 1, 0), start < 0 ? 0 : start)));
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
        if (open) {
          if (!isLoading && options[activeIndex]) choose(options[activeIndex]);
        } else {
          openListbox();
        }
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
          aria-activedescendant={open && !isLoading && !error && options[activeIndex] ? `${triggerId}-opt-${activeIndex}` : undefined}
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
          <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? (
          <ListboxPanel
            ref={listboxRef}
            id={listboxId}
            labelledby={triggerId}
            statusId={statusId}
            options={options}
            isLoading={isLoading}
            error={error}
            loadingPlaceholder={loadingPlaceholder}
            emptyMessage={emptyMessage}
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

export default AsyncSelect;

function ListboxPanel({
  ref,
  id,
  labelledby,
  statusId,
  options,
  isLoading,
  error,
  loadingPlaceholder,
  emptyMessage,
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
  statusId: string;
  options: SelectOption[];
  isLoading: boolean;
  error: string | null;
  loadingPlaceholder: string;
  emptyMessage: string;
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
    if (isLoading || error) return;
    const el = ref.current?.querySelector(`[data-i="${activeIndex}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex, ref, isLoading, error]);

  return (
    <div
      ref={ref}
      id={id}
      role="listbox"
      aria-labelledby={labelledby}
      aria-busy={isLoading || undefined}
      className="absolute z-20 mt-1.5 max-h-60 w-full overflow-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]"
    >
      {error ? (
        <div id={statusId} role="alert" className="flex items-center gap-2 px-2.5 py-2 text-[13px] text-[var(--ds-color-destructive)]">
          <AlertGlyph className="size-4 shrink-0" />
          <span className="truncate">{error}</span>
        </div>
      ) : isLoading ? (
        <div id={statusId} className="flex items-center gap-2 px-2.5 py-2 text-[13px] text-[var(--ds-color-muted-foreground)]">
          <Spinner className="size-4 shrink-0 animate-spin motion-reduce:animate-none" />
          <span>{loadingPlaceholder}</span>
        </div>
      ) : options.length === 0 ? (
        <div id={statusId} className="px-2.5 py-2 text-[13px] text-[var(--ds-color-muted-foreground)]">
          {emptyMessage}
        </div>
      ) : (
        options.map((option, i) => (
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
              <svg className="shrink-0 size-4 text-[var(--ds-color-primary)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M20 6 9 17l-5-5" />
              </svg>
            ) : null}
          </button>
        ))
      )}
    </div>
  );
}
