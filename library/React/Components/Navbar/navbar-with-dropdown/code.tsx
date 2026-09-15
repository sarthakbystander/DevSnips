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
  AnchorHTMLAttributes,
  ButtonHTMLAttributes,
  HTMLAttributes,
  KeyboardEvent as ReactKeyboardEvent,
  ReactNode,
  RefObject,
} from "react";

/**
 * DevSnips React Navbar — with dropdown navigation.
 *
 * Primary navigation containing disclosure dropdowns: real `<a>` links in a
 * labelled panel with roving DOM focus, Escape / outside-pointer close,
 * focus restoration, disabled items, and viewport-aware alignment. Built
 * entirely from the shared Navbar primitives; see the `navbar` reference
 * for the full system documentation.
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type NavbarBreakpoint = "sm" | "md" | "lg";
export type NavbarVariant = "default" | "transparent";
export type NavbarSectionAlign = "start" | "center" | "end";
export type NavbarActionVariant = "primary" | "outline" | "ghost";
export type NavbarMobilePlacement = "panel" | "side";
export type NavbarDropdownPlacement = "bottom-start" | "bottom-end";

/* ------------------------------------------------------------------------ */
/* Shared class constants (single visual system)                            */
/* ------------------------------------------------------------------------ */

// Navigation height 48–56px (DESIGN_TOKENS §22): the bar is h-14 (56px).
const NAV_CLASSES =
  "border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]";
const NAV_TRANSPARENT_CLASSES = "border-b border-transparent bg-transparent";
const BAR_CLASSES = "relative mx-auto flex h-14 max-w-6xl items-center gap-2 px-4 sm:px-6";
const BRAND_CLASSES =
  "inline-flex shrink-0 items-center gap-2 rounded-[var(--ds-radius-sm)] text-sm font-semibold leading-5 tracking-tight text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const SECTION_ALIGN_CLASSES: Record<NavbarSectionAlign, string> = {
  start: "flex min-w-0 items-center gap-1",
  center: "flex min-w-0 flex-1 items-center justify-center gap-1",
  end: "ml-auto flex min-w-0 items-center justify-end gap-2",
};
const LINK_LAYOUT =
  "inline-flex items-center gap-1.5 rounded-[var(--ds-radius-sm)] px-2.5 py-1.5 text-sm font-medium leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const LINK_MOBILE_LAYOUT =
  "flex w-full items-center gap-1.5 rounded-[var(--ds-radius-sm)] px-3 py-2 text-sm font-medium leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const LINK_IDLE =
  "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const LINK_ACTIVE = "bg-[var(--ds-color-surface-active)] text-[var(--ds-color-foreground)]";
const LINK_DISABLED = "pointer-events-none text-[var(--ds-color-muted-foreground)] opacity-50";
const ACTION_LAYOUT =
  "inline-flex h-9 items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] px-3 text-sm font-medium leading-5 transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const ACTION_VARIANT_CLASSES: Record<NavbarActionVariant, string> = {
  primary:
    "bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] shadow-[var(--ds-shadow-xs)] hover:opacity-90",
  outline:
    "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] hover:bg-[var(--ds-color-surface-hover)]",
  ghost:
    "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]",
};
const TOGGLE_CLASSES =
  "ml-auto inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const MOBILE_PANEL_CLASSES =
  "absolute inset-x-0 top-full z-40 max-h-[calc(100dvh-4rem)] overflow-y-auto border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] shadow-[var(--ds-shadow-md)]";
const MOBILE_SIDE_CLASSES =
  "fixed inset-y-0 left-0 z-50 flex w-72 max-w-[calc(100vw-4rem)] flex-col border-r border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] shadow-[var(--ds-shadow-lg)]";
const MOBILE_OVERLAY_CLASSES =
  "fixed inset-0 z-40 bg-[var(--ds-color-overlay)]";
