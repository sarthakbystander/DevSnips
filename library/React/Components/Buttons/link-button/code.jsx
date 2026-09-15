/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const LINK = "inline-flex items-center gap-1.5 rounded-[var(--ds-radius-sm)] border-0 bg-transparent p-0 font-medium leading-none text-[var(--ds-color-link)] underline-offset-4 transition-colors duration-150 ease-out motion-reduce:transition-none hover:text-[var(--ds-color-link-hover)] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50";
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
}) {
  const content = <>
      {iconLeft}
      <span>{children}</span>
      {iconRight}
    </>;
  if (href) {
    return <a
      href={disabled ? undefined : href}
      className={cx(LINK, className)}
      aria-disabled={disabled || undefined}
      onClick={disabled ? (e) => e.preventDefault() : onClick}
      {...rest}
    >
        {content}
      </a>;
  }
  return <button
    type={type}
    className={cx(LINK, className)}
    disabled={disabled}
    onClick={onClick}
    {...rest}
  >
      {content}
    </button>;
}

export default LinkButton;
