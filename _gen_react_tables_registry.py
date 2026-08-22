"""Registry for the DevSnips React Tables generator.

Each ``register()`` call adds one variant's metadata + showcase + README docs
+ ``tsx_header`` (the header doc comment of its derived ``code.tsx`` — the
shared core is identical to the authored reference ``table/code.tsx``). The
generator (``_gen_react_tables.py``) combines these with the reference
``code.tsx`` on disk to write ``code.tsx`` (derived), ``code.jsx``,
``preview.html``, ``metadata.json``, and ``README.md``.

Realistic, product-oriented demo content only (invoices, API tokens,
deployments, team members, audit logs, orders, reports, projects). No lorem
ipsum, no marketing buzzwords, no emoji.
"""
from _gen_react_tables import register

TAGS_BASE = ["table", "data-table", "react", "tailwind", "accessible", "responsive", "tokens"]
FEAT_BASE = ["semantic table elements", "light/dark", "reduced-motion", "focus-visible", "token-driven surfaces"]

# Preview demo helpers shared by every showcase (plain JSX, inlined per preview).
DEMO_HELPERS = r"""const NOTE = "m-0 text-xs leading-4 text-[var(--ds-color-muted-foreground)]";
const LABEL = "m-0 text-[11px] font-medium uppercase tracking-[0.04em] text-[var(--ds-color-muted-foreground)]";
const MONO = "font-mono text-[13px]";
const BTN_PRIMARY_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-[var(--ds-color-primary)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-primary-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,var(--ds-color-primary)_88%,#000)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_OUTLINE_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-foreground)] shadow-[var(--ds-shadow-xs)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_GHOST_SM = "inline-flex h-8 items-center justify-center gap-1.5 rounded-[var(--ds-radius-sm)] border border-transparent bg-transparent px-3 text-[13px] font-medium leading-4 text-[var(--ds-color-foreground)] transition-colors duration-150 ease-out hover:bg-[color-mix(in_srgb,currentColor_8%,transparent)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const BTN_ICON_GHOST = "inline-flex size-8 shrink-0 items-center justify-center rounded-[var(--ds-radius-sm)] text-[var(--ds-color-muted-foreground)] transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] hover:text-[var(--ds-color-foreground)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] disabled:pointer-events-none disabled:opacity-50 motion-reduce:transition-none";
const LINK = "font-medium text-[var(--ds-color-link)] underline underline-offset-2 transition-colors duration-150 ease-out hover:text-[var(--ds-color-link-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";
function money(v) { return "$" + v.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
"""

KEYBOARD_BASE = """Every interactive element in the table is a real native control, so the keyboard model is the browser's: Tab / Shift+Tab moves through sort buttons, checkboxes, expand triggers, links, action buttons, and pagination controls; Enter/Space activates them; and a `focus-visible` ring (2px, `color.focus-ring` token) marks keyboard focus. Rows are never fake buttons, so Tab never stops on a row itself — only on the operable controls inside it."""

A11Y_BASE = """- Real table semantics throughout: `<table>` / `<caption>` / `<thead>` / `<tbody>` / `<tfoot>` / `<tr>` / `<th scope="col">` / `<td>` — never a grid of divs, and no `role="grid"` re-declaration (native semantics are the correct semantics here).
- The `<TableCaption>` names the dataset for assistive technology; prefer it over an off-table heading.
- Controls are real native elements with accessible names: sort buttons announce their label, checkboxes carry `aria-label`, the expand trigger carries `aria-expanded` + `aria-controls`, and pagination controls carry `aria-current` / native `disabled`.
- State is never communicated by color alone: selection pairs its tinted surface with the checkbox's checked state and `aria-selected`; status badges pair a tinted dot with readable text; the indeterminate select-all state is the true `.indeterminate` IDL property."""

RESPONSIVE_BASE = """The table fills its container (`w-full`) inside a deliberate `overflow-x-auto` scroll region: when a dataset is genuinely wider than the viewport, the table scrolls horizontally inside its bordered container — the page itself never gains a scrollbar, and the caption, header rule, and row geometry stay intact. Cell text wraps by default; numeric columns use tabular figures so values stay comparable at any width. No horizontal page overflow at 375 / 768 / 1280px."""

STATES_BASE = """- **Header / footer** — `surface-subtle` with 1px `color.border` rules and `label-sm` type (12px, medium, muted).
- **Row** — `border-subtle` divider, a restrained `surface-hover` shift on hover, and a `transition-colors` that is disabled under reduced motion.
- **Selected row** — `aria-selected` + an accent-tinted surface derived from the accent token via `color-mix` (8% rest, 12% hover).
- **Disabled row** — `aria-disabled`, 60% opacity, no hover affordance; its controls are natively disabled.
- **Controls** — muted-at-rest with a foreground hover shift, a `focus-visible` ring, and native `disabled` styling (50% opacity, no pointer events)."""

# ---------------------------------------------------------------------------
# Shared props documentation
# ---------------------------------------------------------------------------

TABLE_PROPS = r"""### `<Table>`

| Name | Type | Default | Description |
|---|---|---|---|
| `density` | `"default" \| "compact"` | `"default"` | Cell/header density shared by every region primitive via context. |
| `loading` | `boolean` | `false` | Sets `aria-busy="true"` on the `<table>` (pair with `<TableLoading>`). |
| `containerClassName` | `string` | — | Extra classes on the bordered `overflow-x-auto` scroll container. |
| `className` | `string` | — | Extra classes on the `<table>` itself. |
| `children` | `ReactNode` | — | `TableCaption`, `TableHeader`, `TableBody`, `TableFooter` compositions. |

Every other attribute of a plain `<table>` (`id`, `aria-*`, `data-*`) is forwarded."""

CAPTION_PROPS = r"""### `<TableCaption>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the caption. |
| `children` | `ReactNode` | — | The dataset's name/description. |

A real `<caption>` rendered above the table — the accessible name of the dataset."""

SECTION_PROPS = r"""### `<TableHeader>` / `<TableBody>` / `<TableFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the section. |
| `children` | `ReactNode` | — | `TableRow` compositions. |

Real `<thead>` / `<tbody>` / `<tfoot>` elements. A grouped table renders one `<TableBody>` per group (multiple `<tbody>` elements are valid HTML)."""

ROW_PROPS = r"""### `<TableRow>`

| Name | Type | Default | Description |
|---|---|---|---|
| `selected` | `boolean` | `false` | `aria-selected="true"` + accent-tinted surface. |
| `disabled` | `boolean` | `false` | `aria-disabled="true"` + reduced opacity, no hover. Disable the row's controls too. |
| `className` | `string` | — | Extra classes on the row. |
| `children` | `ReactNode` | — | `TableHead` / `TableCell` children. |

A real `<tr>`. Rows are never fake buttons — interactive content lives in real controls inside the cells."""

HEAD_PROPS = r"""### `<TableHead>`

| Name | Type | Default | Description |
|---|---|---|---|
| `align` | `"left" \| "center" \| "right"` | `"left"` | Header alignment (match the column's cells). |
| `sortable` | `boolean` | `false` | Render the label as a real sort `<button>` and manage `aria-sort`. |
| `sortDirection` | `"asc" \| "desc" \| null` | `null` | Current direction; `null` = sortable but unsorted (`aria-sort="none"`). |
| `onSort` | `() => void` | — | Called when the sort button is activated. |
| `scope` | `string` | `"col"` | Header scope; use `"rowgroup"` for group header rows. |
| `className` | `string` | — | Extra classes on the `<th>`. |
| `children` | `ReactNode` | — | Header content. |

A real `<th scope="col">`; `colSpan` and the other native `<th>` attributes forward."""

CELL_PROPS = r"""### `<TableCell>`

| Name | Type | Default | Description |
|---|---|---|---|
| `align` | `"left" \| "center" \| "right"` | `"left"` | Cell alignment (numeric columns: `right`). |
| `numeric` | `boolean` | `false` | Tabular figures (`tabular-nums`) for numeric content. |
| `className` | `string` | — | Extra classes on the `<td>`. |
| `children` | `ReactNode` | — | Cell content — text, links, badges, controls. |

A real `<td>`; `colSpan` / `rowSpan` / `headers` forward natively."""

EMPTY_PROPS = r"""### `<TableEmpty>`

| Name | Type | Default | Description |
|---|---|---|---|
| `colSpan` | `number` | required | Columns the message spans (match the table's column count). |
| `title` | `string` | required | Zero-data headline. |
| `description` | `string` | — | Supporting explanation. |
| `action` | `ReactNode` | — | A real control that resolves the empty state. |
| `icon` | `ReactNode` | — | Decorative leading glyph (always `aria-hidden`). |

One real row with one spanning cell — never fake placeholder rows."""

LOADING_PROPS = r"""### `<TableLoading>`

| Name | Type | Default | Description |
|---|---|---|---|
| `columns` | `number` | required | Column count (match the table). |
| `rows` | `number` | `5` | Skeleton row count (pick a value close to the expected page size). |
| `label` | `string` | `"Loading data"` | Visually hidden announcement while loading. |

Geometry-preserving skeleton rows; the bars are `aria-hidden` and their pulse is disabled under reduced motion. Set `loading` on `<Table>` so the table reports `aria-busy`."""

ACTIONS_PROPS = r"""### `<TableActions>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the cluster. |
| `children` | `ReactNode` | — | Real `<button>` / `<a>` controls. |

An end-aligned control cluster for a cell (`<TableCell align="right">`). Never nest a control inside another control."""

TOOLBAR_PROPS = r"""### `<TableToolbar>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the region. |
| `children` | `ReactNode` | — | Counts, filters, primary actions. |

A layout-only `flex-wrap` region above the table — it renders no table markup and adds no ARIA of its own."""

SELECTION_PROPS = r"""### `<TableSelection>`

| Name | Type | Default | Description |
|---|---|---|---|
| `checked` | `boolean` | required | Current checked state (tracked by the caller). |
| `indeterminate` | `boolean` | `false` | "Some selected" tri-state — the true `.indeterminate` IDL property, set imperatively. |
| `onCheckedChange` | `(checked: boolean) => void` | — | Called with the next checked state. |
| `label` | `string` | required | Accessible name (the control is icon-only), e.g. `"Select all rows"`. |
| `disabled` | `boolean` | `false` | Native disabled (excluded from tab order and form submission). |

A REAL native `<input type="checkbox">` styled after the DevSnips Checkboxes family; other native input attributes (`name`, `value`, `id`) forward."""

EXPAND_PROPS = r"""### `<TableExpand>`

| Name | Type | Default | Description |
|---|---|---|---|
| `expanded` | `boolean` | required | Whether the associated content is expanded. |
| `controls` | `string` | — | `id` of the expanded content region (`aria-controls`). |
| `label` | `string` | `"row"` | Noun phrase completing the accessible name: "details for invoice INV-1042". |
| `onClick` | `(event) => void` | — | Toggle handler (other button attributes forward). |

A real `<button type="button">` with `aria-expanded`; the chevron rotation is reduced-motion safe."""

PAGINATION_PROPS = r"""### `<TablePagination>`

| Name | Type | Default | Description |
|---|---|---|---|
| `page` | `number` | — | Current page, 1-based (controlled). Omit to run uncontrolled. |
| `defaultPage` | `number` | `1` | Initial page (uncontrolled). |
| `onPageChange` | `(page: number) => void` | — | Called with the next 1-based page. |
| `totalItems` | `number` | required | Total rows across all pages. |
| `pageSize` | `number` | `10` | Rows per page. |
| `pageSizeOptions` | `readonly number[]` | — | When provided, renders a labelled native page-size `<select>`. |
| `onPageSizeChange` | `(pageSize: number) => void` | — | Called on page-size change (reset to page 1 here). |
| `label` | `string` | `"Table pagination"` | Accessible label for the `<nav>` landmark. |

Real `<button type="button">` controls, `aria-current="page"`, natively disabled boundaries, a windowed page list, and an `aria-live` "Showing X–Y of Z" status. Pages are clamped into range with the exported `clampPage`."""

