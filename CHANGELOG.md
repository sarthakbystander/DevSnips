# Changelog

## 2026-08-23

### Changed — Vanilla architecture: three first-class content types (Components + Sections + Templates)
- **Split `Vanilla/Components/` into `Vanilla/Components/` + `Vanilla/Sections/`**, mirroring the Tailwind three-type architecture. The 65 neo-brutalist website sections moved to `Vanilla/Sections/`: 15 families moved wholesale (Hero 10, Features 5, Logos 3, Statistics 3, Products 6, Pricing 4, Testimonials 4, Team 3, Process 4, Content 4, Gallery 3, FAQ 2, CTA 4, Contact 3, Footer 3) plus Navigation's 4 section variants (`navbar-simple`, `navbar-sticky`, `navbar-mega-menu`, `sidebar-navigation`). `Vanilla/Components/Navigation/` keeps the legacy navigation sub-families (Breadcrumb/Menu/Navbar/Other/Pagination/Sidebar + `scroll-to-top`).
- **Galleries moved** to `Vanilla/Sections/`: `sections-index.html`, `sections-showcase.html`, `sections-gallery.README.md`. Fixed pre-existing broken cross-links (`showcase.html` → `sections-showcase.html`, `index.html` → `sections-index.html`); relative section links work unchanged at the new location.
- **`type` field added to every Vanilla `metadata.json`** (parity with Tailwind): `type:"component"` (126), `type:"section"` (65, with `category:"components"` → `"sections"`), `type:"template"` (8 — the old page-structure values `single-page`/`multipage` were normalized to `template` per the Tailwind precedent; page counts remain in `pages`).
- **Tooling updated**: `scripts/validate.py` (Vanilla/Sections allowed + scanned, React/Sections still forbidden, `type` enforced + bucket-checked for Vanilla metadata too), `_gen/rebuild_index.py` (`VANILLA_TREES` gains `("Sections", "section", False)`, Vanilla/Sections→Components path fallback preserves curated family data, tech-aware section-family naming so Vanilla section families are never mislabeled "(Tailwind)", `stats.vanillaByType` added, stale-path + type validation extended to Vanilla), `scripts/qa_vanilla.py` (quality bar now scans both Vanilla trees).
- **Index regenerated** (`python3 -m _gen.rebuild_index`): 80 families / 663 variants / 1490 styles — Tailwind unchanged (39 families, 464 variants, identical path sets), Vanilla 41 families / 199 variants (`vanillaByType={component:126, section:65, template:8}`). Vanilla section families keep their curated names; the sections-side Navigation family is named **"Navigation (Sections)"** to disambiguate from the legacy `Vanilla/Components/Navigation/` family.
- Root `index.html` Vanilla card now links to `Vanilla/Sections/sections-index.html` and lists all three content-type chips (Components / Sections / Templates). `COMPONENT_STRUCTURE.md` updated to the three-type Vanilla layout. `scripts/validate.py` passes (0 problems; QA bar: 191 components scanned, 0 required failures).

## 2026-08-22

