import { createContext, useContext, useId, useState } from "react";
import type { ButtonHTMLAttributes, HTMLAttributes, ReactNode } from "react";

/**
 * DevSnips React Accordion — description-trigger variant.
 *
 * The `description` prop on `<AccordionTrigger>` adds a muted 13px
 * supporting line under the title, inside the button — so it wraps with
 * the title and joins the accessible name. Hierarchy is typographic:
 * medium foreground title, muted second line. Shares the entire reference
 * core — only the registered demo content differs.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const TRIGGER_CLASSES =
  "flex w-full min-w-0 items-center gap-3 px-4 py-3 text-left transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";

const CHEVRON = (
  <svg
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
  </svg>
);

/* ------------------------------------------------------------------------ */
/* Accordion context (root state)                                            */
/* ------------------------------------------------------------------------ */

interface AccordionContextValue {
  accordionId: string;
  isOpen: (value: string) => boolean;
  toggleItem: (value: string) => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

function useAccordion(component: string): AccordionContextValue {
  const context = useContext(AccordionContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Accordion>.`);
  }
  return context;
}

/* ------------------------------------------------------------------------ */
/* AccordionItem context (per-item state)                                    */
/* ------------------------------------------------------------------------ */

interface AccordionItemContextValue {
  value: string;
  open: boolean;
  disabled: boolean;
  triggerId: string;
  contentId: string;
  toggle: () => void;
}

const AccordionItemContext = createContext<AccordionItemContextValue | null>(null);

function useAccordionItem(component: string): AccordionItemContextValue {
  const context = useContext(AccordionItemContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <AccordionItem>.`);
  }
  return context;
}

/* ------------------------------------------------------------------------ */
/* Accordion (root provider)                                                 */
/* ------------------------------------------------------------------------ */

// `defaultValue` is omitted from the forwarded div attributes because the
// Accordion API re-purposes it as the initial open value (the native
// attribute only applies to form fields).
interface AccordionBaseProps extends Omit<HTMLAttributes<HTMLDivElement>, "defaultValue"> {
  /**
   * Single mode only: allow the open item to be closed by activating its
   * trigger again. When `false` (default), activating the open item's
   * trigger is a no-op — exactly one item stays open once one has been
   * opened. Ignored when `type="multiple"` (items always toggle freely).
   */
  collapsible?: boolean;
  children?: ReactNode;
}

export interface AccordionSingleProps extends AccordionBaseProps {
  /** Expansion mode: at most one item open at a time (default). */
  type?: "single";
  /** Controlled open value (`null` = nothing open). */
  value?: string | null;
  /** Initial open value when uncontrolled. */
  defaultValue?: string | null;
  /** Called with the next open value (`null` when all items are closed). */
  onValueChange?: (value: string | null) => void;
}

export interface AccordionMultipleProps extends AccordionBaseProps {
  /** Expansion mode: all items may be open at once. */
  type: "multiple";
  /** Controlled open values. */
  value?: string[];
  /** Initial open values when uncontrolled. */
  defaultValue?: string[];
  /** Called with the next array of open values. */
  onValueChange?: (value: string[]) => void;
}

export type AccordionProps = AccordionSingleProps | AccordionMultipleProps;

/** Normalize a mode-shaped value to the internal open-value list. */
function toOpenList(value: string | string[] | null | undefined): string[] {
  if (value == null) return [];
  return Array.isArray(value) ? value : [value];
}

/**
 * The accordion root. Owns the open-item state and provides it to every
 * item. Internally the state is always a `string[]` of open values; the
 * single-mode API only ever stores zero or one entry. The public props are
 * a discriminated union so `value` / `onValueChange` always match `type`.
 */
