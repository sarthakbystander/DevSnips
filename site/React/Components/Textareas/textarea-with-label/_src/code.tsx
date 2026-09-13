import type { ReactNode, TextareaHTMLAttributes } from "react";
import { useId } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

export interface TextareaWithLabelProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label — required; clicking it focuses the textarea. */
  label: ReactNode;
}

/**
 * Textarea with a properly associated visible label. The label uses
 * `<label htmlFor>` pointing at the textarea's `id`, so clicking the label
 * activates the control. Renders a `*` indicator when `required` (the
 * native `required` attribute still carries the semantics — the asterisk
 * is decorative and hidden from assistive tech).
 */
export function TextareaWithLabel({ label, id, className, rows = 3, required, ...props }: TextareaWithLabelProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;

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
        className={cx(TEXTAREA_BASE, TEXTAREA_BORDER, className)}
        {...props}
      />
    </div>
  );
}

export default TextareaWithLabel;