### Added — React DatePicker component family (10 variants)
- Added `React/Components/DatePicker/` — a compound, TypeScript-first, Tailwind-first date picker family. All 10 variants ship the standard `{code.tsx, code.jsx, preview.html, metadata.json, README.md}` asset shape with a single shared core (`date-picker/code.tsx` is the authored reference; the other 9 are derived by `_gen_react_datepicker.py` from `_gen_react_datepicker_registry.py`, header-neutralized equality enforced).
- Variants: `date-picker` (reference — controlled + uncontrolled), `date-picker-with-label` (root-rendered label/description/helper with real `htmlFor` + `aria-describedby`), `date-picker-range` (typed `DateRange`, hover preview, 2-month popover, incomplete state, clear), `date-picker-with-presets` (Today/Yesterday/Last 7/30 days/This month with `aria-current` tracking), `date-picker-with-disabled-dates` (weekend matcher + hold + min/max window), `date-picker-with-error` (real form validation: `role="alert"` + `aria-invalid` + describedby + hidden ISO input), `date-picker-month-year` (`defaultView="months"` + heading cycle + paged 12-year spans, no giant dropdown), `date-picker-with-footer` (`requireApply` staged draft + Today/Clear/Apply), `date-picker-date-time` (`withTime` hour/minute selects, ISO `yyyy-mm-ddThh:mm` form value), `date-picker-mobile` (CSS-only bottom sheet below `sm`, 44px cells, overlay dismissal).
- Compound primitives: `DatePicker` (root provider — value/open/month/constraints/locale/format), `DatePickerInput`, `DatePickerTrigger`, `DatePickerContent` (non-modal `role="dialog"` popover with viewport flip + `mobileSheet`), `DatePickerHeader`, `DatePickerCalendar`, `DatePickerFooter`, `DatePickerPresets`, `DatePickerToday`, `DatePickerClear`, `DatePickerApply`, `DatePickerTime`, `useDatePicker` — plus the exported typed date utilities.
- The calendar core is derived from the React Calendar family (local calendar dates, numeric day keys, constructor arithmetic, roving tabindex, `Intl` labels) — self-contained per the DevSnips snippet architecture; no date-library dependency.
- QA: `scripts/_qa_react_datepicker.py` (static shape/metadata/export-parity/shared-core, Node date utilities across DST timezones, full Playwright behavior per variant, dark mode/focus/reduced-motion/zero-overflow @ 375/768/1280) — 1738 checks passed. Audit: `_audit_react_datepicker.py` (shared-core equality + semantics + anti-AI + parity) passes. TSX strict-checked with `tsc` (typescript in /tmp/dsbuild, build-time-only). `python3 _gen_react_datepicker.py --check` drift-free. React is still not a registered technology in `snippets-index.json` (follow-up; `scripts/validate.py` passes).

## 2026-08-15

### Changed — Vanilla templates consolidation (quality over quantity)
- **Purged 9 off-brand / low-value Vanilla template folders** that fought the design language defined in `design-tokens.md` (glassmorphism, neon, gradients, purple/violet accents, decorative blobs, gradient-saas, cyber aesthetics):
  - `nft-web3-project` (Orbitron + glass + neon NFT aesthetic)
  - `portfolio-site` (4 styles — glassmorphism, cyber-neon, gradient-blob, dark-purple)
  - `startup-template` (3 styles — cyber-neon, soft-gradient)
  - `product-launch` (3 styles — gradient-saas, cyber-neon, playful-pastel)
  - `blog-landing-pages` (4 styles — cyber-neon, soft-pastel-blob, etc.)
  - `micro-saas-product`, `template-element` (low value / vague)
  - `Landing-Pages` (one-page-scrolling), `Standalone` (404 + coming-soon placeholders)
- **Renamed two keepers** to reflect their rebuilt editorial purpose:
  - `freelancer-portfolio` → `developer-portfolio`
  - `ai-tool-launch` → `product-launch`
- **Final Vanilla Templates lineup: 8 templates** (down from 20+): SaaS Dashboard, Documentation Site, Job Board, Agency, Developer Portfolio, Product Launch, Event Conference, HTML5 Boilerplate.

