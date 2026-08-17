import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * SortButton — sets sort field and direction.
 *
 * `field` is the active column, `direction` is "asc"|"desc"|null. Clicking
 * the button toggles direction (desc→asc→none→desc). When `fields` is
 * provided it renders as a menu trigger to pick the column. The active sort
 * is shown via the field label + a rotated chevron, not color alone.
 */
export function SortButton({
  field = "Created",
  direction = "desc",
  onToggle,
  size = "sm",
  variant = "outline",
  ...rest
}) {
  const vc = { outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost" }[variant] || "ds-btn--outline";
  const active = !!direction;
  const dirLabel = direction === "asc" ? "ascending" : direction === "desc" ? "descending" : "unsorted";
  return (
    <button
      type="button"
      className={cls("ds-btn", vc, `ds-btn--${size}`)}
      aria-label={`Sort by ${field}, currently ${dirLabel}`}
      onClick={onToggle}
      style={{ background: active ? "var(--ds-color-surface-active)" : undefined, fontWeight: active ? 600 : 500 }}
      {...rest}
    >
      <Icon name="sort" className="ds-btn-icon" />
      <span>{field}</span>
      <Icon
        name="chevron-down"
        className="ds-btn-icon"
        style={{
          transform: direction === "asc" ? "rotate(180deg)" : "none",
          opacity: active ? 1 : 0.5,
          transition: "transform var(--ds-duration-default) var(--ds-ease)",
        }}
      />
    </button>
  );
}

export default SortButton;
