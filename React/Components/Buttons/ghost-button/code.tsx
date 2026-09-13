import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — GhostButton
 * Transparent, borderless low-emphasis action. No border, transparent fill;
 * hover lifts to color.surface-hover. `active` applies surface-active +
 * aria-pressed for a selected state.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface GhostButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  size?: ButtonSize;
  /** Pressed / selected appearance. Sets `aria-pressed`. */
  active?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
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

export function GhostButton({
  children,
  size = "md",
  active = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}: GhostButtonProps) {
  return (
    <button
      type={type}
      aria-pressed={active || undefined}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
        active && "bg-[var(--ds-color-surface-active)]",
        SIZES[size],
        className,
      )}
      disabled={disabled}
      {...rest}
    >
      {iconLeft}
      <span>{children}</span>
      {iconRight}
    </button>
  );
}

export default GhostButton;
