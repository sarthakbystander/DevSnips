# Button With Icon

Labeled button composition with a leading or trailing icon.

## Usage

```jsx
<ButtonWithIcon icon="download" iconPosition="leading" variant="outline">Download CSV</ButtonWithIcon>
```

## Props

`children` · `icon` (icon key) · `iconPosition` (leading|trailing, default leading) · `variant` · `size` · `disabled` · `onClick`

## Variants

solid · outline · secondary · ghost via `variant`.

## Sizes

sm · **md (default)** · lg · xl.

## States

default · hover · active · focus-visible · disabled.

## Accessibility

Icon is `aria-hidden`; the label provides the accessible name. Focus ring present.

## Behavior

Demonstrates the icon + label composition rules: 8px gap, icon sized to the button's size token, optical alignment via flex centering.

## Design Tokens

Iconography (size scales with button size), Spacing (`control-gap` 8px), Sizing, Color.

## Notes

Use leading icons for actions (New, Download) and trailing for direction/external (Continue, Open docs). Don't add decorative icons.
