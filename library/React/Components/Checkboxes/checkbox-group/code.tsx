import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface CheckboxGroupOption {
  value: string;
  label: ReactNode;
  disabled?: boolean;
  description?: ReactNode;
}

export interface CheckboxGroupProps {
  legend: ReactNode;
  options: CheckboxGroupOption[];
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
  orientation?: "vertical" | "horizontal";
  className?: string;
}

/**
 * A group of related checkboxes inside a `<fieldset>`/`<legend>`. Maintains a
 * value array of selected option values. Controlled (`value`/`onChange`) and
 * uncontrolled (`defaultValue`) modes are both supported. Built on native
 * `<input type="checkbox">` elements sharing a `name`.
 */
export function CheckboxGroup({
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
  orientation = "vertical",
  className,
}: CheckboxGroupProps) {
  const generatedId = useId();
  const groupId = id ?? `checkbox-group-${generatedId}`;
  const messageId = `${groupId}-msg`;
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState<string[]>(defaultValue);
  const selected = isControlled ? value : internal;

  function handleChange(option: CheckboxGroupOption, event: ChangeEvent<HTMLInputElement>) {
    const next = event.target.checked
      ? [...selected, option.value]
      : selected.filter((v) => v !== option.value);
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }

  const describedby = error || helperText ? messageId : undefined;

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
      <div className={cx("flex gap-2", orientation === "vertical" ? "flex-col" : "flex-wrap")}>
        {options.map((option) => {
          const isOn = selected.includes(option.value);
          return (
            <label
              key={option.value}
              htmlFor={`${groupId}-${option.value}`}
              className={cx(
                "inline-flex items-start gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
                option.disabled || disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer",
                orientation === "horizontal" ? "mr-2" : "",
              )}
            >
              <span className="relative mt-[3px] inline-flex size-[18px] shrink-0 items-center justify-center">
                <input
                  id={`${groupId}-${option.value}`}
                  type="checkbox"
                  name={name}
                  value={option.value}
                  checked={isOn}
                  disabled={option.disabled || disabled}
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
              <span className="flex flex-col gap-0.5">
                <span className="select-none font-medium">{option.label}</span>
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

export default CheckboxGroup;
