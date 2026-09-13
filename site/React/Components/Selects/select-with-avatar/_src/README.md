# Select With Avatar

Custom select where each option may carry an avatar shown in trigger and rows.

## Usage

```tsx
import { SelectWithAvatar } from './code';

<SelectWithAvatar label="Assignee" options={[{value:"sarthak",label:"Sarthak",avatar:<Avatar/>}]} />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { SelectWithAvatar } from './code';

<SelectWithAvatar label="Assignee" options={[{value:"sarthak",label:"Sarthak",avatar:<Avatar/>}]} />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `options` | `{value,label,avatar?:ReactNode,description?,disabled?}[]` | — | Options with optional avatar. |
| `value` / `defaultValue` / `onChange` / `size` / `placeholder` / `label` | — | — | Standard. |

## Behavior

The selected option's avatar + label show in the trigger. Option rows show the avatar + label (+ optional description). Avatar slot is a 20px circle; a fallback initials square renders when no avatar is supplied.

## Accessibility

Avatars are decorative (`aria-hidden`); the option label carries the accessible name.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

Does not require an external avatar library — pass any ReactNode (image, initials, icon).
