import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * ExportButton — menu trigger for export destinations.
 *
 * `formats` is an array of {id,label,icon}. Opens a keyboard-navigable menu
 * (aria-haspopup="menu"); Arrow keys move, Enter exports, Escape closes.
 * Use in table/report toolbars where multiple export targets exist.
 */
export function ExportButton({
  formats = [],
  onExport,
  size = "sm",
  variant = "outline",
  disabled = false,
  label = "Export",
  ...rest
}) {
  const [open, setOpen] = React.useState(false);
  const containerRef = useClickOutside(() => setOpen(false), open);
  const itemRefs = React.useRef([]);
  const triggerRef = React.useRef(null);
  function openMenu() { setOpen(true); setTimeout(()=>itemRefs.current[0]&&itemRefs.current[0].focus(),0); }
  function onKey(e, i) {
    if (e.key==="ArrowDown"){e.preventDefault();itemRefs.current[(i+1)%formats.length]&&itemRefs.current[(i+1)%formats.length].focus();}
    else if (e.key==="ArrowUp"){e.preventDefault();itemRefs.current[(i-1+formats.length)%formats.length]&&itemRefs.current[(i-1+formats.length)%formats.length].focus();}
    else if (e.key==="Escape"){setOpen(false);triggerRef.current&&triggerRef.current.focus();}
    else if (e.key==="Enter"||e.key===" "){e.preventDefault();choose(i);}
  }
  function choose(i){ setOpen(false); onExport&&onExport(formats[i].id, formats[i]); triggerRef.current&&triggerRef.current.focus(); }
  const vc = { outline:"ds-btn--outline", secondary:"ds-btn--secondary" }[variant] || "ds-btn--outline";
  return (
    <div ref={containerRef} style={{position:"relative", display:"inline-flex"}}>
      <button
        type="button"
        ref={triggerRef}
        className={cls("ds-btn", vc, `ds-btn--${size}`)}
        aria-haspopup="menu"
        aria-expanded={open}
        disabled={disabled}
        onClick={()=>open?setOpen(false):openMenu()}
        {...rest}
      >
        <Icon name="download" className="ds-btn-icon" />
        <span>{label}</span>
        <Icon name="chevron-down" className="ds-btn-icon" style={{transform:open?"rotate(180deg)":"none",transition:"transform var(--ds-duration-default) var(--ds-ease)"}} />
      </button>
      {open && (
        <div className="ds-menu" role="menu" style={{position:"absolute", top:"calc(100% + 4px)", right:0}}>
          {formats.map((f,i)=>(
            <button key={f.id} ref={el=>itemRefs.current[i]=el} role="menuitem" tabIndex={-1} className="ds-menu-item" onClick={()=>choose(i)} onKeyDown={(e)=>onKey(e,i)}>
              <Icon name={f.icon||"download"} className="ds-btn-icon" />
              <span>{f.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default ExportButton;
