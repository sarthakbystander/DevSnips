# Job Board Template (Vanilla)

A dense, structured **developer job-board** template built for DevSnips with
semantic HTML, CSS, and vanilla JavaScript. The template is split into modular
files — `code.html` (HTML structure) + `style.css` (the design system) +
`script.js` (all views, rendering, filtering, pagination, save/apply, and
interactions) — with `preview.html` as a self-contained single-file preview of
the UI so you can open it directly and see exactly how the template looks.

**Technology:** vanilla
**Category:** templates
**Subcategory:** job-board
**Type:** single-page (one-page job-board application with view switching)

## Files

```
Job Board/
├── code.html               # HTML structure (links style.css + script.js) — the modular source
├── style.css               # the design system (DevSnips --ds-* tokens + Job Board template tokens)
├── script.js               # views, rendering, search, filters, pagination, save/apply, mobile nav + drawer (vanilla JS, no deps)
├── preview.html            # single-file preview of the UI (inlines style.css + script.js) — open this to see it
├── metadata.json           # DevSnips registration metadata
└── README.md               # This file
```

No `assets/` directory is required. The template uses no local images, icons,
or fonts. Company logos are rendered as single-letter text avatars, status and
meta indicators use inline SVG and emoji, and the fonts (Inter and JetBrains
Mono) are loaded from Google Fonts (see **Dependencies**).

## Preview

Open `preview.html` directly in a browser to see the template — it is a
self-contained single-file preview that inlines the CSS and JS:

```bash
cd "Vanilla/Templates/Job Board"
python3 -m http.server 8080
# visit http://localhost:8080/preview.html
```

For development and customization, work with the split files — open `code.html`
(which references `style.css` and `script.js` relatively) in the same served
folder. The whole template runs without a build step. The only external requests
are Google Fonts (Inter and JetBrains Mono), loaded from a CDN.

Per the shared `design-tokens.md` convention, the template folder contains
exactly **one** `preview.html`. It is the canonical preview shown by the DevSnips
website. It is fully responsive, uses the template's real CSS/JS, uses relative
paths, and loads correctly when opened directly.

### Architecture

The template is split into three modular files plus a single-file preview:

- **`code.html`** — the HTML shell (navigation, jobs view, job detail view,
  companies view, company detail view, saved jobs view, candidate area, apply
  modal, toast container, and mobile filter drawer) that links `style.css` and
  `script.js`. This is the modular source you customize.
- **`style.css`** — the entire design system: the DevSnips `--ds-*` shared token
  block (per `design-tokens.md`), the Job Board `--template-*` and original
  `--color-*` tokens mapped onto the shared layer, base/typography/button styles,
  every view and component style, the responsive breakpoints, the opt-in dark
  mode override, and the reduced-motion guard.
- **`script.js`** — the runtime: application data (10 companies, 24 jobs,
  applications), view state, render functions (job cards, job list, pagination,
  job detail, company directory, company detail, candidate tabs), search and
  filtering, save/apply, the apply modal, toasts, mobile nav, and the mobile
  filter drawer. No dependencies.
- **`preview.html`** — a self-contained single-file preview that inlines
  `style.css` and `script.js` into the `code.html` structure, so it can be opened
  directly with no build step and renders identically to the modular version.

## Views

The application is a single page that switches between these views (no page
reloads):

1. **Jobs** — the default view. A search bar (keyword search across title,
   skill, company, and location), location and job-type filter selects, category
   chips, a live result count, and a paginated job list (8 jobs per page).
2. **Job Detail** — full job posting with description, responsibilities,
   requirements, skills, and benefits, plus a company-info sidebar with an
   **Apply Now** button and a **Save Job** toggle, and a job-details sidebar.
3. **Companies** — a responsive auto-fill grid of company cards (logo, name,
   description, location, size, open positions).
4. **Company Detail** — company about, an info sidebar, and the list of open
   positions at that company.
5. **Saved Jobs** — the jobs the user has bookmarked, with an empty state when
   none are saved.
6. **Candidate** — a sidebar (avatar, name, role) with three tabs: **Profile**
   (candidate details and profile completion), **Applications** (a status table
   with badges), and **Saved Jobs**.

