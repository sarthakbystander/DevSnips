# Bordered Accordion

Enterprise-style accordion that presents each section as a distinct bordered card with leading status icons, status chips, and metadata grids. Designed for compliance dashboards, admin panels, and structured data review interfaces where visual separation and status cues matter.

## Preview

The preview shows multiple self-contained accordion cards. Each card has a border, an icon, a status chip, and expandable content with metadata. Opening a card applies an open-state ring.

## Features

- Distinct bordered card treatment per item
- Leading status / accent icons
- Status chips for quick scanning
- Metadata grids inside panels
- Open-state ring feedback
- Focus-visible rings on triggers
- Independent or coordinated toggles (per implementation)
- Semantic structure with ARIA support where present in the markup

## Usage

```bash
npx devsnips add Tailwind/Components/Accordions/bordered-accordion
```

Copy the markup from `code.html` into a Tailwind project. Include any inline script that ships with the component for toggle behavior. No external JS libraries are required.

## Customization

- **Card chrome**: Adjust border color, radius, padding, and shadow classes on the item containers.
- **Status colors**: Update chip and icon color utilities (e.g. green/amber/red semantic tokens).
- **Typography**: Heading size/weight and body text classes inside panels.
- **Spacing**: Gap between cards and internal padding.
- **Focus / open states**: Ring color and width classes.

## Accessibility

- Triggers use native buttons with clear labels.
- Focus-visible rings are present for keyboard users.
- ARIA attributes (`aria-expanded`, `aria-controls`, regions) are used where the implementation includes them.
- Icons that are decorative should remain `aria-hidden`.

## Responsive Behavior

Cards stack vertically and remain full-width on small screens. Metadata grids reflow as the available width changes. No horizontal overflow at common breakpoints.

## Dependencies

- Tailwind CSS
- No external JavaScript libraries
- Inline SVG icons (no icon package required)

## File Structure

- `code.html` — copy/paste component snippet
- `preview.html` — standalone preview/demo
- `metadata.json` — component metadata
- `README.md` — this documentation

## Notes

- Prefer this variant when each accordion item needs strong visual separation and status communication.
- For a lighter documentation style, use the basic or minimal accordion variants instead.
