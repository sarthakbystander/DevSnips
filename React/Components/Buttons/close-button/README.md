# Close Button

Icon-only dismiss control for dialogs, drawers, toasts, and banners.

## Usage

```jsx
<CloseButton size="sm" onClick={close} />  // inside a dialog
```

## Props

`label` (default 'Close', used as `aria-label`) · `size` · `variant` (ghost|outline) · `disabled` · `onClick`

## Variants

ghost (default) · outline.

## Sizes

sm · **md (default)**.

## States

default · hover · focus-visible · disabled.

## Accessibility

Icon-only — `aria-label` defaults to 'Close'. Focus ring present. Pair with Escape handling on the owning surface so keyboard users can dismiss without focusing the button.

## Behavior

Dismisses a surface (dialog, drawer, toast, banner). The owning component should also close on Escape and backdrop click.

## Design Tokens

Iconography (X), Sizing, Color, Radius.

## Notes

Always wire Escape on the parent overlay. A close button alone is not sufficient keyboard dismissal.
