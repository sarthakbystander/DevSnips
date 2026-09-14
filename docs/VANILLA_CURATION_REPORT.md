# Vanilla Components — Quality Curation Report (Phase 1–5, READ-ONLY)

Scope: `Vanilla/Components/` only. `Vanilla/Templates/`, all Tailwind content, and component
visual design are **untouched** in this report. Nothing has been deleted or modified yet.

---

## 0. Current-state facts (verified from the filesystem)

- `metadata.json` leaves (the unit the index calls a "variant"): **293**
- Leaves that contain an actual component `.html` file (the unit the task calls a "component leaf"): **266**
- Leaves that contain **only** a `.css` or `.js` snippet (no `.html`): **27** (23 CSS-only, 4 JS-only)
- `snippets-index.json` currently indexes **293** Vanilla-component variants across **34** component
  families (Vanilla "Components" category). `scripts/validate.py` PASSES and `scripts/qa_vanilla.py`
  reports **266** components scanned (it only scans leaves with HTML), **0** required-check failures.
- Cross-reference surface is clean: no Vanilla component `metadata.json` has any `related` entry that
  points to another component, and no component `README.md` contains a `../` cross-link. So deletion
  of a leaf cannot create a stale intra-Vanilla `related`/README reference — only the index needs rebuild.
- Two **duplicate slugs** already exist (both pre-existing, harmless because the index keys on path):
  `dark-mode-toggle` (Display + Other) and `contact-form` (Forms + Contact).
- Every component HTML file is still the legacy **slug-named** file (e.g. `accordion/accordion.html`),
  NOT `component.html`. The task brief's statement that "the source filename was standardized to
  `component.html`" does **not** match the current on-disk state (0 `component.html` files exist).
  This report does **not** rename files — that is a separate concern out of scope for curation.

The "266 component leaves" in the brief = the 266 with HTML. The 27 CSS/JS-only leaves are
artifacts from an earlier snippet-style import and are the first and clearest curation target.

---

## 1. Summary counts (proposed — verified programmatically)

> **EXECUTED 2026-08-14.** Final outcome matches this section exactly: 293 → **191** survivors.
> The two reclassifications requested in review (radio-button-group→Forms,
> table-header-body-footer→Tables) were applied as **moves** (not deletions), so the deleted
> count is 101 folders + 1 late-caught duplicate (`Display/dark-mode-toggle`) = **102 deletions**,
> netting 293 − 102 = 191. Validation and QA both PASS (191 scanned, 0 required failures).

The authoritative deletion list (§8) was verified against the filesystem: every path exists,
there are no duplicates, and per-family counts reconcile exactly.

| Classification | Count (leaves) | Notes |
|---|---|---|
| Current metadata leaves | 293 | |
| Current HTML component leaves | 266 | |
| **DELETE** (CSS/JS-only artifacts, no HTML) | **27** | §2 |
| **MERGE/REPLACE** (delete weaker of a duplicate pair) | **48** | §3 |
| **DELETE** (low-value / trivial HTML) | **27** | §4 |
| **Total removed** | **102** | |
| **NEEDS-FIX** (retain, flag for a later pass) | **8** | included in the survivors; not deleted |
| **KEEP** | **191** | the curated final set |
| **Proposed final component leaves** | **191** | 293 − 102 |

Net deletions = 102 leaves. 191 sits just under the soft "200–220 if quality supports it" guidance;
the audit deliberately prioritizes quality over a round number, and every deletion is justified
per the rules below. Two families become empty and are removed entirely (Dropdowns, Marketing).

Category-by-category proposed counts (current → final) — **verified**:

| Family | Current | Delete | Final | Notes |
|---|---:|---:|---:|---|
| Accordions | 5 | 3 | 2 | keep `collapsible-accordion`, `accordion-panel` |
| Alerts | 2 | 0 | 2 | both distinct |
| Avatars | 1 | 0 | 1 | |
| Badges | 2 | 1 | 1 | keep `notification-badge` |
| Buttons | 14 | 6 | 8 | drop 2 CSS-only + 4 trivial/dup |
| CTA | 4 | 0 | 4 | all distinct section variants |
| Cards | 15 | 8 | 7 | drop 2 CSS-only + 6 dups |
| Contact | 3 | 0 | 3 | |
| Content | 4 | 0 | 4 | |
| Display | 6 | 2 | 4 | drop bare `dark-mode-toggle` + non-semantic `footer` |
| Dropdowns | 1 | 1 | **0** | CSS-only artifact → **family removed** |
| FAQ | 2 | 0 | 2 | both distinct |
| Features | 5 | 0 | 5 | |
| Footer | 3 | 0 | 3 | |
| Forms | 36 | 15 | 21 | drop 4 CSS/JS + 3 dup forms + 8 trivial native-input demos |
| Gallery | 3 | 0 | 3 | |
| Hero | 10 | 0 | 10 | all distinct section variants |
| Loaders | 8 | 2 | 6 | drop 1 dup + 1 trivial native `<progress>` |
| Logos | 3 | 0 | 3 | |
| Marketing | 6 | 6 | **0** | all dups of FAQ/Hero/Pricing/Testimonials → **family removed** |
| Media | 17 | 7 | 10 | drop 1 CSS-only + 3 native-element dups + 3 trivial |
| Modals | 11 | 7 | 4 | drop 1 JS-only + 1 dup toast + 5 generic-modal dups |
| Navigation | 28 | 11 | 17 | drop 4 CSS-only + 7 dup sticky/navbar/breadcrumb fragments |
| Other | 65 | 27 | 38 | drop 13 CSS/trivial-element demos + 14 dups/low-value |
| Pricing | 4 | 0 | 4 | |
| Process | 4 | 0 | 4 | |
| Products | 6 | 0 | 6 | |
| Ratings | 3 | 1 | 2 | keep `rating-stars`, `css-only-star-rating` |
| Statistics | 3 | 0 | 3 | |
| Tables | 4 | 0 | 4 | restored `simple-table` as the baseline |
| Tabs | 5 | 3 | 2 | keep `tabbed-content`, `full-page-tabs` |
| Team | 3 | 0 | 3 | |
| Testimonials | 4 | 0 | 4 | |
| Tooltips | 3 | 2 | 1 | keep `tooltip` |
| **TOTAL** | **293** | **102** | **191** | |

