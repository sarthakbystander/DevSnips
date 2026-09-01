/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const TEXTAREA_BASE = "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";
const TEXTAREA_BORDER = "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";
export function TextareaWithCounter({
  label,
  helperText,
  id,
  className,
  rows = 3,
  value,
  defaultValue = "",
  onChange,
  maxLength,
  ...props
}) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const countId = `${textareaId}-count`;
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? ""));
  const currentValue = value === undefined ? internalValue : String(value ?? "");
  const atLimit = maxLength !== undefined && currentValue.length >= maxLength;
  function handleChange(event) {
    if (value === undefined) setInternalValue(event.target.value);
    onChange?.(event);
  }
  return <div className="w-full">
      <label
    htmlFor={textareaId}
    className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
  >
        {label}
      </label>
      <textarea
    id={textareaId}
    rows={rows}
    value={currentValue}
    onChange={handleChange}
    maxLength={maxLength}
    aria-describedby={countId}
    className={cx(TEXTAREA_BASE, TEXTAREA_BORDER, className)}
    {...props}
  />
      <div
    id={countId}
    aria-live="polite"
    className="mt-2 flex items-baseline justify-between gap-3 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
  >
        <span>{helperText}</span>
        <span className={cx("shrink-0", atLimit && "font-medium text-[var(--ds-color-foreground)]")}>
          {currentValue.length}{maxLength !== undefined ? ` / ${maxLength}` : ""}
        </span>
      </div>
    </div>;
}

export default TextareaWithCounter;
