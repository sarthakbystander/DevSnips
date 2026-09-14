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

export interface InputWithButtonProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "size" | "prefix"> {
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
  buttonLabel?: string;
  onButtonClick?: () => void;
}

export function InputWithButton({ label = "Invite member", buttonLabel = "Send invite", onButtonClick, helperText, size = "md", id, className, ...props }: InputWithButtonProps) {
  const generatedId = useId(); const inputId = id ?? `input-${generatedId}`; const messageId = `${inputId}-message`;
  return <div className="w-full"><label htmlFor={inputId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">{label}</label><div className="flex flex-col gap-2 sm:flex-row"><input id={inputId} type="email" className={cx(inputClasses(size, "default"), className)} aria-describedby={helperText ? messageId : undefined} {...props} /><button type="button" onClick={onButtonClick} className="h-9 shrink-0 rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-3 text-[13px] font-medium text-[var(--ds-color-primary-foreground)] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none">{buttonLabel}</button></div>{helperText ? <p id={messageId} className="mt-2 text-xs text-[var(--ds-color-muted-foreground)]">{helperText}</p> : null}</div>;
}

export default InputWithButton;
