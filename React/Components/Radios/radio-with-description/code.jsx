/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function RadioWithDescription({
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
  const inputId = id ?? `radio-${generatedId}`;
  const descId = `${inputId}-desc`;
  const describedby = [descId, ariaDescribedby].filter(Boolean).join(" ") || undefined;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  function handleChange(event) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }
  return <label
    htmlFor={inputId}
    className={cx(
      "inline-flex items-start gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
      disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer",
      className
    )}
  >
      <span className="relative mt-[3px] inline-flex size-[18px] shrink-0 items-center justify-center">
        <input
    id={inputId}
    type="radio"
    aria-describedby={describedby}
    className={cx(
      "size-[18px] cursor-pointer appearance-none rounded-full border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
      invalid ? "border-[var(--ds-color-destructive)]" : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)]"
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
      "pointer-events-none absolute inset-0 flex items-center justify-center transition-opacity duration-150 motion-reduce:transition-none",
      isChecked ? "opacity-100" : "opacity-0"
    )}
  >
          <span
    className={cx(
      "block size-[8px] rounded-full",
      invalid ? "bg-[var(--ds-color-destructive)]" : "bg-[var(--ds-color-primary)]"
    )}
  />
        </span>
      </span>
      <span className="flex flex-col gap-0.5">
        <span className="font-medium select-none">
          {label}
          {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
        </span>
        <span id={descId} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {description}
        </span>
      </span>
    </label>;
}

export default RadioWithDescription;
