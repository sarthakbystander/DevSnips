# Dropdown Menu Submenu

One nested menu level with correct menu semantics: ArrowRight opens, ArrowLeft closes, Escape collapses only the submenu, and the panel flips sides at the viewport edge.

## Usage

```tsx
import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from "./dropdown-menu-submenu";

<DropdownMenu>
  <DropdownMenuTrigger>File</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Open</DropdownMenuItem>
    <DropdownMenuSub>
      <DropdownMenuSubTrigger>Share</DropdownMenuSubTrigger>
      <DropdownMenuSubContent>
        <DropdownMenuItem>Copy link</DropdownMenuItem>
        <DropdownMenuItem>Email</DropdownMenuItem>
        <DropdownMenuItem>Export as PDF</DropdownMenuItem>
      </DropdownMenuSubContent>
    </DropdownMenuSub>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Archive</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from "./dropdown-menu-submenu";

<DropdownMenu>
  <DropdownMenuTrigger>File</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Open</DropdownMenuItem>
    <DropdownMenuSub>
      <DropdownMenuSubTrigger>Share</DropdownMenuSubTrigger>
      <DropdownMenuSubContent>
        <DropdownMenuItem>Copy link</DropdownMenuItem>
        <DropdownMenuItem>Email</DropdownMenuItem>
        <DropdownMenuItem>Export as PDF</DropdownMenuItem>
      </DropdownMenuSubContent>
    </DropdownMenuSub>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Archive</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Props

### `<DropdownMenu>`

| Name | Type | Default | Description |
|---|---|---|---|
| `open` | `boolean` | — | Open state (controlled). |
| `defaultOpen` | `boolean` | `false` | Initial open state (uncontrolled). |
| `onOpenChange` | `(open: boolean) => void` | — | Called whenever the menu requests to open or close. |
| `placement` | `"bottom-start" \| "bottom-end" \| "top-start" \| "top-end"` | `"bottom-start"` | Preferred placement; flips to stay in the viewport. |
| `className` | `string` | — | Extra classes on the relative wrapper. |
| `children` | `ReactNode` | — | `DropdownMenuTrigger` + `DropdownMenuContent`. |

### `<DropdownMenuTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the button. |
| `children` | `ReactNode` | — | Visible trigger label (a chevron is rendered after it). |

A real `<button type="button">` with `aria-haspopup="menu"` + `aria-expanded`; every native button attribute (`disabled`, `aria-label`, …) is forwarded.

### `<DropdownMenuContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="menu"` panel. |
| `children` | `ReactNode` | — | Items, labels, groups, and separators. |

Rendered only while open. Labelled by the trigger via `aria-labelledby`; pass `aria-label` to override.

### `<DropdownMenuItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered aria-hidden). |
| `shortcut` | `string` | — | Informational shortcut at the trailing edge (aria-hidden; exposed via `aria-keyshortcuts`). |
| `destructive` | `boolean` | `false` | Destructive styling via the semantic destructive token. |
| `disabled` | `boolean` | `false` | Native disabled: skipped by arrow keys, out of the tab order, not activatable. |
| `closeOnSelect` | `boolean` | `true` | Whether activating the item closes the menu. |
| `onSelect` | `(event) => void` | — | Called on activation before the menu closes; `event.preventDefault()` keeps the menu open. |
| `children` | `ReactNode` | — | Visible item label. |

### `<DropdownMenuLabel>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the label. |
| `children` | `ReactNode` | — | Section heading text. |

Non-interactive. Give it an `id` and point the group's `aria-labelledby` at it when labelling a `DropdownMenuGroup`.

### `<DropdownMenuGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the group. |
| `children` | `ReactNode` | — | Grouped items. |

Renders `role="group"`; forward `aria-labelledby` to associate it with its `DropdownMenuLabel`.

### `<DropdownMenuSeparator>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the separator. |

A `role="separator"` horizontal rule. Not focusable, not announced as an item.

### `<DropdownMenuSub>`

