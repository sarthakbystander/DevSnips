import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * CommandButton — opens a command palette.
 *
 * A wide ghost/outline trigger with a search icon, placeholder text, and a
 * kbd hint showing the platform shortcut (⌘K / Ctrl K). Wire `onOpen` to
 * mount the palette. Listens for the global shortcut when `bindShortcut`
 * is true.
 */
export function CommandButton({
  placeholder = "Search or run a command…",
  shortcut = "⌘K",
  onOpen,
  variant = "outline",
  size = "md",
  bindShortcut = true,
  ...rest
}) {
  React.useEffect(() => {
    if (!bindShortcut) return;
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        onOpen && onOpen();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [bindShortcut, onOpen]);
  const vc = { outline:"ds-btn--outline", secondary:"ds-btn--secondary" }[variant] || "ds-btn--outline";
  return (
    <button
      type="button"
      className={cls("ds-btn", vc, `ds-btn--${size}`)}
      onClick={onOpen}
      style={{ justifyContent:"space-between", width:"100%", maxWidth:420, color:"var(--ds-color-muted-foreground)" }}
      {...rest}
    >
      <span className="ds-row" style={{gap:"var(--ds-spacing-2)"}}>
        <Icon name="search" className="ds-btn-icon" />
        <span>{placeholder}</span>
      </span>
      <kbd style={{font:"var(--ds-font-mono)", fontSize:11, padding:"2px 6px", background:"var(--ds-color-surface-subtle)", border:"1px solid var(--ds-color-border)", borderRadius:"var(--ds-radius-xs)", color:"var(--ds-color-muted-foreground)"}}>{shortcut}</kbd>
    </button>
  );
}

export default CommandButton;
