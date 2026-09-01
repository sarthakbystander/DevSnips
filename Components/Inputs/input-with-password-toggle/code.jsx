/* DevSnips React — JavaScript parity build. Same API and behavior as code.tsx; TypeScript types removed. */
import { useId, useState } from "react";

function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}

const INPUT_SIZES = {
  sm: "h-8 px-2.5 text-[13px]",
  md: "h-9 px-3 text-sm",
  lg: "h-11 px-3.5 text-sm",
};

const ICON_SIZES = {
  sm: "[&_svg]:size-[14px]",
  md: "[&_svg]:size-4",
  lg: "[&_svg]:size-[18px]",
};

function inputClasses(size, tone, hasLeading = false, hasTrailing = false) {
  return cx(
    "w-full rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] text-[var(--ds-color-foreground)] shadow-none transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 read-only:bg-[var(--ds-color-surface-subtle)] read-only:text-[var(--ds-color-muted-foreground)] motion-reduce:transition-none",
    tone === "error" ? "border-[var(--ds-color-destructive)]" : tone === "success" ? "border-[var(--ds-color-success)]" : "border-[var(--ds-color-border)] focus:border-[var(--ds-color-border-strong)]",
    INPUT_SIZES[size],
    hasLeading && "pl-9",
    hasTrailing && "pr-9",
  );
}

function Spinner() {
  return (
    <svg className="size-4 animate-spin motion-reduce:animate-none" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" className="opacity-25" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}

export function InputWithPasswordToggle({ label = "Password", helperText, error, success, size = "md", tone = "default", id, className, disabled, readOnly, autoComplete = "current-password", ...props }) {
  const generatedId = useId();
  const inputId = id ?? `input-${generatedId}`;
  const messageId = `${inputId}-message`;
  const [visible, setVisible] = useState(false);
  const message = error ?? success ?? helperText;
  const resolvedTone = error ? "error" : success ? "success" : tone;

  return (
    <div className="w-full">
      <label htmlFor={inputId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">{label}</label>
      <div className="relative flex items-center">
        <input id={inputId} type={visible ? "text" : "password"} autoComplete={autoComplete} className={cx(inputClasses(size, resolvedTone, false, true), className)} disabled={disabled} readOnly={readOnly} aria-invalid={error ? true : undefined} aria-describedby={message ? messageId : undefined} {...props} />
        <button type="button" aria-label={visible ? "Hide password" : "Show password"} aria-pressed={visible} onClick={() => setVisible((current) => !current)} className="absolute right-2 h-6 rounded-[var(--ds-radius-xs)] px-2 text-[12px] font-medium text-[var(--ds-color-muted-foreground)] transition-colors hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none">{visible ? "Hide" : "Show"}</button>
      </div>
      {message ? <p id={messageId} className={cx("mt-2 text-xs", error ? "text-[var(--ds-color-destructive)]" : success ? "text-[var(--ds-color-success)]" : "text-[var(--ds-color-muted-foreground)]")}>{error ? `Error: ${error}` : success ? `Success: ${success}` : helperText}</p> : null}
    </div>
  );
}

export default InputWithPasswordToggle;
