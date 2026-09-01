/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useCallback, useId, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const TEXTAREA_BASE = "w-full min-h-[80px] resize-y rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] px-3 py-2 text-sm leading-5 text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none";
const TEXTAREA_BORDER = "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]";
const BUTTON_BASE = "inline-flex h-8 select-none items-center justify-center gap-1.5 whitespace-nowrap rounded-[var(--ds-radius-sm)] border px-3 text-xs font-medium leading-none transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none [&_svg]:size-[14px]";
const BUTTON_GHOST = "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]";
const BUTTON_SECONDARY = "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]";
function useCopy(resetMs) {
  const [copied, setCopied] = useState(false);
  const timer = useRef(null);
  const copy = useCallback(async (text) => {
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
    } catch {
    }
  }, [resetMs]);
  return [copied, copy];
}
export function TextareaWithActions({
  label,
  clearLabel = "Clear",
  copyLabel = "Copy",
  copiedLabel = "Copied",
  resetMs = 2e3,
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
}) {
  const generatedId = useId();
  const textareaId = id ?? `textarea-${generatedId}`;
  const countId = `${textareaId}-count`;
  const statusId = `${textareaId}-status`;
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? ""));
  const currentValue = value === undefined ? internalValue : String(value ?? "");
  const isEmpty = currentValue.length === 0;
  const [copied, copy] = useCopy(resetMs);
  function handleChange(event) {
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
  return <div className="w-full">
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
              {copied ? <path d="M20 6 9 17l-5-5" /> : <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>}
            </svg>
            <span>{copied ? copiedLabel : copyLabel}</span>
          </button>
        </div>
      </div>
      <span id={statusId} role="status" aria-live="polite" className="sr-only">
        {copied ? copiedLabel : ""}
      </span>
    </div>;
}

export default TextareaWithActions;