### Added — 3 rebuilt Vanilla templates (editorial minimal, `--ds-*` design system)
All three are **modular** (`pages/code.html` + `pages/style.css` + `pages/script.js` + self-contained `preview.html` that inlines CSS+JS), **light-default** with calm opt-in dark mode (no-flash pre-paint + persisted toggle), hairline 1px borders, small controlled radii, restrained shadows, single controlled blue accent, Inter + JetBrains Mono, IntersectionObserver scroll-reveal (reduced-motion safe), skip link + semantic landmarks + single `h1` + ARIA + `:focus-visible` + native controls throughout.
- **`Developer Portfolio`** (`developer-portfolio/`) — a personal, technical, editorial-minimal portfolio for a software / design engineer. Sections: header (brand mark, anchor nav, theme toggle, mobile drawer), intro (clamp() lead, status badge, metadata grid), selected work (project cards with index/role/year/stack tags), about (narrative + capabilities table + four-up stat row), notes (writing list), contact (channels list), footer. JS: theme toggle, mobile nav, scrollspy (`aria-current`), reveal. QA PASS: 0 overflow at 320–1920px, 0 console errors, interactions verified. ID `developer-portfolio-001`, related `[agency, documentation-site, product-launch]`.
- **`Product Launch`** (`product-launch/`) — a clean, restrained product launch / waitlist landing page for a dev-focused product (fictional "Linear Field"). Sections: header, hero + working waitlist card (name + email inline validation, simulated submission, success state, beta-capacity progress bar), social-proof logo row, three-column feature grid, four-step how-it-works, two-plan pricing teaser, single-open FAQ accordion (CSS-grid 0fr→1fr, ARIA), final CTA, footer. JS: theme toggle, mobile nav, FAQ accordion, waitlist form validation, reveal. QA PASS: 0 overflow, 0 console errors, FAQ single-open + waitlist validation/success verified. ID `product-launch-001`, related `[developer-portfolio, documentation-site, event-conference]`.
- **`Event Conference`** (`event-conference/`, rebuilt from the neon-gradient original) — a dense, structured single-track conference website (fictional "Field Notes Conf 2027"). Sections: header (brand + date, anchor nav), hero + live countdown card (days/hours/mins/secs, paused when tab hidden), about (highlights table + stat row), speakers grid (avatar initials), two-day schedule with ARIA tablist (roving tabindex, Arrow Left/Right/Home/End) + time-rail slot list, venue (details table), capped sponsor tiers, three-tier register panel, footer. JS: theme toggle, mobile nav, schedule tabs, countdown, reveal. QA PASS: 0 overflow, 0 console errors, tab switching + countdown + theme verified. ID `event-conference-001`, related `[product-launch, developer-portfolio, agency]`.

### Changed — HTML5 Boilerplate polished
- **`html5-boilerplate/pages/index.html`** rewritten from a bare 15-line skeleton into a minimal clean starter aligned with the design system: core `--ds-*` token foundation (semantic + accent tokens, fonts, radii, spacing, motion), light-default + calm opt-in dark mode via `[data-theme="dark"]`, no-flash pre-paint theme script, system-font stack (Inter + JetBrains Mono with fallbacks), box-sizing reset, `:focus-visible` ring, `prefers-reduced-motion` guard. No external dependencies. Updated `metadata.json` + `README.md`.

### Added — `agent_instruction.md` for AI adaptation
- Added a concise `agent_instruction.md` to **7 templates** (SaaS Dashboard, Documentation Site, Job Board, Agency, Developer Portfolio, Product Launch, Event Conference): what the template is, the design-system rules to follow, the file layout, how to adapt it (rebrand / swap content / add pages), explicit "do not" guardrails, and the quality bar to re-check. Each points back to `design-tokens.md` as the source of truth.
- Added **`Vanilla/Templates/_build_preview.py`** — a small reusable helper that inlines `pages/style.css` + `pages/script.js` into `pages/code.html` to regenerate a self-contained `preview.html` for any modular Vanilla template (referenced by the `agent_instruction.md` files).

### Added — `scripts/_qa_template.py`
- A Playwright QA harness for individual Vanilla templates: checks horizontal overflow at 320/375/768/1024/1280/1920px, console/page errors, and template-specific interactions (Developer Portfolio: theme toggle + reveal; Product Launch: FAQ single-open + waitlist validation/success; Event Conference: schedule tablist + countdown + theme). Used to verify the rebuilds.

