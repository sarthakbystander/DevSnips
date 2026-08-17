import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * DestructiveButton — filled destructive action.
 *
 * color.destructive background, color.destructive-foreground text. Use for
 * irreversible actions. Provide a confirming context and pair with a
 * non-destructive Cancel. A subtle variant (`outline`) is available for
 * lower-emphasis destructive controls in dense rows.
 */
export function DestructiveButton({
  children,
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
  const variantClass = variant === "outline" ? "ds-btn--outline-destructive" : "ds-btn--destructive";
  const isDisabled = disabled || loading;
  return (
    <button
      type={type}
      className={cls("ds-btn", variantClass, `ds-btn--${size}`, block && "ds-btn--block")}
      disabled={isDisabled}
      aria-busy={loading || undefined}
      onClick={onClick}
      {...rest}
    >
      {loading ? <span className="ds-btn-spinner" aria-hidden="true" /> : iconLeft}
      <span>{children}</span>
    </button>
  );
}

export default DestructiveButton;