const MOBILE_CONTENT_CLASSES = "flex flex-col gap-1 px-4 py-4";
const DROPDOWN_PANEL_CLASSES =
  "absolute z-40 mt-1.5 max-h-[min(24rem,calc(100dvh-6rem))] min-w-[13rem] max-w-[calc(100vw-1.5rem)] overflow-y-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
const DROPDOWN_ITEM_LAYOUT =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2 py-1.5 text-left text-[13px] leading-5 transition-colors duration-150 ease-out focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
const DIVIDER_CLASSES = "mx-1 my-1 h-px bg-[var(--ds-color-border)]";

const CONTENT_VISIBLE_CLASSES: Record<NavbarBreakpoint, string> = {
  sm: "hidden sm:flex",
  md: "hidden md:flex",
  lg: "hidden lg:flex",
};
const BELOW_BREAKPOINT_CLASSES: Record<NavbarBreakpoint, string> = {
  sm: "sm:hidden",
  md: "md:hidden",
  lg: "lg:hidden",
};
const DROPDOWN_PLACEMENT_CLASSES: Record<NavbarDropdownPlacement, string> = {
  "bottom-start": "left-0 top-full",
  "bottom-end": "right-0 top-full",
};

function MenuIcon({ className }: { className?: string }) {
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
      <path d="M4 7h16" />
      <path d="M4 12h16" />
      <path d="M4 17h16" />
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

function ExternalLinkIcon({ className }: { className?: string }) {
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
      <path d="M15 3h6v6" />
      <path d="M10 14 21 3" />
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    </svg>
  );
}

/* ------------------------------------------------------------------------ */
/* Navbar (root) context                                                    */
/* ------------------------------------------------------------------------ */

interface NavbarContextValue {
  mobileOpen: boolean;
  toggleMobile(): void;
  closeMobile(): void;
  toggleRef: RefObject<HTMLButtonElement>;
  mobileRegionId: string;
  breakpoint: NavbarBreakpoint;
}

const NavbarContext = createContext<NavbarContextValue | null>(null);

