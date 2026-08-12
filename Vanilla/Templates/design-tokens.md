# DevSnips Vanilla Templates — Shared Design Token System

Create the shared design-token specification for all templates inside:

```text
DevSnips/
└── Vanilla/
    └── Templates/
        ├── design-tokens.md
        ├── SaaS Dashboard/
        ├── Documentation Site/
        ├── Job Board/
        └── ...
```

## IMPORTANT REPOSITORY RULE

The design-token specification MUST be created directly at:

```text
Vanilla/Templates/design-tokens.md
```

Do NOT create:

```text
Vanilla/Templates/_shared/
Vanilla/Templates/design-system/
Vanilla/Templates/shared/
Vanilla/design-tokens.md
```

Do NOT create a shared folder for this system.

`design-tokens.md` is the single source of truth for the visual design principles and token specifications used by all Vanilla templates.

---

# 1. PURPOSE

Create a shared visual language for the entire DevSnips Vanilla Templates collection.

The system should allow different templates to have different personalities while still clearly belonging to the same DevSnips design family.

Examples:

- SaaS Dashboard → structured, analytical, operational
- Documentation → editorial, technical, typography-focused
- Job Board → dense, structured, content-heavy
- Developer Portfolio → personal, technical, expressive
- Agency → visual, polished, portfolio-driven
- E-commerce → commercial, product-focused
- LMS → educational, structured, progress-oriented

They should NOT all look identical.

They should share the same underlying design discipline.

---

# 2. DESIGN REFERENCES

Use the provided reference images as the aesthetic benchmark.

Do NOT copy their:

- branding
- exact colors
- content
- layouts
- logos
- visual identity
- exact component implementations

Instead, extract the underlying design principles.

The desired visual language is:

- clean
- refined
- editorial
- product-focused
- typography-driven
- information-dense
- neutral
- restrained
- highly usable
- responsive
- accessible
- premium without being flashy

The interface should look:

> Designed, not generated.

---

# 3. CORE DESIGN PHILOSOPHY

Prioritize:

1. Typography
2. Information hierarchy
3. Spacing
4. Alignment
5. Content density
6. Subtle borders
7. Neutral surfaces
8. Controlled accents
9. Responsive behavior
10. Accessibility

Avoid using decoration as a substitute for design.

A UI should feel premium because its:

- typography is strong
- spacing is consistent
- hierarchy is clear
- information is well organized
- details are polished
- responsive behavior is intentional

---

# 4. DO NOT CREATE THE GENERIC AI/SAAS AESTHETIC

The default DevSnips visual language must NOT become:

- glowing violet
- neon indigo
- purple-on-black
- gradient-heavy
- glassmorphism-heavy
- neon borders
- giant gradient backgrounds
- gradient text
- oversized floating icons
- decorative blobs
- excessive blur
- giant rounded cards
- excessive pill controls
- giant marketing hero sections
- generic three-column feature grids
- glossy stock photography
- buzzword-heavy marketing copy
- fake futuristic effects
- animated backgrounds
- giant empty whitespace
- excessive drop shadows

Especially avoid:

```text
dark charcoal background
+
glowing purple/violet cards
+
neon blue buttons
+
gradient text
+
AI buzzwords
```

That is NOT the DevSnips default design language.

---

# 5. TOKEN ARCHITECTURE

Use a three-layer system:

```text
Primitive Tokens
        ↓
Semantic Tokens
        ↓
Template Tokens
        ↓
Components
```

## Primitive tokens

Define raw values.

Example:

```css
--ds-gray-100
--ds-blue-500
--ds-space-4
--ds-radius-md
```

## Semantic tokens

Define meaning.

Example:

```css
--ds-bg-canvas
--ds-text-primary
--ds-border-default
--ds-action-primary
```

Components should primarily consume semantic tokens.

## Template tokens

Allow individual templates to adapt the system.

Example:

```css
--template-accent
--template-sidebar-width
--template-content-width
--template-card-radius
```

Do not force every template to use exactly the same values.

---

# 6. NAMING CONVENTION

Use:

```text
--ds-[category]-[property]
```

Examples:

```css
--ds-bg-canvas
--ds-text-primary
--ds-border-default
--ds-space-4
--ds-radius-md
--ds-shadow-sm
--ds-font-sans
```