### Verified
- `scripts/validate.py` PASSED (architecture, metadata, index consistent); Vanilla quality-bar scan: 191 components, 0 required-check failures.
- `node --check` on all new JS files passes; strict HTML5 validation (html5lib, 0 errors) on all rebuilt `code.html` + `preview.html`.
- Per-template Playwright QA PASS for developer-portfolio, product-launch, event-conference, html5-boilerplate (0 overflow, 0 console errors, interactions verified).
- Calm dark mode verified (computed styles): near-black `rgb(10,10,10)` bg, soft-white `rgb(245,245,245)` text, inverted primary button — no neon/purple, per `design-tokens.md` §42.
- **Regenerated `snippets-index.json`** via `_gen/rebuild_index.py`: **78 families, 662 variants, 1486 styles** (Vanilla 40 families / 199 variants [297 Components + 8 Templates]). Index matches disk exactly.
- **Updated `AGENTS.md`** Vanilla Templates section to the post-consolidation state.

## 2026-08-13

### Changed — Vanilla templates folder layout
- **Standardized every Vanilla template to the same folder shape** so all code files live under a `pages/` sub-directory and only `preview.html` + `metadata.json` + `README.md` (+ optional `assets/`) sit at the root:
  ```
  <Template>/
  ├── pages/              ← all the code files
  │   └── index.html      (single-page) | code.html + style.css + script.js (modular) | *.html (multi-page)
  ├── preview.html
  ├── metadata.json
  └── README.md
  ```
- **Single-page / multi-variant leaves** (24 folders: ai-tool-launch, event-conference, freelancer-portfolio, html5-boilerplate, micro-saas-product, nft-web3-project, template-element, + every style folder under portfolio-site / product-launch / startup-template / blog-landing-pages / Landing-Pages / Standalone): moved the original self-contained `preview.html` to `pages/index.html`; the root `preview.html` is now a thin full-viewport `<iframe src="pages/index.html">` wrapper so the preview still opens directly (no content duplication).
- **Modular templates** (Agency, Documentation Site, Job Board): moved `code.html` + `style.css` + `script.js` together into `pages/` (their relative `href="style.css"` / `src="script.js"` refs stay valid since all three move together); `preview.html` is already self-contained (inlined) so it is unchanged. Documentation Site's `assets/` stays at root and the moved `code.html` favicon ref was rewritten `assets/favicon.svg` → `../assets/favicon.svg`.
- **SaaS Dashboard**: the 30 page files already lived in `pages/`; only the self-contained `code.html` was moved there. `css/`, `js/`, `assets/` stay at root as shared resources referenced by the root `preview.html` gallery shell and the pages (via `../`).
- **Updated `_gen/rebuild_index.py`** `make_variant` to recurse one level into `pages/` so each Vanilla template variant's `files` manifest lists both root files (`README.md`, `metadata.json`, `preview.html`) and the one-level `pages/*` contents (prefixed `pages/`).
- **Regenerated `snippets-index.json`** via `_gen/rebuild_index.py` — index matches disk exactly (0 mismatches); totals unchanged (**89 families, 852 variants, 2014 styles**; Vanilla 51 families / 321 variants).
- **Updated `AGENTS.md`** with the canonical Vanilla template folder layout and per-template notes.

### Verified
- `scripts/validate.py` PASSED (architecture, metadata, and index all consistent). The single pre-existing duplicate-ID note (`feature-grid-neo-brutalism`) is unchanged by this work.
- `scripts/qa_vanilla.py` — 266 components scanned, 0 required-check failures.
- Strict HTML5 validation (html5lib) on the new wrapper previews + sampled moved pages passes; `node --check` on all moved JS files passes. (The SaaS Dashboard `preview.html` strict html5lib error pre-existed and that file was not modified.)

## 2026-08-12

