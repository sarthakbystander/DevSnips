# Download Button

A direct download with progress feedback. Fires `onDownload` (wire to a real fetch/blob), surfaces a working state with a spinner, then a brief done state. Supports a `meta` line (e.g. "CSV · 2.4 MB").

## Installation

This component requires **React** and **Tailwind CSS**. Drop `code.tsx` (or `code.jsx` for JavaScript projects) into your project. Tailwind utility classes are included directly in the component, so no separate CSS file is required.

The component consumes the DevSnips semantic design tokens through Tailwind arbitrary values (for example `bg-[var(--ds-color-primary)]`). Define the `--ds-*` tokens once in your theme — see [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the full token spec.

## Usage

```tsx
<DownloadButton meta="CSV · 2.4 MB" onDownload={fetchCsv}>Download</DownloadButton>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

## Props

| Prop | Type | Default |
|---|---|---|
| `children` | `ReactNode` | `"Download"` |
| `meta` | `ReactNode` | — (secondary line under the label) |
| `href` | `string` | — (if provided, native anchor download) |
| `variant` | `outline \| solid \| secondary` | `outline` |
| `size` | `ButtonSize` | `md` |
| `onDownload` | `() => void \| Promise<void>` | — |

Plus all native `ButtonHTMLAttributes<HTMLButtonElement>`.

## Variants

outline (default) · solid · secondary.

## Sizes

xs (28px) · sm (32px) · **md (36px, default)** · lg (40px) · xl (44px). Horizontal padding scales 8 → 20px; icons scale 14 → 20px.

## States

default · hover · focus-visible · working (spinner + `aria-busy`, disabled) · done (check icon) · disabled (reduced opacity).

## Accessibility

Renders a native `<button>`. Focus-visible ring uses `color.focus-ring`. Loading sets `aria-busy` and disables to prevent double-submit. Disabled never removes the affordance (reduced opacity, not hidden). Meets the 44px touch target at lg/xl. `aria-busy` reflects the working state. The label changes ("Downloading…") to convey progress beyond the spinner.

## Styling

Tailwind classes are included directly in the component and consume the DevSnips semantic design tokens (`--ds-*`) via arbitrary values. The button themes with the surface automatically in light and dark mode. No component-specific CSS file is needed.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This button uses the semantic color, radius, and motion tokens; define them once in your project theme and every button in the family stays in sync.

## Notes

For multiple export targets, use ExportButton. DownloadButton is for a single file with progress feedback.
