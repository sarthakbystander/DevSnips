/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function SwitchGroup({
  legend,
  options,
  value,
  defaultValue = [],
  onChange,
  disabled,
  required,
  invalid,
  error,
  helperText,
  name,
  id,
  orientation = "vertical",
  className
}) {
  const generatedId = useId();
  const groupId = id ?? `switch-group-${generatedId}`;
  const messageId = `${groupId}-msg`;
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState(defaultValue);
  const selected = isControlled ? value : internal;
  function handleChange(option, event) {
    const next = event.target.checked ? [...selected, option.value] : selected.filter((v) => v !== option.value);
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  const describedby = error || helperText ? messageId : undefined;
  return <fieldset
    id={groupId}
    className={cx("min-w-0 border-0 p-0", className)}
    aria-invalid={invalid || error ? true : undefined}
    aria-describedby={describedby}
  >
      <legend className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {legend}
        {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
      </legend>
      <div className={cx("flex gap-2", orientation === "vertical" ? "flex-col" : "flex-wrap")}>
        {options.map((option) => {
    const isOn = selected.includes(option.value);
    const optionDisabled = option.disabled || disabled;
    return <label
      key={option.value}
      htmlFor={`${groupId}-${option.value}`}
      className={cx(
        "inline-flex items-start gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
        optionDisabled ? "cursor-not-allowed" : "cursor-pointer",
        orientation === "horizontal" ? "mr-2" : ""
      )}
    >
              <span className={cx("relative mt-[3px] inline-flex h-[14px] w-[24px] shrink-0 items-center", optionDisabled && "opacity-50")}>
                <input
      id={`${groupId}-${option.value}`}
      type="checkbox"
      role="switch"
      aria-checked={isOn}
      name={name}
      value={option.value}
      checked={isOn}
      disabled={optionDisabled}
      required={required}
      aria-invalid={invalid || error ? true : undefined}
      aria-describedby={option.description ? `${groupId}-${option.value}-desc` : undefined}
      className={cx(
        "absolute inset-0 h-full w-full cursor-pointer appearance-none rounded-full border transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed motion-reduce:transition-none",
        invalid || error ? isOn ? "border-[var(--ds-color-destructive)] bg-[var(--ds-color-destructive)]" : "border-[var(--ds-color-destructive)]" : isOn ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)] bg-[var(--ds-color-input)]"
      )}
      onChange={(e) => handleChange(option, e)}
    />
                <span
      aria-hidden="true"
      className={cx(
        "pointer-events-none absolute left-[2px] top-[2px] size-[10px] rounded-full transition-[transform,background-color] duration-150 ease-out motion-reduce:transition-none",
        isOn ? "translate-x-[10px]" : "translate-x-0",
        (invalid || error) && isOn ? "bg-[var(--ds-color-destructive-foreground)]" : isOn ? "bg-[var(--ds-color-primary-foreground)]" : "bg-[var(--ds-color-muted-foreground)]"
      )}
    />
              </span>
              <span className="flex flex-col gap-0.5">
                <span className="select-none font-medium">{option.label}</span>
                {option.description ? <span id={`${groupId}-${option.value}-desc`} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
                    {option.description}
                  </span> : null}
              </span>
            </label>;
  })}
      </div>
      {error ? <p id={messageId} role="alert" className="mt-2 text-xs leading-4 text-[var(--ds-color-destructive)]">
          {error}
        </p> : helperText ? <p id={messageId} className="mt-2 text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p> : null}
    </fieldset>;
}

export default SwitchGroup;
