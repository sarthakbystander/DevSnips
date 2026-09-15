import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface RadioWithIconsProps {
  label: ReactNode;
  icon?: ReactNode;
  /** Optional trailing indicator icon shown when selected. */
  selectedIcon?: ReactNode;
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
 * A radio with an optional leading icon that communicates meaning (e.g. a
 * workspace-type glyph). Icons are ReactNode and must not be purely
 * decorative — omit `icon` when none adds meaning. Built on the native
 * `<input type="radio">`; the icon sits in the clickable label.
 */
export function RadioWithIcons({
  label,
  icon,
  selectedIcon,
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
}: RadioWithIconsProps) {
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
              ? "border-[var(--ds-color-destructive)]"
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
      {icon ? (
        <span
          className={cx(
            "inline-flex size-4 shrink-0 items-center justify-center",
            isChecked ? "text-[var(--ds-color-primary)]" : "text-[var(--ds-color-muted-foreground)]",
          )}
        >
          {icon}
        </span>
      ) : null}
      <span className="select-none">
        {label}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </span>
      {selectedIcon && isChecked ? (
        <span className="ml-auto inline-flex size-4 shrink-0 items-center justify-center text-[var(--ds-color-primary)]" aria-hidden="true">
          {selectedIcon}
        </span>
      ) : null}
    </label>
  );
}

export default RadioWithIcons;
