# Horizontal Card

A responsive horizontal card: media in a fixed left column with content beside it from `sm` up, collapsing to a top banner + stacked content below `sm`. Uses `CardMedia aspect="none"` with showcase-level layout classes.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, {
  CardMedia,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "./card-horizontal";

<Card className="overflow-hidden sm:flex-row">
  <CardMedia aspect="none" className="h-40 sm:h-auto sm:w-48" src="/cover.svg" alt="Report cover" />
  <div className="flex min-w-0 flex-1 flex-col">
    <CardHeader>
      <CardTitle>Q2 market insights</CardTitle>
      <CardDescription>Quarterly analysis for the pricing team.</CardDescription>
    </CardHeader>
    <CardFooter className="sm:justify-between">
      <p>Report · 14 pages</p>
      <button>Open report</button>
    </CardFooter>
  </div>
</Card>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, {
  CardMedia,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "./card-horizontal";

<Card className="overflow-hidden sm:flex-row">
  <CardMedia aspect="none" className="h-40 sm:h-auto sm:w-48" src="/cover.svg" alt="Report cover" />
  <div className="flex min-w-0 flex-1 flex-col">
    <CardHeader>
      <CardTitle>Q2 market insights</CardTitle>
      <CardDescription>Quarterly analysis for the pricing team.</CardDescription>
    </CardHeader>
    <CardFooter className="sm:justify-between">
      <p>Report · 14 pages</p>
      <button>Open report</button>
    </CardFooter>
  </div>
</Card>
```

## Props

### `<Card>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the surface. |
| `children` | `ReactNode` | — | Header, content, footer, and/or media regions. |

Every attribute of a plain `<div>` (`id`, `aria-*`, `data-*`, …) is forwarded. The card itself is non-interactive — use `InteractiveCard` or `SelectableCard` for click targets.

### `<CardMedia>`

| Name | Type | Default | Description |
|---|---|---|---|
| `src` | `string` | — | Image URL. Omit it to render the decorative `aria-hidden` placeholder (the layout never collapses). |
| `alt` | `string` | `""` | Alternative text; `""` marks decorative images — meaningful images must pass real alt text. |
| `aspect` | `"video" \| "square" \| "none"` | `"video"` | Crop box: 16:9, 1:1, or natural height (for fixed-size layouts like horizontal cards). |
| `className` | `string` | — | Extra classes on the media frame; the image fills it with `object-cover`. |

Every attribute of a plain `<img>` (`loading`, `sizes`, `srcSet`, …) is forwarded.

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

### `<CardDescription>`

| Name | Type | Default | Description |
|---|---|---|---|
| `className` | `string` | — | Extra classes on the paragraph. |
| `children` | `ReactNode` | — | Supporting description text. |

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

Horizontal arrangement is layout, not a new primitive: the card root gets `className="overflow-hidden sm:flex-row"`, the media frame gets `aspect="none"` plus a fixed column width (`h-40 sm:h-auto sm:w-48`), and a flex-column wrapper holds the header/footer regions.

## Behavior

The card is `flex-col` by default; adding `sm:flex-row` places the media frame and the text wrapper side by side from the `sm` breakpoint up. `aspect="none"` removes the ratio box so the frame can be a full-height column (`sm:h-auto sm:w-48`).

Below `sm` the media renders as a fixed-height banner (`h-40`) across the top and the regions stack — content is never clipped or hidden to make space. The card's `overflow-hidden` clips the media corners to the card radius in both arrangements.

## Keyboard Interaction

The card surface itself is not focusable and carries no keyboard behavior — that is intentional, it is not a control. Every action rendered inside it (footer buttons, header icon buttons) is a native `<button>` or `<a>`, so Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus.

## Accessibility

- The card is a plain structural `<div>` — no fake `role="button"`, no `tabIndex` on a container, no click handlers on `<div>` elements.
- `CardTitle` renders a real `<h3>` heading, so card titles participate in the page outline.
- Actions inside the card are real native controls with visible labels or explicit `aria-label`s and `focus-visible` rings.
- State and meaning are never carried by color alone.
- Document order is media, then header/footer regions; when the layout collapses at 375px the image still precedes the text, so reading order stays intact.

## States

- **Surface** — `--ds-color-surface` with a 1px `--ds-color-border`, `radius-md`, and the restrained `shadow-xs` elevation (per the token rules: no floating-card aesthetics).
- **Title / description** — heading-md (18px, 600) on foreground; body-sm on `--ds-color-muted-foreground`.
- **Footer actions** — full-width stacked below `sm`, inline from `sm` up.
- **Disabled actions** — native `disabled`: 50% opacity, no pointer events, out of the tab order.

## Responsive Behavior

Below `sm` (640px) the media is a `h-40` banner and the regions stack full-width; from `sm` up it becomes a 192px column and the text column flexes. Verified against overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

The `overflow-hidden` on the card root clips the media flush to the card border, so the frame needs no per-placement corner overrides.
