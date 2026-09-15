/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useEffect, useId, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function CheckboxWithSelectAll({
  legend,
  options,
  value,
  defaultValue = [],
  onChange,
  selectAllLabel = "Select all",
  disabled,
  required,
  name,
  id,
  className
}) {
  const generatedId = useId();
  const groupId = id ?? `select-all-${generatedId}`;
  const allId = `${groupId}-all`;
  const masterRef = useRef(null);
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState(defaultValue);
  const selected = isControlled ? value : internal;
  const enabled = options.filter((o) => !o.disabled);
  const enabledCount = enabled.length;
  const selectedEnabledCount = enabled.filter((o) => selected.includes(o.value)).length;
  const allChecked = enabledCount > 0 && selectedEnabledCount === enabledCount;
  const someChecked = selectedEnabledCount > 0 && !allChecked;
  useEffect(() => {
    if (masterRef.current) masterRef.current.indeterminate = someChecked;
  }, [someChecked]);
  function commit(next, event) {
    if (!isControlled) setInternal(next);
    onChange?.(next, event);
  }
  function handleMaster(event) {
    const next = event.target.checked ? [.../* @__PURE__ */ new Set([...selected, ...enabled.map((o) => o.value)])] : selected.filter((v) => !enabled.some((o) => o.value === v));
    commit(next, event);
  }
  function handleChild(option, event) {
    const next = event.target.checked ? [...selected, option.value] : selected.filter((v) => v !== option.value);
    commit(next, event);
  }
  return <fieldset id={groupId} className={cx("min-w-0 border-0 p-0", className)}>
      <legend className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {legend}
        {required ? <span aria-hidden="true" className="ml-0.5 text-[var(--ds-color-destructive)]">*</span> : null}
      </legend>
      <div className="flex flex-col gap-2">
        <label
    htmlFor={allId}
    className={cx(
      "inline-flex items-center gap-2.5 border-b border-[var(--ds-color-border-subtle)] pb-2 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]",
      disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"
    )}
  >
          <span className="relative inline-flex size-[18px] shrink-0 items-center justify-center">
            <input
    ref={masterRef}
    id={allId}
    type="checkbox"
    checked={allChecked}
    disabled={disabled}
    className="size-[18px] cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none indeterminate:border-[var(--ds-color-primary)] indeterminate:bg-[var(--ds-color-primary)] checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]"
    onChange={handleMaster}
  />
            <span
    aria-hidden="true"
    className={cx(
      "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
      allChecked || someChecked ? "opacity-100" : "opacity-0"
    )}
  >
              {someChecked ? <span className="block h-[2px] w-[10px] rounded-full bg-current" /> : <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20 6 9 17l-5-5" />
                </svg>}
            </span>
          </span>
          <span className="select-none">{selectAllLabel}</span>
        </label>
        <div className="flex flex-col gap-2 pl-1">
          {options.map((option) => {
    const isOn = selected.includes(option.value);
    const isDisabled = option.disabled || disabled;
    return <label
      key={option.value}
      htmlFor={`${groupId}-${option.value}`}
      className={cx(
        "inline-flex items-start gap-2.5 text-sm leading-5 text-[var(--ds-color-foreground)]",
        isDisabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"
      )}
    >
                <span className="relative mt-[3px] inline-flex size-[18px] shrink-0 items-center justify-center">
                  <input
      id={`${groupId}-${option.value}`}
      type="checkbox"
      name={name}
      value={option.value}
      checked={isOn}
      disabled={isDisabled}
      aria-describedby={option.description ? `${groupId}-${option.value}-desc` : undefined}
      className="size-[18px] cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none checked:border-[var(--ds-color-primary)] checked:bg-[var(--ds-color-primary)]"
      onChange={(e) => handleChild(option, e)}
    />
                  <span
      aria-hidden="true"
      className={cx(
        "pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] transition-opacity duration-150 motion-reduce:transition-none",
        isOn ? "opacity-100" : "opacity-0"
      )}
    >
                    <svg className="size-[12px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
                      <path d="M20 6 9 17l-5-5" />
                    </svg>
                  </span>
                </span>
                <span className="flex flex-col gap-0.5">
                  <span className="select-none">{option.label}</span>
                  {option.description ? <span id={`${groupId}-${option.value}-desc`} className="text-xs leading-4 text-[var(--ds-color-muted-foreground)]">
                      {option.description}
                    </span> : null}
                </span>
              </label>;
  })}
        </div>
      </div>
    </fieldset>;
}

export default CheckboxWithSelectAll;
