import type { ReactNode } from "react";
import { useId } from "react";

export type SelectGroupDirection = "row" | "column";

export interface SelectGroupProps {
  label?: string;
  children: ReactNode;
  direction?: SelectGroupDirection;
  className?: string;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

/**
 * Layout wrapper that arranges multiple related selects into a consistent
 * group. Renders a semantic <fieldset>/<legend> (the group label) and lays
 * its children out in a row (responsive grid) or column with a shared gap.
 * It does NOT reimplement the select itself — children are expected to be
 * select (or other field) components passed by the consumer.
 */
export function SelectGroup({
  label = "Group",
  children,
  direction = "column",
  className,
}: SelectGroupProps) {
  const generatedId = useId();
  const legendId = `select-group-${generatedId}-legend`;

  return (
    <fieldset
      aria-labelledby={legendId}
      className={cx(
        "min-w-0 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4 motion-reduce:transition-none",
        className,
      )}
    >
      {label ? (
        <legend
          id={legendId}
          className="mb-3 px-1 text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
        >
          {label}
        </legend>
      ) : null}
      <div
        className={cx(
          direction === "row"
            ? "grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
            : "flex flex-col gap-4",
        )}
      >
        {children}
      </div>
    </fieldset>
  );
}

export default SelectGroup;
