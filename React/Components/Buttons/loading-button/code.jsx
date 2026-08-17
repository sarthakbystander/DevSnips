import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

const VARIANTS = {
  solid: "ds-btn--solid",
  outline: "ds-btn--outline",
  secondary: "ds-btn--secondary",
  destructive: "ds-btn--destructive",
  success: "ds-btn--success",
};

/**
 * LoadingButton — action button with a first-class loading state.
 *
 * `loading` swaps the leading slot for a spinner, sets `aria-busy`, and
 * disables the button so the action can't be double-fired. The label can
 * change during loading; layout is preserved because the spinner occupies
 * the same icon slot.
 */
export function LoadingButton({
  children,
  loadingLabel,
  variant = "solid",
  size = "md",
  block = false,
  iconLeft,
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
      className={cls("ds-btn", VARIANTS[variant] || "ds-btn--solid", `ds-btn--${size}`, block && "ds-btn--block")}
      disabled={isDisabled}
      aria-busy={loading || undefined}
      onClick={onClick}
      {...rest}
    >
      {loading ? <span className="ds-btn-spinner" aria-hidden="true" /> : iconLeft}
      <span>{loading && loadingLabel ? loadingLabel : children}</span>
    </button>
  );
}

export default LoadingButton;
