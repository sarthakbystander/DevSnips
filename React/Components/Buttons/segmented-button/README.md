# Segmented Button

A joined single-choice control that behaves like a radiogroup: one selected option at a time. Use for 2–5 mutually exclusive options in compact toolbars.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<SegmentedButton label="View" value={view} onChange={setView} options={[{value:"list",label:"List"},{value:"grid",label:"Grid"}}] />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `options` | `Array<{ value: string; label: ReactNode; icon?: string }>` | — |
| `value` | `string` | — (controlled) |
| `onChange` | `(value: string) => void` | — |
| `size` | `ButtonSize` | `sm` |
| `label` | `string` | — (radiogroup `aria-label`) |

Plus all native `HTMLAttributes<HTMLDivElement>`.

## Variants

Single segmented style: bordered container, selected segment uses `surface-active` + `aria-checked="true"` (radiogroup semantics).

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm` for compact toolbars.

## States

default · hover · focus-visible · selected (`aria-checked`, surface-active + font-weight) · disabled (via `disabled` on individual options).

## Accessibility

Renders `role="radiogroup"` with `aria-label`. Each segment is a `role="radio"` button with `aria-checked`. **Keyboard**: ArrowLeft/Right move between segments and select (roving selection, like a native radiogroup). Each segment has a focus-visible ring.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

For multi-select, use ToggleGroup. SegmentedButton is strictly single-choice. Keep to 2–5 options; for more, use a Select.
