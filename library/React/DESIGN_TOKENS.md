# DevSnips React Design Tokens

**Single Source of Truth** for the visual design system of the entire DevSnips React ecosystem.

This document governs every React Component, Section, Template, Dashboard, Marketing interface, SaaS interface, Developer interface, Admin interface, Commerce interface, and Documentation interface.

It is authoritative for both human contributors and AI coding agents.  
Read this file before creating or modifying any visual asset.

---

## 1. DESIGN PHILOSOPHY

**“Neutral first, expressive second.”**

The visual language is:

- Precise
- Restrained
- Modern
- Editorial
- Product-oriented
- Typography-driven
- Border-driven
- Accessible
- Responsive
- Calm
- Functional

### Primary Visual Reference

The calendar / date-picker pattern is a major visual reference. It demonstrates:

- Neutral surfaces
- Strong typography
- Thin borders
- Restrained radius
- Compact controls
- Subtle elevation
- Minimal decoration
- Clear hierarchy
- Light/dark parity
- Limited accent usage

### Core Constraints

- Do **not** make purple the system accent color.
- Purple may appear as a template-specific accent, but the underlying system remains neutral.
- The default system must support controlled accents (black, blue, green, orange, violet, red, cyan, and others) without changing the fundamental design language.
- Decoration is secondary to clarity and hierarchy.
- Typography and borders carry most of the identity.

The goal is coherence across hundreds of independently created assets so they feel like they belong to the same ecosystem.

---

## 2. DESIGN SYSTEM HIERARCHY

```
Primitive Tokens
      ↓
Semantic Tokens
      ↓
Component Tokens
      ↓
Components
      ↓
Sections
      ↓
Templates
```

### Explanation of Layers

| Layer              | Responsibility                                      | Example                          |
|--------------------|-----------------------------------------------------|----------------------------------|
| Primitive Tokens   | Raw values (palette scales, base sizes)             | `neutral-900`, `spacing-4`       |
| Semantic Tokens    | Purpose-driven mappings                             | `color.foreground`, `color.border` |
| Component Tokens   | Component-specific mappings of semantic tokens      | `button.primary.background`      |
| Components         | Reusable UI primitives                              | `<Button />`                     |
| Sections           | Composed blocks                                     | Dashboard Header                 |
| Templates          | Full page / product experiences                     | Atlas Analytics                  |

### Rules

- Lower-level assets **must** consume higher-level tokens.
- Components must never invent new visual values when a semantic or component token already exists.
- Sections and templates must consume components (or semantic tokens) rather than hard-coding values.
- This hierarchy exists to guarantee visual consistency, themeability, and long-term maintainability across independent contributors and AI agents.

---

## 3. COLOR SYSTEM

### Philosophy

The default palette is **predominantly neutral**. Color is used for meaning, hierarchy, and interaction feedback—not decoration.

### Primitive Neutral Scale

| Token          | Light Value   | Dark Value    | Notes                          |
|----------------|---------------|---------------|--------------------------------|
| neutral-0      | `#FFFFFF`     | `#FFFFFF`     | Pure white                     |
| neutral-50     | `#FAFAFA`     | `#FAFAFA`     | Near-white                     |
| neutral-100    | `#F5F5F5`     | `#F5F5F5`     | Subtle background              |
| neutral-200    | `#E5E5E5`     | `#E5E5E5`     | Light border / divider         |
| neutral-300    | `#D4D4D4`     | `#D4D4D4`     | Default border                 |
| neutral-400    | `#A3A3A3`     | `#A3A3A3`     | Muted icons / placeholders     |
| neutral-500    | `#737373`     | `#737373`     | Secondary text                 |
| neutral-600    | `#525252`     | `#525252`     | Body text (darker)             |
| neutral-700    | `#404040`     | `#404040`     | Strong text                    |
| neutral-800    | `#262626`     | `#262626`     | Near-black                     |
| neutral-900    | `#171717`     | `#171717`     | Primary text / surfaces        |
| neutral-950    | `#0A0A0A`     | `#0A0A0A`     | Deepest surface                |
| neutral-1000   | `#000000`     | `#000000`     | Pure black                     |

(Exact hex values may be refined in implementation; the scale must remain continuous and neutral.)

### Semantic Color Categories

