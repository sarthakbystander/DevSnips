# Button With Icon

A labeled button with a leading or trailing icon. Icons use the shared size token for the chosen button size, with the standard control gap keeping icon and label optically aligned.

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<ButtonWithIcon icon="download" iconPosition="trailing">Export</ButtonWithIcon>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | — |
| `icon` | `string` (icon name) | — |
| `iconPosition` | `leading \| trailing` | `leading` |
| `variant` | `solid \| outline \| secondary \| ghost` | `solid` |
| `size` | `ButtonSize` | `md` |
| `disabled` | `boolean` | `false` |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`. Provide your own icon set; this component renders an `<Icon name>` helper slot — see Notes.

## Variants

solid (default) · outline · secondary · ghost.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · active · focus-visible · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. Decorative icons are marked `aria-hidden`; the label provides the accessible name.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

The shipped `icon` prop accepts an icon name string rendered by a small inline `Icon` helper (drop in your own). To use a custom icon node, pass `iconLeft`/`iconRight` to SolidButton/OutlineButton/etc. instead.
