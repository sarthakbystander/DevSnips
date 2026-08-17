import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * FilterButton — opens filters + shows active count.
 *
 * `activeCount` renders a count chip and switches the button to
 * color.surface-active so the filtered state is obvious. `open` rotates the
 * leading icon and exposes aria-expanded. Wire to a popover/panel of filters.
 */
export function FilterButton({
  activeCount = 0,
  open = false,
  size = "sm",
  variant = "outline",
  onToggle,
  label = "Filter",
  ...rest
}) {
  const vc = { outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost" }[variant] || "ds-btn--outline";
  const hasFilters = activeCount > 0;
  return (
    <button
      type="button"
      className={cls("ds-btn", vc, `ds-btn--${size}`)}
      aria-expanded={open || undefined}
      aria-label={hasFilters ? `${label}, ${activeCount} active` : label}
      onClick={onToggle}
      style={{ background: hasFilters ? "var(--ds-color-surface-active)" : undefined, fontWeight: hasFilters ? 600 : 500 }}
      {...rest}
    >
      <Icon name="filter" className="ds-btn-icon" />
      <span>{label}</span>
      {hasFilters && <span className="ds-chip" aria-hidden="true">{activeCount}</span>}
    </button>
  );
}

export default FilterButton;