export function Accordion(props: AccordionProps) {
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
  const [internalOpen, setInternalOpen] = useState<string[]>(() =>
    toOpenList(defaultValue),
  );
  const openValues = isControlled ? toOpenList(value) : internalOpen;

  const toggleItem = (itemValue: string): void => {
    const open = openValues.includes(itemValue);
    let next: string[];
    if (isMultiple) {
      next = open
        ? openValues.filter((entry) => entry !== itemValue)
        : [...openValues, itemValue];
    } else if (open) {
      if (!collapsible) return;
      next = [];
    } else {
      next = [itemValue];
    }
    if (!isControlled) setInternalOpen(next);
    // The public type guarantees the callback matches the mode: single
    // receives `string | null`, multiple receives `string[]`.
    (onValueChange as ((next: string | string[] | null) => void) | undefined)?.(
      isMultiple ? next : (next[0] ?? null),
    );
  };

  const context: AccordionContextValue = {
    accordionId,
    isOpen: (itemValue: string) => openValues.includes(itemValue),
    toggleItem,
  };

  return (
    <AccordionContext.Provider value={context}>
      <div className={cx("w-full min-w-0", className)} {...divProps}>
        {children}
      </div>
    </AccordionContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* AccordionItem                                                             */
/* ------------------------------------------------------------------------ */

export interface AccordionItemProps extends HTMLAttributes<HTMLDivElement> {
  /**
   * Unique, id-safe identifier for this item within the accordion. It keys
   * the open state and derives the trigger/region ids, so keep it stable
   * and free of whitespace.
   */
  value: string;
  /** Disable the item: the trigger cannot be focused or activated. */
  disabled?: boolean;
  children?: ReactNode;
}

/**
 * One accordion entry: a bordered row in the divided list (`border-b`,
 * removed on the last item). Computes its open state from the root and
 * derives the stable trigger/region ids that wire the disclosure
 * relationship.
 */
export function AccordionItem({
  value,
  disabled = false,
  className,
  children,
  ...rest
}: AccordionItemProps) {
  const { accordionId, isOpen, toggleItem } = useAccordion("AccordionItem");
  const open = isOpen(value);
  const context: AccordionItemContextValue = {
    value,
    open,
    disabled,
    triggerId: `${accordionId}-trigger-${value}`,
    contentId: `${accordionId}-content-${value}`,
    toggle: () => {
      if (!disabled) toggleItem(value);
    },
  };
  return (
    <AccordionItemContext.Provider value={context}>
      <div
        className={cx(
          "border-b border-[var(--ds-color-border)] last:border-b-0",
          className,
        )}
        {...rest}
      >
        {children}
      </div>
    </AccordionItemContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* AccordionTrigger                                                          */
/* ------------------------------------------------------------------------ */

// `disabled` lives on AccordionItem (it disables the whole item), so it is
// omitted from the forwarded button attributes.
export interface AccordionTriggerProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "disabled"> {
  /**
   * Leading visual affordance (an icon). Rendered `aria-hidden` — it must
   * supplement the trigger text, never replace it.
   */
  icon?: ReactNode;
  /**
   * Short status/count text rendered as a neutral pill at the trailing
   * edge (for example `"3"`, `"Beta"`, `"4 errors"`). It is plain text
   * inside the button, so it becomes part of the trigger's accessible
   * name — keep it short and meaningful.
   */
  badge?: ReactNode;
  /**
   * A short supporting line rendered under the title. It is part of the
   * button's accessible name, so keep it brief.
   */
  description?: ReactNode;
  children?: ReactNode;
}

/**
 * The disclosure control: a real `<button type="button">` inside an `<h3>`
 * heading (so the accordion participates in the page outline). Exposes
 * `aria-expanded` + `aria-controls` pointing at the region, toggles on
 * native button activation (click, Enter, Space), and carries the trailing
 * chevron that rotates when open (`aria-hidden` — the state is exposed by
 * `aria-expanded`, not by the glyph). A custom `onClick` runs first and may
 * veto the toggle with `event.preventDefault()`. The focus ring is drawn
 * inset (`-outline-offset-2`) so full-bleed triggers inside bordered
 * containers keep an unclipped ring.
 */
export function AccordionTrigger({
  icon,
  badge,
  description,
  className,
  children,
  onClick,
  type,
  ...rest
}: AccordionTriggerProps) {
  const { open, disabled, triggerId, contentId, toggle } =
    useAccordionItem("AccordionTrigger");
  return (
    <h3 className="m-0 flex">
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
        {icon != null && icon !== false ? (
          <span
            aria-hidden="true"
            className="inline-flex size-4 shrink-0 items-center justify-center text-[var(--ds-color-muted-foreground)] [&_svg]:size-4"
          >
            {icon}
          </span>
        ) : null}
        <span className="flex min-w-0 flex-1 flex-col gap-0.5">
          <span className="break-words text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
            {children}
          </span>
          {description != null && description !== false ? (
            <span className="break-words text-[13px] font-normal leading-5 text-[var(--ds-color-muted-foreground)]">
              {description}
            </span>
          ) : null}
        </span>
        {badge != null && badge !== false ? (
          <span className="inline-flex h-5 shrink-0 items-center justify-center rounded-[var(--ds-radius-full)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] px-1.5 text-[11px] font-medium leading-none text-[var(--ds-color-muted-foreground)]">
            {badge}
          </span>
        ) : null}
        <span
          aria-hidden="true"
          className={cx(
            "inline-flex size-4 shrink-0 items-center justify-center text-[var(--ds-color-muted-foreground)] transition-transform duration-200 ease-out motion-reduce:transition-none",
            open && "rotate-180",
          )}
        >
          {CHEVRON}
        </span>
      </button>
    </h3>
  );
}

/* ------------------------------------------------------------------------ */
/* AccordionContent                                                          */
/* ------------------------------------------------------------------------ */

export interface AccordionContentProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

/**
 * The collapsible region: `role="region"` labelled by its trigger, with the
 * stable id the trigger's `aria-controls` references. Height animates via
 * the CSS grid-rows trick (0fr <-> 1fr) — no JavaScript measurement — and a
 * discrete `visibility` transition hides the region from the accessibility
 * tree and tab order the moment the close transition completes (instantly
 * under `prefers-reduced-motion`). The region stays mounted while closed so
 * state inside it survives. `className` and forwarded attributes (for
 * example `aria-busy`) land on the inner content div.
 */
export function AccordionContent({
  className,
  children,
  ...rest
}: AccordionContentProps) {
  const { open, triggerId, contentId } = useAccordionItem("AccordionContent");
  return (
    <div
      id={contentId}
      role="region"
      aria-labelledby={triggerId}
      className={cx(
        "grid transition-[grid-template-rows] duration-200 ease-out motion-reduce:transition-none",
        open ? "grid-rows-[1fr]" : "grid-rows-[0fr]",
      )}
    >
      <div
        className={cx(
          "min-h-0 overflow-hidden transition-[visibility] duration-200 motion-reduce:transition-none",
          open ? "visible" : "invisible",
        )}
      >
        <div
          className={cx(
            "break-words px-4 pb-4 text-sm leading-6 text-[var(--ds-color-muted-foreground)]",
            className,
          )}
          {...rest}
        >
          {children}
        </div>
      </div>
    </div>
  );
}

export default Accordion;
