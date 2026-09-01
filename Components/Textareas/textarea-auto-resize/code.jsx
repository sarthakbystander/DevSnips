/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useCallback, useEffect, useId, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const TEXTAREA_BASE = "w-full min-h-[80px] resize-none overflow-y-auto rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";
const TEXTAREA_BORDER = "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";
export function TextareaAutoResize({
  label,
  id,
  className,
  rows = 3,
  maxHeight = 320,
  value,
  defaultValue = "",
  onChange,
  ...props
}) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const ref = useRef(null);
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? ""));
  const currentValue = value === undefined ? internalValue : String(value ?? "");
  const adjust = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`;
  }, [maxHeight]);
  useEffect(() => {
    adjust();
  }, [adjust, currentValue]);
  useEffect(() => {
    window.addEventListener("resize", adjust);
    document.fonts.ready.then(adjust).catch(() => {
    });
    return () => window.removeEventListener("resize", adjust);
  }, [adjust]);
  function handleChange(event) {
    if (value === undefined) setInternalValue(event.target.value);
    onChange?.(event);
  }
  const control = <textarea
    ref={ref}
    id={textareaId}
    rows={rows}
    value={currentValue}
    onChange={handleChange}
    className={cx(TEXTAREA_BASE, TEXTAREA_BORDER, className)}
    {...props}
  />;
  if (label === undefined || label === null) {
    return control;
  }
  return <div className="w-full">
      <label
    htmlFor={textareaId}
    className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
  >
        {label}
      </label>
      {control}
    </div>;
}

export default TextareaAutoResize;
