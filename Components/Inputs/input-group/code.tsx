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

export interface InputGroupProps {
  legend?: string;
  className?: string;
}

export function InputGroup({ legend = "Contact details", className }: InputGroupProps) {
  const firstId = useId(); const lastId = useId(); const emailId = useId();
  return <fieldset className={cx("w-full rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4", className)}><legend className="px-1 text-[13px] font-medium text-[var(--ds-color-foreground)]">{legend}</legend><div className="grid gap-3 sm:grid-cols-2"><label className="block"><span className="mb-2 block text-[13px] font-medium text-[var(--ds-color-foreground)]">First name</span><input id={firstId} className={inputClasses("md", "default")} placeholder="Maya" /></label><label className="block"><span className="mb-2 block text-[13px] font-medium text-[var(--ds-color-foreground)]">Last name</span><input id={lastId} className={inputClasses("md", "default")} placeholder="Chen" /></label><label className="block sm:col-span-2"><span className="mb-2 block text-[13px] font-medium text-[var(--ds-color-foreground)]">Billing email</span><input id={emailId} type="email" className={inputClasses("md", "default")} placeholder="billing@example.com" /></label></div></fieldset>;
}

export default InputGroup;
