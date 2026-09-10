# Dark Accordion

Modern dark-mode dashboard accordion with single-open behavior, glowing status dots, metric delta badges, and an indigo active accent. Built for analytics and admin panels.

## Preview

Open `preview.html` for a standalone demonstration of this variant. The preview includes Tailwind CDN setup and sample content so you can evaluate layout, interaction, and styling without integrating the snippet first.

## Features

- single-open behavior
- dark surface styling
- status dots / metric badges
- indigo active accent
- ARIA state attributes (`aria-expanded` / `aria-controls`)
- Native interactive elements (`<button>` etc.)
- CSS transitions / animations
- Visible focus states

## Usage

```bash
npx devsnips add Tailwind/Components/Accordions/dark-accordion
```

Copy the markup from `code.html` into a page that already includes Tailwind CSS.
A small inline `<script>` ships with the component to wire up its interactive behavior. Keep it next to the markup or migrate the logic into your own bundle while preserving the same ARIA and class toggles.

## Customization

Styling is entirely Tailwind utility classes in `code.html`. Typical edit points:

- **Colors** — `bg-*`, `text-*`, `border-*`, `ring-*`, accent colors for active/status states
- **Spacing** — `p-*`, `m-*`, `gap-*`
- **Typography** — `text-*`, `font-*`, `leading-*`
- **Borders & radius** — `border`, `rounded-*`
- **Motion** — `transition-*`, `duration-*`

## Accessibility

- Interactive controls use native `<button>` elements.
- Focus-visible styles are present.
- `aria-expanded` and `aria-controls` communicate state.
- Decorative icons should remain `aria-hidden="true"`.

## Responsive Behavior

Primarily fluid width; content stacks or flows naturally across viewports.

## Dependencies

- Tailwind CSS (required)
- Small inline JavaScript (no external JS libraries)
- Inline SVGs when icons are used

## File Structure

- `code.html` — copy/paste component snippet
- `preview.html` — standalone preview/demo
- `metadata.json` — name, slug, tags, features
- `README.md` — this file

## Notes

Prefer this variant for dark admin/analytics UIs. Pair with light variants when the page supports theme switching.
