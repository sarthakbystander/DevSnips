import {
  Children,
  cloneElement,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useMemo,
  useState,
} from "react";
import type {
  FieldsetHTMLAttributes,
  HTMLAttributes,
  LabelHTMLAttributes,
  ReactElement,
  ReactNode,
} from "react";

/**
 * DevSnips React Form Field — with description.
 *
 * `<FormFieldDescription>` renders muted supporting text that frames the
 * field before typing (purpose, impact). It registers its generated id with
 * the field, and `FormFieldControl` links it to the control with
 * `aria-describedby` — the attribute exists only while the description is
 * rendered, never dangling. Same compound core as the reference
 * `form-field`.
 */

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/* ------------------------------------------------------------------------ */
/* Types + contexts                                                          */
/* ------------------------------------------------------------------------ */

export type FormFieldOrientation = "vertical" | "horizontal";
export type FormFieldMessageTone = "error" | "success";

type RegisteredTextKind = "description" | "helper" | "message";

interface RegisteredText {
  id: string;
  kind: RegisteredTextKind;
  tone?: FormFieldMessageTone;
}

/**
 * Nearest-registry contract: `FormField` and `FormFieldGroup` both provide
 * one. Description / helper / message primitives register into the nearest
 * registry, so texts placed inside a `<FormField>` describe that field's
 * control, and texts placed directly inside a `<FormFieldGroup>` describe
 * the whole `<fieldset>`.
 */
interface FieldTextRegistryValue {
  registerText: (entry: RegisteredText) => () => void;
}

interface FormFieldContextValue {
  controlId: string;
  required: boolean;
  disabled: boolean;
  orientation: FormFieldOrientation;
  describedBy: string | undefined;
  hasError: boolean;
}

const FieldTextRegistryContext = createContext<FieldTextRegistryValue | null>(null);
const FormFieldContext = createContext<FormFieldContextValue | null>(null);

/**
 * Access the wiring of the enclosing `<FormField>` (control id, described-by
 * ids, error / required / disabled state). Use it to build custom controls
 * that participate in the field wiring without `<FormFieldControl>`.
 */
export function useFormField(): FormFieldContextValue {
  const field = useContext(FormFieldContext);
  if (!field) {
    throw new Error("useFormField must be used inside <FormField>");
  }
  return field;
}

function useRegisterFieldText(
  id: string,
  kind: RegisteredTextKind,
  tone?: FormFieldMessageTone,
): void {
  const registry = useContext(FieldTextRegistryContext);
  useEffect(() => {
    if (!registry) return;
    return registry.registerText({ id, kind, tone });
  }, [registry, id, kind, tone]);
}

function useFieldTexts(): [RegisteredText[], FieldTextRegistryValue["registerText"]] {
  const [texts, setTexts] = useState<RegisteredText[]>([]);
  const registerText = useCallback((entry: RegisteredText) => {
    setTexts((prev) => (prev.some((t) => t.id === entry.id) ? prev : [...prev, entry]));
    return () => {
      setTexts((prev) => prev.filter((t) => t.id !== entry.id));
    };
  }, []);
  return [texts, registerText];
}

/* ------------------------------------------------------------------------ */
/* Shared classes                                                            */
/* ------------------------------------------------------------------------ */

const LABEL_CLASSES = "block text-[13px] font-medium leading-5";
const DESCRIPTION_CLASSES = "text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const HELPER_CLASSES = "text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const MESSAGE_CLASSES = "flex items-start gap-1.5 text-xs leading-4";
const LEGEND_CLASSES = "p-0 text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]";
// In the horizontal layout the label sits in the left column; every other
// primitive (and the control) is placed in the right column via sm:col-start-2.
const LABEL_HORIZONTAL_CLASSES = "sm:col-start-1 sm:row-start-1 sm:pt-2";
const BODY_HORIZONTAL_CLASSES = "sm:col-start-2";

/* ------------------------------------------------------------------------ */
/* <FormField> — root provider                                               */
/* ------------------------------------------------------------------------ */

export interface FormFieldProps extends HTMLAttributes<HTMLDivElement> {
  /** Id given to the control (and the label's `htmlFor`). Generated when omitted. */
  controlId?: string;
  /** Marks the field required: the label gets a required indicator and the control a native `required`. */
  required?: boolean;
  /** Disables the field: the control gets a native `disabled` and the label is muted. */
  disabled?: boolean;
  /** `horizontal` puts the label in a left column from `sm` up; below `sm` the field stacks. */
  orientation?: FormFieldOrientation;
  children?: ReactNode;
}

