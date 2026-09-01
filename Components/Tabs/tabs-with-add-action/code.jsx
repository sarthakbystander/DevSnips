/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import { createContext, useContext, useId, useRef, useState } from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const TabsContext = createContext(null);
function useTabs(component) {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Tabs>.`);
  }
  return context;
}
const LIST_HORIZONTAL_CLASSES = "inline-flex max-w-full flex-wrap items-center gap-1";
const LIST_VERTICAL_CLASSES = "flex w-full flex-col items-stretch gap-1 sm:w-56 sm:shrink-0";
const TRIGGER_BASE_CLASSES = "inline-flex h-9 shrink-0 select-none items-center gap-2 whitespace-nowrap px-3 text-sm leading-5 font-medium transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const TRIGGER_TREATMENT_CLASSES = "rounded-[var(--ds-radius-sm)]";
const TRIGGER_SELECTED_CLASSES = "bg-[var(--ds-color-surface-active)] text-[var(--ds-color-foreground)]";
const TRIGGER_IDLE_CLASSES = "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const ICON_CLASSES = "inline-flex shrink-0 text-[14px] [&_svg]:size-3.5";
const BADGE_CLASSES = "rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-accent-soft)] px-1.5 py-0.5 text-[11px] font-medium leading-3 text-[var(--ds-color-accent)]";
const COUNT_CLASSES = "inline-flex min-w-5 items-center justify-center rounded-full border border-[var(--ds-color-border)] px-1.5 py-0.5 text-[11px] font-medium leading-3 tabular-nums text-[var(--ds-color-muted-foreground)]";
function Tabs({
  value,
  defaultValue,
  onValueChange,
  orientation = "horizontal",
  className,
  children,
  ...rest
}) {
  const baseId = useId().replace(/:/g, "");
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState(defaultValue);
  const current = isControlled ? value : internal;
  function setValue(next) {
    if (!isControlled) {
      setInternal(next);
    }
    onValueChange?.(next);
  }
  return <TabsContext.Provider value={{ value: current, setValue, orientation, baseId }}>
      {orientation === "vertical" ? <div className={cx("flex flex-col gap-4 sm:flex-row sm:gap-6", className)} {...rest}>
          {children}
        </div> : <div className={className} {...rest}>
          {children}
        </div>}
    </TabsContext.Provider>;
}
function TabsList({ className, children, ...rest }) {
  const context = useTabs("TabsList");
  const listRef = useRef(null);
  function onKeyDown(event) {
    const horizontal = context.orientation === "horizontal";
    const moveKeys = horizontal ? ["ArrowLeft", "ArrowRight"] : ["ArrowUp", "ArrowDown"];
    if (!moveKeys.concat(["Home", "End"]).includes(event.key)) return;
    const list = listRef.current;
    if (!list) return;
    const tabs = Array.from(list.querySelectorAll('[role="tab"]')).filter(
      (tab) => !tab.disabled
    );
    if (tabs.length === 0) return;
    event.preventDefault();
    const currentIndex = tabs.findIndex((tab) => tab === event.target);
    let nextIndex;
    if (event.key === "Home") {
      nextIndex = 0;
    } else if (event.key === "End") {
      nextIndex = tabs.length - 1;
    } else if (currentIndex === -1) {
      nextIndex = 0;
    } else {
      const delta = event.key === moveKeys[1] ? 1 : -1;
      nextIndex = (currentIndex + delta + tabs.length) % tabs.length;
    }
    const next = tabs[nextIndex];
    next.focus();
    if (next.dataset.value !== undefined) {
      context.setValue(next.dataset.value);
    }
  }
  return <div
    ref={listRef}
    role="tablist"
    aria-orientation={context.orientation}
    onKeyDown={onKeyDown}
    className={cx(
      context.orientation === "vertical" ? LIST_VERTICAL_CLASSES : LIST_HORIZONTAL_CLASSES,
      className
    )}
    {...rest}
  >
      {children}
    </div>;
}
function TabsTrigger({
  value,
  icon,
  badge,
  count,
  disabled,
  className,
  children
}) {
  const context = useTabs("TabsTrigger");
  const isSelected = context.value === value;
  const triggerId = `${context.baseId}-tab-${value}`;
  const panelId = `${context.baseId}-panel-${value}`;
  return <button
    type="button"
    role="tab"
    id={triggerId}
    aria-selected={isSelected}
    aria-controls={panelId}
    tabIndex={isSelected ? 0 : -1}
    disabled={disabled}
    data-value={value}
    onClick={() => context.setValue(value)}
    className={cx(
      TRIGGER_BASE_CLASSES,
      context.orientation === "vertical" ? "w-full justify-start" : "justify-center",
      TRIGGER_TREATMENT_CLASSES,
      isSelected ? TRIGGER_SELECTED_CLASSES : TRIGGER_IDLE_CLASSES,
      className
    )}
  >
      {icon ? <span aria-hidden="true" className={ICON_CLASSES}>
          {icon}
        </span> : null}
      {children}
      {badge !== undefined ? <span className={BADGE_CLASSES}>{badge}</span> : null}
      {count !== undefined ? <span className={COUNT_CLASSES}>{count}</span> : null}
    </button>;
}
function TabsContent({ value, className, children }) {
  const context = useTabs("TabsContent");
  const isSelected = context.value === value;
  const triggerId = `${context.baseId}-tab-${value}`;
  const panelId = `${context.baseId}-panel-${value}`;
  return <div
    role="tabpanel"
    id={panelId}
    aria-labelledby={triggerId}
    tabIndex={0}
    hidden={!isSelected}
    className={cx(
      context.orientation === "vertical" ? "min-w-0 flex-1 pt-0" : "pt-4",
      "rounded-[var(--ds-radius-sm)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
      className
    )}
  >
      {children}
    </div>;
}
function TabsAddAction({ className, children, ...rest }) {
  return <button
    type="button"
    className={cx(
      "inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-0 text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
      className
    )}
    {...rest}
  >
      {children ?? <svg
    aria-hidden="true"
    width="14"
    height="14"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
          <path d="M12 5v14" />
          <path d="M5 12h14" />
        </svg>}
    </button>;
}

export { Tabs, TabsList, TabsTrigger, TabsContent, TabsAddAction };

export default Tabs;
