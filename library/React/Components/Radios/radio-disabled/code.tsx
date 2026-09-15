import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface RadioDisabledProps {
  label: ReactNode;
  helperText?: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  name?: string;
  value: string | number | readonly string[];
  id?: string;
  className?: string;
}

/**
 * Radio variant focused on the disabled (non-interactive) state. The native
 * `disabled` attribute carries the semantics; the visual treatment uses
 * reduced opacity + muted foreground so the control stays perceivable
 * without looking interactive. Built on the native `<input type="radio">`.
 */
export function RadioDisabled({
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
}: RadioDisabledProps) {
  const generatedId = useId();
  const inputId = id ?? `radio-${generatedId}`;
  const helperId = `${inputId}-helper`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }

  return (
    <div className={cx("flex flex-col gap-1", className)}>
      <label
        htmlFor={inputId}
        className="inline-flex cursor-not-allowed items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-muted-foreground)] opacity-60"
      >
        <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
            id={inputId}
            type="radio"
            aria-describedby={helperText ? helperId : undefined}
            className="size-[18px] cursor-not-allowed appearance-none rounded-full border border-[var(--ds-color-border)] bg-[var(--ds-color-muted)] opacity-50 checked:border-[var(--ds-color-muted-foreground)] motion-reduce:transition-none"
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
              "pointer-events-none absolute inset-0 flex items-center justify-center transition-opacity duration-150 motion-reduce:transition-none",
              isChecked ? "opacity-100" : "opacity-0",
            )}
          >
            <span className="block size-[8px] rounded-full bg-[var(--ds-color-muted-foreground)]" />
          </span>
        </span>
        <span className="select-none">{label}</span>
      </label>
      {helperText ? (
        <p id={helperId} className="pl-[26px] text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}

export default RadioDisabled;