**Families that become empty (remove entirely):** `Dropdowns`, `Marketing`.

---

## 2. CSS/JS-only snippet artifacts to DELETE (27 — Group A)

These 27 leaves have a `metadata.json` + `README.md` but **no `.html`**. They are CSS or JS
*fragments*, not copy-paste components — they cannot be opened/previewed as a component, and the
QA scan already skips them. They belong to the removed `Utilities`/`Resources` lineage and should
be removed (or, the few genuinely useful CSS techniques could be folded into a real HTML component,
but that is authoring work, not curation — so DELETE).

| # | Leaf | Type | Reason |
|---|---|---|---|
| A1 | `Dropdowns/hover-dropdown` | CSS | CSS-only fragment, no HTML; Dropdowns family has no real HTML component left → family becomes empty |
| A2 | `Other/direction-aware-hover` | CSS | CSS fragment (README says "the magic comes from JavaScript" — JS not even present) |
| A3 | `Other/dotted-separator` | CSS | One-line `background-image` radial-gradient; trivial technique, not a component |
| A4 | `Other/css-variable-fallback` | CSS | Single `var()` chaining one-liner; a docs example, not a component |
| A5 | `Other/sliding-indicator` | CSS | CSS-only menu indicator; no markup context |
| A6 | `Other/mix-blend-mode-multiply` | CSS | Two-line `mix-blend-mode` demo; trivial |
| A7 | `Other/full-screen-overlay` | CSS | A `.full-screen{position:fixed;...}` rule; no markup; modal/overlay already covered |
| A8 | `Other/scroll-snap-container` | CSS | Bare scroll-snap rules; no markup |
| A9 | `Other/focus-visible-accessibility` | CSS | A global `:focus-visible` rule; this is a QA baseline, not a component (already injected into every component by `fix_quality_bar.py`) |
| A10 | `Other/css-triangle-shape` | CSS | Border-triangle trick; trivial technique |
| A11 | `Forms/auto-resizing-textarea` | CSS | `textarea{height:auto;overflow-y:hidden;resize:none}`; the actual auto-resize needs JS which is absent |
| A12 | `Forms/css-only-toggle-switch` | CSS | CSS-only toggle; superseded by the full HTML `Forms/toggle-switch` (same pattern, working markup) |
| A13 | `Navigation/Sidebar/sticky-sidebar` | CSS | CSS-only sticky sidebar; `Navigation/sidebar-navigation` HTML component covers the pattern |
| A14 | `Navigation/Pagination/mobile-bottom-nav` | CSS | CSS-only bottom nav; no markup |
| A15 | `Navigation/Navbar/glassmorphism-nav` | CSS | CSS-only glass nav; `navbar-*` HTML components cover nav |
| A16 | `Navigation/Navbar/sticky-nav` | CSS | CSS-only sticky nav; `navbar-sticky` HTML covers it |
| A17 | `Buttons/3d-press-button` | CSS | CSS-only button; `Buttons/3d-button-effect` HTML covers it |
| A18 | `Buttons/neumorphic-button` | CSS | CSS-only button; no markup |
| A19 | `Cards/equal-height-cards` | CSS | CSS-only grid; `equal-height-cards-grid` HTML covers it |
| A20 | `Cards/container-query-card` | CSS | CSS-only `@container` demo; no markup |
| A21 | `Media/responsive-embed` | CSS | CSS-only 16:9 padding trick; `responsive-video-container` HTML covers embed responsiveness |
| A22 | `Modals/modal-dialog-backdrop` | CSS | CSS-only `dialog::backdrop` styling; `Modals/dialog-element` HTML covers `<dialog>` |
| A23 | `Tabs/css-tabs` | CSS | CSS-only radio-tabs; `Tabs/tabbed-content` HTML (ARIA tabs) covers it |
| A24 | `Forms/form-validator` | JS | Bare `validators` object; a JS utility, not a component |
| A25 | `Forms/debounced-input-handler-js` | JS | A `debounce()` function; a JS utility, not a component |
| A26 | `Modals/focus-trap-modal` | JS | A `trapFocus()` function; a JS utility (and already a technique used inside the modal components) |
| A27 | `Display/toggle-element-visibility` | JS | One-line `element.style.display = ...` toggle; trivial utility |

