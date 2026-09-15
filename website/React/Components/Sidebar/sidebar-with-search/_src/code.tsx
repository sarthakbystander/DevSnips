import {
  createContext,
  useContext,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  KeyboardEvent as ReactKeyboardEvent,
  ReactNode,
  RefObject,
} from "react";

/**
 * DevSnips React Sidebar — search variant.
 *
 * A working navigation filter: labelled search field, live
 * case-insensitive filtering, parent-preserving matches, a role=status
 * empty state, and clear/Escape reset. The implementation core is
 * identical to the reference `sidebar` — this variant is the search
 * *pattern* (SidebarSearch + SidebarNav query).
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type SidebarBreakpoint = "sm" | "md" | "lg";

/* ------------------------------------------------------------------------ */
/* Shared class constants (single visual system)                            */
/* ------------------------------------------------------------------------ */

// Sidebar width 240–280px (DESIGN_TOKENS §22): expanded w-64 (256px),
// collapsed w-16 (64px icon rail). Mobile drawer is w-72 capped by viewport.
const ASIDE_CLASSES =
  "sticky top-0 h-[100dvh] shrink-0 flex-col border-r border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] transition-[width] duration-150 ease-out motion-reduce:transition-none";
const NAV_INNER_CLASSES = "flex h-full min-h-0 flex-col";
const DRAWER_CLASSES =
  "fixed inset-y-0 left-0 z-50 flex w-72 max-w-[calc(100vw-3rem)] flex-col border-r border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] shadow-[var(--ds-shadow-lg)]";
const OVERLAY_CLASSES = "fixed inset-0 z-40 bg-[var(--ds-color-overlay)]";
const DRAWER_CLOSE_CLASSES =
  "absolute right-3 top-3 z-10 inline-flex size-9 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const TRIGGER_CLASSES =
  "inline-flex size-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const RAIL_CLASSES =
  "group/rail absolute inset-y-0 -right-2 z-20 w-4 cursor-ew-resize rounded-none border-none bg-transparent p-0 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const MENU_BUTTON_LAYOUT =
  "group/sbitem relative flex w-full items-center gap-2.5 rounded-[var(--ds-radius-sm)] py-2 text-left text-sm leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const MENU_BUTTON_IDLE =
  "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const MENU_BUTTON_ACTIVE =
  "bg-[var(--ds-color-surface-active)] font-medium text-[var(--ds-color-foreground)] shadow-[inset_2px_0_0_0_var(--ds-color-foreground)]";
const MENU_BUTTON_PARENT_ACTIVE =
  "font-medium text-[var(--ds-color-foreground)]";
const MENU_BUTTON_DISABLED =
  "pointer-events-none text-[var(--ds-color-muted-foreground)] opacity-50";
const SUB_BUTTON_LAYOUT =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2 py-1.5 text-left text-[13px] leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const SUB_BUTTON_IDLE = MENU_BUTTON_IDLE;
const SUB_BUTTON_ACTIVE =
  "bg-[var(--ds-color-surface-active)] font-medium text-[var(--ds-color-foreground)]";
const BADGE_CLASSES =
  "ml-auto inline-flex h-5 min-w-5 shrink-0 items-center justify-center rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-1.5 text-[11px] font-medium leading-none tabular-nums text-[var(--ds-color-muted-foreground)]";
const BADGE_DOT_CLASSES =
  "absolute right-1.5 top-1.5 size-1.5 rounded-full bg-[var(--ds-color-accent)]";
// Collapsed-rail tooltip: rendered `fixed` (never clipped by the content
// scroll container) and positioned by measurement via the DOM style API —
// the same approach as the Tooltips family. Hidden until first measured.
const RAIL_TOOLTIP_CLASSES =
  "pointer-events-none invisible fixed z-[60] -translate-y-1/2 whitespace-nowrap rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] px-2 py-1 text-xs font-medium leading-4 text-[var(--ds-color-foreground)] opacity-0 shadow-[var(--ds-shadow-md)] transition-opacity duration-150 ease-out motion-reduce:transition-none";
const GROUP_LABEL_CLASSES =
  "px-2.5 pt-1 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";

const ABOVE_BREAKPOINT_CLASSES: Record<SidebarBreakpoint, string> = {
  sm: "hidden sm:flex",
  md: "hidden md:flex",
  lg: "hidden lg:flex",
};
const BELOW_BREAKPOINT_CLASSES: Record<SidebarBreakpoint, string> = {
  sm: "sm:hidden",
  md: "md:hidden",
  lg: "lg:hidden",
};
const BREAKPOINT_QUERY: Record<SidebarBreakpoint, string> = {
  sm: "(min-width: 640px)",
  md: "(min-width: 768px)",
  lg: "(min-width: 1024px)",
};

/* ------------------------------------------------------------------------ */
/* Shared icons (component-owned, always aria-hidden)                       */
/* ------------------------------------------------------------------------ */

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

function PanelLeftIcon({ className }: { className?: string }) {
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
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <path d="M9 4v16" />
    </svg>
  );
}

function CloseIcon({ className }: { className?: string }) {
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
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </svg>
  );
}

