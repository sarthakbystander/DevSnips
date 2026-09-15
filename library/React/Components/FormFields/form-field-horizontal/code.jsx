/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  Children,
  cloneElement,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useId,
  useMemo,
  useState
} from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const FieldTextRegistryContext = createContext(null);
const FormFieldContext = createContext(null);
function useFormField() {
  const field = useContext(FormFieldContext);
  if (!field) {
    throw new Error("useFormField must be used inside <FormField>");
  }
  return field;
}
function useRegisterFieldText(id, kind, tone) {
  const registry = useContext(FieldTextRegistryContext);
  useEffect(() => {
    if (!registry) return;
    return registry.registerText({ id, kind, tone });
  }, [registry, id, kind, tone]);
}
function useFieldTexts() {
  const [texts, setTexts] = useState([]);
  const registerText = useCallback((entry) => {
    setTexts((prev) => prev.some((t) => t.id === entry.id) ? prev : [...prev, entry]);
    return () => {
      setTexts((prev) => prev.filter((t) => t.id !== entry.id));
    };
  }, []);
  return [texts, registerText];
}
const LABEL_CLASSES = "block text-[13px] font-medium leading-5";
const DESCRIPTION_CLASSES = "text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const HELPER_CLASSES = "text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const MESSAGE_CLASSES = "flex items-start gap-1.5 text-xs leading-4";
const LEGEND_CLASSES = "p-0 text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]";
const LABEL_HORIZONTAL_CLASSES = "sm:col-start-1 sm:row-start-1 sm:pt-2";
const BODY_HORIZONTAL_CLASSES = "sm:col-start-2";
function FormField({
  controlId,
  required = false,
  disabled = false,
  orientation = "vertical",
  className,
  children,
  ...rest
}) {
  const generatedId = useId();
  const resolvedControlId = controlId ?? `field-${generatedId}`;
  const [texts, registerText] = useFieldTexts();
  const describedBy = texts.length ? texts.map((t) => t.id).join(" ") : undefined;
  const hasError = texts.some((t) => t.kind === "message" && t.tone === "error");
  const fieldValue = useMemo(
    () => ({
      controlId: resolvedControlId,
      required,
      disabled,
      orientation,
      describedBy,
      hasError
    }),
    [resolvedControlId, required, disabled, orientation, describedBy, hasError]
  );
  const registryValue = useMemo(
    () => ({ registerText }),
    [registerText]
  );
  return <FieldTextRegistryContext.Provider value={registryValue}>
      <FormFieldContext.Provider value={fieldValue}>
        <div
    data-ds-form-field=""
    data-orientation={orientation}
    className={cx(
      orientation === "horizontal" ? "grid w-full min-w-0 grid-cols-1 gap-2 sm:grid-cols-[10rem_minmax(0,1fr)] sm:gap-x-4" : "flex w-full min-w-0 flex-col gap-2",
      className
    )}
    {...rest}
  >
          {children}
        </div>
      </FormFieldContext.Provider>
    </FieldTextRegistryContext.Provider>;
}
function FormFieldLabel({
  optional = false,
  className,
  children,
  ...rest
}) {
  const field = useFormField();
  return <label
    htmlFor={field.controlId}
    className={cx(
      LABEL_CLASSES,
      field.disabled ? "text-[var(--ds-color-muted-foreground)]" : "text-[var(--ds-color-foreground)]",
      field.orientation === "horizontal" && LABEL_HORIZONTAL_CLASSES,
      className
    )}
    {...rest}
  >
      {children}
      {field.required ? <>
          <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span>
          <span className="sr-only"> (required)</span>
        </> : optional ? <span className="ml-1 font-normal text-[var(--ds-color-muted-foreground)]">(optional)</span> : null}
    </label>;
}
function FormFieldControl({ children }) {
  const field = useFormField();
  const child = Children.only(children);
  const own = child.props;
  const describedBy = cx(own["aria-describedby"], field.describedBy) || undefined;
  return cloneElement(child, {
    id: field.controlId,
    "aria-describedby": describedBy,
    ...field.hasError ? { "aria-invalid": true } : {},
    ...field.required ? { required: true } : {},
    ...field.disabled ? { disabled: true } : {},
    className: cx(
      own.className,
      field.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES
    )
  });
}
function FormFieldDescription({
  className,
  children,
  ...rest
}) {
  const id = useId();
  useRegisterFieldText(id, "description");
  const field = useContext(FormFieldContext);
  return <p
    id={id}
    className={cx(
      DESCRIPTION_CLASSES,
      field?.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
      className
    )}
    {...rest}
  >
      {children}
    </p>;
}
function FormFieldHelper({ className, children, ...rest }) {
  const id = useId();
  useRegisterFieldText(id, "helper");
  const field = useContext(FormFieldContext);
  return <p
    id={id}
    className={cx(
      HELPER_CLASSES,
      field?.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
      className
    )}
    {...rest}
  >
      {children}
    </p>;
}
function FormFieldMessage({ tone, className, children, ...rest }) {
  const id = useId();
  useRegisterFieldText(id, "message", tone);
  const field = useContext(FormFieldContext);
  return <p
    id={id}
    data-tone={tone}
    role={tone === "error" ? "alert" : "status"}
    className={cx(
      MESSAGE_CLASSES,
      tone === "error" ? "text-[var(--ds-color-destructive)]" : "text-[var(--ds-color-success)]",
      field?.orientation === "horizontal" && BODY_HORIZONTAL_CLASSES,
      className
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
        {tone === "error" ? <>
            <circle cx="12" cy="12" r="10" />
            <path d="M12 8v4" />
            <path d="M12 16h.01" />
          </> : <>
            <circle cx="12" cy="12" r="10" />
            <path d="m9 12 2 2 4-4" />
          </>}
      </svg>
      <span>{children}</span>
    </p>;
}
function FormFieldGroup({
  legend,
  orientation = "vertical",
  disabled,
  className,
  children,
  ...rest
}) {
  const [texts, registerText] = useFieldTexts();
  const describedBy = texts.length ? texts.map((t) => t.id).join(" ") : undefined;
  const registryValue = useMemo(
    () => ({ registerText }),
    [registerText]
  );
  return <FieldTextRegistryContext.Provider value={registryValue}>
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
      orientation === "horizontal" ? "flex flex-wrap gap-x-4 gap-y-2" : "flex flex-col gap-2"
    )}
  >
          {children}
        </div>
      </fieldset>
    </FieldTextRegistryContext.Provider>;
}

export { useFormField, FormField, FormFieldLabel, FormFieldControl, FormFieldDescription, FormFieldHelper, FormFieldMessage, FormFieldGroup };

export default FormField;