Template-specific tokens use:

```text
--template-[property]
```

Examples:

```css
--template-accent
--template-sidebar-width
--template-reading-width
```

Keep naming consistent across the entire collection.

---

# 7. COLOR SYSTEM

The color system must support:

- light mode
- dark mode
- neutral-first interfaces
- semantic feedback states
- accessible contrast
- template-specific accents

## Primitive neutral scale

Create a complete neutral scale:

```css
--ds-gray-0
--ds-gray-25
--ds-gray-50
--ds-gray-100
--ds-gray-150
--ds-gray-200
--ds-gray-300
--ds-gray-400
--ds-gray-500
--ds-gray-600
--ds-gray-700
--ds-gray-800
--ds-gray-850
--ds-gray-900
--ds-gray-950
--ds-gray-1000
```

The exact values can be selected during implementation.

## Accent scales

Provide controlled scales for:

- Blue
- Green
- Red
- Yellow
- Orange

Example:

```css
--ds-blue-50
--ds-blue-100
--ds-blue-200
--ds-blue-300
--ds-blue-400
--ds-blue-500
--ds-blue-600
--ds-blue-700
--ds-blue-800
--ds-blue-900
```

Do not make violet or indigo the default DevSnips accent.

---

# 8. SEMANTIC BACKGROUND TOKENS

Define:

```css
--ds-bg-canvas
--ds-bg-surface
--ds-bg-surface-subtle
--ds-bg-surface-raised
--ds-bg-overlay
```

Use these to create subtle surface hierarchy without relying heavily on shadows.

---

# 9. SEMANTIC TEXT TOKENS

Define:

```css
--ds-text-primary
--ds-text-secondary
--ds-text-muted
--ds-text-disabled
--ds-text-inverse
```

Primary text should provide the strongest hierarchy.

Muted text should be visually subtle but still readable.

---

# 10. BORDER TOKENS

Define:

```css
--ds-border-subtle
--ds-border-default
--ds-border-strong
--ds-border-focus
```

Default structural borders should generally be:

```text
1px
```

Use borders for:

- cards
- panels
- navigation
- tables
- inputs
- dividers
- list items
- code blocks

Prefer subtle borders over heavy shadows.

---

# 11. ACTION TOKENS

Define:

```css
--ds-action-primary
--ds-action-primary-hover
--ds-action-primary-active

--ds-action-secondary
--ds-action-secondary-hover
--ds-action-secondary-active

--ds-action-danger
--ds-action-danger-hover
```

Primary actions should be visually distinct.

Do not make every interactive element a primary action.

---

# 12. STATUS TOKENS

Define:

### Success

```css
--ds-status-success
--ds-status-success-bg
--ds-status-success-border
```

### Warning

```css
--ds-status-warning
--ds-status-warning-bg
--ds-status-warning-border
```

### Danger

```css
--ds-status-danger
--ds-status-danger-bg
--ds-status-danger-border
```

### Info

```css
--ds-status-info
--ds-status-info-bg
--ds-status-info-border
```

Use for:

- alerts
- badges
- validation
- notifications
- states
- system messages

---

# 13. TYPOGRAPHY

Typography is a primary design element across DevSnips.

Define:

```css
--ds-font-sans
--ds-font-mono
--ds-font-display
```

## Sans

Use for:

- interface text
- headings
- navigation
- forms
- buttons
- labels
- content

## Mono

Use for:

- code
- API endpoints
- technical identifiers
- terminal commands
- technical values
- selected numeric interfaces

Do not use monospace for an entire template unless deliberately justified.

---

# 14. TYPE SCALE

Define:

```css
--ds-text-xs
--ds-text-sm
--ds-text-md
--ds-text-lg
--ds-text-xl
--ds-text-2xl
--ds-text-3xl
--ds-text-4xl
--ds-text-5xl
```

Suggested hierarchy:

```text
xs  → metadata
sm  → supporting text
md  → standard content
lg  → emphasized content
xl  → section heading
2xl → large section heading
3xl → page heading
4xl → major heading
5xl → rare display use
```

Do not overuse very large typography.

---

# 15. FONT WEIGHTS

Define:

```css
--ds-weight-regular
--ds-weight-medium
--ds-weight-semibold
--ds-weight-bold
```

