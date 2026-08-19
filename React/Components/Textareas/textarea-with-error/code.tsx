import type { ReactNode, TextareaHTMLAttributes } from "react";
import { useId } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

export interface TextareaWithErrorProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label — required. */
  label: ReactNode;
  /** Error message. When set, the field enters the error state. */
  error?: string;
}

/**
 * Textarea with an inline error state. Passing `error` switches the border
 * to color.destructive, sets `aria-invalid="true"`, and renders the message
 * in a `role="alert"` region linked with `aria-describedby` — the state is
 * never communicated by color alone. Clear `error` (set it back to
 * `undefined`) once the value is valid again.
 */
export function TextareaWithError({ label, error, id, className, rows = 3, required, ...props }: TextareaWithErrorProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const errorId = `${textareaId}-error`;
  const hasError = Boolean(error);

  return (
    <div className="w-full">
      <label
        htmlFor={textareaId}
        className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
      >
        {label}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </label>
      <textarea
        id={textareaId}
        rows={rows}
        required={required}
        aria-invalid={hasError ? true : undefined}
        aria-describedby={hasError ? errorId : undefined}
        className={cx(
          TEXTAREA_BASE,
          hasError
            ? "border-[var(--ds-color-destructive)]"
            : "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]",
          className,
        )}
        {...props}
      />
      {hasError ? (
        <p id={errorId} role="alert" className="mt-2 text-xs leading-4 text-[var(--ds-color-destructive)]">
          Error: {error}
        </p>
      ) : null}
    </div>
  );
}

export default TextareaWithError;