| Semantic Token              | Purpose                                      | Typical Usage                                      |
|-----------------------------|----------------------------------------------|----------------------------------------------------|
| `color.background`          | Page / canvas background                     | Root layout, body                                  |
| `color.foreground`          | Primary text                                 | Headings, body text                                |
| `color.surface`             | Default elevated surface                     | Cards, panels, sidebars                            |
| `color.surface-subtle`      | Slightly different surface                   | Nested regions, table headers                      |
| `color.surface-elevated`    | Higher elevation surface                     | Dropdowns, popovers, floating panels               |
| `color.surface-hover`       | Hover state background                       | Interactive rows, list items                       |
| `color.surface-active`      | Active / pressed background                  | Pressed buttons, active menu items                 |
| `color.surface-selected`    | Selected state background                    | Selected rows, active tabs, chosen options         |
| `color.muted`               | Muted / secondary surface                    | Disabled backgrounds, secondary panels             |
| `color.muted-foreground`    | Secondary / muted text                       | Descriptions, captions, helper text                |
| `color.border`              | Default border                               | Cards, inputs, dividers                            |
| `color.border-subtle`       | Very light border                            | Soft dividers, nested elements                     |
| `color.border-strong`       | Emphasized border                            | Focused or selected containers                     |
| `color.input`               | Input background                             | Text fields, selects, textareas                    |
| `color.input-hover`         | Input hover background                       | Interactive feedback                               |
| `color.input-focus`         | Input focus background                       | Focus state                                        |
| `color.primary`             | Primary action / brand accent                | Primary buttons, selected indicators               |
| `color.primary-foreground`  | Text on primary                              | Button labels                                      |
| `color.secondary`           | Secondary action                             | Secondary buttons, secondary indicators            |
| `color.secondary-foreground`| Text on secondary                            | Secondary button labels                            |
| `color.accent`              | Contextual accent                            | Selection, progress, important highlights          |
| `color.accent-foreground`   | Text on accent                               | Accent button / badge text                         |
| `color.destructive`         | Destructive / error                          | Delete actions, error states                       |
| `color.destructive-foreground` | Text on destructive                       | Destructive button labels                          |
| `color.success`             | Success / positive                           | Success messages, positive metrics                 |
| `color.success-foreground`  | Text on success                              | Success badges                                     |
| `color.warning`             | Warning                                      | Warning alerts, caution states                     |
| `color.warning-foreground`  | Text on warning                              | Warning text                                       |
| `color.info`                | Informational                                | Info alerts, neutral highlights                    |
| `color.info-foreground`     | Text on info                                 | Info text                                          |
| `color.link`                | Link text                                    | Inline links                                       |
| `color.link-hover`          | Link hover                                   | Hovered links                                      |
| `color.focus-ring`          | Focus indicator                              | Keyboard focus outlines                            |
| `color.overlay`             | Modal / drawer overlay                       | Backdrop                                           |

### Primitive vs Semantic vs Component Colors

- **Primitive**: Raw scale values (`neutral-900`, `blue-500`, etc.). Rarely used directly in components.
- **Semantic**: Purpose-based tokens (`color.foreground`, `color.border`). Preferred for almost all usage.
- **Component**: Component-scoped mappings (`button.primary.background`). Used only inside the component definition.

**Rule**: Components must never hard-code arbitrary hex values when a semantic token exists.

---

## 4. ACCENT COLOR SYSTEM

Accent colors are **contextual**, not mandatory branding.

A component must work correctly whether the consuming template uses:

- Neutral
- Blue
- Green
- Orange
- Violet
- Cyan
- Red
- or any other controlled accent

### Primary Accent Roles

Accent should communicate:

- Selection
- Active state
- Primary action
- Focus
- Progress
- Important information

### Explicit Prohibitions

- Do not use accent colors merely to decorate every card or section.
- Avoid rainbow dashboards.
- Avoid default colored metric cards.
- Avoid random colored icons.
- Avoid gradients everywhere.
- Avoid excessive visual noise.

Accent is a signal, not a decoration layer.

---

## 5. LIGHT AND DARK THEMES

Dark mode is **not** a simple inversion of light mode.

### Shared Principles

- Same semantic token names work in both themes.
- Components never require separate markup for theme switching.
- Theme is applied via CSS custom properties (or equivalent) at the root.

### Light Theme Hierarchy

