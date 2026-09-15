import { createContext, useContext, useState } from "react";
import type { HTMLAttributes, LiHTMLAttributes, ReactNode } from "react";

/**
/**
 * DevSnips React Pagination — compact treatment (`size="sm"`, 32px controls)
 * for dense interfaces such as table footers and admin lists. Built on the
 * reference compound core; only the default density changes. Controls stay
 * keyboard-operable and keep visible focus rings at the smaller size.
 *
 * `<Pagination>` renders `<nav aria-label>` and owns the current page
 * (controlled via `page` + `onPageChange`, or uncontrolled via `defaultPage`).
 * `<PaginationContent>` renders the list of controls; `<PaginationItem>` one
 * position. `<PaginationLink>` is a numbered page control,
 * `<PaginationPrevious>` / `<PaginationNext>` step one page back / forward,
 * and `<PaginationEllipsis>` marks a hidden range of pages.
 *
 * Controls render as real `<a href>` when `buildHref` (or an explicit `href`)
 * is provided — normal browser navigation — and as `<button type="button">`
 * for state-driven pagination. Disabled controls render as non-interactive
 * spans with `aria-disabled`. The current page carries `aria-current="page"`.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type PaginationSize = "sm" | "md" | "lg";

const SIZES: Record<PaginationSize, string> = {
  sm: "h-8 min-w-8 gap-1 px-2 text-[13px] leading-4 [&_svg]:size-3.5",
  md: "h-9 min-w-9 gap-1.5 px-2.5 text-sm leading-5 [&_svg]:size-3.5",
  lg: "h-11 min-w-11 gap-2 px-3 text-sm leading-5 [&_svg]:size-4",
};

const CONTROL_BASE_CLASSES =
  "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] font-medium tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const CONTROL_IDLE_CLASSES =
  "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const CONTROL_ACTIVE_CLASSES =
  "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]";
const CONTROL_DISABLED_CLASSES = "pointer-events-none opacity-50";
const ICON_WRAP_CLASSES = "inline-flex shrink-0";

const CHEVRON_LEFT = (
  <svg
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
  </svg>
);
const CHEVRON_RIGHT = (
  <svg
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
  </svg>
);

function clampPage(page: number, totalPages: number): number {
  return Math.min(Math.max(1, page), Math.max(1, totalPages));
}

interface PaginationContextValue {
  page: number;
  totalPages: number;
  setPage: (page: number) => void;
  size: PaginationSize;
  disabled: boolean;
  buildHref?: (page: number) => string;
}

const PaginationContext = createContext<PaginationContextValue | null>(null);

function usePagination(component: string): PaginationContextValue {
  const context = useContext(PaginationContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Pagination>.`);
  }
  return context;
}

export interface PaginationProps extends Omit<HTMLAttributes<HTMLElement>, "onChange"> {
  /** Current page, 1-based (controlled). Omit to run uncontrolled. */
  page?: number;
  /** Initial page, 1-based (uncontrolled). */
  defaultPage?: number;
  /** Total number of pages (required). */
  totalPages: number;
  /** Called with the next 1-based page whenever it changes. */
  onPageChange?: (page: number) => void;
  /** Builds a URL for a page; controls render as real anchors when set. */
  buildHref?: (page: number) => string;
  /** Control density. */
  size?: PaginationSize;
  /** Disable every control in the navigation. */
  disabled?: boolean;
  /** Accessible label for the navigation landmark. */
  label?: string;
  className?: string;
  children?: ReactNode;
}

export function Pagination({
  page,
  defaultPage = 1,
  totalPages,
  onPageChange,
  buildHref,
  size = "sm",
  disabled = false,
  label = "Pagination",
  className,
  children,
  ...rest
}: PaginationProps) {
  const isControlled = page !== undefined;
  const [internal, setInternal] = useState(defaultPage);
  const current = clampPage(isControlled ? page : internal, totalPages);
  function setPage(next: number) {
    const clamped = clampPage(next, totalPages);
    if (clamped === current) return;
    if (!isControlled) {
      setInternal(clamped);
    }
    onPageChange?.(clamped);
  }
  return (
    <PaginationContext.Provider
      value={{ page: current, totalPages, setPage, size, disabled, buildHref }}
    >
      <nav aria-label={label} className={className} {...rest}>
        {children}
      </nav>
    </PaginationContext.Provider>
  );
}

export interface PaginationContentProps extends HTMLAttributes<HTMLUListElement> {
  className?: string;
  children?: ReactNode;
}

export function PaginationContent({ className, children, ...rest }: PaginationContentProps) {
  return (
    <ul
      className={cx("m-0 flex max-w-full list-none flex-wrap items-center gap-1 p-0", className)}
      {...rest}
    >
      {children}
    </ul>
  );
}