export function FormField({
  controlId,
  required = false,
  disabled = false,
  orientation = "vertical",
  className,
  children,
  ...rest
}: FormFieldProps) {
  const generatedId = useId();
  const resolvedControlId = controlId ?? `field-${generatedId}`;
  const [texts, registerText] = useFieldTexts();

  const describedBy = texts.length ? texts.map((t) => t.id).join(" ") : undefined;
  const hasError = texts.some((t) => t.kind === "message" && t.tone === "error");

  // Context values are memoized: the primitives' registration effects depend
  // on the registry, so a new object identity every render would re-run the
  // effects (setState) in a loop.
  const fieldValue = useMemo<FormFieldContextValue>(
    () => ({
      controlId: resolvedControlId,
      required,
      disabled,
      orientation,
      describedBy,
      hasError,
    }),
    [resolvedControlId, required, disabled, orientation, describedBy, hasError],
  );
  const registryValue = useMemo<FieldTextRegistryValue>(
    () => ({ registerText }),
    [registerText],
  );

  return (
    <FieldTextRegistryContext.Provider value={registryValue}>
      <FormFieldContext.Provider value={fieldValue}>
        <div
          data-ds-form-field=""
          data-orientation={orientation}
          className={cx(
            orientation === "horizontal"
              ? "grid w-full min-w-0 grid-cols-1 gap-2 sm:grid-cols-[10rem_minmax(0,1fr)] sm:gap-x-4"
              : "flex w-full min-w-0 flex-col gap-2",
            className,
          )}
          {...rest}
        >
          {children}
        </div>
      </FormFieldContext.Provider>
    </FieldTextRegistryContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* <FormFieldLabel>                                                          */
/* ------------------------------------------------------------------------ */

export interface FormFieldLabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
  /** Show a muted "(optional)" indicator. Use on the optional fields of a mostly-required form. */
  optional?: boolean;
  children?: ReactNode;
}

export function FormFieldLabel({
  optional = false,
  className,
  children,
  ...rest
}: FormFieldLabelProps) {
  const field = useFormField();
  return (
    <label
      htmlFor={field.controlId}
      className={cx(
        LABEL_CLASSES,
        field.disabled
          ? "text-[var(--ds-color-muted-foreground)]"
          : "text-[var(--ds-color-foreground)]",
        field.orientation === "horizontal" && LABEL_HORIZONTAL_CLASSES,
        className,
      )}
      {...rest}
    >
      {children}
      {field.required ? (
        <>
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
          <span className="sr-only"> (required)</span>
        </>
      ) : optional ? (
        <span className="ml-1 font-normal text-[var(--ds-color-muted-foreground)]">(optional)</span>
      ) : null}
    </label>
  );
}

/* ------------------------------------------------------------------------ */
/* <FormFieldControl> — injects the wiring into the wrapped control          */
/* ------------------------------------------------------------------------ */

export interface FormFieldControlProps {
  /**
   * Exactly one control element: a native `<input>` / `<select>` /
   * `<textarea>` / `<button>`-style control, or a DevSnips component that
   * forwards these props to its underlying control.
   */
  children: ReactElement;
}

export function FormFieldControl({ children }: FormFieldControlProps) {
  const field = useFormField();
  const child = Children.only(children);
  const own = child.props as { className?: string; "aria-describedby"?: string };
  const describedBy = cx(own["aria-describedby"], field.describedBy) || undefined;

  return cloneElement(child, {
    id: field.controlId,
    "aria-describedby": describedBy,
    ...(field.hasError ? { "aria-invalid": true } : {}),
    ...(field.required ? { required: true } : {}),
    ...(field.disabled ? { disabled: true } : {}),
    className: cx(
      own.className,
      field.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
    ),
  });
}

/* ------------------------------------------------------------------------ */
/* <FormFieldDescription> / <FormFieldHelper> / <FormFieldMessage>           */
/* ------------------------------------------------------------------------ */

export interface FormFieldDescriptionProps extends HTMLAttributes<HTMLParagraphElement> {
  children?: ReactNode;
}

/**
 * Supporting text that frames the field before typing (purpose, impact).
 * Renders between the label and the control and is linked to the control
 * with `aria-describedby`. In the horizontal layout it may also be placed
 * after the control.
 */
export function FormFieldDescription({
  className,
  children,
  ...rest
}: FormFieldDescriptionProps) {
  const id = useId();
  useRegisterFieldText(id, "description");
  const field = useContext(FormFieldContext);
  return (
    <p
      id={id}
      className={cx(
        DESCRIPTION_CLASSES,
        field?.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
        className,
      )}
      {...rest}
    >
      {children}
    </p>
  );
}

export interface FormFieldHelperProps extends HTMLAttributes<HTMLParagraphElement> {
  children?: ReactNode;
}

/**
 * Persistent hint below the control (format, constraints — "how is this
 * used"), linked with `aria-describedby`. For validation feedback use
 * `<FormFieldMessage>` instead.
 */
export function FormFieldHelper({ className, children, ...rest }: FormFieldHelperProps) {
  const id = useId();
  useRegisterFieldText(id, "helper");
  const field = useContext(FormFieldContext);
  return (
    <p
      id={id}
      className={cx(
        HELPER_CLASSES,
        field?.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
        className,
      )}
      {...rest}
    >
      {children}
    </p>
  );
}

export interface FormFieldMessageProps extends HTMLAttributes<HTMLParagraphElement> {
  /** `error` announces with `role="alert"` and marks the control `aria-invalid`; `success` announces politely with `role="status"`. */
  tone: FormFieldMessageTone;
  children?: ReactNode;
}

/**
 * Validation feedback below the control. An error message is destructive
 * text with an alert icon, announced with `role="alert"`, and flips the
 * control to `aria-invalid="true"` while it is rendered — remove the
 * message to clear the error state. A success message uses the success
 * token with a check icon and `role="status"`. An icon + text carry the
 * state, never color alone.
 */
export function FormFieldMessage({ tone, className, children, ...rest }: FormFieldMessageProps) {
  const id = useId();
  useRegisterFieldText(id, "message", tone);
  const field = useContext(FormFieldContext);
  return (
    <p
      id={id}
      data-tone={tone}
      role={tone === "error" ? "alert" : "status"}
      className={cx(
        MESSAGE_CLASSES,
        tone === "error"
          ? "text-[var(--ds-color-destructive)]"
          : "text-[var(--ds-color-success)]",
        field?.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
        className,
      )}
      {...rest}
    >
      <svg
        aria-hidden="true"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.75}
        strokeLinecap="round"
        strokeLinejoin="round"
        className="mt-px size-3.5 shrink-0"
      >
        {tone === "error" ? (
          <>
            <circle cx="12" cy="12" r="10" />
            <path d="M12 8v4" />
            <path d="M12 16h.01" />
          </>
        ) : (
          <>
            <circle cx="12" cy="12" r="10" />
            <path d="m9 12 2 2 4-4" />
          </>
        )}
      </svg>
      <span>{children}</span>
    </p>
  );
}

