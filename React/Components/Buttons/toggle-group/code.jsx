import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * ToggleGroup — joined toggles, single or multi select.
 *
 * `type="single"` behaves like a radiogroup (one on). `type="multiple"`
 * behaves like a group of checkboxes. Selected segments use
 * color.surface-active + aria-pressed="true". Keyboard arrows move focus.
 */
export function ToggleGroup({
  options,
  value,
  defaultValue,
  onValueChange,
  type = "single",
  size = "sm",
  label,
  ...rest
}) {
  const arr = Array.isArray(value) ? value : (value ? [value] : []);
  const [internal, setInternal] = React.useState(defaultValue ? (Array.isArray(defaultValue)?defaultValue:[defaultValue]) : []);
  const isControlled = value !== undefined;
  const current = isControlled ? arr : internal;
  const refs = React.useRef([]);
  function isActive(v) { return current.indexOf(v) !== -1; }
  function toggle(v) {
    let next;
    if (type === "single") next = isActive(v) ? [] : [v];
    else next = isActive(v) ? current.filter(x=>x!==v) : [...current, v];
    if (!isControlled) setInternal(next);
    onValueChange && onValueChange(type==="single" ? (next[0]||null) : next);
  }
  function onKey(e, i) {
    if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); refs.current[(i+1)%options.length] && refs.current[(i+1)%options.length].focus(); }
    else if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); refs.current[(i-1+options.length)%options.length] && refs.current[(i-1+options.length)%options.length].focus(); }
    else if (e.key === " " || e.key === "Enter") { e.preventDefault(); toggle(options[i].value); }
  }
  return (
    <div className="ds-toggle-group" role="group" aria-label={label} style={{display:"inline-flex", border:"1px solid var(--ds-color-border)", borderRadius:"var(--ds-radius-sm)", overflow:"hidden"}}>
      {options.map((opt, i) => {
        const on = isActive(opt.value);
        return (
          <button
            key={opt.value}
            ref={el => refs.current[i] = el}
            type="button"
            className={cls("ds-btn ds-btn--ghost", `ds-btn--${size}`)}
            aria-pressed={on}
            style={{
              borderRadius:0, border:0, margin:0,
              background: on ? "var(--ds-color-surface-active)" : "transparent",
              fontWeight: on ? 600 : 500,
              borderLeft: i>0 ? "1px solid var(--ds-color-border)" : 0,
            }}
            onClick={() => toggle(opt.value)}
            onKeyDown={(e)=>onKey(e,i)}
          >
            {opt.icon && <Icon name={opt.icon} className="ds-btn-icon" />}
            <span>{opt.label}</span>
          </button>
        );
      })}
    </div>
  );
}

export default ToggleGroup;
