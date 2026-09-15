import {
  createContext,
  useContext,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  KeyboardEvent as ReactKeyboardEvent,
  MouseEvent as ReactMouseEvent,
  ReactNode,
  RefObject,
} from "react";

/**
 * DevSnips React Dropdown Menu — Submenu.
 *
 * The shared menu core plus `<DropdownMenuSub>` + `<DropdownMenuSubTrigger>`
 * + `<DropdownMenuSubContent>`: one nested menu level with correct menu
 * semantics. ArrowRight / Enter / Space open the submenu (focus to first
 * item), ArrowLeft / Escape close only the submenu (focus back to the sub
 * trigger), hovering opens without stealing focus, and the panel flips to
 * the left side when the right side would leave the viewport.
 */


function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type DropdownMenuPlacement = "bottom-start" | "bottom-end" | "top-start" | "top-end";

const TRIGGER_CLASSES =
  "inline-flex h-9 max-w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] aria-expanded:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const MENU_CLASSES =
  "absolute z-40 max-h-[min(20rem,calc(100vh-2rem))] min-w-[12rem] max-w-[calc(100vw-1.5rem)] overflow-y-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
// Layout/interaction only — the text/hover/focus tone is composed per item
// kind so the destructive tone never conflicts with the default tone.
const ITEM_CLASSES =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2 py-1.5 text-left text-[13px] leading-5 transition-colors duration-150 ease-out focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const ITEM_TONE_DEFAULT =
  "text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)]";
const ITEM_TONE_DESTRUCTIVE =
  "text-[var(--ds-color-destructive)] hover:bg-[var(--ds-color-destructive-soft)] focus:bg-[var(--ds-color-destructive-soft)]";
const ICON_SLOT_CLASSES = "inline-flex shrink-0 [&_svg]:size-4";
const SHORTCUT_CLASSES =
  "ml-auto shrink-0 pl-6 text-xs leading-5 text-[var(--ds-color-muted-foreground)]";
const LABEL_CLASSES =
  "px-2 pb-1 pt-1.5 text-[11px] font-medium uppercase tracking-[0.05em] text-[var(--ds-color-muted-foreground)]";
const SEPARATOR_CLASSES = "mx-1 my-1 h-px bg-[var(--ds-color-border)]";

const PLACEMENT_CLASSES: Record<DropdownMenuPlacement, string> = {
  "bottom-start": "left-0 top-full mt-1.5",
  "bottom-end": "right-0 top-full mt-1.5",
  "top-start": "bottom-full left-0 mb-1.5",
  "top-end": "bottom-full right-0 mb-1.5",
};

/** Items owned directly by `content` (excludes items of nested open submenus). */
function menuItems(content: HTMLElement): HTMLElement[] {
  return Array.from(
    content.querySelectorAll<HTMLElement>(
      '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]',
    ),
  ).filter(
    (el) =>
      el.closest('[role="menu"]') === content &&
      !el.hasAttribute("disabled") &&
      el.getAttribute("aria-disabled") !== "true",
  );
}

function focusItem(items: HTMLElement[], index: number): void {
  if (items.length === 0) return;
  const wrapped = ((index % items.length) + items.length) % items.length;
  items[wrapped].focus();
}

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg
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
    </svg>
  );
}

/* ------------------------------------------------------------------------ */
/* Root context                                                              */
/* ------------------------------------------------------------------------ */

interface DropdownMenuContextValue {
  open: boolean;
  initialFocus: "first" | "last";
  requestOpen(next: boolean, focusTarget?: "first" | "last"): void;
  closeMenu(options?: { refocus?: boolean }): void;
  triggerRef: RefObject<HTMLButtonElement>;
  rootRef: RefObject<HTMLDivElement>;
  triggerId: string;
  contentId: string;
  placement: DropdownMenuPlacement;
}

const DropdownMenuContext = createContext<DropdownMenuContextValue | null>(null);

