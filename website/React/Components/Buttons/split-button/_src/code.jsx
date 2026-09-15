/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { useEffect, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const SIZES = {
  xs: "h-7 gap-1 px-2 text-xs [&_svg]:size-[14px]",
  sm: "h-8 gap-1.5 px-3 text-xs [&_svg]:size-[14px]",
  md: "h-9 gap-2 px-3.5 text-[13px] [&_svg]:size-4",
  lg: "h-10 gap-2 px-4 text-[13px] [&_svg]:size-[18px]",
  xl: "h-11 gap-2 px-5 text-sm [&_svg]:size-5"
};
const VARIANTS = {
  solid: "border-transparent bg-[var(--ds-color-primary)] text-[var(--ds-color-primary-foreground)] hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] active:bg-[color-mix(in_srgb,var(--ds-color-primary)_80%,#000)]",
  outline: "border-[var(--ds-color-border-strong)] bg-transparent text-[var(--ds-color-foreground)] hover:bg-[var(--ds-color-surface-hover)] active:bg-[var(--ds-color-surface-active)]"
};
function Icon({ name, className }) {
  if (!name) return null;
  const common = { width: "1em", height: "1em", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.75, strokeLinecap: "round", strokeLinejoin: "round", className, "aria-hidden": "true", focusable: "false" };
  const paths = {
    "upload": <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
    "duplicate": <><rect x="9" y="9" width="12" height="12" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></>,
    "trash": <><path d="M3 6h18" /><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" /></>,
    "edit": <><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></>,
    "share": <><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><path d="m8.6 13.5 6.8 4" /><path d="m15.4 6.5-6.8 4" /></>
  };
  return <svg {...common}>{paths[name]}</svg>;
}
const MENU = "absolute right-0 top-[calc(100%+4px)] z-40 min-w-[180px] rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)]";
const ITEM = "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] border-0 px-2 py-1.5 text-left font-normal text-[13px] leading-none text-[var(--ds-color-foreground)] bg-transparent transition-colors duration-150 ease-out motion-reduce:transition-none hover:bg-[var(--ds-color-surface-hover)] focus:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--ds-color-focus-ring)]";
function ChevronIcon({ open }) {
  return <svg className={cx("h-[1em] w-[1em] shrink-0 transition-transform duration-150 ease-out motion-reduce:transition-none", open ? "rotate-180" : "rotate-0")} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="m6 9 6 6 6-6" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
    </svg>;
}
export function SplitButton({
  label,
  actions = [],
  onAction,
  variant = "solid",
  size = "md",
  disabled,
  className,
  ...rest
}) {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const triggerRef = useRef(null);
  const itemRefs = useRef([]);
  const containerRef = useRef(null);
  useEffect(() => {
    if (!open) return;
    function onDown(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) setOpen(false);
    }
    function onKey(e) {
      if (e.key === "Escape") {
        setOpen(false);
        triggerRef.current?.focus();
      }
    }
    document.addEventListener("mousedown", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);
  function openMenu() {
    setOpen(true);
    setTimeout(() => itemRefs.current[0]?.focus(), 0);
  }
  function choose(i) {
    setOpen(false);
    setActive(i);
    onAction?.(actions[i].id, actions[i]);
    triggerRef.current?.focus();
  }
  function onTriggerKey(e) {
    if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openMenu();
    }
  }
  function onItemKey(e, i) {
    const n = actions.length;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      itemRefs.current[(i + 1) % n]?.focus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      itemRefs.current[(i - 1 + n) % n]?.focus();
    } else if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      choose(i);
    }
  }
  const current = actions[active];
  return <div ref={containerRef} className="relative inline-flex">
      <button
    type="button"
    ref={triggerRef}
    className={cx(
      "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
      VARIANTS[variant],
      SIZES[size],
      "rounded-r-none border-r-0",
      className
    )}
    disabled={disabled}
    onClick={() => onAction?.(current?.id ?? "", current ?? {})}
    onKeyDown={onTriggerKey}
    {...rest}
  >
        {current?.icon ? <Icon name={current.icon} /> : null}
        <span>{current?.label ?? label}</span>
      </button>
      <button
    type="button"
    className={cx(
      "inline-flex select-none items-center justify-center whitespace-nowrap rounded-[var(--ds-radius-sm)] border font-medium leading-none transition-colors duration-150 ease-out motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50",
      VARIANTS[variant],
      SIZES[size],
      "rounded-l-none",
      "px-0 [&_svg]:size-[1em]"
    )}
    aria-haspopup="menu"
    aria-expanded={open}
    aria-label="More actions"
    disabled={disabled}
    onClick={() => open ? setOpen(false) : openMenu()}
  >
        <ChevronIcon open={open} />
      </button>
      {open && <div role="menu" className={MENU}>
          {actions.map((a, i) => <button
    key={a.id}
    ref={(el) => {
      itemRefs.current[i] = el;
    }}
    role="menuitem"
    tabIndex={-1}
    className={cx(ITEM, a.destructive && "text-[var(--ds-color-destructive)]")}
    onClick={() => choose(i)}
    onKeyDown={(e) => onItemKey(e, i)}
  >
              {a.icon ? <Icon name={a.icon} /> : <span className="w-[1em]" />}
              <span className="flex-1">{a.label}</span>
              {i === active && <svg className="h-[1em] w-[1em] shrink-0" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 6 9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
            </button>)}
        </div>}
    </div>;
}

export default SplitButton;
