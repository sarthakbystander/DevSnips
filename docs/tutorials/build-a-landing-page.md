# Build a landing page

Compose several sections into a coherent landing page. This tutorial assembles a typical SaaS landing (nav, hero, features, pricing, testimonials, footer) from DevSnips sections.

## 1. Pick one technology and one style

Consistency matters more than variety. Choose the technology that matches your stack, then one visual style (e.g. Tailwind `vercel` or Vanilla `minimal`) so every section shares the same design language.

```bash
npx devsnips init
```

## 2. Install the sections

Install each section you need. Example (Tailwind, one style):

```bash
npx devsnips add Tailwind/Sections/Navbar/<variant>
npx devsnips add Tailwind/Sections/Hero/<variant>
npx devsnips add Tailwind/Sections/Features/<variant>
npx devsnips add Tailwind/Sections/Pricing/<variant>
npx devsnips add Tailwind/Sections/Testimonials/<variant>
npx devsnips add Tailwind/Sections/Footer/<variant>
```

Replace `<variant>` with a real style name from the registry (query it first — see [Machine-readable overview](../machine-readable/overview.md)). Each lands under `./devsnips/tailwind/sections/<family>/<variant>/`.

## 3. Compose the page

Each section's `code.html` is a self-contained snippet. Stack them in a single page:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My Product</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts the chosen style needs -->
</head>
<body class="antialiased">
  <!-- paste Navbar code.html -->
  <main>
    <!-- paste Hero code.html -->
    <!-- paste Features code.html -->
    <!-- paste Pricing code.html -->
    <!-- paste Testimonials code.html -->
  </main>
  <!-- paste Footer code.html -->
</body>
</html>
```

Rules:

- Keep the chosen style's font `<link>` tags in the `<head>` (each `preview.html` shows which fonts to load).
- Do not merge two different style systems on one page — sections are designed to be visually distinct per style.
- The snippets scope their JS to their own root (`document.currentScript.closest('[data-<scope>]')`), so multiple snippets on one page do not collide.

## 4. Verify

- No horizontal overflow at mobile width (~360px).
- Focus is visible and keyboard operable.
- `prefers-reduced-motion` is respected on animated sections.

Run the QA gates if you edit the composed page further — see [QA](../qa/overview.md).

## Go deeper

- [Sections](../resources/sections.md) — the section type per technology.
- [Install & customize](install-and-customize.md) — adapting a single section.
- [Technologies](../resources/technologies.md) — choosing Tailwind vs React vs Vanilla.
