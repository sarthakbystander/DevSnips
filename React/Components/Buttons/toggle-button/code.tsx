import { useState } from "react";
import type { ButtonHTMLAttributes } from "react";

/* DevSnips React — ToggleButton
 * Single binary switch. Controlled (pressed) or uncontrolled
 * (defaultPressed). Exposes aria-pressed and swaps to surface-active when on.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ToggleVariant = "ghost" | "outline" | "secondary";

export interface ToggleButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "value"> {
  pressed?: boolean;
  defaultPressed?: boolean;
  onToggle?: (pressed: boolean) => void;
  label: string;
  iconOff?: string;
  iconOn?: string;
  variant?: ToggleVariant;
  size?: ButtonSize;
  showLabel?: boolean;
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

const VARIANTS: Record<ToggleVariant, string> = {
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
};

const ICON_ONLY: Record<ButtonSize, string> = {
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
};

function Icon({ name, className }: { name?: string; className?: string }) {
  if (!name) return null;
  const common = { width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" } as const;
  const paths: Record<string, React.ReactNode> = {
    "pin": <path d="M12 17v5" />,
    "bell": <><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></>,
    "star": <path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />,
    "bookmark": <path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z" />,
  };
  return <svg {...common}>{paths[name]}</svg>;
}

export function ToggleButton({
  pressed: pressedProp,
  defaultPressed = false,
  onToggle,
  label,
  iconOff,
  iconOn,
  variant = "ghost",
  size = "md",
  showLabel = true,
  disabled,
  className,
  type = "button",
  ...rest
}: ToggleButtonProps) {
  const [internal, setInternal] = useState(defaultPressed);
  const isControlled = pressedProp !== undefined;
  const value = isControlled ? pressedProp : internal;
  function click() {
    const next = !value;
    if (!isControlled) setInternal(next);
    onToggle?.(next);
  }
  return (
    <button
      type={type}
      aria-pressed={value}
      aria-label={showLabel ? undefined : label}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        value && "bg-[var(--ds-color-surface-active)] font-semibold",
        showLabel ? SIZES[size] : ICON_ONLY[size],
        className,
      )}
      disabled={disabled}
      onClick={click}
      {...rest}
    >
      <Icon name={value ? (iconOn ?? iconOff) : iconOff} className="shrink-0" />
      {showLabel && <span>{label}</span>}
    </button>
  );
}

export default ToggleButton;
