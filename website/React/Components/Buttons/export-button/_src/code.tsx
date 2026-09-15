import { useEffect, useRef, useState } from "react";
import type { ButtonHTMLAttributes, ReactNode } from "react";

/* DevSnips React — ExportButton
 * Menu trigger for export destinations. aria-haspopup="menu", keyboard
 * navigable. Arrow keys move, Enter exports, Escape closes.
 */

export type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
export type ExportVariant = "outline" | "secondary";

export interface ExportFormat {
  id: string;
  label: ReactNode;
  icon?: string;
}

export interface ExportButtonProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "onClick"> {
  formats?: ExportFormat[];
  onExport?: (id: string, format: ExportFormat) => void;
  label?: string;
  variant?: ExportVariant;
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

const VARIANTS: Record<ExportVariant, string> = {
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]",
  secondary: "border-[var(--ds-color-border)] bg-[var(--ds-color-secondary)] text-[var(--ds-color-secondary-foreground)] hover:bg-[var(--ds-color-surface-active)] active:bg-[var(--ds-color-surface-active)]",
};

const MENU =
  "absolute right-0 top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] " +
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
    "download": <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
    "file": <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6" /></>,
    "archive": <><rect x="3" y="4" width="18" height="4" rx="1" /><path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8" /><path d="M10 12h4" /></>,
    "external": <><path d="M15 3h6v6" /><path d="M10 14 21 3" /></>,
  };
  return <svg {...common}>{paths[name]}</svg>;
}

export function ExportButton({
  formats = [],
  onExport,
  label = "Export",
  variant = "outline",
  size = "sm",
  disabled,
  className,
  type = "button",
  ...rest
}: ExportButtonProps) {
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
  function choose(i: number) { setOpen(false); onExport?.(formats[i].id, formats[i]); triggerRef.current?.focus(); }
  function onKey(e: React.KeyboardEvent, i: number) {
    const n = formats.length;
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
        className={cx("inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50", VARIANTS[variant], SIZES[size], className)}
        disabled={disabled}
        onClick={() => (open ? setOpen(false) : openMenu())}
        {...rest}
      >
        <Icon name="download" className="shrink-0" />
        <span>{label}</span>
        <svg className={cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", open ? "rotate-180" : "rotate-0")} viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" /></svg>
      </button>
      {open && (
        <div role="menu" className={MENU}>
          {formats.map((f, i) => (
            <button key={f.id} ref={(el) => { itemRefs.current[i] = el; }} role="menuitem" tabIndex={-1} className={ITEM} onClick={() => choose(i)} onKeyDown={(e) => onKey(e, i)}>
              <Icon name={f.icon ?? "download"} className="shrink-0" />
              <span>{f.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default ExportButton;