Use weight carefully to establish hierarchy.

Avoid making everything bold.

---

# 16. LINE HEIGHT

Define:

```css
--ds-leading-tight
--ds-leading-snug
--ds-leading-normal
--ds-leading-relaxed
```

Use tighter line height for headings.

Use normal/relaxed line height for reading content.

---

# 17. LETTER SPACING

Define where useful:

```css
--ds-tracking-tight
--ds-tracking-normal
--ds-tracking-wide
```

Do not overuse tracking.

Avoid using uppercase + wide tracking as the default way to create hierarchy.

---

# 18. SPACING SYSTEM

Create a predictable scale:

```css
--ds-space-1
--ds-space-2
--ds-space-3
--ds-space-4
--ds-space-5
--ds-space-6
--ds-space-8
--ds-space-10
--ds-space-12
--ds-space-16
--ds-space-20
--ds-space-24
--ds-space-32
```

Use these tokens consistently.

Avoid unnecessary one-off values.

---

# 19. COMPONENT SPACING

Define shared spacing levels:

```css
--ds-component-padding-xs
--ds-component-padding-sm
--ds-component-padding-md
--ds-component-padding-lg
```

Use for:

- cards
- buttons
- inputs
- lists
- navigation
- tables
- panels

---

# 20. LAYOUT TOKENS

Define:

```css
--ds-container-xs
--ds-container-sm
--ds-container-md
--ds-container-lg
--ds-container-xl
--ds-container-wide
```

Templates should choose the most appropriate container width.

Do not force every template to use the maximum width.

---

# 21. CONTENT WIDTH TOKENS

Define:

```css
--ds-content-reading
--ds-content-default
--ds-content-wide
```

Reading-focused templates should maintain comfortable line lengths.

Documentation and article content should never become unnecessarily wide.

---

# 22. PAGE PADDING

Define:

```css
--ds-page-padding-mobile
--ds-page-padding-tablet
--ds-page-padding-desktop
```

Page padding should adapt to viewport size.

---

# 23. SECTION SPACING

Define:

```css
--ds-section-gap-sm
--ds-section-gap-md
--ds-section-gap-lg
--ds-section-gap-xl
```

Use these to create consistent vertical rhythm.

Do not create huge empty spaces only to make a design look premium.

---

# 24. GRID TOKENS

Define:

```css
--ds-grid-gap-xs
--ds-grid-gap-sm
--ds-grid-gap-md
--ds-grid-gap-lg
--ds-grid-gap-xl
```

Use consistent grid gaps across templates.

---

# 25. BORDER SYSTEM

Define:

```css
--ds-border-width-thin
--ds-border-width-default
--ds-border-width-strong
```

Default:

```text
1px
```

Avoid thick borders unless a template intentionally uses a brutalist style.

---

# 26. RADIUS SYSTEM

Define:

```css
--ds-radius-none
--ds-radius-xs
--ds-radius-sm
--ds-radius-md
--ds-radius-lg
--ds-radius-xl
--ds-radius-full
```

Default DevSnips interfaces should primarily use:

```text
none
xs
sm
md
```

Large radius values should be intentional.

Full rounding should be mainly used for:

- badges
- tags
- avatars
- compact pills
- selected special controls

Do not round everything.

---

# 27. SHADOW SYSTEM

Define:

```css
--ds-shadow-none
--ds-shadow-xs
--ds-shadow-sm
--ds-shadow-md
--ds-shadow-lg
```

Shadows should remain subtle.

Primary hierarchy should come from:

- spacing
- typography
- borders
- surface contrast

Avoid:

- glowing shadows
- colored shadows
- neon effects
- massive floating shadows

---

# 28. BUTTON TOKENS

Define:

```css
--ds-button-height-sm
--ds-button-height-md
--ds-button-height-lg

--ds-button-padding-x-sm
--ds-button-padding-x-md
--ds-button-padding-x-lg

--ds-button-radius
```

Buttons need:

- hover
- active
- focus
- disabled
- loading where appropriate

Buttons must remain visually consistent throughout a template.

---

# 29. INPUT TOKENS

Define:

```css
--ds-input-height-sm
--ds-input-height-md
--ds-input-height-lg

--ds-input-padding-x
--ds-input-padding-y

--ds-input-radius
```

