import type { ReactNode, TextareaHTMLAttributes } from "react";
import { useId } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/**
 * Shared textarea visual language (DevSnips input/textarea tokens):
 * full width, 80px minimum height (~3 rows of body-md), vertical-only
 * resize, radius-sm, 1px color.border, bg color.input, body-md text,
 * muted placeholder, hover/focus surface shift, focus-visible ring from
 * color.focus-ring, muted disabled surface, subtle readonly surface,
 * 150ms color transitions (off under prefers-reduced-motion).
 */
const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label; omit and pass `aria-label` for a bare control. */
  label?: ReactNode;
}

/**
 * The reference textarea. A real native `<textarea>` — form submission,
 * keyboard interaction, selection, copy/paste, `name`/`value`, `required`,
 * `disabled`, `readOnly`, `minLength`/`maxLength` all keep their native
 * behavior. Vertical resize stays enabled (the intentional DevSnips resize
 * behavior); `rows` and `min-h-[80px]` give a sensible default height.
 * Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) usage
 * work natively — no duplicated state.
 */
export function Textarea({ label, id, className, rows = 3, ...props }: TextareaProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;

  const control = (
    <textarea
      id={textareaId}
      rows={rows}
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

export default Textarea;