function useDropdownMenu(component: string): DropdownMenuContextValue {
  const context = useContext(DropdownMenuContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <DropdownMenu>.`);
  }
  return context;
}

/**
 * Registry of open submenus at one menu level, so pointer interaction with a
 * sibling item can close the open submenu at that level. Provided by every
 * menu panel (`DropdownMenuContent`, and `DropdownMenuSubContent` in the
 * submenu variant).
 */
interface MenuLevelContextValue {
  registerSub(close: () => void): () => void;
  closeSubs(except?: () => void): void;
}

const MenuLevelContext = createContext<MenuLevelContextValue | null>(null);

function useMenuLevel(): MenuLevelContextValue {
  const subsRef = useRef<Set<() => void> | null>(null);
  const levelRef = useRef<MenuLevelContextValue | null>(null);
  if (!subsRef.current) subsRef.current = new Set();
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
      },
    };
  }
  return levelRef.current;
}

/* ------------------------------------------------------------------------ */
/* DropdownMenu (root)                                                       */
/* ------------------------------------------------------------------------ */

export interface DropdownMenuProps {
  /** Open state (controlled). */
  open?: boolean;
  /** Initial open state (uncontrolled). */
  defaultOpen?: boolean;
  /** Called whenever the menu requests to open or close. */
  onOpenChange?: (open: boolean) => void;
  /** Preferred placement relative to the trigger; flips to stay in the viewport. */
  placement?: DropdownMenuPlacement;
  className?: string;
  children?: ReactNode;
}

export function DropdownMenu({
  open,
  defaultOpen = false,
  onOpenChange,
  placement = "bottom-start",
  className,
  children,
}: DropdownMenuProps) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const [initialFocus, setInitialFocus] = useState<"first" | "last">("first");
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const triggerRef = useRef<HTMLButtonElement>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const reactId = useId();
  const triggerId = `ds-menu-trigger${reactId}`;
  const contentId = `ds-menu${reactId}`;

  function requestOpen(next: boolean, focusTarget: "first" | "last" = "first") {
    setInitialFocus(focusTarget);
    if (!isControlled) setInternalOpen(next);
    onOpenChange?.(next);
  }

  function closeMenu({ refocus = true }: { refocus?: boolean } = {}) {
    requestOpen(false);
    if (refocus) triggerRef.current?.focus();
  }

  // Outside pointer interaction closes the tree; listeners exist only while
  // open and are removed as soon as it closes.
  useEffect(() => {
    if (!actualOpen) return;
    function onPointerDown(event: PointerEvent) {
      if (rootRef.current && !rootRef.current.contains(event.target as Node)) {
        if (!isControlled) setInternalOpen(false);
        onOpenChange?.(false);
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualOpen]);

  const value: DropdownMenuContextValue = {
    open: actualOpen,
    initialFocus,
    requestOpen,
    closeMenu,
    triggerRef,
    rootRef,
    triggerId,
    contentId,
    placement,
  };

  return (
    <DropdownMenuContext.Provider value={value}>
      <div ref={rootRef} className={cx("relative inline-flex", className)}>
        {children}
      </div>
    </DropdownMenuContext.Provider>
  );
}

export default DropdownMenu;

/* ------------------------------------------------------------------------ */
/* DropdownMenuTrigger                                                       */
/* ------------------------------------------------------------------------ */

export interface DropdownMenuTriggerProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  children?: ReactNode;
}

export function DropdownMenuTrigger({
  children,
  className,
  onClick,
  onKeyDown,
  ...rest
}: DropdownMenuTriggerProps) {
  const context = useDropdownMenu("DropdownMenuTrigger");

  function handleClick(event: ReactMouseEvent<HTMLButtonElement>) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    if (context.open) {
      context.closeMenu();
    } else {
      context.requestOpen(true, "first");
    }
  }

  function handleKeyDown(event: ReactKeyboardEvent<HTMLButtonElement>) {
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

  return (
    <button
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
          context.open && "rotate-180",
        )}
      />
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* DropdownMenuContent                                                       */
/* ------------------------------------------------------------------------ */

export interface DropdownMenuContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function DropdownMenuContent({
  children,
  className,
  onKeyDown,
  ...rest
}: DropdownMenuContentProps) {
  const context = useDropdownMenu("DropdownMenuContent");
  const level = useMenuLevel();
  const contentRef = useRef<HTMLDivElement>(null);
  const [resolved, setResolved] = useState<DropdownMenuPlacement>(context.placement);
  const [measured, setMeasured] = useState(false);

  const open = context.open;

  // Move focus into the menu when it opens (first item, or last when the
  // trigger was invoked with ArrowUp).
  useEffect(() => {
    if (!open) return;
    const node = contentRef.current;
    if (!node) return;
    const items = menuItems(node);
    focusItem(items, context.initialFocus === "last" ? items.length - 1 : 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Measure against the viewport and flip the placement when the preferred
  // side/alignment would overflow. Runs before paint, so the flip never
  // flashes; the panel stays `invisible` until the first measurement.
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
    let side: "top" | "bottom" = context.placement.startsWith("top") ? "top" : "bottom";
    if (side === "bottom" && below < c.height + margin && above > below) side = "top";
    else if (side === "top" && above < c.height + margin && below > above) side = "bottom";
    let align: "start" | "end" = context.placement.endsWith("end") ? "end" : "start";
    if (align === "start" && t.left + c.width > window.innerWidth - margin && t.right - c.width >= margin) {
      align = "end";
    } else if (align === "end" && t.right - c.width < margin && t.left + c.width <= window.innerWidth - margin) {
      align = "start";
    }
    setResolved(`${side}-${align}`);
    setMeasured(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, context.placement]);

  function handleKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    const node = contentRef.current;
    if (!node) return;
    const items = menuItems(node);
    const current = items.indexOf(document.activeElement as HTMLElement);
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
        // Let focus leave naturally; close without stealing it back.
        context.closeMenu({ refocus: false });
        break;
      default:
        break;
    }
  }

  // Hovering a plain item closes the open submenu at this level.
  function handlePointerOver(event: ReactMouseEvent<HTMLDivElement>) {
    const node = contentRef.current;
    if (!node) return;
    const item = (event.target as HTMLElement).closest<HTMLElement>(
      '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]',
    );
    if (!item || item.closest('[role="menu"]') !== node) return;
    if (!item.hasAttribute("data-ds-subtrigger")) level.closeSubs();
  }

  if (!open) return null;

  return (
    <MenuLevelContext.Provider value={level}>
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
    </MenuLevelContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* DropdownMenuItem                                                          */
/* ------------------------------------------------------------------------ */

export interface DropdownMenuItemProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  /** Informational keyboard shortcut shown at the trailing edge (aria-hidden; exposed via aria-keyshortcuts). */
  shortcut?: string;
  /** Destructive action styling via the semantic destructive token. */
  destructive?: boolean;
  /** Whether activating the item closes the menu (default true). */
  closeOnSelect?: boolean;
  /** Called when the item is activated, before the menu closes. Call `event.preventDefault()` to keep the menu open. */
  onSelect?: (event: ReactMouseEvent<HTMLButtonElement>) => void;
  children?: ReactNode;
}

export function DropdownMenuItem({
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
}: DropdownMenuItemProps) {
  const context = useDropdownMenu("DropdownMenuItem");

  function handleClick(event: ReactMouseEvent<HTMLButtonElement>) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    onSelect?.(event);
    if (event.defaultPrevented) return;
    if (closeOnSelect) context.closeMenu();
  }

  function handleMouseEnter(event: ReactMouseEvent<HTMLButtonElement>) {
    onMouseEnter?.(event);
    event.currentTarget.focus();
  }

  return (
    <button
      type="button"
      role="menuitem"
      tabIndex={-1}
      aria-keyshortcuts={shortcut}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      className={cx(ITEM_CLASSES, destructive ? ITEM_TONE_DESTRUCTIVE : ITEM_TONE_DEFAULT, className)}
      {...rest}
    >
      {icon ? (
        <span
          aria-hidden="true"
          className={cx(
            ICON_SLOT_CLASSES,
            destructive ? "text-current" : "text-[var(--ds-color-muted-foreground)]",
          )}
        >
          {icon}
        </span>
      ) : null}
      <span className="min-w-0 flex-1 truncate">{children}</span>
      {shortcut ? (
        <span aria-hidden="true" className={SHORTCUT_CLASSES}>
          {shortcut}
        </span>
      ) : null}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* DropdownMenuLabel / DropdownMenuGroup / DropdownMenuSeparator             */
/* ------------------------------------------------------------------------ */

export interface DropdownMenuLabelProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function DropdownMenuLabel({ className, children, ...rest }: DropdownMenuLabelProps) {
  return (
    <div className={cx(LABEL_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export interface DropdownMenuGroupProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function DropdownMenuGroup({ className, children, ...rest }: DropdownMenuGroupProps) {
  return (
    <div role="group" className={className} {...rest}>
      {children}
    </div>
  );
}

export function DropdownMenuSeparator({
  className,
  ...rest
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      role="separator"
      aria-orientation="horizontal"
      className={cx(SEPARATOR_CLASSES, className)}
      {...rest}
    />
  );
}

/* ------------------------------------------------------------------------ */
/* DropdownMenuSub / DropdownMenuSubTrigger / DropdownMenuSubContent         */
/* ------------------------------------------------------------------------ */

interface DropdownMenuSubContextValue {
  open: boolean;
  focusOnOpen: boolean;
  openSub(focusFirst: boolean): void;
  closeSub(): void;
  triggerRef: RefObject<HTMLButtonElement>;
  contentRef: RefObject<HTMLDivElement>;
  subTriggerId: string;
  subContentId: string;
}

const DropdownMenuSubContext = createContext<DropdownMenuSubContextValue | null>(null);

function useDropdownMenuSub(component: string): DropdownMenuSubContextValue {
  const context = useContext(DropdownMenuSubContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <DropdownMenuSub>.`);
  }
  return context;
}

