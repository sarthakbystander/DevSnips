import { useId, useState } from "react";
import type {
  AnchorHTMLAttributes,
  ButtonHTMLAttributes,
  ChangeEvent,
  HTMLAttributes,
  ImgHTMLAttributes,
  ReactNode,
} from "react";

/**
 * DevSnips React Card — List collection.
 *
 * The shared card core; this variant demonstrates the list pattern: a real
 * `<ul>`/`<li>` grid of composed cards (header + meta + footer) with
 * consistent gaps and per-item accessible actions — the reusable component,
 * not a new grid framework.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const CARD_CLASSES =
  "relative flex w-full min-w-0 flex-col rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]";
// Grid with a text column and an auto-sized action column: the title and
// description stack in column 1 and an optional CardAction sits at the top
// of column 2. With no action the second column collapses to zero width.
const HEADER_CLASSES =
  "grid grid-cols-[1fr_auto] items-start gap-x-4 gap-y-1.5 px-5 pt-5";
const TITLE_CLASSES =
  "col-start-1 text-lg font-semibold leading-[1.35] tracking-[-0.01em] text-[var(--ds-color-foreground)]";
const DESCRIPTION_CLASSES =
  "col-start-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
const ACTION_CLASSES = "col-start-2 row-start-1 flex shrink-0 items-center gap-1";
const CONTENT_CLASSES = "min-w-0 px-5 py-4";
// Mirrors the dialog footer: actions stack full-width below `sm` (primary
// last in DOM so it lands on top), lay out inline from `sm` up. Alignment is
// intentionally unset — pass `sm:justify-end` or `sm:justify-between` via
// className (no baked-in justify utility, so overrides never conflict).
const FOOTER_CLASSES =
  "mt-auto flex flex-col-reverse gap-2 px-5 pb-5 pt-4 sm:flex-row sm:items-center [&>button]:w-full sm:[&>button]:w-auto";
const MEDIA_ASPECT_CLASSES: Record<CardMediaAspect, string> = {
  video: "aspect-video",
  square: "aspect-square",
  none: "",
};
const INTERACTIVE_CARD_CLASSES =
  "flex w-full min-w-0 flex-col rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-left text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const SELECTABLE_LABEL_BASE_CLASSES =
  "relative flex w-full min-w-0 cursor-pointer flex-col gap-1.5 rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-4 text-left shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-within:border-[var(--ds-color-border-strong)] motion-reduce:transition-none";
const SELECTABLE_INPUT_CLASSES =
  "size-[18px] cursor-pointer appearance-none border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none";
const SKELETON_BLOCK_CLASSES =
  "animate-pulse rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-surface-active)] motion-reduce:animate-none";

/* ------------------------------------------------------------------------ */
/* Card (root surface)                                                       */
/* ------------------------------------------------------------------------ */

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  children?: ReactNode;
}

