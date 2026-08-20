# Breadcrumbs With Separator

Breadcrumb trail with a configurable separator: set one separator node on the root for the whole trail, or override a single position — separators stay decorative and aria-hidden.

## Usage

```tsx
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-separator";

// One separator for the whole trail:
<Breadcrumbs separator="/">
  <BreadcrumbList>
    <BreadcrumbItem><BreadcrumbLink href="/">Home</BreadcrumbLink></BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem><BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem><BreadcrumbCurrent>Tabs</BreadcrumbCurrent></BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// A custom icon separator:
<Breadcrumbs separator={<ChevronRightIcon />}>…</Breadcrumbs>

// Override a single position in place:
<BreadcrumbSeparator>{">"}</BreadcrumbSeparator>
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
} from "./breadcrumbs-with-separator";

// One separator for the whole trail:
<Breadcrumbs separator="/">
  <BreadcrumbList>
    <BreadcrumbItem><BreadcrumbLink href="/">Home</BreadcrumbLink></BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem><BreadcrumbLink href="/documentation">Documentation</BreadcrumbLink></BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem><BreadcrumbCurrent>Tabs</BreadcrumbCurrent></BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>

// A custom icon separator:
<Breadcrumbs separator={<ChevronRightIcon />}>…</Breadcrumbs>

// Override a single position in place:
<BreadcrumbSeparator>{">"}</BreadcrumbSeparator>
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

The separator is resolved per position: a `<BreadcrumbSeparator>` with children uses them, otherwise it falls back to the `separator` given to `<Breadcrumbs>` through context, otherwise the default chevron. Set it once on the root to restyle the whole trail.

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

Separators are structural decoration, not navigation: every separator renders an `aria-hidden` `role="presentation"` list item, so it is never announced, never focusable, and never behaves like a link — whichever glyph you choose.

## States

- **Link** — muted foreground; hover shifts to the foreground color with an underline.
- **Current page** — foreground color at medium weight; not interactive.
- **Separator** — muted decorative glyph, hidden from assistive technology.
- **Focus-visible** — `--ds-color-focus-ring` outline on links and menu triggers in both themes.

## Responsive Behavior

The list uses `flex-wrap` with a `min-w-0` flexible item per level, so long trails wrap onto multiple lines instead of forcing page-level horizontal scrolling. From 375px up, prefer intentional reduction over squeezing: collapse middle levels with `breadcrumbs-collapsed` and cap long labels with `breadcrumbs-max-width`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This breadcrumb variant uses the semantic color, radius, typography, and motion tokens.

## Notes

Keep separators restrained: a chevron, a slash, or a single angle bracket. The glyph inherits the muted-foreground token and the 14px icon sizing, so custom separators stay in the same visual language.
