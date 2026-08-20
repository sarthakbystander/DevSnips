# Pagination with Ellipsis

Windowed page navigation for large datasets: first/last pages plus a sibling window around the current page, with hidden ranges collapsed to a non-interactive ellipsis.

## Usage

```tsx
import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationPages,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-with-ellipsis";

const [page, setPage] = useState(25);

<Pagination page={page} totalPages={50} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationPages />
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Wider window:
<PaginationPages siblingCount={2} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationPages,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-with-ellipsis";

const [page, setPage] = useState(25);

<Pagination page={page} totalPages={50} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationPages />
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Wider window:
<PaginationPages siblingCount={2} />
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

### `getPaginationRange(currentPage, totalPages, siblingCount?)`

Returns an array of 1-based page numbers and `"ellipsis"` markers. Always includes the first page, the last page, and `siblingCount` pages on each side of the current page; hidden ranges collapse to a single marker. When every page fits (`totalPages <= 2 * siblingCount + 5`) all pages are returned — no marker is produced.

### `<PaginationPages>`

| Name | Type | Default | Description |
|---|---|---|---|
| `siblingCount` | `number` | `1` | Pages shown on each side of the current page. |

Renders the computed range as `<PaginationItem>` children of `<PaginationContent>`: numbered `PaginationLink` controls plus `PaginationEllipsis` markers.

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

`PaginationPages` renders the computed range between the steppers. The ellipsis variant never renders more than `2 * siblingCount + 5` page positions, no matter how large `totalPages` grows.

## Pagination Logic

The root `<Pagination>` owns the current page and clamps every navigation target into `1 … totalPages`, so out-of-range requests are impossible. Both modes are supported:

- **Controlled** — pass `page` + `onPageChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultPage`; the component owns the state.

Controls pick their element from how navigation is driven: with `buildHref` (or an explicit `href`) they render real `<a href>` anchors and the browser performs normal navigation; without URLs they render `<button type="button">` and call `setPage`. `PaginationPrevious` is disabled when the current page is 1, `PaginationNext` when it is `totalPages`.

`getPaginationRange(currentPage, totalPages, siblingCount = 1)` produces the visible range:

- Page 1 of 50 → `1 2 … 50`
- Page 3 of 50 → `1 2 3 4 … 50`
- Page 25 of 50 → `1 … 24 25 26 … 50`
- Page 50 of 50 → `1 … 49 50`
- 5 total pages → `1 2 3 4 5` (everything fits, so no ellipsis)

An ellipsis is only emitted when a range is actually hidden — there is never a marker between adjacent pages, and never more than two markers.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Tab` / `Shift+Tab` | Move focus through the page controls |
| `Enter` / `Space` | Activate the focused button (state-driven pagination) |
| `Enter` | Follow the focused link (URL-based pagination) |

Controls are native anchors or buttons, so they keep their expected browser behavior. The ellipsis is not focusable — it is informational only.

## Accessibility

The structure follows the W3C pagination navigation pattern: a `<nav aria-label="Pagination">` landmark containing a list of controls.

- State-driven controls are native `<button type="button">` elements; URL-based controls are real `<a href>` anchors. No `div` click handlers.
- The current page carries `aria-current="page"` and its accessible name is "Page N"; other pages are named "Go to page N".
- Previous / Next keep visible text labels — the chevron icons are `aria-hidden` decoration.
- Disabled controls are non-interactive spans with `aria-disabled="true"`: not focusable, not activatable.
- The ellipsis glyph is `aria-hidden` with a screen-reader-only "More pages" text; it is never a control.

The ellipsis is informational, not a control: the glyph is `aria-hidden` and a screen-reader-only "More pages" text carries the meaning. It is not focusable and cannot be activated — hidden pages are reached through the first/last window and the steppers.

## States

- **Page control (idle)** — muted foreground; hover shifts to a subtle surface with foreground text.
- **Current page** — bordered surface with a hairline border, foreground text, and `aria-current="page"`. Distinguished by border, surface, and weight together — never by color alone.
- **Previous / Next** — same idle treatment with a directional chevron; the visible text label carries the accessible name.
- **Disabled** — non-interactive `aria-disabled` span at 50% opacity; removed from the tab order.
- **Focus-visible** — `--ds-color-focus-ring` outline on every interactive control in both themes.

## Responsive Behavior

Windowing is the mobile strategy: at any width the control row stays short (7 positions at `siblingCount={1}`), and `flex-wrap` covers the rare narrow overflow. Reduce `siblingCount` rather than shrinking controls on very dense screens.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This pagination variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

Use for large datasets: file managers, log viewers, admin tables, search results. The algorithm handles first/last/current pages, small counts, and both boundaries without special cases in your code.