/* ------------------------------------------------------------------------ */
/* <FormFieldGroup> — fieldset + legend for related fields                   */
/* ------------------------------------------------------------------------ */

export interface FormFieldGroupProps extends FieldsetHTMLAttributes<HTMLFieldSetElement> {
  /** The group's accessible name, rendered as the `<legend>` (required). */
  legend: ReactNode;
  /** `horizontal` lays the children out in a wrapping row; `vertical` stacks them. */
  orientation?: FormFieldOrientation;
  children?: ReactNode;
}

/**
 * A real `<fieldset>` + `<legend>` grouping related controls (radio groups,
 * checkbox sets, address blocks). `disabled` disables every descendant
 * control natively. `FormFieldDescription` / `FormFieldHelper` /
 * `FormFieldMessage` placed directly inside register against the fieldset
 * and are linked to it with `aria-describedby`; nested `<FormField>`
 * children keep their own wiring.
 */
export function FormFieldGroup({
  legend,
  orientation = "vertical",
  disabled,
  className,
  children,
  ...rest
}: FormFieldGroupProps) {
  const [texts, registerText] = useFieldTexts();
  const describedBy = texts.length ? texts.map((t) => t.id).join(" ") : undefined;
  const registryValue = useMemo<FieldTextRegistryValue>(
    () => ({ registerText }),
    [registerText],
  );

  return (
    <FieldTextRegistryContext.Provider value={registryValue}>
      <fieldset
        data-ds-form-field-group=""
        data-orientation={orientation}
        disabled={disabled}
        aria-describedby={describedBy}
        className={cx("m-0 w-full min-w-0 border-0 p-0", className)}
        {...rest}
      >
        <legend className={LEGEND_CLASSES}>{legend}</legend>
        <div
          className={cx(
            "mt-2",
            orientation === "horizontal"
              ? "flex flex-wrap gap-x-4 gap-y-2"
              : "flex flex-col gap-2",
          )}
        >
          {children}
        </div>
      </fieldset>
    </FieldTextRegistryContext.Provider>
  );
}

export default FormField;
