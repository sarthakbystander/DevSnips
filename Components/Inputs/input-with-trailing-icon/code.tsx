import type { ChangeEvent, InputHTMLAttributes, ReactNode } from "react";
import { useId, useState } from "react";

export type InputSize = "sm" | "md" | "lg";
export type InputTone = "default" | "error" | "success";

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const INPUT_SIZES: Record<InputSize, string> = {
  sm: "h-8 px-2.5 text-[13px]",
  md: "h-9 px-3 text-sm",
  lg: "h-11 px-3.5 text-sm",
};

const ICON_SIZES: Record<InputSize, string> = {
  sm: "[&_svg]:size-[14px]",
  md: "[&_svg]:size-4",
  lg: "[&_svg]:size-[18px]",
};

function inputClasses(size: InputSize, tone: InputTone, hasLeading = false, hasTrailing = false): string {
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

export interface InputWithTrailingIconProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "size" | "prefix"> {
  label?: string;
  helperText?: string;
  error?: string;
  success?: string;
  size?: InputSize;
  tone?: InputTone;
  leadingIcon?: ReactNode;
  trailingIcon?: ReactNode;
  prefix?: ReactNode;
  suffix?: ReactNode;
}

export function InputWithTrailingIcon({
  label = "Input with Trailing Icon",
  helperText,
  error,
  success,
  size = "md",
  tone = "default",
  leadingIcon,
  trailingIcon,
  prefix,
  suffix,
  id,
  className,
  type = "text",
  disabled,
  readOnly,
  ...props
}: InputWithTrailingIconProps) {
  const generatedId = useId();
  const inputId = id ?? `input-${generatedId}`;
  const messageId = `${inputId}-message`;
  const message = error ?? success ?? helperText;
  const resolvedTone: InputTone = error ? "error" : success ? "success" : tone;
  const hasLeading = Boolean(leadingIcon ?? prefix);
  const hasTrailing = Boolean(trailingIcon ?? suffix);

  return (
    <div className="w-full">
      <label htmlFor={inputId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      <div className="relative flex items-center">
        {hasLeading ? (
          <span className={cx("pointer-events-none absolute left-3 text-[var(--ds-color-muted-foreground)]", ICON_SIZES[size])}>
            {prefix ?? leadingIcon}
          </span>
        ) : null}
        <input
          id={inputId}
          type={type}
          className={cx(inputClasses(size, resolvedTone, hasLeading, hasTrailing), className)}
          disabled={disabled}
          readOnly={readOnly}
          aria-invalid={error ? true : undefined}
          aria-describedby={message ? messageId : undefined}
          {...props}
        />
        {hasTrailing ? (
          <span className={cx("pointer-events-none absolute right-3 text-[var(--ds-color-muted-foreground)]", ICON_SIZES[size])}>
            {suffix ?? trailingIcon}
          </span>
        ) : null}
      </div>
      {message ? (
        <p id={messageId} className={cx("mt-2 text-xs", error ? "text-[var(--ds-color-destructive)]" : success ? "text-[var(--ds-color-success)]" : "text-[var(--ds-color-muted-foreground)]")}>
          {error ? `Error: ${error}` : success ? `Success: ${success}` : helperText}
        </p>
      ) : null}
    </div>
  );
}

export default InputWithTrailingIcon;
