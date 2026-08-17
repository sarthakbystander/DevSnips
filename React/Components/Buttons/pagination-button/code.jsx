import React from "react";

function cls(...p) { return p.filter(Boolean).join(" "); }

/**
 * PaginationButton — page navigation for paginated lists/tables.
 *
 * `page` is current, `totalPages` is count. Renders Prev, a windowed number
 * set with ellipses, and Next. Active page uses color.surface-active +
 * aria-current="page". Prev/Next disable at the bounds (aria-disabled, not
 * removed, so the affordance stays perceivable).
 */
export function PaginationButton({
  page = 1,
  totalPages = 1,
  onPageChange,
  size = "sm",
  siblingCount = 1,
  ...rest
}) {
  function range(s, e) { const r=[]; for(let i=s;i<=e;i++) r.push(i); return r; }
  function pages() {
    const total = totalPages;
    if (total <= 7) return range(1, total);
    const left = Math.max(2, page - siblingCount);
    const right = Math.min(total - 1, page + siblingCount);
    const out = [1];
    if (left > 2) out.push("…");
    out.push(...range(left, right));
    if (right < total - 1) out.push("…");
    out.push(total);
    return out;
  }
  const vc = "ds-btn--ghost";
  function go(p) { if (p>=1 && p<=totalPages && p!==page) onPageChange && onPageChange(p); }
  return (
    <nav className="ds-pagination" role="navigation" aria-label="Pagination" style={{display:"inline-flex", alignItems:"center", gap:4}} {...rest}>
      <button
        type="button"
        className={cls("ds-btn", vc, `ds-btn--${size}`, "ds-btn--icon")}
        aria-label="Previous page"
        aria-disabled={page<=1 || undefined}
        disabled={page<=1}
        onClick={()=>go(page-1)}
      >
        <Icon name="chevron-left" className="ds-btn-icon" />
      </button>
      {pages().map((p, i) =>
        p === "…" ? (
          <span key={"e"+i} aria-hidden="true" style={{padding:"0 4px", color:"var(--ds-color-muted-foreground)", font:"var(--ds-text-body-sm)"}}>…</span>
        ) : (
          <button
            key={p}
            type="button"
            className={cls("ds-btn", vc, `ds-btn--${size}`)}
            aria-current={p===page?"page":undefined}
            aria-label={`Page ${p}`}
            style={{
              minWidth: "var(--ds-btn-height, 32px)",
              background: p===page ? "var(--ds-color-surface-active)" : undefined,
              fontWeight: p===page ? 600 : 500,
              border: p===page ? "1px solid var(--ds-color-border-strong)" : "1px solid transparent",
            }}
            onClick={()=>go(p)}
          >
            {p}
          </button>
        )
      )}
      <button
        type="button"
        className={cls("ds-btn", vc, `ds-btn--${size}`, "ds-btn--icon")}
        aria-label="Next page"
        aria-disabled={page>=totalPages || undefined}
        disabled={page>=totalPages}
        onClick={()=>go(page+1)}
      >
        <Icon name="chevron-right" className="ds-btn-icon" />
      </button>
    </nav>
  );
}

export default PaginationButton;
