import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * GhostButton — transparent, borderless low-emphasis action.
 *
 * No border, transparent fill; hover lifts to color.surface-hover. Use for
 * tertiary or incidental actions so the primary action keeps emphasis.
 */
export function GhostButton({
  children,
  size = "md",
  iconLeft,
  iconRight,
  active = false,
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  return (
    <button
      type={type}
      className={cls("ds-btn ds-btn--ghost", `ds-btn--${size}`, active && "is-active")}
      style={active ? { background: "var(--ds-color-surface-active)" } : undefined}
      aria-pressed={active || undefined}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      {iconLeft}
      <span>{children}</span>
      {iconRight}
    </button>
  );
}

export default GhostButton;
