import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * RefreshButton — re-fetch with in-flight feedback.
 *
 * `onRefresh` may return a Promise; while it is pending the refresh icon
 * spins (respecting reduced motion), the button is disabled, and aria-busy
 * is set. Icon-only mode for compact toolbars.
 */
export function RefreshButton({
  onRefresh,
  label = "Refresh",
  showLabel = false,
  size = "sm",
  variant = "ghost",
  ...rest
}) {
  const [loading, setLoading] = React.useState(false);
  async function run() {
    if (loading) return;
    setLoading(true);
    try { await Promise.resolve(onRefresh && onRefresh()); }
    finally { setLoading(false); }
  }
  const vc = { ghost:"ds-btn--ghost", outline:"ds-btn--outline", secondary:"ds-btn--secondary" }[variant] || "ds-btn--ghost";
  return (
    <button
      type="button"
      className={cls("ds-btn", vc, `ds-btn--${size}`, !showLabel && "ds-btn--icon")}
      onClick={run}
      disabled={loading}
      aria-busy={loading || undefined}
      aria-label={label}
      {...rest}
    >
      <Icon name="refresh" className="ds-btn-icon" style={loading ? {animation:"ds-spin 0.8s linear infinite"} : undefined} />
      {showLabel && <span>{loading ? "Refreshing…" : label}</span>}
    </button>
  );
}

export default RefreshButton;
