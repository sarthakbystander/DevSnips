import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * BackButton — returns to the previous view.
 *
 * Leading arrow-left + label. Can render as a button (onClick, default) or
 * a link (href). Icon-only mode (`showLabel={false}`) needs a label prop
 * for aria-label. Use above page content or as a wizard footer action.
 */
export function BackButton({
  children = "Back",
  href,
  size = "md",
  variant = "ghost",
  showLabel = true,
  onClick,
  ...rest
}) {
  const vc = { ghost:"ds-btn--ghost", outline:"ds-btn--outline" }[variant] || "ds-btn--ghost";
  const cls_ = cls("ds-btn", vc, `ds-btn--${size}`, !showLabel && "ds-btn--icon");
  const content = (
    <>
      <Icon name="arrow-left" className="ds-btn-icon" />
      {showLabel && <span>{children}</span>}
    </>
  );
  if (href) {
    return <a href={href} className={cls_} {...rest}>{content}</a>;
  }
  return (
    <button type="button" className={cls_} onClick={onClick} aria-label={showLabel ? undefined : (typeof children==="string"?children:"Back")} {...rest}>
      {content}
    </button>
  );
}

export default BackButton;
