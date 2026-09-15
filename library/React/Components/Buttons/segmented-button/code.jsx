/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useRef } from "react";
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
const SEG_BASE = "inline-flex items-center justify-center gap-2 border-0 bg-transparent px-3 font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50";
export function SegmentedButton({
  options,
  value,
  onChange,
  size = "sm",
  label,
  className,
  ...rest
}) {
  const refs = useRef([]);
  const height = SIZES[size];
  function onKey(e, i) {
    const n = options.length;
    let next = -1;
    if (e.key === "ArrowRight" || e.key === "ArrowDown") next = (i + 1) % n;
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = (i - 1 + n) % n;
    if (next >= 0) {
      e.preventDefault();
      const opt = options[next];
      if (!opt.disabled) {
        onChange(opt.value);
        refs.current[next]?.focus();
      }
    }
  }
  return <div role="radiogroup" aria-label={label} className={cx("inline-flex overflow-hidden rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border-strong)]", className)} {...rest}>
      {options.map((opt, i) => {
    const selected = opt.value === value;
    return <button
      key={opt.value}
      ref={(el) => {
        refs.current[i] = el;
      }}
      type="button"
      role="radio"
      aria-checked={selected}
      disabled={opt.disabled}
      onClick={() => onChange(opt.value)}
      onKeyDown={(e) => onKey(e, i)}
      className={cx(
        SEG_BASE,
        height,
        "rounded-none",
        i > 0 && "-ml-px border-l border-[var(--ds-color-border)]",
        selected ? "bg-[var(--ds-color-surface-active)] font-semibold" : "hover:bg-[var(--ds-color-surface-hover)]"
      )}
    >
            {opt.icon ? <Icon name={opt.icon} className="shrink-0" /> : null}
            <span>{opt.label}</span>
          </button>;
  })}
    </div>;
}

export default SegmentedButton;
