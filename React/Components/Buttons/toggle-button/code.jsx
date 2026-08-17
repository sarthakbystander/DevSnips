import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * ToggleButton — single binary switch.
 *
 * `pressed` (controlled) or default-uncontrolled. Exposes aria-pressed and
 * swaps to color.surface-active when on so the state is conveyed by more
 * than color alone. `iconOn`/`iconOff` allow the icon to reflect state.
 */
export function ToggleButton({
  pressed: pressedProp,
  defaultPressed = false,
  onToggle,
  iconOff,
  iconOn,
  label,
  size = "md",
  variant = "ghost",
  showLabel = true,
  ...rest
}) {
  const [pressed, setPressed] = React.useState(defaultPressed);
  const isControlled = pressedProp !== undefined;
  const value = isControlled ? pressedProp : pressed;
  function click() {
    const next = !value;
    if (!isControlled) setPressed(next);
    onToggle && onToggle(next);
  }
  const variantClass = { ghost:"ds-btn--ghost", outline:"ds-btn--outline", secondary:"ds-btn--secondary" }[variant] || "ds-btn--ghost";
  return (
    <button
      type="button"
      className={cls("ds-btn", variantClass, `ds-btn--${size}`, !showLabel && "ds-btn--icon")}
      aria-pressed={value}
      aria-label={label}
      onClick={click}
      style={{ background: value ? "var(--ds-color-surface-active)" : undefined, fontWeight: value ? 600 : 500 }}
      {...rest}
    >
      <Icon name={value ? (iconOn || iconOff) : iconOff} className="ds-btn-icon" />
      {showLabel && <span>{label}</span>}
    </button>
  );
}

export default ToggleButton;
