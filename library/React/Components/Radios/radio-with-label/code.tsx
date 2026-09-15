import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface RadioWithLabelProps {
  label: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  invalid?: boolean;
  name?: string;
  value: string | number | readonly string[];
  id?: string;
  "aria-describedby"?: string;
  className?: string;
}

/**
 * A radio with a visibly-associated label. The label is wrapped in a
 * `<label htmlFor>` so clicking the text selects the option just like
 * clicking the control. Built on the native `<input type="radio">`.
 */
export function RadioWithLabel({
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
  "aria-describedby": ariaDescribedby,
  className,
}: RadioWithLabelProps) {
  const generatedId = useId();
  const inputId = id ?? `radio-${generatedId}`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }

  return (
    <label
      htmlFor={inputId}
      className={cx(
        "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
        disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer",
        className,
      )}
    >
      <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
        <input
          id={inputId}
          type="radio"
          className={cx(
            "size-[18px] cursor-pointer appearance-none rounded-full border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
            invalid
              ? "border-[var(--ds-color-destructive)] checked:border-[var(--ds-color-destructive)]"
              : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)]",
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
            "pointer-events-none absolute inset-0 flex items-center justify-center transition-opacity duration-150 motion-reduce:transition-none",
            isChecked ? "opacity-100" : "opacity-0",
          )}
        >
          <span
            className={cx(
              "block size-[8px] rounded-full",
              invalid ? "bg-[var(--ds-color-destructive)]" : "bg-[var(--ds-color-primary)]",
            )}
          />
        </span>
      </span>
      <span className="select-none">
        {label}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </span>
    </label>
  );
}

export default RadioWithLabel;
