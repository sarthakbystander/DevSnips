import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — FloatingActionButton
 * Primary compose action hovering over content. Circular, elevated,
 * fixed to a corner. aria-label required. One per screen.
 */

export type FabPosition = "bottom-right" | "bottom-left" | "top-right";

export interface FloatingActionButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: ReactNode;
  label: string;
  position?: FabPosition;
  extended?: boolean;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const POS: Record<FabPosition, string> = {
  "bottom-right": "bottom-6 right-6",
  "bottom-left": "bottom-6 left-6",
  "top-right": "top-6 right-6",
};

export function FloatingActionButton({
  icon,
  label,
  position = "bottom-right",
  extended = false,
  disabled,
  className,
  type = "button",
  ...rest
}: FloatingActionButtonProps) {
  return (
    <button
      type={type}
      aria-label={label}
      className={cx(
        "fixed z-40 inline-flex items-center justify-center gap-2 rounded-full",
        "border border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)]",
        "shadow-[var(--ds-shadow-md)] transition-transform duration-150 ease-out motion-reduce:transition-none",
        "hover:-translate-y-0.5 active:translate-y-0",
        "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
        "disabled:pointer-events-none disabled:opacity-50",
        extended ? "h-12 px-5 text-sm [&_svg]:size-5" : "size-14 p-0 [&_svg]:size-5",
        POS[position],
        className,
      )}
      disabled={disabled}
      {...rest}
    >
      {icon}
      {extended && <span>{label}</span>}
    </button>
  );
}

export default FloatingActionButton;
