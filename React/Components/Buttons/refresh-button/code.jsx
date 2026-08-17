/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5"
};
const VARIANTS = {
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]"
};
const ICON_ONLY = {
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5"
};
export function RefreshButton({
  onRefresh,
  label = "Refresh",
  showLabel = false,
  variant = "ghost",
  size = "sm",
  className,
  type = "button",
  ...rest
}) {
  const [loading, setLoading] = useState(false);
  async function run() {
    if (loading) return;
    setLoading(true);
    try {
      await Promise.resolve(onRefresh?.());
    } finally {
      setLoading(false);
    }
  }
  return <button
    type={type}
    aria-label={showLabel ? undefined : label}
    className={cx(
      "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
      VARIANTS[variant],
      showLabel ? SIZES[size] : ICON_ONLY[size],
      className
    )}
    onClick={run}
    disabled={loading}
    aria-busy={loading || undefined}
    {...rest}
  >
      <svg className={cx("h-[1em] w-[1em] shrink-0", loading && "animate-spin motion-reduce:animate-none")} viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M3 12a9 9 0 0 1 15-6.7L21 8" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M21 3v5h-5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M21 12a9 9 0 0 1-15 6.7L3 16" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M3 21v-5h5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {showLabel && <span>{loading ? "Refreshing\u2026" : label}</span>}
    </button>;
}

export default RefreshButton;
