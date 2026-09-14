import { useEffect, useRef, useState } from "react";
import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — MoreActionsButton
 * Overflow menu trigger. aria-haspopup="menu", keyboard navigable.
 * Destructive items render in destructive color.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type MoreVariant = "ghost" | "outline" | "secondary";
export type MoreAlign = "left" | "right";

export interface MoreAction {
  id: string;
  label: ReactNode;
  icon?: string;
  destructive?: boolean;
}

export interface MoreActionsButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {
  actions?: MoreAction[];
  onAction?: (id: string, action: MoreAction) => void;
  label?: string;
  align?: MoreAlign;
  variant?: MoreVariant;
  size?: ButtonSize;
}

function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

const SIZES: Record<ButtonSize, string> = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5",
};

const VARIANTS: Record<MoreVariant, string> = {
  ghost: "border-transparent bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
};

const ICON_ONLY: Record<ButtonSize, string> = {
  xs: "h-7 w-7 px-0 [&_svg]:size-[14px]",
  sm: "h-8 w-8 px-0 [&_svg]:size-[14px]",
  md: "h-9 w-9 px-0 [&_svg]:size-4",
  lg: "h-10 w-10 px-0 [&_svg]:size-[18px]",
  xl: "h-11 w-11 px-0 [&_svg]:size-5",
};

const MENU =
  "absolute top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] " +
  "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 " +
  "shadow-[var(--ds-shadow-md)]";
const ITEM =
  "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border-0 px-2 py-1.5 " +
  "text-left font-normal text-[13px] leading-none text-[var(--ds-color-foreground)] " +
  "bg-transparent transition-colors duration-150 ease-out motion-reduce:transition-none " +
  "hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)] " +
  "focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)]";

function Icon({ name, className }: { name?: string; className?: string }) {
  if (!name) return null;
  const common = { width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" } as const;
  const paths: Record<string, ReactNode> = {
    "edit": <><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></>,
    "duplicate": <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>,
    "share": <><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><path d="m8.6 13.5 6.8 4" /><path d="m15.4 6.5-6.8 4" /></>,
    "archive": <><rect x="3" y="4" width="18" height="4" rx="1" /><path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8" /><path d="M10 12h4" /></>,
    "trash": <><path d="M3 6h18" /><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" /></>,
    "pin": <path d="M12 17v5" />,
    "settings": <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" /></>,
  };
  return <svg {...common}>{paths[name]}</svg>;
}

export function MoreActionsButton({
  actions = [],
  onAction,
  label = "More actions",
  align = "right",
  variant = "ghost",
  size = "sm",
  className,
  type = "button",
  ...rest
}: MoreActionsButtonProps) {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const itemRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    function onDown(e: MouseEvent) { if (containerRef.current && !containerRef.current.contains(e.target as Node)) setOpen(false); }
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") { setOpen(false); triggerRef.current?.focus(); } }
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("mousedown", onDown); document.removeEventListener("keydown", onKey); };
  }, [open]);

  function openMenu() { setOpen(true); setTimeout(() => itemRefs.current[0]?.focus(), 0); }
  function choose(i: number) { setOpen(false); onAction?.(actions[i].id, actions[i]); triggerRef.current?.focus(); }
  function onKey(e: React.KeyboardEvent, i: number) {
    const n = actions.length;
    if (e.key === "ArrowDown") { e.preventDefault(); itemRefs.current[(i + 1) % n]?.focus(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); itemRefs.current[(i - 1 + n) % n]?.focus(); }
    else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(i); }
  }

  return (
    <div ref={containerRef} className="relative inline-flex">
      <button
        type={type}
        ref={triggerRef}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={label}
        className={cx("inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50", VARIANTS[variant], ICON_ONLY[size], className)}
        onClick={() => (open ? setOpen(false) : openMenu())}
        {...rest}
      >
        <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="5" r="1" fill="currentColor" />
          <circle cx="12" cy="12" r="1" fill="currentColor" />
          <circle cx="12" cy="19" r="1" fill="currentColor" />
        </svg>
      </button>
      {open && (
        <div role="menu" className={cx(MENU, align === "left" ? "left-0" : "right-0")}>
          {actions.map((a, i) => (
            <button
              key={a.id}
              ref={(el) => { itemRefs.current[i] = el; }}
              role="menuitem"
              tabIndex={-1}
              className={cx(ITEM, a.destructive && "text-[var(--ds-color-destructive)]")}
              onClick={() => choose(i)}
              onKeyDown={(e) => onKey(e, i)}
            >
              {a.icon ? <Icon name={a.icon} className="shrink-0" /> : <span className="w-[1em]" />}
              <span className="flex-1">{a.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default MoreActionsButton;
