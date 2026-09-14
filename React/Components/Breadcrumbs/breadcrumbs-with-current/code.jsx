/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { createContext, useContext } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const LIST_CLASSES = "m-0 flex max-w-full list-none flex-wrap items-center gap-x-1 gap-y-0.5 p-0 text-sm leading-5";
const ITEM_CLASSES = "inline-flex min-w-0 items-center gap-1.5";
const LINK_CLASSES = "inline-flex min-w-0 items-center gap-1.5 rounded-[var(--ds-radius-xs)] text-[var(--ds-color-muted-foreground)] underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const CURRENT_CLASSES = "inline-flex min-w-0 items-center gap-1.5 font-medium text-[var(--ds-color-foreground)]";
const SEPARATOR_CLASSES = "inline-flex shrink-0 select-none items-center justify-center text-[var(--ds-color-muted-foreground)] [&_svg]:size-3.5";
const ICON_CLASSES = "inline-flex shrink-0 text-[14px] [&_svg]:size-3.5";
const DEFAULT_SEPARATOR = <svg
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
const BreadcrumbsContext = createContext(null);
function useBreadcrumbs(component) {
  const context = useContext(BreadcrumbsContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Breadcrumbs>.`);
  }
  return context;
}
function Breadcrumbs({
  label = "Breadcrumb",
  separator,
  className,
  children,
  ...rest
}) {
  return <BreadcrumbsContext.Provider value={{ separator: separator ?? DEFAULT_SEPARATOR }}>
      <nav aria-label={label} className={className} {...rest}>
        {children}
      </nav>
    </BreadcrumbsContext.Provider>;
}
function BreadcrumbList({ className, children, ...rest }) {
  return <ol className={cx(LIST_CLASSES, className)} {...rest}>
      {children}
    </ol>;
}
function BreadcrumbItem({ className, children, ...rest }) {
  return <li className={cx(ITEM_CLASSES, className)} {...rest}>
      {children}
    </li>;
}
function BreadcrumbLink({ href, icon, current, className, children, ...rest }) {
  if (current) {
    return <span aria-current="page" className={cx(CURRENT_CLASSES, className)}>
        {icon ? <span aria-hidden="true" className={ICON_CLASSES}>
            {icon}
          </span> : null}
        <span className="min-w-0">{children}</span>
      </span>;
  }
  return <a href={href} className={cx(LINK_CLASSES, className)} {...rest}>
      {icon ? <span aria-hidden="true" className={ICON_CLASSES}>
          {icon}
        </span> : null}
      <span className="min-w-0">{children}</span>
    </a>;
}
function BreadcrumbCurrent({ icon, className, children, ...rest }) {
  return <span aria-current="page" className={cx(CURRENT_CLASSES, className)} {...rest}>
      {icon ? <span aria-hidden="true" className={ICON_CLASSES}>
          {icon}
        </span> : null}
      <span className="min-w-0">{children}</span>
    </span>;
}
function BreadcrumbSeparator({ className, children, ...rest }) {
  const context = useBreadcrumbs("BreadcrumbSeparator");
  return <li
    role="presentation"
    aria-hidden="true"
    className={cx(SEPARATOR_CLASSES, className)}
    {...rest}
  >
      {children ?? context.separator}
    </li>;
}

export { Breadcrumbs, BreadcrumbList, BreadcrumbItem, BreadcrumbLink, BreadcrumbCurrent, BreadcrumbSeparator };

export default Breadcrumbs;