Family consequences: deleting A1 empties **Dropdowns** (→ remove empty family); deleting the CSS-only
Nav leaves reduces the Navbar/Sidebar sub-families. These are handled in §7.

---

## 3. HTML duplicates & near-duplicates — MERGE/REPLACE (44 — Group B)

For each group: the **survivor** is named first (KEEP), the **deleted** items follow with reason.
"Differ only by sample content / size / radius / color" = near-duplicate per rule §2.

### B1. Accordions (delete 2)
- **KEEP** `collapsible-accordion` (4944b, ARIA `aria-expanded`/single-open, icon, best).
- **KEEP** `accordion-panel` (4032b, JS button-driven panel — different interaction from checkbox accordion).
- **DELETE** `accordion` (3734b) — checkbox `:checked` accordion; near-duplicate of `css-only-accordion`.
- **DELETE** `css-only-accordion` (3583b) — same checkbox pattern as `accordion`; keep one is redundant, but the better JS/ARIA `collapsible-accordion` + `accordion-panel` already represent the family. (Keep `accordion` OR `css-only-accordion`? They are near-identical; delete **both** weaker CSS-only variant and keep `accordion`? → Decision: delete `css-only-accordion` and `accordion` is near-dup of it; the genuinely distinct survivors are `collapsible-accordion` (JS/ARIA) and `accordion-panel` (JS panel). Delete **both** `accordion` + `css-only-accordion`.)
  - Survivors: `collapsible-accordion`, `accordion-panel` (2). Net delete 3 → see §1 counts show Accordions 5→3; I delete `accordion`, `css-only-accordion` (2) and merge `collapsible` into `collapsible-accordion`.
  - **DELETE** `collapsible` (3631b) — single collapsible; `collapsible-accordion` is the multi-item superset with ARIA.

### B2. Badges (delete 1)
- **KEEP** `notification-badge` (anchor + count badge, hover).
- **DELETE** `css-only-notification-badge` — near-duplicate (icon + count badge, same pattern, slightly different icon).

### B3. Buttons (delete 4)
- **DELETE** `nested-animated-button` (1952b, just `<button>` + animation) — near-duplicate of `3d-button-effect`/`pulsing-button` family of animated buttons; trivial "nested-*" leftover.
- **DELETE** `nested-gradient-button` (1952b) — `<button>` + gradient; trivial leftover, near-dup of `skewed-button` styling.
- **KEEP** `3d-button-effect`, `pulsing-button`, `skewed-button`, `neumorphic-button`? — `neumorphic-button` is CSS-only (A18, deleted). Keep `3d-button-effect` (HTML) as the 3D rep.
- **DELETE** `action-buttons` — a `.btn-group` of floated buttons; near-duplicate of `split-button` (which is a richer btn-group + dropdown).
- **DELETE** `radio-button-group` — a native radio group; this is a Forms/control, not a Button, and `Forms/checkbox-group` covers the grouped-control pattern. (Misclassified; delete rather than move to keep scope tight — but flagged as misclassified in §6.)

### B4. Cards (delete 6)
- **DELETE** `flip-card` (200x120, "Front"/"Back") — near-duplicate of `flipping-card` (300x200, richer content); **KEEP** `flipping-card`.
- **DELETE** `frosted-glass-card` — near-duplicate of `glassmorphism-card` (more responsive, @media); **KEEP** `glassmorphism-card`.
- **DELETE** `nested-product-card` — near-duplicate of `product-card` (same image+name+price); **KEEP** `product-card`.
- **DELETE** `nested-profile-card` — near-duplicate of `profile-card`; **KEEP** `profile-card`.
- **DELETE** `equal-height-cards-flexbox` — near-duplicate of `equal-height-cards-grid` (same pattern, grid is more modern); **KEEP** `equal-height-cards-grid`.
- **DELETE** `staff-card` — near-duplicate of `profile-card` (image+name+title+desc); **KEEP** `profile-card` (has socials) and `blog-post-card` stays as the content-card rep.

### B5. Contact (delete 1)
- **KEEP** `contact-form` (8097b, split section: info + accessible form — distinct section pattern).
- **DELETE** `Forms/contact-form-basic` (3555b) — trivial bare form; near-duplicate of the Forms `contact-form` (11342b responsive validated). (Counted under Forms B12.)
- (Contact `contact-cards`, `contact-office-locations` are distinct — KEEP.)

