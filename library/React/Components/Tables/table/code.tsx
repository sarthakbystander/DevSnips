import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  TableHTMLAttributes,
  TdHTMLAttributes,
  ThHTMLAttributes,
} from "react";

/**
 * DevSnips React Table — reference implementation.
 *
 * Data tables as a compound component over REAL table semantics: `<Table>`
 * renders a bordered scroll container and a native `<table>` (never a grid of
 * divs), and the region primitives map one-to-one onto table elements —
 * `<TableCaption>` (`<caption>`), `<TableHeader>` (`<thead>`), `<TableBody>`
 * (`<tbody>`), `<TableFooter>` (`<tfoot>`), `<TableRow>` (`<tr>`),
 * `<TableHead>` (`<th scope="col">`), and `<TableCell>` (`<td>`).
 *
 * Behavior primitives cover the real data-table patterns:
 * `<TableSelection>` (a native checkbox with a true `.indeterminate` IDL
 * state for select-all), `<TableExpand>` (a real toggle button with
 * `aria-expanded` / `aria-controls`), `<TableLoading>` (geometry-preserving
 * skeleton rows), `<TableEmpty>` (an honest zero-data state, no fake rows),
 * `<TableActions>` (an end-aligned cell cluster of real controls),
 * `<TableToolbar>` (the above-table region), and `<TablePagination>` (a
 * self-contained pagination bar that follows the DevSnips Pagination family
 * semantics: real buttons, `aria-current`, native disabled boundaries).
 *
 * Sorting is primitive-driven and never fake: a sortable `<TableHead>`
 * renders a visible `<button>` inside the `<th>`, carries the correct
 * `aria-sort`, and the typed `sortRows` helper + `useRowSelection` hook give
 * consumers real ordering and real selection state. Density (`default` /
 * `compact`) is the only shared visual context.
 */
function cx(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(" ");
}

export type TableDensity = "default" | "compact";
export type TableAlign = "left" | "center" | "right";
/** `null` means the column is sortable but currently unsorted. */
export type SortDirection = "asc" | "desc" | null;

const ALIGN_CLASSES: Record<TableAlign, string> = {
  left: "text-left",
  center: "text-center",
  right: "text-right",
};

const DENSITY_CLASSES: Record<
  TableDensity,
  { head: string; cell: string; control: string; skeleton: string }
> = {
  default: {
    head: "h-10 px-3",
    cell: "px-3 py-2.5",
    control: "size-[18px]",
    skeleton: "px-3 py-[13px]",
  },
  compact: {
    head: "h-8 px-3",
    cell: "px-3 py-1.5 text-[13px] leading-4",
    control: "size-4",
    skeleton: "px-3 py-2",
  },
};

/* ------------------------------------------------------------------------ */
/* Shared glyphs (lucide-style, 24px grid, currentColor)                     */
/* ------------------------------------------------------------------------ */

const GLYPH_PROPS = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  "aria-hidden": true,
  focusable: false,
} as const;

const SORT_GLYPHS: Record<"asc" | "desc" | "none", ReactNode> = {
  asc: (
    <svg {...GLYPH_PROPS}>
      <path d="m5 12 7-7 7 7" />
      <path d="M12 19V5" />
    </svg>
  ),
  desc: (
    <svg {...GLYPH_PROPS}>
      <path d="M12 5v14" />
      <path d="m19 12-7 7-7-7" />
    </svg>
  ),
  none: (
    <svg {...GLYPH_PROPS}>
      <path d="m21 16-4 4-4-4" />
      <path d="M17 20V4" />
      <path d="m3 8 4-4 4 4" />
      <path d="M7 4v16" />
    </svg>
  ),
};

const CHEVRON_DOWN_GLYPH = (
  <svg {...GLYPH_PROPS}>
    <path d="m6 9 6 6 6-6" />
  </svg>
);

const CHEVRON_LEFT_GLYPH = (
  <svg {...GLYPH_PROPS}>
    <path d="m15 6-6 6 6 6" />
  </svg>
);

