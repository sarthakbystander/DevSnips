import type { ButtonHTMLAttributes } from "react";

/* DevSnips React — CloseButton
 * Dismiss control for overlays. Icon-only (X); requires an accessible name
 * (defaults to "Close"). 36px default; 32px in compact headers.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type CloseVariant = "ghost" | "outline";

export interface CloseButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  label?: string;
  variant?: CloseVariant;
  size?: ButtonSize;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const VARIANTS: Record<CloseVariant, string> = {
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
};

const ICON_ONLY: Record<ButtonSize, string> = {
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
};

export function CloseButton({
  label = "Close",
  variant = "ghost",
  size = "md",
  disabled,
  className,
  type = "button",
  ...rest
}: CloseButtonProps) {
  return (
    <button
      type={type}
      aria-label={label}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        ICON_ONLY[size],
        className,
      )}
      disabled={disabled}
      {...rest}
    >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M18 6 6 18" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="m6 6 12 12" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>
  );
}

export default CloseButton;
