# Loading Button

An action button with a first-class loading state. `loading` swaps the leading slot for a spinner, sets `aria-busy`, and disables the button so the action can't be double-fired.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<LoadingButton onClick={save} loading={saving}>{saving ? "Saving…" : "Save"}</LoadingButton>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | — |
| `variant` | `solid \| outline \| secondary \| destructive \| success` | `solid` |
| `size` | `ButtonSize` | `md` |
| `block` | `boolean` | `false` |
| `loading` | `boolean` | `false` |
| `loadingLabel` | `ReactNode` | — (overrides children while loading) |
| `iconLeft` | `ReactNode` | — |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

solid (default) · outline · secondary · destructive · success. Same token-faithful appearance as the standalone variant buttons.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · loading (spinner + `aria-busy`, disabled, layout preserved) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. Layout is preserved because the spinner occupies the same leading slot as the icon, so the label doesn't shift while pending.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

The label may change during loading (via `loadingLabel` or by swapping `children`). The spinner occupies the icon slot so the button keeps its width and the label doesn't jump.
