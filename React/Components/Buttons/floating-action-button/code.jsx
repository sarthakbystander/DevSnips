import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * FloatingActionButton — primary compose action hovering over content.
 *
 * Circular, elevated (shadow-md), fixed to a corner. Icon + optional label
 * (extended FAB). aria-label required. Reserve one per screen for the
 * primary creation action. Respects reduced motion on hover lift.
 */
export function FloatingActionButton({
  icon = "plus",
  label,
  position = "bottom-right",
  extended = false,
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const pos = {
    "bottom-right": { bottom: "var(--ds-spacing-6)", right: "var(--ds-spacing-6)" },
    "bottom-left": { bottom: "var(--ds-spacing-6)", left: "var(--ds-spacing-6)" },
    "top-right": { top: "var(--ds-spacing-6)", right: "var(--ds-spacing-6)" },
  }[position] || { bottom: "var(--ds-spacing-6)", right: "var(--ds-spacing-6)" };
  return (
    <button
      type={type}
      className={cls("ds-btn ds-btn--solid ds-fab", extended && "ds-fab--extended")}
      style={{
        position: "fixed",
        ...pos,
        zIndex: 35,
        height: extended ? 48 : 56,
        width: extended ? undefined : 56,
        borderRadius: "var(--ds-radius-full)",
        padding: extended ? "0 var(--ds-spacing-5)" : 0,
        boxShadow: "var(--ds-shadow-md)",
        gap: "var(--ds-spacing-2)",
      }}
      aria-label={label || icon}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      <Icon name={icon} className="ds-btn-icon" style={{width:20, height:20}} />
      {extended && label && <span>{label}</span>}
    </button>
  );
}

export default FloatingActionButton;
