import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

const VARIANTS = { solid:"ds-btn--solid", outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost" };

/**
 * AddButton — creation affordance with a leading plus.
 *
 * `label` becomes both the visible text and (when icon-only) the accessible
 * name. Defaults to solid since adding is often the primary creation action
 * on a surface. Icon-only mode (`showLabel={false}`) for dense toolbars.
 */
export function AddButton({
  children = "Add",
  variant = "solid",
  size = "md",
  showLabel = true,
  disabled = false,
  type = "button",
  onClick,
  ...rest
}) {
  const vc = VARIANTS[variant] || "ds-btn--solid";
  return (
    <button
      type={type}
      className={cls("ds-btn", vc, `ds-btn--${size}`, !showLabel && "ds-btn--icon")}
      aria-label={showLabel ? undefined : (typeof children==="string"?children:"Add")}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      <Icon name="plus" className="ds-btn-icon" />
      {showLabel && <span>{children}</span>}
    </button>
  );
}

export default AddButton;
