# Pagination with Page Size

Pagination combined with a Rows per page selector: a labeled native select beside the nav landmark that changes the page size and resets the current page.

## Usage

```tsx
import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationPageSize,
} from "./pagination-with-page-size";

const [page, setPage] = useState(1);
const [pageSize, setPageSize] = useState(20);
const totalPages = Math.ceil(totalItems / pageSize);

<div className="flex flex-wrap items-center justify-between gap-4">
  <PaginationPageSize
    value={pageSize}
    onValueChange={(size) => { setPageSize(size); setPage(1); }}
    options={[10, 20, 50]}
  />
  <Pagination page={page} totalPages={totalPages} onPageChange={setPage}>
    <PaginationContent>
      <PaginationItem><PaginationPrevious /></PaginationItem>
      {Array.from({ length: totalPages }, (_, i) => (
        <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
      ))}
      <PaginationItem><PaginationNext /></PaginationItem>
    </PaginationContent>
  </Pagination>
</div>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationPageSize,
} from "./pagination-with-page-size";

const [page, setPage] = useState(1);
const [pageSize, setPageSize] = useState(20);
const totalPages = Math.ceil(totalItems / pageSize);

<div className="flex flex-wrap items-center justify-between gap-4">
  <PaginationPageSize
    value={pageSize}
    onValueChange={(size) => { setPageSize(size); setPage(1); }}
    options={[10, 20, 50]}
  />
  <Pagination page={page} totalPages={totalPages} onPageChange={setPage}>
    <PaginationContent>
      <PaginationItem><PaginationPrevious /></PaginationItem>
      {Array.from({ length: totalPages }, (_, i) => (
        <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
      ))}
      <PaginationItem><PaginationNext /></PaginationItem>
    </PaginationContent>
  </Pagination>
</div>
```

## Props

### `<Pagination>`

| Name | Type | Default | Description |
|---|---|---|---|
| `page` | `number` | — | Current page, 1-based (controlled). |
| `defaultPage` | `number` | `1` | Initial page, 1-based (uncontrolled). |
| `totalPages` | `number` (required) | — | Total number of pages. |
| `onPageChange` | `(page: number) => void` | — | Called with the next 1-based page. |
| `buildHref` | `(page: number) => string` | — | Builds a URL per page; controls render as real anchors. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Control density (32px / 36px / 44px). |
| `disabled` | `boolean` | `false` | Disable every control in the navigation. |
| `label` | `string` | `"Pagination"` | Accessible label for the `<nav>` landmark. |
| `className` | `string` | — | Extra classes on the `<nav>`. |
| `children` | `ReactNode` | — | `PaginationContent` composition. |

### `<PaginationContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<ul>`. |
| `children` | `ReactNode` | — | `PaginationItem` elements. |

### `<PaginationItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<li>`. |
| `children` | `ReactNode` | — | Usually one page control or an ellipsis. |

### `<PaginationLink>`

| Name | Type | Default | Description |
|---|---|---|---|
| `page` | `number` (required) | — | 1-based page number this control navigates to. |
| `href` | `string` | — | Explicit URL (overrides `buildHref`); renders a real anchor. |
| `disabled` | `boolean` | `false` | Disable this page control (non-interactive span). |
| `aria-label` | `string` | `"Go to page N"` / `"Page N"` | Accessible name override. |
| `className` | `string` | — | Extra classes on the control. |
| `children` | `ReactNode` | the page number | Visible content. |

### `<PaginationPrevious>` / `<PaginationNext>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | — | Explicit URL for the target page (overrides `buildHref`). |
| `label` | `string` | `"Previous"` / `"Next"` | Visible label (also the accessible name). |
| `className` | `string` | — | Extra classes on the control. |

Previous disables automatically on the first page; Next on the last page.

### `<PaginationEllipsis>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the marker. |

Informational only: an `aria-hidden` "…" glyph plus a screen-reader-only "More pages" text. Never a button.

### `<PaginationPageSize>`

| Name | Type | Default | Description |
|---|---|---|---|
| `value` | `number` | — | Selected page size (controlled). |
| `defaultValue` | `number` | first option | Initial page size (uncontrolled). |
| `onValueChange` | `(pageSize: number) => void` | — | Called with the selected page size. |
| `options` | `number[]` | `[10, 20, 50, 100]` | Selectable page sizes. |
| `label` | `string` | `"Rows per page"` | Visible label for the select. |
| `id` | `string` | — | Explicit id for the label/select association. |
| `className` | `string` | — | Extra classes on the wrapper. |

