/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function Switch({
  label,
  checked,
  defaultChecked,
  onChange,
  disabled,
  required,
  invalid,
  name,
  value,
  id,
  "aria-label": ariaLabel,
  "aria-labelledby": ariaLabelledby,
  "aria-describedby": ariaDescribedby,
  className,
  children
}) {
  const generatedId = useId();
  const inputId = id ?? `switch-${generatedId}`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  function handleChange(event) {
    const next = event.target.checked;
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  const control = <span className={cx("relative inline-flex h-[14px] w-[24px] shrink-0 items-center", disabled && "opacity-50")}>
      <input
    id={inputId}
    type="checkbox"
    role="switch"
    aria-checked={isChecked}
    className={cx(
      "absolute inset-0 h-full w-full cursor-pointer appearance-none rounded-full border transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none",
      invalid ? isChecked ? "border-[var(--ds-color-destructive)] bg-[var(--ds-color-destructive)]" : "border-[var(--ds-color-destructive)]" : isChecked ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)] bg-[var(--ds-color-input)]",
      className
    )}
    checked={isControlled ? isChecked : undefined}
    defaultChecked={isControlled ? undefined : defaultChecked}
    disabled={disabled}
    required={required}
    aria-invalid={invalid ? true : undefined}
    aria-label={ariaLabel}
    aria-labelledby={ariaLabelledby}
    aria-describedby={ariaDescribedby}
    name={name}
    value={value}
    onChange={handleChange}
  />
      <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute left-[2px] top-[2px] size-[10px] rounded-full transition-[transform,background-color] duration-150 ease-out motion-reduce:transition-none",
      isChecked ? "translate-x-[10px]" : "translate-x-0",
      invalid && isChecked ? "bg-[var(--ds-color-destructive-foreground)]" : isChecked ? "bg-[var(--ds-color-primary-foreground)]" : "bg-[var(--ds-color-muted-foreground)]"
    )}
  />
    </span>;
  if (!label && !children) {
    return control;
  }
  const labelContent = children ?? label;
  return <label
    htmlFor={inputId}
    className={cx(
      "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
      disabled ? "cursor-not-allowed" : "cursor-pointer"
    )}
  >
      {control}
      {labelContent ? <span className="select-none">{labelContent}</span> : null}
    </label>;
}

export default Switch;
