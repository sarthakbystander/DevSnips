/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const CARD_CLASSES = "relative flex w-full min-w-0 flex-col rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]";
const HEADER_CLASSES = "grid grid-cols-[1fr_auto] items-start gap-x-4 gap-y-1.5 px-5 pt-5";
const TITLE_CLASSES = "col-start-1 text-lg font-semibold leading-[1.35] tracking-[-0.01em] text-[var(--ds-color-foreground)]";
const DESCRIPTION_CLASSES = "col-start-1 text-sm leading-5 text-[var(--ds-color-muted-foreground)]";
const ACTION_CLASSES = "col-start-2 row-start-1 flex shrink-0 items-center gap-1";
const CONTENT_CLASSES = "min-w-0 px-5 py-4";
const FOOTER_CLASSES = "mt-auto flex flex-col-reverse gap-2 px-5 pb-5 pt-4 sm:flex-row sm:items-center [&>button]:w-full sm:[&>button]:w-auto";
const MEDIA_ASPECT_CLASSES = {
  video: "aspect-video",
  square: "aspect-square",
  none: ""
};
const INTERACTIVE_CARD_CLASSES = "flex w-full min-w-0 flex-col rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-left text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const SELECTABLE_LABEL_BASE_CLASSES = "relative flex w-full min-w-0 cursor-pointer flex-col gap-1.5 rounded-[var(--ds-radius-md)] border bg-[var(--ds-color-surface)] p-4 text-left shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-within:border-[var(--ds-color-border-strong)] motion-reduce:transition-none";
const SELECTABLE_INPUT_CLASSES = "size-[18px] cursor-pointer appearance-none border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none";
const SKELETON_BLOCK_CLASSES = "animate-pulse rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-surface-active)] motion-reduce:animate-none";
function Card({ className, children, ...rest }) {
  return <div className={cx(CARD_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function CardHeader({ className, children, ...rest }) {
  return <div className={cx(HEADER_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function CardTitle({ className, children, ...rest }) {
  return <h3 className={cx(TITLE_CLASSES, className)} {...rest}>
      {children}
    </h3>;
}
function CardDescription({ className, children, ...rest }) {
  return <p className={cx(DESCRIPTION_CLASSES, className)} {...rest}>
      {children}
    </p>;
}
function CardAction({ className, children, ...rest }) {
  return <div className={cx(ACTION_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function CardContent({ className, children, ...rest }) {
  return <div className={cx(CONTENT_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
function CardFooter({ className, children, ...rest }) {
  return <div className={cx(FOOTER_CLASSES, className)} {...rest}>
      {children}
    </div>;
}
const MEDIA_FALLBACK_ICON = <svg
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
  </svg>;
function CardMedia({ src, alt = "", aspect = "video", className, ...rest }) {
  return <div
    className={cx(
      "shrink-0 overflow-hidden rounded-t-[calc(var(--ds-radius-md)-1px)] bg-[var(--ds-color-surface-subtle)]",
      MEDIA_ASPECT_CLASSES[aspect],
      className
    )}
  >
      {src ? <img src={src} alt={alt} loading="lazy" className="block h-full w-full object-cover" {...rest} /> : <div
    aria-hidden="true"
    className="flex h-full min-h-[6rem] w-full items-center justify-center text-[var(--ds-color-muted-foreground)]"
  >
          {MEDIA_FALLBACK_ICON}
        </div>}
    </div>;
}
function SelectableCard({
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
  className
}) {
  const generatedId = useId();
  const inputId = id ?? `selectable-card-${generatedId}`;
  const descId = `${inputId}-desc`;
  const isControlled = checked !== undefined;
  const [internal, setInternal] = useState(defaultChecked ?? false);
  const isChecked = isControlled ? checked : internal;
  const describedby = [description ? descId : null, ariaDescribedby].filter(Boolean).join(" ") || undefined;
  function handleChange(event) {
    if (!isControlled) setInternal(event.target.checked);
    onChange?.(event);
  }
  return <label
    htmlFor={inputId}
    className={cx(
      SELECTABLE_LABEL_BASE_CLASSES,
      disabled && "cursor-not-allowed opacity-60 hover:bg-[var(--ds-color-surface)]",
      isChecked ? "border-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)]",
      className
    )}
  >
      <span className="flex items-start justify-between gap-3">
        <span className="min-w-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
          {label}
          {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
        </span>
        <span className="relative mt-0.5 inline-flex size-[18px] shrink-0 items-center justify-center">
          <input
    id={inputId}
    type={type}
    className={cx(
      SELECTABLE_INPUT_CLASSES,
      type === "radio" ? "rounded-full border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)]" : "rounded-[var(--ds-radius-xs)] border-[var(--ds-color-border)] checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]"
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
      isChecked ? "opacity-100" : "opacity-0"
    )}
  >
            {type === "radio" ? <span className="block size-[8px] rounded-full bg-[var(--ds-color-primary)]" /> : <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 6 9 17l-5-5" />
              </svg>}
          </span>
        </span>
      </span>
      {description ? <span id={descId} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {description}
        </span> : null}
    </label>;
}
function SelectableCardGroup({
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
  className
}) {
  const generatedId = useId();
  const groupId = id ?? `selectable-card-group-${generatedId}`;
  const groupName = name ?? groupId;
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState(defaultValue);
  const selected = isControlled ? value : internal;
  function handleChange(option, event) {
    if (!isControlled) setInternal(option.value);
    onChange?.(option.value, event);
  }
  const gridCols = columns === 3 ? "sm:grid-cols-3" : columns === 2 ? "sm:grid-cols-2" : "grid-cols-1";
  return <fieldset id={groupId} className={cx("min-w-0 border-0 p-0", className)}>
      <legend className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {legend}
        {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
      </legend>
      <div className={cx("grid gap-3", gridCols)}>
        {options.map((option) => <SelectableCard
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
  />)}
      </div>
    </fieldset>;
}
function InteractiveCard(props) {
  if (props.href !== undefined) {
    const { className: className2, children: children2, ...rest2 } = props;
    return <a className={cx(INTERACTIVE_CARD_CLASSES, className2)} {...rest2}>
        {children2}
      </a>;
  }
  const { className, children, type, ...rest } = props;
  return <button type={type ?? "button"} className={cx(INTERACTIVE_CARD_CLASSES, className)} {...rest}>
      {children}
    </button>;
}
function CardSkeleton({ media = false, lines = 2, footer = false, label = "Loading\u2026", className }) {
  const lineCount = Math.max(1, Math.round(lines));
  return <Card aria-busy="true" className={className}>
      <span className="sr-only">{label}</span>
      <div aria-hidden="true">
        {media ? <div className={cx(SKELETON_BLOCK_CLASSES, "mx-5 mt-5 aspect-video")} /> : null}
        <div className={cx("flex flex-col gap-2 px-5", media ? "pt-4" : "pt-5", footer ? "pb-4" : "pb-5")}>
          <div className={cx(SKELETON_BLOCK_CLASSES, "h-4 w-2/5")} />
          {Array.from({ length: lineCount }, (_, i) => <div
    key={i}
    className={cx(SKELETON_BLOCK_CLASSES, "h-3", i === lineCount - 1 ? "w-3/5" : "w-full")}
  />)}
        </div>
        {footer ? <div className="flex gap-2 px-5 pb-5 pt-4">
            <div className={cx(SKELETON_BLOCK_CLASSES, "h-9 w-24")} />
            <div className={cx(SKELETON_BLOCK_CLASSES, "h-9 w-24")} />
          </div> : null}
      </div>
    </Card>;
}

export { Card, CardHeader, CardTitle, CardDescription, CardAction, CardContent, CardFooter, CardMedia, SelectableCard, SelectableCardGroup, InteractiveCard, CardSkeleton };

export default Card;
