import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
} from "react";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  ReactNode,
} from "react";

/**
 * DevSnips React Alert — Compact density.
 *
 * The shared alert core; this variant demonstrates `size="sm"`: reduced
 * padding and gaps for dense interfaces (settings panels, inspectors), with
 * the same compound API, live-region roles, and wrapping behavior. Density
 * is a prop — not a className override — so it never conflicts with the
 * base spacing utilities.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type AlertVariant = "default" | "info" | "success" | "warning" | "destructive";
export type AlertSize = "md" | "sm";
export type AlertRole = "status" | "alert";

const ROOT_BASE_CLASSES =
  "flex w-full min-w-0 items-start rounded-[var(--ds-radius-md)] border text-left text-[var(--ds-color-foreground)]";

const SIZE_CLASSES: Record<AlertSize, string> = {
  md: "gap-3 px-4 py-3",
  sm: "gap-2.5 px-3 py-2",
};

// Semantic variants derive their tint from the semantic token via color-mix
// (the same derivation recipe the buttons use for hover), so no component-
// specific color values are invented and dark mode stays in sync for free.
const VARIANT_CLASSES: Record<AlertVariant, string> = {
  default:
    "border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]",
  info: "border-[color-mix(in_srgb,var(--ds-color-info)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-info)_7%,var(--ds-color-surface))]",
  success:
    "border-[color-mix(in_srgb,var(--ds-color-success)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-success)_8%,var(--ds-color-surface))]",
  warning:
    "border-[color-mix(in_srgb,var(--ds-color-warning)_40%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-warning)_10%,var(--ds-color-surface))]",
  destructive:
    "border-[color-mix(in_srgb,var(--ds-color-destructive)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-destructive)_7%,var(--ds-color-surface))]",
};

// Urgency, not decoration: informational feedback is polite, failures and
// cautions that need prompt attention are assertive. Matches the live-region
// conventions used across the DevSnips notification patterns.
const DEFAULT_ROLE: Record<AlertVariant, AlertRole> = {
  default: "status",
  info: "status",
  success: "status",
  warning: "alert",
  destructive: "alert",
};

const ICON_TONE_CLASSES: Record<AlertVariant, string> = {
  default: "text-[var(--ds-color-muted-foreground)]",
  info: "text-[var(--ds-color-info)]",
  success: "text-[var(--ds-color-success)]",
  warning: "text-[var(--ds-color-warning)]",
  destructive: "text-[var(--ds-color-destructive)]",
};

const GLYPH_PROPS = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  className: "size-4",
} as const;

// Small, restrained status glyphs (lucide-style, 24px grid, currentColor).
// They are supplements to the text + role, never the sole carrier of meaning.
const VARIANT_GLYPHS: Record<AlertVariant, ReactNode> = {
  default: null,
  info: (
    <svg {...GLYPH_PROPS}>
      <circle cx="12" cy="12" r="10" />
      <path d="M12 16v-4" />
      <path d="M12 8h.01" />
    </svg>
  ),
  success: (
    <svg {...GLYPH_PROPS}>
      <circle cx="12" cy="12" r="10" />
      <path d="m9 12 2 2 4-4" />
    </svg>
  ),
  warning: (
    <svg {...GLYPH_PROPS}>
      <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
      <path d="M12 9v4" />
      <path d="M12 17h.01" />
    </svg>
  ),
  destructive: (
    <svg {...GLYPH_PROPS}>
      <circle cx="12" cy="12" r="10" />
      <path d="m15 9-6 6" />
      <path d="m9 9 6 6" />
    </svg>
  ),
};

const CLOSE_GLYPH = (
  <svg {...GLYPH_PROPS} className="size-3.5" aria-hidden="true">
    <path d="M18 6 6 18" />
    <path d="m6 6 12 12" />
  </svg>
);

const FOCUSABLE_SELECTOR =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

// When dismissal removes the focused close button from the DOM, the browser
// would drop focus to <body>. Move focus to the next operable element in
// document order (or the previous one at the end of the page) BEFORE the
// alert unmounts, so keyboard users never lose their place.
function moveFocusOut(alertEl: HTMLElement): void {
  const candidates = Array.from(
    document.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR),
  ).filter((el) => !alertEl.contains(el) && el.getClientRects().length > 0);
  const after = candidates.find(
    (el) => (alertEl.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0,
  );
  const target = after ?? candidates[candidates.length - 1];
  target?.focus();
}

/* ------------------------------------------------------------------------ */
/* Alert context                                                             */
/* ------------------------------------------------------------------------ */

interface AlertContextValue {
  variant: AlertVariant;
  size: AlertSize;
  titleId: string;
  descriptionId: string;
  hasTitle: boolean;
  hasDescription: boolean;
  registerTitle(): () => void;
  registerDescription(): () => void;
  dismiss(): void;
  closeLabel: string;
}

const AlertContext = createContext<AlertContextValue | null>(null);

