import { useId, useState } from "react";

export type SelectSize = "sm" | "md" | "lg";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectReadonlyProps {
  label?: string;
  helperText?: string;
  options: SelectOption[];
  value?: string;
  defaultValue?: string;
  size?: SelectSize;
  readOnly?: boolean;
  id?: string;
  name?: string;
  className?: string;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const SIZES: Record<SelectSize, string> = {
  sm: "h-8 text-[13px] [&_svg]:size-[14px]",
  md: "h-9 text-sm [&_svg]:size-4",
  lg: "h-11 text-sm [&_svg]:size-[18px]",
};

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

function LockIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect width={18} height={11} x={3} y={11} rx={2} ry={2} />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
  );
}

/**
 * Custom select demonstrating the READ-ONLY state. When `readOnly` (default
 * true) the chosen value is rendered as a static, non-interactive display —
 * a div styled exactly like the trigger (not a button), so it cannot be opened
 * or changed by the user but is still fully readable and not greyed-out like
 * a disabled control. The static display carries `aria-readonly` and a lock
 * affordance. When `readOnly` is false the component falls back to a fully
 * interactive combobox/listbox trigger with keyboard nav.
 */
export function SelectReadonly({
  label = "Select",
  helperText,
  options,
  value,
  defaultValue = "",
  size = "md",
  readOnly = true,
  id,
  name,
  className,
}: SelectReadonlyProps) {
  const generatedId = useId();
  const triggerId = id ?? `select-${generatedId}`;
  const messageId = `${triggerId}-message`;
  const message = helperText;

  const [internalValue] = useState(defaultValue);
  const selectedValue = value ?? internalValue;
  const selected = options.find((o) => o.value === selectedValue) ?? null;

  return (
    <div className="w-full">
      <label htmlFor={triggerId} className="mb-2 block text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]">
        {label}
      </label>
      {message ? (
        <p id={messageId} className="mb-2 text-xs text-[var(--ds-color-muted-foreground)]">
          {helperText}
        </p>
      ) : null}
      <div className="relative">
        {name ? <input type="hidden" name={name} value={selectedValue} readOnly /> : null}
        {readOnly ? (
          <div
            id={triggerId}
            role="textbox"
            aria-readonly={true}
            aria-describedby={message ? messageId : undefined}
            tabIndex={0}
            className={cx(
              "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
              SIZES[size],
              className,
            )}
          >
            <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
              {selected ? selected.label : "—"}
            </span>
            <LockIcon className="shrink-0 text-[var(--ds-color-muted-foreground)]" />
          </div>
        ) : (
          <div
            id={triggerId}
            className={cx(
              "inline-flex w-full items-center justify-between gap-2 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-3 text-left text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-input-hover,var(--ds-color-input))] focus:bg-[var(--ds-color-input-focus,var(--ds-color-input))] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] focus:border-[var(--ds-color-border-strong)] motion-reduce:transition-none",
              SIZES[size],
              className,
            )}
          >
            <span className={cx("flex-1 truncate", !selected && "text-[var(--ds-color-muted-foreground)]")}>
              {selected ? selected.label : "Select an option"}
            </span>
            <ChevronDown className="shrink-0 text-[var(--ds-color-muted-foreground)]" />
          </div>
        )}
      </div>
    </div>
  );
}

export default SelectReadonly;
