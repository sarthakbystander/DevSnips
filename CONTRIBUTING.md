# 🤝 Contributing to DevSnips

Thanks for helping improve **DevSnips**! This repository is a lightweight collection of framework-free frontend snippets.

## Contribution flow

1. Fork the repository.
2. Create a descriptive branch, for example `feat/toast-snippet`.
3. Add or update snippets in the right family folder:
   - `Tailwind/Components/<Family>/<variant-slug>/` — Tailwind components
   - `Vanilla/Components/<Family>/<variant-slug>/` — Vanilla HTML/CSS/JS components (former Neo-Brutalist website sections are now merged here)
4. Every Tailwind component variant folder contains exactly three files: `code.html` (component only), `preview.html` (full page with Tailwind CDN + app context), and `metadata.json` (see the schema in `COMPONENT_STRUCTURE.md`). Vanilla component variant folders contain a self-contained `<slug>.html`, `metadata.json`, and `README.md`.
5. Update `snippets-index.json` when you add/remove snippets — add the family to `families[]`, list it under `technologies[].families`, and recompute `stats` (or run `python3 -m _gen.rebuild_index`).
6. Run `python3 scripts/validate.py` and open a PR.

## Code style rules

- Use **2-space indentation** for HTML, CSS, and JS.
- Keep snippets focused on one idea/component.
- Use semantic HTML (`main`, `section`, `button`, etc.) where applicable.
- Include accessibility support (labels, ARIA attributes, keyboard-friendly behavior).
- Prefer modern JavaScript (`const`/`let`, arrow functions, array methods).
- Avoid external dependencies unless absolutely necessary.

## Standard snippet comment header

Use this header at the top of every snippet file.

### HTML

```html
<!--
Snippet Name: <name>
Description: <one-line purpose>
Author: <github handle or DevSnips Contributors>
Usage Example: <short usage instruction>
-->
```

### CSS

```css
/*
Snippet Name: <name>
Description: <one-line purpose>
Author: <github handle or DevSnips Contributors>
Usage Example: <short usage instruction>
*/
```

### JavaScript

```js
/**
 * Snippet Name: <name>
 * Description: <one-line purpose>
 * Author: <github handle or DevSnips Contributors>
 * Usage Example: <short usage instruction>
 */
```

## Contributor checklist

- [ ] Snippet includes the standard comment header.
- [ ] Snippet follows 2-space indentation.
- [ ] HTML snippets include `<!DOCTYPE html>`, `lang`, `charset`, and viewport meta.
- [ ] Accessibility has been reviewed (semantic tags + ARIA where needed).
- [ ] JavaScript uses `const`/`let` and modern syntax.
- [ ] Snippet added to `snippets-index.json`.
- [ ] Tested in at least two modern browsers.