HELPERS_PROPS = r"""### Typed helpers

| Export | Signature | Description |
|---|---|---|
| `sortRows` | `<T>(rows: readonly T[], accessor: (row: T) => string \| number, direction: "asc" \| "desc") => T[]` | Returns a sorted COPY (strings via `localeCompare`, numbers numerically); never mutates the input. |
| `useRowSelection` | `<K extends string \| number>(keys: readonly K[]) => RowSelection<K>` | Real selection state: `selected` set, `count`, `allSelected`, `someSelected`, `isSelected`, `toggle`, `toggleAll`, `clear`. Pass the SELECTABLE keys (exclude disabled rows). |
| `clampPage` | `(page: number, totalPages: number) => number` | Clamps a 1-based page into range (minimum 1). |
| `pageRange` | `(current: number, totalPages: number) => Array<number \| "ellipsis">` | The windowed page list used by `<TablePagination>`. |

Shared types: `TableDensity` (`"default" \| "compact"`), `TableAlign` (`"left" \| "center" \| "right"`), `SortDirection` (`"asc" \| "desc" \| null`), `RowSelection<K>`."""


def props_table():
    return "\n\n".join([
        TABLE_PROPS, CAPTION_PROPS, SECTION_PROPS, ROW_PROPS, HEAD_PROPS,
        CELL_PROPS, EMPTY_PROPS, LOADING_PROPS, ACTIONS_PROPS, TOOLBAR_PROPS,
        SELECTION_PROPS, EXPAND_PROPS, PAGINATION_PROPS, HELPERS_PROPS,
    ])


