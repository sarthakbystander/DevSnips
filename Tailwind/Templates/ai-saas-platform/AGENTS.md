# Agent Instructions — AI SaaS Platform

Guidance for an AI coding agent working with this template. Read this before modifying.

## What this template is

A premium, production-ready multi-page website template for an AI SaaS startup called **Nexus AI**. Built with Tailwind CSS only (via CDN), vanilla HTML, and scoped vanilla JavaScript. No frameworks, no build step.

Contains 11 pages: landing page, features, integrations, pricing, customers, blog, blog post, docs, login, signup, and dashboard.

## Design language

Quiet, editorial, light-mode-first design:
- Warm paper background (`#F9F7F4`) with refined neutral ink ramp (`#1C1917` → `#78716C`)
- Single terracotta accent (`#E07A5F` / `#C85D42`) — used sparingly for CTAs, active states, emphasis
- Fraunces (display serif) + Inter (body) typography
- White cards, 1px hairline borders, restrained soft shadows — no gradients as primary visual language
- Subtle scroll-reveal, marquee, and float animations (all `prefers-reduced-motion` safe)

## File layout

```
ai-saas-platform/
├── pages/
│   ├── index.html          # Landing page
│   ├── features.html       # Feature pages
│   ├── integrations.html   # Integrations page
│   ├── pricing.html        # Pricing page
│   ├── customers.html      # Customers page
│   ├── blog.html           # Blog listing
│   ├── blog-post.html      # Blog article
│   ├── docs.html           # Documentation layout
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   └── dashboard.html      # App UI dashboard
├── components/
│   ├── navbar.html         # Sticky navbar + mobile menu
│   ├── footer.html         # Footer with links
│   ├── buttons.html        # Button system
│   └── reusable-ui.html    # Reusable UI patterns
├── assets/
│   ├── icons/              # SVG icons
│   ├── images/             # Mockups and illustrations
│   ├── illustrations/      # Decorative illustrations
│   └── placeholders/       # Placeholder images
├── preview.html            # Template gallery/index
├── metadata.json
└── README.md
```

## How to adapt it

1. **Swap branding**: Update the brand name "Nexus AI" throughout all pages; replace logo in `assets/icons/logo.svg`
2. **Rebrand colors**: Modify the terracotta accent color values in the inline styles or add custom CSS classes
3. **Edit content**: Replace placeholder copy in each page's HTML with actual content
4. **Add/remove pages**: Add new HTML files to `pages/` directory; update navigation links accordingly
5. **Customize components**: Edit component files in `components/` to match desired UI patterns

## Key patterns

- **Scroll-reveal animations**: Elements with reveal classes animate on scroll; respect `prefers-reduced-motion`
- **Mobile menu**: Scoped vanilla JS handles mobile navigation toggle
- **Accordion FAQ**: CSS-grid animation with ARIA attributes and keyboard support
- **Billing toggle**: JavaScript-powered monthly/yearly pricing toggle on pricing page
- **Dashboard charts**: SVG-based chart mockups in dashboard

## Do not

- Do not introduce a build step or framework unless explicitly required
- Do not add additional external dependencies beyond Tailwind CDN
- Do not remove the `prefers-reduced-motion` guards from animations
- Do not change the warm paper background to dark mode (this is a light-mode-first template)

## Quality bar

- Semantic HTML with proper heading hierarchy
- ARIA attributes on interactive elements (accordion, mobile menu)
- Visible focus states on all interactive elements
- `prefers-reduced-motion` support for all animations
- Responsive design from 320px to 1920px+

## Gotchas

- Dashboard page contains chart mockups using SVG — these are static visuals, not live charts
- Docs page has a sidebar navigation that is statically rendered
- Blog post page is a template — update author info and related articles when using
