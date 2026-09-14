/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  sm: "h-8 text-[13px] [&_svg]:size-[14px]",
  md: "h-9 text-sm [&_svg]:size-4",
  lg: "h-11 text-sm [&_svg]:size-[18px]"
};
export function SegmentedSelect({
  label = "Segment",
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  id,
  name,
  className
}) {
  const generatedId = useId();
  const groupId = id ?? `segmented-select-${generatedId}`;
  const labelId = `${groupId}-label`;
  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selectedIndex = options.findIndex((o) => o.value === selectedValue);
  const refs = useRef([]);
  const [focusedIndex, setFocusedIndex] = useState(() => {
    const sel = options.findIndex((o) => o.value === selectedValue && !o.disabled);
    if (sel >= 0) return sel;
    const enabled = options.findIndex((o) => !o.disabled);
    return enabled === -1 ? 0 : enabled;
  });
  function enabledIndex(start, step) {
    for (let i = 0; i < options.length; i++) {
      const next = (start + step * (i + 1) + options.length) % options.length;
      if (!options[next].disabled) return next;
    }
    return start;
  }
  function choose(option) {
    if (option.disabled) return;
    if (value === undefined) setInternalValue(option.value);
    onChange?.(option.value, option);
  }
  function focusSegment(i) {
    setFocusedIndex(i);
    refs.current[i]?.focus();
  }
  function onKeyDown(event) {
    switch (event.key) {
      case "ArrowRight":
      case "ArrowDown":
        event.preventDefault();
        focusSegment(enabledIndex(focusedIndex, 1));
        break;
      case "ArrowLeft":
      case "ArrowUp":
        event.preventDefault();
        focusSegment(enabledIndex(focusedIndex, -1));
        break;
      case "Home":
        event.preventDefault();
        for (let i = 0; i < options.length; i++) if (!options[i].disabled) {
          focusSegment(i);
          break;
        }
        break;
      case "End":
        event.preventDefault();
        for (let i = options.length - 1; i >= 0; i--) if (!options[i].disabled) {
          focusSegment(i);
          break;
        }
        break;
    }
  }
  return <div className={cx("w-full", className)}>
      <span id={labelId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </span>
      {name ? <input type="hidden" name={name} value={selectedValue} readOnly /> : null}
      <div
    role="radiogroup"
    aria-labelledby={labelId}
    onKeyDown={onKeyDown}
    className={cx(
      "inline-flex w-full items-stretch gap-1 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] p-1",
      SIZES[size]
    )}
  >
        {options.map((option, i) => {
    const isActive = i === selectedIndex;
    const isFocused = i === focusedIndex;
    const tabbable = isFocused && !option.disabled || focusedIndex < 0 && i === 0 && !option.disabled;
    return <button
      key={option.value}
      ref={(el) => {
        refs.current[i] = el;
      }}
      type="button"
      role="radio"
      aria-checked={isActive}
      aria-disabled={option.disabled || undefined}
      disabled={option.disabled}
      tabIndex={tabbable ? 0 : -1}
      onClick={() => {
        choose(option);
        setFocusedIndex(i);
      }}
      onFocus={() => setFocusedIndex(i)}
      className={cx(
        "flex flex-1 items-center justify-center gap-1.5 rounded-[var(--ds-radius-xs)] px-3 text-center transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
        isActive ? "border border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface-active)] font-medium text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]" : "border border-transparent bg-transparent text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]",
        option.disabled && !isActive ? "cursor-not-allowed opacity-50" : "",
        option.disabled && isActive ? "opacity-70" : ""
      )}
    >
              <span className="truncate">{option.label}</span>
            </button>;
  })}
      </div>
    </div>;
}

export default SegmentedSelect;
