import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

const VARIANTS = { solid:"ds-btn--solid", outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost" };

/**
 * ButtonWithChevron — labeled button with a trailing chevron.
 *
 * `direction` controls orientation: "down" (default) for menus/disclosure,
 * "right" for advancing/next. `open` rotates a "down" chevron 180° to
 * signal an expanded state. aria-expanded is exposed when used as a trigger.
 */
export function ButtonWithChevron({
  children,
  direction = "down",
  open = false,
  variant = "outline",
  size = "md",
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const name = direction === "right" ? "chevron-right" : "chevron-down";
  const rot = direction === "down" && open ? "rotate(180deg)" : "none";
  return (
    <button
      type={type}
      className={cls("ds-btn", VARIANTS[variant]||"ds-btn--outline", `ds-btn--${size}`)}
      aria-expanded={typeof rest["aria-expanded"] !== "undefined" ? rest["aria-expanded"] : (open || undefined)}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      <span>{children}</span>
      <Icon name={name} className="ds-btn-icon" style={{transition:"transform var(--ds-duration-default) var(--ds-ease)", transform:rot}} />
    </button>
  );
}

export default ButtonWithChevron;