- Canvas: near-white (`neutral-50` / `neutral-100`)
- Surface: white with subtle borders
- Elevated surface: white with slightly stronger border or very soft shadow
- Borders: visible but quiet (`neutral-200`–`neutral-300`)
- Text: high contrast (`neutral-900` / `neutral-800`)
- Muted text: `neutral-500`–`neutral-600`

### Dark Theme Hierarchy

- Canvas: deep neutral (`neutral-950` / `neutral-900`)
- Surface: slightly lighter than canvas (`neutral-900` / `neutral-800`)
- Elevated surface: further lifted with border or restrained shadow
- Borders: carefully tuned for visibility against dark surfaces (often lighter neutrals)
- Text: high contrast (`neutral-50` / `neutral-100`)
- Muted text: `neutral-400`–`neutral-500`

### State Mapping (Both Themes)

| State          | Guidance                                                                 |
|----------------|--------------------------------------------------------------------------|
| Hover          | Slightly lighter or darker surface + optional border emphasis            |
| Active         | Stronger surface shift + possible border strength                        |
| Selected       | Accent background or accent border + clear visual distinction            |
| Focus          | Visible focus ring using `color.focus-ring`                              |
| Disabled       | Reduced opacity + muted colors; never remove visual affordance entirely  |
| Overlay        | Semi-transparent neutral with enough contrast for content underneath     |

Shadows in dark mode are subtler and often rely more on borders than on large soft shadows.

---

## 6. TYPOGRAPHY

Typography is a primary carrier of visual identity. Do not compensate for weak typography with decoration.

### Font Families

| Role              | Recommended Stack                                      | Notes                          |
|-------------------|--------------------------------------------------------|--------------------------------|
| Sans (UI)         | System UI stack or Inter / Geist / similar             | Default for almost everything  |
| Mono              | `ui-monospace`, SF Mono, Menlo, Consolas, monospace    | Code, numbers, data            |
| Display (optional)| Same as Sans or a carefully chosen editorial face      | Rare, large marketing moments  |

### Font Weights

- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

Avoid 300 and 800+ unless specifically justified for display use.

### Type Scale & Styles

| Style            | Size (px) | Line Height | Weight   | Letter Spacing | Primary Use                              |
|------------------|-----------|-------------|----------|----------------|------------------------------------------|
| display-xl       | 48–56     | 1.1–1.15    | 600–700  | -0.02em        | Hero marketing only                      |
| display-lg       | 36–40     | 1.15        | 600      | -0.02em        | Large section titles                     |
| display-md       | 30–32     | 1.2         | 600      | -0.015em       | Page titles                              |
| heading-xl       | 24        | 1.25        | 600      | -0.01em        | Major section headings                   |
| heading-lg       | 20        | 1.3         | 600      | -0.01em        | Subsection headings                      |
| heading-md       | 18        | 1.35        | 600      | normal         | Card titles, dialog titles               |
| heading-sm       | 16        | 1.4         | 600      | normal         | Small headings, list group titles        |
| body-lg          | 16        | 1.5–1.6     | 400      | normal         | Primary body text                        |
| body-md          | 14        | 1.5         | 400      | normal         | Default body, most UI text               |
| body-sm          | 13        | 1.45        | 400      | normal         | Secondary body, dense UI                 |
| label-lg         | 14        | 1.4         | 500      | normal         | Form labels, strong labels               |
| label-md         | 13        | 1.4         | 500      | normal         | Default labels                           |
| label-sm         | 12        | 1.35        | 500      | 0.01em         | Compact labels, table headers            |
| caption          | 12        | 1.4         | 400      | normal         | Captions, helper text                    |
| overline         | 11–12     | 1.3         | 500–600  | 0.04–0.06em    | Category labels, overlines               |
| code-sm          | 12        | 1.4         | 400      | normal         | Inline code, small mono                  |
| code-md          | 13–14     | 1.45        | 400      | normal         | Code blocks, data                        |
| numeric-xl       | 28–32     | 1.2         | 600      | -0.02em        | Large metrics                            |
| numeric-lg       | 20–24     | 1.25        | 600      | -0.015em       | Dashboard metrics                        |
| numeric-md       | 16–18     | 1.3         | 500–600  | normal         | Inline numbers, table emphasis           |

### Usage Guidance