function useNavbar(component: string): NavbarContextValue {
  const context = useContext(NavbarContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Navbar>.`);
  }
  return context;
}

/** True when rendered inside `<NavbarMobileContent>` — links stack full-width. */
const NavbarMobileAreaContext = createContext(false);

export interface NavbarProps {
  /** Mobile-menu open state (controlled). */
  open?: boolean;
  /** Initial mobile-menu open state (uncontrolled). */
  defaultOpen?: boolean;
  /** Called whenever the mobile menu requests to open or close. */
  onOpenChange?: (open: boolean) => void;
  /** Accessible name of the navigation landmark. */
  label?: string;
  /** Responsive breakpoint below which the desktop content collapses. */
  breakpoint?: NavbarBreakpoint;
  /** `transparent` removes the surface + bottom border for use over a page header. */
  variant?: NavbarVariant;
  className?: string;
  children?: ReactNode;
}

export function Navbar({
  open,
  defaultOpen = false,
  onOpenChange,
  label = "Main",
  breakpoint = "md",
  variant = "default",
  className,
  children,
}: NavbarProps) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const rootRef = useRef<HTMLElement>(null);
  const toggleRef = useRef<HTMLButtonElement>(null);
  const reactId = useId();
  const mobileRegionId = `ds-navbar-mobile${reactId}`;

  function requestOpen(next: boolean) {
    if (!isControlled) setInternalOpen(next);
    onOpenChange?.(next);
  }

  const context: NavbarContextValue = {
    mobileOpen: actualOpen,
    toggleMobile() {
      requestOpen(!actualOpen);
    },
    closeMobile() {
      if (actualOpen) requestOpen(false);
    },
    toggleRef,
    mobileRegionId,
    breakpoint,
  };

  // Escape closes the mobile navigation from anywhere in the document.
  useEffect(() => {
    if (!actualOpen) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        requestOpen(false);
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualOpen]);

  // A pointer down outside the navbar closes an open mobile navigation.
  useEffect(() => {
    if (!actualOpen) return;
    function onPointerDown(event: PointerEvent) {
      const root = rootRef.current;
      if (root && !root.contains(event.target as Node)) requestOpen(false);
    }
    document.addEventListener("pointerdown", onPointerDown, true);
    return () => document.removeEventListener("pointerdown", onPointerDown, true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualOpen]);

  // Focus restoration: when the mobile region unmounts, focus would be
  // stranded on <body> — return it to the toggle. Closing via the toggle
  // itself keeps focus on the toggle (no-op), and Tab moves on naturally.
  const wasOpenRef = useRef(false);
  useEffect(() => {
    if (wasOpenRef.current && !actualOpen) {
      const active = document.activeElement;
      const toggle = toggleRef.current;
      if (toggle && toggle.isConnected && (active === null || active === document.body)) {
        toggle.focus();
      }
    }
    wasOpenRef.current = actualOpen;
  }, [actualOpen]);

  return (
    <NavbarContext.Provider value={context}>
      <nav
        ref={rootRef}
        aria-label={label}
        className={cx(variant === "transparent" ? NAV_TRANSPARENT_CLASSES : NAV_CLASSES, className)}
      >
        <div className={BAR_CLASSES}>{children}</div>
      </nav>
    </NavbarContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* Brand / content regions                                                  */
/* ------------------------------------------------------------------------ */

export interface NavbarBrandProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  /** Home URL the brand points at. */
  href?: string;
  children?: ReactNode;
}

export function NavbarBrand({ href = "/", className, children, ...rest }: NavbarBrandProps) {
  return (
    <a href={href} className={cx(BRAND_CLASSES, className)} {...rest}>
      {children}
    </a>
  );
}

export interface NavbarContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function NavbarContent({ className, children, ...rest }: NavbarContentProps) {
  const context = useNavbar("NavbarContent");
  return (
    <div
      className={cx("min-w-0 flex-1 items-center gap-4", CONTENT_VISIBLE_CLASSES[context.breakpoint], className)}
      {...rest}
    >
      {children}
    </div>
  );
}

export interface NavbarSectionProps extends HTMLAttributes<HTMLUListElement> {
  /** Region of the bar: `start` (after the brand), `center`, or `end` (trailing). */
  align?: NavbarSectionAlign;
  children?: ReactNode;
}

export function NavbarSection({ align = "start", className, children, ...rest }: NavbarSectionProps) {
  return (
    <ul role="list" className={cx(SECTION_ALIGN_CLASSES[align], className)} {...rest}>
      {children}
    </ul>
  );
}

export interface NavbarItemProps extends HTMLAttributes<HTMLLIElement> {
  children?: ReactNode;
}

export function NavbarItem({ className, children, ...rest }: NavbarItemProps) {
  return (
    <li className={cx("flex min-w-0", className)} {...rest}>
      {children}
    </li>
  );
}

/* ------------------------------------------------------------------------ */
/* Links and actions                                                        */
/* ------------------------------------------------------------------------ */

export interface NavbarLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  href?: string;
  /** Marks the current page: `aria-current="page"` + the active surface. */
  active?: boolean;
  /** Opens in a new tab (`target="_blank" rel="noreferrer"`) with an indicator. */
  external?: boolean;
  /** Renders a non-interactive `aria-disabled` span — never a dead anchor. */
  disabled?: boolean;
  children?: ReactNode;
}

export function NavbarLink({
  href = "#",
  active = false,
  external = false,
  disabled = false,
  onClick,
  className,
  children,
  ...rest
}: NavbarLinkProps) {
  const context = useNavbar("NavbarLink");
  const inMobileArea = useContext(NavbarMobileAreaContext);
  const classes = cx(
    inMobileArea ? LINK_MOBILE_LAYOUT : LINK_LAYOUT,
    disabled ? LINK_DISABLED : active ? LINK_ACTIVE : LINK_IDLE,
    className,
  );

  if (disabled) {
    return (
      <span aria-disabled="true" className={classes}>
        {children}
      </span>
    );
  }

  return (
    <a
      href={href}
      aria-current={active ? "page" : undefined}
      target={external ? "_blank" : undefined}
      rel={external ? "noreferrer" : undefined}
      onClick={(event) => {
        onClick?.(event);
        context.closeMobile();
      }}
      className={classes}
      {...rest}
    >
      <span className="min-w-0 truncate">{children}</span>
      {external ? (
        <>
          <ExternalLinkIcon className="size-3.5 shrink-0 text-[var(--ds-color-muted-foreground)]" />
          <span className="sr-only">(opens in a new tab)</span>
        </>
      ) : null}
    </a>
  );
}

interface NavbarActionBaseProps {
  /** Visual weight of the action. */
  variant?: NavbarActionVariant;
  className?: string;
  children?: ReactNode;
}
export type NavbarActionProps =
  | (NavbarActionBaseProps & { href: string } & Omit<
        AnchorHTMLAttributes<HTMLAnchorElement>,
        "href"
      >)
  | (NavbarActionBaseProps & { href?: undefined } & ButtonHTMLAttributes<HTMLButtonElement>);

export function NavbarAction(props: NavbarActionProps) {
  if (props.href !== undefined) {
    const { variant = "primary", href, className, children, ...rest } = props;
    return (
      <a href={href} className={cx(ACTION_LAYOUT, ACTION_VARIANT_CLASSES[variant], className)} {...rest}>
        {children}
      </a>
    );
  }
  const { variant = "primary", className, children, type = "button", ...rest } = props;
  return (
    <button type={type} className={cx(ACTION_LAYOUT, ACTION_VARIANT_CLASSES[variant], className)} {...rest}>
      {children}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* Mobile navigation                                                        */
/* ------------------------------------------------------------------------ */

export interface NavbarToggleProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Accessible name override (defaults to "Open/Close navigation menu"). */
  label?: string;
}

export function NavbarToggle({ label, className, onClick, ...rest }: NavbarToggleProps) {
  const context = useNavbar("NavbarToggle");
  // The first mounted toggle (the bar's) permanently owns the shared ref, so
  // a second toggle (e.g. a close button inside a side panel) never leaves
  // the focus-restore target pointing at an unmounted element.
  function claimRef(node: HTMLButtonElement | null) {
    if (node && !context.toggleRef.current) {
      (context.toggleRef as { current: HTMLButtonElement | null }).current = node;
    }
  }
  return (
    <button
      ref={claimRef}
      type="button"
      aria-expanded={context.mobileOpen}
      aria-controls={context.mobileRegionId}
      aria-label={label ?? (context.mobileOpen ? "Close navigation menu" : "Open navigation menu")}
      onClick={(event) => {
        onClick?.(event);
        if (event.defaultPrevented) return;
        context.toggleMobile();
      }}
      className={cx(TOGGLE_CLASSES, BELOW_BREAKPOINT_CLASSES[context.breakpoint], className)}
      {...rest}
    >
      {context.mobileOpen ? <CloseIcon className="size-5" /> : <MenuIcon className="size-5" />}
    </button>
  );
}

export interface NavbarMobileProps {
  /**
   * `panel` (default): a full-width region disclosed directly under the bar.
   * `side`: a compact side panel with an overlay — Escape and overlay
   * interaction close it, body scroll is locked while open, and focus moves
   * into the panel (focus is NOT trapped: this is a navigation disclosure,
   * not a modal dialog).
   */
  placement?: NavbarMobilePlacement;
  className?: string;
  children?: ReactNode;
}

export function NavbarMobile({ placement = "panel", className, children }: NavbarMobileProps) {
  const context = useNavbar("NavbarMobile");
  const panelRef = useRef<HTMLDivElement>(null);
  const open = context.mobileOpen;

  // Side panel only: move focus into the panel on open and lock body scroll
  // (with scrollbar-width compensation so the page does not shift).
  useEffect(() => {
    if (!open || placement !== "side") return;
    const panel = panelRef.current;
    const first = panel?.querySelector<HTMLElement>("a[href], button:not([disabled])");
    first?.focus();
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    const previousOverflow = document.body.style.overflow;
    const previousPaddingRight = document.body.style.paddingRight;
    document.body.style.overflow = "hidden";
    if (scrollbarWidth > 0) document.body.style.paddingRight = `${scrollbarWidth}px`;
    return () => {
      document.body.style.overflow = previousOverflow;
      document.body.style.paddingRight = previousPaddingRight;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, placement]);

  if (!open) return null;

  if (placement === "side") {
    return (
      <>
        <div
          aria-hidden="true"
          data-ds-navbar-overlay=""
          className={cx(MOBILE_OVERLAY_CLASSES, BELOW_BREAKPOINT_CLASSES[context.breakpoint])}
          onPointerDown={() => context.closeMobile()}
        />
        <div
          ref={panelRef}
          id={context.mobileRegionId}
          className={cx(MOBILE_SIDE_CLASSES, BELOW_BREAKPOINT_CLASSES[context.breakpoint], className)}
        >
          {children}
        </div>
      </>
    );
  }

  return (
    <div
      ref={panelRef}
      id={context.mobileRegionId}
      className={cx(MOBILE_PANEL_CLASSES, BELOW_BREAKPOINT_CLASSES[context.breakpoint], className)}
    >
      {children}
    </div>
  );
}

export interface NavbarMobileContentProps extends HTMLAttributes<HTMLUListElement> {
  children?: ReactNode;
}

export function NavbarMobileContent({ className, children, ...rest }: NavbarMobileContentProps) {
  return (
    <NavbarMobileAreaContext.Provider value={true}>
      <ul role="list" className={cx(MOBILE_CONTENT_CLASSES, className)} {...rest}>
        {children}
      </ul>
    </NavbarMobileAreaContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* Navigation dropdown (disclosure pattern — links stay real anchors)       */
/* ------------------------------------------------------------------------ */

interface NavbarDropdownContextValue {
  open: boolean;
  initialFocus: "first" | "last";
  requestOpen(next: boolean, focusTarget?: "first" | "last"): void;
  closeMenu(options?: { refocus?: boolean }): void;
  triggerRef: RefObject<HTMLButtonElement>;
  rootRef: RefObject<HTMLDivElement>;
  triggerId: string;
  contentId: string;
  placement: NavbarDropdownPlacement;
}

const NavbarDropdownContext = createContext<NavbarDropdownContextValue | null>(null);

function useNavbarDropdown(component: string): NavbarDropdownContextValue {
  const context = useContext(NavbarDropdownContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <NavbarDropdown>.`);
  }
  return context;
}