function SearchIcon({ className }: { className?: string }) {
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
      <circle cx="11" cy="11" r="7" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}

/* ------------------------------------------------------------------------ */
/* Module-level scroll lock (shared with the Dialog family's approach)      */
/* ------------------------------------------------------------------------ */

let scrollLockCount = 0;
let previousOverflow = "";
let previousPaddingRight = "";

function lockScroll(): void {
  scrollLockCount += 1;
  if (scrollLockCount === 1) {
    previousOverflow = document.body.style.overflow;
    previousPaddingRight = document.body.style.paddingRight;
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }
    document.body.style.overflow = "hidden";
  }
}

function unlockScroll(): void {
  scrollLockCount -= 1;
  if (scrollLockCount === 0) {
    document.body.style.overflow = previousOverflow;
    document.body.style.paddingRight = previousPaddingRight;
  }
}

const FOCUSABLE_SELECTOR =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

/** Focusable elements inside `root` (excludes hidden / aria-hidden nodes). */
function focusableElements(root: HTMLElement): HTMLElement[] {
  return Array.from(root.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)).filter(
    (el) => !el.hasAttribute("disabled") && !el.hidden && el.getAttribute("aria-hidden") !== "true",
  );
}

/* ------------------------------------------------------------------------ */
/* Collapsed-rail tooltip (measured, fixed-position)                        */
/* ------------------------------------------------------------------------ */

interface RailTooltipHandle {
  /** Callback ref for the control the tooltip describes. */
  anchorRef(element: HTMLElement | null): void;
  tipRef: { current: HTMLSpanElement | null };
  show(): void;
  hide(): void;
}

/**
 * Positions a fixed tooltip next to a collapsed-rail control. Rendering
 * `fixed` keeps the tooltip out of the content scroll container (which
 * clips absolutely positioned descendants); coordinates are assigned via
 * the DOM style API on hover/focus — no inline style attributes, no
 * positioning library. Any scroll hides the tooltip so it never goes stale.
 */
function useRailTooltip(enabled: boolean): RailTooltipHandle {
  const anchorNodeRef = useRef<HTMLElement | null>(null);
  const tipRef = useRef<HTMLSpanElement | null>(null);

  function hide() {
    const tip = tipRef.current;
    if (!tip) return;
    tip.style.opacity = "0";
    tip.style.visibility = "hidden";
    document.removeEventListener("scroll", hide, true);
  }

  function show() {
    if (!enabled) return;
    const anchor = anchorNodeRef.current;
    const tip = tipRef.current;
    if (!anchor || !tip) return;
    const rect = anchor.getBoundingClientRect();
    const tipHeight = tip.offsetHeight || 24;
    const center = rect.top + rect.height / 2;
    const clamped = Math.min(
      Math.max(center, 8 + tipHeight / 2),
      window.innerHeight - 8 - tipHeight / 2,
    );
    tip.style.top = `${Math.round(clamped)}px`;
    tip.style.left = `${Math.round(rect.right + 8)}px`;
    tip.style.visibility = "visible";
    tip.style.opacity = "1";
    document.addEventListener("scroll", hide, true);
  }

  useEffect(() => {
    if (!enabled) hide();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled]);

  return {
    anchorRef(element) {
      anchorNodeRef.current = element;
    },
    tipRef,
    show,
    hide,
  };
}

/* ------------------------------------------------------------------------ */
/* SidebarProvider (state root)                                             */
/* ------------------------------------------------------------------------ */

export interface SidebarContextValue {
  /** Desktop collapsed (icon-rail) state. */
  collapsed: boolean;
  /** Request a collapsed-state change (internal toggle points). */
  requestCollapsed(next: boolean): void;
  /** Mobile drawer open state. */
  mobileOpen: boolean;
  /** Request a mobile drawer open/close change. */
  requestMobileOpen(next: boolean): void;
  /** Close the mobile drawer (no-op when already closed). */
  closeMobile(): void;
  /** Responsive breakpoint below which the drawer replaces the sidebar. */
  breakpoint: SidebarBreakpoint;
  /** True while the viewport is at or above the breakpoint (one listener). */
  isDesktop: boolean;
  /** The `<SidebarTrigger>` button — focus restoration target. */
  triggerRef: RefObject<HTMLButtonElement>;
  /** Landmark ids the trigger's `aria-controls` points at. */
  desktopId: string;
  mobileId: string;
}

const SidebarContext = createContext<SidebarContextValue | null>(null);

/** Which rendering surface a primitive is being composed into. */
const SidebarAreaContext = createContext<"desktop" | "mobile">("desktop");

