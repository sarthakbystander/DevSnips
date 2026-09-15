import type { ChangeEvent, ReactNode, TextareaHTMLAttributes } from "react";
import { useCallback, useId, useRef, useState } from "react";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TEXTAREA_BASE =
  "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";

const TEXTAREA_BORDER =
  "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";

const BUTTON_BASE =
  "inline-flex h-8 select-none items-center justify-center gap-1.5 whitespace-nowrap rounded-[var(--ds-radius-sm)] border px-3 text-xs font-medium leading-none transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none [&_svg]:size-[14px]";

const BUTTON_GHOST =
  "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]";

const BUTTON_SECONDARY =
  "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]";

function useCopy(resetMs: number): readonly [boolean, (text: string) => Promise<void>] {
  const [copied, setCopied] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const copy = useCallback(async (text: string) => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
      }
      setCopied(true);
      if (timer.current) clearTimeout(timer.current);
      timer.current = setTimeout(() => setCopied(false), resetMs);
    } catch { /* clipboard unavailable */ }
  }, [resetMs]);
  return [copied, copy] as const;
}

export interface TextareaWithActionsProps extends Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "onCopy"> {
  /** Visible label — required. */
  label: ReactNode;
  /** Accessible label for the clear action. */
  clearLabel?: string;
  /** Label for the copy action. */
  copyLabel?: string;
  /** Label shown after a successful copy. */
  copiedLabel?: string;
  /** Reset delay (ms) before the copy label returns to normal. */
  resetMs?: number;
  /** Called after the clear action runs. */
  onClear?: () => void;
  /** Called after the copy action runs. */
  onCopy?: (value: string) => void;
}

/**
 * Textarea with a contextual action bar: a live character count plus real
 * Clear and Copy buttons. Clear empties the field (and returns focus to
 * it); Copy writes the current value to the clipboard and confirms with a
 * label swap + an `aria-live` status message. Both actions derive from the
 * real value (controlled or uncontrolled), are disabled when the field is
 * empty, use the DevSnips ghost/secondary button styles, and work fully
 * from the keyboard. The action row wraps on narrow screens.
 */
export function TextareaWithActions({
  label,
  clearLabel = "Clear",
  copyLabel = "Copy",
  copiedLabel = "Copied",
  resetMs = 2000,
  onClear,
  onCopy,
  id,
  className,
  rows = 3,
  value,
  defaultValue = "",
  onChange,
  maxLength,
  ...props
}: TextareaWithActionsProps) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const countId = `${textareaId}-count`;
  const statusId = `${textareaId}-status`;
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? ""));
  const currentValue = value === undefined ? internalValue : String(value ?? "");
  const isEmpty = currentValue.length === 0;
  const [copied, copy] = useCopy(resetMs);

  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    if (value === undefined) setInternalValue(event.target.value);
    onChange?.(event);
  }

  function handleClear() {
    if (value === undefined) setInternalValue("");
    onClear?.();
    document.getElementById(textareaId)?.focus();
  }

  async function handleCopy() {
    await copy(currentValue);
    onCopy?.(currentValue);
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
      <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
        <span
          id={countId}
          aria-live="polite"
          className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]"
        >
          {currentValue.length}{maxLength !== undefined ? ` / ${maxLength}` : " characters"}
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            aria-label={clearLabel}
            onClick={handleClear}
            disabled={isEmpty}
            className={cx(BUTTON_BASE, BUTTON_GHOST)}
          >
            {clearLabel}
          </button>
          <button
            type="button"
            aria-describedby={statusId}
            onClick={handleCopy}
            disabled={isEmpty}
            className={cx(BUTTON_BASE, BUTTON_SECONDARY)}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
              {copied
                ? <path d="M20 6 9 17l-5-5" />
                : <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>}
            </svg>
            <span>{copied ? copiedLabel : copyLabel}</span>
          </button>
        </div>
      </div>
      <span id={statusId} role="status" aria-live="polite" className="sr-only">
        {copied ? copiedLabel : ""}
      </span>
    </div>
  );
}

export default TextareaWithActions;
