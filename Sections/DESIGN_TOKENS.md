# DevSnips React Sections — Design Tokens & Standards

**Single Source of Truth** for the visual design system of every React Section.

This document governs every section in `React/Sections/` — heroes, feature grids, testimonials, pricing, logos, stats, FAQ, CTA, contact, footers, and every future section family.

It is a **child specification** of `React/DESIGN_TOKENS.md`. The root document owns the primitive and semantic token foundation (`--ds-*`); this document owns how those tokens compose into **page-level sections**, and how the four section design directions (Minimal, Dark Premium, Bento, Neo-Brutalist) express them without breaking the shared DevSnips design language.

It is authoritative for both human contributors and AI coding agents.
Read this file — and `React/DESIGN_TOKENS.md` — before creating or modifying any section.

---

## 0. NORMATIVE LANGUAGE & COMPLIANCE

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative:

| Keyword | Meaning |
|---------|---------|
| **MUST / MUST NOT** | Hard requirement. A violation is a defect that blocks shipping. Machine-checkable where possible. |
| **SHOULD / SHOULD NOT** | Strong default. Deviation requires a written justification in the section's README. |
| **MAY** | Genuinely optional, at the author's discretion within the stated bounds. |

Every rule in this document has one of three enforcement levels:

| Level | How it is enforced |
|-------|--------------------|
| **L1 — Automated** | Checkable by grep/static analysis or Playwright QA (token usage, banned patterns, overflow, contrast, focus rings). |
| **L2 — Structural** | Checkable by review of DOM/props (heading hierarchy, grid collapse maps, composition anatomy). |
| **L3 — Judgment** | Requires design review (restraint, realism, editorial quality). Judgment is exercised against the checklists here, not taste. |

A section ships only when **all L1 and L2 rules pass** and the §19 Definition of Done is fully checked.

---

## 1. DESIGN PHILOSOPHY

**"Neutral first, expressive second."**

React Sections MUST feel:

- **Premium** — considered, confident, never template-like
- **Editorial** — typography and layout carry the identity, not decoration
- **Modern** — current without chasing trends
- **Developer-focused** — honest, precise, information-dense where useful
- **Production-ready** — shippable as-is, not a mockup
- **Restrained rather than flashy** — one strong idea per section, executed well
- **Typography- and layout-driven** — hierarchy comes from scale, weight, spacing, and alignment
- **Consistent** — any two sections from the library MUST be able to sit on the same page without visual negotiation

### What a section is

A section is a **composed, full-width page region** built from React Components and semantic tokens:

```
Tokens → Components → Sections → Templates
```

Sections consume tokens and components. They MUST NOT invent new primitive values.

### Explicitly avoided (all are L1/L2 failures)

- Generic AI-generated SaaS aesthetics (purple gradient hero + glass card + blob)
- Excessive gradients; gradient text; gradient buttons
- Excessive rounded cards; radius above `radius-lg`
- Random glassmorphism (`backdrop-blur` card stacks)
- Unnecessary animations; looping background motion
- Inconsistent spacing; off-scale values
- Decorative elements without purpose
- Emoji as UI
- Fake versions of real brands; lorem ipsum

**A section should feel designed, not decorated.**

---

## 2. RELATIONSHIP TO THE ROOT TOKEN SYSTEM

`React/DESIGN_TOKENS.md` owns the foundation. This document **references, never redefines**, those tokens.

| Layer | Owner | Examples |
|-------|-------|----------|
| Primitive tokens | Root spec | `neutral-900`, `spacing-4`, `radius-md` |
| Semantic tokens | Root spec | `color.background`, `color.foreground`, `color.border` |
| Component tokens | Root spec | `button.primary.background` |
| **Section tokens** | **This document** | `section.padding-y`, `section.container`, `section.heading` |
| Direction overrides | This document | Minimal / Dark Premium / Bento / Neo-Brutalist token sets |

### Rules (all L1)

1. Sections **MUST** consume semantic tokens (`var(--ds-color-*)`, `var(--ds-spacing-*)`, …) via Tailwind arbitrary values, exactly like React Components (`bg-[var(--ds-color-surface)]`, `rounded-[var(--ds-radius-md)]`).
2. Sections **MUST NOT** hard-code hex, rgb, or hsl values. The only permitted literal is `#000` inside `color-mix()` for hover darkening, per the root spec.
3. Section-level tokens (§6, §8, §10) are **compositions** of root tokens — they add no new colors, radii, or shadows.
4. The four design directions (§4) are **token override sets**, not new design systems. They re-map the same semantic slots; they MUST NOT add slots.
5. Dark mode MUST work through the same semantic tokens in every direction. No direction may require separate markup per theme.
6. Raw Tailwind palette classes (`bg-blue-500`, `text-gray-700`, `border-neutral-200`, …) are **banned** in section code — they bypass theming. Token arbitrary values only.

---

## 3. COLOR SYSTEM

### 3.1 Neutral palette (L1)

The neutral palette is inherited unchanged from the root spec (`neutral-0` → `neutral-1000`). Neutrals do ≥90% of the work in every section.

