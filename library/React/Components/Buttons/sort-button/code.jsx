/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

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
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]"
};
export function SortButton({
  field = "Created",
  direction = "desc",
  variant = "outline",
  size = "sm",
  onToggle,
  className,
  type = "button",
  ...rest
}) {
  const active = direction !== null;
  const dirLabel = direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "unsorted";
  return <button
    type={type}
    aria-label={`Sort by ${field}, currently ${dirLabel}`}
    className={cx(
      "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
      VARIANTS[variant],
      active && "bg-[var(--ds-color-surface-active)] font-semibold",
      SIZES[size],
      className
    )}
    onClick={onToggle}
    {...rest}
  >
      <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M11 5h10" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="M11 9h7" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="M11 13h4" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
        <path d="m3 17 3 3 3-3" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M6 18V4" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
      </svg>
      <span>{field}</span>
      <svg
    className={cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", direction === "asc" ? "rotate-180" : "rotate-0", !active && "opacity-50")}
    viewBox="0 0 24 24"
    fill="none"
    aria-hidden="true"
  >
        <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </button>;
}

export default SortButton;