A real, explicitly labeled native `<select>` — rendered OUTSIDE the `<nav>` landmark, because choosing a page size is a filter, not navigation.

## Composition

Pagination is a compound component. Seven primitives compose the pattern:

```tsx
<Pagination totalPages={5} page={page} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationLink page={1} /></PaginationItem>
    <PaginationItem><PaginationLink page={2} /></PaginationItem>
    <PaginationItem><PaginationLink page={3} /></PaginationItem>
    <PaginationItem><PaginationEllipsis /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>
```

- `Pagination` — the root `<nav aria-label="Pagination">` landmark. Owns the current page (controlled via `page` + `onPageChange`, or uncontrolled via `defaultPage`) and provides it — plus `totalPages`, `size`, `disabled`, and `buildHref` — to every child through context.
- `PaginationContent` — the list of controls (`<ul>`). Wraps onto multiple lines instead of scrolling horizontally.
- `PaginationItem` — one position in the control list (`<li>`).
- `PaginationLink` — a numbered page control. Renders a real `<a href>` when `buildHref` (or an explicit `href`) is set, otherwise a `<button type="button">`. The current page carries `aria-current="page"`.
- `PaginationPrevious` / `PaginationNext` — step one page back / forward. Disabled automatically at the first / last page.
- `PaginationEllipsis` — an informational marker for a hidden range of pages (`aria-hidden` glyph + screen-reader-only "More pages"). Not a button.

The page-size selector is a sibling of `<Pagination>`, never a child: render both inside a plain flex row. `PaginationPageSize` is styled with the same input tokens as the DevSnips Select family, so the two controls read as one system without sharing semantics.

## Pagination Logic

The root `<Pagination>` owns the current page and clamps every navigation target into `1 … totalPages`, so out-of-range requests are impossible. Both modes are supported:

- **Controlled** — pass `page` + `onPageChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultPage`; the component owns the state.

Controls pick their element from how navigation is driven: with `buildHref` (or an explicit `href`) they render real `<a href>` anchors and the browser performs normal navigation; without URLs they render `<button type="button">` and call `setPage`. `PaginationPrevious` is disabled when the current page is 1, `PaginationNext` when it is `totalPages`.

Changing the page size changes `totalPages`, so always reset to page 1 in `onValueChange` (as in the example above) — otherwise the current page can point past the end of the resized list. Recompute `totalPages` as `Math.ceil(totalItems / pageSize)` and pass it to `<Pagination>`; the clamp inside the root guards any remaining edge.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Tab` / `Shift+Tab` | Move focus through the page-size select and the page controls |
| `Enter` / `Space` | Activate the focused button (state-driven pagination) |
| `ArrowUp` / `ArrowDown` (select focused) | Move through page-size options (native behavior) |

The page-size control is a native `<select>`, so it keeps its full native keyboard and screen-reader behavior.

## Accessibility

The structure follows the W3C pagination navigation pattern: a `<nav aria-label="Pagination">` landmark containing a list of controls.

- State-driven controls are native `<button type="button">` elements; URL-based controls are real `<a href>` anchors. No `div` click handlers.
- The current page carries `aria-current="page"` and its accessible name is "Page N"; other pages are named "Go to page N".
- Previous / Next keep visible text labels — the chevron icons are `aria-hidden` decoration.
- Disabled controls are non-interactive spans with `aria-disabled="true"`: not focusable, not activatable.
- The ellipsis glyph is `aria-hidden` with a screen-reader-only "More pages" text; it is never a control.

The select has a persistent visible `<label>` ("Rows per page") — not a placeholder — and lives outside the `<nav aria-label="Pagination">` landmark, so screen-reader users hear a filter control followed by a navigation landmark rather than a mixed-up widget.

## States

- **Page control (idle)** — muted foreground; hover shifts to a subtle surface with foreground text.
- **Current page** — bordered surface with a hairline border, foreground text, and `aria-current="page"`. Distinguished by border, surface, and weight together — never by color alone.
- **Previous / Next** — same idle treatment with a directional chevron; the visible text label carries the accessible name.
- **Disabled** — non-interactive `aria-disabled` span at 50% opacity; removed from the tab order.
- **Focus-visible** — `--ds-color-focus-ring` outline on every interactive control in both themes.

## Responsive Behavior

Place both controls in a `flex flex-wrap items-center justify-between` row: at 375px the select and the nav stack onto separate lines at full size. Never shrink the select below the input height to keep them on one line.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This pagination variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

Use for data tables and admin lists where the user controls density. Pair with the ellipsis variant when large page sizes can produce many pages.
