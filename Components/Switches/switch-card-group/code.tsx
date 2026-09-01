import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface SwitchCardOption {
  value: string;
  label: ReactNode;
  description?: ReactNode;
  disabled?: boolean;
}

export interface SwitchCardGroupProps {
  legend: ReactNode;
  options: SwitchCardOption[];
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
  columns?: 1 | 2;
  className?: string;
}

/**
 * A group of settings cards inside a `<fieldset>`/`<legend>`, each pairing a
 * label/description with an independently-controlled switch. Maintains a
 * value array of the options that are on; controlled and uncontrolled modes
 * both supported. Each card is a clickable `<label htmlFor>` wrapping a real
 * `<input type="checkbox" role="switch">`.
 */
export function SwitchCardGroup({
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
}: SwitchCardGroupProps) {
  const generatedId = useId();
  const groupId = id ?? `switch-card-group-${generatedId}`;
  const messageId = `${groupId}-msg`;
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState<string[]>(defaultValue);
  const selected = isControlled ? value : internal;

  function handleChange(option: SwitchCardOption, event: ChangeEvent<HTMLInputElement>) {
    const next = event.target.checked
      ? [...selected, option.value]
      : selected.filter((v) => v !== option.value);
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }

  const describedby = error || helperText ? messageId : undefined;
  const gridCols = columns === 2 ? "sm:grid-cols-2" : "grid-cols-1";

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
                "flex w-full items-center gap-3 rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-3.5 text-left transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-within:border-[var(--ds-color-border-strong)] motion-reduce:transition-none",
                isDisabled && "cursor-not-allowed hover:bg-[var(--ds-color-surface)]",
                isOn ? "border-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)]",
                (invalid || error) && "border-[var(--ds-color-destructive)]",
              )}
            >
              <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                <span className="text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">{option.label}</span>
                {option.description ? (
                  <span id={`${groupId}-${option.value}-desc`} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
                    {option.description}
                  </span>
                ) : null}
              </span>
              <span className={cx("relative inline-flex h-[14px] w-[24px] shrink-0 items-center", isDisabled && "opacity-50")}>
                <input
                  id={`${groupId}-${option.value}`}
                  type="checkbox"
                  role="switch"
                  aria-checked={isOn}
                  name={name}
                  value={option.value}
                  checked={isOn}
                  disabled={isDisabled}
                  required={required}
                  aria-invalid={invalid || error ? true : undefined}
                  aria-describedby={option.description ? `${groupId}-${option.value}-desc` : undefined}
                  className={cx(
                    "absolute inset-0 h-full w-full cursor-pointer appearance-none rounded-full border transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none",
                    invalid || error
                      ? (isOn
                        ? "border-[var(--ds-color-destructive)] bg-[var(--ds-color-destructive)]"
                        : "border-[var(--ds-color-destructive)]")
                      : isOn
                        ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]"
                        : "border-[var(--ds-color-border)] bg-[var(--ds-color-input)]",
                  )}
                  onChange={(e) => handleChange(option, e)}
                />
                <span
                  aria-hidden="true"
                  className={cx(
                    "pointer-events-none absolute left-[2px] top-[2px] size-[10px] rounded-full transition-[transform,background-color] duration-150 ease-out motion-reduce:transition-none",
                    isOn ? "translate-x-[10px]" : "translate-x-0",
                    (invalid || error) && isOn
                      ? "bg-[var(--ds-color-destructive-foreground)]"
                      : isOn
                        ? "bg-[var(--ds-color-primary-foreground)]"
                        : "bg-[var(--ds-color-muted-foreground)]",
                  )}
                />
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

export default SwitchCardGroup;
