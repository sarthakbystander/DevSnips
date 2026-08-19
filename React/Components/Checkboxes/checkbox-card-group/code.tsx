import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface CheckboxCardOption {
  value: string;
  label: ReactNode;
  description?: ReactNode;
  disabled?: boolean;
}

export interface CheckboxCardGroupProps {
  legend: ReactNode;
  options: CheckboxCardOption[];
  value?: string[];
  defaultValue?: string[];
  onChange?: (value: string[], event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  invalid?: boolean;
  error?: string;
  helperText?: ReactNode;
  name?: string;
  id?: string;
  columns?: 1 | 2 | 3;
  className?: string;
}

/**
 * A group of selectable card checkboxes inside a `<fieldset>`/`<legend>`.
 * Maintains a value array of selected option values; controlled and
 * uncontrolled modes both supported. Each card is a clickable `<label>`
 * wrapping a real `<input type="checkbox">`.
 */
export function CheckboxCardGroup({
  legend,
  options,
  value,
  defaultValue = [],
  onChange,
  disabled,
  required,
  invalid,
  error,
  helperText,
  name,
  id,
  columns = 1,
  className,
}: CheckboxCardGroupProps) {
  const generatedId = useId();
  const groupId = id ?? `checkbox-card-group-${generatedId}`;
  const messageId = `${groupId}-msg`;
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState<string[]>(defaultValue);
  const selected = isControlled ? value : internal;

  function handleChange(option: CheckboxCardOption, event: ChangeEvent<HTMLInputElement>) {
    const next = event.target.checked
      ? [...selected, option.value]
      : selected.filter((v) => v !== option.value);
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }

  const describedby = error || helperText ? messageId : undefined;
  const gridCols = columns === 3 ? "sm:grid-cols-3" : columns === 2 ? "sm:grid-cols-2" : "grid-cols-1";

  return (
    <fieldset
      id={groupId}
      className={cx("min-w-0 border-0 p-0", className)}
      aria-invalid={invalid || error ? true : undefined}
      aria-describedby={describedby}
    >
      <legend className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {legend}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </legend>
      <div className={cx("grid gap-2", gridCols)}>
        {options.map((option) => {
          const isOn = selected.includes(option.value);
          const isDisabled = option.disabled || disabled;
          return (
            <label
              key={option.value}
              htmlFor={`${groupId}-${option.value}`}
              className={cx(
                "relative flex w-full items-start gap-3 rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-3.5 text-left transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-within:border-[var(--ds-color-border-strong)] motion-reduce:transition-none",
                isDisabled && "cursor-not-allowed opacity-60 hover:bg-[var(--ds-color-surface)]",
                isOn ? "border-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)]",
                (invalid || error) && "border-[var(--ds-color-destructive)]",
              )}
            >
              <span className="relative mt-0.5 inline-flex size-[18px] shrink-0 items-center justify-center">
                <input
                  id={`${groupId}-${option.value}`}
                  type="checkbox"
                  name={name}
                  value={option.value}
                  checked={isOn}
                  disabled={isDisabled}
                  required={required}
                  aria-invalid={invalid || error ? true : undefined}
                  aria-describedby={option.description ? `${groupId}-${option.value}-desc` : undefined}
                  className={cx(
                    "size-[18px] cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
                    invalid || error
                      ? "border-[var(--ds-color-destructive)] checked:border-[var(--ds-color-destructive)] checked:bg-[var(--ds-color-destructive)]"
                      : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]",
                  )}
                  onChange={(e) => handleChange(option, e)}
                />
                <span
                  aria-hidden="true"
                  className={cx(
                    "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
                    isOn ? "opacity-100" : "opacity-0",
                  )}
                >
                  <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
                    <path d="M20 6 9 17l-5-5" />
                  </svg>
                </span>
              </span>
              <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                <span className="text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">{option.label}</span>
                {option.description ? (
                  <span id={`${groupId}-${option.value}-desc`} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
                    {option.description}
                  </span>
                ) : null}
              </span>
            </label>
          );
        })}
      </div>
      {error ? (
        <p id={messageId} role="alert" className="mt-2 text-xs leading-4 text-[var(--ds-color-destructive)]">
          {error}
        </p>
      ) : helperText ? (
        <p id={messageId} className="mt-2 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p>
      ) : null}
    </fieldset>
  );
}

export default CheckboxCardGroup;