/** Focusable dropdown items owned directly by `content`. */
function dropdownItems(content: HTMLElement): HTMLElement[] {
  return Array.from(
    content.querySelectorAll<HTMLElement>("a[href], button"),
  ).filter(
    (el) =>
      el.closest("[data-ds-navbar-dropdown-content]") === content &&
      !el.hasAttribute("disabled") &&
      el.getAttribute("aria-disabled") !== "true",
  );
}

function focusDropdownItem(items: HTMLElement[], index: number): void {
  if (items.length === 0) return;
  const wrapped = ((index % items.length) + items.length) % items.length;
  items[wrapped].focus();
}

export interface NavbarDropdownProps {
  /** Initial open state (uncontrolled). */
  defaultOpen?: boolean;
  /** Alignment of the panel relative to the trigger; flips to stay in the viewport. */
  placement?: NavbarDropdownPlacement;
  className?: string;
  children?: ReactNode;
}

export function NavbarDropdown({
  defaultOpen = false,
  placement = "bottom-start",
  className,
  children,
}: NavbarDropdownProps) {
  const [open, setOpen] = useState(defaultOpen);
  const [initialFocus, setInitialFocus] = useState<"first" | "last">("first");
  const triggerRef = useRef<HTMLButtonElement>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const reactId = useId();
  const triggerId = `ds-navbar-dd-trigger${reactId}`;
  const contentId = `ds-navbar-dd-content${reactId}`;

  function requestOpen(next: boolean, focusTarget: "first" | "last" = "first") {
    setInitialFocus(focusTarget);
    setOpen(next);
  }

  function closeMenu(options?: { refocus?: boolean }) {
    const refocus = options?.refocus ?? true;
    setOpen(false);
    if (refocus) triggerRef.current?.focus();
  }

  // A pointer down outside the dropdown closes it without stealing focus.
  useEffect(() => {
    if (!open) return;
    function onPointerDown(event: PointerEvent) {
      const root = rootRef.current;
      if (root && !root.contains(event.target as Node)) closeMenu({ refocus: false });
    }
    document.addEventListener("pointerdown", onPointerDown, true);
    return () => document.removeEventListener("pointerdown", onPointerDown, true);
  }, [open]);

  const context: NavbarDropdownContextValue = {
    open,
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
    <NavbarDropdownContext.Provider value={context}>
      <div ref={rootRef} className={cx("relative flex min-w-0", className)}>
        {children}
      </div>
    </NavbarDropdownContext.Provider>
  );
}

export interface NavbarDropdownTriggerProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  children?: ReactNode;
}

export function NavbarDropdownTrigger({
  icon,
  className,
  children,
  onClick,
  onKeyDown,
  ...rest
}: NavbarDropdownTriggerProps) {
  const context = useNavbarDropdown("NavbarDropdownTrigger");

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
      ref={context.triggerRef}
      type="button"
      id={context.triggerId}
      aria-haspopup="true"
      aria-expanded={context.open}
      aria-controls={context.contentId}
      onClick={(event) => {
        onClick?.(event);
        if (event.defaultPrevented) return;
        context.requestOpen(!context.open);
      }}
      onKeyDown={handleKeyDown}
      className={cx(
        LINK_LAYOUT,
        LINK_IDLE,
        "aria-expanded:bg-[var(--ds-color-surface-hover)] aria-expanded:text-[var(--ds-color-foreground)]",
        className,
      )}
      {...rest}
    >
      {icon ? (
        <span aria-hidden="true" className="inline-flex shrink-0 [&_svg]:size-3.5">
          {icon}
        </span>
      ) : null}
      <span className="min-w-0 truncate">{children}</span>
      <ChevronDown
        className={cx(
          "size-3.5 shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 ease-out motion-reduce:transition-none",
          context.open && "rotate-180",
        )}
      />
    </button>
  );
}

