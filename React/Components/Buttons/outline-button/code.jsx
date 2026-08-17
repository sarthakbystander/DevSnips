import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * OutlineButton — bordered, transparent-fill action.
 *
 * Medium emphasis. Strong 1px border (color.border-strong), transparent
 * background that lifts to color.surface-hover on hover. Pairs with a
 * SolidButton to establish primary/secondary hierarchy.
 */
export function OutlineButton({
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
      className={cls("ds-btn ds-btn--outline", `ds-btn--${size}`, block && "ds-btn--block")}
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

export default OutlineButton;
