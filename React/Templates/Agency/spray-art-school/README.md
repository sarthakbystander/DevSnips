# SPRAY — Art School Template

A four-page React + TypeScript template for **SPRAY**, a fictional street-art school where beginners learn graffiti, sketching, muralism, and stencil work from working artists. No clean corners, no boring classrooms.

Built with React, TypeScript, Tailwind CSS, react-router-dom, and Framer Motion, bundled by Vite. The template ships with **zero image assets** — every artwork slot is a labeled gradient placeholder, so it renders correctly out of the box.

## Design direction

**Raw DIY-zine street art** — a deliberate anti-gallery aesthetic:

- **Type:** Anton (condensed display, tight tracking) for headlines; Space Grotesk (body, 400–700) for copy.
- **Palette:** ink-black `#0a0a0f` surfaces, ink-navy panels, bone `#f2f0e6` text, one neon-green `#39FF14` primary accent, hot-pink `#ff2ec4` secondary accent.
- **Texture:** torn-paper divider strips (`TornDivider.tsx`), hanging spray-splatter SVG blobs (`SplatterDecoration.tsx`), a subtle fixed film-grain noise overlay, and clip-path spray-button silhouettes (`Button.tsx`).
- **Motion:** restrained Framer Motion reveals on headlines, cards, and roadmap steps; splatter blobs idle-float and torn strips drift.
- **Composition:** rotated cards and badges, an oversized `clamp()`-scaled headline, numbered roadmap only where the sequence is real (enroll → sketch → wall time → critique → show).

The visual system lives entirely in `tailwind.config.ts` (colors, fonts, keyframes), `src/styles/globals.css`, and the presentational components — it does not depend on the shared DevSnips `--ds-*` tokens.



## Pages

| Route | File | Composition |
| --- | --- | --- |
| `/` | `src/pages/Home.tsx` | Hero, Selected Work, Courses, About, Roadmap, Testimonials, CTA, Footer |
| `/work` | `src/pages/Work.tsx` | Section heading + full Selected Work archive, CTA, Footer |
| `/about` | `src/pages/About.tsx` | About, Roadmap, Testimonials, CTA, Footer |
| `/contact` | `src/pages/Contact.tsx` | Labelled contact form with validation + success state, Footer |

## Structure

```text
spray-art-school/
├── index.html                 # Vite entry (theme-color, root mount)
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

## Setup & run

Requires Node.js + npm. From the template root:

```bash
npm install
npm run dev        # Vite dev server — open the printed URL (usually http://localhost:5173)
```

Production build + local preview:

```bash
npm run build      # tsc type-check + Vite production build → dist/
npm run preview     # serve the built app
```

## Sections & components

- **Navbar** — sticky header that gains a blurred ink backdrop on scroll; mobile menu toggles `aria-expanded` and swaps ☰/✕ icons; Sign-up CTA.
- **Hero** — oversized clamp()-scaled “ART / SCHOOL” display, torn divider, lede, spray CTA, floating splatters.

- **SelectedWork** — responsive grid of rotated student-piece cards (gradient placeholder, category badge, student + year).
- **Services** — five course cards with bullets and schedule metadata (Basics, Sketching, Muralism, Stencils, Freedom).
- **About** — oversized manifesto pull-copy with neon/pink emphasis words, splat decoration.

- **Process** — five-step numbered roadmap (Enroll → Sketch → Wall time → Critique → Show) on a vertical/horizontal timeline.

- **Testimonials** — three rotated quote cards with student name + course.
- **CTA** — centered display call-to-action with spray Button..
- **Footer** — logo, social links, auto-year copyright.
- **Contact page** — labelled Name/Email/Message form with native required validation; submit swaps to a `role="status"` success message.



## Customization

- **Content:** edit the typed arrays in `src/data/` (projects, services, testimonials) — card copy never lives in the components themselves.
- **Re-theme:** colors, fonts, and keyframes are defined once in `tailwind.config.ts` and the base styles in `src/styles/globals.css`; swapping the palette re-colors every section consistently.


- **Real artwork:** drop image files into `src/assets/images/`and replace the placeholder blocks in `ProjectCard.tsx` with `<img>` tags when ready. The scaffold intentionally ships asset-free so it always renders without broken images.
- **Add a page:** create a `src/pages/*.tsx` route, compose existing sections, and register it in `src/App.tsx`.



## Accessibility

- Semantic landmarks (`header`, `main`, `section`, `footer`, `nav`, `form`).
- Single `h1` per page; descriptive `h2` section headings with eyebrows..
- Mobile menu wired with `aria-expanded`; contact form labels tied via `htmlFor`/`id`; the success message uses `role="status"`.
- Global `:focus-visible` dashed outline; decorative SVGs (`SplatterDecoration`, `TornDivider`) are `aria-hidden`.
- Reduced-motion: Framer Motion transitions resolve instantly under `prefers-reduced-motion`; CSS animations are purely cosmetic, and the noise overlay is static.



## Browser support

Modern evergreen browsers (Chrome, Firefox, Safari, Edge). Requires JS for routing and animations; no legacy-IE support.