| Name | Type | Default | Description |
|---|---|---|---|
| `children` | `ReactNode` | — | `DropdownMenuSubTrigger` + `DropdownMenuSubContent`. |

Owns the nested level's open state and registers with the parent menu level so sibling pointer interaction closes it.

### `<DropdownMenuSubTrigger>`

| Name | Type | Default | Description |
|---|---|---|---|
| `icon` | `ReactNode` | — | Meaningful leading icon (rendered aria-hidden). |
| `className` | `string` | — | Extra classes on the item. |
| `children` | `ReactNode` | — | Visible item label (a chevron-right is rendered after it). |

A `role="menuitem"` button with `aria-haspopup="menu"` + `aria-expanded`; ArrowRight / Enter / Space open the submenu, hovering opens it without moving focus.

### `<DropdownMenuSubContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the `role="menu"` panel. |
| `children` | `ReactNode` | — | Submenu items. |

Opens to the right of its trigger and flips left when the right side would leave the viewport. ArrowLeft / Escape close only this level.

## Composition

Dropdown Menu is a compound component. Seven primitives compose the pattern:

```tsx
<DropdownMenu>
  <DropdownMenuTrigger>Actions</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>Project</DropdownMenuLabel>
    <DropdownMenuGroup>
      <DropdownMenuItem>Edit</DropdownMenuItem>
      <DropdownMenuItem>Duplicate</DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuSeparator />
    <DropdownMenuItem destructive>Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

- `DropdownMenu` — the root. Owns the open state (controlled via `open` + `onOpenChange`, or uncontrolled via `defaultOpen`), the trigger/content id wiring, the placement preference, and outside-pointer closing. Renders a `relative inline-flex` wrapper the menu panel anchors to.
- `DropdownMenuTrigger` — a real `<button type="button">` with `aria-haspopup="menu"` + `aria-expanded`. Click toggles; ArrowDown opens with the first item focused, ArrowUp with the last. The trailing chevron rotates while open.
- `DropdownMenuContent` — the `role="menu"` panel, labelled by the trigger. Rendered only while open; measures itself before paint and flips placement to stay in the viewport.
- `DropdownMenuItem` — one action: a real `<button>` with `role="menuitem"`. Optional `icon`, `shortcut`, `destructive`, `disabled`, `closeOnSelect`, and `onSelect` props.
- `DropdownMenuLabel` — a non-interactive section heading (uppercase, tracked, smaller type).
- `DropdownMenuGroup` — a `role="group"` wrapper; associate it with its label via `aria-labelledby`.
- `DropdownMenuSeparator` — a `role="separator"` horizontal rule between groups.

A submenu is a `<DropdownMenuSub>` wrapping exactly one `<DropdownMenuSubTrigger>` and one `<DropdownMenuSubContent>`, placed inline among the parent menu's items. The primitives nest recursively, but one level covers almost every real use case — deeper nesting is an information-architecture smell.

## Menu Behavior

Submenus add one nested level through three primitives:

- `DropdownMenuSub` — owns the nested open state and registers a close callback with the parent menu level, so pointer interaction with a sibling item closes the open submenu.
- `DropdownMenuSubTrigger` — a `role="menuitem"` with `aria-haspopup="menu"` + `aria-expanded` and a trailing chevron-right. ArrowRight / Enter / Space open the submenu and focus its first item; hover opens it without moving focus.
- `DropdownMenuSubContent` — the nested `role="menu"` panel, labelled by its sub trigger. It opens to the right of the trigger and flips to the left when the right side would leave the viewport.

Focus moves predictably: into the submenu on open, back to the sub trigger on ArrowLeft / Escape / sibling-close, and back to the root trigger when the whole menu closes. Closing a submenu never strands focus inside a removed panel — it falls back to the sub trigger. Activating a leaf item still closes the whole tree and returns focus to the root trigger.

The root `<DropdownMenu>` owns the open state. Both modes are supported:

- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultOpen`; the component owns the state.

