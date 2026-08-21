# Loading Card

`CardSkeleton` placeholders that match the real card's geometry so content swaps in without layout shift: an accessible busy surface (`aria-busy` + visually hidden label) with a restrained, reduced-motion-safe pulse.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, { CardSkeleton } from "./card-loading";

{loading ? (
  <CardSkeleton lines={2} footer label="Loading report…" />
) : (
  <Card>…real content…</Card>
)}
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, { CardSkeleton } from "./card-loading";

{loading ? (
  <CardSkeleton lines={2} footer label="Loading report…" />
) : (
  <Card>…real content…</Card>
)}
```

## Props

### `<CardSkeleton>`

| Name | Type | Default | Description |
|---|---|---|---|
| `media` | `boolean` | `false` | Render a 16:9 media placeholder block. |
| `lines` | `number` | `2` | Number of body placeholder lines (minimum 1). |
| `footer` | `boolean` | `false` | Render an action-row placeholder. |
| `label` | `string` | `"Loading…"` | Visually hidden announcement while the card carries `aria-busy="true"`. |
| `className` | `string` | — | Extra classes on the surface (e.g. width in a grid). |

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

`CardSkeleton` renders a `Card` root with `aria-busy="true"` — options (`media`, `lines`, `footer`) shape the placeholder to the card it stands in for, so swapping is a clean geometry match.

## Behavior

Each placeholder block is a restrained gray shape on an `animate-pulse` opacity loop, matched to the real region sizes (title-ish bar, text lines, 36px button slots, 16:9 media frame). Toggle the demo's Reload button: the skeleton holds the layout while the (simulated) fetch runs, then the real card swaps in with no shift.

Under `prefers-reduced-motion` the pulse is disabled (`motion-reduce:animate-none`) — the static shapes still communicate loading. The label is visually hidden so the busy state announces without a visible banner, and the blocks are `aria-hidden` like any decorative progress.

## Keyboard Interaction

The card surface itself is not focusable and carries no keyboard behavior — that is intentional, it is not a control. Every action rendered inside it (footer buttons, header icon buttons) is a native `<button>` or `<a>`, so Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus.

## Accessibility

- `aria-busy="true"` marks the surface during loading; a visually hidden `span` (e.g. "Loading report…") announces the state when visible text would be noise.
- Placeholder blocks are wrapped `aria-hidden="true"` so they read as nothing, not garbage.
- The toggle demo announces through an `aria-live` note next to the Reload button.

## States

- **Busy surface** — normal card styling + `aria-busy="true"`; quiet, static gray placeholder blocks.
- **Pulse** — opacity loop only; layout never shifts; disabled under `prefers-reduced-motion`.
- **Options** — `media` adds a 16:9 frame, `lines` sets body line count (min 1), `footer` adds an action row, `label` customizes the hidden announcement.

## Responsive Behavior

The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

Match the skeleton to the destination card's shape (`media` for image cards, `footer` for action cards) — the swap-in reads as instant and stable.
