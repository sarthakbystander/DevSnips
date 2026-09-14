import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";
import { createPortal } from "react-dom";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  KeyboardEvent as ReactKeyboardEvent,
  MouseEvent as ReactMouseEvent,
  ReactNode,
  RefObject,
} from "react";

/**
 * DevSnips React Dialog — Controlled State.
 *
 * The shared dialog core with the open state lifted to the parent
 * (`open` + `onOpenChange`): one controlled dialog can serve many targets,
 * close requests (Escape, overlay, DialogClose) are routed through
 * `onOpenChange(false)` so the parent decides, and a dialog without a
 * visible title is labelled via `aria-label` on `DialogContent`.
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/* ------------------------------------------------------------------------ */
/* Module-level dialog stack + scroll lock                                   */
/* ------------------------------------------------------------------------ */

/**
 * Every open dialog registers its key here; the last entry is the top-most
 * dialog. Escape handling uses the stack so only the top-most dialog closes.
 */
const openDialogKeys: string[] = [];

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

const TRIGGER_CLASSES =
  "inline-flex h-9 max-w-full items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const OVERLAY_CLASSES = "fixed inset-0 z-40 bg-[var(--ds-color-overlay)]";
const CONTENT_CLASSES =
  "fixed left-1/2 top-1/2 z-50 flex max-h-[calc(100dvh-2rem)] w-[calc(100vw-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] shadow-[var(--ds-shadow-lg)] focus:outline-none";
const HEADER_CLASSES = "flex flex-col gap-1.5 px-5 pt-5";
const TITLE_CLASSES =
  "text-lg font-semibold leading-[1.35] tracking-[-0.01em] text-[var(--ds-color-foreground)]";
const DESCRIPTION_CLASSES = "text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
const FOOTER_CLASSES =
  "flex flex-col-reverse gap-2 px-5 pb-5 pt-4 sm:flex-row sm:justify-end [&>button]:w-full sm:[&>button]:w-auto";
// One class constant per close-action kind — the kinds never rely on
// conflicting-utility overrides (Tailwind resolves conflicts by stylesheet
// order, not class order, so overrides of bg-*/border-* are unreliable).
const CLOSE_VARIANT_CLASSES: Record<DialogCloseVariant, string> = {
  outline: TRIGGER_CLASSES,
  primary:
    "inline-flex h-9 max-w-full items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
  destructive:
    "inline-flex h-9 max-w-full items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-destructive)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-destructive-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-destructive)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-destructive)_80%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
  ghost:
    "absolute right-3 top-3 inline-flex size-8 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
};

interface DialogContextValue {
  open: boolean;
  modal: boolean;
  contentId: string;
  titleId: string;
  descriptionId: string;
  hasTitle: boolean;
  hasDescription: boolean;
  registerTitle(): () => void;
  registerDescription(): () => void;
  rememberFocus(element: HTMLElement | null): void;
  requestOpen(next: boolean): void;
  requestClose(): void;
  triggerRef: RefObject<HTMLButtonElement>;
}

const DialogContext = createContext<DialogContextValue | null>(null);