export interface NavbarDropdownContentProps extends HTMLAttributes<HTMLDivElement> {
  /** Explicit accessible name; otherwise the panel is labelled by its trigger. */
  "aria-label"?: string;
  children?: ReactNode;
}

export function NavbarDropdownContent({
  onKeyDown,
  className,
  children,
  ...rest
}: NavbarDropdownContentProps) {
  const context = useNavbarDropdown("NavbarDropdownContent");
  const contentRef = useRef<HTMLDivElement>(null);
  const [resolved, setResolved] = useState<NavbarDropdownPlacement>(context.placement);
  const [measured, setMeasured] = useState(false);
  const open = context.open;

  // Move focus into the panel when it opens (first item, or last when the
  // trigger was invoked with ArrowUp).
  useEffect(() => {
    if (!open) return;
    const node = contentRef.current;
    if (!node) return;
    const items = dropdownItems(node);
    focusDropdownItem(items, context.initialFocus === "last" ? items.length - 1 : 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Measure against the viewport and flip the horizontal alignment when the
  // preferred side would overflow. Runs before paint; the panel stays
  // `invisible` until the first measurement so the flip never flashes.
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
    let align: "start" | "end" = context.placement === "bottom-end" ? "end" : "start";
    if (align === "start" && t.left + c.width > window.innerWidth - margin && t.right - c.width >= margin) {
      align = "end";
    } else if (align === "end" && t.right - c.width < margin && t.left + c.width <= window.innerWidth - margin) {
      align = "start";
    }
    setResolved(align === "end" ? "bottom-end" : "bottom-start");
    setMeasured(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, context.placement]);

  function handleKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    const node = contentRef.current;
    if (!node) return;
    const items = dropdownItems(node);
    const current = items.indexOf(document.activeElement as HTMLElement);
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        event.stopPropagation();
        focusDropdownItem(items, current + 1);
        break;
      case "ArrowUp":
        event.preventDefault();
        event.stopPropagation();
        focusDropdownItem(items, current - 1);
        break;
      case "Home":
        event.preventDefault();
        event.stopPropagation();
        focusDropdownItem(items, 0);
        break;
      case "End":
        event.preventDefault();
        event.stopPropagation();
        focusDropdownItem(items, items.length - 1);
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

  if (!open) return null;

  return (
    <div
      ref={contentRef}
      id={context.contentId}
      data-ds-navbar-dropdown-content=""
      aria-labelledby={rest["aria-label"] ? undefined : context.triggerId}
      onKeyDown={handleKeyDown}
      className={cx(
        DROPDOWN_PANEL_CLASSES,
        DROPDOWN_PLACEMENT_CLASSES[resolved],
        !measured && "invisible",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

export interface NavbarDropdownItemProps {
  /** Navigation target. When omitted, the item renders a `<button>` action. */
  href?: string;
  /** Marks the current page: `aria-current="page"` + the active surface. */
  active?: boolean;
  /** Opens in a new tab (`target="_blank" rel="noreferrer"`) with an indicator. */
  external?: boolean;
  /** Renders a non-interactive `aria-disabled` span — skipped by arrow keys. */
  disabled?: boolean;
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  /** Called when the item is activated, before the dropdown closes. */
  onSelect?: () => void;
  /** Accessible name override (e.g. icon-forward items). */
  "aria-label"?: string;
  className?: string;
  children?: ReactNode;
}

export function NavbarDropdownItem({
  href,
  active = false,
  external = false,
  disabled = false,
  icon,
  onSelect,
  className,
  children,
  ...rest
}: NavbarDropdownItemProps) {
  const context = useNavbarDropdown("NavbarDropdownItem");
  const classes = cx(
    DROPDOWN_ITEM_LAYOUT,
    disabled ? LINK_DISABLED : active ? LINK_ACTIVE : LINK_IDLE,
    className,
  );
  const iconSlot = icon ? (
    <span
      aria-hidden="true"
      className={cx(
        "inline-flex shrink-0 [&_svg]:size-4",
        active ? "text-current" : "text-[var(--ds-color-muted-foreground)]",
      )}
    >
      {icon}
    </span>
  ) : null;
  const label = <span className="min-w-0 flex-1 truncate">{children}</span>;
  const externalMarker = external ? (
    <>
      <ExternalLinkIcon className="size-3.5 shrink-0 text-[var(--ds-color-muted-foreground)]" />
      <span className="sr-only">(opens in a new tab)</span>
    </>
  ) : null;

  if (disabled) {
    return (
      <span aria-disabled="true" className={classes}>
        {iconSlot}
        {label}
      </span>
    );
  }

  if (href !== undefined) {
    return (
      <a
        href={href}
        aria-current={active ? "page" : undefined}
        target={external ? "_blank" : undefined}
        rel={external ? "noreferrer" : undefined}
        onClick={() => {
          onSelect?.();
          context.closeMenu();
        }}
        className={classes}
        {...rest}
      >
        {iconSlot}
        {label}
        {externalMarker}
      </a>
    );
  }

  return (
    <button
      type="button"
      onClick={() => {
        onSelect?.();
        context.closeMenu();
      }}
      className={classes}
      {...rest}
    >
      {iconSlot}
      {label}
    </button>
  );
}

export interface NavbarDividerProps extends HTMLAttributes<HTMLDivElement> {
  children?: undefined;
}

export function NavbarDivider({ className, ...rest }: NavbarDividerProps) {
  return (
    <div
      role="separator"
      aria-orientation="horizontal"
      className={cx(DIVIDER_CLASSES, className)}
      {...rest}
    />
  );
}
