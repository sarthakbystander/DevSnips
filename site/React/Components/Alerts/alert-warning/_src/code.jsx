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
  useMemo,
  useRef,
  useState
} from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const ROOT_BASE_CLASSES = "flex w-full min-w-0 items-start rounded-[var(--ds-radius-md)] border text-left text-[var(--ds-color-foreground)]";
const SIZE_CLASSES = {
  md: "gap-3 px-4 py-3",
  sm: "gap-2.5 px-3 py-2"
};
const VARIANT_CLASSES = {
  default: "border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]",
  info: "border-[color-mix(in_srgb,var(--ds-color-info)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-info)_7%,var(--ds-color-surface))]",
  success: "border-[color-mix(in_srgb,var(--ds-color-success)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-success)_8%,var(--ds-color-surface))]",
  warning: "border-[color-mix(in_srgb,var(--ds-color-warning)_40%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-warning)_10%,var(--ds-color-surface))]",
  destructive: "border-[color-mix(in_srgb,var(--ds-color-destructive)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-destructive)_7%,var(--ds-color-surface))]"
};
const DEFAULT_ROLE = {
  default: "status",
  info: "status",
  success: "status",
  warning: "alert",
  destructive: "alert"
};
const ICON_TONE_CLASSES = {
  default: "text-[var(--ds-color-muted-foreground)]",
  info: "text-[var(--ds-color-info)]",
  success: "text-[var(--ds-color-success)]",
  warning: "text-[var(--ds-color-warning)]",
  destructive: "text-[var(--ds-color-destructive)]"
};
const GLYPH_PROPS = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  className: "size-4"
};
const VARIANT_GLYPHS = {
  default: null,
  info: <svg {...GLYPH_PROPS}>
      <circle cx="12" cy="12" r="10" />
      <path d="M12 16v-4" />
      <path d="M12 8h.01" />
    </svg>,
  success: <svg {...GLYPH_PROPS}>
      <circle cx="12" cy="12" r="10" />
      <path d="m9 12 2 2 4-4" />
    </svg>,
  warning: <svg {...GLYPH_PROPS}>
      <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
      <path d="M12 9v4" />
      <path d="M12 17h.01" />
    </svg>,
  destructive: <svg {...GLYPH_PROPS}>
      <circle cx="12" cy="12" r="10" />
      <path d="m15 9-6 6" />
      <path d="m9 9 6 6" />
    </svg>
};
const CLOSE_GLYPH = <svg {...GLYPH_PROPS} className="size-3.5" aria-hidden="true">
    <path d="M18 6 6 18" />
    <path d="m6 6 12 12" />
  </svg>;
