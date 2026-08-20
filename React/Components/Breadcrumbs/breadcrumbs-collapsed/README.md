# Breadcrumbs Collapsed

Long breadcrumb paths with middle levels collapsed behind an accessible ellipsis disclosure — the hidden levels stay reachable as real links from a keyboard-operable menu.

## Usage

```tsx
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
  BreadcrumbEllipsis,
} from "./breadcrumbs-collapsed";

// Home / … / Components / Buttons
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbEllipsis
      items={[
        { label: "Documentation", href: "/documentation" },
        { label: "React", href: "/documentation/react" },
      ]}
    />
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/react/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>
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
  BreadcrumbEllipsis,
} from "./breadcrumbs-collapsed";

// Home / … / Components / Buttons
<Breadcrumbs>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbEllipsis
      items={[
        { label: "Documentation", href: "/documentation" },
        { label: "React", href: "/documentation/react" },
      ]}
    />
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/documentation/react/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbCurrent>Buttons</BreadcrumbCurrent>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumbs>
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

### `<BreadcrumbEllipsis>`

| Name | Type | Default | Description |
|---|---|---|---|
| `items` | `BreadcrumbEllipsisItem[]` (required) | — | The collapsed levels, in path order. |
| `label` | `string` | `"Show hidden breadcrumb levels"` | Accessible name for the disclosure button. |
| `className` | `string` | — | Extra classes on the wrapping list item. |

`BreadcrumbEllipsisItem` = `{ label: ReactNode; href: string; icon?: ReactNode }`.

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

`<BreadcrumbEllipsis>` renders its own `<li>` and slots between separators where the removed levels would have been. Keep the first level (Home) and the last one or two levels visible; collapse the middle.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Enter` / `Space` / `ArrowDown` | Open the menu and focus the first item |
| `ArrowUp` (closed) | Open the menu and focus the last item |
| `ArrowDown` / `ArrowUp` (open) | Move between menu items (wraps around) |
| `Home` / `End` | Jump to the first / last menu item |
| `Enter` | Follow the focused menu link |
| `Escape` | Close the menu and return focus to the trigger |
| `Tab` | Close the menu and continue through the page |

## Accessibility

The structure follows the W3C Breadcrumb pattern: a `<nav aria-label="Breadcrumb">` landmark containing an ordered list (`<ol>`) whose last item is the current page marked with `aria-current="page"`.

- Every navigable level is a real `<a href>` — normal browser navigation, no click handlers faking links.
- The current page is plain text, not a link; assistive technology announces it as the current page.
- Separators are `aria-hidden` `role="presentation"` list items — never announced, never focusable.
- Icons are decorative (`aria-hidden`); the visible label always carries the accessible name.

The collapsed levels are never hidden with CSS alone — they are real anchor links inside a `role="menu"` disclosure. The trigger is a `<button aria-haspopup="menu" aria-expanded>` named "Show hidden breadcrumb levels" (override with `label`), reachable in the normal tab order, so keyboard and screen-reader users can reach every level. Escape closes and returns focus to the trigger.

## States

- **Link** — muted foreground; hover shifts to the foreground color with an underline.
- **Current page** — foreground color at medium weight; not interactive.
- **Separator** — muted decorative glyph, hidden from assistive technology.
- **Focus-visible** — `--ds-color-focus-ring` outline on links and menu triggers in both themes.
- **Ellipsis trigger** — compact `…` button; `surface-hover` on hover, `surface-active` + foreground while open (`aria-expanded` state, not color alone).
- **Menu items** — `surface-hover` on hover/focus; each is a real anchor link.

## Responsive Behavior

Collapsing is the preferred small-screen strategy: at 375px a five-level trail becomes Home / … / Components / Buttons, which fits without wrapping or scrolling while keeping every level reachable.

The list uses `flex-wrap` with a `min-w-0` flexible item per level, so long trails wrap onto multiple lines instead of forcing page-level horizontal scrolling. From 375px up, prefer intentional reduction over squeezing: collapse middle levels with `breadcrumbs-collapsed` and cap long labels with `breadcrumbs-max-width`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This breadcrumb variant uses the semantic color, radius, typography, and motion tokens.

## Notes

Choose which levels to collapse from your route data (typically `items.slice(1, -2)`). The ellipsis menu preserves path order, top to bottom.
