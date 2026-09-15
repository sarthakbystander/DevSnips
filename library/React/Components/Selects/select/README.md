# Select

Custom accessible select implementing the WAI-ARIA combobox/listbox pattern with full keyboard navigation.

## Usage

```tsx
import { Select } from './code';

<Select label="Environment" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="production" />
```

## JavaScript

A `code.jsx` build is provided for projects that ship plain JSX. It exposes the same API and behavior as `code.tsx` — only the TypeScript types are removed.

```jsx
import { Select } from './code';

<Select label="Environment" options={[{value:"production",label:"Production"},{value:"staging",label:"Staging"},{value:"development",label:"Development"}]} defaultValue="production" />
```

## Props

| Name | Type | Default | Description |
|---|---|---:|---|
| `label` | `string` | `"Select"` | Visible label. |
| `options` | `{value,label,disabled?}[]` | — | Option list. |
| `value` / `defaultValue` | `string` | `""` | Controlled / uncontrolled value. |
| `onChange` | `(value, option) => void` | — | Selection callback. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Control height. |
| `placeholder` | `string` | `"Select an option"` | Placeholder text. |
| `disabled` | `boolean` | — | Disables the trigger. |
| `leadingIcon` | `ReactNode` | — | Icon at the trigger left. |
| `error` / `success` / `helperText` | `string` | — | Message + state. |

## Behavior

Click the trigger (or focus + ArrowDown) to open the listbox. ArrowUp/Down moves the active option (skipping disabled), Home/End jump to the first/last enabled option, Enter/Space selects, Escape closes, Tab closes. Selecting closes the panel and returns focus to the trigger. Controlled (`value`/`onChange`) and uncontrolled (`defaultValue`) modes both supported.

## Accessibility

Trigger `<button aria-haspopup="listbox" aria-expanded aria-controls aria-activedescendant>`; panel `role="listbox"`; options `role="option" aria-selected`. `aria-invalid` for errors, `aria-describedby` for helper/error/success text. Outside-click and Escape close. Visible `focus-visible` ring.

## Styling

Built with React, Tailwind CSS, and DevSnips design tokens. The component consumes the `--ds-*` semantic tokens via arbitrary values (for example `bg-[var(--ds-color-input)]`). Define the tokens once in your theme — no component-specific CSS file is required.

## Design Tokens

See [React/DESIGN_TOKENS.md](../../DESIGN_TOKENS.md) for the authoritative token specification. This select uses the semantic color, radius, spacing, and motion tokens.

## Notes

This is the reference implementation for the Selects family — it establishes the shared dimensions, border, radius, focus treatment, dropdown panel, option spacing, selected/hover/disabled states, and dark-mode behavior that every other select extends.