const CHEVRON_RIGHT_GLYPH = (
  <svg {...GLYPH_PROPS}>
    <path d="m9 6 6 6-6 6" />
  </svg>
);

const CHECK_GLYPH = (
  <svg {...GLYPH_PROPS} strokeWidth={3}>
    <path d="M20 6 9 17l-5-5" />
  </svg>
);

const DASH_GLYPH = (
  <svg {...GLYPH_PROPS} strokeWidth={3}>
    <path d="M5 12h14" />
  </svg>
);

/* ------------------------------------------------------------------------ */
/* Table context (density is the only shared visual state)                   */
/* ------------------------------------------------------------------------ */

interface TableContextValue {
  density: TableDensity;
}

const TableContext = createContext<TableContextValue | null>(null);

function useTable(component: string): TableContextValue {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Table>.`);
  }
  return context;
}

/* ------------------------------------------------------------------------ */
/* Table (root)                                                              */
/* ------------------------------------------------------------------------ */

export interface TableProps extends TableHTMLAttributes<HTMLTableElement> {
  /** Cell/header density: `default` (comfortable) or `compact` (dense data). */
  density?: TableDensity;
  /** Marks the table `aria-busy` while data is loading (pair with `TableLoading`). */
  loading?: boolean;
  /** Extra classes on the bordered scroll container around the `<table>`. */
  containerClassName?: string;
  className?: string;
  children?: ReactNode;
}

/**
 * The root: a bordered, deliberately scrollable container (`overflow-x-auto`
 * — the intentional scroll region when a dataset is genuinely wider than the
 * viewport) around a native `<table>`. Provides density context. Compose the
 * region primitives inside; do not replace them with divs.
 */
export function Table({
  density = "default",
  loading = false,
  containerClassName,
  className,
  children,
  ...rest
}: TableProps) {
  const context = useMemo<TableContextValue>(() => ({ density }), [density]);
  return (
    <TableContext.Provider value={context}>
      <div
        className={cx(
          "relative w-full overflow-x-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]",
          containerClassName,
        )}
      >
        <table
          aria-busy={loading || undefined}
          className={cx(
            "w-full border-collapse text-left text-sm leading-5 text-[var(--ds-color-foreground)]",
            className,
          )}
          {...rest}
        >
          {children}
        </table>
      </div>
    </TableContext.Provider>
  );
}

/* ------------------------------------------------------------------------ */
/* TableCaption                                                              */
/* ------------------------------------------------------------------------ */

export interface TableCaptionProps extends HTMLAttributes<HTMLTableCaptionElement> {
  children?: ReactNode;
}

/**
 * The table's `<caption>` — the accessible name/description of the dataset,
 * rendered above the table. Prefer a caption over an off-table heading so the
 * name travels with the table for assistive technology.
 */
export function TableCaption({ className, children, ...rest }: TableCaptionProps) {
  return (
    <caption
      className={cx(
        "px-3 py-3 text-left text-[13px] leading-5 text-[var(--ds-color-muted-foreground)]",
        className,
      )}
      {...rest}
    >
      {children}
    </caption>
  );
}

/* ------------------------------------------------------------------------ */
/* TableHeader / TableBody / TableFooter                                     */
/* ------------------------------------------------------------------------ */

export interface TableHeaderProps extends HTMLAttributes<HTMLTableSectionElement> {
  children?: ReactNode;
}

/** The `<thead>`. Neutralizes body-row hover/dividers so plain `TableRow`s compose cleanly inside it. */
export function TableHeader({ className, children, ...rest }: TableHeaderProps) {
  return (
    <thead
      className={cx(
        "border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] [&>tr:hover]:bg-transparent [&>tr]:border-0",
        className,
      )}
      {...rest}
    >
      {children}
    </thead>
  );
}

export interface TableBodyProps extends HTMLAttributes<HTMLTableSectionElement> {
  children?: ReactNode;
}

/** The `<tbody>`. The last row's divider is removed so the table edge stays clean. */
export function TableBody({ className, children, ...rest }: TableBodyProps) {
  return (
    <tbody className={cx("[&>tr:last-child]:border-b-0", className)} {...rest}>
      {children}
    </tbody>
  );
}

export interface TableFooterProps extends HTMLAttributes<HTMLTableSectionElement> {
  children?: ReactNode;
}

/** The `<tfoot>` — totals and summaries, visually anchored with a top rule and a subtle surface. */
export function TableFooter({ className, children, ...rest }: TableFooterProps) {
  return (
    <tfoot
      className={cx(
        "border-t border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] font-medium [&>tr:hover]:bg-transparent [&>tr]:border-0",
        className,
      )}
      {...rest}
    >
      {children}
    </tfoot>
  );
}

/* ------------------------------------------------------------------------ */
/* TableRow                                                                  */
/* ------------------------------------------------------------------------ */

export interface TableRowProps extends HTMLAttributes<HTMLTableRowElement> {
  /** Marks the row selected: `aria-selected` + accent-tinted surface (token-derived via color-mix). */
  selected?: boolean;
  /** Marks the row unavailable: `aria-disabled`, reduced opacity, no hover affordance. Row controls must be disabled too. */
  disabled?: boolean;
  children?: ReactNode;
}

/**
 * A `<tr>` with a restrained hover affordance. Selection is a real state
 * (`aria-selected` + an accent-tinted surface), not just a color swap; a
 * disabled row is announced with `aria-disabled` and loses its hover shift.
 * Rows are never fake buttons — interactive content lives in real controls
 * inside the cells.
 */
export function TableRow({
  selected = false,
  disabled = false,
  className,
  children,
  ...rest
}: TableRowProps) {
  return (
    <tr
      aria-selected={selected || undefined}
      aria-disabled={disabled || undefined}
      className={cx(
        "border-b border-[var(--ds-color-border-subtle)] transition-colors duration-150 ease-out motion-reduce:transition-none",
        selected
          ? "bg-[color-mix(in_srgb,var(--ds-color-accent)_8%,var(--ds-color-surface))] hover:bg-[color-mix(in_srgb,var(--ds-color-accent)_12%,var(--ds-color-surface))]"
          : !disabled && "hover:bg-[var(--ds-color-surface-hover)]",
        disabled && "opacity-60",
        className,
      )}
      {...rest}
    >
      {children}
    </tr>
  );
}

/* ------------------------------------------------------------------------ */
/* TableHead                                                                 */
/* ------------------------------------------------------------------------ */

export interface TableHeadProps extends ThHTMLAttributes<HTMLTableCellElement> {
  /** Horizontal alignment of the column header (match the column's cells). */
  align?: TableAlign;
  /** Renders the header content as a visible sort `<button>` and manages `aria-sort`. */
  sortable?: boolean;
  /** Current sort direction for this column; `null` = sortable but unsorted. */
  sortDirection?: SortDirection;
  /** Called when the sort button is activated (click, Enter, or Space). */
  onSort?: () => void;
  className?: string;
  children?: ReactNode;
}

/**
 * A `<th scope="col">`. When `sortable`, the header label becomes a REAL,
 * visible `<button type="button">` (never a mysteriously clickable `<th>`),
 * the `<th>` carries `aria-sort` (`ascending` / `descending` / `none`), and a
 * direction glyph shows the state to sighted users. Keyboard users reach the
 * button with Tab and activate it with Enter/Space.
 */
export function TableHead({
  align = "left",
  sortable = false,
  sortDirection = null,
  onSort,
  scope,
  className,
  children,
  ...rest
}: TableHeadProps) {
  const { density } = useTable("TableHead");
  const ariaSort = sortable
    ? sortDirection === "asc"
      ? "ascending"
      : sortDirection === "desc"
        ? "descending"
        : "none"
    : undefined;
  return (
    <th
      scope={scope ?? "col"}
      aria-sort={ariaSort}
      className={cx(
        DENSITY_CLASSES[density].head,
        "align-middle text-xs font-medium leading-4 tracking-[0.01em] text-[var(--ds-color-muted-foreground)]",
        ALIGN_CLASSES[align],
        className,
      )}
      {...rest}
    >
      {sortable ? (
        <button
          type="button"
          onClick={onSort}
          className={cx(
            "inline-flex items-center gap-1 rounded-[var(--ds-radius-xs)] font-medium tracking-[0.01em] transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
            align === "right" && "flex-row-reverse",
          )}
        >
          <span>{children}</span>
          <span
            aria-hidden="true"
            className={cx(
              "inline-flex [&_svg]:size-3.5",
              sortDirection === null
                ? "opacity-40"
                : "text-[var(--ds-color-foreground)] opacity-100",
            )}
          >
            {SORT_GLYPHS[sortDirection ?? "none"]}
          </span>
        </button>
      ) : (
        children
      )}
    </th>
  );
}

/* ------------------------------------------------------------------------ */
/* TableCell                                                                 */
/* ------------------------------------------------------------------------ */

export interface TableCellProps extends TdHTMLAttributes<HTMLTableCellElement> {
  /** Horizontal alignment: text is usually `left`, numeric values `right`. */
  align?: TableAlign;
  /** Tabular figures for numeric content (pair with `align="right"`). */
  numeric?: boolean;
  className?: string;
  children?: ReactNode;
}

/** A `<td>`. Alignment is intentional and `colSpan` forwards natively. */
export function TableCell({
  align = "left",
  numeric = false,
  className,
  children,
  ...rest
}: TableCellProps) {
  const { density } = useTable("TableCell");
  return (
    <td
      className={cx(
        "align-middle",
        DENSITY_CLASSES[density].cell,
        ALIGN_CLASSES[align],
        numeric && "tabular-nums",
        className,
      )}
      {...rest}
    >
      {children}
    </td>
  );
}

/* ------------------------------------------------------------------------ */
/* TableEmpty                                                                */
/* ------------------------------------------------------------------------ */

export interface TableEmptyProps {
  /** Number of columns the message spans (must match the table's column count). */
  colSpan: number;
  /** The zero-data headline, e.g. "No saved views". */
  title: string;
  /** Supporting explanation. */
  description?: string;
  /** A real control (`<button>` / `<a>`) that resolves the empty state. */
  action?: ReactNode;
  /** Optional leading glyph (decorative: always `aria-hidden`). */
  icon?: ReactNode;
  className?: string;
}

/**
 * An honest empty state: one real row with one spanning cell — no fake
 * placeholder rows just to look populated. The message is plain text in the
 * table flow (readable by everyone); the optional action must be a real
 * control that does something real.
 */
export function TableEmpty({
  colSpan,
  title,
  description,
  action,
  icon,
  className,
}: TableEmptyProps) {
  return (
    <tr>
      <td colSpan={colSpan} className={cx("px-3 py-12 text-center", className)}>
        <div className="mx-auto flex max-w-sm flex-col items-center gap-1.5">
          {icon ? (
            <span
              aria-hidden="true"
              className="mb-1 inline-flex text-[var(--ds-color-muted-foreground)] [&_svg]:size-6"
            >
              {icon}
            </span>
          ) : null}
          <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
            {title}
          </p>
          {description ? (
            <p className="m-0 text-[13px] leading-5 text-[var(--ds-color-muted-foreground)]">
              {description}
            </p>
          ) : null}
          {action ? <div className="mt-3 flex flex-wrap justify-center gap-2">{action}</div> : null}
        </div>
      </td>
    </tr>
  );
}

/* ------------------------------------------------------------------------ */
/* TableLoading                                                              */
/* ------------------------------------------------------------------------ */

const SKELETON_WIDTHS = ["w-3/4", "w-1/2", "w-2/3", "w-1/3"] as const;

export interface TableLoadingProps {
  /** Number of columns (must match the table's column count). */
  columns: number;
  /** Number of skeleton rows (default 5 — pick a value close to the expected page size). */
  rows?: number;
  /** Visually hidden announcement while loading. */
  label?: string;
}

/**
 * Skeleton rows that preserve the table's approximate geometry (same column
 * count, near-identical row heights) so content does not jump when data
 * arrives. Skeleton bars are `aria-hidden` decorative placeholders with a
 * subtle pulse that respects reduced motion; the `label` is announced in a
 * visually hidden row. Set `loading` on `<Table>` so the table reports
 * `aria-busy` for the duration.
 */
export function TableLoading({ columns, rows = 5, label = "Loading data" }: TableLoadingProps) {
  const { density } = useTable("TableLoading");
  return (
    <>
      <tr className="sr-only">
        <td colSpan={columns}>{label}</td>
      </tr>
      {Array.from({ length: rows }, (_, rowIndex) => (
        <tr key={rowIndex} aria-hidden="true" className="border-b border-[var(--ds-color-border-subtle)] last:border-b-0">
          {Array.from({ length: columns }, (_, columnIndex) => (
            <td key={columnIndex} className={DENSITY_CLASSES[density].skeleton}>
              <span
                className={cx(
                  "block h-3 rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-muted)] motion-reduce:animate-none",
                  SKELETON_WIDTHS[(rowIndex + columnIndex) % SKELETON_WIDTHS.length],
                  "animate-pulse",
                )}
              />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

/* ------------------------------------------------------------------------ */
/* TableActions / TableToolbar                                               */
/* ------------------------------------------------------------------------ */

export interface TableActionsProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

/**
 * An end-aligned cluster of real controls for a cell (`<TableCell
 * align="right"><TableActions>…`). Compose only real `<button>` / `<a>`
 * children — never nest a control inside another control.
 */
export function TableActions({ className, children, ...rest }: TableActionsProps) {
  return (
    <div className={cx("flex items-center justify-end gap-1", className)} {...rest}>
      {children}
    </div>
  );
}

export interface TableToolbarProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
}

/**
 * The region above the table: selection counts, filters, and primary actions.
 * A layout-only `flex-wrap` container — it renders no table markup and adds
 * no ARIA of its own, so it never interferes with the table's semantics.
 */
export function TableToolbar({ className, children, ...rest }: TableToolbarProps) {
  return (
    <div className={cx("flex flex-wrap items-center justify-between gap-3", className)} {...rest}>
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------------ */
/* TableSelection                                                            */
/* ------------------------------------------------------------------------ */

export interface TableSelectionProps
  extends Omit<
    InputHTMLAttributes<HTMLInputElement>,
    "type" | "checked" | "defaultChecked" | "onChange" | "size"
  > {
  /** Current checked state (tracked by the caller — works controlled or uncontrolled). */
  checked: boolean;
  /** Tri-state "some selected" state: set imperatively on the DOM node (there is no HTML attribute). */
  indeterminate?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  /** Accessible name, e.g. "Select all rows" or "Select Ada Lovelace". Required (the control is icon-only). */
  label: string;
  className?: string;
}

/**
 * The selection control: a REAL native `<input type="checkbox">` styled after
 * the DevSnips Checkboxes family — the input carries the value, the focus
 * ring, and all native behavior (Space toggles, form submission). The
 * select-all tri-state uses the true `.indeterminate` IDL property, set
 * imperatively via a ref. Never a div fake.
 */
export function TableSelection({
  checked,
  indeterminate = false,
  onCheckedChange,
  label,
  disabled,
  className,
  ...rest
}: TableSelectionProps) {
  const { density } = useTable("TableSelection");
  const inputRef = useRef<HTMLInputElement | null>(null);
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.indeterminate = indeterminate && !checked;
    }
  }, [indeterminate, checked]);
  const active = checked || indeterminate;
  return (
    <span
      className={cx(
        "relative inline-flex shrink-0 items-center justify-center",
        DENSITY_CLASSES[density].control,
      )}
    >
      <input
        ref={inputRef}
        type="checkbox"
        aria-label={label}
        checked={checked}
        disabled={disabled}
        onChange={(event) => onCheckedChange?.(event.target.checked)}
        className={cx(
          "size-full cursor-pointer appearance-none rounded-[var(--ds-radius-xs)] border bg-[var(--ds-color-input)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:cursor-not-allowed disabled:opacity-50 motion-reduce:transition-none",
          active
            ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]"
            : "border-[var(--ds-color-border)]",
          className,
        )}
        {...rest}
      />
      <span
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] [&_svg]:size-3"
      >
        {indeterminate && !checked ? (
          DASH_GLYPH
        ) : (
          <span
            className={cx(
              "inline-flex transition-opacity duration-150 ease-out motion-reduce:transition-none",
              checked ? "opacity-100" : "opacity-0",
            )}
          >
            {CHECK_GLYPH}
          </span>
        )}
      </span>
    </span>
  );
}

/* ------------------------------------------------------------------------ */
/* TableExpand                                                               */
/* ------------------------------------------------------------------------ */

export interface TableExpandProps
  extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, "aria-expanded" | "aria-controls" | "aria-label"> {
  /** Whether the associated content is currently expanded. */
  expanded: boolean;
  /** `id` of the expanded content region (rendered as `aria-controls`). */
  controls?: string;
  /** Noun phrase completing the accessible name: "details for invoice INV-1042". */
  label?: string;
  className?: string;
}

/**
 * The row expand/collapse trigger: a real `<button type="button">` with
 * `aria-expanded` and `aria-controls`, keyboard-operable (Tab + Enter/Space)
 * with a `focus-visible` ring. The chevron rotation is the only motion and it
 * is reduced-motion safe. The consumer renders the expanded content as a real
 * row (a `<TableCell colSpan>` panel) whose `id` matches `controls`.
 */
export function TableExpand({
  expanded,
  controls,
  label,
  className,
  ...rest
}: TableExpandProps) {
  const { density } = useTable("TableExpand");
  return (
    <button
      type="button"
      aria-expanded={expanded}
      aria-controls={controls}
      aria-label={`${expanded ? "Collapse" : "Expand"} ${label ?? "row"}`}
      className={cx(
        "inline-flex items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
        density === "compact" ? "size-7" : "size-8",
        className,
      )}
      {...rest}
    >
      <span
        aria-hidden="true"
        className={cx(
          "inline-flex transition-transform duration-150 ease-out motion-reduce:transition-none [&_svg]:size-4",
          expanded && "rotate-180",
        )}
      >
        {CHEVRON_DOWN_GLYPH}
      </span>
    </button>
  );
}

/* ------------------------------------------------------------------------ */
/* TablePagination                                                           */
/* ------------------------------------------------------------------------ */

/** Clamp a 1-based page into the valid range for `totalPages` (minimum 1). */
export function clampPage(page: number, totalPages: number): number {
  return Math.min(Math.max(1, page), Math.max(1, totalPages));
}

/** Windowed page list: all pages when small, otherwise first/last/current±1 with "ellipsis" markers for hidden ranges. */
export function pageRange(current: number, totalPages: number): Array<number | "ellipsis"> {
  const total = Math.max(1, totalPages);
  const page = clampPage(current, total);
  if (total <= 7) {
    return Array.from({ length: total }, (_, index) => index + 1);
  }
  const wanted = new Set<number>([1, total, page - 1, page, page + 1]);
  const sorted = Array.from(wanted)
    .filter((p) => p >= 1 && p <= total)
    .sort((a, b) => a - b);
  const range: Array<number | "ellipsis"> = [];
  let previous = 0;
  for (const p of sorted) {
    if (p - previous > 1) {
      range.push("ellipsis");
    }
    range.push(p);
    previous = p;
  }
  return range;
}

export interface TablePaginationProps {
  /** Current page, 1-based (controlled). Omit to run uncontrolled. */
  page?: number;
  /** Initial page, 1-based (uncontrolled). */
  defaultPage?: number;
  /** Called with the next 1-based page whenever it changes. */
  onPageChange?: (page: number) => void;
  /** Total number of rows across all pages (required). */
  totalItems: number;
  /** Rows per page. */
  pageSize?: number;
  /** Selectable page sizes; when provided, a labelled native `<select>` is rendered. */
  pageSizeOptions?: readonly number[];
  /** Called when the user picks a new page size (reset to page 1 here). */
  onPageSizeChange?: (pageSize: number) => void;
  /** Accessible label for the navigation landmark. */
  label?: string;
  className?: string;
}

const PAGINATION_CONTROL_BASE =
  "inline-flex h-8 min-w-8 select-none items-center justify-center gap-1 whitespace-nowrap rounded-[var(--ds-radius-sm)] px-2 text-[13px] font-medium leading-4 tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const PAGINATION_CONTROL_IDLE =
  "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const PAGINATION_CONTROL_CURRENT =
  "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]";

/**
 * The table pagination bar — a self-contained `<nav aria-label>` that follows
 * the DevSnips Pagination family's semantics: real `<button type="button">`
 * controls, `aria-current="page"` on the current page, natively disabled
 * Previous/Next at the boundaries, a windowed page list with non-interactive
 * ellipses, and an `aria-live` "Showing X–Y of Z" status. Every page is
 * clamped into range, so an empty page cannot occur through invalid state.
 * The parent slices the dataset by the current page — this component only
 * reports and changes it.
 */
export function TablePagination({
  page,
  defaultPage = 1,
  onPageChange,
  totalItems,
  pageSize = 10,
  pageSizeOptions,
  onPageSizeChange,
  label = "Table pagination",
  className,
}: TablePaginationProps) {
  const isControlled = page !== undefined;
  const [internal, setInternal] = useState(defaultPage);
  const totalPages = Math.max(1, Math.ceil(totalItems / Math.max(1, pageSize)));
  const current = clampPage(isControlled ? page : internal, totalPages);

  function setPage(next: number) {
    const clamped = clampPage(next, totalPages);
    if (clamped === current) {
      return;
    }
    if (!isControlled) {
      setInternal(clamped);
    }
    onPageChange?.(clamped);
  }

  const from = totalItems === 0 ? 0 : (current - 1) * pageSize + 1;
  const to = Math.min(current * pageSize, totalItems);
  const range = pageRange(current, totalPages);

  return (
    <nav
      aria-label={label}
      className={cx("flex flex-wrap items-center justify-between gap-3", className)}
    >
      <p aria-live="polite" className="m-0 text-[13px] leading-4 text-[var(--ds-color-muted-foreground)]">
        Showing <span className="font-medium text-[var(--ds-color-foreground)]">{from}</span>
        {" – "}
        <span className="font-medium text-[var(--ds-color-foreground)]">{to}</span> of{" "}
        <span className="font-medium text-[var(--ds-color-foreground)]">{totalItems}</span>
      </p>
      <div className="flex flex-wrap items-center gap-3">
        {pageSizeOptions ? (
          <label className="flex items-center gap-2 text-[13px] leading-4 text-[var(--ds-color-muted-foreground)]">
            Rows per page
            <select
              value={pageSize}
              onChange={(event) => onPageSizeChange?.(Number(event.target.value))}
              className="h-8 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-2 text-[13px] leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none"
            >
              {pageSizeOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
        ) : null}
        <ul className="m-0 flex max-w-full list-none flex-wrap items-center gap-1 p-0">
          <li className="inline-flex">
            <button
              type="button"
              aria-label="Go to previous page"
              disabled={current <= 1}
              onClick={() => setPage(current - 1)}
              className={cx(PAGINATION_CONTROL_BASE, PAGINATION_CONTROL_IDLE)}
            >
              <span aria-hidden="true" className="inline-flex [&_svg]:size-3.5">
                {CHEVRON_LEFT_GLYPH}
              </span>
              <span>Previous</span>
            </button>
          </li>
          {range.map((item, index) =>
            item === "ellipsis" ? (
              <li key={`ellipsis-${index}`} className="inline-flex">
                <span
                  className={cx(PAGINATION_CONTROL_BASE, "pointer-events-none text-[var(--ds-color-muted-foreground)]")}
                >
                  <span aria-hidden="true">…</span>
                  <span className="sr-only">More pages</span>
                </span>
              </li>
            ) : (
              <li key={item} className="inline-flex">
                <button
                  type="button"
                  aria-label={item === current ? `Page ${item}` : `Go to page ${item}`}
                  aria-current={item === current ? "page" : undefined}
                  onClick={() => setPage(item)}
                  className={cx(
                    PAGINATION_CONTROL_BASE,
                    item === current ? PAGINATION_CONTROL_CURRENT : PAGINATION_CONTROL_IDLE,
                  )}
                >
                  {item}
                </button>
              </li>
            ),
          )}
          <li className="inline-flex">
            <button
              type="button"
              aria-label="Go to next page"
              disabled={current >= totalPages}
              onClick={() => setPage(current + 1)}
              className={cx(PAGINATION_CONTROL_BASE, PAGINATION_CONTROL_IDLE)}
            >
              <span>Next</span>
              <span aria-hidden="true" className="inline-flex [&_svg]:size-3.5">
                {CHEVRON_RIGHT_GLYPH}
              </span>
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

/* ------------------------------------------------------------------------ */
/* Typed helpers (real sorting + real selection state)                        */
/* ------------------------------------------------------------------------ */

/**
 * Return a sorted COPY of `rows` by `accessor` (strings use `localeCompare`,
 * numbers sort numerically). The input array is never mutated.
 */
export function sortRows<T>(
  rows: readonly T[],
  accessor: (row: T) => string | number,
  direction: Exclude<SortDirection, null>,
): T[] {
  const sorted = [...rows];
  sorted.sort((a, b) => {
    const av = accessor(a);
    const bv = accessor(b);
    const compared =
      typeof av === "number" && typeof bv === "number"
        ? av - bv
        : String(av).localeCompare(String(bv));
    return direction === "asc" ? compared : -compared;
  });
  return sorted;
}

export interface RowSelection<K extends string | number> {
  /** Read-only view of the currently selected keys. */
  readonly selected: ReadonlySet<K>;
  /** How many of the tracked `keys` are selected. */
  readonly count: number;
  /** Every tracked key is selected. */
  readonly allSelected: boolean;
  /** Some — but not all — tracked keys are selected (drives the indeterminate state). */
  readonly someSelected: boolean;
  isSelected(key: K): boolean;
  toggle(key: K, checked?: boolean): void;
  toggleAll(checked?: boolean): void;
  clear(): void;
}

/**
 * Real selection state for a table: pass the SELECTABLE row keys (exclude
 * disabled rows) and get the checked set, the derived all/some flags for the
 * header checkbox's checked/indeterminate states, and a selected count.
 * Selection is a real `Set` of keys — it survives re-renders and stays
 * correct as rows are added or removed.
 */
export function useRowSelection<K extends string | number>(
  keys: readonly K[],
): RowSelection<K> {
  const [selected, setSelected] = useState<ReadonlySet<K>>(() => new Set<K>());

  const count = useMemo(
    () => keys.reduce((total, key) => (selected.has(key) ? total + 1 : total), 0),
    [keys, selected],
  );
  const allSelected = keys.length > 0 && count === keys.length;
  const someSelected = count > 0 && !allSelected;

  const isSelected = useCallback((key: K) => selected.has(key), [selected]);

  const toggle = useCallback((key: K, checked?: boolean) => {
    setSelected((previous) => {
      const next = new Set(previous);
      if (checked ?? !next.has(key)) {
        next.add(key);
      } else {
        next.delete(key);
      }
      return next;
    });
  }, []);

  const toggleAll = useCallback(
    (checked?: boolean) => {
      setSelected((previous) => {
        const currentlyAll = keys.length > 0 && keys.every((key) => previous.has(key));
        if (checked ?? !currentlyAll) {
          return new Set<K>(keys);
        }
        return new Set<K>();
      });
    },
    [keys],
  );

  const clear = useCallback(() => setSelected(new Set<K>()), []);

  return { selected, count, allSelected, someSelected, isSelected, toggle, toggleAll, clear };
}

export default Table;