Opening moves focus into the menu: the first item, or the last item when the trigger was invoked with ArrowUp. Activating an item runs its `onSelect` and then closes the menu (set `closeOnSelect={false}` or call `event.preventDefault()` in `onSelect` to keep it open). Closing — via selection, Escape, the trigger, or a pointer down outside — returns focus to the trigger, except on Tab, where focus is allowed to move forward naturally.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the menu, focus the first item |
| `ArrowDown` / `ArrowUp` | Move focus between enabled items at the current level, wrapping |
| `ArrowRight` (sub trigger) | Open the submenu, focus its first item |
| `ArrowLeft` (submenu) | Close the submenu, focus its sub trigger |
| `Enter` / `Space` (sub trigger) | Open the submenu, focus its first item |
| `Home` / `End` | Focus the first / last enabled item at the current level |
| `Escape` (submenu) | Close only the submenu, focus its sub trigger |
| `Escape` (top-level menu) | Close the whole menu, focus the root trigger |
| `Tab` | Close the whole menu and move focus forward naturally |

Pointer: hovering a sub trigger opens its submenu without moving focus; hovering a sibling item closes the open submenu at that level; clicking a sub trigger opens it and focuses the first item.

## Accessibility

The structure follows the WAI-ARIA menu button pattern.

- The trigger is a native `<button>` with `aria-haspopup="menu"`, `aria-expanded`, and `aria-controls` pointing at the open panel.
- The panel is `role="menu"` labelled by its trigger (`aria-labelledby`); items are `role="menuitem"` on real `<button>` elements — no `div` click handlers.
- Focus is real DOM focus: opening moves focus into the menu, closing returns it to the trigger, and focus is never left on an unmounted element.
- Disabled items carry the native `disabled` attribute, which assistive technology announces as unavailable.
- `DropdownMenuSeparator` uses `role="separator"`; icons are `aria-hidden` decoration and shortcuts are exposed via `aria-keyshortcuts`, so accessible names stay clean.

Each level is its own `role="menu"` labelled by its own trigger, and key handling is level-scoped: Escape and ArrowLeft collapse only the innermost open level. The root trigger's `aria-controls` chain stays intact because submenus live inside the root panel's DOM subtree.

## States

- **Trigger (idle)** — bordered surface button with a muted chevron; hover shifts to a subtle surface.
- **Trigger (open)** — `aria-expanded="true"`; keeps the hover surface and rotates the chevron 180°.
- **Item (idle)** — foreground text on the elevated menu surface.
- **Item (hover / focus)** — `--ds-color-surface-hover` background; keyboard focus additionally shows the `--ds-color-focus-ring` outline inside the item bounds.
- **Item (disabled)** — native `disabled`: 50% opacity, no pointer events, skipped by arrow keys, out of the tab order.
- **Panel** — `--ds-color-surface-elevated` with a 1px `--ds-color-border` and the restrained `--ds-shadow-md`, per the Dropdown/Popover token rules (radius-md, subtle border, body-sm type).
- **Sub trigger** — a menu item with a trailing chevron-right affordance; while its submenu is open it keeps `aria-expanded="true"`.
- **Submenu panel** — same surface/border/shadow model as the root panel, anchored to the sub trigger's side instead of below the root trigger.

## Responsive Behavior

The menu panel caps its width at `100vw - 1.5rem` and its height at `min(20rem, 100vh - 2rem)` with internal scrolling, so it stays inside the viewport at every width from 375px up without shrinking the trigger. Placement flips (bottom ↔ top, start ↔ end) keep the panel attached to its trigger near viewport edges. Long item labels truncate within the panel rather than forcing horizontal page overflow; the trigger label truncates within its own `max-w-full` bounds. The trigger keeps the shared 36px (h-9) control height — a comfortable touch target — at every breakpoint. Submenus open to the side rather than below, so the level flip (right ↔ left) is what keeps them on screen on narrow viewports; combined with the panel width cap, a submenu stays fully usable at 375px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This dropdown-menu variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

Hover opens a submenu without moving focus (pointer users keep pointing); keyboard opens move focus to the first sub item. The two entry modes are deliberate — focus follows the modality that opened the level.
