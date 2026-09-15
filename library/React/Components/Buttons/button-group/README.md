# Button Group

A joined row of related buttons. Inner buttons share borders (side radius removed, borders overlapped by 1px) so the group reads as one control. Pass children for full control, or the `items` prop for a quick group.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<ButtonGroup label="Text alignment" items={[{id:"l",label:"Left"},{id:"c",label:"Center",active:true},{id:"r",label:"Right"}}] />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `items` | `Array<{ id?: string; label: ReactNode; icon?: string; active?: boolean; onClick?: () => void }>` | — |
| `children` | `ReactNode` | — (renders children directly when no `items`) |
| `variant` | `outline \| solid \| secondary \| ghost` | `outline` |
| `size` | `ButtonSize` | `md` |
| `label` | `string` | — (group `aria-label`) |

Plus all native `HTMLAttributes<HTMLDivElement>`.

## Variants

outline (default) · solid · secondary · ghost. Children render with their own variant; `items` use the shared `variant`.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · selected (`active` → `aria-pressed` + `surface-active`) · disabled (reduced opacity on each child).

## Accessibility

Renders a `role="group"` container with `aria-label`. Each item is a native `<button>` with `aria-pressed` when `active`. Focus-visible ring on each child.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

For mutually exclusive single-choice control, prefer SegmentedButton (radiogroup semantics). ButtonGroup is a loose toolbar row.
