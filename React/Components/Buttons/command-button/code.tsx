import { useEffect } from "react";
import type { ButtonHTMLAttributes } from "react";

/* DevSnips React — CommandButton
 * Opens a command palette. Wide trigger + search icon + placeholder + kbd
 * hint. bindShortcut listens for Cmd/Ctrl+K to call onOpen.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type CommandVariant = "outline" | "secondary";

export interface CommandButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {
  placeholder?: string;
  shortcut?: string;
  onOpen?: () => void;
  variant?: CommandVariant;
  size?: ButtonSize;
  bindShortcut?: boolean;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const SIZES: Record<ButtonSize, string> = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5",
};

const VARIANTS: Record<CommandVariant, string> = {
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
};

const KBD =
  "inline-flex items-center rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] " +
  "bg-[var(--ds-color-surface-subtle)] px-1.5 py-0.5 font-mono text-[11px] leading-none " +
  "text-[var(--ds-color-muted-foreground)]";

export function CommandButton({
  placeholder = "Search or run a command…",
  shortcut = "⌘K",
  onOpen,
  variant = "outline",
  size = "md",
  bindShortcut = true,
  className,
  type = "button",
  ...rest
}: CommandButtonProps) {
  useEffect(() => {
    if (!bindShortcut) return;
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        onOpen?.();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [bindShortcut, onOpen]);

  return (
    <button
      type={type}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        SIZES[size],
        "w-full max-w-[420px] justify-between text-[var(--ds-color-muted-foreground)]",
        className,
      )}
      onClick={onOpen}
      {...rest}
    >
      <span className="inline-flex items-center gap-2">
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="1.75" />
          <path d="m21 21-4.3-4.3" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <span>{placeholder}</span>
      </span>
      <kbd className={KBD} aria-hidden="true">{shortcut}</kbd>
    </button>
  );
}

export default CommandButton;