- Maximum recommended heading size in product interfaces: `heading-xl` (24px). Larger sizes are reserved for marketing or very sparse layouts.
- Optimal line length for body text: 60–75 characters.
- Paragraph spacing: typically 0.75–1× the line height.
- Labels sit above or beside controls with consistent gap (`control-gap`).
- Tables use `label-sm` or `body-sm` for headers and `body-sm` / `body-md` for cells.
- Data visualization prefers tabular numbers and mono or tightly tracked numeric styles.
- Forms use `label-md` + `body-md` inputs by default.

---

## 7. SPACING

Spacing is based primarily on **4px** and **8px** relationships.

### Base Scale (Primitive)

| Token       | Value |
|-------------|-------|
| spacing-0   | 0     |
| spacing-1   | 4px   |
| spacing-2   | 8px   |
| spacing-3   | 12px  |
| spacing-4   | 16px  |
| spacing-5   | 20px  |
| spacing-6   | 24px  |
| spacing-8   | 32px  |
| spacing-10  | 40px  |
| spacing-12  | 48px  |
| spacing-16  | 64px  |
| spacing-20  | 80px  |
| spacing-24  | 96px  |

### Semantic Spacing Concepts

| Concept            | Typical Range          | Usage                                      |
|--------------------|------------------------|--------------------------------------------|
| `inline-gap`       | 4–12px                 | Horizontal gap between related elements    |
| `stack-gap`        | 8–24px                 | Vertical gap between stacked items         |
| `control-gap`      | 8–12px                 | Gap between label and control, or controls |
| `component-padding`| 8–16px                 | Internal padding of small components       |
| `card-padding`     | 16–24px                | Card / surface internal padding            |
| `section-gap`      | 32–64px                | Vertical gap between major sections        |
| `page-gutter`      | 16–32px (responsive)   | Horizontal page margins                    |
| `content-gap`      | 24–48px                | Gap inside content areas                   |

**Rule**: Do not invent arbitrary spacing values when an existing token is appropriate.

---

## 8. BORDER RADIUS

Restrained radius system. Prefer small-to-medium values.

| Token      | Value   | Typical Use                          |
|------------|---------|--------------------------------------|
| radius-none| 0       | Sharp edges, tables, dense tools     |
| radius-xs  | 2–3px   | Badges, small chips, subtle rounding |
| radius-sm  | 4–6px   | Buttons, inputs, small cards         |
| radius-md  | 8px     | Default cards, dialogs, panels       |
| radius-lg  | 12px    | Larger surfaces, marketing cards     |
| radius-xl  | 16px    | Rare large containers                |
| radius-full| 9999px  | Pills, avatars, fully rounded        |

### Semantic Radius Guidance

| Element          | Preferred Radius     |
|------------------|----------------------|
| Buttons          | `radius-sm`          |
| Inputs / Selects | `radius-sm`          |
| Cards            | `radius-md`          |
| Dialogs          | `radius-md` or `lg`  |
| Dropdowns        | `radius-md`          |
| Popovers         | `radius-md`          |
| Badges           | `radius-xs` or `full`|
| Avatars          | `radius-full` or `md`|
| Panels / Sidebars| `radius-none` or `sm`|

Avoid excessive pill-shaped interfaces, giant rounded cards, and inconsistent radius values.

---

## 9. BORDERS

The default interface relies heavily on **subtle 1px borders**.

| Property          | Guidance                                      |
|-------------------|-----------------------------------------------|
| Width             | 1px default; 2px only for deliberate emphasis |
| Style             | Solid                                         |
| Color             | `color.border`, `color.border-subtle`, `color.border-strong` |
| Dividers          | 1px `color.border-subtle` or `color.border`   |
| Focus borders     | Often combined with focus-ring                |
| Selected borders  | May use accent or `color.border-strong`       |
| Interactive borders| Subtle shift on hover/focus                  |

Borders frequently replace shadows for separation, especially in dense or dark interfaces.

---

## 10. SHADOWS

Elevation philosophy is restrained. Shadows communicate elevation, not decoration.

| Token     | Typical Usage                          |
|-----------|----------------------------------------|
| shadow-none | Flat surfaces                        |
| shadow-xs | Subtle lift (rare)                     |
| shadow-sm | Dropdowns, small popovers              |
| shadow-md | Dialogs, larger popovers, sticky nav   |
| shadow-lg | Floating panels, command palette       |
| shadow-xl | Rare high elevation                    |

