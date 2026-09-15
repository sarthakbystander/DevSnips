# Card with Icon

Icon-led content cards: a restrained icon chip establishes hierarchy without dominating the card. Icons are inline SVG, `aria-hidden`, and carry meaning — the title still does the talking.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, {
  CardContent,
  CardTitle,
  CardDescription,
} from "./card-with-icon";

<Card>
  <CardContent className="flex flex-col gap-3">
    <span aria-hidden="true" className="icon-chip">{/* svg */}</span>
    <CardTitle>API reference</CardTitle>
    <CardDescription>Endpoints, scopes, and error codes.</CardDescription>
  </CardContent>
</Card>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, {
  CardContent,
  CardTitle,
  CardDescription,
} from "./card-with-icon";

<Card>
  <CardContent className="flex flex-col gap-3">
    <span aria-hidden="true" className="icon-chip">{/* svg */}</span>
    <CardTitle>API reference</CardTitle>
    <CardDescription>Endpoints, scopes, and error codes.</CardDescription>
  </CardContent>
</Card>
```

## Props

### `<Card>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the surface. |
| `children` | `ReactNode` | — | Header, content, footer, and/or media regions. |

Every attribute of a plain `<div>` (`id`, `aria-*`, `data-*`, …) is forwarded. The card itself is non-interactive — use `InteractiveCard` or `SelectableCard` for click targets.

### `<CardContent>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the body region. |
| `children` | `ReactNode` | — | The main card content. |

### `<CardTitle>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the heading. |
| `children` | `ReactNode` | — | Title text. |

A real `<h3>` — if the page outline needs a different rank, pass the heading element semantics via your page structure (the visual style stays the same).

### `<CardDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the paragraph. |
| `children` | `ReactNode` | — | Supporting description text. |

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

The icon chip is plain composition, not a new primitive: a 40px rounded `surface-subtle` square holding an inline SVG, stacked above `CardTitle` + `CardDescription` inside `CardContent`.

## Behavior

The icon establishes the category (docs, storage, integrations) so a grid of cards scans quickly — but hierarchy still comes from the heading, and the icon never replaces a label.

Icons come from the shared inline-SVG set used across the React library (stroke-based, `currentColor`, `aria-hidden`). No emoji, no icon fonts, no decorative overload: one icon per card.

## Keyboard Interaction

The card surface itself is not focusable and carries no keyboard behavior — that is intentional, it is not a control. Every action rendered inside it (footer buttons, header icon buttons) is a native `<button>` or `<a>`, so Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus.

## Accessibility

- The card is a plain structural `<div>` — no fake `role="button"`, no `tabIndex` on a container, no click handlers on `<div>` elements.
- `CardTitle` renders a real `<h3>` heading, so card titles participate in the page outline.
- Actions inside the card are real native controls with visible labels or explicit `aria-label`s and `focus-visible` rings.
- State and meaning are never carried by color alone.
- Every icon is wrapped `aria-hidden="true"`; the adjacent `CardTitle` heading carries the accessible name of the card's subject.

## States

- **Surface** — `--ds-color-surface` with a 1px `--ds-color-border`, `radius-md`, and the restrained `shadow-xs` elevation (per the token rules: no floating-card aesthetics).
- **Title / description** — heading-md (18px, 600) on foreground; body-sm on `--ds-color-muted-foreground`.
- **Footer actions** — full-width stacked below `sm`, inline from `sm` up.
- **Disabled actions** — native `disabled`: 50% opacity, no pointer events, out of the tab order.

## Responsive Behavior

The three-up grid collapses to one column below `sm` and the icon chip keeps its fixed 40px size at every width. The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

If the icon is the only thing distinguishing otherwise identical cards, prefer clearer titles instead of more icons.