| Role | Light theme | Dark theme | Min contrast vs. canvas |
|------|-------------|------------|--------------------------|
| Page canvas | `neutral-50` / white | `neutral-950` | — |
| Section surface | white / `neutral-100` | `neutral-900` | — |
| Raised surface | white + 1px border | `neutral-900` + 1px border | — |
| Primary text | `neutral-900` | `neutral-50` | ≥ 7:1 (AAA target) |
| Secondary text | `neutral-600` | `neutral-400` | ≥ 4.5:1 |
| Muted text | `neutral-500` | `neutral-500` | ≥ 4.5:1 — floor for meaningful text |
| Borders | `neutral-200`–`300` | `neutral-800` / white @ 8–12% | ≥ 3:1 for interactive boundaries |

Nothing below muted contrast may carry meaningful text. Placeholder-style faint text (`/40`, `/50` opacity tricks) is an L1 failure.

### 3.2 Background and surface tokens

| Token | Purpose |
|-------|---------|
| `color.background` | Page canvas behind everything |
| `color.surface` | Default section surface (cards, panels inside sections) |
| `color.surface-subtle` | Alternate section band (zebra striping between adjacent sections) |
| `color.surface-elevated` | Floating elements above a section (dropdowns, sticky bars) |
| **`section.canvas`** | The section's own background — usually `color.background`, MAY be `color.surface-subtle` or a direction surface |
| **`section.band`** | A full-bleed tinted band — the only sanctioned way to change background between sections |

Rules (L2):

- Adjacent sections alternate `section.canvas` / `section.band` **at most**. Three different adjacent backgrounds is a defect.
- A section has **exactly one** background. No background inside background inside background.
- Full-bleed dark bands (e.g. a dark CTA on a light page) are the primary sanctioned "expressive" move — **at most one per page**.
- Elevation inside a section steps at most **two levels** above `section.canvas` (canvas → surface → elevated). Deeper stacks are a defect.

### 3.3 Text tokens (L1)

| Token | Use |
|-------|-----|
| `color.foreground` | Section headings, primary body |
| `color.muted-foreground` | Ledes, descriptions, captions, metadata |
| `color.primary` | Links and key actions only |

- Headings are always `color.foreground`. Gradient text is banned. Accent-colored headings are banned (Neo-Brutalist label conventions excepted, §4.5).
- Text inside dark bands uses the same semantic tokens, flipped by theme — never a parallel hard-coded palette.

### 3.4 Border colors (L1)

| Token | Use |
|-------|-----|
| `color.border` | Default hairlines: card borders, dividers, grids |
| `color.border-subtle` | Quiet internal dividers |
| `color.border-strong` | Emphasis: active, selected, featured, Neo-Brutalist hard borders |

Borders — not shadows — are the primary separation mechanism in sections (§9).

### 3.5 Accent colors — the One-Accent Law (L1/L2)

- **One accent per section. Ever.** The accent arrives from the consuming context via `color.primary` / `color.accent`. Sections MUST render correctly with any controlled accent: neutral, blue, green, orange, violet, cyan, red.
- The accent MAY appear in **at most three element types** per section, chosen from: primary CTA, selected/active indicator, one key highlight (a stat number, an eyebrow tick, a featured-tier marker).
- The accent MUST NOT appear in: whole-card backgrounds, headings, decorative shapes, icon recoloring en masse.
- **Area budget**: accent-colored pixels SHOULD be ≤ 5% of the section's rendered area (Neo-Brutalist excepted, §4.5).
- Accent surface tints (badges, soft chips) MUST derive from tokens: `color-mix(in srgb, var(--ds-color-accent) 8–12%, var(--ds-color-surface))`. Never a new hex.
- Status colors (`success` / `warning` / `destructive` / `info`) appear only where they mean something. A feature grid is not a status board.

### 3.6 Direction accent defaults

| Direction | Default accent posture |
|-----------|------------------------|
| Minimal | Near-neutral; accent for CTA and links only |
| Dark Premium | One luminous-but-muted accent on dark canvas; CTA + ≤1 data highlight |
| Bento | Accent in at most 1–2 cells of a grid |
| Neo-Brutalist | Flat saturated blocks (§4.5) — the one direction where accent may fill surfaces |

---

## 4. THE FOUR DESIGN DIRECTIONS

Every section family ships in up to four directions. The directions share **structure, spacing scale, typography scale, grid, breakpoints, and accessibility rules**. They differ **only** in surface treatment, border language, radius, elevation, and accent usage.

### 4.0 Direction parity invariant (L2)

The same section family across directions MUST share:

- The same DOM structure and semantic elements
- The same props/API surface
- The same content slots and responsive collapse behavior
- The same accessibility tree

Directions differ by token remapping and the bounded stylistic deltas below — never by re-architecting the section.

### 4.1 Direction matrix

| | Minimal | Dark Premium | Bento | Neo-Brutalist |
|---|---------|--------------|-------|---------------|
| Canvas | `color.background` (light) | `neutral-950` | Light or dark | Flat cream / light |
| Surface lift | None — canvas + hairlines | +1 step, 1px white/8–12% border | Cells: `color.surface` + 1px border | Flat blocks, 2px border |
| Border width | 1px | 1px | 1px | 2px uniform |
| Radius | `sm` controls / `md` surfaces | `md` | `md`–`lg` | `none` (square) |
| Elevation | None (floating: `shadow-sm`) | None — borders carry lift | Hover: `shadow-xs` max | Hard offset, 0 blur |
| Accent | CTA/links only | CTA + ≤1 highlight | ≤2 cells | 1 primary + ≤2 supporting fills |
| Type posture | Quiet, generous measure | Tight tracking, high contrast | Compact, scannable | 700 headings, uppercase mono labels |
| Gradients | None | Static radial tint ≤8% max | None | None (flat color) |
| Motion | Color/border fades only | Fade/settle only | Cell hover lift only | Press-down translate |

