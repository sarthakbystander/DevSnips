/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
function Spinner() {
  return <svg className="h-[1em] w-[1em] shrink-0 animate-spin motion-reduce:animate-none" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="3" className="opacity-25" />
      <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>;
}
const SIZES = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5"
};
const VARIANTS = {
  solid: "border-transparent bg-[var(--ds-color-destructive)] text-[var(--ds-color-destructive-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-destructive)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-destructive)_80%,#000)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-destructive)] hover:bg-[var(--ds-color-destructive-soft)] active:bg-[var(--ds-color-destructive-soft)]"
};
export function DestructiveButton({
  children,
  variant = "solid",
  size = "md",
  block = false,
  loading = false,
  disabled,
  iconLeft,
  className,
  type = "button",
  ...rest
}) {
  const isDisabled = disabled || loading;
  return <button
    type={type}
    className={cx(
      "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
      VARIANTS[variant],
      SIZES[size],
      block && "w-full",
      className
    )}
    disabled={isDisabled}
    aria-busy={loading || undefined}
    {...rest}
  >
      {loading ? <Spinner /> : iconLeft}
      <span>{children}</span>
    </button>;
}

export default DestructiveButton;