## Interactions

- **Search** — debounced keyword search (250ms) filtering across job title,
  company, skills, and location.
- **Filters** — location and job-type selects refine the list; category chips
  filter by role family.
- **Pagination** — prev/next and numbered page buttons; the list shows 8 jobs
  per page.
- **Save / Unsave** — bookmark any job from its card or the detail sidebar; a
  toast confirms the action and the saved view updates live.
- **Apply** — opens a scoped modal dialog (name, email, cover note) that records
  an application and shows a success toast.
- **Mobile nav** — below 768px the nav links collapse into a dropdown toggled by
  a hamburger button with `aria-expanded` state.
- **Mobile filter drawer** — below 768px the location/type filter selects move
  into a slide-in drawer with an overlay and an **Apply Filters** action;
  Escape and overlay click close it.
- **Toasts** — transient success and default notifications in the bottom-right.

## Design System

The template follows the shared `Vanilla/Templates/design-tokens.md`
specification. The `:root` block defines the DevSnips `--ds-*` token layer
(neutrals, blue accent, semantic status colors, typography, radius, shadow,
motion) and maps the template's original `--color-*` vocabulary onto those
tokens, so the visual output is preserved while the shared system remains the
source of truth. Template-specific tokens (`--template-nav-height`,
`--template-sidebar-width`, `--template-max-width`) extend the shared system.

## Customization

- **Content** — edit the `companies` and `jobs` arrays and the `applications`
  state at the top of `script.js` (or in the inlined block of `preview.html`).
  Each job carries title, company, location, salary, work mode, type,
  experience, posted time, skills, description, responsibilities, requirements,
  and benefits.
- **Theme** — adjust the `--ds-*` tokens in `style.css` (`:root`). Because the
  component styles consume the template's `--color-*` names (which map onto
  `--ds-*`), changing the shared tokens re-themes the whole board. The dark
  mode override lives in the `@media (prefers-color-scheme: dark)` block.
- **Branding** — the nav brand mark and wordmark live in the `.nav-brand` /
  `.nav-brand-icon` elements in `code.html`.
- **Page size** — change `pageSize` (default `8`) in `script.js` to alter how
  many jobs appear per page.

## Responsive Behavior

The layout adapts at four breakpoints:

- **≤ 1024px** — the job-detail two-column grid collapses to one column; the
  detail sidebar becomes a two-column grid; the candidate sidebar narrows.
- **≤ 768px** — nav links collapse into a dropdown menu; the candidate sidebar
  becomes a horizontal row; the company grid becomes a single column; the
  location/type filter selects hide and a **Filters** button opens the drawer.
- **≤ 640px** — the search bar compacts to a single-row search input plus the
  Filters button.
- **≤ 480px** — page and nav padding reduce; the search bar stacks vertically;
  the filter drawer goes full-width.

There is no horizontal overflow from 320px to 1920px.

## Accessibility

- Semantic landmarks (`nav`, the main container, `aside`, `section`).
- ARIA labels on navigation, the search input, filter selects, the modal dialog,
  and icon buttons; `aria-expanded` on the mobile nav toggle and menu.
- The apply modal uses `role="dialog"`, `aria-modal="true"`, and
  `aria-labelledby`; Escape and overlay-click close it.
- `role="list"` / `role="listitem"` on job listings.
- Visible `:focus-visible` outlines on all interactive controls.
- All controls are native `button`, `a`, `input`, `select`, or `textarea`, so
  they are keyboard-operable by default.
- `prefers-reduced-motion` disables animations and smooth scrolling.
- Status badges use text labels (not color alone) to convey application state.

## Dependencies

- Google Fonts — Inter (UI) and JetBrains Mono (monospace), loaded from a CDN.
  System font fallbacks are defined in the token stack, so the template remains
  usable without the font download.

No JavaScript libraries, build tools, or frameworks are used.

## Browser Support

Chrome, Firefox, Safari, and Edge (modern evergreen browsers). The template
uses standard HTML, CSS custom properties, and vanilla JavaScript (ES2015+).
