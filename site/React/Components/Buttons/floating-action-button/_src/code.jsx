/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const POS = {
  "bottom-right": "bottom-6 right-6",
  "bottom-left": "bottom-6 left-6",
  "top-right": "top-6 right-6"
};
export function FloatingActionButton({
  icon,
  label,
  position = "bottom-right",
  extended = false,
  disabled,
  className,
  type = "button",
  ...rest
}) {
  return <button
    type={type}
    aria-label={label}
    className={cx(
      "fixed z-40 inline-flex items-center justify-center gap-2 rounded-full",
      "border border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]",
      "shadow-[var(--ds-shadow-md)] transition-transform duration-150 ease-out motion-reduce:transition-none",
      "hover:-translate-y-0.5 active:translate-y-0",
      "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
      "disabled:pointer-events-none disabled:opacity-50",
      extended ? "h-12 px-5 text-sm [&_svg]:size-5" : "size-14 p-0 [&_svg]:size-5",
      POS[position],
      className
    )}
    disabled={disabled}
    {...rest}
  >
      {icon}
      {extended && <span>{label}</span>}
    </button>;
}

export default FloatingActionButton;
