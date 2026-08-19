/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function CheckboxReadonly({
  label,
  checked,
  onChange,
  name,
  value,
  id,
  helperText,
  className
}) {
  const generatedId = useId();
  const inputId = id ?? `checkbox-${generatedId}`;
  const helperId = `${inputId}-helper`;
  function handleChange(event) {
    event.preventDefault();
    onChange?.(checked, event);
  }
  return <div className={cx("flex flex-col gap-1", className)}>
      <label
    htmlFor={inputId}
    className="inline-flex cursor-default items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]"
  >
        <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
    id={inputId}
    type="checkbox"
    readOnly
    aria-readonly="true"
    aria-describedby={helperText ? helperId : undefined}
    className="size-[18px] cursor-default appearance-none rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] checked:border-[var(--ds-color-muted-foreground)] checked:bg-[var(--ds-color-muted-foreground)] motion-reduce:transition-none"
    checked={checked}
    name={name}
    value={value}
    onChange={handleChange}
  />
          <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
      checked ? "opacity-100" : "opacity-0"
    )}
  >
            <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 6 9 17l-5-5" />
            </svg>
          </span>
        </span>
        <span className="select-none">{label}</span>
      </label>
      {helperText ? <p id={helperId} className="pl-[26px] text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p> : null}
    </div>;
}

export default CheckboxReadonly;