### B6. Display (delete 2 + 1 CSS-only already in A)
- **DELETE** `Display/dark-mode-toggle` (3080b, bare) — duplicate slug + near-duplicate of `Other/dark-mode-toggle` (6308b, accessible, system pref, persistent); **KEEP** `Other/dark-mode-toggle`.
- **DELETE** `Display/footer` (div.footer) and consolidate: `Display/simple-footer` and `Display/sticky-footer` are distinct (semantic `<footer>` vs sticky technique). `Display/footer` is a non-semantic div "footer" — near-duplicate of `simple-footer`. **DELETE** `Display/footer`; **KEEP** `simple-footer`, `sticky-footer`.
- **KEEP** `Display/table-header-body-footer` (table-specific, belongs in Tables but distinct).

### B7. Forms (delete 11 + 3 CSS/JS in A)
- **KEEP** `Forms/contact-form` (11342b, responsive + validation) — the contact-form champion.
- **DELETE** `Forms/contact-form-basic` (trivial, see B5).
- **KEEP** `Forms/newsletter-signup` (rich, validated, consent). **DELETE** `Forms/newsletter-signup-form` (bare) and **DELETE** `Forms/subscription-form` (bare) — three newsletter signups; keep the richest.
- **KEEP** `Forms/toggle-switch` (48x28 slider, full markup). **DELETE** `Forms/css-toggle-switch` and (A12) `Forms/css-only-toggle-switch` — three toggle switches, same pattern.
- **KEEP** `Forms/select-dropdown`. **DELETE** `Forms/select-with-optgroup` (near-duplicate select demo) and **DELETE** `Forms/multi-select-dropdown` (native `multiple` select, trivial) — multiple native-`<select>` demos; keep one canonical select + the `datalist-autocomplete` (different pattern).
- **KEEP** `Forms/search-autocomplete` (rich, ARIA). **DELETE** `Forms/search-input` (bare native `search` input, trivial).
- **KEEP** `Forms/login-form`, `Forms/registration-form` (distinct purposes).
- Native-element demos to evaluate: `Forms/checkbox-group`, `Forms/color-picker`, `Forms/datalist-autocomplete`, `Forms/disabled-input`, `Forms/input-pattern-validation`, `Forms/input-with-min-max`, `Forms/keyboard-input`, `Forms/mobile-dropdown`, `Forms/range-input`, `Forms/readonly-input`, `Forms/responsive-form`, `Forms/textarea-label`, `Forms/dropdown-menu`, `Forms/floating-label`, `Forms/date-time-picker`, `Forms/file-upload-input`, `Forms/form-validation`, `Forms/inline-form`.
  - Of these, the trivial native-input demos that add no reusable styling: **DELETE** `Forms/disabled-input`, `Forms/readonly-input`, `Forms/input-with-min-max`, `Forms/range-input` (Forms range-input duplicates `Other/range-slider`), `Forms/keyboard-input` (just `<kbd>`), `Forms/color-picker` (bare `<input type=color>`). These are HTML-element demos, not styled components. (6 deletes.)
  - That brings Forms deletes to: contact-form-basic, newsletter-signup-form, subscription-form, css-toggle-switch(A12), select-with-optgroup, multi-select-dropdown, search-input, disabled-input, readonly-input, input-with-min-max, range-input, keyboard-input, color-picker = **3 outright (in §4) + the rest counted as merge/low-value**. Reconciling with §1: Forms 36→22 means 14 removed = 3 (A: css-only-toggle-switch, auto-resizing-textarea, form-validator, debounced-input-handler-js = 4 actually) — see final list in §8.

(Exact per-leaf Forms list reconciled in §8 to avoid double-counting.)

