/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { createContext, useContext, useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const TRIGGER_CLASSES = "flex w-full min-w-0 items-center gap-3 px-4 py-3 text-left transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const CHEVRON = <svg
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  strokeWidth={1.75}
  strokeLinecap="round"
  strokeLinejoin="round"
  className="size-4"
  aria-hidden="true"
  focusable="false"
>
    <path d="m6 9 6 6 6-6" />
  </svg>;
const AccordionContext = createContext(null);
function useAccordion(component) {
  const context = useContext(AccordionContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Accordion>.`);
  }
  return context;
}
const AccordionItemContext = createContext(null);
function useAccordionItem(component) {
  const context = useContext(AccordionItemContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <AccordionItem>.`);
  }
  return context;
}
function toOpenList(value) {
  if (value == null) return [];
  return Array.isArray(value) ? value : [value];
}
function Accordion(props) {
  const {
    type = "single",
    collapsible = false,
    value,
    defaultValue,
    onValueChange,
    className,
    children,
    ...divProps
  } = props;
  const isMultiple = type === "multiple";
  const generatedId = useId();
  const accordionId = `accordion-${generatedId}`;
  const isControlled = value !== undefined;
  const [internalOpen, setInternalOpen] = useState(
    () => toOpenList(defaultValue)
  );
  const openValues = isControlled ? toOpenList(value) : internalOpen;
  const toggleItem = (itemValue) => {
    const open = openValues.includes(itemValue);
    let next;
    if (isMultiple) {
      next = open ? openValues.filter((entry) => entry !== itemValue) : [...openValues, itemValue];
    } else if (open) {
      if (!collapsible) return;
      next = [];
    } else {
      next = [itemValue];
    }
    if (!isControlled) setInternalOpen(next);
    onValueChange?.(
      isMultiple ? next : next[0] ?? null
    );
  };
  const context = {
    accordionId,
    isOpen: (itemValue) => openValues.includes(itemValue),
    toggleItem
  };
  return <AccordionContext.Provider value={context}>
      <div className={cx("w-full min-w-0", className)} {...divProps}>
        {children}
      </div>
    </AccordionContext.Provider>;
}
function AccordionItem({
  value,
  disabled = false,
  className,
  children,
  ...rest
}) {
  const { accordionId, isOpen, toggleItem } = useAccordion("AccordionItem");
  const open = isOpen(value);
  const context = {
    value,
    open,
    disabled,
    triggerId: `${accordionId}-trigger-${value}`,
    contentId: `${accordionId}-content-${value}`,
    toggle: () => {
      if (!disabled) toggleItem(value);
    }
  };
  return <AccordionItemContext.Provider value={context}>
      <div
    className={cx(
      "border-b border-[var(--ds-color-border)] last:border-b-0",
      className
    )}
    {...rest}
  >
        {children}
      </div>
    </AccordionItemContext.Provider>;
}
function AccordionTrigger({
  icon,
  badge,
  description,
  className,
  children,
  onClick,
  type,
  ...rest
}) {
  const { open, disabled, triggerId, contentId, toggle } = useAccordionItem("AccordionTrigger");
  return <h3 className="m-0 flex">
      <button
    type={type ?? "button"}
    id={triggerId}
    aria-expanded={open}
    aria-controls={contentId}
    disabled={disabled}
    onClick={(event) => {
      onClick?.(event);
      if (!event.defaultPrevented) toggle();
    }}
    className={cx(TRIGGER_CLASSES, className)}
    {...rest}
  >
        {icon != null && icon !== false ? <span
    aria-hidden="true"
    className="inline-flex size-4 shrink-0 items-center justify-center text-[var(--ds-color-muted-foreground)] [&_svg]:size-4"
  >
            {icon}
          </span> : null}
        <span className="flex min-w-0 flex-1 flex-col gap-0.5">
          <span className="break-words text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
            {children}
          </span>
          {description != null && description !== false ? <span className="break-words text-[13px] font-normal leading-5 text-[var(--ds-color-muted-foreground)]">
              {description}
            </span> : null}
        </span>
        {badge != null && badge !== false ? <span className="inline-flex h-5 shrink-0 items-center justify-center rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-1.5 text-[11px] font-medium leading-none text-[var(--ds-color-muted-foreground)]">
            {badge}
          </span> : null}
        <span
    aria-hidden="true"
    className={cx(
      "inline-flex size-4 shrink-0 items-center justify-center text-[var(--ds-color-muted-foreground)] transition-transform duration-200 ease-out motion-reduce:transition-none",
      open && "rotate-180"
    )}
  >
          {CHEVRON}
        </span>
      </button>
    </h3>;
}
function AccordionContent({
  className,
  children,
  ...rest
}) {
  const { open, triggerId, contentId } = useAccordionItem("AccordionContent");
  return <div
    id={contentId}
    role="region"
    aria-labelledby={triggerId}
    className={cx(
      "grid transition-[grid-template-rows] duration-200 ease-out motion-reduce:transition-none",
      open ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
    )}
  >
      <div
    className={cx(
      "min-h-0 overflow-hidden transition-[visibility] duration-200 motion-reduce:transition-none",
      open ? "visible" : "invisible"
    )}
  >
        <div
    className={cx(
      "break-words px-4 pb-4 text-sm leading-6 text-[var(--ds-color-muted-foreground)]",
      className
    )}
    {...rest}
  >
          {children}
        </div>
      </div>
    </div>;
}

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent };

export default Accordion;
