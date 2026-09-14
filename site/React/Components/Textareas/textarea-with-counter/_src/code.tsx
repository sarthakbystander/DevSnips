import type { ChangeEvent, ReactNode, TextareaHTMLAttributes } from "react";
import { useId, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

export interface TextareaWithCounterProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label — required. */
  label: ReactNode;
  /** Optional helper text rendered beside the counter. */
  helperText?: ReactNode;
}

/**
 * Textarea with a live character counter. The count is derived from the
 * real value — the controlled `value` when provided, otherwise the
 * uncontrolled text the user has typed — so it always reflects what is
 * actually in the field. When `maxLength` is supplied the counter shows
 * `current / maximum` and the native attribute enforces the limit; at the
 * limit the count gains emphasis (weight + foreground color — no loud
 * colors or animation). When no `maxLength` is supplied the counter shows
 * a plain character count. The counter region is `aria-live` polite and
 * linked with `aria-describedby`.
 */
export function TextareaWithCounter({
  label,
  helperText,
  id,
  className,
  rows = 3,
  value,
  defaultValue = "",
  onChange,
  maxLength,
  ...props
}: TextareaWithCounterProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const countId = `${textareaId}-count`;
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? ""));
  const currentValue = value === undefined ? internalValue : String(value ?? "");
  const atLimit = maxLength !== undefined && currentValue.length >= maxLength;

  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    if (value === undefined) setInternalValue(event.target.value);
    onChange?.(event);
  }

  return (
    <div className="w-full">
      <label
        htmlFor={textareaId}
        className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
      >
        {label}
      </label>
      <textarea
        id={textareaId}
        rows={rows}
        value={currentValue}
        onChange={handleChange}
        maxLength={maxLength}
        aria-describedby={countId}
        className={cx(TEXTAREA_BASE, TEXTAREA_BORDER, className)}
        {...props}
      />
      <div
        id={countId}
        aria-live="polite"
        className="mt-2 flex items-baseline justify-between gap-3 text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
      >
        <span>{helperText}</span>
        <span className={cx("shrink-0", atLimit && "font-medium text-[var(--ds-color-foreground)]")}>
          {currentValue.length}{maxLength !== undefined ? ` / ${maxLength}` : ""}
        </span>
      </div>
    </div>
  );
}

export default TextareaWithCounter;
