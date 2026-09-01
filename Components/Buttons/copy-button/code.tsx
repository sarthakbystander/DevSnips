import { useCallback, useRef, useState } from "react";
import type { ButtonHTMLAttributes } from "react";

/* DevSnips React — CopyButton
 * Clipboard copy with transient feedback. Async Clipboard API + execCommand
 * fallback. aria-live announces the copied state; icon + label confirm
 * success without relying on color alone.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type CopyVariant = "outline" | "secondary" | "ghost" | "solid";

export interface CopyButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {
  value: string;
  label?: string;
  copiedLabel?: string;
  resetMs?: number;
  onCopy?: (value: string) => void;
  variant?: CopyVariant;
  size?: ButtonSize;
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

const VARIANTS: Record<CopyVariant, string> = {
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
};

function useCopy(resetMs: number) {
  const [copied, setCopied] = useState(false);
  const t = useRef<ReturnType<typeof setTimeout> | null>(null);
  const copy = useCallback(async (text: string) => {
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); }
      else {
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
      if (t.current) clearTimeout(t.current);
      t.current = setTimeout(() => setCopied(false), resetMs);
    } catch { /* clipboard unavailable */ }
  }, [resetMs]);
  return [copied, copy] as const;
}

export function CopyButton({
  value,
  label = "Copy",
  copiedLabel = "Copied",
  resetMs = 2000,
  onCopy,
  variant = "outline",
  size = "sm",
  className,
  type = "button",
  ...rest
}: CopyButtonProps) {
  const [copied, copy] = useCopy(resetMs);
  async function handle() { await copy(value); onCopy?.(value); }
  return (
    <button
      type={type}
      className={cx("inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50", VARIANTS[variant], SIZES[size], className)}
      onClick={handle}
      aria-label={`${copied ? copiedLabel : label}: ${value}`}
      {...rest}
    >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        {copied
          ? <path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          : <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>}
      </svg>
      <span>{copied ? copiedLabel : label}</span>
      <span className="sr-only" role="status" aria-live="polite">{copied ? copiedLabel : ""}</span>
    </button>
  );
}

export default CopyButton;
