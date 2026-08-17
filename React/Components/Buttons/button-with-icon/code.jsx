import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

const VARIANTS = { solid:"ds-btn--solid", outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost" };

/**
 * ButtonWithIcon — labeled button with leading/trailing icon.
 *
 * Icons use the shared `Icon` set at the size token for the chosen button
 * size (14–20px). The 8px control gap keeps icon and label optically aligned
 * without overpowering the typography.
 */
export function ButtonWithIcon({
  children,
  icon,
  iconPosition = "leading",
  variant = "solid",
  size = "md",
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const iconEl = icon ? <Icon name={icon} className="ds-btn-icon" /> : null;
  return (
    <button
      type={type}
      className={cls("ds-btn", VARIANTS[variant]||"ds-btn--solid", `ds-btn--${size}`)}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      {iconPosition === "leading" && iconEl}
      <span>{children}</span>
      {iconPosition === "trailing" && iconEl}
    </button>
  );
}

export default ButtonWithIcon;
