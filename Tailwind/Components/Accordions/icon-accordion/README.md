# Icon Accordion

Accordion with leading category icons in tinted squares and two-tone chevrons. Useful for help centers, product docs, and category-organized FAQs.

## Preview

Open `preview.html` for a standalone demonstration of this variant.

## Features

- Leading category icons in tinted squares
- Two-tone chevron indicators
- Independent or coordinated toggles
- ARIA state attributes
- Focus-visible rings
- Native button triggers

## Usage

```bash
npx devsnips add Tailwind/Components/Accordions/icon-accordion
```

Copy the markup from `code.html` into a page that includes Tailwind CSS. Keep the inline script for toggle behavior or adapt it to your own initialization.

## Customization

- Icon background / text color utilities
- Chevron colors and transition
- Spacing, typography, and border utilities
- Focus ring color

## Accessibility

- Native `<button>` triggers
- `aria-expanded` / `aria-controls` where present
- Focus-visible styles
- Decorative icons should stay `aria-hidden`

## Responsive Behavior

Fluid width; stacks naturally on small screens.

## Dependencies

- Tailwind CSS
- Small inline JavaScript (no external libraries)
- Inline SVGs

## File Structure

- `code.html` — copy/paste snippet
- `preview.html` — standalone demo
- `metadata.json` — metadata
- `README.md` — this file
