# Table

## Overview

The reference table: a clean semantic data table (real <table>, <caption>, <thead>, <tbody>, <tfoot>, <th>, <td>) with aligned text and numeric columns, a totals footer, and the full compound region set every other variant in the family is built from.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Table, {
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
</Table>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Table, {
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
</Table>
```

## Props

### `<Table>`

| Name | Type | Default | Description |
|---|---|---|---|
| `density` | `"default" \| "compact"` | `"default"` | Cell/header density shared by every region primitive via context. |
| `loading` | `boolean` | `false` | Sets `aria-busy="true"` on the `<table>` (pair with `<TableLoading>`). |
| `containerClassName` | `string` | — | Extra classes on the bordered `overflow-x-auto` scroll container. |
| `className` | `string` | — | Extra classes on the `<table>` itself. |
| `children` | `ReactNode` | — | `TableCaption`, `TableHeader`, `TableBody`, `TableFooter` compositions. |

Every other attribute of a plain `<table>` (`id`, `aria-*`, `data-*`) is forwarded.

### `<TableCaption>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the caption. |
| `children` | `ReactNode` | — | The dataset's name/description. |

A real `<caption>` rendered above the table — the accessible name of the dataset.

### `<TableHeader>` / `<TableBody>` / `<TableFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the section. |
| `children` | `ReactNode` | — | `TableRow` compositions. |

Real `<thead>` / `<tbody>` / `<tfoot>` elements. A grouped table renders one `<TableBody>` per group (multiple `<tbody>` elements are valid HTML).

### `<TableRow>`

| Name | Type | Default | Description |
|---|---|---|---|
| `selected` | `boolean` | `false` | `aria-selected="true"` + accent-tinted surface. |
| `disabled` | `boolean` | `false` | `aria-disabled="true"` + reduced opacity, no hover. Disable the row's controls too. |
| `className` | `string` | — | Extra classes on the row. |
| `children` | `ReactNode` | — | `TableHead` / `TableCell` children. |

A real `<tr>`. Rows are never fake buttons — interactive content lives in real controls inside the cells.

### `<TableHead>`

| Name | Type | Default | Description |
|---|---|---|---|
| `align` | `"left" \| "center" \| "right"` | `"left"` | Header alignment (match the column's cells). |
| `sortable` | `boolean` | `false` | Render the label as a real sort `<button>` and manage `aria-sort`. |
| `sortDirection` | `"asc" \| "desc" \| null` | `null` | Current direction; `null` = sortable but unsorted (`aria-sort="none"`). |
| `onSort` | `() => void` | — | Called when the sort button is activated. |
| `scope` | `string` | `"col"` | Header scope; use `"rowgroup"` for group header rows. |
| `className` | `string` | — | Extra classes on the `<th>`. |
| `children` | `ReactNode` | — | Header content. |

A real `<th scope="col">`; `colSpan` and the other native `<th>` attributes forward.

### `<TableCell>`

| Name | Type | Default | Description |
|---|---|---|---|
| `align` | `"left" \| "center" \| "right"` | `"left"` | Cell alignment (numeric columns: `right`). |
| `numeric` | `boolean` | `false` | Tabular figures (`tabular-nums`) for numeric content. |
| `className` | `string` | — | Extra classes on the `<td>`. |
| `children` | `ReactNode` | — | Cell content — text, links, badges, controls. |

A real `<td>`; `colSpan` / `rowSpan` / `headers` forward natively.

## Compound components

The family is a compound component over real table semantics. Compose only the regions a table needs:

```tsx
<Table>
  <TableCaption />
  <TableHeader>
    <TableRow>
      <TableHead />
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell />
    </TableRow>
  </TableBody>
  <TableFooter />
</Table>
```

| Primitive | Element | Purpose |
|---|---|---|
| `<Table>` | bordered container + `<table>` | Root; provides the `density` context and the deliberate `overflow-x-auto` scroll region; `loading` sets `aria-busy`. |
| `<TableCaption>` | `<caption>` | The table's accessible name/description, rendered above the table. |
| `<TableHeader>` | `<thead>` | Column-header section (subtle surface, bottom rule). |
| `<TableBody>` | `<tbody>` | Data rows; the last row's divider is removed. |
| `<TableFooter>` | `<tfoot>` | Totals/summaries (subtle surface, top rule). |
| `<TableRow>` | `<tr>` | Hover affordance; `selected` (`aria-selected` + accent tint) and `disabled` (`aria-disabled` + reduced opacity) states. |
| `<TableHead>` | `<th scope="col">` | Column header; `sortable` renders a real sort button and manages `aria-sort`. |
| `<TableCell>` | `<td>` | Data cell; `align` + `numeric` (tabular figures); `colSpan` forwards natively. |
| `<TableEmpty>` | `<tr>` + spanning `<td>` | Honest zero-data state (title, description, optional real action). |
| `<TableLoading>` | skeleton `<tr>`s | Geometry-preserving skeleton rows (pair with `<Table loading>`). |
| `<TableActions>` | `<div>` in a cell | End-aligned cluster of real controls. |
| `<TableToolbar>` | `<div>` above the table | Selection counts, filters, primary actions (layout only). |
| `<TablePagination>` | `<nav aria-label>` | Self-contained pagination bar (status, windowed pages, Previous/Next, optional page-size select). |
| `<TableSelection>` | native `<input type="checkbox">` | Row / select-all selection with a true `.indeterminate` tri-state. |
| `<TableExpand>` | `<button>` | Row expand/collapse trigger (`aria-expanded` / `aria-controls`). |

Every region primitive throws a descriptive error when rendered outside `<Table>` (except `TableToolbar` and `TablePagination`, which live next to the table).

The reference composes every structural region — caption, header, body, and a totals footer — so it doubles as the family's syntax reference. The footer is a real `<tfoot>`: it is announced as part of the table and stays at the bottom regardless of row count.

## Data modeling

Tables are data-driven but unopinionated about your data shape. The conventions that keep them sound:

- **Row keys** — give every `<TableRow>` a stable, unique React `key` (an id from your data, never the array index of a sorted/filtered list).
- **Column definitions** — for data-driven tables, describe columns once (`key`, `label`, `accessor`, optional `align` / `numeric` / `format`) and map them to `<TableHead>` / `<TableCell>`; the sortable variant shows the pattern.
- **Custom cell rendering** — cells are just `<td>`s: render links, badges, avatars, progress bars, or controls inside `<TableCell>`; use `<TableActions>` for the trailing actions column.
- **Custom header rendering** — `<TableHead>` accepts any `children`; pass `sortable` + `sortDirection` + `onSort` only for columns that genuinely sort.
- **Alignment** — text columns stay `left`; numeric columns use `align="right"` + `numeric` (tabular figures) on BOTH the header and the cells so digits line up.
- **Column sizing** — the table is `w-full` with automatic layout; constrain a column with a `max-w-*` + `truncate` class on its cells (keep the full value available via `title` or an expansion panel), or size the whole table with `containerClassName`.

## Sorting

Sorting is primitive-driven and real — there is no fake "sorted-looking" state:

1. Mark the column `<TableHead sortable sortDirection={direction} onSort={cycle}>`. The head renders a visible `<button type="button">` (click, Enter, and Space all work) and the `<th>` carries `aria-sort` — `"ascending"` / `"descending"` on the active column, `"none"` on sortable-but-inactive columns.
2. Track `{ key, direction }` in state. The recommended cycle is **ascending → descending → unsorted** (unsorted restores the original data order — a real reset, not a third sort).
3. Order the data with the typed `sortRows(rows, accessor, direction)` helper: it returns a sorted COPY (strings via `localeCompare`, numbers numerically) and immutably leaves the source array alone.

Only one column sorts at a time in this system — that keeps `aria-sort` honest (exactly one column announces a direction) and the model understandable. Multi-column sorting is deliberately out of scope (see Limitations).

## Selection

Selection uses REAL native checkboxes — never div fakes:

- Each selectable row renders `<TableSelection checked={...} onCheckedChange={...} label="Select <row name>" />` in its first cell; the header renders a `<TableSelection>` for select-all.
- The typed `useRowSelection(selectableKeys)` hook tracks the selected key set and derives `count`, `allSelected`, and `someSelected`. Pass `allSelected` to the header checkbox's `checked` and `someSelected` to its `indeterminate` — the tri-state is the true `.indeterminate` IDL property set imperatively on the DOM node (no HTML attribute exists), so it renders a dash distinct from the check mark.
- Disabled rows keep their checkbox `disabled`, are excluded from the selectable key list, and therefore never count toward select-all.
- Selected rows get `selected` on `<TableRow>`: `aria-selected="true"` plus an accent-tinted surface derived from tokens via `color-mix` — strong, and never color alone (the checkbox state carries the same information).

## Expansion

Row expansion uses a real toggle button and a real content row:

- The trigger is `<TableExpand expanded={...} controls={panelId} label="details for <row>" onClick={toggle} />` — a `<button type="button">` with `aria-expanded` and `aria-controls`, operable from the keyboard.
- The expanded content is a real `<TableRow>` whose `<TableCell colSpan={columnCount} id={panelId}>` holds the panel (a description list, text, or any composition — avoid nested tables unless the data genuinely is tabular).
- Expansion toggles instantly (no height animation), so there is no layout thrash and nothing is ever hidden from keyboard users in a half-open state; focus stays on the trigger when a row opens or closes.
- Track the open rows as a `Set` of keys — multiple rows can be open at once unless you deliberately close siblings.

## Pagination

`<TablePagination>` is a self-contained pagination bar that follows the DevSnips Pagination family's semantics. It reports and changes the current page; the parent slices the dataset:

```tsx
const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));
const safePage = clampPage(page, totalPages);
const visible = rows.slice((safePage - 1) * pageSize, safePage * pageSize);

<TablePagination
  page={safePage}
  onPageChange={setPage}
  totalItems={rows.length}
  pageSize={pageSize}
  pageSizeOptions={[8, 12, 20]}
  onPageSizeChange={(size) => { setPageSize(size); setPage(1); }}
/>
```

- Changing the page changes the visible rows — there is no decorative pagination footer.
- Previous/Next disable natively at the boundaries; the current page carries `aria-current="page"`; the page list windows with non-interactive ellipses for large counts.
- Every page value is clamped with the exported `clampPage`, so an empty page cannot occur through invalid state (for example after the dataset shrinks or the page size grows — reset to page 1 on page-size change, as above).
- The "Showing X–Y of Z" status is an `aria-live="polite"` region so page changes are announced.

## Behavior

The reference table is static: no sorting, selection, or pagination — just the structural regions and intentional alignment. Invoice ids render in the mono font, amounts and balances are right-aligned with tabular figures (`align="right"` + `numeric`), and the footer computes its totals from the same data array, so the summary can never disagree with the rows.

Alignment is the design decision that matters here: text is left-aligned, numeric values are right-aligned so digits line up for comparison, and the header alignment matches its column's cells.

## Responsive behavior

The table fills its container (`w-full`) inside a deliberate `overflow-x-auto` scroll region: when a dataset is genuinely wider than the viewport, the table scrolls horizontally inside its bordered container — the page itself never gains a scrollbar, and the caption, header rule, and row geometry stay intact. Cell text wraps by default; numeric columns use tabular figures so values stay comparable at any width. No horizontal page overflow at 375 / 768 / 1280px. The four-column invoice layout fits 375px without scrolling; wider datasets scroll inside the container, never the page.

## Keyboard interaction

Every interactive element in the table is a real native control, so the keyboard model is the browser's: Tab / Shift+Tab moves through sort buttons, checkboxes, expand triggers, links, action buttons, and pagination controls; Enter/Space activates them; and a `focus-visible` ring (2px, `color.focus-ring` token) marks keyboard focus. Rows are never fake buttons, so Tab never stops on a row itself — only on the operable controls inside it.

The reference table renders no interactive elements, so there is nothing extra to tab through — keyboard users read the table with their screen reader's table navigation (caption + `th scope="col"` headers make that navigation meaningful).

## Accessibility

- Real table semantics throughout: `<table>` / `<caption>` / `<thead>` / `<tbody>` / `<tfoot>` / `<tr>` / `<th scope="col">` / `<td>` — never a grid of divs, and no `role="grid"` re-declaration (native semantics are the correct semantics here).
- The `<TableCaption>` names the dataset for assistive technology; prefer it over an off-table heading.
- Controls are real native elements with accessible names: sort buttons announce their label, checkboxes carry `aria-label`, the expand trigger carries `aria-expanded` + `aria-controls`, and pagination controls carry `aria-current` / native `disabled`.
- State is never communicated by color alone: selection pairs its tinted surface with the checkbox's checked state and `aria-selected`; status badges pair a tinted dot with readable text; the indeterminate select-all state is the true `.indeterminate` IDL property.

## States

- **Header / footer** — `surface-subtle` with 1px `color.border` rules and `label-sm` type (12px, medium, muted).
- **Row** — `border-subtle` divider, a restrained `surface-hover` shift on hover, and a `transition-colors` that is disabled under reduced motion.
- **Selected row** — `aria-selected` + an accent-tinted surface derived from the accent token via `color-mix` (8% rest, 12% hover).
- **Disabled row** — `aria-disabled`, 60% opacity, no hover affordance; its controls are natively disabled.
- **Controls** — muted-at-rest with a foreground hover shift, a `focus-visible` ring, and native `disabled` styling (50% opacity, no pointer events).

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`); the selected-row tint derives from the accent token with `color-mix`, so no component-specific color values are invented. Define the tokens once in your theme — no component-specific CSS file is required.

## Design tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This table follows the token system's Table rules: compact-or-default density, clear header styling (`surface-subtle` header/footer, `label-sm` header type), 1px `color.border` / `color.border-subtle` rules instead of shadows, `surface-hover` row affordance, an accent-tinted selected state, semantic status colors for badges, and the `color.focus-ring` token on every control.

## Loading and empty states

**Loading.** Set `loading` on `<Table>` (adds `aria-busy="true"`) and render `<TableLoading columns={n} rows={m} />` inside `<TableBody>`. The skeleton rows keep the table's approximate geometry (same column count, near-identical row heights) to minimize layout shift; the bars are `aria-hidden` decorative placeholders with a subtle pulse that is disabled under reduced motion, and a visually hidden row announces "Loading data".

**Empty.** Render `<TableEmpty colSpan={n} title="…" description="…" action={…} />` inside `<TableBody>` when the dataset is empty. It is one real row with one spanning cell — never fake placeholder rows — and the optional action must be a real control that resolves the state (create, clear filters, retry).

## Notes

Give every row a stable React `key` from the data (the invoice id here). The footer totals are computed from the same array as the rows — derive summaries, never hardcode them.

## Limitations

- **Single-column sorting only.** `aria-sort` is only honest when exactly one column is sorted; multi-column sort is deliberately not built in.
- **No virtualized scrolling.** The table renders every row it is given; for very large datasets paginate (see `<TablePagination>`) or window the data yourself.
- **No column resizing or reordering.** Column sizing is class-based (`max-w-*` + `truncate`, `containerClassName`).
- **No ARIA grid mode.** The family intentionally keeps native table semantics; spreadsheet-style cell-to-cell arrow-key navigation would require `role="grid"` and is out of scope.
- **Sticky headers/columns are not built in.** The scroll container is `overflow-x-auto`; sticky positioning can be layered on with classes but is not part of the shipped core.
- **The responsive card presentation is a composition pattern**, not a primitive: the table-responsive variant shows how to render the same data as a card list below `sm` — your app owns that mapping.
