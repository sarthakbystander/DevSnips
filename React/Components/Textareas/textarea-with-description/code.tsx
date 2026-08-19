import type { ReactNode, TextareaHTMLAttributes } from "react";
import { useId } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

export interface TextareaWithDescriptionProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label — required. */
  label: ReactNode;
  /** Supporting description between the label and the control — required. */
  description: ReactNode;
}

/**
 * Textarea with a label and a supporting description stacked above the
 * control. The description is linked to the textarea with
 * `aria-describedby`, so assistive tech reads it as part of the field's
 * description. Use this when the field needs a sentence of context before
 * the user starts typing (what to include, format expectations, audience).
 */
export function TextareaWithDescription({ label, description, id, className, rows = 3, required, ...props }: TextareaWithDescriptionProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const descriptionId = `${textareaId}-description`;

  return (
    <div className="w-full">
      <label
        htmlFor={textareaId}
        className="block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
      >
        {label}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </label>
      <p id={descriptionId} className="mb-2 mt-1 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
        {description}
      </p>
      <textarea
        id={textareaId}
        rows={rows}
        required={required}
        aria-describedby={descriptionId}
        className={cx(TEXTAREA_BASE, TEXTAREA_BORDER, className)}
        {...props}
      />
    </div>
  );
}

export default TextareaWithDescription;
