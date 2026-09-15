import type { KeyboardEvent, ReactNode, RefObject } from "react";
import { useEffect, useId, useRef, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface InlineEditOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface InlineEditSelectProps {
  label?: string;
  options: InlineEditOption[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string, option: InlineEditOption) => void;
  size?: SelectSize;
  id?: string;
  name?: string;
  className?: string;
  editLabel?: string;
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

function PencilIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
    </svg>
  );
}

/**
 * Inline-editable single value. Displays the selected option's label as static
 * text with a subtle hover affordance and an edit pencil. Activating the row
 * (click / Enter) reveals an editable combobox-style select. Choosing an option
 * saves it and returns to display. Escape cancels (reverts to the value held
 * before editing) and returns to display. Outside-click while editing closes
 * and KEEPS the current selection. Full listbox keyboard nav while open.
 * Controlled (value/onChange) + uncontrolled (defaultValue).
 */
export function InlineEditSelect({
  label,
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  id,
  name,
  className,
  editLabel = "Edit",
}: InlineEditSelectProps) {
  const generatedId = useId();
  const rootId = id ?? `inline-edit-select-${generatedId}`;
  const labelId = `${rootId}-label`;
  const triggerId = `${rootId}-trigger`;
  const listboxId = `${rootId}-listbox`;

  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;

  const [editing, setEditing] = useState(false);
  const [draftValue, setDraftValue] = useState(selectedValue);
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(() => {
    const enabled = options.findIndex((o) => !o.disabled);
    return enabled === -1 ? 0 : enabled;
  });

  const rootRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const displayRef = useRef<HTMLButtonElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);

  function startEditing() {
    setDraftValue(selectedValue);
    setEditing(true);
    setOpen(true);
    const cur = selected ? options.indexOf(selected) : -1;
    const fallback = options.findIndex((o) => !o.disabled);
    const start = cur >= 0 ? cur : fallback;
    setActiveIndex(Math.max(0, Math.min(options.length - 1, start < 0 ? 0 : start)));
  }

  function commit(nextValue: string) {
    const option = options.find((o) => o.value === nextValue) ?? null;
    if (option && option.value !== selectedValue) {
      if (value === undefined) setInternalValue(option.value);
      onChange?.(option.value, option);
    }
    setEditing(false);
    setOpen(false);
  }

  function cancel() {
    setEditing(false);
    setOpen(false);
  }

  function choose(option: InlineEditOption) {
    if (option.disabled) return;
    setDraftValue(option.value);
    commit(option.value);
    displayRef.current?.focus();
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

  // Outside-click while editing: close + keep current selection (commit draft).
  useEffect(() => {
    if (!editing) return;
    function onDown(e: MouseEvent) {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) {
        commit(draftValue);
      }
    }
    document.addEventListener("mousedown", onDown);
    return () => document.removeEventListener("mousedown", onDown);
  }, [editing, draftValue, selectedValue, value]);

  function onTriggerKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        if (!open) setOpen(true);
        else moveActive(1);
        break;
      case "ArrowUp":
        event.preventDefault();
        if (!open) setOpen(true);
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
        else setOpen(true);
        break;
      case "Escape":
        event.preventDefault();
        cancel();
        displayRef.current?.focus();
        break;
      case "Tab":
        if (open) setOpen(false);
        break;
    }
  }

  function onDisplayKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (event.key === "Enter" || event.key === " " || event.key === "Spacebar") {
      event.preventDefault();
      startEditing();
    }
  }

  const selectedIndex = selected ? options.indexOf(selected) : -1;

  return (
    <div ref={rootRef} className={cx("w-full", className)}>
      {label ? (
        <span id={labelId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
          {label}
        </span>
      ) : null}
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValue} readOnly /> : null}
        {editing ? (
          <button
            ref={triggerRef}
            id={triggerId}
            type="button"
            aria-haspopup="listbox"
            aria-expanded={open}
            aria-controls={open ? listboxId : undefined}
            aria-activedescendant={open ? `${triggerId}-opt-${activeIndex}` : undefined}
            aria-label={editLabel}
            onClick={() => setOpen((o) => !o)}
            onKeyDown={onTriggerKeyDown}
            className={cx(
              "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
              "border-[var(--ds-color-border-strong)]",
              SIZES[size],
            )}
          >
            <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
              {selected ? selected.label : "Select an option"}
            </span>
            <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
          </button>
        ) : (
          <button
            ref={displayRef}
            type="button"
            aria-label={editLabel}
            onClick={startEditing}
            onKeyDown={onDisplayKeyDown}
            className={cx(
              "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-transparent px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
              SIZES[size],
            )}
          >
            <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
              {selected ? selected.label : "—"}
            </span>
            <PencilIcon className="shrink-0 text-[var(--ds-color-muted-foreground)]" />
          </button>
        )}
        {editing && open ? (
          <InlineEditPanel
            ref={listboxRef}
            id={listboxId}
            labelledby={label ? labelId : triggerId}
            options={options}
            activeIndex={activeIndex}
            selectedIndex={selectedIndex}
            triggerId={triggerId}
            onChoose={choose}
            onHover={setActiveIndex}
          />
        ) : null}
      </div>
    </div>
  );
}

export default InlineEditSelect;

function InlineEditPanel({
  ref,
  id,
  labelledby,
  options,
  activeIndex,
  selectedIndex,
  triggerId,
  onChoose,
  onHover,
}: {
  ref: RefObject<HTMLDivElement>;
  id: string;
  labelledby: string;
  options: InlineEditOption[];
  activeIndex: number;
  selectedIndex: number;
  triggerId: string;
  onChoose: (o: InlineEditOption) => void;
  onHover: (i: number) => void;
}) {
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
