import { createContext, useContext } from "react";
import type {
  AnchorHTMLAttributes,
  HTMLAttributes,
  LiHTMLAttributes,
  ReactNode,
} from "react";

/**
 * DevSnips React Breadcrumbs — With Separator.
 *
 * The separator is structural decoration: each `<BreadcrumbSeparator>`
 * renders an aria-hidden `role="presentation"` list item. Set one
 * `separator` ReactNode on `<Breadcrumbs>` to restyle every separator at
 * once, or pass children to an individual `<BreadcrumbSeparator>` to
 * override it in place. The default is a small chevron.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const LIST_CLASSES =
  "m-0 flex max-w-full list-none flex-wrap items-center gap-x-1 gap-y-0.5 p-0 text-sm leading-5";
const ITEM_CLASSES = "inline-flex min-w-0 items-center gap-1.5";
const LINK_CLASSES =
  "inline-flex min-w-0 items-center gap-1.5 rounded-[var(--ds-radius-xs)] text-[var(--ds-color-muted-foreground)] underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const CURRENT_CLASSES =
  "inline-flex min-w-0 items-center gap-1.5 font-medium text-[var(--ds-color-foreground)]";
const SEPARATOR_CLASSES =
  "inline-flex shrink-0 select-none items-center justify-center text-[var(--ds-color-muted-foreground)] [&_svg]:size-3.5";
const ICON_CLASSES = "inline-flex shrink-0 text-[14px] [&_svg]:size-3.5";

const DEFAULT_SEPARATOR = (
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

interface BreadcrumbsContextValue {
  separator: ReactNode;
}

const BreadcrumbsContext = createContext<BreadcrumbsContextValue | null>(null);

function useBreadcrumbs(component: string): BreadcrumbsContextValue {
  const context = useContext(BreadcrumbsContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Breadcrumbs>.`);
  }
  return context;
}

export interface BreadcrumbsProps extends HTMLAttributes<HTMLElement> {
  /** Accessible label for the navigation landmark. */
  label?: string;
  /** Default separator content used by every `<BreadcrumbSeparator>` without children. */
  separator?: ReactNode;
  className?: string;
  children?: ReactNode;
}

export function Breadcrumbs({
  label = "Breadcrumb",
  separator,
  className,
  children,
  ...rest
}: BreadcrumbsProps) {
  return (
    <BreadcrumbsContext.Provider value={{ separator: separator ?? DEFAULT_SEPARATOR }}>
      <nav aria-label={label} className={className} {...rest}>
        {children}
      </nav>
    </BreadcrumbsContext.Provider>
  );
}

export interface BreadcrumbListProps extends HTMLAttributes<HTMLOListElement> {
  className?: string;
  children?: ReactNode;
}

export function BreadcrumbList({ className, children, ...rest }: BreadcrumbListProps) {
  return (
    <ol className={cx(LIST_CLASSES, className)} {...rest}>
      {children}
    </ol>
  );
}

export interface BreadcrumbItemProps extends LiHTMLAttributes<HTMLLIElement> {
  className?: string;
  children?: ReactNode;
}

export function BreadcrumbItem({ className, children, ...rest }: BreadcrumbItemProps) {
  return (
    <li className={cx(ITEM_CLASSES, className)} {...rest}>
      {children}
    </li>
  );
}

export interface BreadcrumbLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  /** Destination URL — rendered as a real anchor with normal browser navigation. */
  href: string;
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  className?: string;
  children?: ReactNode;
}

export function BreadcrumbLink({ href, icon, className, children, ...rest }: BreadcrumbLinkProps) {
  return (
    <a href={href} className={cx(LINK_CLASSES, className)} {...rest}>
      {icon ? (
        <span aria-hidden="true" className={ICON_CLASSES}>
          {icon}
        </span>
      ) : null}
      <span className="min-w-0">{children}</span>
    </a>
  );
}

export interface BreadcrumbCurrentProps extends HTMLAttributes<HTMLSpanElement> {
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  className?: string;
  children?: ReactNode;
}

export function BreadcrumbCurrent({ icon, className, children, ...rest }: BreadcrumbCurrentProps) {
  return (
    <span aria-current="page" className={cx(CURRENT_CLASSES, className)} {...rest}>
      {icon ? (
        <span aria-hidden="true" className={ICON_CLASSES}>
          {icon}
        </span>
      ) : null}
      <span className="min-w-0">{children}</span>
    </span>
  );
}

export interface BreadcrumbSeparatorProps extends LiHTMLAttributes<HTMLLIElement> {
  className?: string;
  children?: ReactNode;
}

export function BreadcrumbSeparator({ className, children, ...rest }: BreadcrumbSeparatorProps) {
  const context = useBreadcrumbs("BreadcrumbSeparator");
  return (
    <li
      role="presentation"
      aria-hidden="true"
      className={cx(SEPARATOR_CLASSES, className)}
      {...rest}
    >
      {children ?? context.separator}
    </li>
  );
}

export default Breadcrumbs;
