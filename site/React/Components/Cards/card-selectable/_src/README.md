# Selectable Card

Real selection semantics, not a clickable `<div>`: `SelectableCard` wraps a native radio or checkbox input whose whole card is the `<label>`, and `SelectableCardGroup` manages the single choice inside a `<fieldset>`/`legend`. Controlled and uncontrolled modes both supported.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
import Card, { SelectableCard, SelectableCardGroup } from "./card-selectable";

// Single choice (recommended — the group keeps state in sync):
<SelectableCardGroup
  legend="Choose a plan"
  columns={3}
  options={[
    { value: "starter", label: "Starter" },
    { value: "team", label: "Team" },
    { value: "enterprise", label: "Enterprise" },
  ]}
/>

// Independent multi-select:
<SelectableCard label="Usage alerts" description="Notify at 80% of limits." />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import Card, { SelectableCard, SelectableCardGroup } from "./card-selectable";

// Single choice (recommended — the group keeps state in sync):
<SelectableCardGroup
  legend="Choose a plan"
  columns={3}
  options={[
    { value: "starter", label: "Starter" },
    { value: "team", label: "Team" },
    { value: "enterprise", label: "Enterprise" },
  ]}
/>

// Independent multi-select:
<SelectableCard label="Usage alerts" description="Notify at 80% of limits." />
```

## Props

### `<SelectableCard>`

| Name | Type | Default | Description |
|---|---|---|---|
| `type` | `"checkbox" \| "radio"` | `"checkbox"` | `checkbox` for independent multi-select; `radio` for single choice within a `name` (`SelectableCardGroup` renders this for each option). |
| `label` | `ReactNode` | — | Visible card label; also the input's accessible name. |
| `description` | `ReactNode` | — | Supporting text, wired via `aria-describedby`. |
| `checked` / `defaultChecked` | `boolean` | — | Controlled (with `onChange`) or uncontrolled selection. |
| `onChange` | `(event) => void` | — | Native change event handler. |
| `disabled` / `required` | `boolean` | — | Native input semantics. |
| `name` / `value` | `string` | — | Native form association. |
| `id` | `string` | — | Explicit input id (generated with `useId` otherwise). |

The whole card is the `<label htmlFor>` of a real native input: clicking anywhere on the card toggles it, Space toggles, radio groups keep browser arrow-key navigation, and forms submit the value.

### `<SelectableCardGroup>`

| Name | Type | Default | Description |
|---|---|---|---|
| `legend` | `ReactNode` | — | Visible `<legend>` for the fieldset. |
| `options` | `SelectableCardOption[]` | — | `{ value, label, description?, disabled? }[]`. |
| `value` / `defaultValue` | `string` | — | Controlled (with `onChange`) or uncontrolled selected option value. |
| `onChange` | `(value, event) => void` | — | Called with the newly selected option value. |
| `disabled` / `required` | `boolean` | — | Applied to every option. |
| `name` | `string` | — | Radio group name (generated otherwise). |
| `columns` | `1 \| 2 \| 3` | `1` | Card columns from `sm` up. |

Single choice via `<input type="radio">` cards. The group owns the value and passes controlled `checked` down, so uncontrolled mode stays in sync even though a deselected radio receives no change event of its own — the same group-tracking recipe the radio family uses.

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

`SelectableCard` is self-contained: its `<label htmlFor>` wraps the input, the visible label, the description, and the tracked indicator. For single choice prefer `SelectableCardGroup`, which renders one `SelectableCard` per option inside a `<fieldset>` and owns the value.

## Behavior

Each selectable card's entire surface is the `<label htmlFor>` of its input, so clicking anywhere toggles the control — and the input's own change handler keeps the tracked React state (border + indicator) in sync in both controlled (`checked` + `onChange`) and uncontrolled (`defaultChecked`) modes.

`SelectableCardGroup` is a `<fieldset>` of `type="radio"` cards. It owns the selected value and passes `checked` down to each option — the same recipe the Radio family uses — because a deselected radio receives no change event of its own; the group re-derives every option's state. `defaultValue` keeps uncontrolled mode working while `onChange` reports every new selection (shown in the live note). Checkbox semantics (`type="checkbox"`) are for independent multi-select; radio semantics (`type="radio"`) are for single choice within the same `name`.

## Keyboard Interaction

| Key | Behavior |
|---|---|
| `Tab` | Move into / between selectable cards (native input focus order) |
| `Space` | Toggle the focused radio / checkbox card |
| `Arrow keys` (radio group) | Move selection within the group (native browser behavior) |
| Click on the card | Toggles — the whole card is the `<label htmlFor>` |

Each input exposes a real `focus-visible` outline via the `color.focus-ring` token; disabled options are skipped by Tab and cannot be activated.

## Accessibility

- Selection semantics come from native `<input type="radio">` / `<input type="checkbox">` elements — no fake `role="button"`, no click-handlers on `<div>`s.
- The visible label text is the input's accessible name via `<label htmlFor>`; the description is wired with `aria-describedby` on the input.
- `SelectableCardGroup` is a real `<fieldset>` + `<legend>`, so screen readers announce the group context for each option.
- The selected state is border + visible control glyph; the tracked indicator div is `aria-hidden`.

## States

- **Idle** — bordered surface with the card shadow-xs; hover shifts to `surface-hover`.
- **Selected** — `--ds-color-primary` border plus the checked indicator (check glyph / radio dot) — border + control, never color alone.
- **Focus** — `focus-visible` 2px outline on the real input; `focus-within` strengthens the card border.
- **Disabled** — native `disabled` on the input: 60% opacity on the label, `cursor-not-allowed`, out of the tab order.

## Responsive Behavior

The group's grid is single-column below `sm` and uses the `columns` count from `sm` up; labels and descriptions wrap instead of overflowing. The card is fluid-width (`w-full min-w-0`) and fills its container at every viewport: at 375px titles and descriptions wrap, long words break, and the header action slot shrinks to its content instead of pushing text out (the header text column is `1fr` with a `min-w-0` grid track). Footer actions stack full-width below `sm` and lay out inline from `sm` up. No horizontal overflow at 375 / 768 / 1280px.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-surface)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../../DESIGN_TOKENS.md) for the authoritative token specification. This card variant follows the token system rules: `radius-md` surfaces, 1px `color.border`, restrained `shadow-xs` elevation, heading-md titles, body-sm descriptions, and semantic status colors for trends.

## Notes

For multi-select checkboxes use ≤ a few cards or consider the Checkboxes family; `SelectableCard` reuses that control recipe at card scale.