### Semantic Shadow Guidance

| Element              | Preferred Shadow   |
|----------------------|--------------------|
| Dropdowns            | `shadow-sm`–`md`   |
| Popovers             | `shadow-sm`–`md`   |
| Dialogs              | `shadow-md`–`lg`   |
| Sticky navigation    | `shadow-sm` or border |
| Floating controls    | `shadow-sm`        |
| Card hover           | Optional very subtle or none |

Avoid huge soft shadows and floating-card aesthetics.

---

## 11. SIZING

### Control Heights (Default Density)

| Control          | Small   | Default | Large   |
|------------------|---------|---------|---------|
| Button           | 28–32px | 36px    | 40–44px |
| Input / Select   | 28–32px | 36px    | 40–44px |
| Textarea        | auto    | auto    | auto    |
| Checkbox / Radio | 16px    | 16–18px | 20px    |
| Switch           | 20×12   | 24×14   | 28×16   |
| Icon Button      | 28–32px | 36px    | 40px    |
| Avatar           | 24–32px | 40px    | 48–64px |
| Badge            | auto    | auto    | auto    |

### Structural Dimensions

| Element            | Guidance                          |
|--------------------|-----------------------------------|
| Navigation height  | 48–56px (top nav)                 |
| Sidebar width      | 240–280px (default), collapsible  |
| Dialog max-width   | 400–640px depending on content    |
| Table row height   | 36–48px depending on density      |
| Touch targets      | Minimum 44×44px where possible    |

All interactive elements must meet accessible touch-target sizes on touch devices.

---

## 12. LAYOUT

### Philosophy

Layouts are intentional, hierarchical, and free of unnecessary nesting. Prefer clear regions over deeply nested wrappers.

### Core Dimensions

| Concept              | Guidance                                      |
|----------------------|-----------------------------------------------|
| Container max-width  | 1280–1440px for most product pages            |
| Page gutter          | 16px (mobile) → 24–32px (desktop)             |
| Content width        | Constrained for readability when appropriate  |
| Dashboard width      | Full available width within sidebar layout    |
| Sidebar width        | 240–280px                                     |
| Navigation height    | 48–56px                                       |
| Column gap           | 16–24px                                       |
| Section vertical gap | 32–64px                                       |

### Common Layout Patterns

- Single-column
- Split layout (sidebar + content)
- Two-column
- Three-column
- Dashboard grid (responsive cards / metrics)
- 12-column grid (when precise alignment is needed)
- Sidebar + content
- Centered content (forms, auth, documentation)
- Full-bleed section (marketing heroes)

Avoid deep nesting of containers that add no structural meaning.

---

## 13. RESPONSIVE DESIGN

### Breakpoints (Reference)

| Name          | Min-width | Notes                          |
|---------------|-----------|--------------------------------|
| Mobile        | 0         | Base                           |
| Tablet        | 768px     |                                |
| Desktop       | 1024px    |                                |
| Wide Desktop  | 1280px+   |                                |

### Response Rules

- Do **not** simply shrink desktop layouts.
- Navigation collapses into drawer / hamburger on small screens.
- Sidebars become overlay or bottom sheets on mobile.
- Tables may become horizontally scrollable or transform into card lists.
- Cards stack vertically on narrow viewports.
- Forms remain single-column on mobile.
- Dialogs become full-screen or bottom sheets on small screens when appropriate.
- Charts adapt by reducing density or enabling horizontal scroll.
- Typography scales modestly; do not over-reduce body text.
- Spacing tightens on mobile but remains intentional.

Mobile layouts must remain deliberate and usable, not residual afterthoughts.

---

## 14. DENSITY

Three density modes:

| Mode         | Primary Use Cases                          | Characteristics                     |
|--------------|--------------------------------------------|-------------------------------------|
| Compact      | Dashboards, admin panels, tables, dev tools| Reduced padding, smaller controls   |
| Default      | Normal product interfaces                  | Balanced                            |
| Comfortable  | Marketing, onboarding, content-heavy       | Increased spacing, larger targets   |

Density changes spacing and control dimensions **without** changing the fundamental visual language (radius, border style, typography hierarchy, color philosophy).

