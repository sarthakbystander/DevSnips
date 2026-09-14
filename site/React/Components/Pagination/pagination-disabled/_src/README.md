# Disabled Pagination

Disabled-state patterns for page navigation: boundary-disabled steppers, an individually disabled page control, and a fully disabled navigation.

## Usage

```tsx
import Pagination, {
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
} from "./pagination-disabled";

// Boundary disabling is automatic — Previous is disabled on page 1:
<Pagination page={1} totalPages={5} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationLink page={1} /></PaginationItem>
    <PaginationItem><PaginationLink page={2} /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Disable one page (e.g. results still loading):
<PaginationLink page={3} disabled />

// Disable the whole navigation:
<Pagination disabled page={2} totalPages={5} onPageChange={setPage}>…</Pagination>
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
} from "./pagination-disabled";

// Boundary disabling is automatic — Previous is disabled on page 1:
<Pagination page={1} totalPages={5} onPageChange={setPage}>
  <PaginationContent>
    <PaginationItem><PaginationPrevious /></PaginationItem>
    <PaginationItem><PaginationLink page={1} /></PaginationItem>
    <PaginationItem><PaginationLink page={2} /></PaginationItem>
    <PaginationItem><PaginationNext /></PaginationItem>
  </PaginationContent>
</Pagination>

// Disable one page (e.g. results still loading):
<PaginationLink page={3} disabled />

// Disable the whole navigation:
<Pagination disabled page={2} totalPages={5} onPageChange={setPage}>…</Pagination>
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

No new primitives — this variant documents and demonstrates the three disabled paths built into the core: automatic boundary disabling on the steppers, `disabled` on a single `PaginationLink`, and `disabled` on the `<Pagination>` root.

## Pagination Logic

The root `<Pagination>` owns the current page and clamps every navigation target into `1 … totalPages`, so out-of-range requests are impossible. Both modes are supported:

- **Controlled** — pass `page` + `onPageChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultPage`; the component owns the state.

Controls pick their element from how navigation is driven: with `buildHref` (or an explicit `href`) they render real `<a href>` anchors and the browser performs normal navigation; without URLs they render `<button type="button">` and call `setPage`. `PaginationPrevious` is disabled when the current page is 1, `PaginationNext` when it is `totalPages`.

Every disabled path renders the control as a non-interactive `<span aria-disabled="true">` instead of an anchor or button: it stays visible (50% opacity, same geometry, no layout shift) but leaves the tab order and cannot be activated by click, Enter, or Space. When a boundary control becomes enabled again it returns to its normal element.

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

Disabled controls are announced as "dimmed"/unavailable via `aria-disabled` and are skipped by keyboard focus, so users cannot land on a control that does nothing. The current page keeps `aria-current="page"` even while the navigation is disabled, preserving position context.

## States

- **Page control (idle)** — muted foreground; hover shifts to a subtle surface with foreground text.
- **Current page** — bordered surface with a hairline border, foreground text, and `aria-current="page"`. Distinguished by border, surface, and weight together — never by color alone.
- **Previous / Next** — same idle treatment with a directional chevron; the visible text label carries the accessible name.
- **Disabled** — non-interactive `aria-disabled` span at 50% opacity; removed from the tab order.
- **Focus-visible** — `--ds-color-focus-ring` outline on every interactive control in both themes.

## Responsive Behavior

The control list uses `flex-wrap` with a `gap-1` rhythm, so on narrow screens controls wrap onto a second line instead of shrinking below usable sizes or forcing page-level horizontal scrolling. From 375px up, prefer intentional reduction over squeezing: show fewer numbered links (previous/next-only with `pagination-with-previous-next`), or collapse the range with `pagination-with-ellipsis`. Controls keep their full height at every width: 36px at `md`, 32px at `sm`, 44px at `lg` (a comfortable touch target).

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This pagination variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

Do not fake disabled states with `pointer-events: none` on active elements — a disabled control must be a genuinely non-interactive element. This variant's demos cover the first page, the last page, an unavailable middle page, and a fully disabled navigation.
