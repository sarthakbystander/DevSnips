/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function SwitchLoading({
  label,
  loading,
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
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  const isBusy = Boolean(loading);
  const isDisabled = disabled || isBusy;
  function handleChange(event) {
    const next = event.target.checked;
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  return <label
    htmlFor={inputId}
    className={cx(
      "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
      isDisabled ? "cursor-not-allowed" : "cursor-pointer",
      className
    )}
  >
      <span className={cx("relative inline-flex h-[14px] w-[24px] shrink-0 items-center", isDisabled && "opacity-50")}>
        <input
    id={inputId}
    type="checkbox"
    role="switch"
    aria-checked={isChecked}
    aria-busy={isBusy ? true : undefined}
    className={cx(
      "absolute inset-0 h-full w-full cursor-pointer appearance-none rounded-full border transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none",
      isChecked ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)] bg-[var(--ds-color-input)]"
    )}
    checked={isControlled ? isChecked : undefined}
    defaultChecked={isControlled ? undefined : defaultChecked}
    disabled={isDisabled}
    name={name}
    value={value}
    onChange={handleChange}
  />
        {isBusy ? <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute left-[2px] top-[2px] flex size-[10px] items-center justify-center",
      isChecked ? "translate-x-[10px]" : "translate-x-0",
      isChecked ? "text-[var(--ds-color-primary-foreground)]" : "text-[var(--ds-color-muted-foreground)]"
    )}
  >
            <svg
    className="size-[10px] animate-spin motion-reduce:animate-none"
    viewBox="0 0 16 16"
    fill="none"
    stroke="currentColor"
  >
              <circle cx="8" cy="8" r="6" strokeOpacity={0.25} strokeWidth={2.5} />
              <path d="M14 8a6 6 0 0 0-6-6" strokeWidth={2.5} strokeLinecap="round" />
            </svg>
          </span> : <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute left-[2px] top-[2px] size-[10px] rounded-full transition-[transform,background-color] duration-150 ease-out motion-reduce:transition-none",
      isChecked ? "translate-x-[10px]" : "translate-x-0",
      isChecked ? "bg-[var(--ds-color-primary-foreground)]" : "bg-[var(--ds-color-muted-foreground)]"
    )}
  />}
      </span>
      <span className="select-none">{label}</span>
    </label>;
}

export default SwitchLoading;
