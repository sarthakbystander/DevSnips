import { useState } from "react";
import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — DownloadButton
 * Direct download with progress feedback. Fires onDownload; shows a
 * spinner + "Downloading…" while pending, then a brief done state.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type DownloadVariant = "outline" | "solid" | "secondary";

export interface DownloadButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> {
  meta?: ReactNode;
  href?: string;
  variant?: DownloadVariant;
  size?: ButtonSize;
  onDownload?: () => void | Promise<void>;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

function Spinner() {
  return (
    <svg className="h-[1em] w-[1em] shrink-0 animate-spin motion-reduce:animate-none" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" className="opacity-25" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}

const SIZES: Record<ButtonSize, string> = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5",
};

const VARIANTS: Record<DownloadVariant, string> = {
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
};

export function DownloadButton({
  children = "Download",
  meta,
  href,
  variant = "outline",
  size = "md",
  onDownload,
  className,
  type = "button",
  ...rest
}: DownloadButtonProps) {
  const [state, setState] = useState<"idle" | "working" | "done">("idle");
  async function start(e: React.MouseEvent) {
    if (state !== "idle") return;
    setState("working");
    try { await Promise.resolve(onDownload?.()); }
    finally { setState("done"); setTimeout(() => setState("idle"), 1800); }
  }
  const label = state === "working" ? "Downloading…" : state === "done" ? "Downloaded" : children;
  return (
    <button
      type={type}
      className={cx("inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50", VARIANTS[variant], SIZES[size], className)}
      onClick={start}
      disabled={state === "working"}
      aria-busy={state === "working" || undefined}
      {...rest}
    >
      {state === "working" ? <Spinner /> : (
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          {state === "done"
            ? <path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            : <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><path d="m7 10 5 5 5-5" /><path d="M12 15V3" /></>}
        </svg>
      )}
      <span className="flex flex-col items-start leading-tight">
        <span>{label}</span>
        {meta && <span className="text-[11px] font-normal text-[var(--ds-color-muted-foreground)]">{meta}</span>}
      </span>
    </button>
  );
}

export default DownloadButton;