function useDialog(component: string): DialogContextValue {
  const context = useContext(DialogContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Dialog>.`);
  }
  return context;
}

/* ------------------------------------------------------------------------ */
/* Dialog (root)                                                             */
/* ------------------------------------------------------------------------ */

export interface DialogProps {
  /** Open state (controlled). */
  open?: boolean;
  /** Initial open state (uncontrolled). */
  defaultOpen?: boolean;
  /** Called whenever the dialog requests to open or close. */
  onOpenChange?: (open: boolean) => void;
  /**
   * Modal behavior (default true): overlay, scroll lock, focus trap, and
   * `aria-modal`. Set false for a non-modal floating panel (page stays
   * interactive; close on Escape or outside pointer down).
   */
  modal?: boolean;
  children?: ReactNode;
}

export function Dialog({
  open,
  defaultOpen = false,
  onOpenChange,
  modal = true,
  children,
}: DialogProps) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const triggerRef = useRef<HTMLButtonElement>(null);
  const restoreFocusRef = useRef<HTMLElement | null>(null);
  const reactId = useId();
  const dialogKey = `ds-dialog${reactId}`;
  const contentId = `ds-dialog-content${reactId}`;
  const titleId = `ds-dialog-title${reactId}`;
  const descriptionId = `ds-dialog-description${reactId}`;
  const [hasTitle, setHasTitle] = useState(false);
  const [hasDescription, setHasDescription] = useState(false);

  const openRef = useRef(actualOpen);
  openRef.current = actualOpen;
  const requestOpen = useCallback(
    (next: boolean) => {
      // Remember the focused element at the moment the open is REQUESTED
      // (the trigger, or a row action). Capturing here — not in the open
      // effect — because mounted-child effects run before the root's, so by
      // effect time focus has already moved into the dialog.
      if (next && !openRef.current) {
        restoreFocusRef.current = document.activeElement as HTMLElement | null;
      }
      if (!isControlled) setInternalOpen(next);
      onOpenChange?.(next);
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [isControlled, onOpenChange],
  );
  const requestClose = useCallback(() => requestOpen(false), [requestOpen]);
  const requestCloseRef = useRef(requestClose);
  requestCloseRef.current = requestClose;

  const registerTitle = useCallback(() => {
    setHasTitle(true);
    return () => setHasTitle(false);
  }, []);
  const registerDescription = useCallback(() => {
    setHasDescription(true);
    return () => setHasDescription(false);
  }, []);

  // Fallback focus capture for opens that never pass through requestOpen
  // (e.g. a parent flipping controlled `open` directly): DialogContent calls
  // this from its open effect — the first code that moves focus — while the
  // pre-open focused element is still active.
  const rememberFocus = useCallback((element: HTMLElement | null) => {
    if (restoreFocusRef.current === null) {
      restoreFocusRef.current = element;
    }
  }, []);

  // While open: register on the dialog stack and lock body scroll (modal
  // only); on close restore focus to the trigger (or whatever was focused
  // when the dialog opened — captured in requestOpen).
  useEffect(() => {
    if (!actualOpen) return;
    openDialogKeys.push(dialogKey);
    if (modal) lockScroll();
    return () => {
      const index = openDialogKeys.indexOf(dialogKey);
      if (index !== -1) openDialogKeys.splice(index, 1);
      if (modal) unlockScroll();
      const element = restoreFocusRef.current;
      restoreFocusRef.current = null;
      if (element && element.isConnected) element.focus();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualOpen, modal, dialogKey]);

  // Escape closes only the top-most open dialog (nesting-safe).
  useEffect(() => {
    if (!actualOpen) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape" && openDialogKeys[openDialogKeys.length - 1] === dialogKey) {
        event.preventDefault();
        requestCloseRef.current();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualOpen, dialogKey]);

  const value: DialogContextValue = {
    open: actualOpen,
    modal,
    contentId,
    titleId,
    descriptionId,
    hasTitle,
    hasDescription,
    registerTitle,
    registerDescription,
    rememberFocus,
    requestOpen,
    requestClose,
    triggerRef,
  };

  return <DialogContext.Provider value={value}>{children}</DialogContext.Provider>;
}

export default Dialog;

/* ------------------------------------------------------------------------ */
/* DialogTrigger                                                             */
/* ------------------------------------------------------------------------ */

export interface DialogTriggerProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children?: ReactNode;
}

export function DialogTrigger({ children, className, onClick, ...rest }: DialogTriggerProps) {
  const context = useDialog("DialogTrigger");

  function handleClick(event: ReactMouseEvent<HTMLButtonElement>) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    if (context.open) {
      context.requestClose();
    } else {
      context.requestOpen(true);
    }
  }

  return (
    <button
      type="button"
      ref={context.triggerRef}
      aria-haspopup="dialog"
      aria-expanded={context.open}
      aria-controls={context.contentId}
      onClick={handleClick}
      className={cx(TRIGGER_CLASSES, className)}
      {...rest}
    >
      {children}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* DialogContent (portal to document.body)                                   */
/* ------------------------------------------------------------------------ */

export interface DialogContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function DialogContent({ children, className, onKeyDown, ...rest }: DialogContentProps) {
  const context = useDialog("DialogContent");
  const contentRef = useRef<HTMLDivElement>(null);
  const open = context.open;

  // Move focus into the dialog on open: the first focusable element, or the
  // dialog container itself when it has no focusable children. This effect
  // is the first code that moves focus (child effects run before the root's
  // open effect), so it also captures the pre-open focused element for
  // externally-controlled opens that never passed through requestOpen.
  useEffect(() => {
    if (!open) return;
    const node = contentRef.current;
    if (!node) return;
    context.rememberFocus(document.activeElement as HTMLElement | null);
    const items = focusableElements(node);
    (items[0] ?? node).focus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Non-modal mode: an outside pointer down closes the dialog (modal closes
  // via its overlay instead).
  useEffect(() => {
    if (!open || context.modal) return;
    function onPointerDown(event: PointerEvent) {
      const node = contentRef.current;
      const target = event.target as Node;
      const trigger = context.triggerRef.current;
      if (node && !node.contains(target) && !(trigger && trigger.contains(target))) {
        context.requestClose();
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, context.modal]);

  // Focus trap (modal only): wrap Tab / Shift+Tab at the first / last
  // focusable element. Skipped while focus lives inside a NESTED dialog —
  // the nested dialog traps its own keys.
  function handleKeyDown(event: ReactKeyboardEvent<HTMLDivElement>) {
    onKeyDown?.(event);
    if (event.defaultPrevented || event.key !== "Tab" || !context.modal) return;
    const node = contentRef.current;
    if (!node || !node.contains(document.activeElement)) return;
    const items = focusableElements(node);
    if (items.length === 0) {
      event.preventDefault();
      node.focus();
      return;
    }
    const first = items[0];
    const last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  if (!open) return null;
  if (typeof document === "undefined") return null;

  return createPortal(
    <>
      {context.modal ? (
        <div
          aria-hidden="true"
          data-ds-dialog-overlay=""
          className={OVERLAY_CLASSES}
          // Canceling pointerdown suppresses the compatibility mousedown, so
          // the browser's default "focus the clicked surface" behavior never
          // steals focus from the trigger the close is about to restore.
          onPointerDown={(event) => {
            event.preventDefault();
            context.requestClose();
          }}
        />
      ) : null}
      <div
        ref={contentRef}
        id={context.contentId}
        role="dialog"
        aria-modal={context.modal ? true : undefined}
        aria-labelledby={context.hasTitle ? context.titleId : undefined}
        aria-describedby={context.hasDescription ? context.descriptionId : undefined}
        tabIndex={-1}
        onKeyDown={handleKeyDown}
        className={cx(CONTENT_CLASSES, className)}
        {...rest}
      >
        {children}
      </div>
    </>,
    document.body,
  );
}

/* ------------------------------------------------------------------------ */
/* DialogHeader / DialogTitle / DialogDescription                            */
/* ------------------------------------------------------------------------ */

export interface DialogHeaderProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function DialogHeader({ className, children, ...rest }: DialogHeaderProps) {
  return (
    <div className={cx(HEADER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export interface DialogTitleProps extends HTMLAttributes<HTMLHeadingElement> {
  children?: ReactNode;
}

export function DialogTitle({ className, children, ...rest }: DialogTitleProps) {
  const context = useDialog("DialogTitle");
  // Register so DialogContent can wire `aria-labelledby` — and omit it when
  // no title is rendered (content then relies on an explicit `aria-label`).
  useEffect(() => context.registerTitle(), [context]);
  return (
    <h2 id={context.titleId} className={cx(TITLE_CLASSES, className)} {...rest}>
      {children}
    </h2>
  );
}

export interface DialogDescriptionProps extends HTMLAttributes<HTMLParagraphElement> {
  children?: ReactNode;
}

export function DialogDescription({ className, children, ...rest }: DialogDescriptionProps) {
  const context = useDialog("DialogDescription");
  // Register so DialogContent can wire `aria-describedby`.
  useEffect(() => context.registerDescription(), [context]);
  return (
    <p id={context.descriptionId} className={cx(DESCRIPTION_CLASSES, className)} {...rest}>
      {children}
    </p>
  );
}

/* ------------------------------------------------------------------------ */
/* DialogFooter / DialogClose                                                */
/* ------------------------------------------------------------------------ */

export interface DialogFooterProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function DialogFooter({ className, children, ...rest }: DialogFooterProps) {
  return (
    <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export type DialogCloseVariant = "outline" | "primary" | "destructive" | "ghost";

export interface DialogCloseProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * `outline` (default) is the bordered footer cancel action; `primary` /
   * `destructive` are confirming actions that also close; `ghost` is the
   * icon-sized corner close button (positioned top-right of the panel —
   * give it an `aria-label`).
   */
  variant?: DialogCloseVariant;
  children?: ReactNode;
}

export function DialogClose({ children, className, onClick, variant = "outline", ...rest }: DialogCloseProps) {
  const context = useDialog("DialogClose");

  function handleClick(event: ReactMouseEvent<HTMLButtonElement>) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    context.requestClose();
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className={cx(CLOSE_VARIANT_CLASSES[variant], className)}
      {...rest}
    >
      {children}
    </button>
  );
}
