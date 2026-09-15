/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { createContext, useContext, useEffect, useRef, useState } from "react";
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
function BreadcrumbLink({ href, icon, className, children, ...rest }) {
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
const DROPDOWN_TRIGGER_CLASSES = "inline-flex min-w-0 items-center gap-1 rounded-[var(--ds-radius-xs)] text-[var(--ds-color-muted-foreground)] underline-offset-4 transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] aria-expanded:text-[var(--ds-color-foreground)] motion-reduce:transition-none";
const MENU_CLASSES = "absolute left-0 top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
const MENU_ITEM_CLASSES = "flex w-full items-center gap-1.5 rounded-[var(--ds-radius-sm)] px-2 py-1.5 text-[13px] leading-5 text-[var(--ds-color-foreground)] no-underline transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
function BreadcrumbDropdown({
  label,
  items,
  className,
  ...rest
}) {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef(null);
  const itemRefs = useRef([]);
  const containerRef = useRef(null);
  useEffect(() => {
    if (!open) return;
    function onDown(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setOpen(false);
      }
    }
    function onKey(event) {
      if (event.key === "Escape") {
        setOpen(false);
        triggerRef.current?.focus();
      }
      if (event.key === "Tab") {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);
  function openMenu(focusIndex) {
    setOpen(true);
    setTimeout(() => itemRefs.current[focusIndex]?.focus(), 0);
  }
  function onTriggerKeyDown(event) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      open ? itemRefs.current[0]?.focus() : openMenu(0);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      open ? itemRefs.current[items.length - 1]?.focus() : openMenu(items.length - 1);
    }
  }
  function onItemKeyDown(event, index) {
    const count = items.length;
    if (event.key === "ArrowDown") {
      event.preventDefault();
      itemRefs.current[(index + 1) % count]?.focus();
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      itemRefs.current[(index - 1 + count) % count]?.focus();
    } else if (event.key === "Home") {
      event.preventDefault();
      itemRefs.current[0]?.focus();
    } else if (event.key === "End") {
      event.preventDefault();
      itemRefs.current[count - 1]?.focus();
    }
  }
  return <li ref={containerRef} className={cx("relative inline-flex min-w-0 items-center gap-1.5", className)}>
      <button
    type="button"
    ref={triggerRef}
    aria-haspopup="menu"
    aria-expanded={open}
    onClick={() => open ? setOpen(false) : openMenu(0)}
    onKeyDown={onTriggerKeyDown}
    className={DROPDOWN_TRIGGER_CLASSES}
    {...rest}
  >
        <span className="min-w-0">{label}</span>
        <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    focusable="false"
    className={cx(
      "size-3.5 shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none",
      open && "rotate-180"
    )}
  >
          <path d="m6 9 6 6 6-6" />
        </svg>
      </button>
      {open ? <div role="menu" aria-label={label} className={MENU_CLASSES}>
          {items.map((item, index) => <a
    key={item.href}
    ref={(el) => {
      itemRefs.current[index] = el;
    }}
    role="menuitem"
    tabIndex={-1}
    href={item.href}
    aria-current={item.current ? "page" : undefined}
    className={cx(MENU_ITEM_CLASSES, item.current && "font-medium")}
    onClick={() => setOpen(false)}
    onKeyDown={(event) => onItemKeyDown(event, index)}
  >
              {item.icon ? <span aria-hidden="true" className={ICON_CLASSES}>
                  {item.icon}
                </span> : null}
              <span className="min-w-0 flex-1">{item.label}</span>
            </a>)}
        </div> : null}
    </li>;
}

export { Breadcrumbs, BreadcrumbList, BreadcrumbItem, BreadcrumbLink, BreadcrumbCurrent, BreadcrumbSeparator, BreadcrumbDropdown };

export default Breadcrumbs;
