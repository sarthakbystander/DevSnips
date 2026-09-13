# Datetime Input

Native date-time input using datetime-local semantics.

## Usage

```tsx
import { DatetimeInput } from './code';

<DatetimeInput label="Workspace name" placeholder="Acme design" />
```

## JavaScript

```jsx
import { DatetimeInput } from './code';

<DatetimeInput label="Billing email" placeholder="billing@example.com" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | component label | Visible label associated with the input. |
| `helperText` | `string` | `undefined` | Supporting text announced through `aria-describedby`. |
| `error` | `string` | `undefined` | Error message; sets `aria-invalid`. |
| `success` | `string` | `undefined` | Success message associated with the control. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Control height and text sizing. |
| `tone` | `"default" \| "error" \| "success"` | `"default"` | Visual state when no message prop overrides it. |
| `className` | `string` | `undefined` | Adds layout classes to the input element. |
| native input props | `InputHTMLAttributes<HTMLInputElement>` | — | Supports `value`, `defaultValue`, `onChange`, `name`, `id`, `placeholder`, `disabled`, `readOnly`, `required`, and `aria-*`. |

## States

Supports default, hover, focus-visible, disabled, readonly, error, success, and loading where applicable.

## Accessibility

Uses a native `input`, a visible `label`, associated helper/error text, `aria-invalid` for errors, and keyboard-accessible buttons for interactive controls.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. No component-specific CSS file is required.

## Design Tokens

Visual decisions reference `React/DESIGN_TOKENS.md` rather than duplicating the token system.
