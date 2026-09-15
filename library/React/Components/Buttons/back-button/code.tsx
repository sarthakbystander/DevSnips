import type { ButtonHTMLAttributes, AnchorHTMLAttributes, ReactNode } from "react";

/* DevSnips React — BackButton
 * Returns to the previous view. Leading arrow-left + label. Renders a
 * button (onClick) or a link (href). Icon-only mode needs a label for an
 * accessible name.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type BackVariant = "ghost" | "outline";

export interface BackButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "href"> {
  href?: string;
  variant?: BackVariant;
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

const VARIANTS: Record<BackVariant, string> = {
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

function ArrowLeft() {
  return (
    <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M19 12H5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      <path d="m11 19-7-7 7-7" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function BackButton({
  children = "Back",
  href,
  variant = "ghost",
  size = "md",
  showLabel = true,
  className,
  type = "button",
  onClick,
  ...rest
}: BackButtonProps) {
  const cls = cx(
    "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
    VARIANTS[variant],
    showLabel ? SIZES[size] : ICON_ONLY[size],
    className,
  );
  const content = (
    <>
      <ArrowLeft />
      {showLabel && <span>{children}</span>}
    </>
  );
  if (href) {
    return <a href={href} className={cls} {...rest}>{content}</a>;
  }
  return (
    <button
      type={type}
      className={cls}
      aria-label={showLabel ? undefined : (typeof children === "string" ? children : "Back")}
      onClick={onClick}
      {...rest}
    >
      {content}
    </button>
  );
}

export default BackButton;