const FOCUSABLE_SELECTOR = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
function moveFocusOut(alertEl) {
  const candidates = Array.from(
    document.querySelectorAll(FOCUSABLE_SELECTOR)
  ).filter((el) => !alertEl.contains(el) && el.getClientRects().length > 0);
  const after = candidates.find(
    (el) => (alertEl.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0
  );
  const target = after ?? candidates[candidates.length - 1];
  target?.focus();
}
const AlertContext = createContext(null);
function useAlert(component) {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Alert>.`);
  }
  return context;
}
function Alert({
  variant = "default",
  size = "md",
  role,
  dismissible = false,
  open,
  defaultOpen = true,
  onDismiss,
  icon,
  closeLabel = "Dismiss alert",
  className,
  children,
  id,
  ...rest
}) {
  const generatedId = useId();
  const alertId = id ?? `alert-${generatedId}`;
  const titleId = `${alertId}-title`;
  const descriptionId = `${alertId}-description`;
  const [hasTitle, setHasTitle] = useState(false);
  const [hasDescription, setHasDescription] = useState(false);
  const registerTitle = useCallback(() => {
    setHasTitle(true);
    return () => setHasTitle(false);
  }, []);
  const registerDescription = useCallback(() => {
    setHasDescription(true);
    return () => setHasDescription(false);
  }, []);
  const isControlled = open !== undefined;
  const [internalOpen, setInternalOpen] = useState(defaultOpen);
  const isOpen = isControlled ? open : internalOpen;
  const rootRef = useRef(null);
  const dismiss = useCallback(() => {
    const el = rootRef.current;
    if (el && el.contains(document.activeElement)) moveFocusOut(el);
    if (!isControlled) setInternalOpen(false);
    onDismiss?.();
  }, [isControlled, onDismiss]);
  const context = useMemo(
    () => ({
      variant,
      size,
      titleId,
      descriptionId,
      hasTitle,
      hasDescription,
      registerTitle,
      registerDescription,
      dismiss,
      closeLabel
    }),
    [
      variant,
      size,
      titleId,
      descriptionId,
      hasTitle,
      hasDescription,
      registerTitle,
      registerDescription,
      dismiss,
      closeLabel
    ]
  );
  if (!isOpen) return null;
  const resolvedRole = role === undefined ? DEFAULT_ROLE[variant] : role ?? undefined;
  const showIcon = icon === undefined ? variant !== "default" : icon !== null && icon !== false;
  return <AlertContext.Provider value={context}>
      <div
    ref={rootRef}
    id={alertId}
    role={resolvedRole}
    aria-labelledby={hasTitle ? titleId : undefined}
    aria-describedby={hasDescription ? descriptionId : undefined}
    className={cx(ROOT_BASE_CLASSES, SIZE_CLASSES[size], VARIANT_CLASSES[variant], className)}
    {...rest}
  >
        {showIcon ? <AlertIcon>{icon === undefined ? undefined : icon}</AlertIcon> : null}
        <div className="flex min-w-0 flex-1 flex-col gap-1">{children}</div>
        {dismissible ? <AlertClose /> : null}
      </div>
    </AlertContext.Provider>;
}
function AlertIcon({ className, children, ...rest }) {
  const { variant } = useAlert("AlertIcon");
  return <span
    aria-hidden="true"
    className={cx(
      "mt-0.5 inline-flex size-4 shrink-0 items-center justify-center",
      ICON_TONE_CLASSES[variant],
      className
    )}
    {...rest}
  >
      {children ?? VARIANT_GLYPHS[variant]}
    </span>;
}
function AlertTitle({ className, children, ...rest }) {
  const context = useAlert("AlertTitle");
  useEffect(() => context.registerTitle(), [context]);
  return <p
    id={context.titleId}
    className={cx("m-0 break-words text-sm font-medium leading-5 text-[var(--ds-color-foreground)]", className)}
    {...rest}
  >
      {children}
    </p>;
}
function AlertDescription({ className, children, ...rest }) {
  const context = useAlert("AlertDescription");
  useEffect(() => context.registerDescription(), [context]);
  return <div
    id={context.descriptionId}
    className={cx("break-words text-sm leading-5 text-[var(--ds-color-muted-foreground)]", className)}
    {...rest}
  >
      {children}
    </div>;
}
function AlertAction({ className, children, ...rest }) {
  return <div className={cx("mt-1.5 flex flex-wrap items-center gap-2", className)} {...rest}>
      {children}
    </div>;
}
function AlertClose({
  label,
  className,
  onClick,
  type,
  children,
  ...rest
}) {
  const { dismiss, closeLabel, size } = useAlert("AlertClose");
  return <button
    type={type ?? "button"}
    aria-label={label ?? closeLabel}
    onClick={(event) => {
      onClick?.(event);
      if (!event.defaultPrevented) dismiss();
    }}
    className={cx(
      "inline-flex shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,currentColor_8%,transparent)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
      size === "sm" ? "-my-0.5 -mr-1.5 size-7" : "-my-1 -mr-2 size-8",
      className
    )}
    {...rest}
  >
      {children ?? CLOSE_GLYPH}
    </button>;
}

export { Alert, AlertIcon, AlertTitle, AlertDescription, AlertAction, AlertClose };

export default Alert;
