/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function SwitchWithStatus({
  label,
  onText = "Enabled",
  offText = "Disabled",
  checked,
  defaultChecked,
  onChange,
  disabled,
  name,
  value,
  id,
  className
}) {
  const generatedId = useId();
  const inputId = id ?? `switch-${generatedId}`;
  const statusId = `${inputId}-status`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  function handleChange(event) {
    const next = event.target.checked;
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  return <label
    htmlFor={inputId}
    className={cx(
      "flex w-full items-center gap-3 text-left",
      disabled ? "cursor-not-allowed" : "cursor-pointer",
      className
    )}
  >
      <span className="flex min-w-0 flex-1 flex-col gap-0.5">
        <span className="text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">{label}</span>
        <span
    id={statusId}
    className={cx(
      "text-xs leading-4",
      isChecked ? "text-[var(--ds-color-foreground)]" : "text-[var(--ds-color-muted-foreground)]"
    )}
  >
          {isChecked ? onText : offText}
        </span>
      </span>
      <span className={cx("relative inline-flex h-[14px] w-[24px] shrink-0 items-center", disabled && "opacity-50")}>
        <input
    id={inputId}
    type="checkbox"
    role="switch"
    aria-checked={isChecked}
    aria-describedby={statusId}
    className={cx(
      "absolute inset-0 h-full w-full cursor-pointer appearance-none rounded-full border transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none",
      isChecked ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)] bg-[var(--ds-color-input)]"
    )}
    checked={isControlled ? isChecked : undefined}
    defaultChecked={isControlled ? undefined : defaultChecked}
    disabled={disabled}
    name={name}
    value={value}
    onChange={handleChange}
  />
        <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute left-[2px] top-[2px] size-[10px] rounded-full transition-[transform,background-color] duration-150 ease-out motion-reduce:transition-none",
      isChecked ? "translate-x-[10px]" : "translate-x-0",
      isChecked ? "bg-[var(--ds-color-primary-foreground)]" : "bg-[var(--ds-color-muted-foreground)]"
    )}
  />
      </span>
    </label>;
}

export default SwitchWithStatus;