Inputs should support:

- default
- focus
- error
- success where appropriate
- disabled
- readonly

---

# 30. CARD TOKENS

Define:

```css
--ds-card-padding
--ds-card-radius
--ds-card-border
--ds-card-shadow
```

Cards are optional.

Do not turn every section into a card.

Use cards when they improve grouping or hierarchy.

---

# 31. NAVIGATION TOKENS

Define:

```css
--ds-nav-height
--ds-nav-item-height
--ds-nav-gap
--ds-nav-padding-x
--ds-nav-padding-y
```

Navigation needs:

- hover
- active
- selected
- focus
- collapsed
- mobile states

---

# 32. TABLE TOKENS

Define:

```css
--ds-table-cell-padding-x
--ds-table-cell-padding-y
--ds-table-row-height
--ds-table-header-height
```

Tables should support information density without becoming difficult to scan.

---

# 33. BADGE TOKENS

Define:

```css
--ds-badge-height
--ds-badge-padding-x
--ds-badge-padding-y
--ds-badge-radius
```

Badges should communicate:

- status
- category
- priority
- state

Do not use them purely for decoration.

---

# 34. ICON TOKENS

Define:

```css
--ds-icon-xs
--ds-icon-sm
--ds-icon-md
--ds-icon-lg
--ds-icon-xl
```

Icons should:

- align with text
- remain visually lightweight
- have consistent sizing
- communicate meaning

Avoid oversized decorative icons.

---

# 35. RESPONSIVE SYSTEM

Create shared breakpoints:

```css
--ds-breakpoint-sm
--ds-breakpoint-md
--ds-breakpoint-lg
--ds-breakpoint-xl
```

Do not interpret these simply as:

```text
mobile
tablet
desktop
```

They should represent meaningful layout changes.

---

# 36. RESPONSIVE DESIGN PRINCIPLES

Every template must be intentionally responsive across:

- large desktop
- desktop
- laptop
- tablet
- mobile
- small mobile

Do NOT use:

```text
desktop layout → shrink everything
```

Instead:

```text
desktop composition
tablet composition
mobile composition
```

Examples:

- sidebar → drawer
- multi-column grid → reduced grid
- table → compact table/list
- large header → compact header
- right-side content → collapsible content
- complex toolbar → grouped controls

---

# 37. MOBILE RULES

Mobile must:

- avoid horizontal overflow
- maintain readable typography
- preserve usable controls
- prevent clipping
- handle long labels
- handle tables
- handle code
- handle dialogs
- handle navigation
- handle filters

The mobile design must feel intentional.

---

# 38. MOTION

Define:

```css
--ds-duration-fast
--ds-duration-normal
--ds-duration-slow

--ds-ease-standard
--ds-ease-emphasized
```

Use motion for:

- drawers
- dropdowns
- dialogs
- navigation
- state changes
- subtle interaction feedback

Avoid decorative animation.

Respect:

```css
prefers-reduced-motion
```

---

# 39. Z-INDEX

Define a predictable stacking system:

```css
--ds-z-base
--ds-z-dropdown
--ds-z-sticky
--ds-z-overlay
--ds-z-modal
--ds-z-toast
```

Avoid random extreme z-index values.

---

# 40. LIGHT MODE

Light mode should use:

- white
- off-white
- light gray
- charcoal
- black

with controlled accents.

Use surface variation and borders for hierarchy.

---

# 41. DARK MODE

Dark mode should use:

- near-black
- deep charcoal
- subtle dark surfaces
- muted borders
- soft white text

Do not convert dark mode into:

```text
black + neon purple
```

Dark mode should feel calm, readable, and professional.

---

# 42. ACCESSIBILITY

All tokens should support accessible interfaces.

Consider:

- contrast
- keyboard navigation
- focus states
- disabled states
- selected states
- hover states
- readable muted text
- dark-mode contrast
- touch targets
- reduced motion

Visual subtlety must never destroy usability.

---

# 43. DATA-DENSE INTERFACES

The token system must work for information-heavy templates:

- SaaS dashboards
- documentation
- job boards
- finance
- CRM
- developer tools
- project management
- analytics
- e-commerce

Density should be controlled through:

- typography
- spacing
- grouping
- borders
- hierarchy

