# Split Button

A primary action paired with an attached, keyboard-navigable menu of alternatives. The leading button fires the default action; the chevron opens a menu. A shared border and negative margin keep it one composite control.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<SplitButton label="Create project" actions={[{id:"blank",label:"Blank project"},{id:"import",label:"Import"}} onAction={handle} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `label` | `ReactNode` | — |
| `actions` | `Array<{ id: string; label: ReactNode; icon?: string; destructive?: boolean }>` | `[]` |
| `onAction` | `(id, action) => void` | — |
| `variant` | `solid \| outline` | `solid` |
| `size` | `ButtonSize` | `md` |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

solid (default) · outline. The menu is always a bordered elevated surface (`surface-elevated`, `radius-md`, `shadow-md`).

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · open (menu, `aria-expanded`) · disabled (reduced opacity).

## Accessibility

The chevron trigger has `aria-haspopup="menu"` + `aria-expanded`. The menu uses `role="menu"` and items `role="menuitem"`. **Keyboard**: trigger ArrowDown/Enter/Space opens; ArrowUp/Down move between items; Enter/Space activates; Escape closes and returns focus to the trigger; outside click closes. Selecting an item sets it as the new default and fires `onAction`.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use for action variants (one default + alternatives). Don't use for navigation. The leading button fires the last-chosen action.
