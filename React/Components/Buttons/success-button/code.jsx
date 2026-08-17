import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * SuccessButton — filled positive action.
 *
 * color.success background, color.success-foreground text. Contextual only:
 * confirm/approve/publish/complete. Not a replacement for the primary
 * action. Supports a `done` state for transient completion feedback.
 */
export function SuccessButton({
  children,
  size = "md",
  block = false,
  iconLeft,
  iconRight,
  loading = false,
  done = false,
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const isDisabled = disabled || loading;
  return (
    <button
      type={type}
      className={cls("ds-btn ds-btn--success", `ds-btn--${size}`, block && "ds-btn--block")}
      disabled={isDisabled}
      aria-busy={loading || undefined}
      onClick={onClick}
      {...rest}
    >
      {loading ? <span className="ds-btn-spinner" aria-hidden="true" /> : done ? <Icon name="check" className="ds-btn-icon" /> : iconLeft}
      <span>{children}</span>
      {!loading && !done && iconRight}
    </button>
  );
}

export default SuccessButton;
