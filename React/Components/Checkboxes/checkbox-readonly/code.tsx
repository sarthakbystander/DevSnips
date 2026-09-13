import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface CheckboxReadonlyProps {
  label: ReactNode;
  checked: boolean;
  onChange?: (checked: boolean, event: ChangeEvent<HTMLInputElement>) => void;
  name?: string;
  value?: string | number | readonly string[];
  id?: string;
  helperText?: ReactNode;
  className?: string;
}

/**
 * Read-only checkbox. The control cannot be changed by the user but is NOT
 * disabled — it remains focusable and perceivable as part of the document
 * (e.g. a permission that is fixed). The native input uses `readOnly` plus a
 * `preventDefault` on change (browsers do not natively honor `readOnly` on
 * checkboxes), so clicks and Space do not toggle the value.
 */
export function CheckboxReadonly({
  label,
  checked,
  onChange,
  name,
  value,
  id,
  helperText,
  className,
}: CheckboxReadonlyProps) {
  const generatedId = useId();
  const inputId = id ?? `checkbox-${generatedId}`;
  const helperId = `${inputId}-helper`;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    // Browsers do not honor `readOnly` on checkboxes — force the rendered
    // state back so it cannot be toggled. The onChange callback still fires so
    // a parent can log the (blocked) attempt if it wants.
    event.preventDefault();
    onChange?.(checked, event);
  }

  return (
    <div className={cx("flex flex-col gap-1", className)}>
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
              checked ? "opacity-100" : "opacity-0",
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

export default CheckboxReadonly;