export interface DropdownMenuSubProps {
  children?: ReactNode;
}

/**
 * A nested menu level. Owns its open state and registers a stable close
 * callback with the parent menu level, so pointer interaction with a sibling
 * item closes the open submenu. Closing never strands focus inside a removed
 * panel — it falls back to the sub trigger.
 */
export function DropdownMenuSub({ children }: DropdownMenuSubProps) {
  useDropdownMenu("DropdownMenuSub");
  const [subOpen, setSubOpen] = useState(false);
  const [focusOnOpen, setFocusOnOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const reactId = useId();
  const subTriggerId = `ds-subtrigger${reactId}`;
  const subContentId = `ds-submenu${reactId}`;
  const parentLevel = useContext(MenuLevelContext);

  const closeSubRef = useRef<(() => void) | null>(null);
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

  function openSub(focusFirst: boolean) {
    parentLevel?.closeSubs(stableClose);
    setFocusOnOpen(focusFirst);
    setSubOpen(true);
  }

  const value: DropdownMenuSubContextValue = {
    open: subOpen,
    focusOnOpen,
    openSub,
    closeSub: stableClose,
    triggerRef,
    contentRef,
    subTriggerId,
    subContentId,
  };

  return (
    <DropdownMenuSubContext.Provider value={value}>
      <div className="relative">{children}</div>
    </DropdownMenuSubContext.Provider>
  );
}

export interface DropdownMenuSubTriggerProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  children?: ReactNode;
}