export function Card({ className, children, ...rest }: CardProps) {
  return (
    <div className={cx(CARD_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* CardHeader / CardTitle / CardDescription / CardAction                     */
/* ------------------------------------------------------------------------ */

export interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  children?: ReactNode;
}

export function CardHeader({ className, children, ...rest }: CardHeaderProps) {
  return (
    <div className={cx(HEADER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export interface CardTitleProps extends HTMLAttributes<HTMLHeadingElement> {
  className?: string;
  children?: ReactNode;
}

/** Real `<h3>` heading — cards are page regions, so titles are headings. */
export function CardTitle({ className, children, ...rest }: CardTitleProps) {
  return (
    <h3 className={cx(TITLE_CLASSES, className)} {...rest}>
      {children}
    </h3>
  );
}

export interface CardDescriptionProps extends HTMLAttributes<HTMLParagraphElement> {
  className?: string;
  children?: ReactNode;
}

export function CardDescription({ className, children, ...rest }: CardDescriptionProps) {
  return (
    <p className={cx(DESCRIPTION_CLASSES, className)} {...rest}>
      {children}
    </p>
  );
}

export interface CardActionProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  children?: ReactNode;
}

/** Header action slot (icon buttons, a menu trigger) — top-right of the header. */
export function CardAction({ className, children, ...rest }: CardActionProps) {
  return (
    <div className={cx(ACTION_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* CardContent / CardFooter                                                  */
/* ------------------------------------------------------------------------ */

export interface CardContentProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  children?: ReactNode;
}

export function CardContent({ className, children, ...rest }: CardContentProps) {
  return (
    <div className={cx(CONTENT_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

export interface CardFooterProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
  children?: ReactNode;
}

export function CardFooter({ className, children, ...rest }: CardFooterProps) {
  return (
    <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* CardMedia                                                                 */
/* ------------------------------------------------------------------------ */

export type CardMediaAspect = "video" | "square" | "none";

export interface CardMediaProps extends ImgHTMLAttributes<HTMLImageElement> {
  /**
   * Image URL. When omitted, a decorative `aria-hidden` placeholder surface
   * renders instead (the layout never collapses on a missing image).
   */
  src?: string;
  /** Alternative text. Defaults to `""` (decorative); meaningful images must pass real alt text. */
  alt?: string;
  /** Crop box: `video` 16:9 (default), `square` 1:1, `none` natural height (for fixed-size layouts such as horizontal cards). */
  aspect?: CardMediaAspect;
  /** Extra classes on the media frame (the image always fills it with `object-cover`). */
  className?: string;
}

const MEDIA_FALLBACK_ICON = (
  <svg
    className="size-6"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    focusable="false"
  >
    <rect width="18" height="18" x="3" y="3" rx="2" />
    <circle cx="9" cy="9" r="2" />
    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
  </svg>
);

export function CardMedia({ src, alt = "", aspect = "video", className, ...rest }: CardMediaProps) {
  return (
    <div
      className={cx(
        "shrink-0 overflow-hidden rounded-t-[calc(var(--ds-radius-md)-1px)] bg-[var(--ds-color-surface-subtle)]",
        MEDIA_ASPECT_CLASSES[aspect],
        className,
      )}
    >
      {src ? (
        <img src={src} alt={alt} loading="lazy" className="block h-full w-full object-cover" {...rest} />
      ) : (
        <div
          aria-hidden="true"
          className="flex h-full min-h-[6rem] w-full items-center justify-center text-[var(--ds-color-muted-foreground)]"
        >
          {MEDIA_FALLBACK_ICON}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* SelectableCard (real radio / checkbox, card as label)                     */
/* ------------------------------------------------------------------------ */

export interface SelectableCardProps {
  /** `checkbox` (default) for independent multi-select; `radio` for a single choice within a `name` group — use `SelectableCardGroup` to manage the group. */
  type?: "radio" | "checkbox";
  /** Visible card label (also the input's accessible name). */
  label: ReactNode;
  /** Supporting text; wired to the input via `aria-describedby`. */
  description?: ReactNode;
  checked?: boolean;
  defaultChecked?: boolean;
  onChange?: (event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  name?: string;
  value?: string | number | readonly string[];
  id?: string;
  "aria-describedby"?: string;
  className?: string;
}

/**
 * A selectable card: the whole card is the `<label>` of a real native
 * `<input type="radio">` / `type="checkbox">`, so clicking anywhere on the
 * card toggles the input and all native behavior (Space toggling, arrow-key
 * radio navigation, form submission) works. The selected state is tracked
 * from React state (controlled `checked` + `onChange`, or uncontrolled
 * `defaultChecked`) so it stays correct in both modes; it is shown with a
 * primary border plus the visible control — never color alone.
 */
export function SelectableCard({
  type = "checkbox",
  label,
  description,
  checked,
  defaultChecked,
  onChange,
  disabled,
  required,
  name,
  value,
  id,
  "aria-describedby": ariaDescribedby,
  className,
}: SelectableCardProps) {
  const generatedId = useId();
  const inputId = id ?? `selectable-card-${generatedId}`;
  const descId = `${inputId}-desc`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState<boolean>(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  const describedby = [description ? descId : null, ariaDescribedby].filter(Boolean).join(" ") || undefined;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }

  return (
    <label
      htmlFor={inputId}
      className={cx(
        SELECTABLE_LABEL_BASE_CLASSES,
        disabled && "cursor-not-allowed opacity-60 hover:bg-[var(--ds-color-surface)]",
        isChecked ? "border-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)]",
        className,
      )}
    >
      <span className="flex items-start justify-between gap-3">
        <span className="min-w-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
          {label}
          {required ? (
            <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
          ) : null}
        </span>
        <span className="relative mt-0.5 inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
            id={inputId}
            type={type}
            className={cx(
              SELECTABLE_INPUT_CLASSES,
              type === "radio"
                ? "rounded-full border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)]"
                : "rounded-[var(--ds-radius-xs)] border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]",
            )}
            checked={isControlled ? isChecked : undefined}
            defaultChecked={isControlled ? undefined : defaultChecked}
            disabled={disabled}
            required={required}
            aria-describedby={describedby}
            name={name}
            value={value}
            onChange={handleChange}
          />
          <span
            aria-hidden="true"
            className={cx(
              "pointer-events-none absolute inset-0 flex items-center justify-center transition-opacity duration-150 motion-reduce:transition-none",
              type === "checkbox" && "text-[var(--ds-color-primary-foreground)]",
              isChecked ? "opacity-100" : "opacity-0",
            )}
          >
            {type === "radio" ? (
              <span className="block size-[8px] rounded-full bg-[var(--ds-color-primary)]" />
            ) : (
              <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 6 9 17l-5-5" />
              </svg>
            )}
          </span>
        </span>
      </span>
      {description ? (
        <span id={descId} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {description}
        </span>
      ) : null}
    </label>
  );
}

/* ------------------------------------------------------------------------ */
/* SelectableCardGroup (single-choice fieldset of selectable cards)          */
/* ------------------------------------------------------------------------ */

export interface SelectableCardOption {
  value: string;
  label: ReactNode;
  description?: ReactNode;
  disabled?: boolean;
}

export interface SelectableCardGroupProps {
  /** Visible `<legend>` for the fieldset. */
  legend: ReactNode;
  options: SelectableCardOption[];
  /** Selected option value (controlled). */
  value?: string;
  /** Initially selected option value (uncontrolled). */
  defaultValue?: string;
  onChange?: (value: string, event: ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  name?: string;
  id?: string;
  /** Card columns from `sm` up (1, 2, or 3). */
  columns?: 1 | 2 | 3;
  className?: string;
}

/**
 * A single-choice group of selectable cards inside a `<fieldset>`/`<legend>`.
 * The group owns the selected value (controlled `value` + `onChange`, or
 * uncontrolled `defaultValue`) and passes it down as controlled `checked`, so
 * every card's selected state stays in sync even in uncontrolled mode —
 * where a deselected radio receives no change event of its own. Keyboard
 * users get the browser's native radio-group arrow-key navigation.
 */
export function SelectableCardGroup({
  legend,
  options,
  value,
  defaultValue = "",
  onChange,
  disabled,
  required,
  name,
  id,
  columns = 1,
  className,
}: SelectableCardGroupProps) {
  const generatedId = useId();
  const groupId = id ?? `selectable-card-group-${generatedId}`;
  const groupName = name ?? groupId;
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState<string>(defaultValue);
  const selected = isControlled ? value : internal;

  function handleChange(option: SelectableCardOption, event: ChangeEvent<HTMLInputElement>) {
    if (!isControlled) setInternal(option.value);
    onChange?.(option.value, event);
  }

  const gridCols = columns === 3 ? "sm:grid-cols-3" : columns === 2 ? "sm:grid-cols-2" : "grid-cols-1";

  return (
    <fieldset id={groupId} className={cx("min-w-0 border-0 p-0", className)}>
      <legend className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {legend}
        {required ? (
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
        ) : null}
      </legend>
      <div className={cx("grid gap-3", gridCols)}>
        {options.map((option) => (
          <SelectableCard
            key={option.value}
            type="radio"
            label={option.label}
            description={option.description}
            name={groupName}
            value={option.value}
            checked={selected === option.value}
            disabled={option.disabled || disabled}
            required={required}
            onChange={(event) => handleChange(option, event)}
          />
        ))}
      </div>
    </fieldset>
  );
}

/* ------------------------------------------------------------------------ */
/* InteractiveCard (real anchor for navigation, real button for actions)     */
/* ------------------------------------------------------------------------ */

interface InteractiveCardSharedProps {
  className?: string;
  children?: ReactNode;
}

export interface InteractiveCardAnchorProps
  extends InteractiveCardSharedProps,
    AnchorHTMLAttributes<HTMLAnchorElement> {
  /** Destination URL — renders a real `<a>` with normal browser navigation. */
  href: string;
}

export interface InteractiveCardButtonProps
  extends InteractiveCardSharedProps,
    ButtonHTMLAttributes<HTMLButtonElement> {
  href?: undefined;
}

export type InteractiveCardProps = InteractiveCardAnchorProps | InteractiveCardButtonProps;

/**
 * A card that is itself the interactive element — never a `<div>` with a
 * click handler. With `href` it renders a real anchor (navigation: middle-
 * click, open-in-new-tab, and screen-reader link semantics all work);
 * without `href` it renders a real `<button type="button">` (actions), which
 * also carries the only meaningful `disabled` state. Because the whole card
 * is one control, keep other interactive elements (links, buttons, menus)
 * out of its children — nested interactive elements are invalid and confuse
 * activation. Put secondary actions in a sibling card's `CardAction` instead.
 */
export function InteractiveCard(props: InteractiveCardProps) {
  if (props.href !== undefined) {
    const { className, children, ...rest } = props;
    return (
      <a className={cx(INTERACTIVE_CARD_CLASSES, className)} {...rest}>
        {children}
      </a>
    );
  }
  const { className, children, type, ...rest } = props;
  return (
    <button type={type ?? "button"} className={cx(INTERACTIVE_CARD_CLASSES, className)} {...rest}>
      {children}
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* CardSkeleton (loading placeholder)                                        */
/* ------------------------------------------------------------------------ */

export interface CardSkeletonProps {
  /** Render a media placeholder block (16:9) at the top of the card. */
  media?: boolean;
  /** Number of body text lines (default 2). */
  lines?: number;
  /** Render an action-row placeholder in the footer position. */
  footer?: boolean;
  /** Visually hidden loading announcement (default "Loading…"). */
  label?: string;
  className?: string;
}

/**
 * Loading placeholder matching the real card's geometry, so content swaps in
 * without layout shift. The card carries `aria-busy="true"` plus a visually
 * hidden loading label; the placeholder blocks are `aria-hidden`. The pulse
 * is a restrained opacity animation and is disabled under
 * `prefers-reduced-motion`.
 */
export function CardSkeleton({ media = false, lines = 2, footer = false, label = "Loading…", className }: CardSkeletonProps) {
  const lineCount = Math.max(1, Math.round(lines));
  return (
    <Card aria-busy="true" className={className}>
      <span className="sr-only">{label}</span>
      <div aria-hidden="true">
        {media ? <div className={cx(SKELETON_BLOCK_CLASSES, "mx-5 mt-5 aspect-video")} /> : null}
        <div className={cx("flex flex-col gap-2 px-5", media ? "pt-4" : "pt-5", footer ? "pb-4" : "pb-5")}>
          <div className={cx(SKELETON_BLOCK_CLASSES, "h-4 w-2/5")} />
          {Array.from({ length: lineCount }, (_, i) => (
            <div
              key={i}
              className={cx(SKELETON_BLOCK_CLASSES, "h-3", i === lineCount - 1 ? "w-3/5" : "w-full")}
            />
          ))}
        </div>
        {footer ? (
          <div className="flex gap-2 px-5 pb-5 pt-4">
            <div className={cx(SKELETON_BLOCK_CLASSES, "h-9 w-24")} />
            <div className={cx(SKELETON_BLOCK_CLASSES, "h-9 w-24")} />
          </div>
        ) : null}
      </div>
    </Card>
  );
}

export default Card;
