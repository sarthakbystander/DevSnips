/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  createContext,
  useContext,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState
} from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const TRIGGER_CLASSES = "inline-flex h-9 max-w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] aria-expanded:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const MENU_CLASSES = "absolute z-40 max-h-[min(20rem,calc(100vh-2rem))] min-w-[12rem] max-w-[calc(100vw-1.5rem)] overflow-y-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
const ITEM_CLASSES = "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2 py-1.5 text-left text-[13px] leading-5 transition-colors duration-150 ease-out focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const ITEM_TONE_DEFAULT = "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)]";
const ITEM_TONE_DESTRUCTIVE = "text-[var(--ds-color-destructive)] hover:bg-[var(--ds-color-destructive-soft)] focus:bg-[var(--ds-color-destructive-soft)]";
const ICON_SLOT_CLASSES = "inline-flex shrink-0 [&_svg]:size-4";
const SHORTCUT_CLASSES = "ml-auto shrink-0 pl-6 text-xs leading-5 text-[var(--ds-color-muted-foreground)]";
const LABEL_CLASSES = "px-2 pb-1 pt-1.5 text-[11px] font-medium uppercase tracking-[0.05em] text-[var(--ds-color-muted-foreground)]";
const SEPARATOR_CLASSES = "mx-1 my-1 h-px bg-[var(--ds-color-border)]";
const PLACEMENT_CLASSES = {
  "bottom-start": "left-0 top-full mt-1.5",
  "bottom-end": "right-0 top-full mt-1.5",
  "top-start": "bottom-full left-0 mb-1.5",
  "top-end": "bottom-full right-0 mb-1.5"
};
function menuItems(content) {
  return Array.from(
    content.querySelectorAll(
      '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]'
    )
  ).filter(
    (el) => el.closest('[role="menu"]') === content && !el.hasAttribute("disabled") && el.getAttribute("aria-disabled") !== "true"
  );
}
function focusItem(items, index) {
  if (items.length === 0) return;
  const wrapped = (index % items.length + items.length) % items.length;
  items[wrapped].focus();
}
function ChevronDown({ className }) {
  return <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    focusable="false"
  >
      <path d="m6 9 6 6 6-6" />
    </svg>;
}
const DropdownMenuContext = createContext(null);
function useDropdownMenu(component) {
  const context = useContext(DropdownMenuContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <DropdownMenu>.`);
  }
  return context;
}
const MenuLevelContext = createContext(null);
function useMenuLevel() {
  const subsRef = useRef(null);
  const levelRef = useRef(null);
  if (!subsRef.current) subsRef.current = /* @__PURE__ */ new Set();
  if (!levelRef.current) {
    const subs = subsRef.current;
    levelRef.current = {
      registerSub(close) {
        subs.add(close);
        return () => {
          subs.delete(close);
        };
      },
      closeSubs(except) {
        subs.forEach((close) => {
          if (close !== except) close();
        });
      }
    };
  }
  return levelRef.current;
}
function DropdownMenu({
  open,
  defaultOpen = false,
  onOpenChange,
  placement = "bottom-start",
  className,
  children
}) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const [initialFocus, setInitialFocus] = useState("first");
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const triggerRef = useRef(null);
  const rootRef = useRef(null);
  const reactId = useId();
  const triggerId = `ds-menu-trigger${reactId}`;
  const contentId = `ds-menu${reactId}`;
  function requestOpen(next, focusTarget = "first") {
    setInitialFocus(focusTarget);
    if (!isControlled) setInternalOpen(next);
    onOpenChange?.(next);
  }
  function closeMenu({ refocus = true } = {}) {
    requestOpen(false);
    if (refocus) triggerRef.current?.focus();
  }
  useEffect(() => {
    if (!actualOpen) return;
    function onPointerDown(event) {
      if (rootRef.current && !rootRef.current.contains(event.target)) {
        if (!isControlled) setInternalOpen(false);
        onOpenChange?.(false);
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, [actualOpen]);
  const value = {
    open: actualOpen,
    initialFocus,
    requestOpen,
    closeMenu,
    triggerRef,
    rootRef,
    triggerId,
    contentId,
    placement
  };
  return <DropdownMenuContext.Provider value={value}>
      <div ref={rootRef} className={cx("relative inline-flex", className)}>
        {children}
      </div>
    </DropdownMenuContext.Provider>;
}
function DropdownMenuTrigger({
  children,
  className,
  onClick,
  onKeyDown,
  ...rest
}) {
  const context = useDropdownMenu("DropdownMenuTrigger");
  function handleClick(event) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    if (context.open) {
      context.closeMenu();
    } else {
      context.requestOpen(true, "first");
    }
  }
  function handleKeyDown(event) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    if (event.key === "ArrowDown") {
      event.preventDefault();
      context.requestOpen(true, "first");
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      context.requestOpen(true, "last");
    }
  }
  return <button
    type="button"
    ref={context.triggerRef}
    id={context.triggerId}
    aria-haspopup="menu"
    aria-expanded={context.open}
    aria-controls={context.open ? context.contentId : undefined}
    data-state={context.open ? "open" : "closed"}
    onClick={handleClick}
    onKeyDown={handleKeyDown}
    className={cx(TRIGGER_CLASSES, className)}
    {...rest}
  >
      <span className="min-w-0 truncate">{children}</span>
      <ChevronDown
    className={cx(
      "size-4 shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 ease-out motion-reduce:transition-none",
      context.open && "rotate-180"
    )}
  />
    </button>;
}
function DropdownMenuContent({
  children,
  className,
  onKeyDown,
  ...rest
}) {
  const context = useDropdownMenu("DropdownMenuContent");
  const level = useMenuLevel();
  const contentRef = useRef(null);
  const [resolved, setResolved] = useState(context.placement);
  const [measured, setMeasured] = useState(false);
  const open = context.open;
  useEffect(() => {
    if (!open) return;
    const node = contentRef.current;
    if (!node) return;
    const items = menuItems(node);
    focusItem(items, context.initialFocus === "last" ? items.length - 1 : 0);
  }, [open]);
  useLayoutEffect(() => {
    if (!open) {
      setMeasured(false);
      setResolved(context.placement);
      return;
    }
    const node = contentRef.current;
    const trigger = context.triggerRef.current;
    if (!node || !trigger) return;
    const t = trigger.getBoundingClientRect();
    const c = node.getBoundingClientRect();
    const margin = 8;
    const below = window.innerHeight - t.bottom;
    const above = t.top;
    let side = context.placement.startsWith("top") ? "top" : "bottom";
    if (side === "bottom" && below < c.height + margin && above > below) side = "top";
    else if (side === "top" && above < c.height + margin && below > above) side = "bottom";
    let align = context.placement.endsWith("end") ? "end" : "start";
    if (align === "start" && t.left + c.width > window.innerWidth - margin && t.right - c.width >= margin) {
      align = "end";
    } else if (align === "end" && t.right - c.width < margin && t.left + c.width <= window.innerWidth - margin) {
      align = "start";
    }
    setResolved(`${side}-${align}`);
    setMeasured(true);
  }, [open, context.placement]);
  function handleKeyDown(event) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    const node = contentRef.current;
    if (!node) return;
    const items = menuItems(node);
    const current = items.indexOf(document.activeElement);
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, current + 1);
        break;
      case "ArrowUp":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, current - 1);
        break;
      case "Home":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, 0);
        break;
      case "End":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, items.length - 1);
        break;
      case "Escape":
        event.preventDefault();
        event.stopPropagation();
        context.closeMenu();
        break;
      case "Tab":
        context.closeMenu({ refocus: false });
        break;
      default:
        break;
    }
  }
  function handlePointerOver(event) {
    const node = contentRef.current;
    if (!node) return;
    const item = event.target.closest(
      '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]'
    );
    if (!item || item.closest('[role="menu"]') !== node) return;
    if (!item.hasAttribute("data-ds-subtrigger")) level.closeSubs();
  }
  if (!open) return null;
  return <MenuLevelContext.Provider value={level}>
      <div
    ref={contentRef}
    id={context.contentId}
    role="menu"
    aria-labelledby={context.triggerId}
    tabIndex={-1}
    onKeyDown={handleKeyDown}
    onPointerOver={handlePointerOver}
    className={cx(MENU_CLASSES, PLACEMENT_CLASSES[resolved], !measured && "invisible", className)}
    {...rest}
  >
        {children}
      </div>
    </MenuLevelContext.Provider>;
}
function DropdownMenuItem({
  icon,
  shortcut,
  destructive = false,
  closeOnSelect = true,
  onSelect,
  onClick,
  onMouseEnter,
  className,
  children,
  ...rest
}) {
  const context = useDropdownMenu("DropdownMenuItem");
  function handleClick(event) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    onSelect?.(event);
    if (event.defaultPrevented) return;
    if (closeOnSelect) context.closeMenu();
  }
  function handleMouseEnter(event) {
    onMouseEnter?.(event);
    event.currentTarget.focus();
  }
  return <button
    type="button"
    role="menuitem"
    tabIndex={-1}
    aria-keyshortcuts={shortcut}
    onClick={handleClick}
    onMouseEnter={handleMouseEnter}
    className={cx(ITEM_CLASSES, destructive ? ITEM_TONE_DESTRUCTIVE : ITEM_TONE_DEFAULT, className)}
    {...rest}
  >
      {icon ? <span
    aria-hidden="true"
    className={cx(
      ICON_SLOT_CLASSES,
      destructive ? "text-current" : "text-[var(--ds-color-muted-foreground)]"
    )}
  >
          {icon}
        </span> : null}
      <span className="min-w-0 flex-1 truncate">{children}</span>
      {shortcut ? <span aria-hidden="true" className={SHORTCUT_CLASSES}>
          {shortcut}
        </span> : null}
    </button>;
}
function DropdownMenuLabel({ className, children, ...rest }) {
  return <div className={cx(LABEL_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function DropdownMenuGroup({ className, children, ...rest }) {
  return <div role="group" className={className} {...rest}>
      {children}
    </div>;
}
function DropdownMenuSeparator({
  className,
  ...rest
}) {
  return <div
    role="separator"
    aria-orientation="horizontal"
    className={cx(SEPARATOR_CLASSES, className)}
    {...rest}
  />;
}
const DropdownMenuSubContext = createContext(null);
function useDropdownMenuSub(component) {
  const context = useContext(DropdownMenuSubContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <DropdownMenuSub>.`);
  }
  return context;
}
function DropdownMenuSub({ children }) {
  useDropdownMenu("DropdownMenuSub");
  const [subOpen, setSubOpen] = useState(false);
  const [focusOnOpen, setFocusOnOpen] = useState(false);
  const triggerRef = useRef(null);
  const contentRef = useRef(null);
  const reactId = useId();
  const subTriggerId = `ds-subtrigger${reactId}`;
  const subContentId = `ds-submenu${reactId}`;
  const parentLevel = useContext(MenuLevelContext);
  const closeSubRef = useRef(null);
  if (closeSubRef.current === null) {
    closeSubRef.current = () => {
      setSubOpen(false);
      if (contentRef.current && contentRef.current.contains(document.activeElement)) {
        triggerRef.current?.focus();
      }
    };
  }
  const stableClose = closeSubRef.current;
  useEffect(() => {
    if (!parentLevel) return;
    return parentLevel.registerSub(stableClose);
  }, [parentLevel, stableClose]);
  function openSub(focusFirst) {
    parentLevel?.closeSubs(stableClose);
    setFocusOnOpen(focusFirst);
    setSubOpen(true);
  }
  const value = {
    open: subOpen,
    focusOnOpen,
    openSub,
    closeSub: stableClose,
    triggerRef,
    contentRef,
    subTriggerId,
    subContentId
  };
  return <DropdownMenuSubContext.Provider value={value}>
      <div className="relative">{children}</div>
    </DropdownMenuSubContext.Provider>;
}
function DropdownMenuSubTrigger({
  icon,
  children,
  className,
  onClick,
  onKeyDown,
  onMouseEnter,
  ...rest
}) {
  useDropdownMenu("DropdownMenuSubTrigger");
  const sub = useDropdownMenuSub("DropdownMenuSubTrigger");
  function handleClick(event) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    sub.openSub(true);
  }
  function handleKeyDown(event) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    if (event.key === "ArrowRight") {
      event.preventDefault();
      event.stopPropagation();
      sub.openSub(true);
    }
  }
  function handleMouseEnter(event) {
    onMouseEnter?.(event);
    event.currentTarget.focus();
    sub.openSub(false);
  }
  return <button
    type="button"
    role="menuitem"
    tabIndex={-1}
    data-ds-subtrigger
    id={sub.subTriggerId}
    ref={sub.triggerRef}
    aria-haspopup="menu"
    aria-expanded={sub.open}
    aria-controls={sub.open ? sub.subContentId : undefined}
    onClick={handleClick}
    onKeyDown={handleKeyDown}
    onMouseEnter={handleMouseEnter}
    className={cx(ITEM_CLASSES, ITEM_TONE_DEFAULT, className)}
    {...rest}
  >
      {icon ? <span aria-hidden="true" className={cx(ICON_SLOT_CLASSES, "text-[var(--ds-color-muted-foreground)]")}>
          {icon}
        </span> : null}
      <span className="min-w-0 flex-1 truncate">{children}</span>
      <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    focusable="false"
    className="ml-auto size-4 shrink-0 text-[var(--ds-color-muted-foreground)]"
  >
        <path d="m9 6 6 6-6 6" />
      </svg>
    </button>;
}
const SUBMENU_CLASSES = "absolute z-40 max-h-[min(20rem,calc(100vh-2rem))] min-w-[10rem] max-w-[calc(100vw-1.5rem)] overflow-y-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
const SUBMENU_SIDE_CLASSES = {
  right: "left-full top-0 ml-1.5",
  left: "right-full top-0 mr-1.5"
};
function DropdownMenuSubContent({
  children,
  className,
  onKeyDown,
  ...rest
}) {
  const menu = useDropdownMenu("DropdownMenuSubContent");
  const sub = useDropdownMenuSub("DropdownMenuSubContent");
  const level = useMenuLevel();
  const [side, setSide] = useState("right");
  const [measured, setMeasured] = useState(false);
  const open = sub.open;
  useEffect(() => {
    if (!open) return;
    if (!sub.focusOnOpen) return;
    const node = sub.contentRef.current;
    if (!node) return;
    focusItem(menuItems(node), 0);
  }, [open]);
  useLayoutEffect(() => {
    if (!open) {
      setMeasured(false);
      setSide("right");
      return;
    }
    const node = sub.contentRef.current;
    const trigger = sub.triggerRef.current;
    if (!node || !trigger) return;
    const t = trigger.getBoundingClientRect();
    const c = node.getBoundingClientRect();
    const margin = 8;
    const spaceRight = window.innerWidth - t.right;
    setSide(spaceRight < c.width + margin && t.left > spaceRight ? "left" : "right");
    setMeasured(true);
  }, [open]);
  function handleKeyDown(event) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    const node = sub.contentRef.current;
    if (!node) return;
    const items = menuItems(node);
    const current = items.indexOf(document.activeElement);
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, current + 1);
        break;
      case "ArrowUp":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, current - 1);
        break;
      case "Home":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, 0);
        break;
      case "End":
        event.preventDefault();
        event.stopPropagation();
        focusItem(items, items.length - 1);
        break;
      case "ArrowLeft":
        event.preventDefault();
        event.stopPropagation();
        sub.closeSub();
        break;
      case "Escape":
        event.preventDefault();
        event.stopPropagation();
        sub.closeSub();
        break;
      case "Tab":
        menu.closeMenu({ refocus: false });
        break;
      default:
        break;
    }
  }
  function handlePointerOver(event) {
    const node = sub.contentRef.current;
    if (!node) return;
    const item = event.target.closest(
      '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]'
    );
    if (!item || item.closest('[role="menu"]') !== node) return;
    if (!item.hasAttribute("data-ds-subtrigger")) level.closeSubs();
  }
  if (!open) return null;
  return <MenuLevelContext.Provider value={level}>
      <div
    ref={sub.contentRef}
    id={sub.subContentId}
    role="menu"
    aria-labelledby={sub.subTriggerId}
    tabIndex={-1}
    onKeyDown={handleKeyDown}
    onPointerOver={handlePointerOver}
    className={cx(SUBMENU_CLASSES, SUBMENU_SIDE_CLASSES[side], !measured && "invisible", className)}
    {...rest}
  >
        {children}
      </div>
    </MenuLevelContext.Provider>;
}

export { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuGroup, DropdownMenuSeparator, DropdownMenuSub, DropdownMenuSubTrigger, DropdownMenuSubContent };

export default DropdownMenu;
