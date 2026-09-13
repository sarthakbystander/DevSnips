/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useId } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
export function SelectGroup({
  label = "Group",
  children,
  direction = "column",
  className
}) {
  const generatedId = useId();
  const legendId = `select-group-${generatedId}-legend`;
  return <fieldset
    aria-labelledby={legendId}
    className={cx(
      "min-w-0 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-4 motion-reduce:transition-none",
      className
    )}
  >
      {label ? <legend
    id={legendId}
    className="mb-3 px-1 text-[13px] font-medium leading-5 text-[var(--ds-color-foreground)]"
  >
          {label}
        </legend> : null}
      <div
    className={cx(
      direction === "row" ? "grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3" : "flex flex-col gap-4"
    )}
  >
        {children}
      </div>
    </fieldset>;
}

export default SelectGroup;