### Added — Vanilla template
- **`Job Board`** (`Vanilla/Templates/Job Board/`) — a dense, structured developer job-board template. Modular files: `code.html` (links `style.css` + `script.js`) + `style.css` + `script.js` + `preview.html` (self-contained single-file preview inlining CSS+JS) + `metadata.json` + `README.md`. No `assets/` (text-logo avatars + inline SVG/emoji; Inter + JetBrains Mono via Google Fonts CDN). Single-page view switching: Jobs (search + location/type filters + category chips + paginated list), Job Detail (sidebar Apply/Save), Companies + Company Detail, Saved Jobs, Candidate (Profile / Applications status table / Saved). Scoped apply modal, toasts, mobile nav dropdown, mobile filter drawer. Built on the shared `--ds-*` token system (`design-tokens.md`); the original `--color-*` vocabulary is mapped onto `--ds-*` so the light-mode output is identical to the uploaded design. Opt-in calm dark mode (`prefers-color-scheme`), `prefers-reduced-motion` guard, generic `.hidden` utility. QA verified (Playwright) for both `code.html` and `preview.html`: 0 console errors, 0 horizontal overflow at 320/375/768/1024/1280/1920px, strict HTML5 valid (html5lib), `script.js` valid (node --check), interactions pass, light-mode computed styles match the original 1:1. ID `job-board-001`, slug `job-board`, source `DevSnips`, related `[saas-dashboard, documentation-site, agency]`.
- **Regenerated `snippets-index.json`** via `_gen/rebuild_index.py`: **110 families, 856 variants** (Vanilla now 51 families / 321 variants [297 Components + 24 Templates]). Index matches disk exactly (0 mismatches). Updated README.md + AGENTS.md authoritative counts.

## 2026-08-10 (architecture migration)

### Changed — Components + Templates architecture
- **Consolidated the repository to two content types per technology.** Each of `Tailwind/`, `Vanilla/`, and `React/` now contains only `Components/` and `Templates/`. Created `React/Components/` and `React/Templates/` (currently empty, reserved for future content).
- **Merged all Sections into Components.** Every former `Tailwind/Sections/` family (165 fifteen-style components across 11 categories, 33 multi-concept components across ai-product/app-ui/developer/marketing/premium-visual, and 18 SaaS components) moved to `Tailwind/Components/`. Every former `Vanilla/Sections/` Neo-Brutalist family (65 sections across 16 families) moved to `Vanilla/Components/`. Section metadata `category` updated `sections`/`Sections` → `components`/`Components`; IDs, slugs, names, and descriptions preserved.
- **Merged `Vanilla/Sections/Navigation/` into `Vanilla/Components/Navigation/`** (4 variants folded into the existing 24, now 28 variants).
- **Removed the standalone `Vanilla/Utilities/` (76 snippets) and `Vanilla/Resources/` (67 JS helpers) collections.** No existing component depended on them; no broken references remain.
- **Removed empty reserved dirs** `Tailwind/Sections/`, `Tailwind/Utilities/`, `Tailwind/Pages/`, `Vanilla/Tools/`.
- **Moved `Tailwind/Sections/STYLE_TOKENS.md`** to `Tailwind/Components/STYLE_TOKENS.md` (design-token reference for the section-style components).
- **Updated `_gen/` generator** (`generate.py`, `update_index.py`) to emit section-style components into `Tailwind/Components/` with `category: components`, preserving reproducibility.
- **Added `scripts/validate.py`** and **`_gen/rebuild_index.py`** (regenerates `snippets-index.json` from the filesystem, preserving curated family metadata by path match and cross-validating indexed == on-disk).
- **Regenerated `snippets-index.json`** from the migrated filesystem: **106 families, 846 variants** (Tailwind 59 families / 535 variants [526 Components + 9 Templates]; Vanilla 47 families / 311 variants [297 Components + 14 Templates]). Index matches disk exactly (0 mismatches).
- **Updated docs**: README.md, CONTRIBUTING.md, COMPONENT_STRUCTURE.md describe the new Components + Templates architecture and the recalculated counts.

### Notes
- Two pre-existing duplicate IDs (`feature-grid-neo-brutalism` across marketing/saas; `contact-form-001` across Forms/Contact and Contact) existed before the migration at their old locations and are preserved unchanged per the "preserve existing IDs" rule.

## 2026-08-10

