import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — ButtonWithIcon
 * Labeled button with a leading/trailing icon. Icons use the shared size
 * token for the chosen button size; the 8px control gap keeps icon and
 * label optically aligned.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type WithIconVariant = "solid" | "outline" | "secondary" | "ghost";
export type IconPosition = "leading" | "trailing";

export interface ButtonWithIconProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Icon name (rendered by the inline Icon helper). */
  icon?: string;
  iconPosition?: IconPosition;
  variant?: WithIconVariant;
  size?: ButtonSize;
  /** Override the leading slot with a custom icon node. */
  iconLeft?: ReactNode;
  /** Override the trailing slot with a custom icon node. */
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

const VARIANTS: Record<WithIconVariant, string> = {
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
};

function Icon({ name, className }: { name?: string; className?: string }) {
  if (!name) return null;
  // Minimal stroke icon set used by the preview. In a real project, import
  // your icon library here; the component only needs an SVG node.
  const common = { width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" } as const;
  const paths: Record<string, ReactNode> = {
    "download": <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
    "arrow-right": <><path d="M5 12h14" /><path d="m13 5 7 7-7 7" /></>,
    "plus": <><path d="M12 5v14" /><path d="M5 12h14" /></>,
    "save": <><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" /><path d="M17 21v-8H7v8" /><path d="M7 3v5h8" /></>,
  };
  return <svg {...common}>{paths[name]}</svg>;
}

export function ButtonWithIcon({
  children,
  icon,
  iconPosition = "leading",
  variant = "solid",
  size = "md",
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}: ButtonWithIconProps) {
  const leading = iconPosition === "leading" ? (iconLeft ?? (icon ? <Icon name={icon} className="shrink-0" /> : null)) : iconLeft;
  const trailing = iconPosition === "trailing" ? (iconRight ?? (icon ? <Icon name={icon} className="shrink-0" /> : null)) : iconRight;
  return (
    <button
      type={type}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        SIZES[size],
        className,
      )}
      disabled={disabled}
      {...rest}
    >
      {leading}
      <span>{children}</span>
      {trailing}
    </button>
  );
}

export default ButtonWithIcon;
