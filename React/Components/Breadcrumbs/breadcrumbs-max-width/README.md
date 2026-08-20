# Breadcrumbs Max Width

Breadcrumb trail that bounds long labels with max-width truncation while keeping the full text available through the title attribute — no clipped, meaningless navigation.

## Usage

```tsx
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-max-width";

<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/design-tokens">
        Design tokens and theming guidelines
      </BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Overriding tokens for white-label themes</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// Labels truncate at 9rem (14rem from sm up). The `title` attribute is
// auto-filled from string children — pass `title` explicitly when the
// label is a ReactNode:
<BreadcrumbLink href="/glossary" title="White-label theming">
  <em>White-label</em> theming
</BreadcrumbLink>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-max-width";

<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/design-tokens">
        Design tokens and theming guidelines
      </BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Overriding tokens for white-label themes</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// Labels truncate at 9rem (14rem from sm up). The `title` attribute is
// auto-filled from string children — pass `title` explicitly when the
// label is a ReactNode:
<BreadcrumbLink href="/glossary" title="White-label theming">
  <em>White-label</em> theming
</BreadcrumbLink>
```

## Props

### `<Breadcrumbs>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | `"Breadcrumb"` | Accessible label for the `<nav>` landmark. |
| `separator` | `ReactNode` | chevron icon | Default separator content for every `<BreadcrumbSeparator>` without children. |
| `className` | `string` | — | Extra classes on the `<nav>`. |
| `children` | `ReactNode` | — | `BreadcrumbList` composition. |

### `<BreadcrumbList>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<ol>`. |
| `children` | `ReactNode` | — | `BreadcrumbItem` + `BreadcrumbSeparator` elements. |

### `<BreadcrumbItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `<li>`. |
| `children` | `ReactNode` | — | Usually one `BreadcrumbLink` or `BreadcrumbCurrent`. |

### `<BreadcrumbLink>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` (required) | — | Destination URL — rendered as a real anchor with normal browser navigation. |
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered `aria-hidden`). |
| `className` | `string` | — | Extra classes on the anchor. |
| `children` | `ReactNode` | — | Visible label. |

All native anchor attributes (`target`, `rel`, `aria-label`, `title`, …) are forwarded.

### `<BreadcrumbCurrent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered `aria-hidden`). |
| `className` | `string` | — | Extra classes on the span. |
| `children` | `ReactNode` | — | Visible label (rendered with `aria-current="page"`). |

### `<BreadcrumbSeparator>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the list item. |
| `children` | `ReactNode` | context `separator` | Custom separator content for this position only. |

## Composition

Breadcrumbs is a compound component. Six primitives compose the pattern:

```tsx
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>
```

- `Breadcrumbs` — the root `<nav aria-label="Breadcrumb">` landmark. Provides the default `separator` to every separator through context.
- `BreadcrumbList` — the ordered list (`<ol>`). Wraps onto multiple lines instead of scrolling horizontally.
- `BreadcrumbItem` — one level of the trail (`<li>`).
- `BreadcrumbLink` — a real `<a href>` for navigable levels: normal browser navigation, optional leading `icon`.
- `BreadcrumbCurrent` — the current page: plain text with `aria-current="page"`, never a link.
- `BreadcrumbSeparator` — decorative structure between levels (`role="presentation"`, `aria-hidden`); renders its own `children`, else the `separator` given to `<Breadcrumbs>`, else the default chevron.

Same six primitives — this variant bakes a bounded `max-w` + `truncate` into `BreadcrumbLink` and `BreadcrumbCurrent` and auto-fills `title` from string children, so truncation never destroys the meaning of the trail.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Tab` / `Shift+Tab` | Move focus through the links |
| `Enter` | Follow the focused link |

## Accessibility

The structure follows the W3C Breadcrumb pattern: a `<nav aria-label="Breadcrumb">` landmark containing an ordered list (`<ol>`) whose last item is the current page marked with `aria-current="page"`.

- Every navigable level is a real `<a href>` — normal browser navigation, no click handlers faking links.
- The current page is plain text, not a link; assistive technology announces it as the current page.
- Separators are `aria-hidden` `role="presentation"` list items — never announced, never focusable.
- Icons are decorative (`aria-hidden`); the visible label always carries the accessible name.

Truncation is purely visual CSS (`truncate`) — the full label remains in the accessibility tree, so screen readers announce the complete text. The `title` attribute (auto-filled from string children, or passed explicitly for ReactNode labels) exposes the full text to sighted users on hover.

## States

- **Link** — muted foreground; hover shifts to the foreground color with an underline.
- **Current page** — foreground color at medium weight; not interactive.
- **Separator** — muted decorative glyph, hidden from assistive technology.
- **Focus-visible** — `--ds-color-focus-ring` outline on links and menu triggers in both themes.
- **Truncated label** — ends in an ellipsis inside `max-w-[9rem]` (`sm:max-w-[14rem]`); hovering reveals the native `title` tooltip with the full text.

## Responsive Behavior

Each label is capped at `max-w-[9rem]` below `sm` and `max-w-[14rem]` above, so no single verbose level can push the trail past the viewport. The list still wraps (`flex-wrap`) when several capped levels exceed the line — truncation bounds labels, wrapping handles volume. Neither creates page-level horizontal scrolling.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This breadcrumb variant uses the semantic color, radius, typography, and motion tokens.

## Notes

Do not rely on `overflow-hidden` alone: without the `title` attribute and the full accessibility-tree text, clipping would destroy meaning. Tune the caps through the `LINK_CLASSES` / `CURRENT_CLASSES` constants if your density differs.