### Fixed (repository-wide audit & sync)
- **Synced `snippets-index.json` to the actual filesystem.** The index was 253 items out of date (declared 90 families / 735 variants; actual 114 families / 988 variants). Regenerated `families[]`, `variants[]`, `variantsCount`, `stats`, and `technologies[].families` from on-disk `metadata.json`, preserving existing hand-curated descriptions/tags/searchTerms where present. All counts now match the disk exactly (0 mismatches).
  - **Tailwind Components:** Buttons recount fixed 15 → 58 (the index counted the 15 variant-group folders instead of the 58 leaf sub-variants). Total now 310 (was 267 in the index).
  - **Tailwind Templates:** added 3 missing templates (northline-atelier, krat-adventure, quiet-place). Total now 8.
  - **Vanilla Components:** recount fixed Forms 6 → 38, Navigation 8 → 24, Marketing 4 → 6, Accordions 5, Media 17. Total now 232 (was 182 in the index).
  - **Vanilla Sections:** confirmed 65 (was already correct).
  - **Vanilla Templates:** added all 14 (were entirely missing from the index).
  - **Vanilla Utilities:** added all 76 across Animations (33), Layout (22), Typography (10), Theming (7), Clipboard (3), Scrollbar (1) (were entirely missing).
  - **Vanilla Resources:** added all 67 JS helpers — Helpers (65), LocalStorage (2) (were entirely missing).
  - Recomputed stats: **114 families**, **988 variants**.

### Fixed (content quality)
- Reclassified 5 items under `Vanilla/Components/` whose `metadata.json` and `README.md` wrongly declared `category: utilities` despite living under Components with an `.html` file (css-toggle-switch, accordion-panel, image-slider, responsive-sticky-header-with-shadow, scroll-to-top). Now `category: components` with a matching `subcategory`, so path and metadata agree.
- Removed an empty placeholder file `Vanilla/Templates/product-launch/launchsite3.html` (0 bytes; unreferenced).

### Changed
- Updated `README.md` structure tree and family tables to the on-disk counts (Tailwind Components 267 → 310, Buttons 15 → 58; Vanilla Components 182 → 232) and documented the previously-missing Vanilla Templates (14), Utilities (76), Resources (67), and Tailwind Sections (216) and Templates (8).
- Corrected a stale `CHANGELOG.md` reference to a non-existent `devsnips/snippets/{html,css,js}-snippets` tree to point at the real `Vanilla/Components/`, `Vanilla/Utilities/`, and `Vanilla/Resources/` locations. *(These two standalone collections have since been removed in the 2026-08-10 architecture migration — see the entry above.)*

## 2026-08-05

### Added
- **Indexed all unindexed Tailwind and Vanilla components in `snippets-index.json`.** Registered 14 missing Tailwind `Input` variants (chat-input, credit-card, currency-input, cvv, email-input, expiration-date, markdown-editor, mention-input, otp-6-digit, phone-input, rich-text-editor, search-with-autocomplete, search-with-filters, url-input — Input now has 49 variants, was 35). Registered all 19 `Vanilla/Components/` families that were entirely missing from the index: Accordions (5), Alerts (2), Avatars (1), Badges (2), Buttons (14), Cards (15), Display (7), Dropdowns (1), Forms (6 subcategories), Loaders (8), Marketing (4 subcategories), Media (17), Modals (12), Navigation (8), Other (65), Ratings (3), Tables (4), Tabs (5), Tooltips (3). Added all 19 names to `technologies[].families` for Vanilla. Stats recomputed: **47 families** (was 28), **514 variants** (was 318), **520 styles** (was 324). All variant counts now match on-disk folders (0 out of sync).
- Added the **Tooltips** Tailwind component family with 6 production-ready variants: `basic-tooltip` (top-positioned with arrow, hover + focus), `directional-tooltip` (all 4 directions with auto-positioned arrows), `rich-tooltip` (title + multi-line description for form help text), `delayed-tooltip` (600ms show delay via CSS transition-delay, instant hide), `icon-tooltip` (icon-button labeling with `aria-label` + `role=tooltip`), and `status-tooltip` (status dots with success/warning/error/info themed tooltips). All variants are pure CSS — no JavaScript — and accessible via `role=tooltip` + `aria-describedby` and `:focus-visible` keyboard triggers.
- Added the **Progress** Tailwind component family with 6 production-ready variants: `linear-bar` (determinate/indeterminate/completed), `circular-spinner` (4 sizes, pure CSS), `skeleton-loader` (card + list shimmer with reduced-motion support), `segmented-stepper` (3-step checkout with interactive next/back), `step-progress` (vertical milestone timeline), and `upload-progress` (multi-file list with per-file bars and success transitions). Each ships the standard `code.html` / `preview.html` / `metadata.json` trio with `role=progressbar`/`status` + `aria-live=polite` accessibility.
- Added the **Toasts** Tailwind component family with 6 production-ready variants: `basic-toast`, `status-toasts` (success/error/warning/info), `action-toast` (inline Undo action with `onAction` callback), `stacked-toasts` (notification queue with dismiss-all), `persistent-toast` (countdown progress bar that pauses on hover), and `minimal-toast` (compact pill for terse "Copied!" feedback). Each variant ships the standard `code.html` / `preview.html` / `metadata.json` trio with `role=status`/`alert` + `aria-live=polite` accessibility.
- Registered the Toasts, Progress, and Tooltips families in `snippets-index.json` (`families[]` and `technologies[].families`).