### 4.2 Minimal — the reference direction

If a section works in Minimal, its structure is sound. Minimal is the default answer to "how should this look?"

- Canvas: `color.background`; bands in `color.surface-subtle` at most.
- Separation by **whitespace and 1px hairlines** (`color.border`), not cards.
- Content MAY sit directly on the canvas. Cards only when grouping genuinely adds meaning (§11).
- Radius: `radius-sm` controls, `radius-md` contained surfaces. Shadows: none except `shadow-sm` on truly floating elements.
- Generous vertical rhythm (§8). **The design is the spacing.**

### 4.3 Dark Premium

Premium dark surfaces for product heroes, CTAs, and showcase sections.

- Canvas: `neutral-950`–`900`. Surfaces lift **exactly one step** above canvas with a 1px border (white at 8–12% opacity), never with shadows or glow.
- Text: `neutral-50` headings, `neutral-400` body. All pairings MUST still pass §13 contrast minimums.
- One accent: CTA + at most one data/highlight element.
- **Banned without exception**: neon, glow, purple haze, animated mesh backgrounds, starfields, particle fields.
- Atmosphere ceiling (MAY): **one** static radial tint, ≤8% opacity, monochrome or single-accent, behind content, never animated (§9.4).
- Dark Premium sections MUST still consume semantic tokens — the direction is a theme mapping, not a hard-coded dark page.

### 4.4 Bento

Modular cell grids for features, integrations, and product overviews.

- **One grid per section**: 12-column base; cells span 3–8 columns and 1–2 rows.
- Cells: `color.surface`, 1px `color.border`, `radius-md` (product) or `radius-lg` (spacious marketing — pick one per family), padding `spacing-6` (24px) mobile / `spacing-8` (32px) desktop.
- Gap: uniform — `spacing-4` (16px) mobile, `spacing-6` (24px) desktop. Mixed gaps in one grid are an L2 defect.
- Cell content: **one idea per cell** — icon or small visual, `heading-sm`–`heading-md` title, `body-sm`–`body-md` description of 1–2 sentences.
- At most **one hero cell** (span 6–8) per grid. At most **2 cells** may carry accent tint.
- Cells align to the grid. Rotated, overlapping, or out-of-grid floating cells are banned.
- Hover: `border-strong` or `shadow-xs` lift only. No scale, no tilt, no glow.

### 4.5 Neo-Brutalist

The expressive ceiling of the system — bold but **disciplined**.

- Canvas: flat warm off-white (cream tint mapped from tokens) or `color.background`. Flat means flat: no gradients, no textures, no noise.
- Borders: **2px solid** `color.border-strong`, uniform — every bordered element in the section uses the same 2px weight. Mixed 1px/2px/3px is an L1 defect.
- Radius: `radius-none`. Square corners everywhere, including inputs, buttons, media, chips.
- Shadows: hard offset only — `4px 4px 0 0` (default) or `8px 8px 0 0` (hero elements), solid `color.border-strong`, **zero blur, zero spread variation**. Soft shadows anywhere in the direction are an L1 defect.
- Accent: flat saturated fills (yellow / pink / lime / cyan family) on chips, badges, buttons, and at most one background block per section. **One primary accent + at most two supporting accent colors.** Text on accent fills MUST pass AA (usually near-black text).
- Typography: headings MAY be 700; eyebrow/labels uppercase with +0.05em tracking; mono for metadata, tags, numbers.
- Interaction: press-down — on `:active` the element translates by the shadow offset (`translate(4px,4px)` / `(8px,8px)`) and the shadow collapses to `0 0 0 0`. Duration ≤100ms. No grow, no glow.
- Brutalism is not a license for chaos: §3.5's discipline applies with the direction's stated caps.

### 4.6 Shared invariants (all four directions, L1/L2)

These never change between directions:

