# Copy Button

Clipboard copy control with transient check and Copied feedback.

## Usage

```jsx
<CopyButton value={projectId} />
```

## Props

`value` (string to copy) · `label` (default 'Copy') · `copiedLabel` (default 'Copied') · `size` · `variant` · `resetMs` (default 2000) · `onCopy(value)`

## Variants

outline (default) · secondary · ghost · solid.

## Sizes

**sm (default)** · md.

## States

default · hover · **copied** (check + 'Copied' + `aria-live` announcement, reverts after `resetMs`) · focus-visible.

## Accessibility

Uses the async Clipboard API with an `execCommand` fallback. `aria-live` region announces 'Copied'. Icon + label change confirm success without relying on color. `aria-label` includes the value being copied.

## Behavior

Copies `value` to the clipboard and shows transient confirmation. Gracefully degrades when the Clipboard API is unavailable (older browsers, insecure contexts).

## Design Tokens

Motion (state transition), Iconography (copy, check), Sizing, Color.

## Notes

Always pair with the value displayed nearby (a code/ID row) so the copy target is unambiguous.
