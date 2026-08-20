# Breadcrumbs With Current

Breadcrumb trail that explicitly distinguishes the current location: aria-current page text that is never a navigable link, via BreadcrumbCurrent or the current prop for data-driven trails.

## Usage

```tsx
import { Fragment } from "react";
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-current";

const trail = [
  { label: "Home", href: "/" },
  { label: "Documentation", href: "/documentation" },
  { label: "Components", href: "/documentation/components" },
  { label: "Tabs", href: "/documentation/components/tabs", current: true },
];

// Data-driven: `current` turns the link into non-navigable current text,
// so every level maps through one component without branching.
<Breadcrumbs>
  <BreadcrumbList>
    {trail.map((level, index) => (
      <Fragment key={level.href}>
        {index > 0 ? <BreadcrumbSeparator /> : null}
        <BreadcrumbItem>
          <BreadcrumbLink href={level.href} current={level.current}>
            {level.label}
          </BreadcrumbLink>
        </BreadcrumbItem>
      </Fragment>
    ))}
  </BreadcrumbList>
</Breadcrumbs>

// Explicit composition uses <BreadcrumbCurrent> for the last level.
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { Fragment } from "react";
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
} from "./breadcrumbs-with-current";

const trail = [
  { label: "Home", href: "/" },
  { label: "Documentation", href: "/documentation" },
  { label: "Components", href: "/documentation/components" },
  { label: "Tabs", href: "/documentation/components/tabs", current: true },
];

// Data-driven: `current` turns the link into non-navigable current text,
// so every level maps through one component without branching.
<Breadcrumbs>
  <BreadcrumbList>
    {trail.map((level, index) => (
      <Fragment key={level.href}>
        {index > 0 ? <BreadcrumbSeparator /> : null}
        <BreadcrumbItem>
          <BreadcrumbLink href={level.href} current={level.current}>
            {level.label}
          </BreadcrumbLink>
        </BreadcrumbItem>
      </Fragment>
    ))}
  </BreadcrumbList>
</Breadcrumbs>

// Explicit composition uses <BreadcrumbCurrent> for the last level.
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

Two ways to mark the current page: compose `<BreadcrumbCurrent>` explicitly, or pass `current` to `<BreadcrumbLink>` — it then renders the same non-navigable `aria-current="page"` text instead of an anchor, which keeps data-driven trails (route tables, CMS slugs) branch-free.

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

The current page is never a link to itself: `aria-current="page"` marks it for assistive technology, and the medium-weight foreground treatment keeps the distinction subtle and token-driven — never color alone, since weight changes with it.

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

Use the `current` prop when levels come from data (every entry has an href, including the page you are on); use `<BreadcrumbCurrent>` when composing by hand.
