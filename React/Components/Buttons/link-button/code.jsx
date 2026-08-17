import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * LinkButton — button rendered as an inline link.
 *
 * color.link text, underline on hover, no border or fill. Use for terse
 * inline actions ("View all", "Forgot password?") that should read as links
 * but still trigger onClick. For true navigation, prefer an <a>.
 */
export function LinkButton({
  children,
  iconLeft,
  iconRight,
  disabled = false,
  type = "button",
  onClick,
  href,
  ...rest
}) {
  if (href) {
    return (
      <a
        href={href}
        className={cls("ds-btn ds-btn--link", disabled && "is-disabled")}
        style={disabled ? { opacity: 0.5, pointerEvents: "none" } : undefined}
        aria-disabled={disabled || undefined}
        {...rest}
      >
        {iconLeft}
        <span>{children}</span>
        {iconRight}
      </a>
    );
  }
  return (
    <button
      type={type}
      className="ds-btn ds-btn--link"
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

export default LinkButton;
