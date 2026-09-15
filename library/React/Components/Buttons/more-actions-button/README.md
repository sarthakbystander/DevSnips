# More Actions Button

An overflow menu trigger. `actions` is a list of actions; opens a keyboard-navigable menu (aria-haspopup="menu"). Destructive actions render in `destructive` color. Icon-only by default; pass `label` for the accessible name.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<MoreActionsButton label="More actions" actions={[{id:"edit",label:"Edit"},{id:"delete",label:"Delete",destructive:true}}] onAction={handle} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `actions` | `Array<{ id: string; label: ReactNode; icon?: string; destructive?: boolean }>` | `[]` |
| `onAction` | `(id, action) => void` | — |
| `label` | `string` | `"More actions"` (rendered as `aria-label`) |
| `align` | `left \| right` | `right` (menu alignment) |
| `variant` | `ghost \| outline \| secondary` | `ghost` |
| `size` | `ButtonSize` | `sm` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

ghost (default) · outline · secondary. Menu is a bordered elevated surface; destructive items use `destructive` color.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm`; icon-only (three-dots).

## States

default · hover · focus-visible · open (menu, `aria-expanded`) · disabled (reduced opacity).

## Accessibility

Trigger has `aria-haspopup="menu"` + `aria-expanded` + `aria-label`. Menu uses `role="menu"`, items `role="menuitem"`. **Keyboard**: ArrowUp/Down move, Enter/Space activates, Escape closes and returns focus, outside click closes. Destructive items are visually marked with the destructive color (a cue, not the only signal — the label conveys intent).

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use in dense rows/headers where actions would otherwise overflow. For a primary action + alternatives, use SplitButton.