---

## 15. COMPONENT STATES

Every interactive component follows a consistent state model.

| State            | Description                                      | Notes                                      |
|------------------|--------------------------------------------------|--------------------------------------------|
| default          | Resting state                                    | Always defined                             |
| hover            | Pointer over                                     | Subtle surface / border change             |
| focus            | Programmatic focus                               | May be combined with focus-visible         |
| focus-visible    | Keyboard / assistive focus                       | Must be clearly visible                    |
| active           | Pressed / currently interacting                  | Stronger feedback                          |
| selected         | Chosen / active in a set                         | Distinct from hover                        |
| disabled         | Non-interactive                                  | Reduced opacity + muted colors             |
| loading          | In progress                                      | Spinner / skeleton / disabled interaction  |
| error            | Validation or system error                       | Destructive color + message                |
| success          | Successful action / valid                        | Success color + optional message           |
| warning          | Caution                                          | Warning color + message                    |

Not every component needs every state. Focus-visible must never be omitted for interactive elements.

---

## 16. ACCESSIBILITY

### Requirements

- WCAG AA contrast minimum for text and interactive elements.
- Full keyboard navigation support.
- Visible focus indicators (`color.focus-ring`).
- Touch targets ≥ 44×44px where feasible.
- Disabled states remain perceivable.
- Error and success states are not communicated by color alone.
- Selected states use more than color (border, background, icon, or text weight).
- Visual states must be compatible with screen readers (proper ARIA when needed).
- Respect `prefers-reduced-motion`.

**Selected ≠ only color change**  
**Error ≠ only red**  
**Success ≠ only green**

---

## 17. MOTION

### Principles

Motion is subtle, functional, fast, and predictable.

| Token / Concept     | Guidance                          |
|---------------------|-----------------------------------|
| Duration (fast)     | 100–150ms                         |
| Duration (default)  | 150–200ms                         |
| Duration (slow)     | 250–300ms                         |
| Easing              | Ease-out or standard cubic-bezier |
| Enter transitions   | Opacity + slight translate        |
| Exit transitions    | Opacity + slight translate        |
| Hover transitions   | Color / background / border       |
| State transitions   | Consistent short duration         |

### Prohibitions

- Excessive bouncing
- Dramatic page animations
- Decorative animation
- Constant movement

### Reduced Motion

When `prefers-reduced-motion: reduce` is active:

- Prefer opacity changes only, or instant transitions.
- Disable non-essential motion.

---

## 18. ICONOGRAPHY

| Aspect                | Guidance                                      |
|-----------------------|-----------------------------------------------|
| Sizing                | 16px (default), 14px (compact), 20px (large)  |
| Stroke                | Consistent weight across the set              |
| Alignment             | Optical alignment with text                   |
| Icon + text spacing   | 6–8px                                         |
| Icon button size      | Matches control height                        |
| Color                 | Inherits or uses semantic foreground / muted  |

Icons support hierarchy; they are not decoration. Do not mix radically different icon styles within the same interface.

---

## 19. FORMS

### Visual Rules

| Element              | Guidance                                              |
|----------------------|-------------------------------------------------------|
| Labels               | `label-md` or `label-sm`, above or beside control     |
| Inputs               | Consistent height, `radius-sm`, 1px border            |
| Placeholders         | Muted foreground, never critical information          |
| Descriptions         | `caption` or `body-sm`, muted                         |
| Validation messages  | Inline, clear, associated with the field              |
| Error state          | Border + text color + message (not color alone)       |
| Success state        | Optional positive indicator                           |
| Required indicators  | Asterisk or “required” text, accessible               |
| Help text            | Below field, muted                                    |
| Disabled fields      | Muted appearance, still readable                      |
| Focus states         | Clear ring or border emphasis                         |
| Grouped fields       | Consistent vertical rhythm (`stack-gap`)              |

Forms must feel identical in structure across every template.

---

## 20. DATA-DENSE INTERFACES

### Rules

- Tables are preferred for dense tabular data.
- Dashboards use a mix of direct canvas content and bordered surfaces.
- Metrics may sit on the canvas or inside restrained surfaces.
- Charts follow the data-visualization rules (Section 23).
- Filters, pagination, sorting, and search must be visually quiet and consistent.
- Empty states are calm and instructional.
- Loading states use skeletons or restrained spinners.

