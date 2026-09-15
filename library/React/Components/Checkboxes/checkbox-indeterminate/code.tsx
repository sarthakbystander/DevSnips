import type { ChangeEvent, ReactNode } from "react";
import { useEffect, useId, useRef, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface CheckboxIndeterminateProps {
  label?: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  indeterminate?: boolean;
  onChange?: (checked: boolean, event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  invalid?: boolean;
  name?: string;
  value?: string | number | readonly string[];
  id?: string;
  "aria-describedby"?: string;
  className?: string;
}

/**
 * Checkbox that supports a REAL indeterminate state. The underlying
 * `HTMLInputElement.indeterminate` property is set imperatively on the DOM
 * node (there is no HTML attribute for it) via a layout-effect that runs
 * whenever `indeterminate` changes. The indeterminate indicator is a
 * horizontal dash, distinct from the checked check mark. Built on the native
 * `<input type="checkbox">`.
 */
export function CheckboxIndeterminate({
  label,
  checked,
  defaultChecked,
  indeterminate = false,
  onChange,
  disabled,
  required,
  invalid,
  name,
  value,
  id,
  "aria-describedby": ariaDescribedby,
  className,
}: CheckboxIndeterminateProps) {
  const generatedId = useId();
  const inputId = id ?? `checkbox-${generatedId}`;
  const ref = useRef<HTMLInputElement>(null);
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;

  // Imperatively set the indeterminate IDL property — no HTML attribute.
  useEffect(() => {
    if (ref.current) ref.current.indeterminate = indeterminate;
  }, [indeterminate]);

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event.target.checked, event);
  }

  const control = (
    <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
      <input
        ref={ref}
        id={inputId}
        type="checkbox"
        className={cx(
          "size-[18px] cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
          invalid
            ? "border-[var(--ds-color-destructive)]"
            : "border-[var(--ds-color-border)]",
          (indeterminate || isChecked) && !invalid
            ? "bg-[var(--ds-color-primary)] border-[var(--ds-color-primary)]"
            : "",
          (indeterminate || isChecked) && invalid
            ? "bg-[var(--ds-color-destructive)] border-[var(--ds-color-destructive)]"
            : "",
        )}
        checked={isControlled ? isChecked : undefined}
        defaultChecked={isControlled ? undefined : defaultChecked}
        disabled={disabled}
        required={required}
        aria-invalid={invalid ? true : undefined}
        aria-describedby={ariaDescribedby}
        name={name}
        value={value}
        onChange={handleChange}
      />
      <span
        aria-hidden="true"
        className={cx(
          "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
          indeterminate || isChecked ? "opacity-100" : "opacity-0",
        )}
      >
        {indeterminate ? (
          <span className="block h-[2px] w-[10px] rounded-full bg-current" />
        ) : (
          <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 6 9 17l-5-5" />
          </svg>
        )}
      </span>
    </span>
  );

  if (!label) return control;

  return (
    <label
      htmlFor={inputId}
      className={cx(
        "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
        disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer",
        className,
      )}
    >
      {control}
      <span className="select-none">
        {label}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </span>
    </label>
  );
}

export default CheckboxIndeterminate;
