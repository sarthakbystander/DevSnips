import {
  Children,
  cloneElement,
  createContext,
  useContext,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import type {
  FocusEvent as ReactFocusEvent,
  HTMLAttributes,
  PointerEvent as ReactPointerEvent,
  ReactElement,
  ReactNode,
  Ref,
  RefObject,
} from "react";

/**
 * DevSnips React Tooltip — disabled-trigger variant.
 *
 * Identical core to the reference tooltip; this variant demonstrates the
 * two disabled patterns: (1) explaining a natively disabled control by
 * wrapping it in a focusable <span tabIndex={0}> (the inner control is
 * pointer-events-none), and (2) suppressing a tooltip entirely with the
 * root's `disabled` prop.
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type TooltipSide = "top" | "right" | "bottom" | "left";
export type TooltipAlign = "start" | "center" | "end";
export type TooltipPlacement = `${TooltipSide}-${TooltipAlign}`;

// `w-max` sizes the bubble to its content: the containing block is the
// (often tiny) trigger wrapper, so shrink-to-fit would squeeze the text to
// the trigger's width. max-w caps it at a readable measure / the viewport.
const CONTENT_CLASSES =
  "pointer-events-none absolute z-40 w-max max-w-[min(16rem,calc(100vw-2rem))] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] px-2.5 py-1.5 text-left text-[13px] leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-sm)] transition-opacity duration-150 ease-out motion-reduce:transition-none";
const ARROW_BASE_CLASSES =
  "absolute size-1.5 rotate-45 border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)]";

const POSITION_CLASSES: Record<TooltipPlacement, string> = {
  "top-start": "bottom-full left-0",
  "top-center": "bottom-full left-1/2 -translate-x-1/2",
  "top-end": "bottom-full right-0",
  "bottom-start": "top-full left-0",
  "bottom-center": "top-full left-1/2 -translate-x-1/2",
  "bottom-end": "top-full right-0",
  "left-start": "right-full top-0",
  "left-center": "right-full top-1/2 -translate-y-1/2",
  "left-end": "right-full bottom-0",
  "right-start": "left-full top-0",
  "right-center": "left-full top-1/2 -translate-y-1/2",
  "right-end": "left-full bottom-0",
};

// The two borders adjacent to the rotated square's trigger-facing corner,
// so the arrow reads as a notch pointing at the trigger.
const ARROW_BORDER_CLASSES: Record<TooltipSide, string> = {
  top: "border-r border-b",
  bottom: "border-l border-t",
  left: "border-t border-r",
  right: "border-b border-l",
};

const ARROW_POSITION_CLASSES: Record<TooltipPlacement, string> = {
  "top-start": "left-3 top-full -translate-y-1/2",
  "top-center": "left-1/2 top-full -translate-x-1/2 -translate-y-1/2",
  "top-end": "right-3 top-full -translate-y-1/2",
  "bottom-start": "bottom-full left-3 translate-y-1/2",
  "bottom-center": "bottom-full left-1/2 -translate-x-1/2 translate-y-1/2",
  "bottom-end": "bottom-full right-3 translate-y-1/2",
  "left-start": "right-full top-2 translate-x-1/2",
  "left-center": "right-full top-1/2 translate-x-1/2 -translate-y-1/2",
  "left-end": "bottom-2 right-full translate-x-1/2",
  "right-start": "left-full top-2 -translate-x-1/2",
  "right-center": "left-full top-1/2 -translate-x-1/2 -translate-y-1/2",
  "right-end": "bottom-2 left-full -translate-x-1/2",
};

function composeRefs<T>(...refs: Array<Ref<T> | undefined>): (node: T | null) => void {
  return (node) => {
    for (const ref of refs) {
      if (typeof ref === "function") ref(node);
      else if (ref) (ref as { current: T | null }).current = node;
    }
  };
}

/* ------------------------------------------------------------------------ */
/* Root context                                                              */
/* ------------------------------------------------------------------------ */

interface TooltipContextValue {
  open: boolean;
  disabled: boolean;
  handleTriggerPointerEnter(): void;
  handleTriggerPointerLeave(): void;
  handleTriggerFocus(): void;
  handleTriggerBlur(): void;
  triggerRef: RefObject<HTMLElement>;
  contentId: string;
  side: TooltipSide;
  align: TooltipAlign;
  sideOffset: number;
}

const TooltipContext = createContext<TooltipContextValue | null>(null);

function useTooltip(component: string): TooltipContextValue {
  const context = useContext(TooltipContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Tooltip>.`);
  }
  return context;
}

/* ------------------------------------------------------------------------ */
/* Tooltip (root)                                                            */
/* ------------------------------------------------------------------------ */

export interface TooltipProps {
  /** Open state (controlled). */
  open?: boolean;
  /** Initial open state (uncontrolled). */
  defaultOpen?: boolean;
  /** Called whenever the tooltip requests to open or close. */
  onOpenChange?: (open: boolean) => void;
  /** Preferred side of the trigger; flips to stay in the viewport. */
  side?: TooltipSide;
  /** Alignment along the trigger; shifts to stay in the viewport. */
  align?: TooltipAlign;
  /** Gap between the trigger and the tooltip, in pixels. */
  sideOffset?: number;
  /** Hover delay before opening, in milliseconds (focus opens immediately). */
  delayDuration?: number;
  /** Suppress the tooltip entirely (hover and focus do nothing). */
  disabled?: boolean;
  className?: string;
  children?: ReactNode;
}

export function Tooltip({
  open,
  defaultOpen = false,
  onOpenChange,
  side = "top",
  align = "center",
  sideOffset = 6,
  delayDuration = 300,
  disabled = false,
  className,
  children,
}: TooltipProps) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  // What opened the tooltip: pointer-opened tooltips close on pointer leave,
  // focus-opened tooltips close on blur. This keeps the two gestures from
  // fighting when both apply to the same trigger.
  const [openedBy, setOpenedBy] = useState<"pointer" | "focus" | null>(actualOpen ? "focus" : null);
  const triggerRef = useRef<HTMLElement>(null);
  const hoveringRef = useRef(false);
  const openTimerRef = useRef<number | null>(null);
  const reactId = useId();
  const contentId = `ds-tooltip-${reactId.replace(/:/g, "")}`;

  function cancelScheduledOpen() {
    if (openTimerRef.current !== null) {
      window.clearTimeout(openTimerRef.current);
      openTimerRef.current = null;
    }
  }

  function requestOpen(source: "pointer" | "focus") {
    setOpenedBy(source);
    if (!actualOpen) {
      if (!isControlled) setInternalOpen(true);
      onOpenChange?.(true);
    }
  }

  function requestClose() {
    cancelScheduledOpen();
    setOpenedBy(null);
    if (actualOpen) {
      if (!isControlled) setInternalOpen(false);
      onOpenChange?.(false);
    }
  }

  function handleTriggerPointerEnter() {
    hoveringRef.current = true;
    if (disabled || actualOpen) return;
    cancelScheduledOpen();
    openTimerRef.current = window.setTimeout(() => requestOpen("pointer"), delayDuration);
  }

  function handleTriggerPointerLeave() {
    hoveringRef.current = false;
    cancelScheduledOpen();
    if (disabled) return;
    if (openedBy === "pointer") requestClose();
  }

  function handleTriggerFocus() {
    if (disabled) return;
    cancelScheduledOpen();
    // Focus opens without the hover delay: keyboard users must not wait.
    requestOpen("focus");
  }

  function handleTriggerBlur() {
    if (hoveringRef.current) {
      // Focus left while the pointer still hovers: hand ownership to the
      // pointer so the tooltip closes on pointer leave instead.
      if (openedBy === "focus") setOpenedBy("pointer");
      return;
    }
    requestClose();
  }

  // A tooltip that becomes disabled while open closes.
  useEffect(() => {
    if (disabled && actualOpen) requestClose();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [disabled, actualOpen]);

  // Escape dismisses the open tooltip; focus stays on the trigger.
  useEffect(() => {
    if (!actualOpen) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") requestClose();
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actualOpen]);

  // Never leave a scheduled hover-open behind on unmount.
  useEffect(() => cancelScheduledOpen, []);

  return (
    <TooltipContext.Provider
      value={{
        open: actualOpen,
        disabled,
        handleTriggerPointerEnter,
        handleTriggerPointerLeave,
        handleTriggerFocus,
        handleTriggerBlur,
        triggerRef,
        contentId,
        side,
        align,
        sideOffset,
      }}
    >
      <span className={cx("relative inline-flex", className)}>{children}</span>
    </TooltipContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* TooltipTrigger                                                            */
/* ------------------------------------------------------------------------ */

interface TriggerChildProps {
  ref?: Ref<HTMLElement>;
  "aria-describedby"?: string;
  onPointerEnter?: (event: ReactPointerEvent<HTMLElement>) => void;
  onPointerLeave?: (event: ReactPointerEvent<HTMLElement>) => void;
  onFocus?: (event: ReactFocusEvent<HTMLElement>) => void;
  onBlur?: (event: ReactFocusEvent<HTMLElement>) => void;
}

export interface TooltipTriggerProps {
  /**
   * Exactly one element: a native focusable element (`<button>`, `<a>`,
   * `<input>`, …) or a component that forwards its ref and these handlers.
   * For a disabled control, wrap it in a `<span tabIndex={0}>` so the
   * explanation stays reachable (see the tooltip-disabled-trigger variant).
   */
  children: ReactElement;
}

export function TooltipTrigger({ children }: TooltipTriggerProps) {
  const context = useTooltip("TooltipTrigger");
  const child = Children.only(children) as ReactElement<TriggerChildProps>;
  const childRef = (child as unknown as { ref?: Ref<HTMLElement> }).ref;
  return cloneElement(child, {
    ref: composeRefs(context.triggerRef, childRef),
    "aria-describedby": context.contentId,
    onPointerEnter: (event: ReactPointerEvent<HTMLElement>) => {
      child.props.onPointerEnter?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerPointerEnter();
    },
    onPointerLeave: (event: ReactPointerEvent<HTMLElement>) => {
      child.props.onPointerLeave?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerPointerLeave();
    },
    onFocus: (event: ReactFocusEvent<HTMLElement>) => {
      child.props.onFocus?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerFocus();
    },
    onBlur: (event: ReactFocusEvent<HTMLElement>) => {
      child.props.onBlur?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerBlur();
    },
  });
}

/* ------------------------------------------------------------------------ */
/* TooltipContent                                                            */
/* ------------------------------------------------------------------------ */

export interface TooltipContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

export function TooltipContent({ className, children, ...rest }: TooltipContentProps) {
  const context = useTooltip("TooltipContent");
  const contentRef = useRef<HTMLDivElement>(null);
  const [resolved, setResolved] = useState<{ side: TooltipSide; align: TooltipAlign }>({
    side: context.side,
    align: context.align,
  });
  const [measured, setMeasured] = useState(false);

  const open = context.open;

  // Measure against the viewport and flip the side / shift the alignment
  // when the preferred placement would overflow. The first pass runs before
  // paint (so the correction never flashes and doubles as the fade-in); a
  // second pass runs one task later to refine against runtime-injected CSS
  // (e.g. the Tailwind CDN inserts its rules in a MutationObserver microtask,
  // after this layout effect — compiled CSS settles the second pass to a
  // no-op).
  useLayoutEffect(() => {
    if (!open) {
      setMeasured(false);
      setResolved({ side: context.side, align: context.align });
      return;
    }
    const node = contentRef.current;
    const trigger = context.triggerRef.current;
    if (!node || !trigger) return;

    function measure() {
      if (!node || !trigger) return;
      const t = trigger.getBoundingClientRect();
      const c = node.getBoundingClientRect();
      const margin = 8;
      const horizontal = context.side === "top" || context.side === "bottom";
      let side = context.side;
      if (horizontal) {
        const below = window.innerHeight - t.bottom;
        const above = t.top;
        if (side === "top" && above < c.height + margin && below > above) side = "bottom";
        else if (side === "bottom" && below < c.height + margin && above > below) side = "top";
      } else {
        const before = t.left;
        const after = window.innerWidth - t.right;
        if (side === "left" && before < c.width + margin && after > before) side = "right";
        else if (side === "right" && after < c.width + margin && before > after) side = "left";
      }
      let align = context.align;
      if (horizontal) {
        const center = t.left + t.width / 2;
        if (align === "center" && center - c.width / 2 < margin) align = "start";
        else if (align === "center" && center + c.width / 2 > window.innerWidth - margin) align = "end";
        if (align === "start" && t.left + c.width > window.innerWidth - margin && t.right - c.width >= margin) {
          align = "end";
        } else if (align === "end" && t.right - c.width < margin && t.left + c.width <= window.innerWidth - margin) {
          align = "start";
        }
      } else {
        const center = t.top + t.height / 2;
        if (align === "center" && center - c.height / 2 < margin) align = "start";
        else if (align === "center" && center + c.height / 2 > window.innerHeight - margin) align = "end";
        if (align === "start" && t.top + c.height > window.innerHeight - margin && t.bottom - c.height >= margin) {
          align = "end";
        } else if (align === "end" && t.bottom - c.height < margin && t.top + c.height <= window.innerHeight - margin) {
          align = "start";
        }
      }
      // sideOffset is applied here (not as a margin utility) so a numeric
      // offset works for every side, including after a flip.
      node.style.marginTop = side === "bottom" ? `${context.sideOffset}px` : "0px";
      node.style.marginBottom = side === "top" ? `${context.sideOffset}px` : "0px";
      node.style.marginLeft = side === "right" ? `${context.sideOffset}px` : "0px";
      node.style.marginRight = side === "left" ? `${context.sideOffset}px` : "0px";
      // Clamp the bubble to the room actually available on the resolved
      // placement, so a trigger hard against the viewport edge keeps the
      // tooltip on-screen (the text simply wraps taller). This only tightens
      // the CSS max-w (the 16rem measure, or a className override) — reset
      // the inline value first so the computed style reflects the CSS cap.
      node.style.maxWidth = "";
      const cssCap = parseFloat(getComputedStyle(node).maxWidth);
      let available: number;
      if (side === "right") available = window.innerWidth - t.right - context.sideOffset - margin;
      else if (side === "left") available = t.left - context.sideOffset - margin;
      else if (align === "start") available = window.innerWidth - t.left - margin;
      else if (align === "end") available = t.right - margin;
      else available = 2 * Math.min(t.left + t.width / 2, window.innerWidth - t.left - t.width / 2) - margin;
      const cap = Math.min(available, window.innerWidth - 2 * margin, Number.isFinite(cssCap) ? cssCap : available);
      node.style.maxWidth = `${Math.floor(Math.max(cap, 96))}px`;
      setResolved({ side, align });
      setMeasured(true);
    }

    measure();
    const refine = window.setTimeout(measure, 0);
    return () => window.clearTimeout(refine);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, context.side, context.align, context.sideOffset]);

  if (!open) return null;

  const placement: TooltipPlacement = `${resolved.side}-${resolved.align}`;

  return (
    <div
      ref={contentRef}
      id={context.contentId}
      role="tooltip"
      className={cx(
        CONTENT_CLASSES,
        POSITION_CLASSES[placement],
        measured ? "opacity-100" : "opacity-0",
        className,
      )}
      {...rest}
    >
      {children}
      <span
        aria-hidden="true"
        className={cx(ARROW_BASE_CLASSES, ARROW_BORDER_CLASSES[resolved.side], ARROW_POSITION_CLASSES[placement])}
      />
    </div>
  );
}

export default Tooltip;
