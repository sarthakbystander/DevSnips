import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * CopyButton — clipboard copy with feedback.
 *
 * Uses the async Clipboard API with an execCommand fallback. On success,
 * swaps the icon to a check and the label to `copiedLabel` for `resetMs`,
 * then reverts. aria-live announces the copied state.
 */
export function CopyButton({
  value,
  label = "Copy",
  copiedLabel = "Copied",
  size = "sm",
  variant = "outline",
  resetMs = 2000,
  onCopy,
  ...rest
}) {
  const [copied, copy] = useCopy(resetMs);
  async function handle() {
    await copy(value);
    onCopy && onCopy(value);
  }
  const vc = { outline:"ds-btn--outline", secondary:"ds-btn--secondary", ghost:"ds-btn--ghost", solid:"ds-btn--solid" }[variant] || "ds-btn--outline";
  return (
    <button
      type="button"
      className={cls("ds-btn", vc, `ds-btn--${size}`)}
      onClick={handle}
      aria-label={`${copied ? copiedLabel : label}: ${value}`}
      {...rest}
    >
      <Icon name={copied ? "check" : "copy"} className="ds-btn-icon" />
      <span>{copied ? copiedLabel : label}</span>
      <span className="sr-only" role="status" aria-live="polite">{copied ? copiedLabel : ""}</span>
    </button>
  );
}

export default CopyButton;
