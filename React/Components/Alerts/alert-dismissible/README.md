# Dismissible Alert

An alert the user can dismiss: a real close button with an accessible name, controlled (`open` + `onDismiss`) or uncontrolled (`defaultOpen`) state, and focus management that never strands keyboard users when the alert unmounts.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-dismissible";

// Uncontrolled
<Alert variant="info" dismissible onDismiss={() => persistDismissal()}>
  <AlertTitle>Usage resets on the 1st</AlertTitle>
  <AlertDescription>Your quota renews each billing cycle.</AlertDescription>
</Alert>

// Controlled
const [open, setOpen] = useState(true);
<Alert
  variant="info"
  dismissible
  open={open}
  onDismiss={() => setOpen(false)}
>
  …
</Alert>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-dismissible";

// Uncontrolled
<Alert variant="info" dismissible onDismiss={() => persistDismissal()}>
  <AlertTitle>Usage resets on the 1st</AlertTitle>
  <AlertDescription>Your quota renews each billing cycle.</AlertDescription>
</Alert>

// Controlled
const [open, setOpen] = useState(true);
<Alert
  variant="info"
  dismissible
  open={open}
  onDismiss={() => setOpen(false)}
>
  …
</Alert>
```

## Props

### `<Alert>`

| Name | Type | Default | Description |
|---|---|---|---|
| `variant` | `"default" \| "info" \| "success" \| "warning" \| "destructive"` | `"default"` | Semantic intent: tints the surface, picks the default icon, and picks the default live-region role. |
| `size` | `"md" \| "sm"` | `"md"` | Density: `sm` reduces padding/gap for dense interfaces. |
| `role` | `"status" \| "alert" \| null` | derived from `variant` | Live-region role: `status` (polite) for default/info/success, `alert` (assertive) for warning/destructive. Pass `null` for static page content that must not announce itself. |
| `dismissible` | `boolean` | `false` | Render a trailing `AlertClose` wired to the dismissal state. |
| `open` | `boolean` | — | Controlled visibility (with `onDismiss`). |
| `defaultOpen` | `boolean` | `true` | Initial visibility when uncontrolled. |
| `onDismiss` | `() => void` | — | Called when the user dismisses the alert via the close button. |
| `icon` | `ReactNode` | variant glyph | `undefined` renders the variant's semantic icon (none for `default`), a ReactNode replaces it, `null` hides it. |
| `closeLabel` | `string` | `"Dismiss alert"` | Accessible name for the auto-rendered close button. |
| `id` | `string` | generated | Root element id; the title/description ids derive from it. |
| `className` | `string` | — | Extra classes on the surface. |
| `children` | `ReactNode` | — | `AlertTitle`, `AlertDescription`, `AlertAction`, `AlertClose` compositions. |

Every other attribute of a plain `<div>` (`aria-*`, `data-*`, …) is forwarded — including `aria-live`, for the rare case the role's implicit live behavior needs adjusting.

### `<AlertClose>`

| Name | Type | Default | Description |
|---|---|---|---|
| `label` | `string` | root's `closeLabel` | Accessible name for the icon-only button. |
| `onClick` | `(event) => void` | — | Runs before dismissal; call `event.preventDefault()` to veto the dismiss. |
| `children` | `ReactNode` | × glyph | Custom button content (kept `aria-hidden` — the name comes from `label`). |
| `className` | `string` | — | Extra classes on the button. |

A real `<button type="button">` that dismisses the nearest `<Alert>`: Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus. If the alert was unmounting the focused button, focus moves to the next operable element in document order before removal.

### `<AlertTitle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the title. |
| `children` | `ReactNode` | — | Title text. |

A styled `<p>`, not a heading — alerts are feedback regions, so they stay out of the page outline. Registers itself with the root, which then wires `aria-labelledby`.

### `<AlertDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the description. |
| `children` | `ReactNode` | — | Supporting content — a `<div>`, so paragraphs, lists, and links are all valid. |

Registers itself with the root, which then wires `aria-describedby`.

## Composition

