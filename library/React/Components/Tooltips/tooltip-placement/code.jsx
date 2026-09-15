/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  Children,
  cloneElement,
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
const CONTENT_CLASSES = "pointer-events-none absolute z-40 w-max max-w-[min(16rem,calc(100vw-2rem))] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] px-2.5 py-1.5 text-left text-[13px] leading-5 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-sm)] transition-opacity duration-150 ease-out motion-reduce:transition-none";
const ARROW_BASE_CLASSES = "absolute size-1.5 rotate-45 border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)]";
const POSITION_CLASSES = {
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
  "right-end": "left-full bottom-0"
};
const ARROW_BORDER_CLASSES = {
  top: "border-r border-b",
  bottom: "border-l border-t",
  left: "border-t border-r",
  right: "border-b border-l"
};
const ARROW_POSITION_CLASSES = {
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
  "right-end": "bottom-2 left-full -translate-x-1/2"
};
function composeRefs(...refs) {
  return (node) => {
    for (const ref of refs) {
      if (typeof ref === "function") ref(node);
      else if (ref) ref.current = node;
    }
  };
}
const TooltipContext = createContext(null);
function useTooltip(component) {
  const context = useContext(TooltipContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Tooltip>.`);
  }
  return context;
}
function Tooltip({
  open,
  defaultOpen = false,
  onOpenChange,
  side = "top",
  align = "center",
  sideOffset = 6,
  delayDuration = 300,
  disabled = false,
  className,
  children
}) {
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const actualOpen = isControlled ? open : internalOpen;
  const [openedBy, setOpenedBy] = useState(actualOpen ? "focus" : null);
  const triggerRef = useRef(null);
  const hoveringRef = useRef(false);
  const openTimerRef = useRef(null);
  const reactId = useId();
  const contentId = `ds-tooltip-${reactId.replace(/:/g, "")}`;
  function cancelScheduledOpen() {
    if (openTimerRef.current !== null) {
      window.clearTimeout(openTimerRef.current);
      openTimerRef.current = null;
    }
  }
  function requestOpen(source) {
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
    requestOpen("focus");
  }
  function handleTriggerBlur() {
    if (hoveringRef.current) {
      if (openedBy === "focus") setOpenedBy("pointer");
      return;
    }
    requestClose();
  }
  useEffect(() => {
    if (disabled && actualOpen) requestClose();
  }, [disabled, actualOpen]);
  useEffect(() => {
    if (!actualOpen) return;
    function onKeyDown(event) {
      if (event.key === "Escape") requestClose();
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [actualOpen]);
  useEffect(() => cancelScheduledOpen, []);
  return <TooltipContext.Provider
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
      sideOffset
    }}
  >
      <span className={cx("relative inline-flex", className)}>{children}</span>
    </TooltipContext.Provider>;
}
function TooltipTrigger({ children }) {
  const context = useTooltip("TooltipTrigger");
  const child = Children.only(children);
  const childRef = child.ref;
  return cloneElement(child, {
    ref: composeRefs(context.triggerRef, childRef),
    "aria-describedby": context.contentId,
    onPointerEnter: (event) => {
      child.props.onPointerEnter?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerPointerEnter();
    },
    onPointerLeave: (event) => {
      child.props.onPointerLeave?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerPointerLeave();
    },
    onFocus: (event) => {
      child.props.onFocus?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerFocus();
    },
    onBlur: (event) => {
      child.props.onBlur?.(event);
      if (event.defaultPrevented) return;
      context.handleTriggerBlur();
    }
  });
}
function TooltipContent({ className, children, ...rest }) {
  const context = useTooltip("TooltipContent");
  const contentRef = useRef(null);
  const [resolved, setResolved] = useState({
    side: context.side,
    align: context.align
  });
  const [measured, setMeasured] = useState(false);
  const open = context.open;
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
      node.style.marginTop = side === "bottom" ? `${context.sideOffset}px` : "0px";
      node.style.marginBottom = side === "top" ? `${context.sideOffset}px` : "0px";
      node.style.marginLeft = side === "right" ? `${context.sideOffset}px` : "0px";
      node.style.marginRight = side === "left" ? `${context.sideOffset}px` : "0px";
      node.style.maxWidth = "";
      const cssCap = parseFloat(getComputedStyle(node).maxWidth);
      let available;
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
  }, [open, context.side, context.align, context.sideOffset]);
  if (!open) return null;
  const placement = `${resolved.side}-${resolved.align}`;
  return <div
    ref={contentRef}
    id={context.contentId}
    role="tooltip"
    className={cx(
      CONTENT_CLASSES,
      POSITION_CLASSES[placement],
      measured ? "opacity-100" : "opacity-0",
      className
    )}
    {...rest}
  >
      {children}
      <span
    aria-hidden="true"
    className={cx(ARROW_BASE_CLASSES, ARROW_BORDER_CLASSES[resolved.side], ARROW_POSITION_CLASSES[placement])}
  />
    </div>;
}

export { Tooltip, TooltipTrigger, TooltipContent };

export default Tooltip;
