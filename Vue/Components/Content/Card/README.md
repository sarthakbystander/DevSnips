# Card

A minimal, responsive content surface for Vue 3 applications.

## Features

- Vue 3 single-file component
- Optional media slot
- Optional action/content slot
- Can render as an `article` or link
- Mobile-first responsive layout
- Light/dark theme support
- Visible keyboard focus state
- No runtime dependencies

## Props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | `string` | — | Card heading |
| `description` | `string` | — | Supporting text |
| `href` | `string` | — | Renders the card as an anchor when supplied |

## Slots

- `media` — optional media area
- default — optional actions or additional content

## Responsive behavior

The component uses a fluid width and spacing system so it can sit inside one-column mobile layouts or wider grid layouts without requiring breakpoint-specific markup.
