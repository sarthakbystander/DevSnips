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
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]"
};
const BASE_BTN = "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50";
export function ButtonGroup({
  items,
  children,
  variant = "outline",
  size = "md",
  label,
  className,
  ...rest
}) {
  return <div role="group" aria-label={label} className={cx("inline-flex", className)} {...rest}>
      {items ? items.map((it, i) => <button
    key={it.id ?? i}
    type="button"
    aria-pressed={it.active || undefined}
    onClick={it.onClick}
    className={cx(
      BASE_BTN,
      VARIANTS[variant],
      SIZES[size],
      "rounded-none border-r-0",
      i === 0 ? "rounded-l-[var(--ds-radius-sm)]" : "-ml-px",
      i === items.length - 1 && "rounded-r-[var(--ds-radius-sm)] border-r",
      it.active && "bg-[var(--ds-color-surface-active)]"
    )}
  >
              {it.icon ? <Icon name={it.icon} className="shrink-0" /> : null}
              <span>{it.label}</span>
            </button>) : children}
    </div>;
}

export default ButtonGroup;
