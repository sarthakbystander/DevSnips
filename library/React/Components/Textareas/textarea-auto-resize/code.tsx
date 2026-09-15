import type { ChangeEvent, ReactNode, TextareaHTMLAttributes } from "react";
import { useCallback, useEffect, useId, useRef, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-none overflow-y-auto rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

export interface TextareaAutoResizeProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Visible label; omit and pass `aria-label` for a bare control. */
  label?: ReactNode;
  /** Maximum height in px before the field scrolls instead of growing. */
  maxHeight?: number;
}

/**
 * Auto-resizing textarea. The field grows with its content and shrinks
 * when content is removed, capped at `maxHeight` (default 320px) where it
 * scrolls instead of growing further. Resizing is managed programmatically
 * from the real value — controlled (`value`/`onChange`) and uncontrolled
 * (`defaultValue`) both work, and the initial content is measured on
 * mount. Height changes are instant (no animation), so behavior is
 * identical under prefers-reduced-motion. Manual resize is disabled
 * (`resize-none`) because the component owns the height; without the
 * effect running it still renders as a normal scrollable `rows`-sized
 * textarea.
 */
export function TextareaAutoResize({
  label,
  id,
  className,
  rows = 3,
  maxHeight = 320,
  value,
  defaultValue = "",
  onChange,
  ...props
}: TextareaAutoResizeProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const ref = useRef<HTMLTextAreaElement>(null);
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? ""));
  const currentValue = value === undefined ? internalValue : String(value ?? "");

  const adjust = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    // Reset to natural height first so removed lines collapse the field,
    // then clamp to the cap. Two writes + one read per change, only when
    // the value, cap, or available width actually changes.
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, maxHeight)}px`;
  }, [maxHeight]);

  // Measure on mount (initial value) and after every value change.
  useEffect(() => {
    adjust();
  }, [adjust, currentValue]);

  // Re-measure on viewport resize (width changes reflow wrapped lines) and
  // once the web font settles (a late font load changes the wrapping, so the
  // first measurement can otherwise hold a stale height). Both are single,
  // cleaned-up subscriptions.
  useEffect(() => {
    window.addEventListener("resize", adjust);
    document.fonts.ready.then(adjust).catch(() => {});
    return () => window.removeEventListener("resize", adjust);
  }, [adjust]);

  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    if (value === undefined) setInternalValue(event.target.value);
    onChange?.(event);
  }

  const control = (
    <textarea
      ref={ref}
      id={textareaId}
      rows={rows}
      value={currentValue}
      onChange={handleChange}
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

export default TextareaAutoResize;
