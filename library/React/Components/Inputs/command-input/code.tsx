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

export interface CommandInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "size"> {
  label?: string;
  commands?: string[];
  size?: InputSize;
  className?: string;
}

export function CommandInput({ label = "Command", commands = ["Open settings", "Invite member", "Create project"], size = "md", id, className, value, defaultValue = "", onChange, ...props }: CommandInputProps) {
  const generatedId = useId(); const inputId = id ?? `input-${generatedId}`; const listboxId = `${inputId}-listbox`;
  const [internalValue, setInternalValue] = useState(String(defaultValue ?? "")); const [open, setOpen] = useState(false); const [activeIndex, setActiveIndex] = useState(0);
  const currentValue = value === undefined ? internalValue : String(value);
  function handleChange(event: ChangeEvent<HTMLInputElement>) { if (value === undefined) setInternalValue(event.target.value); onChange?.(event); setOpen(true); }
  function choose(command: string) { if (value === undefined) setInternalValue(command); setOpen(false); }
  return <div className="w-full"><label htmlFor={inputId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">{label}</label><div className="relative"><input id={inputId} type="search" role="combobox" aria-expanded={open} aria-controls={listboxId} aria-activedescendant={open ? `${inputId}-option-${activeIndex}` : undefined} className={cx(inputClasses(size, "default"), className)} value={currentValue} onFocus={() => setOpen(true)} onChange={handleChange} onKeyDown={(event) => { if (event.key === "Escape") setOpen(false); if (event.key === "ArrowDown") { event.preventDefault(); setOpen(true); setActiveIndex((activeIndex + 1) % commands.length); } if (event.key === "ArrowUp") { event.preventDefault(); setOpen(true); setActiveIndex((activeIndex - 1 + commands.length) % commands.length); } if (event.key === "Enter" && open) { event.preventDefault(); choose(commands[activeIndex]); } }} placeholder="Search commands" {...props} />{open ? <div id={listboxId} role="listbox" className="absolute z-10 mt-2 w-full rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-sm)]">{commands.map((command, index) => <button id={`${inputId}-option-${index}`} role="option" aria-selected={activeIndex === index} key={command} type="button" className={cx("block w-full rounded-[var(--ds-radius-sm)] px-3 py-2 text-left text-sm text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]", activeIndex === index && "bg-[var(--ds-color-surface-selected)]")} onMouseEnter={() => setActiveIndex(index)} onClick={() => choose(command)}>{command}</button>)}</div> : null}</div></div>;
}

export default CommandInput;