# ===========================================================================
# 1. table — reference implementation
# ===========================================================================
register(
    "table",
    title="Table",
    subcategory="Core",
    description="The reference table: a clean semantic data table (real <table>, <caption>, <thead>, <tbody>, <tfoot>, <th>, <td>) with aligned text and numeric columns, a totals footer, and the full compound region set every other variant in the family is built from.",
    tags=TAGS_BASE + ["reference", "compound", "caption", "footer", "numeric"],
    features=FEAT_BASE + ["compound regions", "caption + totals footer", "right-aligned tabular numerics"],
    accessibility=["native table semantics", "caption names the dataset", "th scope=col headers"],
    interactive=False,
    related=["table-sortable", "table-selectable", "table-with-pagination", "table-status"],
    usage='''import Table, {
  TableCaption,
  TableHeader,
  TableBody,
  TableFooter,
  TableRow,
  TableHead,
  TableCell,
} from "./table";

<Table>
  <TableCaption>Invoices for the 2026 billing year — amounts in USD.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Invoice</TableHead>
      <TableHead>Billing period</TableHead>
      <TableHead align="right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {invoices.map((inv) => (
      <TableRow key={inv.id}>
        <TableCell className="font-medium">{inv.id}</TableCell>
        <TableCell>{inv.period}</TableCell>
        <TableCell align="right" numeric>{money(inv.amount)}</TableCell>
      </TableRow>
    ))}
  </TableBody>
  <TableFooter>
    <TableRow>
      <TableCell colSpan={2}>Total</TableCell>
      <TableCell align="right" numeric>{money(total)}</TableCell>
    </TableRow>
  </TableFooter>
</Table>''',
    props_doc="\n\n".join([TABLE_PROPS, CAPTION_PROPS, SECTION_PROPS, ROW_PROPS, HEAD_PROPS, CELL_PROPS]),
    composition_note="The reference composes every structural region — caption, header, body, and a totals footer — so it doubles as the family's syntax reference. The footer is a real `<tfoot>`: it is announced as part of the table and stays at the bottom regardless of row count.",
    logic_doc="""The reference table is static: no sorting, selection, or pagination — just the structural regions and intentional alignment. Invoice ids render in the mono font, amounts and balances are right-aligned with tabular figures (`align="right"` + `numeric`), and the footer computes its totals from the same data array, so the summary can never disagree with the rows.

Alignment is the design decision that matters here: text is left-aligned, numeric values are right-aligned so digits line up for comparison, and the header alignment matches its column's cells.""",
    keyboard_doc=KEYBOARD_BASE + """

The reference table renders no interactive elements, so there is nothing extra to tab through — keyboard users read the table with their screen reader's table navigation (caption + `th scope="col"` headers make that navigation meaningful).""",
    behavior_doc=STATES_BASE,
    a11y_doc=A11Y_BASE,
    responsive_doc=RESPONSIVE_BASE + " The four-column invoice layout fits 375px without scrolling; wider datasets scroll inside the container, never the page.",
    notes_doc="Give every row a stable React `key` from the data (the invoice id here). The footer totals are computed from the same array as the rows — derive summaries, never hardcode them.",
    tsx_header='''/**
 * DevSnips React Table — reference implementation.
 *
 * A clean semantic data table over REAL table elements: `<Table>` renders a
 * bordered scroll container + native `<table>`, and the region primitives
 * map one-to-one onto table elements — `<TableCaption>` (`<caption>`),
 * `<TableHeader>` (`<thead>`), `<TableBody>` (`<tbody>`), `<TableFooter>`
 * (`<tfoot>`), `<TableRow>` (`<tr>`), `<TableHead>` (`<th scope="col">`),
 * `<TableCell>` (`<td>`). Never a grid of divs.
 *
 * This variant demonstrates the structural baseline every other variant
 * builds on: a caption naming the dataset, aligned text and numeric columns
 * (right-aligned tabular figures), and a totals footer computed from the
 * same data as the rows.
 */''',
    showcase=DEMO_HELPERS + '''
const INVOICES = [
  { id: "INV-1042", period: "Jul 1 – Jul 31, 2026", amount: 1240.00, balance: 0.00 },
  { id: "INV-1043", period: "Jun 1 – Jun 30, 2026", amount: 1240.00, balance: 0.00 },
  { id: "INV-1044", period: "May 1 – May 31, 2026", amount: 980.00, balance: 0.00 },
  { id: "INV-1045", period: "Apr 1 – Apr 30, 2026", amount: 980.00, balance: 0.00 },
  { id: "INV-1046", period: "Mar 1 – Mar 31, 2026", amount: 1412.50, balance: 172.50 },
  { id: "INV-1047", period: "Feb 1 – Feb 28, 2026", amount: 1412.50, balance: 0.00 },
];

function Showcase() {
  const totalAmount = INVOICES.reduce((sum, inv) => sum + inv.amount, 0);
  const totalBalance = INVOICES.reduce((sum, inv) => sum + inv.balance, 0);
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Semantic composition</p>
        <Table>
          <TableCaption>Invoices for the 2026 billing year — amounts in USD.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Invoice</TableHead>
              <TableHead>Billing period</TableHead>
              <TableHead align="right">Amount</TableHead>
              <TableHead align="right">Balance due</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {INVOICES.map((inv) => (
              <TableRow key={inv.id}>
                <TableCell className="font-medium"><span className={MONO}>{inv.id}</span></TableCell>
                <TableCell>{inv.period}</TableCell>
                <TableCell align="right" numeric>{money(inv.amount)}</TableCell>
                <TableCell align="right" numeric>{money(inv.balance)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TableCell colSpan={2}>Total</TableCell>
              <TableCell align="right" numeric>{money(totalAmount)}</TableCell>
              <TableCell align="right" numeric>{money(totalBalance)}</TableCell>
            </TableRow>
          </TableFooter>
        </Table>
        <p className={NOTE}>Real table elements throughout — caption, thead, tbody, tfoot, th, td. Numeric columns are right-aligned with tabular figures; the footer totals derive from the same data as the rows.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 2. table-with-actions
# ===========================================================================
register(
    "table-with-actions",
    title="Table with Actions",
    subcategory="Actions",
    description="A table with a trailing Actions column: a real View link, an icon-only Edit button, and a keyboard-navigable More-actions menu per row — composed from real controls, never nested or fake.",
    tags=TAGS_BASE + ["actions", "dropdown", "menu", "links", "buttons"],
    features=FEAT_BASE + ["row action cluster", "keyboard-navigable menu", "destructive action", "action log"],
    accessibility=["real buttons and links", "aria-haspopup=menu + aria-expanded", "Escape closes and refocuses the trigger", "no nested interactive elements"],
    interactive=True,
    related=["table", "table-status", "table-expandable"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell, TableActions,
} from "./table";

<TableCell align="right">
  <TableActions>
    <a href={`/tokens/${token.id}`}>View</a>
    <button type="button" aria-label={`Edit ${token.name}`} onClick={onEdit}>
      <EditIcon />
    </button>
    <RowMenu label={`More actions for ${token.name}`} items={menuItems} />
  </TableActions>
</TableCell>''',
    props_doc="\n\n".join([TABLE_PROPS, ROW_PROPS, HEAD_PROPS, CELL_PROPS, ACTIONS_PROPS]),
    composition_note="The Actions column is a plain `<TableCell align=\"right\">` wrapping a `<TableActions>` cluster. The header for that column carries a visually hidden \"Actions\" label so the column is named for screen readers without adding visual noise.",
    logic_doc="""Each row ends with three real controls: a View **link** (a real `<a href>` — browser navigation, middle-clickable), an icon-only Edit **button** (its accessible name comes from `aria-label`), and a More-actions **menu**.

The menu follows the DevSnips Dropdowns family's keyboard model, implemented self-contained in the preview: the trigger is a real `<button>` with `aria-haspopup="menu"` + `aria-expanded`; ArrowDown opens and focuses the first item, arrows/Home/End cycle, Escape closes and returns focus to the trigger, Tab closes, and outside pointer-down closes. Selecting an item runs the action, closes the menu, and restores focus to the trigger. Menus on the last two rows open upward so they are never clipped by the table's scroll container.

Every action records to the live demo log under the table — nothing is a dead control.""",
    keyboard_doc=KEYBOARD_BASE + """

The More-actions menu: Tab reaches the trigger, Enter/Space toggles it, ArrowDown opens it and focuses the first item (ArrowUp focuses the last), arrows cycle items, Home/End jump, Escape closes and refocuses the trigger, and Tab closes the menu and moves on. Focus is never stranded when the menu closes.""",
    behavior_doc=STATES_BASE + """

- **Menu** — `surface-elevated` panel, 1px `color.border`, `radius-md`, `shadow-md` (it is floating, unlike the table); items are 13px with a `surface-hover` shift; the destructive item uses the `color.destructive` token.
- **Actions column** — controls are consistently end-aligned via `<TableActions>`; icon-only buttons always carry an accessible name.""",
    a11y_doc=A11Y_BASE + """
- The menu trigger announces `aria-haspopup="menu"` + `aria-expanded`; the menu is `role="menu"` with real `<button role="menuitem">` children, and the destructive action is text + token color (never color alone).
- No nested interactive elements: the row is not clickable, and the View link, Edit button, and menu trigger are siblings.""",
    responsive_doc=RESPONSIVE_BASE + " The Actions column stays end-aligned and its controls remain reachable; at 375px the table scrolls inside its container and the menus flip upward near the bottom so they are never clipped.",
    notes_doc="The menu in this preview is a compact self-contained implementation of the DevSnips Dropdowns keyboard model — in an app, compose the Dropdowns family directly. Actions that mutate data should confirm or undo (Revoke here only logs, because this is a preview).",
    tsx_header='''/**
 * DevSnips React Table — table-with-actions.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on the trailing Actions column: `<TableActions>`
 * clusters real controls — a View link, an icon-only Edit button, and a
 * keyboard-navigable More-actions menu — inside a plain `<TableCell
 * align="right">`. Rows are never fake buttons and controls are never
 * nested inside one another.
 */''',
    showcase=DEMO_HELPERS + r'''
const TOKENS = [
  { id: "tok_1", name: "CI deploy key", prefix: "dsk_live_9f2", lastUsed: "2 hours ago", created: "2026-03-14" },
  { id: "tok_2", name: "Preview deployments", prefix: "dsk_live_41a", lastUsed: "Yesterday", created: "2026-05-02" },
  { id: "tok_3", name: "Metrics exporter", prefix: "dsk_live_7c8", lastUsed: "Aug 18, 2026", created: "2026-06-21" },
  { id: "tok_4", name: "Local development", prefix: "dsk_test_3e5", lastUsed: "Aug 10, 2026", created: "2026-07-08" },
  { id: "tok_5", name: "Legacy importer", prefix: "dsk_live_0b1", lastUsed: "Jun 30, 2026", created: "2025-11-19" },
];

const MENU_ITEM = "flex w-full items-center gap-2 rounded-[var(--ds-radius-sm)] px-2 py-1.5 text-left text-[13px] leading-4 transition-colors duration-150 ease-out hover:bg-[var(--ds-color-surface-hover)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--ds-color-focus-ring)] motion-reduce:transition-none";

function RowMenu({ label, up, items }) {
  const [open, setOpen] = React.useState(false);
  const rootRef = React.useRef(null);
  const triggerRef = React.useRef(null);
  const menuRef = React.useRef(null);

  React.useEffect(() => {
    if (!open) return undefined;
    function onPointerDown(event) {
      if (rootRef.current && !rootRef.current.contains(event.target)) setOpen(false);
    }
    function onKeyDown(event) {
      if (event.key === "Escape") {
        event.preventDefault();
        setOpen(false);
        if (triggerRef.current) triggerRef.current.focus();
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  function focusItem(which) {
    window.setTimeout(() => {
      if (!menuRef.current) return;
      const nodes = Array.from(menuRef.current.querySelectorAll('[role="menuitem"]'));
      const target = which === "last" ? nodes[nodes.length - 1] : nodes[0];
      if (target) target.focus();
    }, 0);
  }

  function onMenuKeyDown(event) {
    const nodes = Array.from(menuRef.current.querySelectorAll('[role="menuitem"]'));
    const index = nodes.indexOf(document.activeElement);
    if (event.key === "ArrowDown") {
      event.preventDefault();
      (nodes[index + 1] || nodes[0]).focus();
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      (nodes[index - 1] || nodes[nodes.length - 1]).focus();
    } else if (event.key === "Home") {
      event.preventDefault();
      nodes[0].focus();
    } else if (event.key === "End") {
      event.preventDefault();
      nodes[nodes.length - 1].focus();
    } else if (event.key === "Tab") {
      setOpen(false);
    }
  }

  return (
    <div ref={rootRef} className="relative inline-flex">
      <button
        ref={triggerRef}
        type="button"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={label}
        className={BTN_ICON_GHOST}
        onClick={() => setOpen((prev) => !prev)}
        onKeyDown={(event) => {
          if (event.key === "ArrowDown") { event.preventDefault(); setOpen(true); focusItem("first"); }
          else if (event.key === "ArrowUp") { event.preventDefault(); setOpen(true); focusItem("last"); }
        }}
      >
        <Icon name="more" />
      </button>
      {open ? (
        <div
          ref={menuRef}
          role="menu"
          aria-label={label}
          onKeyDown={onMenuKeyDown}
          className={"absolute right-0 z-10 min-w-40 rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface-elevated)] p-1 shadow-[var(--ds-shadow-md)] " + (up ? "bottom-full mb-1" : "top-full mt-1")}
        >
          {items.map((item) => (
            <button
              key={item.label}
              type="button"
              role="menuitem"
              className={MENU_ITEM + (item.destructive ? " text-[var(--ds-color-destructive)]" : " text-[var(--ds-color-foreground)]")}
              onClick={() => {
                setOpen(false);
                if (triggerRef.current) triggerRef.current.focus();
                item.onSelect();
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function Showcase() {
  const [log, setLog] = React.useState("No actions yet.");
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Row actions</p>
        <Table>
          <TableCaption>API tokens for the DevSnips workspace.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Prefix</TableHead>
              <TableHead>Last used</TableHead>
              <TableHead>Created</TableHead>
              <TableHead align="right"><span className="sr-only">Actions</span></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {TOKENS.map((token, index) => (
              <TableRow key={token.id}>
                <TableCell className="font-medium">{token.name}</TableCell>
                <TableCell><span className={MONO}>{token.prefix}</span></TableCell>
                <TableCell>{token.lastUsed}</TableCell>
                <TableCell>{token.created}</TableCell>
                <TableCell align="right">
                  <TableActions>
                    <a href={"#/tokens/" + token.id} className={LINK} onClick={() => setLog("Viewed " + token.name + ".")}>View</a>
                    <button type="button" aria-label={"Edit " + token.name} className={BTN_ICON_GHOST} onClick={() => setLog("Editing " + token.name + ".")}>
                      <Icon name="edit" />
                    </button>
                    <RowMenu
                      label={"More actions for " + token.name}
                      up={index >= TOKENS.length - 2}
                      items={[
                        { label: "Duplicate", onSelect: () => setLog("Duplicated " + token.name + ".") },
                        { label: "Rotate token", onSelect: () => setLog("Rotated " + token.name + ".") },
                        { label: "Revoke", destructive: true, onSelect: () => setLog("Revoked " + token.name + ".") },
                      ]}
                    />
                  </TableActions>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <p className={NOTE} aria-live="polite">Last action: {log}</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 3. table-sortable
# ===========================================================================
register(
    "table-sortable",
    title="Sortable Table",
    subcategory="Sorting",
    description="A table with real sortable columns: visible sort buttons inside the <th> elements, honest aria-sort values, a three-state cycle (ascending → descending → unsorted), and ordering that actually changes the data.",
    tags=TAGS_BASE + ["sorting", "aria-sort", "column-definitions", "keyboard"],
    features=FEAT_BASE + ["tri-state sort cycle", "aria-sort", "typed column definitions", "keyboard sort controls"],
    accessibility=["aria-sort ascending/descending/none", "visible sort buttons (not clickable th)", "keyboard-operable sorting"],
    interactive=True,
    related=["table", "table-with-pagination", "table-compact"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell, sortRows,
} from "./table";

const [sort, setSort] = useState<{ key: string | null; direction: SortDirection }>({
  key: null,
  direction: null,
});

function cycle(key: string) {
  setSort((prev) => {
    if (prev.key !== key) return { key, direction: "asc" };
    if (prev.direction === "asc") return { key, direction: "desc" };
    return { key: null, direction: null }; // unsorted: original order
  });
}

const column = columns.find((c) => c.key === sort.key);
const rows = column && sort.direction
  ? sortRows(data, column.accessor, sort.direction)
  : data;

<TableHead
  sortable
  sortDirection={sort.key === "service" ? sort.direction : null}
  onSort={() => cycle("service")}
>
  Service
</TableHead>''',
    props_doc="\n\n".join([TABLE_PROPS, HEAD_PROPS, CELL_PROPS, HELPERS_PROPS]),
    composition_note="Only the Duration column is numeric — its header and cells share `align=\"right\"` + `numeric` so the sorted values line up digit-for-digit. Columns are described once in a typed `COLUMNS` array (key, label, accessor, optional align/format) and mapped to both header and cells.",
    logic_doc="""Sorting is real and state-driven. Clicking a sortable header cycles **ascending → descending → unsorted**: the first click sorts ascending, the second reverses it, and the third restores the original data order (a genuine reset, not a third sort).

The visible control is a `<button type="button">` rendered inside the `<th>` by `TableHead sortable` — the `<th>` itself is never a mysterious clickable region. The `<th>` carries `aria-sort`: `"ascending"` / `"descending"` on the active column and `"none"` on the other sortable columns, and a direction glyph shows the same state visually.

The ordering itself comes from the typed `sortRows(rows, accessor, direction)` helper: strings compare with `localeCompare`, numbers compare numerically, and the input array is never mutated. Only one column sorts at a time, so `aria-sort` is always honest.""",
    keyboard_doc=KEYBOARD_BASE + """

Sorting is fully keyboard-operable: Tab reaches each sort button (they are real buttons in the header cells), and Enter/Space activates the cycle — ascending, descending, unsorted. The `aria-sort` change is announced, and focus stays on the button while the rows reorder beneath it.""",
    behavior_doc=STATES_BASE + """

- **Sort glyphs** — the unsorted state shows a muted up/down glyph (40% opacity affordance); the active direction shows a solid arrow in the foreground color. The glyph supplements `aria-sort`, it never replaces it.""",
    a11y_doc=A11Y_BASE + """
- `aria-sort` is set on the `<th>` (not the button), per the ARIA sortable-table pattern: `"ascending"` / `"descending"` on the sorted column, `"none"` on sortable-but-inactive columns, and absent entirely on non-sortable columns.""",
    responsive_doc=RESPONSIVE_BASE + " Sort buttons wrap with their labels and remain fully operable at 375px.",
    notes_doc="The demo sorts strings (Service, Region, Deployed as zero-padded ISO timestamps) and numbers (Duration) through the same `sortRows` helper. Dates stored as ISO-8601 strings sort chronologically with plain string comparison — keep them zero-padded.",
    tsx_header='''/**
 * DevSnips React Table — table-sortable.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on real sorting: `<TableHead sortable>` renders a
 * visible sort `<button>` inside the `<th>`, manages `aria-sort`
 * (ascending / descending / none), and the typed `sortRows` helper orders
 * the data for real — ascending, descending, then back to the original
 * order.
 */''',
    showcase=DEMO_HELPERS + '''
const DEPLOYMENTS = [
  { id: "d1", service: "api-gateway", region: "us-east-1", durationSeconds: 148, deployedAt: "2026-08-21 14:32" },
  { id: "d2", service: "billing-service", region: "eu-west-1", durationSeconds: 96, deployedAt: "2026-08-21 11:05" },
  { id: "d3", service: "edge-cache", region: "ap-southeast-2", durationSeconds: 61, deployedAt: "2026-08-20 22:47" },
  { id: "d4", service: "auth-service", region: "us-east-1", durationSeconds: 183, deployedAt: "2026-08-20 16:20" },
  { id: "d5", service: "data-pipeline", region: "us-west-2", durationSeconds: 402, deployedAt: "2026-08-19 08:11" },
  { id: "d6", service: "docs-site", region: "eu-central-1", durationSeconds: 34, deployedAt: "2026-08-18 19:58" },
  { id: "d7", service: "metrics-api", region: "us-east-1", durationSeconds: 77, deployedAt: "2026-08-18 07:26" },
  { id: "d8", service: "search-indexer", region: "ap-south-1", durationSeconds: 265, deployedAt: "2026-08-17 13:40" },
];

const COLUMNS = [
  { key: "service", label: "Service", accessor: (row) => row.service },
  { key: "region", label: "Region", accessor: (row) => row.region },
  { key: "duration", label: "Duration", align: "right", numeric: true, accessor: (row) => row.durationSeconds, format: (row) => row.durationSeconds + "s" },
  { key: "deployed", label: "Deployed", accessor: (row) => row.deployedAt },
];

function Showcase() {
  const [sort, setSort] = React.useState({ key: null, direction: null });
  function cycle(key) {
    setSort((prev) => {
      if (prev.key !== key) return { key: key, direction: "asc" };
      if (prev.direction === "asc") return { key: key, direction: "desc" };
      return { key: null, direction: null };
    });
  }
  const activeColumn = COLUMNS.find((c) => c.key === sort.key);
  const rows = React.useMemo(
    () => (activeColumn && sort.direction ? sortRows(DEPLOYMENTS, activeColumn.accessor, sort.direction) : DEPLOYMENTS),
    [sort, activeColumn]
  );
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Sortable columns</p>
        <Table>
          <TableCaption>Recent deployments. Activate a column header to sort; activate again to reverse, and a third time to restore the original order.</TableCaption>
          <TableHeader>
            <TableRow>
              {COLUMNS.map((column) => (
                <TableHead
                  key={column.key}
                  align={column.align || "left"}
                  sortable
                  sortDirection={sort.key === column.key ? sort.direction : null}
                  onSort={() => cycle(column.key)}
                >
                  {column.label}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.id}>
                <TableCell className="font-medium">{row.service}</TableCell>
                <TableCell><span className={MONO}>{row.region}</span></TableCell>
                <TableCell align="right" numeric>{row.durationSeconds}s</TableCell>
                <TableCell><span className={MONO}>{row.deployedAt}</span></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <p className={NOTE} aria-live="polite">{activeColumn && sort.direction ? "Sorted by " + activeColumn.label + (sort.direction === "asc" ? " (ascending)." : " (descending).") : "Unsorted — original order."}</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 4. table-selectable
# ===========================================================================
register(
    "table-selectable",
    title="Selectable Table",
    subcategory="Selection",
    description="A table with real row selection: native checkboxes, a select-all header checkbox with a true indeterminate tri-state, selected-row styling with aria-selected, a live selected count, and a disabled row excluded from selection.",
    tags=TAGS_BASE + ["selection", "checkbox", "indeterminate", "select-all", "aria-selected"],
    features=FEAT_BASE + ["row + select-all checkboxes", "true indeterminate tri-state", "selected count", "disabled row", "bulk remove"],
    accessibility=["native checkboxes with aria-label", "true .indeterminate IDL state", "aria-selected rows", "live selected count"],
    interactive=True,
    related=["table", "table-with-pagination", "table-with-actions"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell,
  TableSelection, TableToolbar, useRowSelection,
} from "./table";

const selectableKeys = members.filter((m) => !m.disabled).map((m) => m.id);
const selection = useRowSelection(selectableKeys);

<TableHead className="w-10">
  <TableSelection
    checked={selection.allSelected}
    indeterminate={selection.someSelected}
    onCheckedChange={() => selection.toggleAll()}
    label="Select all members"
  />
</TableHead>

{members.map((m) => (
  <TableRow key={m.id} selected={selection.isSelected(m.id)} disabled={m.disabled}>
    <TableCell className="w-10">
      <TableSelection
        checked={selection.isSelected(m.id)}
        onCheckedChange={(checked) => selection.toggle(m.id, checked)}
        label={`Select ${m.name}`}
        disabled={m.disabled}
      />
    </TableCell>
    <TableCell>{m.name}</TableCell>
  </TableRow>
))}''',
    props_doc="\n\n".join([TABLE_PROPS, ROW_PROPS, HEAD_PROPS, CELL_PROPS, SELECTION_PROPS, TOOLBAR_PROPS, HELPERS_PROPS]),
    composition_note="The selection column is a narrow first column (`w-10`) containing `<TableSelection>` — a native checkbox in the header for select-all and one per row. The `<TableToolbar>` above the table holds the live count and the bulk action.",
    logic_doc="""Selection is real state, tracked by the typed `useRowSelection(selectableKeys)` hook: a `Set` of selected keys plus the derived `count`, `allSelected`, and `someSelected` flags. The demo's **Remove selected** bulk action genuinely removes the rows and clears the selection.

The header checkbox synchronizes in both directions: it is **checked** when every selectable row is selected, **indeterminate** when some are (the true `.indeterminate` IDL property — rendered as a dash, distinct from the check mark), and **unchecked** when none are. Activating it selects or clears every selectable row.

The suspended member demonstrates disabled rows: its checkbox is natively `disabled`, the row carries `aria-disabled` with reduced opacity and no hover, and its key is excluded from `selectableKeys` — so select-all never selects it and the count reads "N of 5", not "N of 6".""",
    keyboard_doc=KEYBOARD_BASE + """

Selection is fully keyboard-operable: Tab reaches each native checkbox (header first, then row by row) and Space toggles it — the browser's native checkbox behavior, no custom key handling. The bulk action in the toolbar is a real button right after the table in the tab order.""",
    behavior_doc=STATES_BASE + """

- **Checked checkbox** — `color.primary` fill with a `color.primary-foreground` check mark.
- **Indeterminate checkbox** — `color.primary` fill with a dash, set via the `.indeterminate` IDL property (there is no HTML attribute).
- **Selected row** — `aria-selected="true"` + accent-tinted surface; the checkbox state carries the same information, so selection is never color alone.""",
    a11y_doc=A11Y_BASE + """
- Every checkbox has an accessible name (`"Select all members"`, `"Select Ada Lovelace"`); the visible row text is the label's context.
- The selected count is an `aria-live="polite"` region so bulk changes are announced.""",
    responsive_doc=RESPONSIVE_BASE + " The selection column keeps a fixed narrow width (`w-10`) so checkboxes stay tappable at 375px, and the toolbar wraps above the table.",
    notes_doc="Pass only the SELECTABLE keys to `useRowSelection` (exclude disabled rows) — `allSelected` / `someSelected` / the count are then correct by construction. When rows are removed, call `clear()` (or prune the set) so stale keys never linger.",
    tsx_header='''/**
 * DevSnips React Table — table-selectable.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on real selection: `<TableSelection>` native
 * checkboxes, a select-all header checkbox with the true `.indeterminate`
 * IDL tri-state, `aria-selected` rows with an accent-tinted surface, a live
 * selected count, and disabled rows excluded from select-all — all driven
 * by the typed `useRowSelection` hook.
 */''',
    showcase=DEMO_HELPERS + '''
const INITIAL_MEMBERS = [
  { id: "m1", name: "Ada Lovelace", email: "ada@devsnips.io", role: "Owner", joined: "2024-11-02", disabled: false },
  { id: "m2", name: "Grace Hopper", email: "grace@devsnips.io", role: "Engineer", joined: "2025-01-19", disabled: false },
  { id: "m3", name: "Alan Turing", email: "alan@devsnips.io", role: "Engineer", joined: "2025-03-08", disabled: false },
  { id: "m4", name: "Edsger Dijkstra", email: "edsger@devsnips.io", role: "Engineer — suspended", joined: "2025-04-27", disabled: true },
  { id: "m5", name: "Margaret Hamilton", email: "margaret@devsnips.io", role: "Designer", joined: "2025-09-14", disabled: false },
  { id: "m6", name: "Katherine Johnson", email: "katherine@devsnips.io", role: "Analyst", joined: "2026-02-01", disabled: false },
];

function Showcase() {
  const [members, setMembers] = React.useState(INITIAL_MEMBERS);
  const selectableKeys = React.useMemo(() => members.filter((m) => !m.disabled).map((m) => m.id), [members]);
  const selection = useRowSelection(selectableKeys);
  function removeSelected() {
    setMembers((prev) => prev.filter((m) => !selection.selected.has(m.id)));
    selection.clear();
  }
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Row selection</p>
        <TableToolbar>
          <p className={NOTE} aria-live="polite">{selection.count} of {selectableKeys.length} selected</p>
          <button type="button" className={BTN_OUTLINE_SM} disabled={selection.count === 0} onClick={removeSelected}>Remove selected</button>
        </TableToolbar>
        <Table>
          <TableCaption>Workspace members. Suspended members cannot be selected.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead className="w-10">
                <TableSelection
                  checked={selection.allSelected}
                  indeterminate={selection.someSelected}
                  onCheckedChange={() => selection.toggleAll()}
                  label="Select all members"
                />
              </TableHead>
              <TableHead>Member</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Joined</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {members.map((member) => (
              <TableRow key={member.id} selected={selection.isSelected(member.id)} disabled={member.disabled}>
                <TableCell className="w-10">
                  <TableSelection
                    checked={selection.isSelected(member.id)}
                    onCheckedChange={(checked) => selection.toggle(member.id, checked)}
                    label={"Select " + member.name}
                    disabled={member.disabled}
                  />
                </TableCell>
                <TableCell className="font-medium">
                  {member.name}
                  <span className="block text-[13px] font-normal leading-4 text-[var(--ds-color-muted-foreground)]">{member.email}</span>
                </TableCell>
                <TableCell>{member.role}</TableCell>
                <TableCell>{member.joined}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <p className={NOTE}>The header checkbox reflects none / some (indeterminate dash) / all. The suspended member is excluded from select-all, and Remove selected genuinely removes rows.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 5. table-with-pagination
# ===========================================================================
register(
    "table-with-pagination",
    title="Table with Pagination",
    subcategory="Pagination",
    description="A table integrated with real pagination: changing the page or page size changes the visible rows, Previous/Next disable at the boundaries, the current page carries aria-current, and an aria-live status announces the visible range.",
    tags=TAGS_BASE + ["pagination", "page-size", "aria-current", "windowed pages"],
    features=FEAT_BASE + ["self-contained pagination bar", "page-size select", "boundary disabling", "aria-live range status"],
    accessibility=["nav landmark with accessible label", "aria-current=page", "native disabled boundaries", "aria-live status"],
    interactive=True,
    related=["table", "table-sortable", "table-selectable"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell,
  TablePagination, clampPage,
} from "./table";

const [page, setPage] = useState(1);
const [pageSize, setPageSize] = useState(8);
const totalPages = Math.max(1, Math.ceil(entries.length / pageSize));
const safePage = clampPage(page, totalPages);
const visible = entries.slice((safePage - 1) * pageSize, safePage * pageSize);

<Table>…rows={visible}…</Table>
<TablePagination
  page={safePage}
  onPageChange={setPage}
  totalItems={entries.length}
  pageSize={pageSize}
  pageSizeOptions={[8, 12, 20]}
  onPageSizeChange={(size) => { setPageSize(size); setPage(1); }}
/>''',
    props_doc="\n\n".join([TABLE_PROPS, HEAD_PROPS, CELL_PROPS, PAGINATION_PROPS, HELPERS_PROPS]),
    composition_note="`<TablePagination>` renders BELOW the table (outside the bordered container) — it is a navigation landmark, not a table region. The parent owns the page state and slices the dataset; the component reports and changes the page.",
    logic_doc="""The pagination is real: the 42-event audit log is sliced by the current page, so changing the page or the page size changes the visible rows. Previous/Next disable natively at the boundaries (page 1 and the last page), the current page button carries `aria-current="page"`, and the page list windows with non-interactive ellipses when the count is large.

State integrity is guarded two ways: the exported `clampPage` keeps the current page inside the valid range (so shrinking the dataset or growing the page size can never land on an empty page), and changing the page size resets to page 1 — the only predictable behavior when the page geometry changes.

The "Showing X–Y of Z" status is an `aria-live="polite"` region, so page changes are announced without moving focus.""",
    keyboard_doc=KEYBOARD_BASE + """

Every pagination control is a real `<button type="button">` (the page-size control is a native `<select>`): Tab moves through Previous, the page numbers, Next, and the select; Enter/Space activates a button; the select opens natively. Disabled boundary buttons leave the tab order entirely.""",
    behavior_doc=STATES_BASE + """

- **Current page** — bordered `surface` chip with `shadow-xs` + `aria-current="page"` (structure, not color alone).
- **Page-size select** — input surface with a hover border shift and a focus ring, labelled "Rows per page".""",
    a11y_doc=A11Y_BASE + """
- The pagination bar is a `<nav aria-label="Table pagination">` landmark, distinct from the table itself.
- Ellipses are non-interactive spans (`aria-hidden` glyph + sr-only "More pages") — never fake buttons.""",
    responsive_doc=RESPONSIVE_BASE + " The pagination bar is `flex-wrap`: at 375px the status, page-size select, and controls wrap onto their own lines instead of overflowing, and every control keeps its 32px target height.",
    notes_doc="This demo keeps selection and pagination in separate variants deliberately: if you combine them, decide and document whether selection persists across pages (a key-based `Set` from `useRowSelection` persists naturally).",
    tsx_header='''/**
 * DevSnips React Table — table-with-pagination.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on real pagination: `<TablePagination>` — a
 * self-contained `<nav>` bar following the DevSnips Pagination family's
 * semantics (real buttons, `aria-current`, natively disabled boundaries,
 * windowed pages, `aria-live` range status, optional page-size select). The
 * parent slices the dataset; every page value is clamped so an empty page
 * cannot occur.
 */''',
    showcase=DEMO_HELPERS + '''
const ACTORS = ["ada", "grace", "alan", "margaret", "katherine", "edsger"];
const AUDIT_ACTIONS = ["deployed", "rotated keys for", "invited a member to", "updated settings on", "created a branch on", "archived"];
const AUDIT_TARGETS = ["api-gateway", "billing-service", "docs-site", "edge-cache", "auth-service", "data-pipeline"];
const AUDIT = Array.from({ length: 42 }, (_, i) => ({
  id: "evt_" + (1000 + i),
  actor: ACTORS[i % ACTORS.length],
  action: AUDIT_ACTIONS[i % AUDIT_ACTIONS.length],
  target: AUDIT_TARGETS[(i * 3 + 1) % AUDIT_TARGETS.length],
  time: "2026-08-" + String(22 - Math.floor(i / 3)).padStart(2, "0") + " " + String(9 + (i % 9)).padStart(2, "0") + ":" + String((i * 7) % 60).padStart(2, "0"),
}));

function Showcase() {
  const [page, setPage] = React.useState(1);
  const [pageSize, setPageSize] = React.useState(8);
  const totalPages = Math.max(1, Math.ceil(AUDIT.length / pageSize));
  const safePage = clampPage(page, totalPages);
  React.useEffect(() => {
    if (page !== safePage) setPage(safePage);
  }, [page, safePage]);
  const visible = AUDIT.slice((safePage - 1) * pageSize, safePage * pageSize);
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Paginated dataset</p>
        <Table>
          <TableCaption>Audit log — 42 events, paged.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Event</TableHead>
              <TableHead>Actor</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Target</TableHead>
              <TableHead>Time</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {visible.map((entry) => (
              <TableRow key={entry.id}>
                <TableCell><span className={MONO}>{entry.id}</span></TableCell>
                <TableCell className="font-medium">{entry.actor}</TableCell>
                <TableCell>{entry.action}</TableCell>
                <TableCell>{entry.target}</TableCell>
                <TableCell><span className={MONO}>{entry.time}</span></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          page={safePage}
          onPageChange={setPage}
          totalItems={AUDIT.length}
          pageSize={pageSize}
          pageSizeOptions={[8, 12, 20]}
          onPageSizeChange={(size) => { setPageSize(size); setPage(1); }}
        />
        <p className={NOTE}>Changing the page or page size changes the visible rows. Previous/Next disable at the boundaries, and the range status is announced.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 6. table-expandable
# ===========================================================================
register(
    "table-expandable",
    title="Expandable Table",
    subcategory="Expansion",
    description="A table with expandable rows: a real toggle button per row (aria-expanded + aria-controls), an associated detail panel rendered as a real spanning row, instant reduced-motion-safe toggling, and multiple rows open at once.",
    tags=TAGS_BASE + ["expandable", "collapsible", "aria-expanded", "row-details"],
    features=FEAT_BASE + ["expand/collapse toggle", "associated detail panel", "multiple open rows", "no layout-jump animation"],
    accessibility=["aria-expanded + aria-controls", "keyboard-operable toggle", "focus stays on the trigger"],
    interactive=True,
    related=["table", "table-grouped", "table-with-actions"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell, TableExpand,
} from "./table";

const [expanded, setExpanded] = useState<ReadonlySet<string>>(new Set());

{orders.map((order) => {
  const open = expanded.has(order.id);
  const panelId = `order-${order.id}-details`;
  return (
    <Fragment key={order.id}>
      <TableRow>
        <TableCell className="w-10">
          <TableExpand
            expanded={open}
            controls={panelId}
            label={`details for order ${order.id}`}
            onClick={() => toggle(order.id)}
          />
        </TableCell>
        <TableCell>{order.id}</TableCell>
      </TableRow>
      {open ? (
        <TableRow>
          <TableCell colSpan={5} id={panelId}>
            …line items + delivery note…
          </TableCell>
        </TableRow>
      ) : null}
    </Fragment>
  );
})}''',
    props_doc="\n\n".join([TABLE_PROPS, ROW_PROPS, HEAD_PROPS, CELL_PROPS, EXPAND_PROPS]),
    composition_note="The expand column is a narrow first column (`w-10`) of `<TableExpand>` triggers; its header carries a visually hidden \"Expand\" label. The detail panel is a real second row per data row — a `<TableCell colSpan>` on the `surface-subtle` background — whose `id` matches the trigger's `aria-controls`.",
    logic_doc="""Expansion is real and independently tracked per row: a `Set` of open order ids, so any number of rows can be open at once. The trigger is `<TableExpand>` — a real `<button type="button">` with `aria-expanded` and `aria-controls` pointing at the panel row's cell id.

The panel is a real `<TableRow>` rendered directly after its parent row, containing line items as a description list (name × quantity, line total) plus the delivery note — deliberately NOT a nested table, because line items here are a summary, not tabular data.

Toggling is instant (no height animation): the row appears or disappears in one frame, so there is no layout thrash, nothing is ever trapped in a half-open state, and reduced-motion users lose nothing. Focus stays on the trigger when a row opens or closes.""",
    keyboard_doc=KEYBOARD_BASE + """

The expand trigger is a real button: Tab reaches it, Enter/Space toggles the row, and focus remains on the trigger after toggling — so a keyboard user can open a row, Tab once into the panel's content, and Shift+Tab back. The chevron rotation is the only motion and it is reduced-motion safe.""",
    behavior_doc=STATES_BASE + """

- **Expanded panel** — `surface-subtle` background spanning all columns, visually grouped under its parent row.
- **Trigger** — muted chevron that rotates 180° while open, with a `surface-hover` wash and a focus ring.""",
    a11y_doc=A11Y_BASE + """
- The trigger's accessible name describes what expands ("Expand details for order ORD-5201" / "Collapse details for order ORD-5201"), and `aria-controls` associates it with the panel's `id`.
- Expanded content is plain readable content in the table flow — it is never hidden from keyboard or screen-reader users while open.""",
    responsive_doc=RESPONSIVE_BASE + " The detail panel spans all columns and its line items wrap at 375px; the trigger keeps a 32px target in the narrow expand column.",
    notes_doc="Multiple rows can be open at once (tracked as a `Set`). If your product wants an accordion instead, close the siblings in the same `toggle` — the primitive does not impose either policy.",
    tsx_header='''/**
 * DevSnips React Table — table-expandable.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on real row expansion: `<TableExpand>` — a real
 * toggle button with `aria-expanded` + `aria-controls` — opens a detail
 * panel rendered as a real spanning row associated with the correct record.
 * Toggling is instant (no layout-jump animation), multiple rows can be
 * open, and focus stays on the trigger.
 */''',
    showcase=DEMO_HELPERS + '''
const ORDERS = [
  { id: "ORD-5201", customer: "Northwind Studio", date: "2026-08-18", total: 348.00, items: [ { name: "Desk lamp — brass", qty: 2, price: 129.00 }, { name: "Cable tray", qty: 1, price: 90.00 } ], note: "Delivered Aug 20 — signed at reception." },
  { id: "ORD-5202", customer: "Harbor & Co", date: "2026-08-17", total: 129.00, items: [ { name: "Desk lamp — brass", qty: 1, price: 129.00 } ], note: "Ships in two parcels; the second arrives Aug 25." },
  { id: "ORD-5203", customer: "Meredith Lane", date: "2026-08-15", total: 812.50, items: [ { name: "Lounge chair — oak", qty: 1, price: 640.00 }, { name: "Wool throw", qty: 1, price: 172.50 } ], note: "White-glove delivery scheduled for Aug 28." },
  { id: "ORD-5204", customer: "Atlas Freight", date: "2026-08-12", total: 258.00, items: [ { name: "Cable tray", qty: 2, price: 90.00 }, { name: "Monitor arm", qty: 1, price: 78.00 } ], note: "Delivered Aug 14." },
  { id: "ORD-5205", customer: "Quiet Place Books", date: "2026-08-09", total: 469.00, items: [ { name: "Bookshelf — walnut", qty: 1, price: 469.00 } ], note: "Customer requested a Saturday delivery window." },
];

function Showcase() {
  const [expanded, setExpanded] = React.useState(() => new Set());
  function toggle(id) {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Expandable rows</p>
        <Table>
          <TableCaption>Recent orders. Expand a row for line items and delivery notes.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead className="w-10"><span className="sr-only">Expand</span></TableHead>
              <TableHead>Order</TableHead>
              <TableHead>Customer</TableHead>
              <TableHead>Date</TableHead>
              <TableHead align="right">Total</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {ORDERS.map((order) => {
              const open = expanded.has(order.id);
              const panelId = "order-" + order.id + "-details";
              return (
                <React.Fragment key={order.id}>
                  <TableRow>
                    <TableCell className="w-10">
                      <TableExpand expanded={open} controls={panelId} label={"details for order " + order.id} onClick={() => toggle(order.id)} />
                    </TableCell>
                    <TableCell className="font-medium"><span className={MONO}>{order.id}</span></TableCell>
                    <TableCell>{order.customer}</TableCell>
                    <TableCell>{order.date}</TableCell>
                    <TableCell align="right" numeric>{money(order.total)}</TableCell>
                  </TableRow>
                  {open ? (
                    <TableRow>
                      <TableCell colSpan={5} id={panelId} className="bg-[var(--ds-color-surface-subtle)] px-4 py-3">
                        <dl className="m-0 space-y-1">
                          {order.items.map((item) => (
                            <div key={item.name} className="flex items-baseline justify-between gap-4 text-[13px] leading-5">
                              <dt className="text-[var(--ds-color-foreground)]">{item.name} × {item.qty}</dt>
                              <dd className="m-0 tabular-nums text-[var(--ds-color-muted-foreground)]">{money(item.price * item.qty)}</dd>
                            </div>
                          ))}
                        </dl>
                        <p className="m-0 mt-2 text-[13px] leading-5 text-[var(--ds-color-muted-foreground)]">{order.note}</p>
                      </TableCell>
                    </TableRow>
                  ) : null}
                </React.Fragment>
              );
            })}
          </TableBody>
        </Table>
        <p className={NOTE}>Multiple rows can be open at once. The panel is a real row associated with its trigger via aria-controls — not a nested table.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 7. table-grouped
# ===========================================================================
register(
    "table-grouped",
    title="Grouped Table",
    subcategory="Grouping",
    description="A table with logically grouped rows: one <tbody> per department, a th scope=rowgroup header row per group (visually distinct without color alone), member counts, and collapsible groups.",
    tags=TAGS_BASE + ["grouping", "rowgroup", "collapsible", "multiple-tbody"],
    features=FEAT_BASE + ["one tbody per group", "scope=rowgroup headers", "collapse/expand groups", "member counts"],
    accessibility=["th scope=rowgroup", "aria-expanded group toggles", "group identity not color-alone"],
    interactive=True,
    related=["table", "table-expandable", "table-compact"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell,
} from "./table";

{groups.map((group) => (
  <TableBody key={group.slug} id={`group-${group.slug}-rows`}>
    <TableRow className="bg-[var(--ds-color-surface-subtle)]">
      <TableHead scope="rowgroup" colSpan={4} className="h-auto px-3 py-2">
        <button
          type="button"
          aria-expanded={!collapsed.has(group.slug)}
          aria-controls={`group-${group.slug}-rows`}
          onClick={() => toggleGroup(group.slug)}
        >
          {group.name} · {group.members.length} people
        </button>
      </TableHead>
    </TableRow>
    {collapsed.has(group.slug) ? null : group.members.map((m) => (
      <TableRow key={m.name}>…</TableRow>
    ))}
  </TableBody>
))}''',
    props_doc="\n\n".join([TABLE_PROPS, SECTION_PROPS, ROW_PROPS, HEAD_PROPS, CELL_PROPS]),
    composition_note="A grouped table renders one `<TableBody>` per group (multiple `<tbody>` elements are valid HTML) with a group header row whose `<TableHead scope=\"rowgroup\" colSpan>` labels every row beneath it.",
    logic_doc="""Rows are grouped by department — Engineering, Design, Operations — with each group in its own `<tbody>`. The group header row spans all columns with `<th scope="rowgroup">`, so assistive technology announces the department as the header for every row in its group.

Groups are distinguishable without relying on color: an uppercase tracked label, a building glyph, a member count, a collapse chevron, AND a `surface-subtle` background — five cues, one of which is structural.

Each group collapses independently: the toggle is a real button with `aria-expanded` and `aria-controls` pointing at the group's `<tbody id>`. Collapsing removes the member rows from the table (they are not merely hidden with CSS), and the count stays visible so the group never looks empty by accident.""",
    keyboard_doc=KEYBOARD_BASE + """

Each group toggle is a real button: Tab reaches it and Enter/Space collapses or expands the group. Collapsed groups remove their rows from the tab order entirely, so keyboard users never tab into hidden content.""",
    behavior_doc=STATES_BASE + """

- **Group header row** — `surface-subtle` background, uppercase `label-sm` text, building glyph, member count, and a chevron that reflects the collapse state.""",
    a11y_doc=A11Y_BASE + """
- `<th scope="rowgroup">` makes the department the announced header for every row in its group — grouping is conveyed structurally, not just visually.
- The group toggle's accessible name ("Collapse Engineering group") and `aria-expanded` state make the group's visibility unambiguous.""",
    responsive_doc=RESPONSIVE_BASE + " Group header rows span all columns and their labels wrap at 375px; the toggle keeps a 24px+ target.",
    notes_doc="Multiple `<tbody>` elements are valid HTML and are the correct structure for grouped rows — do not flatten groups into a single body with spacer rows. `useRowSelection` and `sortRows` compose with grouped tables: pass keys/accessors across the flattened member list.",
    tsx_header='''/**
 * DevSnips React Table — table-grouped.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on grouped rows: one `<tbody>` per department, a
 * `<th scope="rowgroup">` header row per group (uppercase label + glyph +
 * count + chevron + subtle surface — never color alone), and independent
 * collapse/expand per group via real buttons with `aria-expanded` +
 * `aria-controls`.
 */''',
    showcase=DEMO_HELPERS + '''
const GROUPS = [
  { name: "Engineering", slug: "engineering", members: [
    { name: "Alan Turing", role: "Staff Engineer", location: "London", since: "2023" },
    { name: "Grace Hopper", role: "Principal Engineer", location: "New York", since: "2022" },
    { name: "Edsger Dijkstra", role: "Engineer", location: "Amsterdam", since: "2025" },
  ] },
  { name: "Design", slug: "design", members: [
    { name: "Margaret Hamilton", role: "Product Designer", location: "Boston", since: "2024" },
    { name: "Radia Perlman", role: "Design Engineer", location: "Seattle", since: "2025" },
  ] },
  { name: "Operations", slug: "operations", members: [
    { name: "Katherine Johnson", role: "Operations Analyst", location: "Hampton", since: "2026" },
    { name: "Ada Lovelace", role: "Head of Operations", location: "London", since: "2021" },
  ] },
];

function Showcase() {
  const [collapsed, setCollapsed] = React.useState(() => new Set());
  function toggleGroup(slug) {
    setCollapsed((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug);
      else next.add(slug);
      return next;
    });
  }
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Grouped rows</p>
        <Table>
          <TableCaption>Team directory grouped by department. Groups can be collapsed independently.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Location</TableHead>
              <TableHead align="right">Since</TableHead>
            </TableRow>
          </TableHeader>
          {GROUPS.map((group) => {
            const isCollapsed = collapsed.has(group.slug);
            return (
              <TableBody key={group.slug} id={"group-" + group.slug + "-rows"}>
                <TableRow className="bg-[var(--ds-color-surface-subtle)] hover:bg-[var(--ds-color-surface-subtle)]">
                  <TableHead scope="rowgroup" colSpan={4} className="h-auto px-3 py-2">
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        aria-expanded={!isCollapsed}
                        aria-controls={"group-" + group.slug + "-rows"}
                        aria-label={(isCollapsed ? "Expand " : "Collapse ") + group.name + " group"}
                        className={BTN_ICON_GHOST + " size-6"}
                        onClick={() => toggleGroup(group.slug)}
                      >
                        <Icon name={isCollapsed ? "chevron-right" : "chevron-down"} />
                      </button>
                      <Icon name="building" className="size-3.5 text-[var(--ds-color-muted-foreground)]" />
                      <span className="text-xs font-medium uppercase tracking-[0.04em] text-[var(--ds-color-foreground)]">{group.name}</span>
                      <span className="text-xs text-[var(--ds-color-muted-foreground)]">{group.members.length} people</span>
                    </div>
                  </TableHead>
                </TableRow>
                {isCollapsed ? null : group.members.map((member) => (
                  <TableRow key={member.name}>
                    <TableCell className="font-medium">{member.name}</TableCell>
                    <TableCell>{member.role}</TableCell>
                    <TableCell>{member.location}</TableCell>
                    <TableCell align="right" numeric>{member.since}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            );
          })}
        </Table>
        <p className={NOTE}>One tbody per group, th scope="rowgroup" per group header. Collapsed groups remove their rows from the table — nothing is hidden with CSS alone.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 8. table-compact
# ===========================================================================
register(
    "table-compact",
    title="Compact Table",
    subcategory="Density",
    description="A dense table optimized for large datasets: compact density (reduced cell padding, 13px text), strong right-aligned tabular numerics, long values with predictable truncation, and full accessibility preserved.",
    tags=TAGS_BASE + ["compact", "density", "numeric", "truncation", "data-dense"],
    features=FEAT_BASE + ["compact density", "tabular numerics", "predictable truncation", "12-row dataset"],
    accessibility=["density without accessibility loss", "title preserves truncated values", "th scope=col headers"],
    interactive=False,
    related=["table", "table-sortable", "table-status"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell,
} from "./table";

<Table density="compact">
  <TableHeader>
    <TableRow>
      <TableHead>Endpoint</TableHead>
      <TableHead align="right">p95</TableHead>
      <TableHead align="right">Requests</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {endpoints.map((e) => (
      <TableRow key={e.path}>
        <TableCell>
          <span className="block max-w-[240px] truncate" title={e.path}>{e.path}</span>
        </TableCell>
        <TableCell align="right" numeric>{e.p95} ms</TableCell>
        <TableCell align="right" numeric>{e.requests.toLocaleString()}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>''',
    props_doc="\n\n".join([TABLE_PROPS, HEAD_PROPS, CELL_PROPS]),
    composition_note="Density is a single prop: `<Table density=\"compact\">` flows through context to every header and cell (8px row headers, 6px vertical cell padding, 13px text) — including `<TableSelection>` and `<TableExpand>` control sizes, so dense selectable/expandable tables stay coherent.",
    logic_doc="""Compact density is for data-dense scanning: twelve endpoint rows of trailing-24-hour performance metrics fit where six comfortable rows would. The density prop reduces padding and text size — and nothing else. Row dividers, hover affordance, header hierarchy, and focus rings are all preserved, because density must never cost accessibility.

The numeric discipline does the real work: p50 / p95 / p99 latencies, request counts, and error rates are all right-aligned with tabular figures, so columns of numbers line up and outliers pop. Long endpoint paths truncate predictably (`max-w-[240px] truncate`) with the full value preserved in the `title` attribute — truncation is a rendering choice, not data loss.""",
    keyboard_doc=KEYBOARD_BASE + """

This variant renders no interactive elements — density changes geometry, not behavior. Compact selectable or expandable tables keep the same keyboard model as their comfortable counterparts (the controls shrink, they never disappear).""",
    behavior_doc=STATES_BASE + """

- **Compact density** — 32px header rows, 6px vertical cell padding, 13px/16px text; dividers and hover states unchanged.""",
    a11y_doc=A11Y_BASE + """
- Truncated values keep their full text in the `title` attribute (and the cell content is still in the accessibility tree — `truncate` clips visually, it does not remove content).""",
    responsive_doc=RESPONSIVE_BASE + " Compact tables are the best fit for narrow viewports: at 375px the endpoint column truncates and the numeric columns stay aligned inside the container.",
    notes_doc="Choose `rows` values close to your real page size when pairing compact density with `<TableLoading>` — the skeleton then matches the loaded geometry exactly.",
    tsx_header='''/**
 * DevSnips React Table — table-compact.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on density: `<Table density="compact">` reduces cell
 * padding and text size through context — headers, cells, selection
 * checkboxes, and expand triggers all shrink together — while dividers,
 * hover states, focus rings, and semantic structure are fully preserved.
 */''',
    showcase=DEMO_HELPERS + '''
const ENDPOINTS = [
  { path: "/v1/components/search", p50: 42, p95: 118, p99: 240, requests: 1842203, errors: 0.12 },
  { path: "/v1/components", p50: 31, p95: 84, p99: 162, requests: 962410, errors: 0.04 },
  { path: "/v1/workspaces/{workspaceId}/deployments/{deploymentId}/logs/stream", p50: 88, p95: 240, p99: 512, requests: 40218, errors: 0.31 },
  { path: "/v1/tokens", p50: 24, p95: 61, p99: 118, requests: 208441, errors: 0.02 },
  { path: "/v1/usage/aggregate", p50: 120, p95: 388, p99: 940, requests: 52004, errors: 0.18 },
  { path: "/v1/members/invite", p50: 64, p95: 172, p99: 310, requests: 8412, errors: 0.44 },
  { path: "/v1/components/{id}/versions", p50: 38, p95: 96, p99: 204, requests: 318772, errors: 0.06 },
  { path: "/v1/audit-log", p50: 52, p95: 140, p99: 288, requests: 44910, errors: 0.03 },
  { path: "/v1/billing/invoices", p50: 71, p95: 204, p99: 402, requests: 12086, errors: 0.09 },
  { path: "/v1/search/reindex", p50: 240, p95: 890, p99: 2104, requests: 1204, errors: 1.02 },
  { path: "/v1/webhooks/deliveries", p50: 46, p95: 128, p99: 266, requests: 96310, errors: 0.21 },
  { path: "/v1/status", p50: 8, p95: 18, p99: 42, requests: 2408812, errors: 0.00 },
];

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Compact density</p>
        <Table density="compact">
          <TableCaption>API endpoint performance — trailing 24 hours.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Endpoint</TableHead>
              <TableHead align="right">p50</TableHead>
              <TableHead align="right">p95</TableHead>
              <TableHead align="right">p99</TableHead>
              <TableHead align="right">Requests</TableHead>
              <TableHead align="right">Errors</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {ENDPOINTS.map((endpoint) => (
              <TableRow key={endpoint.path}>
                <TableCell><span className={MONO + " block max-w-[240px] truncate"} title={endpoint.path}>{endpoint.path}</span></TableCell>
                <TableCell align="right" numeric>{endpoint.p50} ms</TableCell>
                <TableCell align="right" numeric>{endpoint.p95} ms</TableCell>
                <TableCell align="right" numeric>{endpoint.p99} ms</TableCell>
                <TableCell align="right" numeric>{endpoint.requests.toLocaleString("en-US")}</TableCell>
                <TableCell align="right" numeric>{endpoint.errors.toFixed(2)}%</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <p className={NOTE}>Density="compact": 6px cell padding, 13px text, tabular numerics. Long paths truncate with the full value in the title attribute.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 9. table-responsive
# ===========================================================================
register(
    "table-responsive",
    title="Responsive Table",
    subcategory="Responsive",
    description="A table with an intentionally designed narrow-screen presentation: a full semantic table at desktop, replaced below 640px by a card list built from the same data — not a squeezed table and not an afterthought scroll.",
    tags=TAGS_BASE + ["responsive", "mobile", "card-list", "adaptive"],
    features=FEAT_BASE + ["desktop table + mobile cards", "same data both presentations", "usable at 375px"],
    accessibility=["both presentations fully readable", "cards keep label/value structure", "no hidden data on mobile"],
    interactive=True,
    related=["table", "table-compact", "table-status"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell,
} from "./table";

{/* Desktop: the full semantic table */}
<div className="hidden sm:block">
  <Table>…all columns…</Table>
</div>

{/* Mobile: a card list built from the SAME data */}
<ul className="m-0 list-none space-y-3 p-0 sm:hidden">
  {projects.map((p) => (
    <li key={p.id} className="rounded-[var(--ds-radius-md)] border p-3">
      <header>{p.name} — {p.status}</header>
      <dl>…Owner / Updated / Budget label-value pairs…</dl>
      <footer>…View link + Edit button…</footer>
    </li>
  ))}
</ul>''',
    props_doc="\n\n".join([TABLE_PROPS, HEAD_PROPS, CELL_PROPS, ACTIONS_PROPS]),
    composition_note="The responsive pattern is a composition, not a primitive: the desktop table and the mobile card list render side by side from the same data array, each hidden at the other's breakpoint (`hidden sm:block` / `sm:hidden`). Your app owns the card mapping — the table primitives own the desktop half.",
    logic_doc="""Below 640px, four columns of project data stop being a table. The mobile presentation is a deliberately designed card list: each project becomes a bordered card with its name and status badge up top, the remaining fields as label/value pairs in a description list, and the same actions (View link, Edit button) in a footer row.

Both presentations render from the SAME data array — the cards are not a second, stale copy of the content. Nothing is hidden on mobile: every field and every action present on desktop is present in the cards, just re-laid-out for a narrow column.

This is the honest alternative to two common non-solutions: squeezing the table until cells are unreadable, or adding `overflow-x-auto` and calling the problem solved. (Horizontal scrolling IS the right answer for genuinely wide datasets — the container does it deliberately — but four columns of project metadata reads better as cards.)""",
    keyboard_doc=KEYBOARD_BASE + """

Only one presentation is visible at a time, and the hidden one is `display: none` — so keyboard users tab through exactly the controls they can see, never into the hidden presentation.""",
    behavior_doc=STATES_BASE + """

- **Mobile card** — `surface` + 1px `color.border` + `radius-md`, name + status badge header, `dl` label/value pairs, actions footer separated by a `border-subtle` rule.""",
    a11y_doc=A11Y_BASE + """
- The hidden presentation is `display: none`, so it is removed from the accessibility tree — screen-reader users get exactly one presentation.
- Cards keep a `dl` label/value structure, so "Owner: Grace Hopper" reads as a pair, not as two orphaned text runs.""",
    responsive_doc="The whole point of the variant: at 1280px and 768px the full table renders; below 640px the card list renders instead. Both are fully usable and neither produces horizontal page overflow at 375 / 768 / 1280px.",
    notes_doc="Choose the card threshold per dataset (`sm` here). Genuinely wide or numeric-heavy datasets should stay tables and use the container's deliberate horizontal scroll instead — see the compact and status variants.",
    tsx_header='''/**
 * DevSnips React Table — table-responsive.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on the narrow-screen presentation: the full semantic
 * table renders at `sm` and up, and below `sm` the SAME data renders as a
 * deliberately designed card list (name + status header, `dl` label/value
 * pairs, actions footer) — not a squeezed table, not an afterthought
 * scroll.
 */''',
    showcase=DEMO_HELPERS + '''
const PROJECTS = [
  { id: "p1", name: "Atlas Analytics", status: "Active", owner: "Grace Hopper", updated: "2026-08-21", budget: 12400 },
  { id: "p2", name: "Meridian Ops", status: "Active", owner: "Alan Turing", updated: "2026-08-19", budget: 8200 },
  { id: "p3", name: "Quiet Place", status: "Paused", owner: "Margaret Hamilton", updated: "2026-07-30", budget: 3150 },
  { id: "p4", name: "Vesper Security", status: "Archived", owner: "Katherine Johnson", updated: "2026-05-12", budget: 19980 },
];

const PROJECT_BADGE = {
  Active: "border-[color-mix(in_srgb,var(--ds-color-success)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-success)_8%,var(--ds-color-surface))] text-[var(--ds-color-success)]",
  Paused: "border-[color-mix(in_srgb,var(--ds-color-warning)_40%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-warning)_10%,var(--ds-color-surface))] text-[var(--ds-color-warning)]",
  Archived: "border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)]",
};

function ProjectBadge({ status }) {
  return (
    <span className={"inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-xs font-medium leading-4 " + PROJECT_BADGE[status]}>
      <span aria-hidden="true" className="size-1.5 rounded-full bg-current" />
      {status}
    </span>
  );
}

function Showcase() {
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Adaptive presentation</p>
        <div className="hidden sm:block">
          <Table>
            <TableCaption>Workspace projects with ownership and budget.</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Project</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Owner</TableHead>
                <TableHead>Updated</TableHead>
                <TableHead align="right">Budget</TableHead>
                <TableHead align="right"><span className="sr-only">Actions</span></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {PROJECTS.map((project) => (
                <TableRow key={project.id}>
                  <TableCell className="font-medium">{project.name}</TableCell>
                  <TableCell><ProjectBadge status={project.status} /></TableCell>
                  <TableCell>{project.owner}</TableCell>
                  <TableCell>{project.updated}</TableCell>
                  <TableCell align="right" numeric>{money(project.budget)}</TableCell>
                  <TableCell align="right">
                    <TableActions>
                      <a href={"#/projects/" + project.id} className={LINK}>View</a>
                      <button type="button" className={BTN_GHOST_SM}>Edit</button>
                    </TableActions>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <ul className="m-0 list-none space-y-3 p-0 sm:hidden">
          {PROJECTS.map((project) => (
            <li key={project.id} className="rounded-[var(--ds-radius-md)] border border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] p-3">
              <div className="flex items-start justify-between gap-3">
                <p className="m-0 text-sm font-medium leading-5 text-[var(--ds-color-foreground)]">{project.name}</p>
                <ProjectBadge status={project.status} />
              </div>
              <dl className="m-0 mt-2 space-y-1 text-[13px] leading-5">
                <div className="flex items-baseline justify-between gap-4">
                  <dt className="text-[var(--ds-color-muted-foreground)]">Owner</dt>
                  <dd className="m-0 text-[var(--ds-color-foreground)]">{project.owner}</dd>
                </div>
                <div className="flex items-baseline justify-between gap-4">
                  <dt className="text-[var(--ds-color-muted-foreground)]">Updated</dt>
                  <dd className="m-0 text-[var(--ds-color-foreground)]">{project.updated}</dd>
                </div>
                <div className="flex items-baseline justify-between gap-4">
                  <dt className="text-[var(--ds-color-muted-foreground)]">Budget</dt>
                  <dd className="m-0 tabular-nums text-[var(--ds-color-foreground)]">{money(project.budget)}</dd>
                </div>
              </dl>
              <div className="mt-3 flex items-center gap-2 border-t border-[var(--ds-color-border-subtle)] pt-2.5">
                <a href={"#/projects/" + project.id} className={LINK}>View</a>
                <button type="button" className={BTN_GHOST_SM}>Edit</button>
              </div>
            </li>
          ))}
        </ul>
        <p className={NOTE}>Resize below 640px: the table is replaced by a card list built from the same data — every field and action survives the transition.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 10. table-loading
# ===========================================================================
register(
    "table-loading",
    title="Loading Table",
    subcategory="States",
    description="A table with a real loading state: aria-busy on the table, geometry-preserving skeleton rows (aria-hidden bars + a visually hidden announcement), a reduced-motion-safe pulse, and a live transition from skeleton to data.",
    tags=TAGS_BASE + ["loading", "skeleton", "aria-busy", "reduced-motion"],
    features=FEAT_BASE + ["aria-busy", "geometry-preserving skeleton", "sr-only announcement", "reload round-trip"],
    accessibility=["aria-busy during load", "skeleton bars aria-hidden", "visually hidden loading announcement"],
    interactive=True,
    related=["table", "table-empty", "table-with-pagination"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell, TableLoading,
} from "./table";

<Table loading={loading}>
  <TableHeader>…</TableHeader>
  <TableBody>
    {loading ? (
      <TableLoading columns={4} rows={5} />
    ) : (
      reports.map((r) => <TableRow key={r.id}>…</TableRow>)
    )}
  </TableBody>
</Table>''',
    props_doc="\n\n".join([TABLE_PROPS, LOADING_PROPS, HEAD_PROPS, CELL_PROPS]),
    composition_note="`<TableLoading>` renders inside `<TableBody>` in place of the data rows, and `loading` on `<Table>` marks the whole table `aria-busy` for the duration — the header and caption stay put, so the table's structure never flashes.",
    logic_doc="""The demo's **Reload** button runs a real load cycle: the table becomes `aria-busy="true"`, the data rows are replaced by `<TableLoading>` skeleton rows, and ~1.4 seconds later the data returns. The skeleton preserves the table's approximate geometry — same four columns, five rows at near-identical heights — so the layout does not jump when data arrives.

The skeleton bars are decorative placeholders: they are `aria-hidden`, their subtle pulse is disabled under reduced motion (`motion-reduce:animate-none`), and a visually hidden row announces "Loading data" while they are shown. No decorative animated blobs, no layout-breaking transitions.""",
    keyboard_doc=KEYBOARD_BASE + """

The Reload button is disabled while loading (native `disabled`, so it leaves the tab order and cannot double-fire), and the skeleton rows contain no focusable content — keyboard users wait on a stable page instead of tabbing into placeholders.""",
    behavior_doc=STATES_BASE + """

- **Skeleton bars** — `color.muted` blocks at deterministic widths (w-3/4 / w-1/2 / w-2/3 / w-1/3 cycling per cell) with a subtle `animate-pulse` that reduced motion disables.""",
    a11y_doc=A11Y_BASE + """
- `aria-busy="true"` on the `<table>` tells assistive technology the region is being updated; the visually hidden "Loading data" row states it in words; the skeleton bars are `aria-hidden` so nothing meaningless is announced.""",
    responsive_doc=RESPONSIVE_BASE + " The skeleton mirrors the loaded table's column count and row heights at every width, so the swap causes no horizontal or vertical jump at 375 / 768 / 1280px.",
    notes_doc="Pick the skeleton `rows` count close to the expected page size (5 here, matching the five reports) — the closer the geometry, the smaller the layout shift when data arrives.",
    tsx_header='''/**
 * DevSnips React Table — table-loading.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on the loading state: `<Table loading>` marks the
 * table `aria-busy` while `<TableLoading>` renders geometry-preserving
 * skeleton rows — `aria-hidden` bars with a reduced-motion-safe pulse plus
 * a visually hidden announcement — that swap to real data without a layout
 * jump.
 */''',
    showcase=DEMO_HELPERS + '''
const REPORTS = [
  { id: "rpt_1", name: "Weekly usage digest", schedule: "Mondays 09:00", recipients: 12, status: "Active" },
  { id: "rpt_2", name: "Deploy frequency", schedule: "Daily 18:00", recipients: 6, status: "Active" },
  { id: "rpt_3", name: "Error budget burn", schedule: "Hourly", recipients: 3, status: "Active" },
  { id: "rpt_4", name: "Cost anomaly review", schedule: "Mondays 08:30", recipients: 4, status: "Paused" },
  { id: "rpt_5", name: "Quarterly access audit", schedule: "Quarterly", recipients: 2, status: "Active" },
];

function Showcase() {
  const [loading, setLoading] = React.useState(false);
  const timer = React.useRef(null);
  React.useEffect(() => () => window.clearTimeout(timer.current), []);
  function reload() {
    window.clearTimeout(timer.current);
    setLoading(true);
    timer.current = window.setTimeout(() => setLoading(false), 1400);
  }
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Loading state</p>
        <TableToolbar>
          <p className={NOTE}>{loading ? "Refreshing report data…" : "Data current as of a few seconds ago."}</p>
          <button type="button" className={BTN_OUTLINE_SM} onClick={reload} disabled={loading}>{loading ? "Loading…" : "Reload"}</button>
        </TableToolbar>
        <Table loading={loading}>
          <TableCaption>Scheduled reports for the workspace.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Report</TableHead>
              <TableHead>Schedule</TableHead>
              <TableHead align="right">Recipients</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableLoading columns={4} rows={5} />
            ) : (
              REPORTS.map((report) => (
                <TableRow key={report.id}>
                  <TableCell className="font-medium">{report.name}</TableCell>
                  <TableCell>{report.schedule}</TableCell>
                  <TableCell align="right" numeric>{report.recipients}</TableCell>
                  <TableCell>{report.status}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
        <p className={NOTE}>Reload runs a real load cycle: aria-busy + geometry-preserving skeleton rows, then data — with the pulse disabled under reduced motion.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 11. table-empty
# ===========================================================================
register(
    "table-empty",
    title="Empty Table",
    subcategory="States",
    description="A table with an honest empty state: a zero-data message with a description and a real action, rendered as one real spanning row inside the semantic table structure — never fake placeholder rows.",
    tags=TAGS_BASE + ["empty-state", "zero-data", "action"],
    features=FEAT_BASE + ["zero-data message", "real resolving action", "create/clear round-trip"],
    accessibility=["accessible empty messaging", "real action control", "no fake rows"],
    interactive=True,
    related=["table", "table-loading", "table-with-actions"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell, TableEmpty,
} from "./table";

<TableBody>
  {views.length === 0 ? (
    <TableEmpty
      colSpan={3}
      title="No saved views"
      description="Save a filtered view of your components to return to it quickly."
      action={<button type="button" onClick={createView}>Create a view</button>}
    />
  ) : (
    views.map((v) => <TableRow key={v.id}>…</TableRow>)
  )}
</TableBody>''',
    props_doc="\n\n".join([TABLE_PROPS, EMPTY_PROPS, HEAD_PROPS, CELL_PROPS, TOOLBAR_PROPS]),
    composition_note="`<TableEmpty>` renders inside `<TableBody>` when the dataset is empty — the caption and header stay, so the table keeps its structure and its column labels; only the data rows are absent.",
    logic_doc="""The empty state is honest: one real row with one spanning cell containing the title ("No saved views"), a description of why it is empty and what to do next, and a REAL action — **Create a view** genuinely adds a row to the table, and the **Clear all** toolbar button (visible once rows exist) returns the table to empty. The round-trip works in both directions.

There are no fake placeholder rows: a screen reader announcing the table finds the header and the empty message, not five rows of dashes pretending to be data.""",
    keyboard_doc=KEYBOARD_BASE + """

The empty state's action is a real button in the normal tab order; activating it creates the first row and the toolbar's Clear all button appears next in the order. Nothing appears or disappears that a keyboard user cannot reach.""",
    behavior_doc=STATES_BASE + """

- **Empty message** — centered in a `max-w-sm` column: a decorative glyph (always `aria-hidden`), a medium title, a muted description, and the action row below.""",
    a11y_doc=A11Y_BASE + """
- The empty message is plain text in the table flow — readable by everyone, no special roles required; the decorative glyph is `aria-hidden` so the message carries the meaning.""",
    responsive_doc=RESPONSIVE_BASE + " The empty message is a centered `max-w-sm` column that wraps naturally at 375px; the action row is `flex-wrap` so multiple actions never overflow.",
    notes_doc="For filter-driven empty states, the action should clear the filters (\"Clear search\") rather than create data — the same primitive covers both because the action is just a real control you supply.",
    tsx_header='''/**
 * DevSnips React Table — table-empty.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on the empty state: `<TableEmpty>` — one real
 * spanning row with a zero-data message, a description, and a real action
 * that resolves the state — inside the intact semantic table structure.
 * Never fake placeholder rows.
 */''',
    showcase=DEMO_HELPERS + '''
function Showcase() {
  const [views, setViews] = React.useState([]);
  function createView() {
    setViews((prev) => prev.concat({
      id: "view_" + (prev.length + 1),
      name: "Untitled view " + (prev.length + 1),
      filters: "Status: active",
      created: "Just now",
    }));
  }
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Empty state</p>
        <TableToolbar>
          <p className={NOTE} aria-live="polite">{views.length === 0 ? "No saved views yet." : views.length + " saved view" + (views.length === 1 ? "." : "s.")}</p>
          {views.length > 0 ? (
            <button type="button" className={BTN_GHOST_SM} onClick={() => setViews([])}>Clear all</button>
          ) : null}
        </TableToolbar>
        <Table>
          <TableCaption>Saved component-library views.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Filters</TableHead>
              <TableHead>Created</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {views.length === 0 ? (
              <TableEmpty
                colSpan={3}
                icon={<Icon name="inbox" />}
                title="No saved views"
                description="Save a filtered view of your components to return to it quickly."
                action={<button type="button" className={BTN_PRIMARY_SM} onClick={createView}>Create a view</button>}
              />
            ) : (
              views.map((view) => (
                <TableRow key={view.id}>
                  <TableCell className="font-medium">{view.name}</TableCell>
                  <TableCell>{view.filters}</TableCell>
                  <TableCell>{view.created}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
        <p className={NOTE}>The empty state is one real row — no fake placeholder rows — and its action actually creates a view. Clear all returns to empty.</p>
      </div>
    </div>
  );
}
''',
)