- `Alert` — the root surface (radius-md, 1px border, token-tinted per variant) and the dismissal state owner (controlled `open` + `onDismiss`, or uncontrolled `defaultOpen`). When `dismissible` it appends a trailing `AlertClose`.
- `AlertIcon` — the leading icon slot; renders the variant's semantic glyph by default, a custom `ReactNode` when given, and is always `aria-hidden` (the role + text carry the meaning).
- `AlertTitle` — the alert headline (a styled `<p>` — alerts are feedback regions, not document headings). Registers itself so the root wires `aria-labelledby` only when a title exists.
- `AlertDescription` — supporting content (a `<div>`, so lists and links are valid children). Registers itself for `aria-describedby`.
- `AlertAction` — the actions row inside the text column; `flex-wrap` keeps real `<button>` / `<a>` children usable at narrow widths.
- `AlertClose` — a real `<button type="button">` with an accessible name that dismisses the nearest `Alert` (auto-rendered when `dismissible`, or composed manually for custom placement).

Compose only the primitives an alert actually needs — a bare `Alert` with an `AlertDescription` is valid; so is the full icon + title + description + action + close composition.

Set `dismissible` and the root appends a trailing `AlertClose` wired to the alert's dismissal state — no manual wiring. For custom placement, compose `<AlertClose />` yourself (it reads the nearest `Alert` context) and leave `dismissible` off.

## Behavior

Dismissal works in both state modes:

- **Uncontrolled** (demo 1): the alert owns its visibility. Clicking the close button unmounts it and `onDismiss` still fires (persist the dismissal there). The "Reset demo" button remounts it.
- **Controlled** (demo 2): the parent owns `open`. Clicking close fires `onDismiss` and the alert hides only when the parent sets `open={false}` — the event log shows the callback firing.

In both modes the close button is a real `<button type="button">` with an accessible name (`closeLabel` on the root, or `label` on `AlertClose`). Because the focused button unmounts on dismissal, focus first moves to the next operable element in document order — try it: Tab to the close button, press Enter, and focus lands on the control after the alert instead of dropping to `<body>`.

## Keyboard Interaction

The alert surface itself is not focusable and carries no keyboard behavior — it is feedback, not a control. Any interactive element composed inside it (an action button, a link) is a real native control: Tab reaches it, Enter/Space activates it, and a `focus-visible` ring (2px, `color.focus-ring` token) marks keyboard focus.

The close button is a real `<button type="button">`: Tab reaches it and Enter/Space activates it. When dismissal removes the focused button from the DOM, focus moves to the next operable element in document order (or the previous one at the end of the page) — it never drops to `<body>`.

## Accessibility

- The root carries a live-region role matched to urgency: `role="status"` (polite) for default/info/success, `role="alert"` (assertive) for warning/destructive — informational messages are never blanket-promoted to `role="alert"`.
- `AlertTitle` / `AlertDescription` register themselves with the root, so `aria-labelledby` / `aria-describedby` always reference real rendered content and are omitted entirely when the region is absent.
- The semantic icon is `aria-hidden="true"`: meaning is carried by the role and text, so state is never communicated by color alone.
- Pass `role={null}` for static page content that should not announce itself (for example an always-visible note rendered at page load).
- The icon-only close button always carries an accessible name (`"Dismiss alert"` by default; customize with `closeLabel` per message).
- Dismissal moves focus to the next operable element before unmounting — keyboard users never lose their place.

## States

- **Surface** — `color.surface` for `default`, or a semantic tint derived via `color-mix` from `color.info` / `color.success` / `color.warning` / `color.destructive`; 1px border (part token, part tint), `radius-md`, no elevation — inline alerts are not floating.
- **Title / description** — body-sm: a medium title on `color.foreground`, muted body on `color.muted-foreground`.
- **Icon** — 16px, colored by the variant's semantic token, decorative to assistive technology.
- **Close button** — muted glyph with a translucent `currentColor` hover wash, a `focus-visible` ring, and native `disabled` styling (50% opacity, no pointer events).
- **Dismissed** — unmounts from the DOM (uncontrolled) or when the parent sets `open={false}` (controlled); `onDismiss` fires in both modes.

## Responsive Behavior

The alert is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px the title and description wrap (long words break), while the icon and close button shrink-wrap instead of pushing text out — the text column is `flex-1` with `min-w-0`. `AlertAction` is `flex-wrap`, so multiple actions wrap to another row instead of overflowing, and the close button stays reachable. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`); semantic tints are derived from the semantic tokens with `color-mix`, so no component-specific values are invented. Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This alert variant follows the token system rules: `radius-md` surfaces, 1px borders, body-sm text, semantic status colors (`color.info` / `color.success` / `color.warning` / `color.destructive`) for tints and icons, and the `color.focus-ring` token for keyboard focus.

## Notes

`AlertClose` supports a veto: call `event.preventDefault()` in a custom `onClick` to stop the dismissal (for example while a save is in flight).
