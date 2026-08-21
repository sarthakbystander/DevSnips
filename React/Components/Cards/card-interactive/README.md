# Interactive Card

A card that is itself the interactive element — without the fake-`<div>` anti-pattern. With `href` it renders a real anchor (navigation); without `href` it renders a real `<button type="button">` (actions). Discriminated-union typing keeps the two modes apart.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, {
  InteractiveCard,
  CardContent,
} from "./card-interactive";

// Navigation — renders a real <a>:
<InteractiveCard href="/docs">
  <CardContent>Browse the documentation</CardContent>
</InteractiveCard>

// Action — renders a real <button type="button">:
<InteractiveCard onClick={startExport} disabled={busy}>
  <CardContent>Export usage report</CardContent>
</InteractiveCard>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, {
  InteractiveCard,
  CardContent,
} from "./card-interactive";

// Navigation — renders a real <a>:
<InteractiveCard href="/docs">
  <CardContent>Browse the documentation</CardContent>
</InteractiveCard>

// Action — renders a real <button type="button">:
<InteractiveCard onClick={startExport} disabled={busy}>
  <CardContent>Export usage report</CardContent>
</InteractiveCard>
```

## Props

### `<InteractiveCard>`

| Name | Type | Default | Description |
|---|---|---|---|
| `href` | `string` | — | Destination URL; renders a real `<a>`. Omit `href` and the card renders a real `<button type="button">` for actions. |
| `onClick` / `disabled` | — | — | Button-mode props (action cards). `disabled` only exists on the button branch (anchors cannot be disabled natively). |
| `className` | `string` | — | Extra classes on the control. |
| `children` | `ReactNode` | — | `CardHeader` / `CardContent` sections rendered inside the single control. |

The whole card is one real control — anchor for navigation, button for actions. Do not nest other interactive elements inside it; put secondary actions in a sibling `CardAction` slot of a plain `Card`.

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

`InteractiveCard` replaces the `Card` root for one-of-one-control cards: its children are still the normal region primitives (`CardHeader`, `CardContent`), but the surface is a single anchor/button instead of a `<div>`.

## Behavior

The anchor branch is the navigation pattern: middle-click, open-in-new-tab, copy-link, and screen-reader link semantics all work, and the demo below tracks the live hash — the same hash-navigation trick the Breadcrumbs/Pagination previews use.

The button branch is the action pattern: it activates on Enter and Space, carries the only meaningful `disabled` state (anchors cannot be disabled natively — the prop simply does not exist on the anchor branch, enforced by the typed union).

Because the whole card is one control, other interactive elements must not be nested inside it — that produces invalid, confusing activation. Secondary actions belong on a sibling `Card` (e.g. in a `CardAction` slot), never inside an `InteractiveCard`.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Tab` | Reach the card control (one tab stop per card) |
| `Enter` | Follow the link (anchor mode) or activate the button (button mode) |
| `Space` | Activate the button (button mode) |

Anchor-mode cards are followed with Enter like any link; button-mode cards use the native button activation set. Disabled button cards are skipped by Tab.

## Accessibility

- The card is one real control — `<a href>` for navigation, `<button type="button">` for actions — never a `<div>` with a click handler.
- Screen readers announce a link or a button with its text content as the accessible name; icons inside are `aria-hidden`.
- No nested interactive elements inside the card; only such a structure produces one clean activation.
- `disabled` exists only on the button branch (anchors have no native disabled state) and is exposed by the native attribute.

## States

- **Idle** — bordered surface (shadow-xs) exactly like a plain card.
- **Hover** — border strengthens and the surface shifts (`surface-hover`); the whole card signals it is one target.
- **Active** — `surface-active` press feedback (colors only, no transform).
- **Focus-visible** — 2px `color.focus-ring` outline, offset 2px, around the whole card.
- **Disabled (button mode)** — native `disabled`: 50% opacity, `pointer-events-none`, out of the tab order.

## Responsive Behavior

The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

If you need more than one action per card, use a plain `Card` with `CardAction`/`CardFooter` instead of stretching `InteractiveCard` into a multi-control container.
