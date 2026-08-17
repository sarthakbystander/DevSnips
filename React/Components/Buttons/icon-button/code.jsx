import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * IconButton — square icon-only control.
 *
 * No visible label, so an `aria-label` is required for an accessible name.
 * Maintains 36px (md) default touch target; the `--icon` modifier makes the
 * button square (width == height). Use for controls where a label would be
 * redundant given surrounding context (toolbar, card header).
 */
export function IconButton({
  name,
  label,
  size = "md",
  variant = "ghost",
  active = false,
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const variantClass = {
    ghost: "ds-btn--ghost",
    outline: "ds-btn--outline",
    secondary: "ds-btn--secondary",
    solid: "ds-btn--solid",
  }[variant] || "ds-btn--ghost";
  return (
    <button
      type={type}
      className={cls("ds-btn", variantClass, `ds-btn--${size}`, "ds-btn--icon")}
      style={active ? { background: "var(--ds-color-surface-active)" } : undefined}
      aria-label={label}
      aria-pressed={active || undefined}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      <Icon name={name} className="ds-btn-icon" />
    </button>
  );
}

export default IconButton;
