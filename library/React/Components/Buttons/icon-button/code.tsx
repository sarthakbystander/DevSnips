import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — IconButton
 * Square icon-only control. `label` is required for an accessible name
 * (rendered as aria-label). Maintains the size token's height; the --icon
 * modifier makes the button square.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type IconButtonVariant = "ghost" | "outline" | "secondary" | "solid";

export interface IconButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Icon node (rendered at the size token for the chosen button size). */
  icon: ReactNode;
  /** Required accessible name (rendered as aria-label). */
  label: string;
  variant?: IconButtonVariant;
  size?: ButtonSize;
  /** Pressed / selected state. Sets aria-pressed. */
  active?: boolean;
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

const VARIANTS: Record<IconButtonVariant, string> = {
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
};

const ICON_ONLY: Record<ButtonSize, string> = {
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
};

export function IconButton({
  icon,
  label,
  variant = "ghost",
  size = "md",
  active = false,
  disabled,
  className,
  type = "button",
  ...rest
}: IconButtonProps) {
  return (
    <button
      type={type}
      aria-label={label}
      aria-pressed={active || undefined}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        active && "bg-[var(--ds-color-surface-active)]",
        ICON_ONLY[size],
        className,
      )}
      disabled={disabled}
      {...rest}
    >
      {icon}
    </button>
  );
}

export default IconButton;