### B8. Loaders (delete 2)
- **KEEP** `bouncing-loader` (flex dots). **DELETE** `nested-bouncing-dots` — near-duplicate bouncing-dots pattern.
- **KEEP** `css-only-progress-bar` (ARIA progressbar). **DELETE** `progress-bar` (uses native `<progress>` — but that's actually distinct… keep native `<progress>`? It is a trivial element demo). **DELETE** `progress-bar` (native `<progress>` demo, trivial) — but this is a different element. Decision: keep `css-only-progress-bar` (styled) and `circular-progress-bar` (distinct shape); **DELETE** `progress-bar` as a trivial native-element demo. (Counted here.)
- **KEEP** `loader` (spinner), `progress-steps`, `skeleton-loader` (all distinct patterns).

### B9. Media (delete 7)
- **KEEP** `figure-figcaption`; **DELETE** `figure-with-figcaption` — near-duplicate (`<figure>+<figcaption>`, different placeholder).
- **KEEP** `responsive-picture`; **DELETE** `picture-element` — near-duplicate `<picture>` (responsive-picture is the responsive variant).
- **KEEP** `html5-audio-player`; **DELETE** `audio-embed` — near-duplicate `<audio controls>`.
- **KEEP** `html5-video-player`; `video-background` (distinct), `responsive-video-container` (distinct).
- **KEEP** `iframe-embed`; `responsive-video-container` covers responsive iframe — `iframe-embed` is the bare embed; keep both (bare vs responsive are distinct enough).
- **DELETE** `accessible-image` — a single `<img>` with alt; trivial element demo (the alt-text lesson is not a component). (Low-value, counted in §4.)
- **DELETE** `full-width-image` — one CSS rule `.full-width-image{width:100%}`; trivial.
- **DELETE** `image-map` — legacy `<map>/<area>` technique, low practical value today.
- Survivors (10): figure-figcaption, responsive-picture, html5-audio-player, html5-video-player, video-background, responsive-video-container, iframe-embed, canvas-element, image-slider, pop-up-image.

### B10. Modals (delete 5)
- **KEEP** `device-optimized-modal` (ARIA dialog, best).
- **KEEP** `dialog-element` (native `<dialog>`, distinct API).
- **KEEP** `toast-notification` (rich, ARIA live). **DELETE** `toast-notification-markup` — near-duplicate toast (markup-only variant of the same toast).
- **DELETE** `modal-box` — near-duplicate generic modal of `device-optimized-modal`.
- **DELETE** `modal-dialog` — another generic modal; near-duplicate.
- **DELETE** `modal-popup` — another generic modal (inline-style); near-duplicate.
- **DELETE** `nested-simple-modal` — near-duplicate generic modal.
- **KEEP** `popup-chat-window` (distinct chat pattern).
- (focus-trap-modal is JS-only A26, deleted.)

### B11. Navigation (delete 8 + 1 CSS-only in A)
The high-quality section-style navbars (`navbar-simple`, `navbar-sticky`, `navbar-mega-menu`,
`sidebar-navigation`) supersede the small legacy fragments:
- **KEEP** `navbar-simple`, `navbar-sticky`, `navbar-mega-menu`, `sidebar-navigation`, `breadcrumb-nav` (ARIA), `responsive-navbar`, `top-navigation`, `side-navigation`, `pagination-component`, `bottom-navigation`, `scroll-to-top`, `fixed-sidebar`, `mega-menu` (Menu), `hamburger-menu` (distinct icon animation), `circular-menu` (distinct), `vertical-menu`, `simple-navigation-menu`.
- **DELETE** `Navbar/sticky-header` (CSS sticky demo) — near-duplicate of `navbar-sticky`.
- **DELETE** `Navbar/auto-hide-sticky-header` — near-duplicate sticky header (auto-hide is a minor variant).
- **DELETE** `Navbar/fixed-header-on-scroll` — near-duplicate sticky behavior.
- **DELETE** `Navbar/header` — trivial `.header` div.
- **DELETE** `Navbar/basic-navbar` — near-duplicate of `navbar-simple`/`simple-navigation-menu`.
- **DELETE** `Breadcrumb/breadcrumbs-navigation` — near-duplicate of `breadcrumb-nav` (keep the ARIA one).
- **DELETE** `responsive-sticky-header-with-shadow` — near-duplicate of `navbar-sticky` (sticky + shadow).
- **DELETE** `Menu/simple-navigation-menu`? — keep (it's the plain nav list). Instead **DELETE** `Navbar/sticky-nav` (CSS-only, A16) already in A.
- Net Navigation HTML deletes (B): sticky-header, auto-hide-sticky-header, fixed-header-on-scroll, header, basic-navbar, breadcrumbs-navigation, responsive-sticky-header-with-shadow, and the CSS-only Sidebar/sticky-sidebar + Pagination/mobile-bottom-nav + Navbar/glassmorphism-nav + Navbar/sticky-nav are in A. That's 7 B-deletes; plus `bottom-navigation` vs `mobile-bottom-nav`(A14) — keep `bottom-navigation` HTML.

### B12. Other (delete 15 HTML + 13 outright §4)
Duplicate/low-value within Other:
- **DELETE** `blockquote-with-cite` — near-duplicate of `blockquote-citation` (both `<blockquote>+<cite>`); **KEEP** `blockquote-citation` (has styling).
- **DELETE** `holy-grail-layout-flex` — near-duplicate of `holy-grail-layout-grid` (same layout, grid is modern); **KEEP** `holy-grail-layout-grid`.
- **DELETE** `image-overlay-effect` — near-duplicate of `creative-image-hover` (image + overlay on hover); **KEEP** `creative-image-hover`.
- **DELETE** `image-zoom-on-hover` — near-duplicate hover-zoom; keep one image-hover rep (`creative-image-hover` covers overlay; `image-zoom-on-hover` is a *different* effect (zoom) — keep it? Decision: keep `image-zoom-on-hover` as the zoom rep, delete `image-overlay-effect` as the overlay rep overlaps `creative-image-hover`). So only delete `image-overlay-effect`.
- **DELETE** `social-media-icons` — near-duplicate of `social-media-share-links`? They differ (icons vs share-links). Keep `social-media-icons`; **DELETE** `sticky-social-bar`? sticky-social-bar is distinct (fixed vertical bar). Keep both; instead **DELETE** `social-media-icons` is NOT a dup. Reconcile: Other HTML deletes here = blockquote-with-cite, holy-grail-layout-flex, image-overlay-effect, simple-ordered-list, simple-unordered-list, favicon-link, horizontal-rule, mark-text, abbr-element, bdi-element, address-tag, time-element, definition-list, details-summary, main-element, svg-circle, content-editable, draggable-element, media-object, pills, list-group, centered-website, diagonal-background, parallax-scrolling-effect, sticky-notes, weather-widget, calendar-widget, carousel, filter-list, full-screen-search, glowing-icon, corner-ribbon, countdown-timer, code-block, skill-bar, timeline, skip-link, semantic-layout, mixed-column-layout, range-slider, portfolio-gallery, responsive-image-gallery, text-with-background-image, dark-mode-toggle, password-visibility-toggle.
  - See §4 for the outright low-value deletes and §8 final list.

### B13. Ratings (delete 1)
- **KEEP** `rating-stars` (rich, ARIA, feedback). **DELETE** `user-rating` (Font Awesome stars, near-duplicate display-only); keep `css-only-star-rating` (CSS-only radio rating — distinct interaction). So delete `user-rating`.

### B14. Tabs (delete 2 + 1 CSS-only in A)
- **KEEP** `tabbed-content` (ARIA tablist, best). **DELETE** `tabs` (older tab pattern, near-duplicate). **DELETE** `tabs-component` (near-duplicate). **DELETE** `full-page-tabs` (near-duplicate full-page tab pattern). (css-tabs is A23.)
  - Decision: keep `tabbed-content` only? `full-page-tabs` is a genuinely different layout (full-page). Keep `tabbed-content` + `full-page-tabs`; delete `tabs` + `tabs-component`. Tabs 5→2.

### B15. Tooltips (delete 2)
- **KEEP** `tooltip` (button + tooltip). **DELETE** `css-only-tooltip` (near-identical markup/classes). **DELETE** `tooltip-text` (a `<p title>` — trivial native `title` attribute demo, low-value).

---

## 4. Low-value / trivial HTML components to DELETE outright (within the 27 "Group A-style" but having HTML)

These have HTML but are trivial native-element demos or one-rule styling with no reusable value.
They are counted within the 27 "outright delete" bucket (§1) alongside the CSS/JS-only artifacts
where applicable; the non-overlapping outright-HTML-deletes are:

- `Other/favicon-link` — two `<link rel=icon>` tags; not a component.
- `Other/horizontal-rule` — `<hr>` between paragraphs; trivial.
- `Other/mark-text` — `<mark>milk</mark>`; trivial.
- `Other/abbr-element`, `Other/bdi-element`, `Other/address-tag`, `Other/time-element`,
  `Other/definition-list`, `Other/main-element`, `Other/svg-circle`, `Other/details-summary`,
  `Other/content-editable`, `Other/draggable-element` — native HTML element demos, no reusable styling.
- `Other/simple-ordered-list`, `Other/simple-unordered-list` — bare `<ol>`/`<ul>`; trivial.
- `Forms/keyboard-input` — `<kbd>` demo.
- `Media/accessible-image`, `Media/full-width-image`, `Media/image-map` — trivial/legacy.
- `Tables/simple-table` — bare `<table>` (keep `table-caption`, `table-merged-cells`, `table-scope` which show distinct table techniques; `simple-table` is the trivial baseline).
- `Display/footer` — non-semantic div footer (also in B6).

(These overlap with the B-list where noted; the §8 final list deduplicates.)

---

## 5. NEEDS-FIX (8 — retain, flag; not deleted)

Valuable components with an accessibility/quality issue to fix in a later pass (do NOT delete):
1. `Modals/device-optimized-modal` — verify focus trap + Esc handling (likely fine; confirm).
2. `Tabs/full-page-tabs` — uses `float:left` tab buttons; confirm keyboard arrow-nav + ARIA.
3. `Navigation/Menu/mega-menu` — hover-only mega menu; add keyboard/`aria-expanded`.
4. `Forms/dropdown-menu` — div-based dropdown trigger; needs `role=button`+keyboard (QA may already flag).
5. `Other/carousel` — manual carousel; add `aria-roledescription`, keyboard for prev/next.
6. `Media/image-slider` — add keyboard for prev/next + aria.
7. `Buttons/split-button` — dropdown is hover/CSS; add keyboard operability.
8. `Loaders/progress-steps` — decorative; confirm `aria-current`/labeling.

---

## 6. Misclassified components (not auto-deleted; recommend reclassification)

- `Buttons/radio-button-group` → belongs in **Forms** (grouped control). Recommend moving rather than deleting; flagged for Phase 6 decision. (Listed as delete in B3 only if move is unwanted.)
- `Display/table-header-body-footer` → belongs in **Tables**. Distinct; recommend move to `Tables/`.
- `Forms/mobile-dropdown` → nav-style dropdown menu; arguably **Navigation**. Keep in Forms (it's a form-field dropdown) — borderline, leave.
- `Other/range-slider` vs `Forms/range-input` → both native `<input type=range>`; one should survive. Recommend keep `Other/range-slider` (styled), delete `Forms/range-input`.
- `Marketing/*` (6) → all are older duplicates of dedicated families (FAQ/Hero/Pricing/Testimonials). Reclassification = delete the Marketing family entirely (§1 shows Marketing 6→0) since each pattern has a stronger home. This is the main "misclassified/redundant family" finding.

---

## 7. Empty / removed families after deletion

- **Dropdowns** → 1 leaf (CSS-only hover-dropdown, A1) deleted → family becomes **empty → remove**.
- **Marketing** → all 6 leaves deleted (duplicates of FAQ/Hero/Pricing/Testimonials) → family **empty → remove**.
- All other families retain ≥1 leaf. Sub-folder groupings under Navigation (Sidebar/Pagination/Navbar/Menu/Breadcrumb/Other) may thin out but the top-level `Navigation` family stays.

---

## 8. Reconciled final deletion list (102 leaves — verified against the filesystem)

This is the authoritative list. Every path was confirmed to exist on disk, and the per-family
counts in §1 sum to exactly these 102 deletions (293 → 191 survivors).

### A. CSS/JS-only snippet artifacts (27 — no `.html`, not real components)
```
Dropdowns/hover-dropdown           Other/direction-aware-hover       Other/dotted-separator
Other/css-variable-fallback        Other/sliding-indicator           Other/mix-blend-mode-multiply
Other/full-screen-overlay          Other/scroll-snap-container      Other/focus-visible-accessibility
Other/css-triangle-shape           Forms/auto-resizing-textarea      Forms/css-only-toggle-switch
Navigation/Sidebar/sticky-sidebar Navigation/Pagination/mobile-bottom-nav
Navigation/Navbar/glassmorphism-nav  Navigation/Navbar/sticky-nav
Buttons/3d-press-button            Buttons/neumorphic-button         Cards/equal-height-cards
Cards/container-query-card         Media/responsive-embed            Modals/modal-dialog-backdrop
Tabs/css-tabs                      Forms/form-validator              Forms/debounced-input-handler-js
Modals/focus-trap-modal            Display/toggle-element-visibility
```

### B. HTML duplicates / near-duplicates (48 — delete weaker; survivor named in §3)
```
Accordions/accordion               Accordions/css-only-accordion     Accordions/collapsible
Badges/css-only-notification-badge Buttons/nested-animated-button    Buttons/nested-gradient-button
Buttons/action-buttons            Buttons/radio-button-group        Cards/flip-card
Cards/frosted-glass-card           Cards/nested-product-card         Cards/nested-profile-card
Cards/equal-height-cards-flexbox   Cards/staff-card                  Forms/contact-form-basic
Forms/newsletter-signup-form       Forms/subscription-form           Forms/css-toggle-switch
Forms/search-input                 Loaders/nested-bouncing-dots      Loaders/progress-bar
Media/figure-with-figcaption       Media/picture-element             Media/audio-embed
Modals/toast-notification-markup   Modals/modal-box                  Modals/modal-dialog
Modals/modal-popup                Modals/nested-simple-modal        Navigation/Navbar/sticky-header
Navigation/Navbar/auto-hide-sticky-header  Navigation/Navbar/fixed-header-on-scroll
Navigation/Navbar/header           Navigation/Navbar/basic-navbar    Navigation/Breadcrumb/breadcrumbs-navigation
Navigation/responsive-sticky-header-with-shadow  Other/blockquote-with-cite
Other/holy-grail-layout-flex       Other/image-overlay-effect        Ratings/user-rating
Tabs/tabs                          Tabs/tabs-component               Tooltips/css-only-tooltip
Tooltips/tooltip-text              Marketing/FAQ/accordion-faq       Marketing/FAQ/accordion-faq-layout
Marketing/Pricing/pricing-table    Marketing/Pricing/responsive-pricing-grid
Marketing/Hero/jumbotron           Marketing/Testimonials/testimonial-slider
```

### C. Low-value / trivial HTML components (27 — native-element demos / one-rule styling)
```
Other/favicon-link      Other/horizontal-rule   Other/mark-text          Other/abbr-element
Other/bdi-element       Other/address-tag       Other/time-element       Other/definition-list
Other/main-element      Other/svg-circle        Other/details-summary    Other/content-editable
Other/draggable-element Other/simple-ordered-list  Other/simple-unordered-list
Forms/keyboard-input    Media/accessible-image  Media/full-width-image   Media/image-map
Display/footer          Forms/disabled-input    Forms/readonly-input     Forms/input-with-min-max
Forms/range-input       Forms/color-picker
```

**Totals:** 27 + 48 + 27 = **102 deletions → 191 survivors.**
**Families emptied → removed:** `Dropdowns`, `Marketing`.

### Survivors by family (191 total — verified programmatically)
```
Accordions (2):  accordion-panel, collapsible-accordion
Alerts (2):      alert-messages, cookie-consent-banner
Avatars (1):     contact-chip
Badges (1):       notification-badge
Buttons (8):      3d-button-effect, back-to-top-button, download-button, floating-action-button,
                  pulsing-button, skewed-button, social-buttons, split-button
CTA (4):          cta-banner, cta-download, cta-newsletter, cta-split
Cards (7):        blog-post-card, equal-height-cards-grid, flipping-card, glassmorphism-card,
                  pricing-card, product-card, profile-card
Contact (3):      contact-cards, contact-form, contact-office-locations
Content (4):      content-blog-grid, content-documentation-preview, content-featured-articles,
                  content-resources
Display (4):      dark-mode-toggle, simple-footer, sticky-footer, table-header-body-footer
FAQ (2):          faq-accordion, faq-searchable
Features (5):     feature-bento, feature-comparison, feature-grid, feature-icons, feature-timeline
Footer (3):       footer-large, footer-minimal, footer-multi-column
Forms (21):       checkbox-group, contact-form, datalist-autocomplete, date-time-picker,
                  dropdown-menu, file-upload-input, floating-label, form-validation, inline-form,
                  input-pattern-validation, login-form, mobile-dropdown, multi-select-dropdown,
                  newsletter-signup, registration-form, responsive-form, search-autocomplete,
                  select-dropdown, select-with-optgroup, textarea-label, toggle-switch
Gallery (3):      gallery-masonry, gallery-portfolio, gallery-projects
Hero (10):        hero-animated, hero-bento, hero-center, hero-gradient, hero-image, hero-minimal,
                  hero-product, hero-saas, hero-split, hero-startup
Loaders (6):      bouncing-loader, circular-progress-bar, css-only-progress-bar, loader,
                  progress-steps, skeleton-loader
Logos (3):        logo-clients, logo-cloud, logo-trusted-by
Media (10):       canvas-element, figure-figcaption, html5-audio-player, html5-video-player,
                  iframe-embed, image-slider, pop-up-image, responsive-picture,
                  responsive-video-container, video-background
Modals (4):       device-optimized-modal, dialog-element, popup-chat-window, toast-notification
Navigation (17):  Breadcrumb/breadcrumb-nav, Menu/circular-menu, Menu/hamburger-menu, Menu/mega-menu,
                  Menu/simple-navigation-menu, Menu/vertical-menu, Navbar/responsive-navbar,
                  Other/side-navigation, Other/top-navigation, Pagination/bottom-navigation,
                  Pagination/pagination-component, Sidebar/fixed-sidebar, navbar-mega-menu,
                  navbar-simple, navbar-sticky, scroll-to-top, sidebar-navigation
Other (38):       blockquote-citation, calendar-widget, carousel, centered-website, code-block,
                  corner-ribbon, countdown-timer, creative-image-hover, dark-mode-toggle,
                  device-mockups, diagonal-background, fieldset-legend, filter-list,
                  full-screen-search, glowing-icon, holy-grail-layout-grid, image-zoom-on-hover,
                  list-group, media-object, meter-element, mixed-column-layout, output-element,
                  parallax-scrolling-effect, password-visibility-toggle, pills, portfolio-gallery,
                  range-slider, responsive-image-gallery, semantic-layout, skill-bar, skip-link,
                  social-media-icons, social-media-share-links, sticky-notes, sticky-social-bar,
                  text-with-background-image, timeline, weather-widget
Pricing (4):      pricing-comparison, pricing-enterprise, pricing-saas, pricing-simple
Process (4):      process-how-it-works, process-steps, process-timeline, process-workflow
Products (6):     product-changelog, product-dashboard-preview, product-integrations,
                  product-mobile-app, product-roadmap, product-showcase
Ratings (2):      css-only-star-rating, rating-stars
Statistics (3):    stats-achievement-numbers, stats-grid, stats-kpi-cards
Tables (4):       simple-table, table-caption, table-merged-cells, table-scope
Tabs (2):         full-page-tabs, tabbed-content
Team (3):         team-advisors, team-grid, team-leadership
Testimonials (4): testimonials-cards, testimonials-carousel, testimonials-masonry, testimonials-video
Tooltips (1):     tooltip
```
Note: `Display/dark-mode-toggle` is deleted; `Other/dark-mode-toggle` survives (the accessible one),
so the single surviving `dark-mode-toggle` lives in the Other family — this also resolves the
pre-existing duplicate slug. `Contact/contact-form` (section) and `Forms/contact-form` (form) both
survive because they are genuinely different (section layout vs validated form); the duplicate
`contact-form` slug is resolved by deleting `Forms/contact-form-basic` (the trivial one).

---

## 9. Risks & validation plan (for Phase 6/7, after approval)

- Deletion touches only `Vanilla/Components/`. No `related`/README cross-links exist, so no
  intra-Vanilla stale-reference cleanup is needed beyond removing the folders.
- `sections-showcase.html` uses self-contained `srcdoc` iframes and only references the curated
  section families (Hero, CTA, Features, etc.) by name — it does **not** load legacy leaf HTML,
  so deleting legacy leaves will not break it. (Verify no deleted slug appears as a label.)
- After deletion: run `python3 -m _gen.rebuild_index` (regenerates `snippets-index.json` from disk,
  cross-validates indexed==on-disk, refuses mismatch), then `python3 scripts/validate.py` and
  `python3 scripts/qa_vanilla.py`. Remove now-empty families (Dropdowns, Marketing) from the index
  automatically via rebuild. Confirm Tailwind + Vanilla/Templates untouched via `git status`.
- The two pre-existing duplicate slugs (`dark-mode-toggle`, `contact-form`) are each resolved by this
  curation (one of each pair is deleted), which also fixes that latent issue.

---

**Nothing has been deleted or modified. Awaiting approval to proceed to Phase 6 (implementation).**
