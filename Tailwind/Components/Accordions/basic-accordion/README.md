# Basic Accordion

Simple documentation-style accordion with chevron rotation and smooth height animation via CSS grid. Each item toggles independently. Useful for knowledge bases, docs pages, FAQs, and any collapsible content list.

## Preview

The preview demonstrates three independent accordion items with typical documentation questions. Clicking a trigger expands/collapses its panel with a 300ms ease-out transition and rotates the chevron.

## Features

- Independent item toggles (multiple can be open)
- Chevron rotation on open/close
- Smooth height animation using `grid-rows-[0fr]` / `grid-rows-[1fr]`
- Focus-visible rings on triggers
- Proper ARIA: `aria-expanded`, `aria-controls`, `role="region"`, `aria-labelledby`
- Semantic headings (`h3`) wrapping each trigger button
- Minimal visual style: divide-y borders, muted text

## Usage

```bash
npx devsnips add Tailwind/Components/Accordions/basic-accordion
```

This installs the component files into your project. Copy the markup from `code.html` into any page that has Tailwind CSS available. The inline `<script>` initializes the toggles for the nearest `[data-accordion]` root; no external JS libraries are required.

## Customization

- **Colors**: Change `text-gray-900`, `text-gray-600`, `divide-gray-200`, `border-gray-200`, and the focus ring color (`ring-blue-500`).
- **Spacing**: Adjust `py-4`, `pb-4`, `gap-4`, `pr-8`.
- **Typography**: Modify `text-sm`, `font-medium`, `leading-relaxed`.
- **Animation**: The duration/easing lives on `.accordion-panel` (`duration-300 ease-out`) and the chevron `transition-transform`.
- **Borders**: The outer `border-y` and item `divide-y` can be removed or restyled.

## Accessibility

- Triggers are real `<button type="button">` elements inside `<h3>` headings.
- Each panel is a `role="region"` with `aria-labelledby` pointing to its trigger.
- `aria-expanded` is toggled by the script.
- Focus-visible rings provide a clear keyboard focus indicator.
- Chevron SVG is marked `aria-hidden="true"`.

## Responsive Behavior

Fluid width (`w-full`). Text wraps naturally. No special breakpoint classes; the layout remains a vertical stack at all viewport sizes.

## Dependencies

- Tailwind CSS (utility classes)
- No external JavaScript libraries
- No icon libraries (inline SVG)
- No fonts beyond the page default

Dependency-free beyond Tailwind.

## File Structure

- `code.html` — copy/paste component snippet (includes the small initialization script)
- `preview.html` — standalone preview/demo page
- `metadata.json` — component metadata
- `README.md` — this documentation

## Notes

- The script scopes itself to the nearest `[data-accordion]` ancestor so multiple instances can coexist on a page.
- Animation relies on the modern `grid-template-rows` transition; older browsers without support will simply snap open/closed.
- Content inside panels should not rely on the panel being visible for layout calculations during the closed state.
