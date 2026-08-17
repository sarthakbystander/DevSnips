# Download Button

Direct download trigger with working and done states plus optional file metadata.

## Usage

```jsx
<DownloadButton meta="CSV · 2.4 MB" onDownload={fetchBlob}>Download report</DownloadButton>
```

## Props

`children` · `meta` (file metadata shown under the label) · `href` · `variant` (outline|solid|secondary) · `size` · `onDownload` (may return a Promise)

## Variants

outline (default) · solid · secondary.

## Sizes

sm · **md (default)**.

## States

default · hover · **working** (spinner + 'Downloading…' + `aria-busy` + disabled) · **done** (check + 'Downloaded', reverts after 2s) · focus-visible.

## Accessibility

`aria-busy` while working. State conveyed by icon + label change, not color alone. `meta` is visible text so screen readers announce the file details.

## Behavior

Fires `onDownload` (wire to a real fetch/blob URL) and surfaces working → done → idle. Layout preserved because the spinner occupies the icon slot.

## Design Tokens

Motion (spinner), Iconography (download, check), Sizing, Color, States (§15).

## Notes

For multiple formats, use ExportButton. `meta` improves perceived quality — show format and size where known.
