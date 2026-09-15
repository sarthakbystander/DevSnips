# AGENTS.md — SPRAY Art School

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A four-page **React + TypeScript** template for **SPRAY**,a fictional street-art school where beginners learn graffiti, sketching, muralism,and stencil work from working artists. The template ships the full Vite project with **zero image assets** — every artwork slot is a labeled gradient placeholder,so it renders correctly out of the box. Built with React 18, TypeScript, Tailwind CSS, react-router-dom,and Framer Motion,bundled by Vite.



## Design system

**Raw DIY-zine street art** — a deliberate anti-gallery aesthetic: **Anton**(condensed display, tight tracking) for headlines + **Space Grotesk**(body, 400–700)for copy; palette ink-black `#0a0a0f` surfaces, ink-navy panels, bone `#f2f0e6` text, one neon-green `#39FF14` primary accent + hot-pink `#ff2ec4` secondary accent; texture via torn-paper dividers(`TornDivider.tsx`),hanging spray-splatter SVG blobs(`SplatterDecoration.tsx`),a subtle fixed film-grain noise overlay,and clip-path spray-button silhouettes(`Button.tsx`). Motion:restrained Framer Motion reveals on headlines, cards,and roadmap steps(reduced-motion friendly. The visual system lives entirely in `tailwind.config.ts` (colors, fonts, keyframes), `src/styles/globals.css`,and the presentational components — it does not depend on the shared DevSnips `--ds-*` tokens.



## File layout

```
spray-art-school/
├── index.html                 # Vite entry (theme-color, root mount)
├── preview.html               # Self-contained static preview of the whole site (open directly)
├── package.json               # React 18, React Router 6, Framer Motion 11, Vite 5
├── tailwind.config.ts         # colors, fonts, animation keyframes
├── postcss.config.js
├── tsconfig.json              # strict TypeScript
└── src/
    ├── main.tsx              # BrowserRouter + StrictMode mount
    ├── App.tsx               # Navbar + routed pages + noise overlay
    ├── components/           # Navbar, Button, Logo, Badge, ProjectCard, ServiceCard,
    │                            SectionHeading, TornDivider, SplatterDecoration
    ├── sections/              # Hero, SelectedWork, Services, About, Process,
    │                            Testimonials, CTA, Footer
    ├── pages/                # Home, Work, About, Contact
    ├── data/                 # Typed content arrays: projects, services, testimonials
    └── styles/
        └── globals.css        # Google Fonts, Tailwind layers, noise texture, clip-paths
```

Routes: `/` Home(Hero, Selected Work, Courses( Services), About, Roadmap( Process), Testimonials, CTA, Footer), `/work` Work(archive), `/about` About( Roadmap, Testimonials, CTA, Footer}, `/contact` Contact(labelled form with validation + success state.



## How to adapt it

1. **Swap the school**: edit the typed content arrays in `src/data/` (projects, services, testimonials) — card copy never lives in the components themselves.
2. **Re-theme**: colors, fonts,and keyframes are defined once in `tailwind.config.ts` + `src/styles/globals.css`;swapping the palette re-colors every section consistently..
3. **Add a page**: create a `src/pages/*.tsx` route, compose existing sections,and register it in `src/App.tsx`.
4. **Real artwork**: drop image files into `src/assets/images/` and replace the placeholder blocks in `ProjectCard.tsx` with `<img>` tags when ready..
5. **Run the app**: `npm install` → `npm run dev` (dev server); `npm run build` (tsc + Vite production build→ `dist/`,then `npm run preview`.



## Do not

- Do not introduce a state-management library or extra runtime dependencies—the template deliberately has zero beyond React, React Router,and Framer Motion..
- Do not remove the `aria-hidden` treatment on decorative splatters/torn dividers or the `role="status"` success state on the contact form..
- Do not change the gradient-placeholder artwork slots into broken `<img>` tags without adding real asset files.



## Quality bar

Semantic landmarks(`header`, `main`, `section`, `footer`, `nav`, `form`), single `h1` per page, descriptive `h2` section headings with eyebrows, mobile menu `aria-expanded`, form labels via `htmlFor`/`id`, `role="status"` success message, global `:focus-visible` dashed outline, `prefers-reduced-motion` resolves Framer Motion transitions instantly. Run `npm run build` (strict `tsc` type-check) and `python3 scripts/validate.py` after changes.

