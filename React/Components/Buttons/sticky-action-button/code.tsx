import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — StickyActionButton
 * Persistent primary CTA. Sticks to the bottom of the viewport with a
 * hairline top border + translucent backdrop-blurred surface. Single
 * full-width block action.
 */

export type StickyVariant = "solid" | "destructive" | "success";

export interface StickyActionButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: StickyVariant;
  loading?: boolean;
  iconLeft?: ReactNode;
  iconRight?: ReactNode;
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

const SIZES_LG = "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]";

const VARIANTS: Record<StickyVariant, string> = {
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
  destructive: "border-transparent bg-[var(--ds-color-destructive)] text-[var(--ds-color-destructive-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-destructive)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-destructive)_80%,#000)]",
  success: "border-transparent bg-[var(--ds-color-success)] text-[var(--ds-color-success-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-success)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-success)_80%,#000)]",
};

export function StickyActionButton({
  children,
  variant = "solid",
  loading = false,
  disabled,
  iconLeft,
  iconRight,
  className,
  type = "button",
  ...rest
}: StickyActionButtonProps) {
  const isDisabled = disabled || loading;
  return (
    <div
      className={cx(
        "sticky bottom-0 left-0 right-0 z-20 flex items-center gap-3",
        "border-t border-[var(--ds-color-border)] bg-[color-mix(in_srgb,var(--ds-color-background)_88%,transparent)]",
        "px-0 py-3 backdrop-blur",
        className,
      )}
    >
      <button
        type={type}
        className={cx(
          "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
          VARIANTS[variant],
          SIZES_LG,
          "w-full",
          className,
        )}
        disabled={isDisabled}
        aria-busy={loading || undefined}
        {...rest}
      >
        {loading ? <Spinner /> : iconLeft}
        <span>{children}</span>
        {!loading && iconRight}
      </button>
    </div>
  );
}

export default StickyActionButton;
