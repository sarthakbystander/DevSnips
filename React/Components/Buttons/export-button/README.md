# Export Button

A menu trigger for export destinations. `formats` is a list of export targets; opens a keyboard-navigable menu (aria-haspopup="menu"). Arrow keys move, Enter exports, Escape closes.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<ExportButton formats={[{id:"csv",label:"Export as CSV"},{id:"pdf",label:"Export as PDF"}}] onExport={handle} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `formats` | `Array<{ id: string; label: ReactNode; icon?: string }>` | `[]` |
| `onExport` | `(id, format) => void` | — |
| `label` | `string` | `"Export"` |
| `variant` | `outline \| secondary` | `outline` |
| `size` | `ButtonSize` | `sm` |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

outline (default) · secondary. Menu is a bordered elevated surface.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px. Default is `sm` for toolbars.

## States

default · hover · focus-visible · open (menu, `aria-expanded`) · disabled (reduced opacity).

## Accessibility

Trigger has `aria-haspopup="menu"` + `aria-expanded`. Menu uses `role="menu"`, items `role="menuitem"`. **Keyboard**: ArrowUp/Down move, Enter/Space exports, Escape closes and returns focus to the trigger, outside click closes.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Use in table/report toolbars where multiple export targets exist. For a single target, use DownloadButton instead.
