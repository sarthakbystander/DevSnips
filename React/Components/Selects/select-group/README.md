# Select Group

Layout wrapper that groups multiple related selects with consistent spacing.

## Usage

```tsx
import { SelectGroup } from './code';

<SelectGroup label="Location"><Select .../><Select .../></SelectGroup>
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectGroup } from './code';

<SelectGroup label="Location"><Select .../><Select .../></SelectGroup>
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Group"` | Group legend. |
| `children` | `ReactNode` | — | The selects to lay out. |
| `direction` | `"row" \| "column"` | `"column"` | Layout direction. |
| `className` | `string` | — | Extra classes. |

## Behavior

Renders a semantic `<fieldset><legend>` and arranges child selects in a column (`flex-col gap-4`) or responsive row grid (`grid gap-4`, 1 to 2 to 3 cols). It does NOT reimplement the select — it is a layout wrapper.

## Accessibility

`<fieldset><legend>` provides an accessible group label for the contained controls.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Use to keep alignment and spacing consistent across related selects (e.g. Country / Region / City).
