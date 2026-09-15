/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function CheckboxWithHelper({
  label,
  helperText,
  checked,
  defaultChecked,
  onChange,
  disabled,
  required,
  invalid,
  name,
  value,
  id,
  className
}) {
  const generatedId = useId();
  const inputId = id ?? `checkbox-${generatedId}`;
  const helperId = `${inputId}-helper`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  function handleChange(event) {
    const next = event.target.checked;
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  return <div className={cx("flex flex-col gap-1", className)}>
      <label
    htmlFor={inputId}
    className={cx(
      "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
      disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"
    )}
  >
        <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
    id={inputId}
    type="checkbox"
    aria-describedby={helperId}
    className={cx(
      "size-[18px] cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
      invalid ? "border-[var(--ds-color-destructive)] checked:border-[var(--ds-color-destructive)] checked:bg-[var(--ds-color-destructive)]" : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]"
    )}
    checked={isControlled ? isChecked : undefined}
    defaultChecked={isControlled ? undefined : defaultChecked}
    disabled={disabled}
    required={required}
    aria-invalid={invalid ? true : undefined}
    name={name}
    value={value}
    onChange={handleChange}
  />
          <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
      isChecked ? "opacity-100" : "opacity-0"
    )}
  >
            <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 6 9 17l-5-5" />
            </svg>
          </span>
        </span>
        <span className="select-none">
          {label}
          {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
        </span>
      </label>
      <p id={helperId} className="pl-[26px] text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
        {helperText}
      </p>
    </div>;
}

export default CheckboxWithHelper;
