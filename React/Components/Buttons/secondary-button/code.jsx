import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * SecondaryButton — tonal secondary surface.
 *
 * color.secondary background with color.border. Lower emphasis than solid,
 * higher than outline/ghost. Good for repeated toolbar actions.
 */
export function SecondaryButton({
  children,
  size = "md",
  block = false,
  iconLeft,
  iconRight,
  loading = false,
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const isDisabled = disabled || loading;
  return (
    <button
      type={type}
      className={cls("ds-btn ds-btn--secondary", `ds-btn--${size}`, block && "ds-btn--block")}
      disabled={isDisabled}
      aria-busy={loading || undefined}
      onClick={onClick}
      {...rest}
    >
      {loading ? <span className="ds-btn-spinner" aria-hidden="true" /> : iconLeft}
      <span>{children}</span>
      {!loading && iconRight}
    </button>
  );
}

export default SecondaryButton;
