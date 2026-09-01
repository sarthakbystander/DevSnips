# Card with Footer

The footer region: a primary + secondary action row that stacks full-width on small screens, plus a split footer (metadata left, action right) via a `sm:justify-between` className override.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, {
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "./card-with-footer";

<Card>
  <CardHeader>
    <CardTitle>Team plan</CardTitle>
  </CardHeader>
  <CardContent>…</CardContent>
  <CardFooter className="sm:justify-end">
    <button>Compare plans</button>
    <button>Upgrade</button>
  </CardFooter>
</Card>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, {
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "./card-with-footer";

<Card>
  <CardHeader>
    <CardTitle>Team plan</CardTitle>
  </CardHeader>
  <CardContent>…</CardContent>
  <CardFooter className="sm:justify-end">
    <button>Compare plans</button>
    <button>Upgrade</button>
  </CardFooter>
</Card>
```

## Props

### `<Card>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the surface. |
| `children` | `ReactNode` | — | Header, content, footer, and/or media regions. |

Every attribute of a plain `<div>` (`id`, `aria-*`, `data-*`, …) is forwarded. The card itself is non-interactive — use `InteractiveCard` or `SelectableCard` for click targets.

### `<CardHeader>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the header grid. |
| `children` | `ReactNode` | — | `CardTitle`, `CardDescription`, and optionally `CardAction`. |

A `grid-cols-[1fr_auto]`: title + description stack in the text column; an optional `CardAction` sits at the top of the auto-sized action column.

### `<CardTitle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the heading. |
| `children` | `ReactNode` | — | Title text. |

A real `<h3>` — if the page outline needs a different rank, pass the heading element semantics via your page structure (the visual style stays the same).

### `<CardContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the body region. |
| `children` | `ReactNode` | — | The main card content. |

### `<CardFooter>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the footer row (alignment: `sm:justify-end` / `sm:justify-between`). |
| `children` | `ReactNode` | — | Footer actions and metadata. |

Actions stack full-width below `sm` (primary last in DOM lands on top) and lay out inline from `sm` up. No baked-in justify utility, so alignment overrides never conflict.

## Composition

- `Card` — the root surface (radius-md, 1px border, surface color, shadow-xs). A plain `<div>` that only carries structure — it adds no fake interactivity.
- `CardHeader` — the header grid: title + description in a text column, an optional `CardAction` slot at the top right.
- `CardTitle` — a real `<h3>` heading (cards are page regions, so titles are headings).
- `CardDescription` — a `<p>` of muted supporting text.
- `CardAction` — the header action slot (icon buttons, a menu trigger).
- `CardContent` — the padded body region between header and footer.
- `CardFooter` — the action row; buttons stack full-width below `sm` and lay out inline from `sm` up (same recipe as the dialog footer).
- `CardMedia` — an image framed in a crop box (`video` 16:9 / `square` 1:1 / `none` natural) with graceful fallback when `src` is omitted.
- `SelectableCard` — a native `<input type="radio">` / `type="checkbox">` whose whole card is its `<label>`; controlled and uncontrolled.
- `SelectableCardGroup` — a `<fieldset>`/`<legend>` radio group owning the single selection for single-choice card pickers.
- `InteractiveCard` — a real `<a href>` when `href` is set (navigation), otherwise a real `<button type="button">` (actions).
- `CardSkeleton` — the loading placeholder: `aria-busy` + visually hidden label, reduced-motion-safe pulse.

Compose only the primitives a card actually needs — a plain `Card` with `CardContent` and no header or footer is valid.

`CardFooter` reuses the dialog-footer recipe: `flex-col-reverse` below `sm` (the primary action, last in DOM, lands on top of the stack) and an inline row from `sm` up. No justify utility is baked in — pass `sm:justify-end` for right-aligned actions or `sm:justify-between` for a split footer, and the override never conflicts.

## Behavior

Footers pin to the bottom of the card (`mt-auto`), so cards in an equal-height grid keep their action rows aligned.

The first demo is the standard secondary + primary pair. The second is the split pattern: muted metadata on the left, a single action on the right, composed with `sm:justify-between` and a plain `<p>` — no special primitive needed. Both sets of actions are real `<button>` elements and stay reachable when they stack at 375px.

## Keyboard Interaction

The card surface itself is not focusable and carries no keyboard behavior — that is intentional, it is not a control. Every action rendered inside it (footer buttons, header icon buttons) is a native `<button>` or `<a>`, so Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus.

## Accessibility

- The card is a plain structural `<div>` — no fake `role="button"`, no `tabIndex` on a container, no click handlers on `<div>` elements.
- `CardTitle` renders a real `<h3>` heading, so card titles participate in the page outline.
- Actions inside the card are real native controls with visible labels or explicit `aria-label`s and `focus-visible` rings.
- State and meaning are never carried by color alone.
- The primary action is last in DOM order, so keyboard users reach the safe secondary action first when tabbing, and the destructive-or-committing action is never the first stop.

## States

- **Surface** — `--ds-color-surface` with a 1px `--ds-color-border`, `radius-md`, and the restrained `shadow-xs` elevation (per the token rules: no floating-card aesthetics).
- **Title / description** — heading-md (18px, 600) on foreground; body-sm on `--ds-color-muted-foreground`.
- **Footer actions** — full-width stacked below `sm`, inline from `sm` up.
- **Disabled actions** — native `disabled`: 50% opacity, no pointer events, out of the tab order.

## Responsive Behavior

The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

Footer content is not limited to buttons — links, metadata, and status chips all work. Keep interactive elements real (`<button>` / `<a>`).