# ===========================================================================
# 12. table-status
# ===========================================================================
register(
    "table-status",
    title="Status Table",
    subcategory="Content",
    description="A table of realistic product data: semantic status badges (text + restrained token tints, never color alone), user cells with avatar initials, dates, right-aligned durations, rollout progress bars with real progressbar semantics, and row actions.",
    tags=TAGS_BASE + ["status", "badges", "progress", "users", "mixed-content"],
    features=FEAT_BASE + ["semantic status badges", "progressbar semantics", "user cells", "row actions"],
    accessibility=["status as text + tint (not color alone)", "role=progressbar with values", "named icon-only actions"],
    interactive=True,
    related=["table", "table-with-actions", "table-compact"],
    usage='''import Table, {
  TableHeader, TableBody, TableRow, TableHead, TableCell, TableActions,
} from "./table";

<TableCell>
  <span className={badgeClasses(job.status)}>
    <span aria-hidden="true" className="size-1.5 rounded-full bg-current" />
    {job.status}
  </span>
</TableCell>
<TableCell>
  <div role="progressbar" aria-valuenow={job.rollout} aria-valuemin={0}
       aria-valuemax={100} aria-label={`Rollout of ${job.service}`}>
    <div className={widthClass(job.rollout)} />
  </div>
</TableCell>''',
    props_doc="\n\n".join([TABLE_PROPS, ROW_PROPS, HEAD_PROPS, CELL_PROPS, ACTIONS_PROPS]),
    composition_note="Mixed cell content is just composition inside `<TableCell>`: badges, avatar + name stacks, mono timestamps, progress bars, and an actions cluster — all on the same restrained row grid, with no card-in-cell nesting.",
    logic_doc="""This variant is the reality check: six deployment jobs with genuinely mixed content — a service name, a semantic status badge, the person who deployed, a mono timestamp, a right-aligned duration, a rollout progress bar, and row actions — and the table stays a table, not an over-designed dashboard.

Status badges pair a small tinted dot with readable text on a token-derived soft tint (the same `color-mix` derivation the Alerts family uses): Running = info, Complete = success, Failed = destructive, Queued = neutral. The text carries the meaning; the tint only speeds scanning.

The rollout bar is a real `role="progressbar"` with `aria-valuenow` / `aria-valuemin` / `aria-valuemax` and an `aria-label` naming the service — the fill width is visual, the values are the content. Row actions (View link + Retry button) follow the actions variant's rules: real controls, accessible names, nothing nested.""",
    keyboard_doc=KEYBOARD_BASE + """

Row actions are real controls (a link and a button): Tab reaches them, Enter activates them, and the retry action records to the live log. Progress bars and badges are not focusable — they are content, not controls.""",
    behavior_doc=STATES_BASE + """

- **Status badge** — 1px tinted border + soft tinted surface + tinted text + dot, all derived from the semantic tokens via `color-mix`; Queued is a neutral bordered chip.
- **Progress bar** — `color.muted` track, `color.accent` fill, `radius-full`, 6px tall.
- **Avatar** — `accent-soft` circle with accent-colored initials, always `aria-hidden` (the name next to it is the content).""",
    a11y_doc=A11Y_BASE + """
- Status is text + tint, never color alone; the progress bar exposes its value through `role="progressbar"` + `aria-value*`; the avatar initials are `aria-hidden` because the adjacent name is the accessible content.""",
    responsive_doc=RESPONSIVE_BASE + " Seven columns of mixed content is a genuinely wide dataset — the deliberate `overflow-x-auto` container handles it at 375px while every column keeps its alignment and every control stays reachable.",
    notes_doc="Badge tints derive from the semantic tokens with `color-mix` (border ~35% tone + border, surface ~8% tone + surface) — no new color values are invented, and dark mode stays in sync for free.",
    tsx_header='''/**
 * DevSnips React Table — table-status.
 *
 * The shared compound core (identical to the reference `table` variant) with
 * the showcase focused on realistic mixed content: semantic status badges
 * (text + token-derived tints, never color alone), user cells with avatar
 * initials, mono timestamps, right-aligned tabular durations, rollout
 * progress bars with real `role="progressbar"` semantics, and row actions —
 * product data without the over-designed dashboard.
 */''',
    showcase=DEMO_HELPERS + '''
const JOBS = [
  { id: "job_1", service: "api-gateway", status: "Running", user: { name: "Grace Hopper", initials: "GH" }, started: "2026-08-22 09:14", durationSeconds: 212, rollout: 45 },
  { id: "job_2", service: "billing-service", status: "Complete", user: { name: "Alan Turing", initials: "AT" }, started: "2026-08-22 08:52", durationSeconds: 96, rollout: 100 },
  { id: "job_3", service: "edge-cache", status: "Failed", user: { name: "Margaret Hamilton", initials: "MH" }, started: "2026-08-22 08:31", durationSeconds: 388, rollout: 62 },
  { id: "job_4", service: "auth-service", status: "Queued", user: { name: "Katherine Johnson", initials: "KJ" }, started: "2026-08-22 09:20", durationSeconds: 0, rollout: 0 },
  { id: "job_5", service: "data-pipeline", status: "Running", user: { name: "Ada Lovelace", initials: "AL" }, started: "2026-08-22 09:02", durationSeconds: 154, rollout: 78 },
  { id: "job_6", service: "docs-site", status: "Complete", user: { name: "Grace Hopper", initials: "GH" }, started: "2026-08-22 07:48", durationSeconds: 34, rollout: 100 },
];

const STATUS_BADGE = {
  Running: "border-[color-mix(in_srgb,var(--ds-color-info)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-info)_8%,var(--ds-color-surface))] text-[var(--ds-color-info)]",
  Complete: "border-[color-mix(in_srgb,var(--ds-color-success)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-success)_8%,var(--ds-color-surface))] text-[var(--ds-color-success)]",
  Failed: "border-[color-mix(in_srgb,var(--ds-color-destructive)_35%,var(--ds-color-border))] bg-[color-mix(in_srgb,var(--ds-color-destructive)_7%,var(--ds-color-surface))] text-[var(--ds-color-destructive)]",
  Queued: "border-[var(--ds-color-border)] bg-[var(--ds-color-surface)] text-[var(--ds-color-muted-foreground)]",
};

const ROLLOUT_WIDTH = { 0: "w-0", 45: "w-[45%]", 62: "w-[62%]", 78: "w-[78%]", 100: "w-full" };

function formatDuration(seconds) {
  if (seconds === 0) return "—";
  const minutes = Math.floor(seconds / 60);
  const rest = seconds % 60;
  return minutes > 0 ? minutes + "m " + rest + "s" : rest + "s";
}

function Showcase() {
  const [log, setLog] = React.useState("No actions yet.");
  return (
    <div className="w-full space-y-8">
      <div className="space-y-2">
        <p className={LABEL}>Realistic product data</p>
        <Table>
          <TableCaption>Deployment jobs for the production environment.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead>Service</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Deployed by</TableHead>
              <TableHead>Started</TableHead>
              <TableHead align="right">Duration</TableHead>
              <TableHead>Rollout</TableHead>
              <TableHead align="right"><span className="sr-only">Actions</span></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {JOBS.map((job) => (
              <TableRow key={job.id}>
                <TableCell className="font-medium">{job.service}</TableCell>
                <TableCell>
                  <span className={"inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-xs font-medium leading-4 " + STATUS_BADGE[job.status]}>
                    <span aria-hidden="true" className="size-1.5 rounded-full bg-current" />
                    {job.status}
                  </span>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span aria-hidden="true" className="inline-flex size-6 shrink-0 items-center justify-center rounded-full bg-[var(--ds-color-accent-soft)] text-[10px] font-medium text-[var(--ds-color-accent)]">{job.user.initials}</span>
                    <span>{job.user.name}</span>
                  </div>
                </TableCell>
                <TableCell><span className={MONO}>{job.started}</span></TableCell>
                <TableCell align="right" numeric>{formatDuration(job.durationSeconds)}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <div role="progressbar" aria-valuenow={job.rollout} aria-valuemin={0} aria-valuemax={100} aria-label={"Rollout of " + job.service} className="h-1.5 w-20 overflow-hidden rounded-full bg-[var(--ds-color-muted)]">
                      <div className={"h-full rounded-full bg-[var(--ds-color-accent)] " + ROLLOUT_WIDTH[job.rollout]} />
                    </div>
                    <span className="text-[13px] tabular-nums text-[var(--ds-color-muted-foreground)]">{job.rollout}%</span>
                  </div>
                </TableCell>
                <TableCell align="right">
                  <TableActions>
                    <a href={"#/jobs/" + job.id} className={LINK}>View</a>
                    <button type="button" aria-label={"Retry " + job.service} className={BTN_ICON_GHOST} onClick={() => setLog("Retried " + job.service + ".")}>
                      <Icon name="refresh" />
                    </button>
                  </TableActions>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <p className={NOTE} aria-live="polite">Last action: {log}</p>
      </div>
    </div>
  );
}
''',
)
