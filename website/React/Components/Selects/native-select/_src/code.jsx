/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  sm: "h-8 text-[13px] [&_svg]:size-[14px]",
  md: "h-9 text-sm [&_svg]:size-4",
  lg: "h-11 text-sm [&_svg]:size-[18px]"
};
function ChevronDown({ className }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m6 9 6 6 6-6" />
    </svg>;
}
export function NativeSelect({
  label = "Select",
  helperText,
  error,
  success,
  options,
  value,
  defaultValue = "",
  onChange,
  size = "md",
  placeholder = "Select an option",
  disabled,
  leadingIcon,
  id,
  className,
  name
}) {
  const generatedId = useId();
  const selectId = id ?? `native-select-${generatedId}`;
  const messageId = `${selectId}-message`;
  const message = error ?? success ?? helperText;
  const [internalValue, setInternalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;
  function handleChange(event) {
    const next = event.target.value;
    const option = options.find((o) => o.value === next) ?? { value: next, label: next };
    if (value === undefined) setInternalValue(next);
    onChange?.(next, option);
  }
  return <div className="w-full">
      <label
    htmlFor={selectId}
    className={cx(
      "mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]",
      disabled && "text-[var(--ds-color-muted-foreground)]"
    )}
  >
        {label}
      </label>
      {message ? <p
    id={messageId}
    className={cx(
      "mb-2 text-xs",
      error ? "text-[var(--ds-color-destructive)]" : success ? "text-[var(--ds-color-success)]" : "text-[var(--ds-color-muted-foreground)]"
    )}
  >
          {error ? `Error: ${error}` : success ? `Success: ${success}` : helperText}
        </p> : null}
      <div className="relative">
        {leadingIcon ? <span className="pointer-events-none absolute left-3 z-10 text-[var(--ds-color-muted-foreground)]">{leadingIcon}</span> : null}
        <select
    id={selectId}
    name={name}
    value={selectedValue}
    defaultValue={value === undefined ? defaultValue : undefined}
    onChange={handleChange}
    disabled={disabled}
    aria-invalid={error ? true : undefined}
    aria-describedby={message ? messageId : undefined}
    className={cx(
      "w-full appearance-none rounded-[var(--ds-radius-sm)] border bg-[var(--ds-color-input)] pr-9 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:bg-[var(--ds-color-muted)] disabled:text-[var(--ds-color-muted-foreground)] disabled:opacity-60 motion-reduce:transition-none",
      error ? "border-[var(--ds-color-destructive)]" : success ? "border-[var(--ds-color-success)]" : "border-[var(--ds-color-border)]",
      SIZES[size],
      leadingIcon ? "pl-9" : "pl-3",
      className
    )}
  >
          {!selected ? <option value="" disabled>
              {placeholder}
            </option> : null}
          {options.map((option) => <option key={option.value} value={option.value} disabled={option.disabled}>
              {option.label}
            </option>)}
        </select>
        <ChevronDown
    className={cx(
      "pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 shrink-0 text-[var(--ds-color-muted-foreground)] transition-transform duration-150 motion-reduce:transition-none",
      disabled && "opacity-60"
    )}
  />
      </div>
    </div>;
}

export default NativeSelect;
