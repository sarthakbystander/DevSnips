import type { ChangeEvent, ReactNode } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export interface RadioProps {
  /** Accessible label when no visible label is rendered. */
  label?: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  invalid?: boolean;
  name?: string;
  value: string | number | readonly string[];
  id?: string;
  "aria-label"?: string;
  "aria-labelledby"?: string;
  "aria-describedby"?: string;
  className?: string;
  children?: ReactNode;
}

/**
 * Native radio styled to the DevSnips select/input visual language. The real
 * `<input type="radio">` carries all native behavior; a sibling dot renders
 * the selected indicator through the tracked `isChecked` state. Controlled
 * (`checked`/`onChange`) and uncontrolled (`defaultChecked`) modes are both
 * supported.
 */
export function Radio({
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
  "aria-label": ariaLabel,
  "aria-labelledby": ariaLabelledby,
  "aria-describedby": ariaDescribedby,
  className,
  children,
}: RadioProps) {
  const generatedId = useId();
  const inputId = id ?? `radio-${generatedId}`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }

  const control = (
    <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
      <input
        id={inputId}
        type="radio"
        className={cx(
          "size-[18px] cursor-pointer appearance-none rounded-full border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
          invalid
            ? "border-[var(--ds-color-destructive)] checked:border-[var(--ds-color-destructive)]"
            : "border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)]",
          className,
        )}
        checked={isControlled ? isChecked : undefined}
        defaultChecked={isControlled ? undefined : defaultChecked}
        disabled={disabled}
        required={required}
        aria-invalid={invalid ? true : undefined}
        aria-label={ariaLabel}
        aria-labelledby={ariaLabelledby}
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
  );

  if (!label && !children) {
    return control;
  }

  const labelContent = children ?? label;
  return (
    <label
      htmlFor={inputId}
      className={cx(
        "inline-flex items-center gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
        disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer",
      )}
    >
      {control}
      {labelContent ? <span className="select-none">{labelContent}</span> : null}
    </label>
  );
}

export default Radio;