function useAlert(component: string): AlertContextValue {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Alert>.`);
  }
  return context;
}

/* ------------------------------------------------------------------------ */
/* Alert (root surface + dismissal state)                                    */
/* ------------------------------------------------------------------------ */

// `role` and `size` are omitted from the forwarded div attributes because the
// Alert API narrows them (`role` is limited to live-region roles, `size` is
// the density scale, not the obsolete HTML attribute).
export interface AlertProps extends Omit<HTMLAttributes<HTMLDivElement>, "role" | "size"> {
  /** Semantic intent: colors the surface, picks the default icon and role. */
  variant?: AlertVariant;
  /** Density: `md` default, `sm` for dense interfaces (reduced padding/gap). */
  size?: AlertSize;
  /**
   * Live-region role. Defaults to `status` (polite) for default/info/success
   * and `alert` (assertive) for warning/destructive. Pass `null` for static
   * page content that must not announce itself.
   */
  role?: AlertRole | null;
  /** Render a trailing `AlertClose` button wired to the dismissal state. */
  dismissible?: boolean;
  /** Controlled visibility (with `onDismiss`). */
  open?: boolean;
  /** Initial visibility when uncontrolled (default `true`). */
  defaultOpen?: boolean;
  /** Called when the user dismisses the alert (close button activated). */
  onDismiss?: () => void;
  /**
   * Leading icon: `undefined` renders the variant's semantic glyph (none for
   * `default`), a ReactNode replaces it, and `null` hides the icon entirely.
   */
  icon?: ReactNode;
  /** Accessible name for the auto-rendered close button. */
  closeLabel?: string;
  className?: string;
  children?: ReactNode;
}

export function Alert({
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
}: AlertProps) {
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
  const rootRef = useRef<HTMLDivElement | null>(null);

  const dismiss = useCallback(() => {
    const el = rootRef.current;
    if (el && el.contains(document.activeElement)) moveFocusOut(el);
    if (!isControlled) setInternalOpen(false);
    onDismiss?.();
  }, [isControlled, onDismiss]);

  const context = useMemo<AlertContextValue>(
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
      closeLabel,
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
      closeLabel,
    ],
  );

  if (!isOpen) return null;

  const resolvedRole = role === undefined ? DEFAULT_ROLE[variant] : role ?? undefined;
  const showIcon =
    icon === undefined ? variant !== "default" : icon !== null && icon !== false;

  return (
    <AlertContext.Provider value={context}>
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
    </AlertContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* AlertIcon                                                                 */
/* ------------------------------------------------------------------------ */

export interface AlertIconProps extends HTMLAttributes<HTMLSpanElement> {
  /** Custom glyph; defaults to the alert variant's semantic icon. */
  children?: ReactNode;
}

/**
 * The leading icon slot. Always `aria-hidden`: the icon supplements the
 * variant's role + text, it never carries meaning on its own (so there is
 * nothing to hide from — and nothing lost for — assistive technology).
 */
export function AlertIcon({ className, children, ...rest }: AlertIconProps) {
  const { variant } = useAlert("AlertIcon");
  return (
    <span
      aria-hidden="true"
      className={cx(
        "mt-0.5 inline-flex size-4 shrink-0 items-center justify-center",
        ICON_TONE_CLASSES[variant],
        className,
      )}
      {...rest}
    >
      {children ?? VARIANT_GLYPHS[variant]}
    </span>
  );
}

/* ------------------------------------------------------------------------ */
/* AlertTitle / AlertDescription                                             */
/* ------------------------------------------------------------------------ */

export interface AlertTitleProps extends HTMLAttributes<HTMLParagraphElement> {
  children?: ReactNode;
}

/**
 * The alert's headline — a styled `<p>`, not a heading: alerts are feedback
 * regions, not document structure, so they stay out of the page outline.
 * Registers itself so the root wires `aria-labelledby` only when a title
 * exists.
 */
export function AlertTitle({ className, children, ...rest }: AlertTitleProps) {
  const context = useAlert("AlertTitle");
  useEffect(() => context.registerTitle(), [context]);
  return (
    <p
      id={context.titleId}
      className={cx("m-0 break-words text-sm font-medium leading-5 text-[var(--ds-color-foreground)]", className)}
      {...rest}
    >
      {children}
    </p>
  );
}

export interface AlertDescriptionProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

/**
 * Supporting content (a `<div>`, so lists and links are valid children).
 * Registers itself so the root wires `aria-describedby` only when a
 * description exists.
 */
export function AlertDescription({ className, children, ...rest }: AlertDescriptionProps) {
  const context = useAlert("AlertDescription");
  useEffect(() => context.registerDescription(), [context]);
  return (
    <div
      id={context.descriptionId}
      className={cx("break-words text-sm leading-5 text-[var(--ds-color-muted-foreground)]", className)}
      {...rest}
    >
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* AlertAction                                                               */
/* ------------------------------------------------------------------------ */

export interface AlertActionProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

/**
 * The actions row, rendered inside the text column below the description.
 * `flex-wrap` keeps real `<button>` / `<a>` children usable at narrow
 * widths — they wrap instead of overflowing. Compose only real controls
 * here; never put a control inside another control.
 */
export function AlertAction({ className, children, ...rest }: AlertActionProps) {
  return (
    <div className={cx("mt-1.5 flex flex-wrap items-center gap-2", className)} {...rest}>
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* AlertClose                                                                */
/* ------------------------------------------------------------------------ */

export interface AlertCloseProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Accessible name (icon-only button); defaults to the root's `closeLabel`. */
  label?: string;
}

/**
 * A real `<button type="button">` that dismisses the nearest `<Alert>`.
 * Icon-only, so it always carries an accessible name; keyboard users reach
 * it with Tab and activate it with Enter/Space. Call `event.preventDefault()`
 * from a custom `onClick` to veto the dismissal.
 */
export function AlertClose({
  label,
  className,
  onClick,
  type,
  children,
  ...rest
}: AlertCloseProps) {
  const { dismiss, closeLabel, size } = useAlert("AlertClose");
  return (
    <button
      type={type ?? "button"}
      aria-label={label ?? closeLabel}
      onClick={(event) => {
        onClick?.(event);
        if (!event.defaultPrevented) dismiss();
      }}
      className={cx(
        "inline-flex shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,currentColor_8%,transparent)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
        size === "sm" ? "-my-0.5 -mr-1.5 size-7" : "-my-1 -mr-2 size-8",
        className,
      )}
      {...rest}
    >
      {children ?? CLOSE_GLYPH}
    </button>
  );
}

export default Alert;
