import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * MoreActionsButton — overflow menu trigger.
 *
 * `actions` is an array of {id,label,icon,destructive}. Opens a menu
 * (aria-haspopup="menu") positioned below-right by default. Keyboard:
 * Arrow keys move, Enter activates, Escape closes and returns focus.
 */
export function MoreActionsButton({
  actions = [],
  onAction,
  size = "sm",
  variant = "ghost",
  label = "More actions",
  align = "right",
  ...rest
}) {
  const [open, setOpen] = React.useState(false);
  const containerRef = useClickOutside(() => setOpen(false), open);
  const itemRefs = React.useRef([]);
  const triggerRef = React.useRef(null);
  function openMenu() { setOpen(true); setTimeout(()=>itemRefs.current[0]&&itemRefs.current[0].focus(),0); }
  function onKey(e, i) {
    if (e.key==="ArrowDown"){e.preventDefault();itemRefs.current[(i+1)%actions.length]&&itemRefs.current[(i+1)%actions.length].focus();}
    else if (e.key==="ArrowUp"){e.preventDefault();itemRefs.current[(i-1+actions.length)%actions.length]&&itemRefs.current[(i-1+actions.length)%actions.length].focus();}
    else if (e.key==="Escape"){setOpen(false);triggerRef.current&&triggerRef.current.focus();}
    else if (e.key==="Enter"||e.key===" "){e.preventDefault();choose(i);}
  }
  function choose(i){ setOpen(false); onAction&&onAction(actions[i].id, actions[i]); triggerRef.current&&triggerRef.current.focus(); }
  const vc = { ghost:"ds-btn--ghost", outline:"ds-btn--outline", secondary:"ds-btn--secondary" }[variant] || "ds-btn--ghost";
  return (
    <div ref={containerRef} style={{position:"relative", display:"inline-flex"}}>
      <button
        type="button"
        ref={triggerRef}
        className={cls("ds-btn", vc, `ds-btn--${size}`, "ds-btn--icon")}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={label}
        onClick={()=>open?setOpen(false):openMenu()}
        {...rest}
      >
        <Icon name="more" className="ds-btn-icon" />
      </button>
      {open && (
        <div className="ds-menu" role="menu" style={{position:"absolute", top:"calc(100% + 4px)", [align]:"0"}}>
          {actions.map((a,i)=>(
            <button key={a.id} ref={el=>itemRefs.current[i]=el} role="menuitem" tabIndex={-1} className="ds-menu-item" data-variant={a.destructive?"destructive":undefined} onClick={()=>choose(i)} onKeyDown={(e)=>onKey(e,i)}>
              {a.icon && <Icon name={a.icon} className="ds-btn-icon" />}
              <span>{a.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default MoreActionsButton;
