import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface CheckboxDisabledProps {
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
 * Checkbox variant focused on the disabled (read-only non-interactive)
 * state. The native `disabled` attribute carries the semantics; the visual
 * treatment uses reduced opacity + muted foreground so the control stays
 * perceivable without looking interactive. Built on the native
 * `<input type="checkbox">`.
 */
export function CheckboxDisabled({
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
}: CheckboxDisabledProps) {
  const generatedId = useId();
  const inputId = id ?? `checkbox-${generatedId}`;
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
        className="inline-flex cursor-not-allowed items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-muted-foreground)] opacity-60"
      >
        <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
            id={inputId}
            type="checkbox"
            aria-describedby={helperText ? helperId : undefined}
            className="size-[18px] cursor-not-allowed appearance-none rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-muted)] opacity-50 checked:border-[var(--ds-color-muted-foreground)] checked:bg-[var(--ds-color-muted-foreground)] motion-reduce:transition-none"
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
              "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
              isChecked ? "opacity-100" : "opacity-0",
            )}
          >
            <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 6 9 17l-5-5" />
            </svg>
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

export default CheckboxDisabled;
