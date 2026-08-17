import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

const VARIANTS = { solid:"ds-btn--solid", outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost" };

/**
 * ButtonGroup — joined row of related buttons.
 *
 * Renders a `role="group"` container of buttons that share borders (inner
 * buttons lose their side radius and overlap borders by 1px). Pass children
 * directly (`<ButtonGroup><button/>…</ButtonGroup>`) for full control, or the
 * `items` prop for a quick outline/secondary group.
 */
export function ButtonGroup({ children, items, variant = "outline", size = "md", label, ...rest }) {
  const vc = VARIANTS[variant] || "ds-btn--outline";
  return (
    <div className="ds-btn-group" role="group" aria-label={label} style={{display:"inline-flex"}} {...rest}>
      {items ? items.map((it, i) => (
        <button
          key={it.id || i}
          type="button"
          className={cls("ds-btn", vc, `ds-btn--${size}`)}
          style={{
            borderRadius: 0,
            marginLeft: i > 0 ? -1 : 0,
            ...(it.active ? { background: "var(--ds-color-surface-active)", fontWeight: 600 } : {}),
          }}
          aria-pressed={it.active || undefined}
          onClick={it.onClick}
        >
          {it.icon && <Icon name={it.icon} className="ds-btn-icon" />}
          <span>{it.label}</span>
        </button>
      )) : React.Children.map(children, (child, i) => {
        if (!React.isValidElement(child)) return child;
        return React.cloneElement(child, {
          style: { ...(child.props.style||{}), borderRadius: 0, marginLeft: i > 0 ? -1 : 0 },
        });
      })}
    </div>
  );
}

export default ButtonGroup;
