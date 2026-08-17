import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — ButtonWithChevron
 * Labeled button with a trailing chevron. `direction` controls orientation;
 * `open` rotates a down chevron 180° to signal an expanded state and sets
 * aria-expanded.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ChevronVariant = "solid" | "outline" | "secondary" | "ghost";
export type ChevronDirection = "down" | "right";

export interface ButtonWithChevronProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  direction?: ChevronDirection;
  /** Expanded state (down chevron rotates 180°; sets aria-expanded). */
  open?: boolean;
  variant?: ChevronVariant;
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

const VARIANTS: Record<ChevronVariant, string> = {
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
};

function ChevronIcon({ direction, open }: { direction: ChevronDirection; open: boolean }) {
  const rotate = direction === "down" && open ? "rotate-180" : "rotate-0";
  return (
    <svg
      className={cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", rotate)}
      viewBox="0 0 24 24" fill="none" aria-hidden="true"
    >
      {direction === "down"
        ? <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        : <path d="m9 6 6 6-6 6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />}
    </svg>
  );
}

export function ButtonWithChevron({
  children,
  direction = "down",
  open = false,
  variant = "outline",
  size = "md",
  disabled,
  className,
  type = "button",
  "aria-expanded": ariaExpanded,
  ...rest
}: ButtonWithChevronProps) {
  return (
    <button
      type={type}
      aria-expanded={ariaExpanded !== undefined ? ariaExpanded : open || undefined}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        SIZES[size],
        className,
      )}
      disabled={disabled}
      {...rest}
    >
      <span>{children}</span>
      <ChevronIcon direction={direction} open={open} />
    </button>
  );
}

export default ButtonWithChevron;
