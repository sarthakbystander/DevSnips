/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useRef,
  useState
} from "react";
import { createPortal } from "react-dom";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const openDialogKeys = [];
let scrollLockCount = 0;
let previousOverflow = "";
let previousPaddingRight = "";
function lockScroll() {
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
function unlockScroll() {
  scrollLockCount -= 1;
  if (scrollLockCount === 0) {
    document.body.style.overflow = previousOverflow;
    document.body.style.paddingRight = previousPaddingRight;
  }
}
const FOCUSABLE_SELECTOR = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
function focusableElements(root) {
  return Array.from(root.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
    (el) => !el.hasAttribute("disabled") && !el.hidden && el.getAttribute("aria-hidden") !== "true"
  );
}
const TRIGGER_CLASSES = "inline-flex h-9 max-w-full items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const OVERLAY_CLASSES = "fixed inset-0 z-40 bg-[var(--ds-color-overlay)]";
const CONTENT_CLASSES = "fixed left-1/2 top-1/2 z-50 flex max-h-[calc(100dvh-2rem)] w-[calc(100vw-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 flex-col overflow-hidden rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] shadow-[var(--ds-shadow-lg)] focus:outline-none";
const HEADER_CLASSES = "flex flex-col gap-1.5 px-5 pt-5";
const TITLE_CLASSES = "text-lg font-semibold leading-[1.35] tracking-[-0.01em] text-[var(--ds-color-foreground)]";
const DESCRIPTION_CLASSES = "text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
const FOOTER_CLASSES = "flex flex-col-reverse gap-2 px-5 pb-5 pt-4 sm:flex-row sm:justify-end [&>button]:w-full sm:[&>button]:w-auto";
const CLOSE_VARIANT_CLASSES = {
  outline: TRIGGER_CLASSES,
  primary: "inline-flex h-9 max-w-full items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
  destructive: "inline-flex h-9 max-w-full items-center justify-center gap-2 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-destructive)] px-3 text-sm font-medium leading-5 text-[var(--ds-color-destructive-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-destructive)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-destructive)_80%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
  ghost: "absolute right-3 top-3 inline-flex size-8 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none"
};
const DialogContext = createContext(null);
function useDialog(component) {
  const context = useContext(DialogContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Dialog>.`);
  }
  return context;
}
function Dialog({
  open,
  defaultOpen = false,
  onOpenChange,
  modal = true,
  children
}) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const triggerRef = useRef(null);
  const restoreFocusRef = useRef(null);
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
    (next) => {
      if (next && !openRef.current) {
        restoreFocusRef.current = document.activeElement;
      }
      if (!isControlled) setInternalOpen(next);
      onOpenChange?.(next);
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [isControlled, onOpenChange]
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
  const rememberFocus = useCallback((element) => {
    if (restoreFocusRef.current === null) {
      restoreFocusRef.current = element;
    }
  }, []);
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
  }, [actualOpen, modal, dialogKey]);
  useEffect(() => {
    if (!actualOpen) return;
    function onKeyDown(event) {
      if (event.key === "Escape" && openDialogKeys[openDialogKeys.length - 1] === dialogKey) {
        event.preventDefault();
        requestCloseRef.current();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [actualOpen, dialogKey]);
  const value = {
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
    triggerRef
  };
  return <DialogContext.Provider value={value}>{children}</DialogContext.Provider>;
}
function DialogTrigger({ children, className, onClick, ...rest }) {
  const context = useDialog("DialogTrigger");
  function handleClick(event) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    if (context.open) {
      context.requestClose();
    } else {
      context.requestOpen(true);
    }
  }
  return <button
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
    </button>;
}
function DialogContent({ children, className, onKeyDown, ...rest }) {
  const context = useDialog("DialogContent");
  const contentRef = useRef(null);
  const open = context.open;
  useEffect(() => {
    if (!open) return;
    const node = contentRef.current;
    if (!node) return;
    context.rememberFocus(document.activeElement);
    const items = focusableElements(node);
    (items[0] ?? node).focus();
  }, [open]);
  useEffect(() => {
    if (!open || context.modal) return;
    function onPointerDown(event) {
      const node = contentRef.current;
      const target = event.target;
      const trigger = context.triggerRef.current;
      if (node && !node.contains(target) && !(trigger && trigger.contains(target))) {
        context.requestClose();
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, [open, context.modal]);
  function handleKeyDown(event) {
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
      {context.modal ? <div
      aria-hidden="true"
      data-ds-dialog-overlay=""
      className={OVERLAY_CLASSES}
      onPointerDown={(event) => {
        event.preventDefault();
        context.requestClose();
      }}
    /> : null}
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
    document.body
  );
}
function DialogHeader({ className, children, ...rest }) {
  return <div className={cx(HEADER_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function DialogTitle({ className, children, ...rest }) {
  const context = useDialog("DialogTitle");
  useEffect(() => context.registerTitle(), [context]);
  return <h2 id={context.titleId} className={cx(TITLE_CLASSES, className)} {...rest}>
      {children}
    </h2>;
}
function DialogDescription({ className, children, ...rest }) {
  const context = useDialog("DialogDescription");
  useEffect(() => context.registerDescription(), [context]);
  return <p id={context.descriptionId} className={cx(DESCRIPTION_CLASSES, className)} {...rest}>
      {children}
    </p>;
}
function DialogFooter({ className, children, ...rest }) {
  return <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function DialogClose({ children, className, onClick, variant = "outline", ...rest }) {
  const context = useDialog("DialogClose");
  function handleClick(event) {
    onClick?.(event);
    if (event.defaultPrevented) return;
    context.requestClose();
  }
  return <button
    type="button"
    onClick={handleClick}
    className={cx(CLOSE_VARIANT_CLASSES[variant], className)}
    {...rest}
  >
      {children}
    </button>;
}

export { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter, DialogClose };

export default Dialog;
