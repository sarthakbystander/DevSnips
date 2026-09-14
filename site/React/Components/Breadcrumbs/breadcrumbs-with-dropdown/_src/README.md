# Breadcrumbs With Dropdown

Breadcrumb trail where one level opens a keyboard-accessible menu of related pages — a real menu button with aria-haspopup and aria-expanded, containing real anchor links.

## Usage

```tsx
import Breadcrumbs, {
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbCurrent,
  BreadcrumbSeparator,
  BreadcrumbDropdown,
} from "./breadcrumbs-with-dropdown";

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
    <BreadcrumbDropdown
      label="Components"
      items={[
        { label: "Buttons", href: "/documentation/components/buttons", current: true },
        { label: "Inputs", href: "/documentation/components/inputs" },
        { label: "Selects", href: "/documentation/components/selects" },
        { label: "Tabs", href: "/documentation/components/tabs" },
        { label: "Breadcrumbs", href: "/documentation/components/breadcrumbs" },
      ]}
    />
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
  BreadcrumbDropdown,
} from "./breadcrumbs-with-dropdown";

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
    <BreadcrumbDropdown
      label="Components"
      items={[
        { label: "Buttons", href: "/documentation/components/buttons", current: true },
        { label: "Inputs", href: "/documentation/components/inputs" },
        { label: "Selects", href: "/documentation/components/selects" },
        { label: "Tabs", href: "/documentation/components/tabs" },
        { label: "Breadcrumbs", href: "/documentation/components/breadcrumbs" },
      ]}
    />
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

### `<BreadcrumbDropdown>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` (required) | — | Visible trigger label — the name of this breadcrumb level. Also the menu's `aria-label`. |
| `items` | `BreadcrumbDropdownItem[]` (required) | — | Related pages offered at this level. |
| `aria-label` | `string` | `label` | Accessible name override for the trigger. |
| `className` | `string` | — | Extra classes on the wrapping list item. |

`BreadcrumbDropdownItem` = `{ label: ReactNode; href: string; icon?: ReactNode; current?: boolean }`. Set `current` on the item matching the page you are on — it is marked `aria-current="page"` and emphasized.

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

`<BreadcrumbDropdown>` renders its own `<li>` and slots between separators like any other level. Only that level becomes a menu — the rest of the trail stays plain breadcrumb navigation.

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

The trigger is a real `<button>` with `aria-haspopup="menu"` and `aria-expanded`; the menu is `role="menu"` of real `<a role="menuitem">` links, labelled by the level name. Escape closes and returns focus to the trigger; pointer interaction outside closes the menu. Focus moves into the menu on open and cycles with the arrow keys.

## States

- **Link** — muted foreground; hover shifts to the foreground color with an underline.
- **Current page** — foreground color at medium weight; not interactive.
- **Separator** — muted decorative glyph, hidden from assistive technology.
- **Focus-visible** — `--ds-color-focus-ring` outline on links and menu triggers in both themes.
- **Dropdown trigger** — styled as a breadcrumb link with a chevron; the chevron rotates 180° while open and the label takes the foreground color (`aria-expanded` state, not color alone).
- **Menu items** — `surface-hover` on hover/focus; the `current` item is medium weight with `aria-current="page"`.

## Responsive Behavior

The trigger is a `min-w-0` flexible item, so a long level name truncates with the rest of the trail on narrow screens. The menu is absolutely positioned under its level with `min-w-[180px]`; keep item labels short enough to fit small viewports.

The list uses `flex-wrap` with a `min-w-0` flexible item per level, so long trails wrap onto multiple lines instead of forcing page-level horizontal scrolling. From 375px up, prefer intentional reduction over squeezing: collapse middle levels with `breadcrumbs-collapsed` and cap long labels with `breadcrumbs-max-width`.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `text-[var(--ds-color-muted-foreground)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This breadcrumb variant uses the semantic color, radius, typography, and motion tokens.

## Notes

Use the dropdown when a level has meaningful siblings a reader may want to jump between (component categories, doc sections). Do not turn the whole trail into a menu — one level at most.
