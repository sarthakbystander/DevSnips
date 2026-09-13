# Live-Region Alert

Dynamic application feedback done right: alerts mounted on the event announce through their role — `role="status"` politely for outcomes, `role="alert"` assertively for failures — with one live region per message so nothing is announced twice.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-live";

const [result, setResult] = useState(null);

async function save() {
  await api.save(settings);
  // Mount the alert when the event happens — the role announces it.
  setResult({ variant: "success", title: "Settings saved" });
}

{result ? (
  <Alert variant={result.variant}>
    <AlertTitle>{result.title}</AlertTitle>
  </Alert>
) : null}
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Alert, {
  AlertTitle,
  AlertDescription,
} from "./alert-live";

const [result, setResult] = useState(null);

async function save() {
  await api.save(settings);
  // Mount the alert when the event happens — the role announces it.
  setResult({ variant: "success", title: "Settings saved" });
}

{result ? (
  <Alert variant={result.variant}>
    <AlertTitle>{result.title}</AlertTitle>
  </Alert>
) : null}
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

No extra primitives: live-region behavior comes from the role the variant already carries. The pattern is *where* the alert mounts — conditionally, on the event — not a new component.

## Behavior

A live region announces when **content changes inside it**. The reliable pattern is to mount the alert when the event happens: the role (`status` or `alert`) makes the insertion an announcement. Do not pre-render a hidden alert and toggle visibility — a region that exists but is hidden behaves inconsistently across screen readers.

Demo 1 runs a fake async save: "Save settings" resolves into a `role="status"` success alert (polite), "Simulate failure" resolves into a `role="alert"` destructive alert (assertive). One alert node exists at a time, so each event produces exactly one announcement — nesting `aria-live` wrappers around an alert would announce it twice.

Demo 2 is the contrast case: an always-visible project note with `role={null}`. It is static content, so it announces nothing — which is correct.

## Keyboard Interaction

The alert surface itself is not focusable and carries no keyboard behavior — it is feedback, not a control. Any interactive element composed inside it (an action button, a link) is a real native control: Tab reaches it, Enter/Space activates it, and a `focus-visible` ring (2px, `color.focus-ring` token) marks keyboard focus.

## Accessibility

- The root carries a live-region role matched to urgency: `role="status"` (polite) for default/info/success, `role="alert"` (assertive) for warning/destructive — informational messages are never blanket-promoted to `role="alert"`.
- `AlertTitle` / `AlertDescription` register themselves with the root, so `aria-labelledby` / `aria-describedby` always reference real rendered content and are omitted entirely when the region is absent.
- The semantic icon is `aria-hidden="true"`: meaning is carried by the role and text, so state is never communicated by color alone.
- Pass `role={null}` for static page content that should not announce itself (for example an always-visible note rendered at page load).
- Mount-on-event gives one announcement per event; a new event replaces the alert node, which re-announces with the new content.
- Never wrap an `Alert` in another `aria-live` container — nested live regions cause duplicate announcements.

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

If the alert appears near the control that triggered it, sighted users get the spatial connection for free; screen-reader users get the announcement — you do not need to move focus to the alert (and should not, unless it contains required actions).
