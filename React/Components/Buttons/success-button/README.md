# Success Button

A positive-emphasis action for confirm, publish, approve, and complete flows. Contextual only — not a replacement for the primary action.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<SuccessButton onClick={publish}>Publish</SuccessButton>
<SuccessButton done>Approved</SuccessButton>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | — |
| `size` | `ButtonSize` | `md` |
| `block` | `boolean` | `false` |
| `loading` | `boolean` | `false` |
| `done` | `boolean` | `false` |
| `disabled` | `boolean` | `false` |
| `iconLeft` / `iconRight` | `ReactNode` | — |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

Single filled variant built on `color.success` / `color.success-foreground`. `done` swaps the leading icon for a check for transient completion feedback.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · loading (spinner + `aria-busy`) · `done` (check icon) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. The `done` state is a visual confirmation; convey the same outcome to assistive tech via a live region on the owning surface.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

Contextual only — confirm/approve/publish/complete. Don't use success styling for the main save action; that's the SolidButton's job.