**Avoid** automatically placing every piece of data inside a card.

Content may exist directly on the page canvas when a bordered surface adds no additional meaning.

---

## 21. SURFACE PHILOSOPHY

Three primary structural concepts:

| Concept  | Definition                                      | When to Use                                      |
|----------|-------------------------------------------------|--------------------------------------------------|
| Canvas   | The page itself                                 | Root background, main content area               |
| Panel    | A major functional region                       | Sidebar, main content column, settings panel     |
| Surface  | A contained element with its own boundary       | Cards, dialogs, dropdowns, elevated groups       |

**Explicitly discourage**: “Everything must be a card.”

Cards communicate grouping. They are not mandatory decoration.

---

## 22. NAVIGATION

Navigation is visually quiet and highly functional.

| Pattern              | Guidance                                              |
|----------------------|-------------------------------------------------------|
| Top navigation       | Height 48–56px, subtle bottom border or shadow        |
| Sidebar              | Fixed or collapsible, clear active state              |
| Mobile navigation    | Drawer or bottom bar, accessible                      |
| Breadcrumbs          | Compact, muted, clear hierarchy                       |
| Tabs                 | Underline or subtle background for active             |
| Command palette      | High elevation, strong focus, keyboard-first          |
| Workspace switchers  | Quiet, consistent with sidebar or top nav             |

Active states must be unambiguous without relying solely on color.

---

## 23. DATA VISUALIZATION

| Aspect                | Guidance                                              |
|-----------------------|-------------------------------------------------------|
| Chart colors          | Limited, purposeful palette; theme-aware              |
| Chart typography      | `body-sm` / `caption` / numeric styles                |
| Grid lines            | Subtle, low-contrast                                  |
| Axis labels           | Readable, not cramped                                 |
| Tooltips              | Elevated surface, restrained shadow, clear text       |
| Legends               | Compact, consistent placement                         |
| Positive / negative   | Success / destructive or dedicated directional colors |
| Comparison states     | Clear visual distinction                              |

Charts must remain understandable in both light and dark themes.  
Do not use five unrelated bright colors merely to make a chart look exciting.

---

## 24. TEMPLATE PERSONALITY

DevSnips React has **ONE DESIGN LANGUAGE** but **MULTIPLE PRODUCT PERSONALITIES**.

| Template / Product Type | Personality Characteristics                  |
|-------------------------|----------------------------------------------|
| Atlas Analytics         | Dense, analytical, serious                   |
| Forge                   | Technical, editorial, developer-focused      |
| AI product              | Slightly more expressive                     |
| Commerce                | Visual and spacious                          |
| Admin                   | Functional and dense                         |
| Documentation           | Typographic and content-focused              |

Each template may choose its own accent and density while sharing the same fundamental tokens, radius system, border language, typography scale, and state model.

---

## 25. TOKEN NAMING

### Naming Convention

```
category.property
category.property.variant
category.property.size
```

Examples:

- `color.background`
- `color.foreground`
- `color.border`
- `color.primary`
- `spacing.md`
- `radius.sm`
- `shadow.md`
- `typography.body-md`
- `button.primary.background`
- `input.border`

### CSS Custom Property Mapping

```
--ds-color-background
--ds-color-foreground
--ds-color-border
--ds-spacing-md
--ds-radius-sm
--ds-shadow-md
--ds-typography-body-md
```

The Markdown file is the **specification**. Implementation (CSS variables, Tailwind theme, JS tokens, etc.) must follow this naming structure.

---

## 26. COMPONENT-SPECIFIC RULES

### Button

- Height: 36px default (density variants)
- Radius: `radius-sm`
- Border: 1px or none (filled)
- Typography: `label-md` / `label-sm`
- Padding: horizontal 12–16px
- States: default, hover, active, focus-visible, disabled, loading
- Elevation: none (or very subtle for secondary)
- Color: primary / secondary / destructive / ghost variants using semantic tokens

### Input / Select / Textarea

- Height: 36px (input/select)
- Radius: `radius-sm`
- Border: 1px `color.border`
- Typography: `body-md`
- Padding: 8–12px
- States: default, hover, focus, error, disabled
- Focus: clear ring or border emphasis

### Checkbox / Radio / Switch

