import type { ButtonHTMLAttributes } from "react";

/* DevSnips React — FilterButton
 * Opens filters + shows active count. activeCount renders a count chip and
 * switches to surface-active. open rotates the leading icon + aria-expanded.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type FilterVariant = "outline" | "secondary" | "ghost";

export interface FilterButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> {
  activeCount?: number;
  open?: boolean;
  label?: string;
  variant?: FilterVariant;
  size?: ButtonSize;
  onToggle?: () => void;
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

const VARIANTS: Record<FilterVariant, string> = {
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
};

export function FilterButton({
  activeCount = 0,
  open = false,
  label = "Filter",
  variant = "outline",
  size = "sm",
  onToggle,
  className,
  type = "button",
  ...rest
}: FilterButtonProps) {
  const hasFilters = activeCount > 0;
  return (
    <button
      type={type}
      aria-expanded={open || undefined}
      aria-label={hasFilters ? `${label}, ${activeCount} active` : label}
      className={cx(
        "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant],
        hasFilters && "bg-[var(--ds-color-surface-active)] font-semibold",
        SIZES[size],
        className,
      )}
      onClick={onToggle}
      {...rest}
    >
      <svg className={cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", open ? "rotate-180" : "rotate-0")} viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <span>{label}</span>
      {hasFilters && (
        <span className="ml-1 inline-flex h-[18px] min-w-[18px] items-center justify-center rounded-full bg-[var(--ds-color-accent)] px-[5px] text-[11px] font-semibold leading-none text-[var(--ds-color-accent-foreground)]" aria-hidden="true">{activeCount}</span>
      )}
    </button>
  );
}

export default FilterButton;
