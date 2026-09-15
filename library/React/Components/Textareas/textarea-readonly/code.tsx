import type { ReactNode, TextareaHTMLAttributes } from "react";
import { useId } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

export interface TextareaReadonlyProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label; omit and pass `aria-label` for a bare control. */
  label?: ReactNode;
}

/**
 * Read-only textarea. Uses the real native `readOnly` attribute (defaulted
 * to `true`): the value cannot be edited but the control stays focusable,
 * its text stays selectable and copyable, and its value IS submitted with
 * the form — unlike `disabled`, which blocks all of that. The readonly
 * treatment (subtle surface, muted text) comes from the native
 * `:read-only` pseudo-class. Use it for values the user may inspect or
 * copy but not change (a generated summary, an audit trail, a locked
 * message draft).
 */
export function TextareaReadonly({ label, id, className, rows = 3, readOnly = true, ...props }: TextareaReadonlyProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;

  const control = (
    <textarea
      id={textareaId}
      rows={rows}
      readOnly={readOnly}
      className={cx(TEXTAREA_BASE, TEXTAREA_BORDER, className)}
      {...props}
    />
  );

  if (label === undefined || label === null) {
    return control;
  }

  return (
    <div className="w-full">
      <label
        htmlFor={textareaId}
        className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
      >
        {label}
      </label>
      {control}
    </div>
  );
}

export default TextareaReadonly;
