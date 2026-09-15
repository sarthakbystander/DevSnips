import type { ButtonHTMLAttributes, AnchorHTMLAttributes, ReactNode } from "react";

/* DevSnips React — LinkButton
 * Button styled as an inline link. color.link text, underline on hover, no
 * border or fill. Renders an <a> when href is set, a <button> otherwise.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

export interface LinkButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "href"> {
  /** Render as an anchor with this URL. */
  href?: string;
  /** Disabled state (button: disabled attr; anchor: aria-disabled). */
  disabled?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const LINK =
  "inline-flex items-center gap-1.5 rounded-[var(--ds-radius-sm)] border-0 bg-transparent " +
  "p-0 font-medium leading-none text-[var(--ds-color-link)] underline-offset-4 " +
  "transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "hover:text-[var(--ds-color-link-hover)] hover:underline " +
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] " +
  "disabled:pointer-events-none disabled:opacity-50";

export function LinkButton({
  children,
  href,
  disabled = false,
  iconLeft,
  iconRight,
  className,
  type = "button",
  onClick,
  ...rest
}: LinkButtonProps) {
  const content = (
    <>
      {iconLeft}
      <span>{children}</span>
      {iconRight}
    </>
  );
  if (href) {
    return (
      <a
        href={disabled ? undefined : href}
        className={cx(LINK, className)}
        aria-disabled={disabled || undefined}
        onClick={disabled ? (e: React.MouseEvent) => e.preventDefault() : onClick}
        {...rest}
      >
        {content}
      </a>
    );
  }
  return (
    <button
      type={type}
      className={cx(LINK, className)}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      {content}
    </button>
  );
}

export default LinkButton;
