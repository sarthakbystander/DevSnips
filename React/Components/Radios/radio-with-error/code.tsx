import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface RadioWithErrorProps {
  label: ReactNode;
  error?: string;
  helperText?: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  name?: string;
  value: string | number | readonly string[];
  id?: string;
  className?: string;
}

/**
 * Radio with an associated validation message. Sets `aria-invalid="true"` and
 * links the error message with `aria-describedby`, so the failure is
 * communicated beyond color. The control border + dot take the destructive
 * token. Built on the native `<input type="radio">`.
 */
export function RadioWithError({
  label,
  error,
  helperText,
  checked,
  defaultChecked,
  onChange,
  disabled,
  required,
  name,
  value,
  id,
  className,
}: RadioWithErrorProps) {
  const generatedId = useId();
  const inputId = id ?? `radio-${generatedId}`;
  const messageId = `${inputId}-msg`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  const hasError = Boolean(error);

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }

  return (
    <div className={cx("flex flex-col gap-1", className)}>
      <label
        htmlFor={inputId}
        className={cx(
          "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
          disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer",
        )}
      >
        <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
            id={inputId}
            type="radio"
            aria-invalid={hasError ? true : undefined}
            aria-describedby={hasError || helperText ? messageId : undefined}
            className={cx(
              "size-[18px] cursor-pointer appearance-none rounded-full border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
              hasError
                ? "border-[var(--ds-color-destructive)]"
                : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)]",
            )}
            checked={isControlled ? isChecked : undefined}
            defaultChecked={isControlled ? undefined : defaultChecked}
            disabled={disabled}
            required={required}
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
                hasError ? "bg-[var(--ds-color-destructive)]" : "bg-[var(--ds-color-primary)]",
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
      {hasError ? (
        <p id={messageId} role="alert" className="pl-[26px] text-xs leading-4 text-[var(--ds-color-destructive)]">
          {error}
        </p>
      ) : helperText ? (
        <p id={messageId} className="pl-[26px] text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}

export default RadioWithError;
