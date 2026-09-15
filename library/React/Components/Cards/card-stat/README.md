# Stat Card

Compact metric presentation: an uppercase muted label, a large tabular-numeral value, and a semantic trend (icon + text, success/quiet tokens — never color alone). Plain composition of the card primitives — no fake chart components.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, { CardContent } from "./card-stat";

<Card>
  <CardContent className="flex flex-col gap-1.5 py-5">
    <p className="label">Monthly recurring revenue</p>
    <p className="value">$48,290</p>
    <p className="trend">+12.4% vs last month</p>
  </CardContent>
</Card>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, { CardContent } from "./card-stat";

<Card>
  <CardContent className="flex flex-col gap-1.5 py-5">
    <p className="label">Monthly recurring revenue</p>
    <p className="value">$48,290</p>
    <p className="trend">+12.4% vs last month</p>
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

A stat card is composition, not a new export: `Card` + `CardContent` with a muted label, a large `tabular-nums` value, and a trend line. The pattern is small enough to keep out of the component API.

## Behavior

The label is uppercase muted text, the value is 24px semibold with `tabular-nums` so figures align in dashboards, and the trend line pairs a 14px direction icon with a text delta plus a baseline ("vs last month").

The demos show the three common cases — up (revenue, users), down-as-good (fewer tickets), and the neutral reading — using the `success` token for positive movement and muted text for the neutral frame. A real product can map movement direction to its own semantics the same way. No decorative sparklines or fake charts: the point of the variant is the reusable metric structure.

## Keyboard Interaction

The card surface itself is not focusable and carries no keyboard behavior — that is intentional, it is not a control. Every action rendered inside it (footer buttons, header icon buttons) is a native `<button>` or `<a>`, so Tab reaches it, Enter/Space activates it, and a `focus-visible` ring marks keyboard focus.

## Accessibility

- The card is a plain structural `<div>` — no fake `role="button"`, no `tabIndex` on a container, no click handlers on `<div>` elements.
- `CardTitle` renders a real `<h3>` heading, so card titles participate in the page outline.
- Actions inside the card are real native controls with visible labels or explicit `aria-label`s and `focus-visible` rings.
- State and meaning are never carried by color alone.
- The trend line is text ('+12.4% vs last month') — the arrow icon is decorative and `aria-hidden`; movement is never conveyed by color or icon alone.

## States

- **Label** — uppercase, muted, 12px: category of the metric.
- **Value** — 24px semibold with `tabular-nums` on the foreground color.
- **Trend** — direction icon + delta text in the `success` token for favorable movement; muted text for the baseline. Color is always paired with text.

## Responsive Behavior

The three-up grid collapses to one column below `sm`; values keep `tabular-nums` alignment; long labels wrap. The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

Keep stat cards to four-or-fewer per row so each metric stays readable — a row of equal-width metric cards is the intended composition.
