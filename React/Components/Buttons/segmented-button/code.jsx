import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * SegmentedButton — joined single-choice control.
 *
 * Behaves like a radiogroup: one selected option at a time. The selected
 * segment uses color.surface-active + aria-checked="true". Use for 2–5
 * mutually exclusive options in compact toolbars.
 */
export function SegmentedButton({ options, value, onChange, size = "sm", label, ...rest }) {
  return (
    <div className="ds-segmented" role="radiogroup" aria-label={label} style={{display:"inline-flex", border:"1px solid var(--ds-color-border)", borderRadius:"var(--ds-radius-sm)", overflow:"hidden"}}>
      {options.map((opt, i) => {
        const selected = opt.value === value;
        return (
          <button
            key={opt.value}
            type="button"
            role="radio"
            aria-checked={selected}
            className={cls("ds-btn ds-btn--ghost", `ds-btn--${size}`)}
            style={{
              borderRadius: 0,
              border: 0,
              margin: 0,
              background: selected ? "var(--ds-color-surface-active)" : "transparent",
              fontWeight: selected ? 600 : 500,
              borderLeft: i > 0 ? "1px solid var(--ds-color-border)" : 0,
            }}
            onClick={() => onChange && onChange(opt.value)}
          >
            {opt.icon && <Icon name={opt.icon} className="ds-btn-icon" />}
            <span>{opt.label}</span>
          </button>
        );
      })}
    </div>
  );
}

export default SegmentedButton;
