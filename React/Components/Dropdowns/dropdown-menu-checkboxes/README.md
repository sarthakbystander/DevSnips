# Dropdown Menu Checkboxes

Checkable menu items (role=menuitemcheckbox + aria-checked) for toggling view options — controlled and uncontrolled, with the menu staying open while options are flipped.

## Usage

```tsx
import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuSeparator,
} from "./dropdown-menu-checkboxes";

// Uncontrolled:
<DropdownMenu>
  <DropdownMenuTrigger>View options</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuCheckboxItem defaultChecked>Show sidebar</DropdownMenuCheckboxItem>
    <DropdownMenuCheckboxItem>Show toolbar</DropdownMenuCheckboxItem>
    <DropdownMenuCheckboxItem defaultChecked>Show status bar</DropdownMenuCheckboxItem>
  </DropdownMenuContent>
</DropdownMenu>

// Controlled:
const [rulers, setRulers] = useState(false);
<DropdownMenuCheckboxItem checked={rulers} onCheckedChange={setRulers}>
  Show rulers
</DropdownMenuCheckboxItem>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import DropdownMenu, {
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuSeparator,
} from "./dropdown-menu-checkboxes";

// Uncontrolled:
<DropdownMenu>
  <DropdownMenuTrigger>View options</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuCheckboxItem defaultChecked>Show sidebar</DropdownMenuCheckboxItem>
    <DropdownMenuCheckboxItem>Show toolbar</DropdownMenuCheckboxItem>
    <DropdownMenuCheckboxItem defaultChecked>Show status bar</DropdownMenuCheckboxItem>
  </DropdownMenuContent>
</DropdownMenu>

// Controlled:
const [rulers, setRulers] = useState(false);
<DropdownMenuCheckboxItem checked={rulers} onCheckedChange={setRulers}>
  Show rulers
</DropdownMenuCheckboxItem>
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

### `<DropdownMenuCheckboxItem>`

| Name | Type | Default | Description |
|---|---|---|---|
| `checked` | `boolean` | — | Checked state (controlled). |
| `defaultChecked` | `boolean` | `false` | Initial checked state (uncontrolled). |
| `onCheckedChange` | `(checked: boolean) => void` | — | Called with the next checked state on activation. |
| `closeOnSelect` | `boolean` | `false` | Whether activating the item closes the menu. |
| `onSelect` | `(event) => void` | — | Called on activation after the state toggles. |
| `shortcut` | `string` | — | Informational shortcut at the trailing edge. |
| `disabled` | `boolean` | `false` | Native disabled: skipped by keys, not activatable. |
| `children` | `ReactNode` | — | Visible item label. |

Renders `role="menuitemcheckbox"` with `aria-checked`; the check indicator is aria-hidden decoration.

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

`<DropdownMenuCheckboxItem>` joins the core primitives: a real button with `role="menuitemcheckbox"` and `aria-checked`, a fixed 16px indicator slot whose check glyph tracks the checked state, and the same keyboard/pointer behavior as a plain item. Mix checkbox items with plain items, labels, and separators freely.

## Menu Behavior

The root `<DropdownMenu>` owns the open state. Both modes are supported:

- **Controlled** — pass `open` + `onOpenChange`; the parent owns the state.
- **Uncontrolled** — pass `defaultOpen`; the component owns the state.

Opening moves focus into the menu: the first item, or the last item when the trigger was invoked with ArrowUp. Activating an item runs its `onSelect` and then closes the menu (set `closeOnSelect={false}` or call `event.preventDefault()` in `onSelect` to keep it open). Closing — via selection, Escape, the trigger, or a pointer down outside — returns focus to the trigger, except on Tab, where focus is allowed to move forward naturally.

The panel opens relative to its trigger at the requested `placement` (`bottom-start` by default) and measures itself in a layout effect before paint: if the preferred side would leave the viewport, it flips to the other side (bottom ↔ top, start ↔ end). The panel also caps its own height (`min(20rem, 100vh - 2rem)` with internal scrolling) and width (`100vw - 1.5rem`), so menus never routinely overflow the viewport. No positioning library is involved.

`<DropdownMenuCheckboxItem>` is the exception to close-on-select: toggling an option keeps the menu open by default (`closeOnSelect` defaults to `false`), so several view options can be flipped in one visit. Both state modes are supported — controlled (`checked` + `onCheckedChange`) and uncontrolled (`defaultChecked`).

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Enter` / `Space` (trigger) | Open the menu, focus the first item |
| `ArrowDown` (trigger) | Open the menu, focus the first item |
| `ArrowUp` (trigger) | Open the menu, focus the last item |
| `ArrowDown` / `ArrowUp` (menu) | Move focus to the next / previous enabled item, wrapping at the ends |
| `Home` / `End` (menu) | Focus the first / last enabled item |
| `Enter` / `Space` (menu) | Activate the focused item; on a checkbox item, toggles its checked state |
| `Escape` | Close the menu and return focus to the trigger |
| `Tab` | Close the menu and move focus forward naturally |

