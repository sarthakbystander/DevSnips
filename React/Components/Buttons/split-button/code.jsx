import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * SplitButton — primary action + attached action menu.
 *
 * The leading button performs the default action. The trailing icon button
 * opens a menu of alternative actions (aria-haspopup="menu", aria-expanded).
 * Keyboard: the trigger opens the menu; Arrow keys move; Enter activates;
 * Escape closes and returns focus to the trigger.
 */
export function SplitButton({
  label,
  onAction,
  actions = [],
  size = "md",
  variant = "solid",
  disabled = false,
  ...rest
}) {
  const [open, setOpen] = React.useState(false);
  const [active, setActive] = React.useState(0);
  const triggerRef = React.useRef(null);
  const itemRefs = React.useRef([]);
  const containerRef = useClickOutside(() => setOpen(false), open);

  function openMenu() {
    setOpen(true);
    setTimeout(() => itemRefs.current[0] && itemRefs.current[0].focus(), 0);
  }
  function onTriggerKey(e) {
    if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") { e.preventDefault(); openMenu(); }
  }
  function onItemKey(e, i) {
    if (e.key === "ArrowDown") { e.preventDefault(); const n=(i+1)%actions.length; itemRefs.current[n]&&itemRefs.current[n].focus(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); const n=(i-1+actions.length)%actions.length; itemRefs.current[n]&&itemRefs.current[n].focus(); }
    else if (e.key === "Escape") { setOpen(false); triggerRef.current && triggerRef.current.focus(); }
    else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(i); }
  }
  function choose(i) {
    setOpen(false);
    setActive(i);
    onAction && onAction(actions[i].id, actions[i]);
    triggerRef.current && triggerRef.current.focus();
  }
  const variantClass = variant === "outline" ? "ds-btn--outline" : "ds-btn--solid";
  return (
    <div className="ds-split" ref={containerRef} style={{display:"inline-flex", position:"relative"}}>
      <button
        type="button"
        ref={triggerRef}
        className={cls("ds-btn", variantClass, `ds-btn--${size}`)}
        style={{borderTopRightRadius:0, borderBottomRightRadius:0, marginRight:-1}}
        disabled={disabled}
        onClick={() => onAction && onAction(actions[active]?.id, actions[active])}
        {...rest}
      >
        {actions[active]?.icon && <Icon name={actions[active].icon} className="ds-btn-icon" />}
        <span>{actions[active]?.label || label}</span>
      </button>
      <button
        type="button"
        className={cls("ds-btn", variantClass, `ds-btn--${size}`, "ds-btn--icon")}
        style={{borderTopLeftRadius:0, borderBottomLeftRadius:0}}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label="More actions"
        disabled={disabled}
        onClick={() => (open ? setOpen(false) : openMenu())}
        onKeyDown={onTriggerKey}
      >
        <Icon name="chevron-down" className="ds-btn-icon" style={{transform:open?"rotate(180deg)":"none", transition:"transform var(--ds-duration-default) var(--ds-ease)"}} />
      </button>
      {open && (
        <div className="ds-menu" role="menu" style={{position:"absolute", top:"calc(100% + 4px)", right:0}}>
          {actions.map((a, i) => (
            <button
              key={a.id}
              ref={el => itemRefs.current[i] = el}
              role="menuitem"
              className="ds-menu-item"
              data-variant={a.destructive ? "destructive" : undefined}
              tabIndex={-1}
              onClick={() => choose(i)}
              onKeyDown={(e) => onItemKey(e, i)}
            >
              {a.icon && <Icon name={a.icon} className="ds-btn-icon" />}
              <span>{a.label}</span>
              {i === active && <Icon name="check" className="ds-btn-icon" style={{marginLeft:"auto"}} />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default SplitButton;