- Semantic token consumption (no hard-coded values)
- Type scale and font stacks (§5)
- Spacing scale and section rhythm (§6, §8)
- Container widths and breakpoints (§10, §12)
- One-Accent Law (§3.5, with §4.5's stated caps)
- Accessibility requirements (§13)
- Motion constraints (§14)
- Content realism (§15)

---

## 5. TYPOGRAPHY

Sections inherit the root type scale and extend it with section-level roles. Section typography is the main carrier of the editorial feel. All values below are **exact** — not ranges.

### 5.1 Font families (L1)

| Role | Stack | Use |
|------|-------|-----|
| Sans (default) | System UI / Inter / Geist | Everything by default |
| Mono | `ui-monospace`, SF Mono, Menlo, Consolas, monospace | Eyebrows, metadata, stats labels, code, Neo-Brutalist details |
| Display (optional) | Same as sans, or one editorial face per direction | Hero headings only — never body |

- A section uses **at most two families** (sans + mono). Three is an L2 defect.
- Sections MUST NOT introduce a webfont dependency by default; the system stack is the baseline. A direction-level display face is a documented exception.

### 5.2 Section type roles (L1 — exact spec)

| Role | Size (fluid) | Line height | Weight | Tracking | Use |
|------|--------------|-------------|--------|----------|-----|
| `section.eyebrow` | 12px | 1.3 | 600 | +0.05em, uppercase | Category label above the heading |
| `section.display` | `clamp(2.5rem, 1.9rem + 2.8vw, 3.5rem)` (40→56px) | 1.1 | 600–700 | −0.02em | Hero headline — **one per page** |
| `section.heading` | `clamp(1.875rem, 1.65rem + 1vw, 2.25rem)` (30→36px) | 1.15 | 600 | −0.02em | Standard section heading |
| `section.heading-sm` | 24px | 1.25 | 600 | −0.01em | Sub-section / compact heading |
| `section.lede` | `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)` (16→18px) | 1.5 | 400 | 0 | The one supporting paragraph under a heading |
| `section.body` | 14px | 1.5 | 400 | 0 | Card text, descriptions |
| `section.caption` | 12px | 1.4 | 400 | 0 | Metadata, footnotes, logo-row labels |
| `section.stat` | `clamp(1.75rem, 1.5rem + 1.2vw, 2.25rem)` (28→36px) | 1.2 | 600 | −0.02em, `tabular-nums` | Big numbers in stats sections |

### 5.3 Weights and line heights (L1)

- Weights: **400 / 500 / 600 / 700 only**. 300 and 800+ are banned. 700 is reserved for display/heading emphasis and Neo-Brutalist labels.
- Line heights MUST follow §5.2 exactly. `line-height: 1` on display type is banned — glyph boxes overflow and collide (known defect class).
- Tracking: headings MAY tighten to −0.02em maximum. Body text is never tracked. Positive tracking only on uppercase eyebrow/labels.
- Numeric data in stats/pricing/tables MUST use `tabular-nums`.

### 5.4 Measure and hierarchy (L2)

- Heading + lede blocks are capped at **56–68 characters** (`max-w-xl`–`max-w-2xl`). A heading never spans the full container unless it is genuinely that long.
- One heading per section, one lede. A section needing three paragraphs of explanation is doing too much — split it.
- Hierarchy is built from size + weight + spacing. Never from color alone, never from gradient text, never from font-size roulette (more than 4 distinct type roles in one section is an L2 defect).

---

## 6. SPACING SCALE

Sections use the root 4px-based scale unchanged: `spacing-1` (4px) → `spacing-24` (96px). **Off-scale values are an L1 defect.**

Section-specific spacing semantics (exact):

| Concept | Value | Use |
|---------|-------|-----|
| `section.header-gap` | 12px (eyebrow→heading), 16px (heading→lede) | Header block internal rhythm |
| `section.header-margin` | 48px mobile / 64px desktop | Header block → content region |
| `section.content-gap` | 24px (grids, cards) / 32px (major regions) | Grid gaps, card gaps |
| `section.inline-gap` | 8px (icon+text) / 12px (chip rows, button groups) | Inline clusters |
| `section.gutter` | 16px (<640px) / 24px (640–1023px) / 32px (≥1024px) | Horizontal page margins |
| `section.padding-y` | §8 | Vertical section rhythm |

Rules (L1/L2):

- **No arbitrary values.** If a gap isn't on the scale, the layout is wrong, not the scale.
- Vertical rhythm inside a section descends strictly: `header-margin` > `content-gap` > `header-gap` > `inline-gap`.
- Identical elements in a row/grid have identical gaps. A grid with three different gaps is a defect.
- Margin collapsing hacks, negative-margin nudges, and `mt-[-2px]`-style optical corrections are banned; fix the rhythm instead.

---

## 7. BORDER RADIUS & BORDER WIDTHS

### 7.1 Radius (L1)

| Context | Radius |
|---------|--------|
| Buttons, inputs, chips | `radius-sm` (4–6px) |
| Cards, cells, panels | `radius-md` (8px) |
| Large marketing surfaces (Bento hero cells) | `radius-lg` (12px) — ceiling |
| Media thumbnails inside cards | `radius-sm`–`md`; nested radius MUST be < parent radius |
| Avatars, pills | `radius-full` |
| Neo-Brutalist (everything) | `radius-none` |

- Radius is uniform within a section: cards in one grid share one radius value.
- 24px+ "squircle" cards are banned. Mixed radius language (rounded cards + square buttons) within a direction is banned — Minimal's sole exception: square-edged media inside `radius-md` cards.

### 7.2 Border widths (L1)

| Context | Width |
|---------|-------|
| Default hairlines, cards, dividers | 1px |
| Emphasis (selected, featured, focus-adjacent) | 1px `border-strong`, or 2px where the direction allows |
| Neo-Brutalist | 2px everywhere, uniformly |

Dividers between list items and columns are 1px `color.border` — borders do the work shadows don't.

---

## 8. SECTION SPACING & VERTICAL RHYTHM

Section vertical padding is the strongest consistency signal across a page. Values are **exact**:

| Context | Mobile (<768px) | Tablet (768–1023px) | Desktop (≥1024px) | Fluid form |
|---------|-----------------|---------------------|-------------------|------------|
| `section.padding-y` standard | 64px | 80px | 96px | `clamp(4rem, 3rem + 4vw, 6rem)` |
| `section.padding-y` compact (logos, stat strips) | 40px | 48px | 64px | `clamp(2.5rem, 2rem + 2vw, 4rem)` |
| `section.padding-y` hero | 80px | 96px | 128px | `clamp(5rem, 3.5rem + 6vw, 8rem)` |
| Footer | 48px | 64px | 64px | — |

Rules (L1/L2):

- Top and bottom padding are equal within a section (heroes MAY add extra top for nav clearance — the only asymmetry allowed).
- Adjacent sections never both add `header-margin`-scale separation — separation comes from `padding-y` alone.
- Compact sections use compact rhythm; don't inflate them to standard.
- First/last sections on a page keep the same rhythm — no special-casing that breaks the beat.
- The fluid `clamp()` forms are the canonical implementation; the stepped values are the acceptance criteria at QA widths.

---

## 9. ELEVATION, SHADOWS, GRADIENTS, Z-INDEX

### 9.1 Shadow scale (L1 — exact values)

| Token | Value | Section use |
|-------|-------|-------------|
| `shadow-none` | — | Default for all section surfaces |
| `shadow-xs` | `0 1px 2px rgb(0 0 0 / 0.05)` | Bento cell hover (max) |
| `shadow-sm` | `0 1px 2px rgb(0 0 0 / 0.06), 0 2px 4px rgb(0 0 0 / 0.04)` | Floating elements, sticky bars |
| `shadow-md` | `0 4px 12px rgb(0 0 0 / 0.08)` | Dropdowns/popovers inside sections — ceiling |
| `shadow-nb-sm` | `4px 4px 0 0 var(--ds-color-border-strong)` | Neo-Brutalist default |
| `shadow-nb-lg` | `8px 8px 0 0 var(--ds-color-border-strong)` | Neo-Brutalist hero elements |

- Static cards and surfaces have **no shadow**. "Featured" elevation is expressed with `border-strong`, not bigger shadows.
- In dark themes, shadows recede further: borders carry elevation. `shadow-md`+ on dark canvas is a defect.
- Diffuse, colorful, or long soft shadows (`0 20px 50px rgb(0 0 0 / 0.15)`) are banned everywhere.

### 9.2 Z-index scale (L1)

| Layer | Value |
|-------|-------|
| Section content | 0 (auto) |
| Sticky section nav / bars | 10 |
| Overlays / backdrops | 40 |
| Dropdowns / popovers | 50 |
| Dialogs / drawers | 60 |
| Toasts | 70 |

Arbitrary z-index values (`z-[999]`) are banned. Sections SHOULD NOT need z-index beyond this scale.

### 9.3 Gradients (L1)

**Default: none.**

- No gradient text. No gradient buttons. No gradient card backgrounds. No rainbow meshes. No animated gradients anywhere.
- Sanctioned exceptions, all bounded:
  1. **Dark Premium atmosphere**: one static radial tint, ≤8% opacity, behind content, monochrome or single-accent. Static — never animated.
  2. **Media placeholders**: a subtle two-stop linear gradient inside an image placeholder where a real image would ship.
  3. **Chart fills**: single-hue alpha fades in data visualization.
- If a section "needs" a gradient to look good, the typography and spacing are undercooked. Fix those first.

### 9.4 Textures and decoration (L2)

- No blobs, squiggles, confetti, grid-paper backgrounds, noise overlays, or glow orbs by default.
- Allowed functional texture: 1px hairline rule systems (editorial dividers); in Neo-Brutalist, the flat-color block.
- Every visual element MUST answer "what does this communicate?" Decoration without an answer is removed.

---

## 10. CONTAINERS, GRID SYSTEMS, LAYOUT

### 10.1 Container widths (L1 — exact)

| Token | Value | Use |
|-------|-------|-----|
| `section.container` | 1280px max | Default section container |
| `section.container-wide` | 1440px max | Expansive marketing heroes, galleries |
| `section.container-narrow` | 768px max | FAQ, single-column content, forms |
| `section.measure` | 65ch (within `max-w-xl`–`max-w-2xl`) | Heading+lede blocks, prose |

- The container is centered (`margin-inline: auto`) and padded by `section.gutter` (§6).
- **One container per section.** Nested max-widths inside the container only for `section.measure` text blocks. Nested containers with competing max-widths are an L2 defect.
- Full-bleed is for backgrounds and bands — content still lands in a container.

### 10.2 Grid systems (L2)

| Pattern | Spec | Use |
|---------|------|-----|
| 12-column | `grid-cols-12`, gap 24px | Complex/editorial layouts, bento base |
| Even columns | 2 / 3 / 4 cols, gap 24–32px | Feature grids, logos, team, testimonials |
| Split | 5/7 or 6/6 of 12 | Hero copy + visual, content + media |
| Asymmetric editorial | 4/8 or 3/9 of 12 | Editorial content, case-study style |
| Bento | 12-col, spans 3–8, rows 1–2 | §4.4 |

Rules:

- Grids never rely on fixed heights; rows size to content. Cells in a row MAY stretch for equal height.
- Alignment: text blocks left-aligned by default. Centered layouts are allowed for heroes, CTAs, and compact sections — **one alignment per section header**, not both.
- Absolutely-positioned overlapping content cards as a layout strategy are banned. Layered visuals inside a single hero cell are the ceiling.
- `gap` utilities only — no margin-based grid spacing.

---

## 11. SECTION COMPOSITION RULES

### 11.1 Anatomy (L2)

A well-formed section is exactly:

```
<section>                     ← semantic element, aria-labelledby → heading
  container
    header block              ← eyebrow? + heading + lede?  (left OR centered)
    content region            ← grid / split / list / media
    actions?                  ← 1 primary + at most 1 secondary CTA
</section>
```

- **Eyebrow**: optional; mono/uppercase overline, MAY carry a small accent tick. It names the section; it doesn't sell.
- **Heading**: required (accessibility + hierarchy). Visually hidden only with a real accessible substitute.
- **Lede**: optional and singular.
- **Actions**: at most two. Primary uses `color.primary`; secondary is ghost/outline. Three-button hero rows are a defect.
- **Media**: product visuals, code blocks, or real imagery — purposeful, bordered like surrounding surfaces, `aspect-ratio` reserved (§16), never floating decoration.

### 11.2 Composition do / don't (L2/L3)

| Do | Don't |
|----|-------|
| One idea per section | Cram features + stats + testimonials + CTA into one section |
| Consistent internal grid | Mix 3-col and 4-col grids in one content region |
| Realistic content (plausible product names, honest copy) | Lorem ipsum, "Awesome Feature #1", emoji bullets |
| Compose with React Components (Button, Badge, Accordion, Tabs, Card) | Re-implement control primitives inside a section |
| Semantic HTML5 (`section`, `header`, `figure`, `ul`) | Div soup with click handlers |
| Let whitespace separate | Wrap everything in bordered cards |

### 11.3 Family-specific standards

- **Hero**: one `section.display` headline per page. Visual is a product artifact (UI panel, code, media), not abstract shapes. CTAs ≤ 2.
- **Features**: 3–6 items for even grids; bento for 5–8 mixed-weight items. Icon + title + one-sentence description.
- **Logos**: monochrome, uniform optical size, `section.caption` label. Marquee only with hover-pause and reduced-motion stop.
- **Stats**: 3–4 numbers, `section.stat` + caption label, `tabular-nums`.
- **Testimonials**: quote + attribution (name, role, company). Avatar optional. Star ratings only when reviews are the subject.
- **Pricing**: 2–4 tiers; at most one highlighted tier via `border-strong` (never a gradient). Feature lists are real `<ul>`.
- **FAQ**: compose the Accordion component. `container-narrow`.
- **CTA**: the sanctioned expressive peak — dark band or accent block allowed. Still one heading, one lede, ≤2 actions.
- **Footer**: quiet. Multi-column link lists, `body-sm`, muted. Giant decorative wordmarks only with editorial justification.

---

## 12. RESPONSIVE STANDARD

### 12.1 Breakpoints (L1 — exact, aligned with root spec and Tailwind)

| Name | Min-width | Role |
|------|-----------|------|
| Base (mobile) | 0 | Single column, stacked |
| `sm` | 640px | 2-col grids begin |
| `md` | 768px | Tablet: halved grids, tighter rhythm |
| `lg` | 1024px | Desktop: full grids, splits engage |
| `xl` | 1280px | Container caps |
| `2xl` | 1536px | Wide container cap only — **no layout change** |

### 12.2 Grid collapse map (L2 — mandatory behavior)

| Pattern | ≥1024px | 640–1023px | <640px |
|---------|---------|------------|--------|
| 4-col even | 4 | 2 | 1 |
| 3-col even | 3 | 2 (or 1) | 1 |
| 2-col even | 2 | 2 (or 1) | 1 |
| Split (5/7, 6/6) | side-by-side | stacked, copy first | stacked, copy first |
| Editorial (4/8, 3/9) | side-by-side | stacked | stacked |
| Bento | authored spans | 2-col equal | 1-col |

Collapse happens **by halving** at `sm` and `lg`. Custom per-cell breakpoint choreography is a defect.

### 12.3 Rules (L1/L2)

- **Mobile-first**: base styles are the mobile layout; breakpoints enhance. Desktop-first `max-width` media logic is banned.
- **Zero horizontal overflow** at every QA width: **320, 375, 768, 1024, 1280, 1440px**. This is an L1 Playwright gate.
- Display type scales via the §5.2 `clamp()` forms; body text never shrinks below `body-md` (14px).
- `section.padding-y` follows §8 exactly — rhythm compresses, never collapses to zero.
- Touch targets ≥ 44×44px on mobile. Stacked CTAs go full-width below `sm`.
- Long unbroken strings (URLs, hashes, tokens) MUST wrap (`break-words`) — no 375px blowouts.
- Marquees and wide tables scroll internally; they never widen the page.
- Sticky/fixed elements inside sections MUST NOT cover content at any QA width.

---

## 13. ACCESSIBILITY STANDARD

Non-negotiable, all directions (L1 unless noted):

- **Contrast**: WCAG AA minimum — **4.5:1** body text (7:1 AAA target for primary text), **3:1** large text and interactive boundaries. This binds Dark Premium muted text and Neo-Brutalist accent fills equally. Verified by measurement, not eyeballing.
- **Headings**: one logical hierarchy; a section's heading level fits the page outline (`h1` hero → `h2` sections → `h3` sub-blocks). No skipped levels (L2).
- **Landmarks**: `<section>` with `aria-labelledby` pointing at its heading when the heading exists (L2).
- **Keyboard**: every interactive element reachable and operable; focus order matches visual order (L2).
- **Focus ring**: 2px solid `color.focus-ring`, offset 2px, via `:focus-visible` — and it MUST remain ≥3:1 against every canvas, including dark bands and Neo-Brutalist accent fills.
- **State without color**: selected, error, success, and featured states use border/weight/icon/text in addition to color.
- **Media**: informative images get alt text; decorative visuals are `aria-hidden`. Icon-only controls have accessible names.
- **Motion**: `prefers-reduced-motion` honored everywhere (§14).
- **Lists**: feature lists, logo rows, footers use real `ul/ol` semantics (L2).
- **Forms** inside sections (newsletter, contact): real `label htmlFor`, described errors, native inputs — per the React Forms rules.
- **Touch targets**: ≥44×44px (WCAG 2.5.5) wherever feasible.

---

## 14. MOTION STANDARD

Motion in sections is **functional feedback**, not entertainment.

### 14.1 Motion tokens (L1 — exact)

| Token | Value | Use |
|-------|-------|-----|
| `duration-fast` | 100ms | Micro feedback, press states |
| `duration-default` | 150ms | Hover color/border/background |
| `duration-slow` | 250ms | Disclosure, small layout settles |
| `duration-max` | 300ms | Absolute ceiling for any section motion |
| `easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default |
| `easing-enter` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrances (opacity + ≤8px translate) |

### 14.2 Allowed motion (L1/L2)

| Context | Allowed |
|---------|---------|
| Hover (cards, cells, links, buttons) | Color/border/background transitions, `duration-default` |
| Bento cell hover | `border-strong` or `shadow-xs` lift — no scale, no tilt |
| Neo-Brutalist press | Translate by shadow offset on `:active`, shadow collapses, ≤100ms |
| Disclosure (FAQ accordions) | Grid-rows `0fr↔1fr`, 200–300ms, per the Accordion component |
| Marquee (logos) | Slow linear loop, pauses on hover, **stops** under reduced motion |
| Scroll reveal | SHOULD NOT be used. If justified: single opacity + ≤8px translate, once, ≤300ms, disabled under reduced motion |

### 14.3 Banned motion (L1)

- Parallax, scroll-jacking, pinned scroll narratives
- Looping background animations (gradient drift, floating blobs, particle fields)
- Staggered cascade entrances on every card
- Animated gradients anywhere
- `transition: all`
- Animating `width`/`height`/`top`/`left`/`margin` (the grid-rows disclosure trick is the sole exception)
- `will-change` left permanently on static elements

### 14.4 Reduced motion (L1)

Under `prefers-reduced-motion: reduce`: all non-essential motion becomes instant or opacity-only; marquees stop; reveals render in final state immediately. Verified in QA, not assumed.

---

## 15. CONTENT & REALISM STANDARD (L3)

- Copy is plausible and specific: real-ish product language, believable names, honest numbers.
- No lorem ipsum, no "Lorem feature dolor", no emoji anywhere in UI.
- Logo rows use abstract/invented wordmarks, styled uniformly — never fake versions of real brands.
- Code shown in developer-focused sections is syntactically real and uses the mono stack.
- Images: purposeful product/media slots with consistent aspect ratios (16:9, 4:3, 1:1), bordered per direction, `object-cover`, lazy-loaded.
- Numbers in stats/pricing are internally consistent (a "12k customers" stat doesn't sit under a "3 companies" logo row).

---

## 16. IMPLEMENTATION RULES (React + Tailwind) — L1

Sections follow the React Components stack exactly:

- **TypeScript-first**: `code.tsx` primary, `code.jsx` parity build. **No `any`.**
- **Tailwind-first** with token arbitrary values: `bg-[var(--ds-color-surface)]`, `py-[clamp(4rem,3rem+4vw,6rem)]`, `rounded-[var(--ds-radius-md)]`.
- **Banned**: raw palette utilities (`bg-blue-500`, `text-gray-600`), inline `style=` for static values, `!important`, component-specific CSS files. Scoped `<style>` only if a keyframe/marquee genuinely requires it.
- **Composition over configuration**: sections import and compose React Components (Button, Badge, Accordion, Tabs, Card) rather than re-building them.
- **Controlled accent**: sections read accent from tokens; nothing assumes a specific hue.
- **Both themes by token flip alone** — verified in QA, light and dark.
- **No layout shift**: media reserves `aspect-ratio`; fonts are system-stack by default so there is no FOUT-driven reflow.
- **No runtime layout measurement** for static layouts; measure-in-effect patterns only where interaction genuinely requires them.

### 16.1 Required files per variant (L1/L2)

Every section variant folder ships exactly:

```
React/Sections/<Family>/<variant-slug>/
├── code.tsx          ← authored, single source of truth
├── metadata.json     ← declares family, direction, token compliance (§17.13)
└── preview.html      ← generated, self-contained runnable demo
```

`code.tsx` is the only authored file; `preview.html` is **generated from it** — never hand-edited.

### 16.2 preview.html standard (L1)

Each `preview.html` is a self-contained, double-click-runnable demo that renders the **actual** `code.tsx` (not a copy, not a mock), following the React Components preview architecture:

- **Stack**: Tailwind CDN + React 18 UMD + Babel standalone — the same runtime the React Components previews use. No build step, no bundler, no network API calls.
- **Tokens**: the canonical `--ds-*` token block (light + dark `[data-theme="dark"]`) is inlined before paint, identical to the React Components previews, so the section renders exactly as it would inside a consuming app.
- **Fidelity**: `code.tsx` is inlined after a deterministic transform (types stripped, imports/exports removed) so the preview is byte-identical in behavior and classes to the shipped source.
- **Mount**: sections render **full-bleed** (a section is a full-width page region — it MUST NOT be squeezed into a constrained component-showcase column).
- **Theme toggle**: a persisted, no-flash light/dark page toggle is required, so both themes are demonstrable. Directions that pin a theme mapping (§4.3 Dark Premium) keep their pin on the section root and are shown holding it across page-theme toggles.
- **Generation**: previews are produced by the family's `_gen_react_sections_*` generator (modeled on `_gen_react_buttons.py`); `--check` mode flags drift and fails CI. Build-time tools (esbuild) stay outside the repo.

---

## 17. CONSISTENCY INVARIANTS (machine-checkable)

The following hold for **every** section in the library and are intended to be enforced by automated QA:

1. Zero hex/rgb/hsl literals outside `color-mix(..., #000)` hover darkening.
2. Zero raw Tailwind palette utilities (color, spacing off-scale, arbitrary radii).
3. Zero `transition: all`, zero `!important`, zero `z-[n]` outside §9.2.
4. Exactly one heading element per section; heading level follows §13.
5. Every `<section>` carries `aria-labelledby` when a visible heading exists.
6. Every grid uses `gap` tokens from §6; no margin-based grid spacing.
7. Every interactive element has a `:focus-visible` ring per §13.
8. Every animated/transitioned element is guarded by a `prefers-reduced-motion` rule.
9. Zero horizontal overflow at 320/375/768/1024/1280/1440px, light and dark.
10. Text contrast per §13 at every text/canvas pairing, both themes.
11. TSX strict-passes; JSX parity build matches exports and props.
12. Direction parity per §4.0 across a family's directions.
13. `metadata.json` declares the direction, family, and token compliance.
14. No emoji, no lorem ipsum, no external image dependencies that can rot (self-contained or placeholder-safe).

---

## 18. ANTI-PATTERN CHECKLIST

A section fails review if it has any of:

- [ ] Hard-coded hex/rgb/hsl outside `color-mix(..., #000)` hover darkening
- [ ] Raw Tailwind palette utilities (`bg-blue-500`, `text-gray-700`, …)
- [ ] Gradient text, gradient buttons, gradient card fills, animated mesh backgrounds
- [ ] Glassmorphism (`backdrop-blur` cards) outside a sanctioned direction experiment
- [ ] Purple/violet as a default accent
- [ ] Radius above `radius-lg`, or mixed radius language in one direction
- [ ] Soft diffuse shadows on static cards
- [ ] More than one accent color (Neo-Brutalist: one primary + two supporting max)
- [ ] Accent in more than three element types, or >5% of section area
- [ ] Three or more CTAs in one section
- [ ] More than four distinct type roles in one section
- [ ] Off-scale spacing, margin-based grid gaps, negative-margin nudges
- [ ] Emoji, lorem ipsum, or placeholder-obvious copy
- [ ] Horizontal overflow at any QA width (320–1440px)
- [ ] Animation not disabled under `prefers-reduced-motion`
- [ ] State communicated by color alone
- [ ] Re-implemented primitives instead of composed React Components
- [ ] Nested containers with competing max-widths
- [ ] Decorative elements with no communicative purpose
- [ ] `transition: all`, `!important`, arbitrary z-index

---

## 19. DEFINITION OF DONE (quality gates)

A section is shippable only when **every** gate passes:

| # | Gate | Pass criterion |
|---|------|----------------|
| 1 | Tokens | §17 invariants 1–3 pass (grep/static) |
| 2 | Structure | §11.1 anatomy; §17 invariants 4–6 pass |
| 3 | Responsive | Zero horizontal overflow at 320/375/768/1024/1280/1440px; §12.2 collapse map verified |
| 4 | Themes | Light and dark both render correctly by token flip alone; no hard-coded breaks |
| 5 | Contrast | §13 ratios measured at every text/canvas pairing, both themes |
| 6 | Keyboard | Full interactive path operable; focus order matches visual order; §13 focus ring visible on every canvas |
| 7 | Motion | §14.3 bans verified absent; reduced-motion run shows instant/opacity-only behavior |
| 8 | Types | `code.tsx` strict-passes, no `any`; `code.jsx` parity verified |
| 9 | Direction | Matches its §4 direction table exactly; §4.0 parity holds across the family |
| 10 | Content | §15 realism review passes; §18 checklist is empty |
| 11 | Console | Zero console errors/warnings at all QA widths |
| 12 | Metadata | `metadata.json` complete and valid |
| 13 | Preview | `preview.html` exists, renders the actual `code.tsx` full-bleed, matches the generator output (`--check` clean), and passes §12 responsive + both-theme rendering in the preview shell |

---

## 20. CONTRIBUTOR & AI AGENT RULES

Before creating any React Section:

1. Read `React/DESIGN_TOKENS.md` and this file in full.
2. Choose the direction (Minimal / Dark Premium / Bento / Neo-Brutalist) and apply its §4 override set — nothing outside it.
3. Compose from existing React Components and semantic tokens.
4. Do not invent visual values; if truly unavoidable, document the exception in the section's README (a SHOULD-level deviation requires this).
5. Verify against §19 gates 1–13 before submitting (including generating `preview.html` per §16.1–§16.2).
6. After implementation, re-read §17 and §18 and check the result line by line.

---

## 21. QUALITY STANDARD

A React Section should feel:

**"A page worth shipping, one section at a time."**

- Coherent with every other section in the library
- Direction-faithful: unmistakably Minimal, Dark Premium, Bento, or Neo-Brutalist — yet unmistakably DevSnips
- Calm, typographic, intentional
- Accessible, responsive, theme-aware — measurably, not aspirationally
- Free of everything on the anti-pattern checklist

The system is strong enough that four directions and dozens of families still read as one product — and strict enough that no single section can quietly lower the bar.

---

*End of React/Sections/DESIGN_TOKENS.md*
