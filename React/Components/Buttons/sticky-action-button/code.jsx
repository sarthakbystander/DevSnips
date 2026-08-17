import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * StickyActionButton — persistent primary CTA.
 *
 * Sticks to the bottom of the viewport with a hairline top border and a
 * translucent surface so content scrolls beneath. Use for the single
 * primary action on long forms or review screens. Renders leading + label
 * + optional trailing, and disables cleanly.
 */
export function StickyActionButton({
  children,
  iconLeft,
  iconRight,
  loading = false,
  disabled = false,
  variant = "solid",
  type = "button",
  onClick,
  ...rest
}) {
  const vc = { solid:"ds-btn--solid", destructive:"ds-btn--destructive", success:"ds-btn--success" }[variant] || "ds-btn--solid";
  return (
    <div className="ds-sticky-bar" style={{position:"sticky", bottom:0, left:0, right:0, zIndex:20, display:"flex", alignItems:"center", gap:"var(--ds-spacing-3)", padding:"var(--ds-spacing-3) 0", background:"color-mix(in srgb, var(--ds-color-background) 88%, transparent)", backdropFilter:"blur(8px)", borderTop:"1px solid var(--ds-color-border)"}}>
      <button
        type={type}
        className={cls("ds-btn", vc, "ds-btn--lg", "ds-btn--block")}
        disabled={disabled || loading}
        aria-busy={loading || undefined}
        onClick={onClick}
        {...rest}
      >
        {loading ? <span className="ds-btn-spinner" aria-hidden="true" /> : iconLeft}
        <span>{children}</span>
        {!loading && iconRight}
      </button>
    </div>
  );
}

export default StickyActionButton;