export interface PaginationItemProps extends LiHTMLAttributes<HTMLLIElement> {
  className?: string;
  children?: ReactNode;
}

export function PaginationItem({ className, children, ...rest }: PaginationItemProps) {
  return (
    <li className={cx("inline-flex", className)} {...rest}>
      {children}
    </li>
  );
}

export interface PaginationLinkProps {
  /** 1-based page number this control navigates to. */
  page: number;
  /** Explicit URL for URL-based pagination (overrides `buildHref`). */
  href?: string;
  /** Disable this page control (renders a non-interactive span). */
  disabled?: boolean;
  className?: string;
  children?: ReactNode;
  "aria-label"?: string;
}

export function PaginationLink({
  page,
  href,
  disabled,
  className,
  children,
  "aria-label": ariaLabel,
}: PaginationLinkProps) {
  const context = usePagination("PaginationLink");
  const isCurrent = page === context.page;
  const isDisabled = Boolean(disabled) || context.disabled;
  const label = ariaLabel ?? (isCurrent ? `Page ${page}` : `Go to page ${page}`);
  const classes = cx(
    CONTROL_BASE_CLASSES,
    SIZES[context.size],
    isCurrent ? CONTROL_ACTIVE_CLASSES : CONTROL_IDLE_CLASSES,
    isDisabled && CONTROL_DISABLED_CLASSES,
    className,
  );
  const url = href ?? context.buildHref?.(page);
  if (isDisabled) {
    return (
      <span
        aria-disabled="true"
        aria-label={label}
        aria-current={isCurrent ? "page" : undefined}
        className={classes}
      >
        {children ?? page}
      </span>
    );
  }
  if (url !== undefined) {
    return (
      <a href={url} aria-label={label} aria-current={isCurrent ? "page" : undefined} className={classes}>
        {children ?? page}
      </a>
    );
  }
  return (
    <button
      type="button"
      onClick={() => context.setPage(page)}
      aria-label={label}
      aria-current={isCurrent ? "page" : undefined}
      className={classes}
    >
      {children ?? page}
    </button>
  );
}

interface StepControlProps {
  direction: "previous" | "next";
  href?: string;
  label: string;
  className?: string;
}

function StepControl({ direction, href, label, className }: StepControlProps) {
  const context = usePagination(direction === "previous" ? "PaginationPrevious" : "PaginationNext");
  const target = direction === "previous" ? context.page - 1 : context.page + 1;
  const isDisabled = context.disabled || target < 1 || target > context.totalPages;
  const classes = cx(
    CONTROL_BASE_CLASSES,
    SIZES[context.size],
    CONTROL_IDLE_CLASSES,
    isDisabled && CONTROL_DISABLED_CLASSES,
    className,
  );
  const content =
    direction === "previous" ? (
      <>
        <span aria-hidden="true" className={ICON_WRAP_CLASSES}>
          {CHEVRON_LEFT}
        </span>
        <span>{label}</span>
      </>
    ) : (
      <>
        <span>{label}</span>
        <span aria-hidden="true" className={ICON_WRAP_CLASSES}>
          {CHEVRON_RIGHT}
        </span>
      </>
    );
  const url = href ?? context.buildHref?.(target);
  if (isDisabled) {
    return (
      <span aria-disabled="true" className={classes}>
        {content}
      </span>
    );
  }
  if (url !== undefined) {
    return (
      <a href={url} className={classes}>
        {content}
      </a>
    );
  }
  return (
    <button type="button" onClick={() => context.setPage(target)} className={classes}>
      {content}
    </button>
  );
}

export interface PaginationPreviousProps {
  /** Explicit URL for the previous page (overrides `buildHref`). */
  href?: string;
  /** Visible label (also the accessible name). */
  label?: string;
  className?: string;
}

export function PaginationPrevious({ href, label = "Previous", className }: PaginationPreviousProps) {
  return <StepControl direction="previous" href={href} label={label} className={className} />;
}

export interface PaginationNextProps {
  /** Explicit URL for the next page (overrides `buildHref`). */
  href?: string;
  /** Visible label (also the accessible name). */
  label?: string;
  className?: string;
}

export function PaginationNext({ href, label = "Next", className }: PaginationNextProps) {
  return <StepControl direction="next" href={href} label={label} className={className} />;
}

export interface PaginationEllipsisProps {
  className?: string;
}

export function PaginationEllipsis({ className }: PaginationEllipsisProps) {
  const context = usePagination("PaginationEllipsis");
  return (
    <span
      className={cx(
        "inline-flex select-none items-center justify-center text-[var(--ds-color-muted-foreground)]",
        SIZES[context.size],
        className,
      )}
    >
      <span aria-hidden="true">…</span>
      <span className="sr-only">More pages</span>
    </span>
  );
}

export default Pagination;
