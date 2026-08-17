import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * CloseButton — dismiss control for overlays.
 *
 * Icon-only (X), requires `aria-label` (defaults to "Close"). Use inside
 * dialogs, drawers, toasts, and banners. Pair with Escape handling on the
 * owning surface. 36px default; 32px in compact headers.
 */
export function CloseButton({
  label = "Close",
  size = "md",
  variant = "ghost",
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const vc = { ghost:"ds-btn--ghost", outline:"ds-btn--outline" }[variant] || "ds-btn--ghost";
  return (
    <button
      type={type}
      className={cls("ds-btn", vc, `ds-btn--${size}`, "ds-btn--icon")}
      aria-label={label}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      <Icon name="x" className="ds-btn-icon" />
    </button>
  );
}

export default CloseButton;
