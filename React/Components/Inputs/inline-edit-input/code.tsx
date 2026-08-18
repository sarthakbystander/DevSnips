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

export interface InlineEditInputProps {
  label?: string;
  initialValue?: string;
  onSave?: (value: string) => void;
  className?: string;
}

export function InlineEditInput({ label = "Project name", initialValue = "DevSnips web", onSave, className }: InlineEditInputProps) {
  const [value, setValue] = useState(initialValue); const [draft, setDraft] = useState(initialValue); const [editing, setEditing] = useState(false);
  function save() { setValue(draft); setEditing(false); onSave?.(draft); }
  function cancel() { setDraft(value); setEditing(false); }
  if (!editing) return <div className={cx("flex w-full items-center gap-2", className)}><span className="min-h-9 flex-1 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-3 py-2 text-sm text-[var(--ds-color-foreground)]">{value}</span><button type="button" onClick={() => setEditing(true)} className="h-9 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] px-3 text-[13px] font-medium text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]">Edit</button></div>;
  return <div className={cx("flex w-full flex-col gap-2 sm:flex-row", className)}><label className="sr-only" htmlFor="inline-edit-input">{label}</label><input id="inline-edit-input" className={inputClasses("md", "default")} value={draft} onChange={(event) => setDraft(event.target.value)} onKeyDown={(event) => { if (event.key === "Escape") cancel(); if (event.key === "Enter") save(); }} autoFocus /><button type="button" onClick={save} className="h-9 rounded-[var(--ds-radius-sm)] bg-[var(--ds-color-primary)] px-3 text-[13px] font-medium text-[var(--ds-color-primary-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]">Save</button><button type="button" onClick={cancel} className="h-9 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] px-3 text-[13px] font-medium text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]">Cancel</button></div>;
}

export default InlineEditInput;