### Fixed
- Synced `snippets-index.json` with the on-disk layout: registered 5 previously-missing Tailwind component families — **Accordions** (15 variants), **Cards** (40), **Dropdowns** (30), **Navigation** (35), and **Tables** (20) — pulling real names, descriptions, features, and tags from each variant's `metadata.json`. Added **Tabs** to `technologies[].families`. All 12 Tailwind families now appear in both `families[]` and `technologies[].families`.

### Changed
- Rewrote `README.md` structure tree and Component Families table to list all 12 Tailwind families (was only Buttons) and all 19 Vanilla/Components families (was a one-line summary).
- Updated `CONTRIBUTING.md` contribution flow to reference the real `Tailwind/Components/` and `Vanilla/Components/` paths (was pointing at a nonexistent `devsnips/snippets/` tree) and documented the three-file-per-variant convention.
- Recomputed index stats: **47 families** (was 21), **514 variants** (was 166), **520 styles** (was 172). Index now matches on-disk counts exactly.

## 2026-03-10

### Added
- Added new HTML snippets: modal dialog, accordion FAQ layout, pricing card, skeleton loader, and toast notification markup.
- Added new CSS snippets: dark mode variables, responsive grid system, animated hamburger menu, and focus-visible accessibility styles.
- Added new JS snippets: debounce utility, clipboard copy helper, local storage wrapper, form validator, and lazy image loader.
- Added `snippets-index.json` containing metadata for all snippet files.
- Added shared project config: `.editorconfig`, `.htmlhintrc`, `eslint.config.js`, and GitHub Actions lint workflow at `.github/workflows/lint.yml`.

### Changed
- Added standardized snippet header comments to existing snippet files in `Vanilla/Components/`, `Vanilla/Utilities/`, and `Vanilla/Resources/` where missing.
- Rewrote `README.md` with a clearer structure, usage guide, badges, and a full snippet table.
- Updated `CONTRIBUTING.md` with explicit code style rules, header templates, and a contribution checklist.
- Updated `PULL_REQUEST_TEMPLATE.md` with accessibility and cross-browser testing checks.

### Tradeoffs / Decisions for Maintainer Review
- Snippet descriptions in `snippets-index.json` are generated from filenames for consistency and maintainability; maintainers may want to manually curate descriptions over time.
- Workflow linting currently targets snippet directories only to avoid failures from demo/landing-page files with different structure.
- Existing snippet formatting was standardized by documentation and headers first; full per-file semantic and indentation normalization across all legacy snippets was not performed in this pass to keep changes reviewable.
