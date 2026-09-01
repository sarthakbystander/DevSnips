import { createContext, useContext, useId, useRef, useState } from "react";
import type { HTMLAttributes, KeyboardEvent, ReactNode } from "react";

/**
 * DevSnips React Tabs — accessible tabbed navigation as a compound component.
 * Treatment: underline (restrained bottom rule on the selected tab)
 *
 * `<Tabs>` owns the selected value (controlled via `value` + `onValueChange`,
 * or uncontrolled via `defaultValue`) and the arrow-key orientation.
 * `<TabsList>` renders `role="tablist"` and owns arrow-key / Home / End
 * navigation with automatic activation. `<TabsTrigger>` renders a native
 * `role="tab"` button with roving `tabIndex`. `<TabsContent>` renders the
 * associated `role="tabpanel"`; every panel stays mounted and is toggled with
 * the `hidden` attribute so panel state is preserved.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type TabsOrientation = "horizontal" | "vertical";

interface TabsContextValue {
  value: string | undefined;
  setValue: (next: string) => void;
  orientation: TabsOrientation;
  baseId: string;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs(component: string): TabsContextValue {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Tabs>.`);
  }
  return context;
}

const LIST_HORIZONTAL_CLASSES = "inline-flex max-w-full flex-wrap items-center gap-1 border-b border-[var(--ds-color-border)]";
const LIST_VERTICAL_CLASSES = "flex w-full flex-col items-stretch gap-1 sm:w-56 sm:shrink-0";
const TRIGGER_BASE_CLASSES =
  "inline-flex h-9 shrink-0 select-none items-center gap-2 whitespace-nowrap px-3 text-sm leading-5 font-medium transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const TRIGGER_TREATMENT_CLASSES = "-mb-px rounded-none border-b-2";
const TRIGGER_SELECTED_CLASSES = "border-[var(--ds-color-primary)] text-[var(--ds-color-foreground)]";
const TRIGGER_IDLE_CLASSES = "border-transparent text-[var(--ds-color-muted-foreground)] hover:border-[var(--ds-color-border-strong)] hover:text-[var(--ds-color-foreground)]";
const ICON_CLASSES = "inline-flex shrink-0 text-[14px] [&_svg]:size-3.5";
const BADGE_CLASSES =
  "rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-accent-soft)] px-1.5 py-0.5 text-[11px] font-medium leading-3 text-[var(--ds-color-accent)]";
const COUNT_CLASSES =
  "inline-flex min-w-5 items-center justify-center rounded-full border border-[var(--ds-color-border)] px-1.5 py-0.5 text-[11px] font-medium leading-3 tabular-nums text-[var(--ds-color-muted-foreground)]";

export interface TabsProps
  extends Omit<HTMLAttributes<HTMLDivElement>, "defaultValue" | "onChange"> {
  /** Selected tab value (controlled). Omit to run uncontrolled. */
  value?: string;
  /** Initially selected tab value (uncontrolled). */
  defaultValue?: string;
  /** Called with the next value whenever the selection changes. */
  onValueChange?: (value: string) => void;
  /** Arrow-key navigation axis + layout. */
  orientation?: TabsOrientation;
  className?: string;
  children?: ReactNode;
}

export function Tabs({
  value,
  defaultValue,
  onValueChange,
  orientation = "horizontal",
  className,
  children,
  ...rest
}: TabsProps) {
  const baseId = useId().replace(/:/g, "");
  const isControlled = value !== undefined;
  const [internal, setInternal] = useState<string | undefined>(defaultValue);
  const current = isControlled ? value : internal;
  function setValue(next: string) {
    if (!isControlled) {
      setInternal(next);
    }
    onValueChange?.(next);
  }
  return (
    <TabsContext.Provider value={{ value: current, setValue, orientation, baseId }}>
      {orientation === "vertical" ? (
        <div className={cx("flex flex-col gap-4 sm:flex-row sm:gap-6", className)} {...rest}>
          {children}
        </div>
      ) : (
        <div className={className} {...rest}>
          {children}
        </div>
      )}
    </TabsContext.Provider>
  );
}

export interface TabsListProps {
  /** Group label for the tablist (recommended). */
  "aria-label"?: string;
  className?: string;
  children?: ReactNode;
}

export function TabsList({ className, children, ...rest }: TabsListProps) {
  const context = useTabs("TabsList");
  const listRef = useRef<HTMLDivElement>(null);

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const horizontal = context.orientation === "horizontal";
    const moveKeys = horizontal ? ["ArrowLeft", "ArrowRight"] : ["ArrowUp", "ArrowDown"];
    if (!moveKeys.concat(["Home", "End"]).includes(event.key)) return;
    const list = listRef.current;
    if (!list) return;
    const tabs = Array.from(list.querySelectorAll<HTMLButtonElement>('[role="tab"]')).filter(
      (tab) => !tab.disabled,
    );
    if (tabs.length === 0) return;
    event.preventDefault();
    const currentIndex = tabs.findIndex((tab) => tab === event.target);
    let nextIndex: number;
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

  return (
    <div
      ref={listRef}
      role="tablist"
      aria-orientation={context.orientation}
      onKeyDown={onKeyDown}
      className={cx(
        context.orientation === "vertical" ? LIST_VERTICAL_CLASSES : LIST_HORIZONTAL_CLASSES,
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}

export interface TabsTriggerProps {
  /** Value this trigger selects (associates it with its panel). */
  value: string;
  /** Meaningful leading icon (rendered aria-hidden). */
  icon?: ReactNode;
  /** Small contextual chip after the label (e.g. "New", "Beta"). */
  badge?: ReactNode;
  /** Meaningful numeric count after the label (e.g. open comments). */
  count?: number;
  disabled?: boolean;
  className?: string;
  children?: ReactNode;
}

export function TabsTrigger({
  value,
  icon,
  badge,
  count,
  disabled,
  className,
  children,
}: TabsTriggerProps) {
  const context = useTabs("TabsTrigger");
  const isSelected = context.value === value;
  const triggerId = `${context.baseId}-tab-${value}`;
  const panelId = `${context.baseId}-panel-${value}`;
  return (
    <button
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
        className,
      )}
    >
      {icon ? (
        <span aria-hidden="true" className={ICON_CLASSES}>
          {icon}
        </span>
      ) : null}
      {children}
      {badge !== undefined ? <span className={BADGE_CLASSES}>{badge}</span> : null}
      {count !== undefined ? <span className={COUNT_CLASSES}>{count}</span> : null}
    </button>
  );
}

export interface TabsContentProps {
  /** Value of the tab this panel belongs to. */
  value: string;
  className?: string;
  children?: ReactNode;
}

export function TabsContent({ value, className, children }: TabsContentProps) {
  const context = useTabs("TabsContent");
  const isSelected = context.value === value;
  const triggerId = `${context.baseId}-tab-${value}`;
  const panelId = `${context.baseId}-panel-${value}`;
  return (
    <div
      role="tabpanel"
      id={panelId}
      aria-labelledby={triggerId}
      tabIndex={0}
      hidden={!isSelected}
      className={cx(
        context.orientation === "vertical" ? "min-w-0 flex-1 pt-0" : "pt-4",
        "rounded-[var(--ds-radius-sm)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)]",
        className,
      )}
    >
      {children}
    </div>
  );
}

export default Tabs;
