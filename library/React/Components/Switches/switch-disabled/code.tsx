import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface SwitchDisabledProps {
  label: ReactNode;
  helperText?: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  onChange?: (checked: boolean, event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  name?: string;
  value?: string | number | readonly string[];
  id?: string;
  className?: string;
}

/**
 * Switch variant focused on the disabled (non-interactive) state. The native
 * `disabled` attribute carries the semantics; the visual treatment uses
 * reduced opacity + muted foreground so the control stays perceivable without
 * looking interactive. Built on the native `<input type="checkbox"
 * role="switch">`.
 */
export function SwitchDisabled({
  label,
  helperText,
  checked,
  defaultChecked,
  onChange,
  disabled = true,
  name,
  value,
  id,
  className,
}: SwitchDisabledProps) {
  const generatedId = useId();
  const inputId = id ?? `switch-${generatedId}`;
  const helperId = `${inputId}-helper`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const next = event.target.checked;
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }

  return (
    <div className={cx("flex flex-col gap-1", className)}>
      <label
        htmlFor={inputId}
        className="inline-flex cursor-not-allowed items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-muted-foreground)]"
      >
        <span className="relative inline-flex h-[14px] w-[24px] shrink-0 items-center opacity-50">
          <input
            id={inputId}
            type="checkbox"
            role="switch"
            aria-checked={isChecked}
            aria-describedby={helperText ? helperId : undefined}
            className={cx(
              "absolute inset-0 h-full w-full cursor-not-allowed appearance-none rounded-full border transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
              isChecked
                ? "border-[var(--ds-color-muted-foreground)] bg-[var(--ds-color-muted-foreground)]"
                : "border-[var(--ds-color-border)] bg-[var(--ds-color-input)]",
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
              isChecked ? "translate-x-[10px] bg-[var(--ds-color-primary-foreground)]" : "translate-x-0 bg-[var(--ds-color-muted-foreground)]",
            )}
          />
        </span>
        <span className="select-none">{label}</span>
      </label>
      {helperText ? (
        <p id={helperId} className="pl-[34px] text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}

export default SwitchDisabled;
