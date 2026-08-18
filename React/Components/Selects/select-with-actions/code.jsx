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
function PlusGlyph({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 5v14M5 12h14" />
    </svg>;
}
function GearGlyph({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09A1.65 1.65 0 0 0 15 4.6a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1Z" />
    </svg>;
}
function ActionIcon({ action }) {
  if (action.icon) return <span className="shrink-0">{action.icon}</span>;
  const label = action.label.toLowerCase();
  if (label.startsWith("add") || label.includes("new")) return <PlusGlyph className="size-4 shrink-0" />;
  if (label.includes("manage") || label.includes("settings") || label.includes("edit")) return <GearGlyph className="size-4 shrink-0" />;
  return <PlusGlyph className="size-4 shrink-0" />;
}
export function SelectWithActions({
  label = "Select",
  helperText,
  options,
  value,
  defaultValue = "",
  onChange,
  actions,
  size = "md",
  placeholder = "Select an option",
  id,
  name,
  className
}) {
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
  const triggerRef = useRef(null);
  const listboxRef = useRef(null);
  function openListbox(nextActive) {
    setOpen(true);
    const cur = selected ? options.indexOf(selected) : -1;
    const fallback = options.findIndex((o) => !o.disabled);
    const start = nextActive ?? (cur >= 0 ? cur : fallback);
    setActiveIndex(Math.max(0, Math.min(options.length - 1, start < 0 ? 0 : start)));
  }
  function choose(option) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
    setOpen(false);
    triggerRef.current?.focus();
  }
  function runAction(action) {
    if (action.disabled) return;
    setOpen(false);
    action.onSelect();
    triggerRef.current?.focus();
  }
  function moveActive(step) {
    setActiveIndex((cur) => {
      let next = cur;
      for (let i = 0; i < options.length; i++) {
        next = (next + step + options.length) % options.length;
        if (!options[next].disabled) return next;
      }
      return cur;
    });
  }
  function onKeyDown(event) {
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
        if (open) {
          event.preventDefault();
          for (let i = 0; i < options.length; i++) if (!options[i].disabled) {
            setActiveIndex(i);
            break;
          }
        }
        break;
      case "End":
        if (open) {
          event.preventDefault();
          for (let i = options.length - 1; i >= 0; i--) if (!options[i].disabled) {
            setActiveIndex(i);
            break;
          }
        }
        break;
      case "Enter":
      case " ":
      case "Spacebar":
        event.preventDefault();
        if (open) choose(options[activeIndex]);
        else openListbox();
        break;
      case "Escape":
        if (open) {
          event.preventDefault();
          setOpen(false);
        }
        break;
      case "Tab":
        if (open) setOpen(false);
        break;
    }
  }
  const selectedIndex = selected ? options.indexOf(selected) : -1;
  return <div className="w-full">
      <label htmlFor={triggerId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      {helperText ? <p id={messageId} className="mb-2 text-xs text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p> : null}
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
    onClick={() => open ? setOpen(false) : openListbox()}
    onKeyDown={onKeyDown}
    className={cx(
      "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
      SIZES[size],
      className
    )}
  >
          <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
            {selected ? selected.label : placeholder}
          </span>
          <ChevronDown className={cx("shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none", open && "rotate-180")} />
        </button>
        {open ? <ListboxPanel
    ref={listboxRef}
    id={listboxId}
    labelledby={triggerId}
    options={options}
    actions={actions}
    activeIndex={activeIndex}
    selectedIndex={selectedIndex}
    triggerId={triggerId}
    onChoose={choose}
    onHover={setActiveIndex}
    onAction={runAction}
    onOutside={() => setOpen(false)}
  /> : null}
      </div>
    </div>;
}
function ListboxPanel({
  ref,
  id,
  labelledby,
  options,
  actions,
  activeIndex,
  selectedIndex,
  triggerId,
  onChoose,
  onHover,
  onAction,
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
    const el = ref.current?.querySelector(`[data-i="${activeIndex}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex, ref]);
  return <div
    ref={ref}
    id={id}
    role="listbox"
    aria-labelledby={labelledby}
    className="absolute z-20 mt-1.5 max-h-60 w-full overflow-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]"
  >
      <div className="overflow-y-auto">
        {options.map((option, i) => <button
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
      option.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : ""
    )}
  >
            <span className="truncate">{option.label}</span>
            {i === selectedIndex ? <svg className="shrink-0 size-4 text-[var(--ds-color-primary)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M20 6 9 17l-5-5" />
              </svg> : null}
          </button>)}
      </div>
      {actions.length > 0 ? <div className="mt-1 border-t border-[var(--ds-color-border)] pt-1">
          {actions.map((action, i) => <button
    key={`${action.label}-${i}`}
    type="button"
    disabled={action.disabled || undefined}
    onClick={() => onAction(action)}
    className={cx(
      "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-left text-[13px] font-medium text-[var(--ds-color-foreground)] transition-colors motion-reduce:transition-none hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
      action.disabled ? "cursor-not-allowed text-[var(--ds-color-muted-foreground)] opacity-60" : ""
    )}
  >
              <ActionIcon action={action} />
              <span className="flex-1 truncate">{action.label}</span>
            </button>)}
        </div> : null}
    </div>;
}

export default SelectWithActions;