The trigger and items are native `<button>` elements, so Enter/Space activation follows normal browser behavior. Disabled items use the native `disabled` attribute: they are skipped by arrow-key navigation, removed from the tab order, and cannot be activated.

## Accessibility

The structure follows the WAI-ARIA menu button pattern.

- The trigger is a native `<button>` with `aria-haspopup="menu"`, `aria-expanded`, and `aria-controls` pointing at the open panel.
- The panel is `role="menu"` labelled by its trigger (`aria-labelledby`); items are `role="menuitem"` on real `<button>` elements — no `div` click handlers.
- Focus is real DOM focus: opening moves focus into the menu, closing returns it to the trigger, and focus is never left on an unmounted element.
- Disabled items carry the native `disabled` attribute, which assistive technology announces as unavailable.
- `DropdownMenuSeparator` uses `role="separator"`; icons are `aria-hidden` decoration and shortcuts are exposed via `aria-keyshortcuts`, so accessible names stay clean.

State is communicated by `aria-checked` on the item itself, not by the glyph — the check mark is `aria-hidden` decoration. Because the items are real buttons, Space/Enter toggle them natively.

## States

- **Trigger (idle)** — bordered surface button with a muted chevron; hover shifts to a subtle surface.
- **Trigger (open)** — `aria-expanded="true"`; keeps the hover surface and rotates the chevron 180°.
- **Item (idle)** — foreground text on the elevated menu surface.
- **Item (hover / focus)** — `--ds-color-surface-hover` background; keyboard focus additionally shows the `--ds-color-focus-ring` outline inside the item bounds.
- **Item (disabled)** — native `disabled`: 50% opacity, no pointer events, skipped by arrow keys, out of the tab order.
- **Panel** — `--ds-color-surface-elevated` with a 1px `--ds-color-border` and the restrained `--ds-shadow-md`, per the Dropdown/Popover token rules (radius-md, subtle border, body-sm type).
- **Checkbox item (checked)** — the leading check glyph fades in (`--ds-color-primary`), `aria-checked="true"` carries the state to assistive technology.
- **Checkbox item (unchecked)** — the indicator slot stays empty, reserving alignment.
- **Checkbox item (disabled)** — native `disabled` with the current state frozen and visible.

## Responsive Behavior

The menu panel caps its width at `100vw - 1.5rem` and its height at `min(20rem, 100vh - 2rem)` with internal scrolling, so it stays inside the viewport at every width from 375px up without shrinking the trigger. Placement flips (bottom ↔ top, start ↔ end) keep the panel attached to its trigger near viewport edges. Long item labels truncate within the panel rather than forcing horizontal page overflow; the trigger label truncates within its own `max-w-full` bounds. The trigger keeps the shared 36px (h-9) control height — a comfortable touch target — at every breakpoint.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface-elevated)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This dropdown-menu variant uses the semantic color, radius, shadow, typography, and motion tokens.

## Notes

The check column is reserved on every checkbox item so checked and unchecked rows keep identical label alignment. Use checkboxes for independent options; for mutually exclusive options use dropdown-menu-radio.
