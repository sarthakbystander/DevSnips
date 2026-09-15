/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { createContext, useContext, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  sm: "h-8 min-w-8 gap-1 px-2 text-[13px] leading-4 [&_svg]:size-3.5",
  md: "h-9 min-w-9 gap-1.5 px-2.5 text-sm leading-5 [&_svg]:size-3.5",
  lg: "h-11 min-w-11 gap-2 px-3 text-sm leading-5 [&_svg]:size-4"
};
const CONTROL_BASE_CLASSES = "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] font-medium tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const CONTROL_IDLE_CLASSES = "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const CONTROL_ACTIVE_CLASSES = "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]";
const CONTROL_DISABLED_CLASSES = "pointer-events-none opacity-50";
const ICON_WRAP_CLASSES = "inline-flex shrink-0";
const CHEVRON_LEFT = <svg
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  strokeWidth={1.75}
  strokeLinecap="round"
  strokeLinejoin="round"
  aria-hidden="true"
  focusable="false"
>
    <path d="m15 6-6 6 6 6" />
  </svg>;
const CHEVRON_RIGHT = <svg
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  strokeWidth={1.75}
  strokeLinecap="round"
  strokeLinejoin="round"
  aria-hidden="true"
  focusable="false"
>
    <path d="m9 6 6 6-6 6" />
  </svg>;
function clampPage(page, totalPages) {
  return Math.min(Math.max(1, page), Math.max(1, totalPages));
}
const PaginationContext = createContext(null);
function usePagination(component) {
  const context = useContext(PaginationContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Pagination>.`);
  }
  return context;
}
function Pagination({
  page,
  defaultPage = 1,
  totalPages,
  onPageChange,
  buildHref,
  size = "md",
  disabled = false,
  label = "Pagination",
  className,
  children,
  ...rest
}) {
  const isControlled = page !== undefined;
  const [internal, setInternal] = useState(defaultPage);
  const current = clampPage(isControlled ? page : internal, totalPages);
  function setPage(next) {
    const clamped = clampPage(next, totalPages);
    if (clamped === current) return;
    if (!isControlled) {
      setInternal(clamped);
    }
    onPageChange?.(clamped);
  }
  return <PaginationContext.Provider
    value={{ page: current, totalPages, setPage, size, disabled, buildHref }}
  >
      <nav aria-label={label} className={className} {...rest}>
        {children}
      </nav>
    </PaginationContext.Provider>;
}
function PaginationContent({ className, children, ...rest }) {
  return <ul
    className={cx("m-0 flex max-w-full list-none flex-wrap items-center gap-1 p-0", className)}
    {...rest}
  >
      {children}
    </ul>;
}
function PaginationItem({ className, children, ...rest }) {
  return <li className={cx("inline-flex", className)} {...rest}>
      {children}
    </li>;
}
function PaginationLink({
  page,
  href,
  disabled,
  className,
  children,
  "aria-label": ariaLabel
}) {
  const context = usePagination("PaginationLink");
  const isCurrent = page === context.page;
  const isDisabled = Boolean(disabled) || context.disabled;
  const label = ariaLabel ?? (isCurrent ? `Page ${page}` : `Go to page ${page}`);
  const classes = cx(
    CONTROL_BASE_CLASSES,
    SIZES[context.size],
    isCurrent ? CONTROL_ACTIVE_CLASSES : CONTROL_IDLE_CLASSES,
    isDisabled && CONTROL_DISABLED_CLASSES,
    className
  );
  const url = href ?? context.buildHref?.(page);
  if (isDisabled) {
    return <span
      aria-disabled="true"
      aria-label={label}
      aria-current={isCurrent ? "page" : undefined}
      className={classes}
    >
        {children ?? page}
      </span>;
  }
  if (url !== undefined) {
    return <a href={url} aria-label={label} aria-current={isCurrent ? "page" : undefined} className={classes}>
        {children ?? page}
      </a>;
  }
  return <button
    type="button"
    onClick={() => context.setPage(page)}
    aria-label={label}
    aria-current={isCurrent ? "page" : undefined}
    className={classes}
  >
      {children ?? page}
    </button>;
}
function StepControl({ direction, href, label, className }) {
  const context = usePagination(direction === "previous" ? "PaginationPrevious" : "PaginationNext");
  const target = direction === "previous" ? context.page - 1 : context.page + 1;
  const isDisabled = context.disabled || target < 1 || target > context.totalPages;
  const classes = cx(
    CONTROL_BASE_CLASSES,
    SIZES[context.size],
    CONTROL_IDLE_CLASSES,
    isDisabled && CONTROL_DISABLED_CLASSES,
    className
  );
  const content = direction === "previous" ? <>
        <span aria-hidden="true" className={ICON_WRAP_CLASSES}>
          {CHEVRON_LEFT}
        </span>
        <span>{label}</span>
      </> : <>
        <span>{label}</span>
        <span aria-hidden="true" className={ICON_WRAP_CLASSES}>
          {CHEVRON_RIGHT}
        </span>
      </>;
  const url = href ?? context.buildHref?.(target);
  if (isDisabled) {
    return <span aria-disabled="true" className={classes}>
        {content}
      </span>;
  }
  if (url !== undefined) {
    return <a href={url} className={classes}>
        {content}
      </a>;
  }
  return <button type="button" onClick={() => context.setPage(target)} className={classes}>
      {content}
    </button>;
}
function PaginationPrevious({ href, label = "Previous", className }) {
  return <StepControl direction="previous" href={href} label={label} className={className} />;
}
function PaginationNext({ href, label = "Next", className }) {
  return <StepControl direction="next" href={href} label={label} className={className} />;
}
function PaginationEllipsis({ className }) {
  const context = usePagination("PaginationEllipsis");
  return <span
    className={cx(
      "inline-flex select-none items-center justify-center text-[var(--ds-color-muted-foreground)]",
      SIZES[context.size],
      className
    )}
  >
      <span aria-hidden="true">…</span>
      <span className="sr-only">More pages</span>
    </span>;
}
function PaginationStatus({ format, className, ...rest }) {
  const context = usePagination("PaginationStatus");
  const text = format ? format(context.page, context.totalPages) : `Page ${context.page} of ${context.totalPages}`;
  return <span
    aria-live="polite"
    className={cx(
      "inline-flex select-none items-center whitespace-nowrap px-2 text-sm tabular-nums text-[var(--ds-color-muted-foreground)]",
      className
    )}
    {...rest}
  >
      {text}
    </span>;
}

export { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationPrevious, PaginationNext, PaginationEllipsis, PaginationStatus };

export default Pagination;
