import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * DownloadButton — direct download with progress feedback.
 *
 * Fires `onDownload` (wire to a real fetch/blob) and surfaces a working
 * state with a spinner + "Downloading…" label, then a brief done state.
 * Supports `meta` (e.g. "CSV · 2.4 MB") under or beside the label.
 */
export function DownloadButton({
  children = "Download",
  meta,
  href,
  variant = "outline",
  size = "md",
  onDownload,
  ...rest
}) {
  const [state, setState] = React.useState("idle");
  function start(e) {
    if (state !== "idle") return;
    setState("working");
    Promise.resolve(onDownload && onDownload()).finally(() => {
      setState("done");
      setTimeout(() => setState("idle"), 2000);
    });
  }
  const vc = { outline:"ds-btn--outline", solid:"ds-btn--solid", secondary:"ds-btn--secondary" }[variant] || "ds-btn--outline";
  const label = state === "working" ? "Downloading…" : state === "done" ? "Downloaded" : children;
  return (
    <button
      type="button"
      className={cls("ds-btn", vc, `ds-btn--${size}`)}
      onClick={start}
      disabled={state==="working"}
      aria-busy={state==="working"||undefined}
      {...rest}
    >
      {state==="working" ? <span className="ds-btn-spinner" aria-hidden="true" /> : <Icon name={state==="done"?"check":"download"} className="ds-btn-icon" />}
      <span style={{display:"inline-flex", flexDirection:"column", alignItems:"flex-start", lineHeight:1.2}}>
        <span>{label}</span>
        {meta && <span style={{font:"var(--ds-text-caption)", color:"var(--ds-color-muted-foreground)", fontWeight:400}}>{meta}</span>}
      </span>
    </button>
  );
}

export default DownloadButton;