export function useSidebar(component = "useSidebar"): SidebarContextValue {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <SidebarProvider>.`);
  }
  return context;
}

export interface SidebarProviderProps {
  /** Desktop collapsed state (controlled). */
  collapsed?: boolean;
  /** Initial desktop collapsed state (uncontrolled). */
  defaultCollapsed?: boolean;
  /** Called whenever the collapsed state requests a change. */
  onCollapsedChange?: (collapsed: boolean) => void;
  /** Mobile drawer open state (controlled). */
  mobileOpen?: boolean;
  /** Initial mobile drawer open state (uncontrolled). */
  defaultMobileOpen?: boolean;
  /** Called whenever the mobile drawer requests to open or close. */
  onMobileOpenChange?: (open: boolean) => void;
  /** Responsive breakpoint below which the sidebar becomes a drawer. */
  breakpoint?: SidebarBreakpoint;
  children?: ReactNode;
}

export function SidebarProvider({
  collapsed,
  defaultCollapsed = false,
  onCollapsedChange,
  mobileOpen,
  defaultMobileOpen = false,
  onMobileOpenChange,
  breakpoint = "md",
  children,
}: SidebarProviderProps) {
  const [internalCollapsed, setInternalCollapsed] = useState(defaultCollapsed);
  const collapsedControlled = collapsed !== undefined;
  const actualCollapsed = collapsedControlled ? collapsed : internalCollapsed;

  const [internalMobileOpen, setInternalMobileOpen] = useState(defaultMobileOpen);
  const mobileControlled = mobileOpen !== undefined;
  const actualMobileOpen = mobileControlled ? mobileOpen : internalMobileOpen;

  const triggerRef = useRef<HTMLButtonElement>(null);
  const reactId = useId();
  const desktopId = `ds-sidebar${reactId}`;
  const mobileId = `ds-sidebar-mobile${reactId}`;

  const [isDesktop, setIsDesktop] = useState(
    () => typeof window === "undefined" || window.matchMedia(BREAKPOINT_QUERY[breakpoint]).matches,
  );
  useEffect(() => {
    const mql = window.matchMedia(BREAKPOINT_QUERY[breakpoint]);
    function onChange(event: MediaQueryListEvent) {
      setIsDesktop(event.matches);
    }
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, [breakpoint]);

  function requestCollapsed(next: boolean) {
    if (!collapsedControlled) setInternalCollapsed(next);
    onCollapsedChange?.(next);
  }
  function requestMobileOpen(next: boolean) {
    if (!mobileControlled) setInternalMobileOpen(next);
    onMobileOpenChange?.(next);
  }

  const context: SidebarContextValue = {
    collapsed: actualCollapsed,
    requestCollapsed,
    mobileOpen: actualMobileOpen,
    requestMobileOpen,
    closeMobile() {
      if (actualMobileOpen) requestMobileOpen(false);
    },
    breakpoint,
    isDesktop,
    triggerRef,
    desktopId,
    mobileId,
  };

  // Escape closes the drawer from anywhere in the document.
  useEffect(() => {
    if (!actualMobileOpen) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        requestMobileOpen(false);
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualMobileOpen]);

  // A resize to desktop while the drawer is open closes it (and releases the
  // scroll lock) instead of leaving a hidden modal active.
  useEffect(() => {
    if (isDesktop && actualMobileOpen) requestMobileOpen(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isDesktop, actualMobileOpen]);

  // Focus restoration: when the drawer unmounts, focus would be stranded on
  // <body> — return it to the trigger. Closing via the trigger itself is a
  // no-op; pointer dismissals only run while the drawer owns focus.
  const wasMobileOpenRef = useRef(false);
  useEffect(() => {
    if (wasMobileOpenRef.current && !actualMobileOpen) {
      const active = document.activeElement;
      const trigger = triggerRef.current;
      if (trigger && trigger.isConnected && (active === null || active === document.body)) {
        trigger.focus();
      }
    }
    wasMobileOpenRef.current = actualMobileOpen;
  }, [actualMobileOpen]);

  return (
    <SidebarContext.Provider value={context}>{children}</SidebarContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* Sidebar (desktop landmark + mobile drawer)                               */
/* ------------------------------------------------------------------------ */

export interface SidebarProps {
  /** Accessible name of the navigation landmark (and the mobile dialog). */
  label?: string;
  className?: string;
  children?: ReactNode;
}

export function Sidebar({ label = "Sidebar", className, children }: SidebarProps) {
  const context = useSidebar("Sidebar");
  const panelRef = useRef<HTMLDivElement>(null);
  const mobileOpen = context.mobileOpen;
  const collapsed = context.collapsed;

  // Drawer open: move focus into the drawer (first navigation control) and
  // lock body scroll with scrollbar-width compensation.
  useEffect(() => {
    if (!mobileOpen) return;
    const panel = panelRef.current;
    if (!panel) return;
    const focusables = focusableElements(panel);
    (focusables[0] ?? panel).focus();
    lockScroll();
    return () => unlockScroll();
  }, [mobileOpen]);

  // Tab trap at the drawer boundaries: modal behavior without stealing Tab
  // from the natural order (links first, the built-in close button last).
  function handleDrawerKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key !== "Tab") return;
    const panel = panelRef.current;
    if (!panel) return;
    const focusables = focusableElements(panel);
    if (focusables.length === 0) return;
    const first = focusables[0] as HTMLElement | undefined;
    const last = focusables[focusables.length - 1] as HTMLElement | undefined;
    if (!first || !last) return;
    const active = document.activeElement;
    if (event.shiftKey && (active === first || !panel.contains(active))) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && active === last) {
      event.preventDefault();
      first.focus();
    }
  }

  return (
    <>
      {/* Desktop: persistent navigation landmark. */}
      <aside
        id={context.desktopId}
        className={cx(
          ASIDE_CLASSES,
          ABOVE_BREAKPOINT_CLASSES[context.breakpoint],
          collapsed ? "w-16" : "w-64",
          className,
        )}
        data-collapsed={collapsed ? "" : undefined}
      >
        <SidebarAreaContext.Provider value="desktop">
          <nav aria-label={label} className={NAV_INNER_CLASSES}>
            {children}
          </nav>
        </SidebarAreaContext.Provider>
      </aside>
      {/* Mobile: modal navigation drawer (rendered only while open). */}
      {mobileOpen ? (
        <SidebarAreaContext.Provider value="mobile">
          <div
            aria-hidden="true"
            data-ds-sidebar-overlay=""
            onPointerDown={() => context.closeMobile()}
            className={cx(OVERLAY_CLASSES, BELOW_BREAKPOINT_CLASSES[context.breakpoint])}
          />
          <div
            ref={panelRef}
            role="dialog"
            aria-modal="true"
            aria-label={label}
            id={context.mobileId}
            tabIndex={-1}
            onKeyDown={handleDrawerKeyDown}
            className={cx(DRAWER_CLASSES, BELOW_BREAKPOINT_CLASSES[context.breakpoint], className)}
          >
            <nav aria-label={label} className={NAV_INNER_CLASSES}>
              {children}
              <button
                type="button"
                aria-label="Close navigation"
                onClick={() => context.closeMobile()}
                className={DRAWER_CLOSE_CLASSES}
              >
                <CloseIcon className="size-4" />
              </button>
            </nav>
          </div>
        </SidebarAreaContext.Provider>
      ) : null}
    </>
  );
}

/* ------------------------------------------------------------------------ */
/* Header / Content / Footer regions                                        */
/* ------------------------------------------------------------------------ */

export interface SidebarHeaderProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function SidebarHeader({ className, children, ...rest }: SidebarHeaderProps) {
  const context = useSidebar("SidebarHeader");
  return (
    <div
      className={cx(
        "flex h-14 shrink-0 items-center gap-2 border-b border-[var(--ds-color-border-subtle)]",
        context.collapsed ? "justify-center px-2" : "px-4",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

export interface SidebarContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function SidebarContent({ className, children, ...rest }: SidebarContentProps) {
  const context = useSidebar("SidebarContent");
  return (
    <div
      className={cx(
        "flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto py-4",
        context.collapsed ? "px-2" : "px-3",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

export interface SidebarFooterProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function SidebarFooter({ className, children, ...rest }: SidebarFooterProps) {
  const context = useSidebar("SidebarFooter");
  return (
    <div
      className={cx(
        "mt-auto shrink-0 border-t border-[var(--ds-color-border-subtle)]",
        context.collapsed ? "p-2" : "p-3",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* Groups                                                                   */
/* ------------------------------------------------------------------------ */

export interface SidebarGroupProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function SidebarGroup({ className, children, ...rest }: SidebarGroupProps) {
  return (
    <div className={cx("flex flex-col gap-1", className)} {...rest}>
      {children}
    </div>
  );
}

export interface SidebarGroupLabelProps extends HTMLAttributes<HTMLParagraphElement> {
  children?: ReactNode;
}

export function SidebarGroupLabel({ className, children, ...rest }: SidebarGroupLabelProps) {
  const context = useSidebar("SidebarGroupLabel");
  return (
    <p
      className={cx(GROUP_LABEL_CLASSES, context.collapsed && "sr-only", className)}
      {...rest}
    >
      {children}
    </p>
  );
}

/* ------------------------------------------------------------------------ */
/* Menu rows                                                                */
/* ------------------------------------------------------------------------ */

export interface SidebarMenuProps extends HTMLAttributes<HTMLUListElement> {
  children?: ReactNode;
}

export function SidebarMenu({ className, children, ...rest }: SidebarMenuProps) {
  return (
    <ul className={cx("flex flex-col gap-0.5", className)} {...rest}>
      {children}
    </ul>
  );
}

export interface SidebarMenuItemProps extends HTMLAttributes<HTMLLIElement> {
  children?: ReactNode;
}

export function SidebarMenuItem({ className, children, ...rest }: SidebarMenuItemProps) {
  return (
    <li className={cx("relative", className)} {...rest}>
      {children}
    </li>
  );
}

interface MenuButtonState {
  active: boolean;
  disabled: boolean;
}

interface MenuButtonContent {
  icon?: ReactNode;
  badge?: ReactNode;
  children?: ReactNode;
}

/** Shared inner content of a navigation row (icon, label, badge). */
function menuButtonChildren(
  content: MenuButtonContent,
  collapsed: boolean,
): ReactNode[] {
  const { icon, badge, children } = content;
  const parts: ReactNode[] = [];
  if (icon) {
    parts.push(
      <span
        key="icon"
        aria-hidden="true"
        className="inline-flex shrink-0 items-center justify-center [&_svg]:size-4"
      >
        {icon}
      </span>,
    );
  }
  parts.push(
    <span
      key="label"
      className={collapsed ? "sr-only" : "min-w-0 flex-1 truncate"}
    >
      {children}
    </span>,
  );
  if (badge !== undefined && badge !== null) {
    if (collapsed) {
      // The count stays in the accessibility tree; visually it collapses to
      // a dot so the 64px rail never overflows.
      parts.push(
        <span key="badge-sr" className="sr-only">
          {badge}
        </span>,
        <span key="badge-dot" aria-hidden="true" className={BADGE_DOT_CLASSES} />,
      );
    } else {
      parts.push(
        <span key="badge" className={BADGE_CLASSES}>
          {badge}
        </span>,
      );
    }
  }
  return parts;
}

function menuButtonClasses(state: MenuButtonState, collapsed: boolean, className?: string): string {
  return cx(
    MENU_BUTTON_LAYOUT,
    collapsed ? "justify-center px-2" : "px-2.5",
    state.disabled
      ? MENU_BUTTON_DISABLED
      : state.active
        ? MENU_BUTTON_ACTIVE
        : MENU_BUTTON_IDLE,
    className,
  );
}

export interface SidebarMenuButtonProps {
  /** Navigation target. When omitted, the row renders a `<button>` action. */
  href?: string;
  /** Marks the current page: `aria-current="page"` + the active treatment. */
  active?: boolean;
  /** Renders a non-interactive `aria-disabled` span — never a dead control. */
  disabled?: boolean;
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  /** Trailing count/status badge (kept accessible in the collapsed rail). */
  badge?: ReactNode;
  /** Collapsed-rail tooltip text; defaults to a string `children` label. */
  tooltip?: string;
  /** Activated when the row is a button action. */
  onClick?: () => void;
  /** Accessible name override (e.g. icon-forward rows). */
  "aria-label"?: string;
  className?: string;
  children?: ReactNode;
}

export function SidebarMenuButton({
  href,
  active = false,
  disabled = false,
  icon,
  badge,
  tooltip,
  onClick,
  className,
  children,
  ...rest
}: SidebarMenuButtonProps) {
  const context = useSidebar("SidebarMenuButton");
  const mobileArea = useContext(SidebarAreaContext) === "mobile";
  const collapsed = context.collapsed && !mobileArea;
  const accessibleTooltip =
    tooltip ?? (typeof children === "string" ? children : undefined);
  const tip = useRailTooltip(collapsed && !disabled && accessibleTooltip !== undefined);
  const classes = menuButtonClasses({ active, disabled }, collapsed, className);
  const content = menuButtonChildren({ icon, badge, children }, collapsed);
  const tipNode =
    collapsed && !disabled && accessibleTooltip !== undefined ? (
      <span ref={tip.tipRef} aria-hidden="true" className={RAIL_TOOLTIP_CLASSES}>
        {accessibleTooltip}
      </span>
    ) : null;
  const tipHandlers = {
    onMouseEnter: tip.show,
    onMouseLeave: tip.hide,
    onFocus: tip.show,
    onBlur: tip.hide,
  };

  if (disabled) {
    return (
      <span aria-disabled="true" className={classes}>
        {content}
      </span>
    );
  }

  if (href !== undefined) {
    return (
      <a
        ref={tip.anchorRef}
        href={href}
        aria-current={active ? "page" : undefined}
        onClick={() => {
          onClick?.();
          if (mobileArea) context.closeMobile();
        }}
        className={classes}
        {...tipHandlers}
        {...rest}
      >
        {content}
        {tipNode}
      </a>
    );
  }

  return (
    <button
      ref={tip.anchorRef}
      type="button"
      aria-current={active ? "page" : undefined}
      onClick={() => onClick?.()}
      className={classes}
      {...tipHandlers}
      {...rest}
    >
      {content}
      {tipNode}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* Collapsible parents + nested levels                                      */
/* ------------------------------------------------------------------------ */

interface SidebarCollapsibleContextValue {
  contentId: string;
  open: boolean;
}

const SidebarCollapsibleContext = createContext<SidebarCollapsibleContextValue | null>(null);

export interface SidebarMenuCollapsibleProps {
  /** Visible + accessible label of the parent row. */
  label: string;
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  /** Trailing badge, rendered before the chevron. */
  badge?: ReactNode;
  /** A descendant is the current page (parent-indication treatment). */
  active?: boolean;
  /** Renders a non-interactive `aria-disabled` span. */
  disabled?: boolean;
  /** Expanded state (controlled). */
  open?: boolean;
  /** Initial expanded state (uncontrolled). */
  defaultOpen?: boolean;
  /** Called whenever the parent requests to expand or collapse. */
  onOpenChange?: (open: boolean) => void;
  className?: string;
  /** The nested level: one `<SidebarMenuSub>` (plus optional siblings). */
  children?: ReactNode;
}

export function SidebarMenuCollapsible({
  label,
  icon,
  badge,
  active = false,
  disabled = false,
  open,
  defaultOpen = false,
  onOpenChange,
  className,
  children,
}: SidebarMenuCollapsibleProps) {
  const context = useSidebar("SidebarMenuCollapsible");
  const mobileArea = useContext(SidebarAreaContext) === "mobile";
  const collapsed = context.collapsed && !mobileArea;
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const reactId = useId();
  const contentId = `ds-sidebar-sub${reactId}`;
  const tip = useRailTooltip(collapsed && !disabled);

  function requestOpen(next: boolean) {
    if (!isControlled) setInternalOpen(next);
    onOpenChange?.(next);
  }

  function handleClick() {
    if (collapsed) {
      // From the icon rail, activating a parent expands the sidebar and
      // opens the group so the nested level is immediately reachable.
      context.requestCollapsed(false);
      requestOpen(true);
      return;
    }
    requestOpen(!actualOpen);
  }

  const value: SidebarCollapsibleContextValue = { contentId, open: actualOpen };

  if (disabled) {
    return (
      <span aria-disabled="true" className={cx(MENU_BUTTON_LAYOUT, collapsed ? "justify-center px-2" : "px-2.5", MENU_BUTTON_DISABLED, className)}>
        {menuButtonChildren({ icon, badge, children: label }, collapsed)}
      </span>
    );
  }

  return (
    <SidebarCollapsibleContext.Provider value={value}>
      <button
        ref={tip.anchorRef}
        type="button"
        aria-expanded={collapsed ? false : actualOpen}
        aria-controls={collapsed ? undefined : contentId}
        onClick={handleClick}
        onMouseEnter={tip.show}
        onMouseLeave={tip.hide}
        onFocus={tip.show}
        onBlur={tip.hide}
        className={cx(
          MENU_BUTTON_LAYOUT,
          collapsed ? "justify-center px-2" : "px-2.5",
          active ? MENU_BUTTON_PARENT_ACTIVE : MENU_BUTTON_IDLE,
          className,
        )}
      >
        {icon ? (
          <span aria-hidden="true" className="inline-flex shrink-0 items-center justify-center [&_svg]:size-4">
            {icon}
          </span>
        ) : null}
        <span className={collapsed ? "sr-only" : "min-w-0 flex-1 truncate"}>{label}</span>
        {badge !== undefined && badge !== null ? (
          collapsed ? (
            <>
              <span className="sr-only">{badge}</span>
              <span aria-hidden="true" className={BADGE_DOT_CLASSES} />
            </>
          ) : (
            <span className={BADGE_CLASSES}>{badge}</span>
          )
        ) : null}
        <ChevronDown
          className={cx(
            "ml-auto size-3.5 shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none",
            actualOpen && !collapsed && "rotate-180",
            collapsed && "hidden",
          )}
        />
        {collapsed ? (
          <span ref={tip.tipRef} aria-hidden="true" className={RAIL_TOOLTIP_CLASSES}>
            {label}
          </span>
        ) : null}
      </button>
      {actualOpen && !collapsed ? children : null}
    </SidebarCollapsibleContext.Provider>
  );
}

export interface SidebarMenuSubProps extends HTMLAttributes<HTMLUListElement> {
  children?: ReactNode;
}

export function SidebarMenuSub({ className, children, ...rest }: SidebarMenuSubProps) {
  const context = useSidebar("SidebarMenuSub");
  const mobileArea = useContext(SidebarAreaContext) === "mobile";
  const collapsible = useContext(SidebarCollapsibleContext);
  if (context.collapsed && !mobileArea) return null;
  return (
    <ul
      id={collapsible?.contentId}
      className={cx(
        "ml-[18px] mt-0.5 flex flex-col gap-0.5 border-l border-[var(--ds-color-border)] pl-2",
        className,
      )}
      {...rest}
    >
      {children}
    </ul>
  );
}

export interface SidebarMenuSubItemProps extends HTMLAttributes<HTMLLIElement> {
  children?: ReactNode;
}

export function SidebarMenuSubItem({ className, children, ...rest }: SidebarMenuSubItemProps) {
  return (
    <li className={cx("relative", className)} {...rest}>
      {children}
    </li>
  );
}

export interface SidebarMenuSubButtonProps {
  /** Navigation target. When omitted, the row renders a `<button>` action. */
  href?: string;
  /** Marks the current page: `aria-current="page"` + the active treatment. */
  active?: boolean;
  /** Renders a non-interactive `aria-disabled` span. */
  disabled?: boolean;
  /** Activated when the row is a button action. */
  onClick?: () => void;
  /** Accessible name override. */
  "aria-label"?: string;
  className?: string;
  children?: ReactNode;
}

export function SidebarMenuSubButton({
  href,
  active = false,
  disabled = false,
  onClick,
  className,
  children,
  ...rest
}: SidebarMenuSubButtonProps) {
  const context = useSidebar("SidebarMenuSubButton");
  const mobileArea = useContext(SidebarAreaContext) === "mobile";
  const classes = cx(
    SUB_BUTTON_LAYOUT,
    disabled ? MENU_BUTTON_DISABLED : active ? SUB_BUTTON_ACTIVE : SUB_BUTTON_IDLE,
    className,
  );
  const label = <span className="min-w-0 flex-1 truncate">{children}</span>;

  if (disabled) {
    return (
      <span aria-disabled="true" className={classes}>
        {label}
      </span>
    );
  }

  if (href !== undefined) {
    return (
      <a
        href={href}
        aria-current={active ? "page" : undefined}
        onClick={() => {
          onClick?.();
          if (mobileArea) context.closeMobile();
        }}
        className={classes}
        {...rest}
      >
        {label}
      </a>
    );
  }

  return (
    <button
      type="button"
      aria-current={active ? "page" : undefined}
      onClick={() => onClick?.()}
      className={classes}
      {...rest}
    >
      {label}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* Mode controls (trigger + rail)                                           */
/* ------------------------------------------------------------------------ */

export interface SidebarTriggerProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "children"> {
  children?: undefined;
}

export function SidebarTrigger({ className, ...rest }: SidebarTriggerProps) {
  const context = useSidebar("SidebarTrigger");
  const expanded = context.isDesktop ? !context.collapsed : context.mobileOpen;
  return (
    <button
      ref={context.triggerRef}
      type="button"
      aria-label="Toggle sidebar"
      aria-expanded={expanded}
      aria-controls={context.isDesktop ? context.desktopId : context.mobileId}
      onClick={() => {
        if (context.isDesktop) {
          context.requestCollapsed(!context.collapsed);
        } else {
          context.requestMobileOpen(!context.mobileOpen);
        }
      }}
      className={cx(TRIGGER_CLASSES, className)}
      {...rest}
    >
      <PanelLeftIcon className="size-4" />
    </button>
  );
}

export interface SidebarRailProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "children"> {
  children?: undefined;
}

export function SidebarRail({ className, ...rest }: SidebarRailProps) {
  const context = useSidebar("SidebarRail");
  const mobileArea = useContext(SidebarAreaContext) === "mobile";
  if (mobileArea) return null;
  return (
    <button
      type="button"
      aria-label={context.collapsed ? "Expand sidebar" : "Collapse sidebar"}
      aria-expanded={!context.collapsed}
      aria-controls={context.desktopId}
      onClick={() => context.requestCollapsed(!context.collapsed)}
      className={cx(RAIL_CLASSES, className)}
      {...rest}
    >
      <span
        aria-hidden="true"
        className="absolute inset-y-0 left-1/2 w-0.5 -translate-x-1/2 rounded-[var(--ds-radius-full)] bg-transparent transition-colors duration-150 ease-out group-hover/rail:bg-[var(--ds-color-border-strong)] group-focus-visible/rail:bg-[var(--ds-color-border-strong)] motion-reduce:transition-none"
      />
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* SidebarSearch (navigation filter field)                                  */
/* ------------------------------------------------------------------------ */

export interface SidebarSearchProps {
  /** Query value (controlled). */
  value?: string;
  /** Initial query value (uncontrolled). */
  defaultValue?: string;
  /** Called on every change, including the clear action (with `""`). */
  onValueChange?: (value: string) => void;
  /** Placeholder text. */
  placeholder?: string;
  /** Accessible name of the field (rendered sr-only). */
  label?: string;
  /** Disables the field. */
  disabled?: boolean;
  /** Explicit id; paired with the sr-only label either way. */
  id?: string;
  className?: string;
}

export function SidebarSearch({
  value,
  defaultValue = "",
  onValueChange,
  placeholder = "Search navigation",
  label = "Search navigation",
  disabled = false,
  id,
  className,
}: SidebarSearchProps) {
  const context = useSidebar("SidebarSearch");
  const mobileArea = useContext(SidebarAreaContext) === "mobile";
  const [internalValue, setInternalValue] = useState(defaultValue);
  const isControlled = value !== undefined;
  const actualValue = isControlled ? value : internalValue;
  const reactId = useId();
  const inputId = id ?? `ds-sidebar-search${reactId}`;

  if (context.collapsed && !mobileArea) return null;

  function requestValue(next: string) {
    if (!isControlled) setInternalValue(next);
    onValueChange?.(next);
  }

  return (
    <div className={cx("relative", className)}>
      <label htmlFor={inputId} className="sr-only">
        {label}
      </label>
      <span
        aria-hidden="true"
        className="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 text-[var(--ds-color-muted-foreground)] [&_svg]:size-3.5"
      >
        <SearchIcon />
      </span>
      <input
        id={inputId}
        type="search"
        value={actualValue}
        disabled={disabled}
        placeholder={placeholder}
        autoComplete="off"
        onChange={(event) => requestValue(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Escape" && actualValue !== "") {
            // Clear the query without closing the mobile drawer.
            event.stopPropagation();
            requestValue("");
          }
        }}
        className="h-9 w-full rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] pl-8 pr-8 text-sm leading-5 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out placeholder:text-[var(--ds-color-muted-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none [&::-webkit-search-cancel-button]:hidden"
      />
      {actualValue !== "" && !disabled ? (
        <button
          type="button"
          aria-label="Clear search"
          onClick={() => requestValue("")}
          className="absolute right-1.5 top-1/2 inline-flex size-6 -translate-y-1/2 items-center justify-center rounded-[var(--ds-radius-xs)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none"
        >
          <CloseIcon className="size-3" />
        </button>
      ) : null}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* SidebarNav (typed data-driven renderer)                                  */
/* ------------------------------------------------------------------------ */

export interface SidebarNavItem {
  /** Stable id (used for expansion bookkeeping). */
  id: string;
  /** Visible + accessible label. */
  label: string;
  /** Navigation target; items without `href` are plain actions/labels. */
  href?: string;
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  /** Trailing count/status badge. */
  badge?: ReactNode;
  /** Renders a non-interactive `aria-disabled` row. */
  disabled?: boolean;
  /** Marks the current page (`aria-current="page"`). */
  active?: boolean;
  /** Nested level (renderers support up to three levels of indentation). */
  children?: SidebarNavItem[];
}

export interface SidebarNavSection {
  /** Stable id. */
  id: string;
  /** Optional group label (uppercase eyebrow). */
  label?: string;
  items: SidebarNavItem[];
}

export interface SidebarNavProps {
  sections: SidebarNavSection[];
  /** Filter query — case-insensitive label match; parents of matching
   * children stay visible and expand. */
  query?: string;
  /** Message shown when a query matches nothing (rendered as status text). */
  emptyMessage?: string;
  className?: string;
}

function itemMatchesQuery(item: SidebarNavItem, query: string): boolean {
  return item.label.toLowerCase().includes(query);
}

/** Recursive case-insensitive filter: a child match keeps its parent chain;
 * a matching parent keeps its whole subtree. */
function filterNavItems(items: SidebarNavItem[], query: string): SidebarNavItem[] {
  const out: SidebarNavItem[] = [];
  for (const item of items) {
    if (itemMatchesQuery(item, query)) {
      out.push(item);
      continue;
    }
    const children = item.children ? filterNavItems(item.children, query) : undefined;
    if (children && children.length > 0) {
      out.push({ ...item, children });
    }
  }
  return out;
}

function hasActiveDescendant(item: SidebarNavItem): boolean {
  return (item.children ?? []).some(
    (child) => child.active === true || hasActiveDescendant(child),
  );
}

interface SidebarNavGroupRendererProps {
  items: SidebarNavItem[];
  query: string;
  overrides: Record<string, boolean>;
  onToggle: (id: string, open: boolean) => void;
}

function SidebarNavLevel({ items, query, overrides, onToggle }: SidebarNavGroupRendererProps) {
  return (
    <SidebarMenu>
      {items.map((item) => {
        const children = item.children ?? [];
        const descendantActive = hasActiveDescendant(item);
        const effectiveOpen =
          overrides[item.id] ?? (query !== "" ? true : descendantActive);
        return (
          <SidebarMenuItem key={item.id}>
            {children.length > 0 ? (
              <>
                <SidebarMenuCollapsible
                  label={item.label}
                  icon={item.icon}
                  badge={item.badge}
                  active={descendantActive}
                  disabled={item.disabled}
                  open={effectiveOpen}
                  onOpenChange={(next) => onToggle(item.id, next)}
                >
                  <SidebarMenuSub>
                    {(children ?? []).map((child) => (
                      <SidebarMenuSubItem key={child.id}>
                        <SidebarMenuSubButton
                          href={child.href}
                          active={child.active}
                          disabled={child.disabled}
                        >
                          {child.label}
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
                  </SidebarMenuSub>
                </SidebarMenuCollapsible>
              </>
            ) : (
              <SidebarMenuButton
                href={item.href}
                active={item.active}
                disabled={item.disabled}
                icon={item.icon}
                badge={item.badge}
              >
                {item.label}
              </SidebarMenuButton>
            )}
          </SidebarMenuItem>
        );
      })}
    </SidebarMenu>
  );
}

export function SidebarNav({
  sections,
  query = "",
  emptyMessage,
  className,
}: SidebarNavProps) {
  const normalizedQuery = query.trim().toLowerCase();
  const [overrides, setOverrides] = useState<Record<string, boolean>>({});
  const searching = normalizedQuery !== "";
  const renderedSections = searching
    ? sections
        .map((section) => ({
          ...section,
          items: filterNavItems(section.items, normalizedQuery),
        }))
        .filter((section) => section.items.length > 0)
    : sections;

  function onToggle(id: string, open: boolean) {
    setOverrides((current) => ({ ...current, [id]: open }));
  }

  if (renderedSections.length === 0) {
    return (
      <p role="status" className="px-2.5 py-2 text-sm leading-5 text-[var(--ds-color-muted-foreground)]">
        {emptyMessage ?? `No navigation items match "${query}".`}
      </p>
    );
  }

  return (
    <div className={cx("flex flex-col gap-4", className)}>
      {renderedSections.map((section) => (
        <SidebarGroup key={section.id}>
          {section.label ? <SidebarGroupLabel>{section.label}</SidebarGroupLabel> : null}
          <SidebarNavLevel
            items={section.items ?? []}
            query={normalizedQuery}
            overrides={overrides}
            onToggle={onToggle}
          />
        </SidebarGroup>
      ))}
    </div>
  );
}