Not visual clutter.

---

# 44. TEMPLATE-SPECIFIC TOKENS

Individual templates may define their own variables.

Example:

```css
--template-accent
--template-sidebar-width
--template-content-width
--template-card-radius
--template-density
```

Template-specific tokens should extend the shared system.

Do not modify the entire global design language for one template.

---

# 45. TEMPLATE PERSONALITY

The shared system should establish the foundation.

Templates should remain visually distinct.

For example:

Documentation:

```text
editorial
compact
technical
typography-driven
```

Job Board:

```text
structured
dense
content-focused
```

SaaS Dashboard:

```text
analytical
operational
data-focused
```

Developer Portfolio:

```text
personal
technical
expressive
```

Agency:

```text
visual
polished
portfolio-oriented
```

All should still feel like DevSnips.

---

# 46. CONTENT RULES

Templates should use realistic content.

Avoid excessive use of:

```text
Lorem ipsum
Card title
Description here
John Doe
12345
```

Use realistic:

- names
- dates
- titles
- metrics
- categories
- statuses
- descriptions
- examples
- technical values

Good content is part of good visual design because it demonstrates actual spacing and density.

---

# 47. PREVIEW.HTML CONVENTION

Every individual template folder MUST contain exactly one:

```text
preview.html
```

Example:

```text
Vanilla/
└── Templates/
    ├── design-tokens.md
    │
    ├── SaaS Dashboard/
    │   └── preview.html
    │
    ├── Documentation Site/
    │   └── preview.html
    │
    └── Job Board/
        └── preview.html
```

`preview.html` is the canonical preview displayed by the DevSnips website.

It must represent the real template.

It must:

- be fully responsive
- use the actual template design
- use realistic content
- use the template's real CSS/JS
- work without a backend
- use relative paths
- load correctly when opened directly
- contain no broken interactions
- contain no JavaScript errors

Do NOT create:

```text
desktop-preview.html
tablet-preview.html
mobile-preview.html
```

There must be exactly one `preview.html` for every template folder.

---

# 48. TEMPLATE FOLDER STRUCTURE

The root structure is:

```text
DevSnips/
└── Vanilla/
    └── Templates/
        ├── design-tokens.md
        │
        ├── SaaS Dashboard/
        │   ├── preview.html
        │   ├── ...
        │
        ├── Documentation Site/
        │   ├── preview.html
        │   ├── ...
        │
        └── ...
```

Do NOT create:

```text
_templates/
_shared/
design-system/
Vanilla/Templates/system/
```

The token specification lives directly at:

```text
Vanilla/Templates/design-tokens.md
```

---

# 49. IMPLEMENTATION EXPECTATION

This task creates the shared specification.

Do not turn this into a complete component library.

Do not create:

- React
- Vue
- Next.js
- Tailwind
- Bootstrap
- backend infrastructure

The token specification should be framework-independent and designed primarily for:

- HTML
- CSS
- Vanilla JavaScript

Individual templates may use lightweight tools such as Pico CSS when appropriate, while still following this visual system.

---

# 50. VALIDATION

Validate the design system against at least:

1. SaaS Dashboard
2. Documentation
3. Job Board
4. Developer Portfolio
5. Agency Website

Check whether it can support:

- light mode
- dark mode
- desktop
- tablet
- mobile
- dense tables
- long-form content
- forms
- navigation
- cards
- dashboards
- documentation
- status states

The system should support all of these without forcing them into a single visual style.

---

# 51. FINAL STANDARD

The DevSnips Vanilla design language should communicate:

> Professional interfaces designed with intention.

The visual quality should come from:

- typography
- spacing
- hierarchy
- alignment
- realistic content
- subtle borders
- neutral surfaces
- controlled color
- responsive behavior
- accessibility
- consistency

Not from:

- glow
- neon
- excessive gradients
- excessive rounding
- decorative noise
- generic AI aesthetics
- giant marketing sections
- artificial content

Create the specification at:

```text
Vanilla/Templates/design-tokens.md
```

This file becomes the visual reference that every future Vanilla template should follow.

Do not create a new template in this task.

Do not create a `_shared` folder.

Do not move the design-token specification elsewhere.

The output of this task is the complete:

```text
Vanilla/Templates/design-tokens.md
```

file.