- Size: 16–18px (checkbox/radio), switch proportional
- Radius: `radius-xs` (checkbox), full (radio/switch)
- Clear selected / unchecked states
- Focus-visible required

### Card

- Radius: `radius-md`
- Border: 1px `color.border`
- Padding: `card-padding` (16–24px)
- Elevation: none or `shadow-xs` / `sm` on hover (optional)
- Background: `color.surface`

### Dialog / Drawer

- Radius: `radius-md` or `lg`
- Elevation: `shadow-md`–`lg`
- Overlay: `color.overlay`
- Clear header / body / footer structure
- Focus trap and keyboard support required

### Dropdown / Popover / Tooltip

- Radius: `radius-md`
- Elevation: `shadow-sm`–`md`
- Border: 1px subtle
- Typography: `body-sm` / `body-md`
- Max-height and scroll for long lists

### Tabs

- Active state clearly indicated (underline or background)
- Typography: `label-md`
- Consistent height with navigation

### Accordion

- Clear expand/collapse affordance
- Consistent padding and border treatment

### Badge

- Radius: `radius-xs` or `full`
- Typography: `label-sm` or `caption`
- Compact padding

### Avatar

- Radius: `radius-full` or `md`
- Consistent sizing scale
- Fallback initials or icon

### Toast / Alert

- Clear severity using semantic colors + icon + text
- Not color alone
- Radius: `radius-md`
- Elevation appropriate to floating nature

### Progress / Slider

- Track and indicator use semantic colors
- Accessible labels and values

### Calendar / Date Picker

- Follows the primary visual reference: neutral surfaces, strong typography, thin borders, restrained radius, compact controls, clear selected state, light/dark parity

### Command Palette

- High elevation, strong focus, keyboard-first
- Dense but readable list
- Clear active item

### Table

- Compact or default density
- Clear header styling
- Hover and selected row states
- Borders or subtle dividers preferred over heavy shadows

### Pagination / Breadcrumb / Sidebar / Navigation / Skeleton

- Quiet, consistent with overall language
- Skeleton uses muted surfaces and subtle animation (respect reduced motion)

---

## 27. CONTRIBUTOR RULES

### DO NOT

- Invent arbitrary colors
- Invent arbitrary spacing
- Invent arbitrary radius values
- Introduce random shadows
- Use gradients without a clear, justified reason
- Use purple as a mandatory system accent
- Create excessive card layouts
- Mix unrelated typography scales or weights
- Create component-specific design systems that diverge from this document
- Ignore dark mode
- Ignore responsive behavior
- Rely only on color for state communication
- Add unnecessary animation
- Use inconsistent icon styles
- Bypass semantic tokens in favor of raw values

---

## 28. AI AGENT RULES

Before creating any React component, section, or template:

1. Read `React/DESIGN_TOKENS.md` in full.
2. Identify the appropriate semantic tokens.
3. Reuse existing component patterns whenever possible.
4. Do not invent visual values unless absolutely necessary and document the exception.
5. Preserve light/dark behavior through semantic tokens.
6. Preserve responsive behavior.
7. Follow the density rules of the target context.
8. Follow accessibility rules (contrast, focus, touch targets, non-color state cues).
9. Follow the consistent state model.
10. After implementation, check the resulting component against this document.

This file is authoritative. Treat it as the formal design-system specification.

---

## 29. QUALITY STANDARD

A React asset should feel:

**“designed, not decorated.”**

It must be:

- Visually coherent
- Technically reusable
- Accessible
- Responsive
- Theme-aware
- Predictable
- Intentional

The design system is strong enough that two different contributors, working independently, can create two components and those components still look like they belong to the same product.

---

## 30. FINAL AUDIT

This document has been internally audited for:

- Consistent terminology
- Consistent naming conventions
- Clear hierarchy (Primitive → Semantic → Component → …)
- Coherent color philosophy (neutral-first)
- Complete light/dark strategy
- Spacing scale and semantic concepts
- Restrained radius system
- Typography hierarchy and usage guidance
- Density modes
- Responsive rules
- Accessibility requirements
- Motion principles
- Component state model
- Template personality variation
- Contributor rules
- AI agent rules

No other files are required.  
This single Markdown file is the complete formal design-system specification for the DevSnips React ecosystem.

---

*End of DESIGN_TOKENS.md*
