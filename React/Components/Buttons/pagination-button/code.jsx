/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  xs: "h-7 min-w-7 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 min-w-8 px-2.5 text-xs [&_svg]:size-[14px]",
  md: "h-9 min-w-9 px-3 text-[13px] [&_svg]:size-4",
  lg: "h-10 min-w-10 px-3 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 min-w-11 px-3.5 text-sm [&_svg]:size-5"
};
function range(s, e) {
  const r = [];
  for (let i = s; i <= e; i++) r.push(i);
  return r;
}
export function PaginationButton({
  page = 1,
  totalPages = 1,
  onPageChange,
  size = "sm",
  siblingCount = 1,
  className,
  ...rest
}) {
  function pages() {
    if (totalPages <= 7) return range(1, totalPages);
    const left = Math.max(2, page - siblingCount);
    const right = Math.min(totalPages - 1, page + siblingCount);
    const out = [1];
    if (left > 2) out.push("ellipsis");
    out.push(...range(left, right));
    if (right < totalPages - 1) out.push("ellipsis");
    out.push(totalPages);
    return out;
  }
  function go(p) {
    if (p >= 1 && p <= totalPages && p !== page) onPageChange?.(p);
  }
  const BTN = "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]";
  const GHOST = "border-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]";
  const ELL = "inline-flex items-center justify-center text-[var(--ds-color-muted-foreground)]";
  return <nav aria-label="Pagination" className={cx("inline-flex items-center gap-1", className)} {...rest}>
      <button
    type="button"
    className={cx(BTN, GHOST, SIZES[size], "px-0", page <= 1 && "pointer-events-none opacity-50")}
    aria-label="Previous page"
    aria-disabled={page <= 1 || undefined}
    disabled={page <= 1}
    onClick={() => go(page - 1)}
  >
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m15 6-6 6 6 6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </button>
      {pages().map(
    (p, i) => p === "ellipsis" ? <span key={`e${i}`} className={cx(ELL, SIZES[size])} aria-hidden="true">…</span> : <button
      key={p}
      type="button"
      className={cx(
        BTN,
        p === page ? "border-[var(--ds-color-border-strong)] bg-[var(--ds-color-surface-active)] font-semibold" : "border-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)]",
        SIZES[size]
      )}
      aria-current={p === page ? "page" : undefined}
      aria-label={`Page ${p}`}
      onClick={() => go(p)}
    >
            {p}
          </button>
  )}
      <button
    type="button"
    className={cx(BTN, GHOST, SIZES[size], "px-0", page >= totalPages && "pointer-events-none opacity-50")}
    aria-label="Next page"
    aria-disabled={page >= totalPages || undefined}
    disabled={page >= totalPages}
    onClick={() => go(page + 1)}
  >
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m9 6 6 6-6 6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </button>
    </nav>;
}

export default PaginationButton;
