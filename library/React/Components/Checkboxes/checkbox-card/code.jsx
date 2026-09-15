/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function CheckboxCard({
  label,
  description,
  checked,
  defaultChecked,
  onChange,
  disabled,
  required,
  invalid,
  name,
  value,
  id,
  "aria-describedby": ariaDescribedby,
  className
}) {
  const generatedId = useId();
  const inputId = id ?? `checkbox-card-${generatedId}`;
  const descId = `${inputId}-desc`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  const describedby = [description ? descId : null, ariaDescribedby].filter(Boolean).join(" ") || undefined;
  function handleChange(event) {
    const next = event.target.checked;
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  return <label
    htmlFor={inputId}
    className={cx(
      "relative flex w-full cursor-pointer items-start gap-3 rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-3.5 text-left transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-within:border-[var(--ds-color-border-strong)] motion-reduce:transition-none",
      disabled && "cursor-not-allowed opacity-60 hover:bg-[var(--ds-color-surface)]",
      invalid || !isChecked ? "border-[var(--ds-color-border)]" : "border-[var(--ds-color-primary)]",
      invalid && "border-[var(--ds-color-destructive)]",
      className
    )}
  >
      <span className="relative mt-0.5 inline-flex size-[18px] shrink-0 items-center justify-center">
        <input
    id={inputId}
    type="checkbox"
    className={cx(
      "size-[18px] cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
      invalid ? "border-[var(--ds-color-destructive)] checked:border-[var(--ds-color-destructive)] checked:bg-[var(--ds-color-destructive)]" : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]"
    )}
    checked={isControlled ? isChecked : undefined}
    defaultChecked={isControlled ? undefined : defaultChecked}
    disabled={disabled}
    required={required}
    aria-invalid={invalid ? true : undefined}
    aria-describedby={describedby}
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
      <span className="flex min-w-0 flex-1 flex-col gap-0.5">
        <span className="text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
          {label}
          {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
        </span>
        {description ? <span id={descId} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
            {description}
          </span> : null}
      </span>
    </label>;
}

export default CheckboxCard;
