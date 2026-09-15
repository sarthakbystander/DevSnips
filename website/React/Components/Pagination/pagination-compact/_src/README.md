# Compact Pagination

Compact pagination (32px controls, size=sm) for dense interfaces such as table footers and admin lists — same system, smaller density.

## Usage

```tsx
import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-compact";

const [page, setPage] = useState(1);

// size="sm" is the default in this variant:
<Pagination page={page} totalPages={6} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    {Array.from({ length: 6 }, (_, i) => (
      <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
    ))}
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>
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
} from "./pagination-compact";

const [page, setPage] = useState(1);

// size="sm" is the default in this variant:
<Pagination page={page} totalPages={6} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    {Array.from({ length: 6 }, (_, i) => (
      <PaginationItem key={i + 1}><PaginationLink page={i + 1} /></PaginationItem>
    ))}
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>
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

Identical primitives to the reference — the only change is the default `size` of `"sm"` (32px controls, 13px labels). Pass `size="md"` to opt back into the default density.

## Pagination Logic

The root `<Pagination>` owns the current page and clamps every navigation target into `1 … totalPages`, so out-of-range requests are impossible. Both modes are supported:

- **Controlled** — pass `page` + `onPageChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultPage`; the component owns the state.

Controls pick their element from how navigation is driven: with `buildHref` (or an explicit `href`) they render real `<a href>` anchors and the browser performs normal navigation; without URLs they render `<button type="button">` and call `setPage`. `PaginationPrevious` is disabled when the current page is 1, `PaginationNext` when it is `totalPages`.

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

Compact does not mean cramped: controls stay 32px tall with full `focus-visible` rings and unchanged accessible names. Touch targets remain usable; nothing is shrunk below the small density of the DevSnips Buttons/Inputs families.

## States

- **Page control (idle)** — muted foreground; hover shifts to a subtle surface with foreground text.
- **Current page** — bordered surface with a hairline border, foreground text, and `aria-current="page"`. Distinguished by border, surface, and weight together — never by color alone.
- **Previous / Next** — same idle treatment with a directional chevron; the visible text label carries the accessible name.
- **Disabled** — non-interactive `aria-disabled` span at 50% opacity; removed from the tab order.
- **Focus-visible** — `--ds-color-focus-ring` outline on every interactive control in both themes.

## Responsive Behavior

Built for tight layouts: pair with `flex-wrap` footers (status text on the left, pagination on the right) and the row collapses gracefully at 375px. The smaller footprint also makes it the right choice inside cards and panels.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This pagination variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

Use in dense, productivity-focused surfaces: data-table footers, admin lists, log viewers. For marketing or editorial pages, prefer the reference or large treatments.
