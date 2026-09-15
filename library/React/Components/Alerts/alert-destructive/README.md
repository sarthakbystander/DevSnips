# Destructive Alert

Failures and blocking errors: a red tint derived from the `color.destructive` token, the error glyph, and an assertive `role="alert"` — for failed operations and validation summaries the user must resolve.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-destructive";

<Alert variant="destructive">
  <AlertTitle>Deployment failed</AlertTitle>
  <AlertDescription>
    Build #482 exited with code 1 during the test step.
  </AlertDescription>
</Alert>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-destructive";

<Alert variant="destructive">
  <AlertTitle>Deployment failed</AlertTitle>
  <AlertDescription>
    Build #482 exited with code 1 during the test step.
  </AlertDescription>
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

### `<AlertIcon>`

| Name | Type | Default | Description |
|---|---|---|---|
| `children` | `ReactNode` | variant glyph | Custom icon content; defaults to the alert variant's semantic glyph. |
| `className` | `string` | — | Extra classes on the icon slot. |

The slot is always `aria-hidden="true"`: the icon supplements the variant's role + text and never carries meaning alone. Colored by the variant's semantic token (16px, currentColor).

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

`variant="destructive"` supplies the tint, the error glyph, and the assertive role. `AlertDescription` is a `<div>`, so an error summary can contain a real list — see the second demo.

## Behavior

The destructive variant is assertive (`role="alert"`): the operation failed and the user must do something before they can continue.

The first demo reports a failed deployment. The second is the form error-summary pattern: the description contains a real `<ul>` of field errors, so keyboard and screen-reader users can enumerate what must be fixed — the summary says what is wrong, the fields say where.

## Keyboard Interaction

The alert surface itself is not focusable and carries no keyboard behavior — it is feedback, not a control. Any interactive element composed inside it (an action button, a link) is a real native control: Tab reaches it, Enter/Space activates it, and a `focus-visible` ring (2px, `color.focus-ring` token) marks keyboard focus.

## Accessibility

- The root carries a live-region role matched to urgency: `role="status"` (polite) for default/info/success, `role="alert"` (assertive) for warning/destructive — informational messages are never blanket-promoted to `role="alert"`.
- `AlertTitle` / `AlertDescription` register themselves with the root, so `aria-labelledby` / `aria-describedby` always reference real rendered content and are omitted entirely when the region is absent.
- The semantic icon is `aria-hidden="true"`: meaning is carried by the role and text, so state is never communicated by color alone.
- Pass `role={null}` for static page content that should not announce itself (for example an always-visible note rendered at page load).
- Error summaries list every problem in text; the red tint and glyph are supplements, never the only error indication.

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

When the user can fix the failure inline (retry, update billing), add an action — see `alert-with-action`. When the message arrives asynchronously, mount it on the event — see `alert-live`.