/**
 * The parent item that opens a submenu. It is a `role="menuitem"` with
 * `aria-haspopup="menu"` + `aria-expanded`: ArrowRight / Enter / Space open
 * the submenu and move focus to its first item; hovering opens it without
 * moving focus.
 */
export function DropdownMenuSubTrigger({
  icon,
  children,
  className,
  onClick,
  onKeyDown,
  onMouseEnter,
  ...rest
}: DropdownMenuSubTriggerProps) {
  useDropdownMenu("DropdownMenuSubTrigger");
  const sub = useDropdownMenuSub("DropdownMenuSubTrigger");

  function handleClick(event: ReactMouseEvent<HTMLButtonElement>) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    sub.openSub(true);
  }

  function handleKeyDown(event: ReactKeyboardEvent<HTMLButtonElement>) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    if (event.key === "ArrowRight") {
      event.preventDefault();
      event.stopPropagation();
      sub.openSub(true);
    }
  }

  function handleMouseEnter(event: ReactMouseEvent<HTMLButtonElement>) {
    onMouseEnter?.(event);
    event.currentTarget.focus();
    sub.openSub(false);
  }

  return (
    <button
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
      {icon ? (
        <span aria-hidden="true" className={cx(ICON_SLOT_CLASSES, "text-[var(--ds-color-muted-foreground)]")}>
          {icon}
        </span>
      ) : null}
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
    </button>
  );
}

export interface DropdownMenuSubContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

const SUBMENU_CLASSES =
  "absolute z-40 max-h-[min(20rem,calc(100vh-2rem))] min-w-[10rem] max-w-[calc(100vw-1.5rem)] overflow-y-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
const SUBMENU_SIDE_CLASSES: Record<"right" | "left", string> = {
  right: "left-full top-0 ml-1.5",
  left: "right-full top-0 mr-1.5",
};

/**
 * The submenu panel (`role="menu"`). Opens to the side of its trigger and
 * flips left when the right side would leave the viewport. ArrowLeft and
 * Escape close only this level and return focus to the sub trigger; the
 * parent menu stays open.
 */
export function DropdownMenuSubContent({
  children,
  className,
  onKeyDown,
  ...rest
}: DropdownMenuSubContentProps) {
  const menu = useDropdownMenu("DropdownMenuSubContent");
  const sub = useDropdownMenuSub("DropdownMenuSubContent");
  const level = useMenuLevel();
  const [side, setSide] = useState<"right" | "left">("right");
  const [measured, setMeasured] = useState(false);
  const open = sub.open;

  // Keyboard/click opens move focus to the first sub item; hover opens do not.
  useEffect(() => {
    if (!open) return;
    if (!sub.focusOnOpen) return;
    const node = sub.contentRef.current;
    if (!node) return;
    focusItem(menuItems(node), 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Flip to the left side when there is more room there. Runs before paint.
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  function handleKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    const node = sub.contentRef.current;
    if (!node) return;
    const items = menuItems(node);
    const current = items.indexOf(document.activeElement as HTMLElement);
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
        // Close only this level; the parent menu stays open.
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

  function handlePointerOver(event: ReactMouseEvent<HTMLDivElement>) {
    const node = sub.contentRef.current;
    if (!node) return;
    const item = (event.target as HTMLElement).closest<HTMLElement>(
      '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]',
    );
    if (!item || item.closest('[role="menu"]') !== node) return;
    if (!item.hasAttribute("data-ds-subtrigger")) level.closeSubs();
  }

  if (!open) return null;

  return (
    <MenuLevelContext.Provider value={level}>
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
    </MenuLevelContext.Provider>
  );
}
