/* DevSnips React — JavaScript parity build.
 * Same API, behavior, and classes as code.tsx; TypeScript types removed.
 * Regenerated from code.tsx — edit code.tsx and re-run the generator.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState
} from "react";
function cx(...parts) {
  return parts.filter(Boolean).join(" ");
}
const ALIGN_CLASSES = {
  left: "text-left",
  center: "text-center",
  right: "text-right"
};
const DENSITY_CLASSES = {
  default: {
    head: "h-10 px-3",
    cell: "px-3 py-2.5",
    control: "size-[18px]",
    skeleton: "px-3 py-[13px]"
  },
  compact: {
    head: "h-8 px-3",
    cell: "px-3 py-1.5 text-[13px] leading-4",
    control: "size-4",
    skeleton: "px-3 py-2"
  }
};
const GLYPH_PROPS = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.75,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  "aria-hidden": true,
  focusable: false
};
const SORT_GLYPHS = {
  asc: <svg {...GLYPH_PROPS}>
      <path d="m5 12 7-7 7 7" />
      <path d="M12 19V5" />
    </svg>,
  desc: <svg {...GLYPH_PROPS}>
      <path d="M12 5v14" />
      <path d="m19 12-7 7-7-7" />
    </svg>,
  none: <svg {...GLYPH_PROPS}>
      <path d="m21 16-4 4-4-4" />
      <path d="M17 20V4" />
      <path d="m3 8 4-4 4 4" />
      <path d="M7 4v16" />
    </svg>
};
const CHEVRON_DOWN_GLYPH = <svg {...GLYPH_PROPS}>
    <path d="m6 9 6 6 6-6" />
  </svg>;
const CHEVRON_LEFT_GLYPH = <svg {...GLYPH_PROPS}>
    <path d="m15 6-6 6 6 6" />
  </svg>;
const CHEVRON_RIGHT_GLYPH = <svg {...GLYPH_PROPS}>
    <path d="m9 6 6 6-6 6" />
  </svg>;
const CHECK_GLYPH = <svg {...GLYPH_PROPS} strokeWidth={3}>
    <path d="M20 6 9 17l-5-5" />
  </svg>;
const DASH_GLYPH = <svg {...GLYPH_PROPS} strokeWidth={3}>
    <path d="M5 12h14" />
  </svg>;
const TableContext = createContext(null);
function useTable(component) {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error(`<${component}> must be rendered inside <Table>.`);
  }
  return context;
}
function Table({
  density = "default",
  loading = false,
  containerClassName,
  className,
  children,
  ...rest
}) {
  const context = useMemo(() => ({ density }), [density]);
  return <TableContext.Provider value={context}>
      <div
    className={cx(
      "relative w-full overflow-x-auto rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)]",
      containerClassName
    )}
  >
        <table
    aria-busy={loading || undefined}
    className={cx(
      "w-full border-collapse text-left text-sm leading-5 text-[var(--ds-color-foreground)]",
      className
    )}
    {...rest}
  >
          {children}
        </table>
      </div>
    </TableContext.Provider>;
}
function TableCaption({ className, children, ...rest }) {
  return <caption
    className={cx(
      "px-3 py-3 text-left text-[13px] leading-5 text-[var(--ds-color-muted-foreground)]",
      className
    )}
    {...rest}
  >
      {children}
    </caption>;
}
function TableHeader({ className, children, ...rest }) {
  return <thead
    className={cx(
      "border-b border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] [&>tr:hover]:bg-transparent [&>tr]:border-0",
      className
    )}
    {...rest}
  >
      {children}
    </thead>;
}
function TableBody({ className, children, ...rest }) {
  return <tbody className={cx("[&>tr:last-child]:border-b-0", className)} {...rest}>
      {children}
    </tbody>;
}
function TableFooter({ className, children, ...rest }) {
  return <tfoot
    className={cx(
      "border-t border-[var(--ds-color-border)] bg-[var(--ds-color-surface-subtle)] font-medium [&>tr:hover]:bg-transparent [&>tr]:border-0",
      className
    )}
    {...rest}
  >
      {children}
    </tfoot>;
}
function TableRow({
  selected = false,
  disabled = false,
  className,
  children,
  ...rest
}) {
  return <tr
    aria-selected={selected || undefined}
    aria-disabled={disabled || undefined}
    className={cx(
      "border-b border-[var(--ds-color-border-subtle)] transition-colors duration-150 ease-out motion-reduce:transition-none",
      selected ? "bg-[color-mix(in_srgb,var(--ds-color-accent)_8%,var(--ds-color-surface))] hover:bg-[color-mix(in_srgb,var(--ds-color-accent)_12%,var(--ds-color-surface))]" : !disabled && "hover:bg-[var(--ds-color-surface-hover)]",
      disabled && "opacity-60",
      className
    )}
    {...rest}
  >
      {children}
    </tr>;
}
function TableHead({
  align = "left",
  sortable = false,
  sortDirection = null,
  onSort,
  scope,
  className,
  children,
  ...rest
}) {
  const { density } = useTable("TableHead");
  const ariaSort = sortable ? sortDirection === "asc" ? "ascending" : sortDirection === "desc" ? "descending" : "none" : undefined;
  return <th
    scope={scope ?? "col"}
    aria-sort={ariaSort}
    className={cx(
      DENSITY_CLASSES[density].head,
      "align-middle text-xs font-medium leading-4 tracking-[0.01em] text-[var(--ds-color-muted-foreground)]",
      ALIGN_CLASSES[align],
      className
    )}
    {...rest}
  >
      {sortable ? <button
    type="button"
    onClick={onSort}
    className={cx(
      "inline-flex items-center gap-1 rounded-[var(--ds-radius-xs)] font-medium tracking-[0.01em] transition-colors duration-150 ease-out hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none",
      align === "right" && "flex-row-reverse"
    )}
  >
          <span>{children}</span>
          <span
    aria-hidden="true"
    className={cx(
      "inline-flex [&_svg]:size-3.5",
      sortDirection === null ? "opacity-40" : "text-[var(--ds-color-foreground)] opacity-100"
    )}
  >
            {SORT_GLYPHS[sortDirection ?? "none"]}
          </span>
        </button> : children}
    </th>;
}
function TableCell({
  align = "left",
  numeric = false,
  className,
  children,
  ...rest
}) {
  const { density } = useTable("TableCell");
  return <td
    className={cx(
      "align-middle",
      DENSITY_CLASSES[density].cell,
      ALIGN_CLASSES[align],
      numeric && "tabular-nums",
      className
    )}
    {...rest}
  >
      {children}
    </td>;
}
function TableEmpty({
  colSpan,
  title,
  description,
  action,
  icon,
  className
}) {
  return <tr>
      <td colSpan={colSpan} className={cx("px-3 py-12 text-center", className)}>
        <div className="mx-auto flex max-w-sm flex-col items-center gap-1.5">
          {icon ? <span
    aria-hidden="true"
    className="mb-1 inline-flex text-[var(--ds-color-muted-foreground)] [&_svg]:size-6"
  >
              {icon}
            </span> : null}
          <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">
            {title}
          </p>
          {description ? <p className="m-0 text-[13px] leading-5 text-[var(--ds-color-muted-foreground)]">
              {description}
            </p> : null}
          {action ? <div className="mt-3 flex flex-wrap justify-center gap-2">{action}</div> : null}
        </div>
      </td>
    </tr>;
}
const SKELETON_WIDTHS = ["w-3/4", "w-1/2", "w-2/3", "w-1/3"];
function TableLoading({ columns, rows = 5, label = "Loading data" }) {
  const { density } = useTable("TableLoading");
  return <>
      <tr className="sr-only">
        <td colSpan={columns}>{label}</td>
      </tr>
      {Array.from({ length: rows }, (_, rowIndex) => <tr key={rowIndex} aria-hidden="true" className="border-b border-[var(--ds-color-border-subtle)] last:border-b-0">
          {Array.from({ length: columns }, (_2, columnIndex) => <td key={columnIndex} className={DENSITY_CLASSES[density].skeleton}>
              <span
    className={cx(
      "block h-3 rounded-[var(--ds-radius-xs)] bg-[var(--ds-color-muted)] motion-reduce:animate-none",
      SKELETON_WIDTHS[(rowIndex + columnIndex) % SKELETON_WIDTHS.length],
      "animate-pulse"
    )}
  />
            </td>)}
        </tr>)}
    </>;
}
function TableActions({ className, children, ...rest }) {
  return <div className={cx("flex items-center justify-end gap-1", className)} {...rest}>
      {children}
    </div>;
}
function TableToolbar({ className, children, ...rest }) {
  return <div className={cx("flex flex-wrap items-center justify-between gap-3", className)} {...rest}>
      {children}
    </div>;
}
function TableSelection({
  checked,
  indeterminate = false,
  onCheckedChange,
  label,
  disabled,
  className,
  ...rest
}) {
  const { density } = useTable("TableSelection");
  const inputRef = useRef(null);
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.indeterminate = indeterminate && !checked;
    }
  }, [indeterminate, checked]);
  const active = checked || indeterminate;
  return <span
    className={cx(
      "relative inline-flex shrink-0 items-center justify-center",
      DENSITY_CLASSES[density].control
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
      active ? "border-[var(--ds-color-primary)] bg-[var(--ds-color-primary)]" : "border-[var(--ds-color-border)]",
      className
    )}
    {...rest}
  />
      <span
    aria-hidden="true"
    className="pointer-events-none absolute inset-0 flex items-center justify-center text-[var(--ds-color-primary-foreground)] [&_svg]:size-3"
  >
        {indeterminate && !checked ? DASH_GLYPH : <span
    className={cx(
      "inline-flex transition-opacity duration-150 ease-out motion-reduce:transition-none",
      checked ? "opacity-100" : "opacity-0"
    )}
  >
            {CHECK_GLYPH}
          </span>}
      </span>
    </span>;
}
function TableExpand({
  expanded,
  controls,
  label,
  className,
  ...rest
}) {
  const { density } = useTable("TableExpand");
  return <button
    type="button"
    aria-expanded={expanded}
    aria-controls={controls}
    aria-label={`${expanded ? "Collapse" : "Expand"} ${label ?? "row"}`}
    className={cx(
      "inline-flex items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none",
      density === "compact" ? "size-7" : "size-8",
      className
    )}
    {...rest}
  >
      <span
    aria-hidden="true"
    className={cx(
      "inline-flex transition-transform duration-150 ease-out motion-reduce:transition-none [&_svg]:size-4",
      expanded && "rotate-180"
    )}
  >
        {CHEVRON_DOWN_GLYPH}
      </span>
    </button>;
}
function clampPage(page, totalPages) {
  return Math.min(Math.max(1, page), Math.max(1, totalPages));
}
function pageRange(current, totalPages) {
  const total = Math.max(1, totalPages);
  const page = clampPage(current, total);
  if (total <= 7) {
    return Array.from({ length: total }, (_, index) => index + 1);
  }
  const wanted = /* @__PURE__ */ new Set([1, total, page - 1, page, page + 1]);
  const sorted = Array.from(wanted).filter((p) => p >= 1 && p <= total).sort((a, b) => a - b);
  const range = [];
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
const PAGINATION_CONTROL_BASE = "inline-flex h-8 min-w-8 select-none items-center justify-center gap-1 whitespace-nowrap rounded-[var(--ds-radius-sm)] px-2 text-[13px] font-medium leading-4 tabular-nums transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const PAGINATION_CONTROL_IDLE = "text-[var(--ds-color-muted-foreground)] hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)]";
const PAGINATION_CONTROL_CURRENT = "border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)]";
function TablePagination({
  page,
  defaultPage = 1,
  onPageChange,
  totalItems,
  pageSize = 10,
  pageSizeOptions,
  onPageSizeChange,
  label = "Table pagination",
  className
}) {
  const isControlled = page !== undefined;
  const [internal, setInternal] = useState(defaultPage);
  const totalPages = Math.max(1, Math.ceil(totalItems / Math.max(1, pageSize)));
  const current = clampPage(isControlled ? page : internal, totalPages);
  function setPage(next) {
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
  return <nav
    aria-label={label}
    className={cx("flex flex-wrap items-center justify-between gap-3", className)}
  >
      <p aria-live="polite" className="m-0 text-[13px] leading-4 text-[var(--ds-color-muted-foreground)]">
        Showing <span className="font-medium text-[var(--ds-color-foreground)]">{from}</span>
        {" \u2013 "}
        <span className="font-medium text-[var(--ds-color-foreground)]">{to}</span> of{" "}
        <span className="font-medium text-[var(--ds-color-foreground)]">{totalItems}</span>
      </p>
      <div className="flex flex-wrap items-center gap-3">
        {pageSizeOptions ? <label className="flex items-center gap-2 text-[13px] leading-4 text-[var(--ds-color-muted-foreground)]">
            Rows per page
            <select
    value={pageSize}
    onChange={(event) => onPageSizeChange?.(Number(event.target.value))}
    className="h-8 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-input)] px-2 text-[13px] leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:border-[var(--ds-color-border-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none"
  >
              {pageSizeOptions.map((option) => <option key={option} value={option}>
                  {option}
                </option>)}
            </select>
          </label> : null}
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
          {range.map(
    (item, index) => item === "ellipsis" ? <li key={`ellipsis-${index}`} className="inline-flex">
                <span
      className={cx(PAGINATION_CONTROL_BASE, "pointer-events-none text-[var(--ds-color-muted-foreground)]")}
    >
                  <span aria-hidden="true">…</span>
                  <span className="sr-only">More pages</span>
                </span>
              </li> : <li key={item} className="inline-flex">
                <button
      type="button"
      aria-label={item === current ? `Page ${item}` : `Go to page ${item}`}
      aria-current={item === current ? "page" : undefined}
      onClick={() => setPage(item)}
      className={cx(
        PAGINATION_CONTROL_BASE,
        item === current ? PAGINATION_CONTROL_CURRENT : PAGINATION_CONTROL_IDLE
      )}
    >
                  {item}
                </button>
              </li>
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
    </nav>;
}
function sortRows(rows, accessor, direction) {
  const sorted = [...rows];
  sorted.sort((a, b) => {
    const av = accessor(a);
    const bv = accessor(b);
    const compared = typeof av === "number" && typeof bv === "number" ? av - bv : String(av).localeCompare(String(bv));
    return direction === "asc" ? compared : -compared;
  });
  return sorted;
}
function useRowSelection(keys) {
  const [selected, setSelected] = useState(() => /* @__PURE__ */ new Set());
  const count = useMemo(
    () => keys.reduce((total, key) => selected.has(key) ? total + 1 : total, 0),
    [keys, selected]
  );
  const allSelected = keys.length > 0 && count === keys.length;
  const someSelected = count > 0 && !allSelected;
  const isSelected = useCallback((key) => selected.has(key), [selected]);
  const toggle = useCallback((key, checked) => {
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
    (checked) => {
      setSelected((previous) => {
        const currentlyAll = keys.length > 0 && keys.every((key) => previous.has(key));
        if (checked ?? !currentlyAll) {
          return new Set(keys);
        }
        return /* @__PURE__ */ new Set();
      });
    },
    [keys]
  );
  const clear = useCallback(() => setSelected(/* @__PURE__ */ new Set()), []);
  return { selected, count, allSelected, someSelected, isSelected, toggle, toggleAll, clear };
}

export { Table, TableCaption, TableHeader, TableBody, TableFooter, TableRow, TableHead, TableCell, TableEmpty, TableLoading, TableActions, TableToolbar, TableSelection, TableExpand, clampPage, pageRange, TablePagination, sortRows, useRowSelection };

export default Table;
