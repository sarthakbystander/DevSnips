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

---

# 1. REPOSITORY RULE

The design-token specification MUST exist directly at:

```text
Vanilla/Templates/design-tokens.md
```

Do NOT create:

```text
Vanilla/Templates/_shared/
Vanilla/Templates/design-system/
Vanilla/Templates/shared/
Vanilla/design-tokens.md
Vanilla/Templates/system/
```

Do NOT create a shared folder for the token system.

`design-tokens.md` is the single source of truth for the visual foundation used by all DevSnips Vanilla templates.

---

# 2. PURPOSE

Create one coherent visual foundation for the entire DevSnips Vanilla Templates collection.

Different templates may have different personalities, density, layouts, and content structures, but they must feel like they belong to the same product family.

Examples:

```text
SaaS Dashboard     → structured, analytical, operational
Documentation      → editorial, technical, typography-focused
Job Board          → dense, structured, content-heavy
Developer Portfolio → personal, technical, expressive
Agency             → visual, polished, portfolio-oriented
E-commerce         → commercial, product-focused
LMS                → educational, structured, progress-oriented
```

They must NOT become copies of one another.

The design tokens provide the common visual language.

---

# 3. PRIMARY AESTHETIC

The default DevSnips Vanilla aesthetic is:

```text
minimal
light
editorial
clean
neutral
typography-driven
product-focused
information-dense
responsive
accessible
lightweight
restrained
intentional
```

The visual quality must come from:

```text
typography
spacing
alignment
hierarchy
content density
subtle borders
surface contrast
controlled color
responsive behavior
micro-interactions
```

The interface should feel:

> Designed, not generated.

The default visual impression should be closer to a refined documentation platform or premium product interface than a decorative marketing template.

---

# 4. VISUAL PRIORITIES

Use this priority order:

1. Typography
2. Information hierarchy
3. Spacing
4. Alignment
5. Content density
6. Borders
7. Surface hierarchy
8. Controlled accent color
9. Interaction feedback
10. Decoration

Decoration must never compensate for weak hierarchy or spacing.

---

# 5. DEFAULT DESIGN CHARACTER

The DevSnips default should be:

```text
white background
black / near-black primary text
soft gray secondary text
very subtle gray borders
small controlled radius
minimal shadows
restrained color
large but intentional whitespace
compact navigation
precise alignment
clean content containers
```

Do not make every page feel empty.

Whitespace should be intentional and balanced with useful content density.

---

# 6. AVOID THE GENERIC AI / SAAS LOOK

The shared system must NOT default to:

```text
glowing purple
neon blue
purple-on-black
gradient-heavy backgrounds
gradient text
glassmorphism
frosted cards
giant rounded cards
excessive pill controls
glowing borders
colored shadows
oversized floating icons
decorative blobs
blur-heavy layouts
animated backgrounds
generic three-column feature grids
fake futuristic UI
oversized hero sections
excessive drop shadows
```

Especially avoid:

```text
dark charcoal background
+
purple gradient cards
+
neon blue buttons
+
gradient headings
+
AI-style decorative effects
```

That is not the default DevSnips design language.

---

# 7. DESIGN TOKEN ARCHITECTURE

Use four layers:

```text
Primitive Tokens
      ↓
Semantic Tokens
      ↓
Template Tokens
      ↓
Components
```

## Primitive Tokens

Raw design values.

Example:

```css
--ds-gray-100
--ds-black
--ds-white
--ds-space-4
--ds-radius-sm
```

## Semantic Tokens

Meaning-based values.

Example:

```css
--ds-bg-canvas
--ds-bg-surface
--ds-text-primary
--ds-text-secondary
--ds-border-default
--ds-action-primary
```

Components should primarily consume semantic tokens.

## Template Tokens

Template-specific adaptations.

Example:

```css
--template-accent
--template-sidebar-width
--template-content-width
--template-density
```

Template tokens may override presentation without changing the global language.

---

# 8. NAMING CONVENTION

Shared tokens:

```text
--ds-[category]-[property]
```

Examples:

```css
--ds-bg-canvas
--ds-text-primary
--ds-border-default
--ds-space-4
--ds-radius-sm
--ds-shadow-xs
--ds-font-sans
```

Template tokens:

```text
--template-[property]
```

Examples:

```css
--template-accent
--template-sidebar-width
--template-content-width
--template-reading-width
--template-density
```

Keep naming consistent across every Vanilla template.

---

# 9. COLOR PHILOSOPHY

Color is supportive, not decorative.

The default system must be:

```text
neutral-first
black-first
white-first
low-saturation
semantic when necessary
```

Most interfaces should be visually understandable with grayscale alone.

Accent colors should only reinforce hierarchy, interaction, categorization, or state.

---

# 10. PRIMITIVE NEUTRAL SCALE

Define:

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

Recommended implementation:

```css
--ds-gray-0: #ffffff;
--ds-gray-25: #fdfdfd;
--ds-gray-50: #fafafa;
--ds-gray-100: #f5f5f5;
--ds-gray-150: #eeeeee;
--ds-gray-200: #e7e7e7;
--ds-gray-300: #d7d7d7;
--ds-gray-400: #b8b8b8;
--ds-gray-500: #8f8f8f;
--ds-gray-600: #6b6b6b;
--ds-gray-700: #4a4a4a;
--ds-gray-800: #2f2f2f;
--ds-gray-850: #222222;
--ds-gray-900: #171717;
--ds-gray-950: #0f0f0f;
--ds-gray-1000: #000000;
```

The exact values may be adjusted during implementation if contrast or browser rendering requires it.

---

# 11. ACCENT SCALES

Provide controlled scales for:

```text
blue
green
red
yellow
orange
```

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

Repeat the same structure for other semantic colors.

Do NOT make violet or indigo the default DevSnips accent.

---

# 12. SEMANTIC BACKGROUND TOKENS

Define:

```css
--ds-bg-canvas
--ds-bg-surface
--ds-bg-surface-subtle
--ds-bg-surface-raised
--ds-bg-overlay
```

Light-mode defaults:

```css
--ds-bg-canvas: var(--ds-gray-0);
--ds-bg-surface: var(--ds-gray-0);
--ds-bg-surface-subtle: var(--ds-gray-50);
--ds-bg-surface-raised: var(--ds-gray-0);
--ds-bg-overlay: rgb(0 0 0 / 0.45);
```

Use surface variation sparingly.

---

# 13. SEMANTIC TEXT TOKENS

Define:

```css
--ds-text-primary
--ds-text-secondary
--ds-text-muted
--ds-text-disabled
--ds-text-inverse
```

Recommended light values:

```css
--ds-text-primary: #111111;
--ds-text-secondary: #4b4b4b;
--ds-text-muted: #707070;
--ds-text-disabled: #a0a0a0;
--ds-text-inverse: #ffffff;
```

Muted text must remain readable.

Do not sacrifice accessibility for visual subtlety.

---

# 14. BORDER TOKENS

Define:

```css
--ds-border-subtle
--ds-border-default
--ds-border-strong
--ds-border-focus
```

Recommended light values:

```css
--ds-border-subtle: #f0f0f0;
--ds-border-default: #e5e5e5;
--ds-border-strong: #d2d2d2;
--ds-border-focus: #111111;
```

The default structural border should normally be:

```text
1px
```

Use borders for:

```text
cards
panels
navigation
tables
inputs
dividers
lists
code blocks
```

Prefer borders over heavy shadows.

---

# 15. ACTION TOKENS

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

Default primary action:

```css
--ds-action-primary: #111111;
--ds-action-primary-hover: #222222;
--ds-action-primary-active: #000000;
```

Primary actions should feel deliberate.

Do not make every interactive element visually dominant.

---

# 16. STATUS TOKENS

Define:

```css
--ds-status-success
--ds-status-success-bg
--ds-status-success-border

--ds-status-warning
--ds-status-warning-bg
--ds-status-warning-border

--ds-status-danger
--ds-status-danger-bg
--ds-status-danger-border

--ds-status-info
--ds-status-info-bg
--ds-status-info-border
```

Use status colors for:

```text
alerts
badges
validation
notifications
state indicators
system messages
```

Use muted backgrounds and borders instead of highly saturated blocks.

---

# 17. TYPOGRAPHY

Typography is one of the most important parts of the DevSnips visual system.

Define:

```css
--ds-font-sans
--ds-font-mono
--ds-font-display
```

Recommended:

```css
--ds-font-sans:
  Inter,
  ui-sans-serif,
  system-ui,
  -apple-system,
  BlinkMacSystemFont,
  "Segoe UI",
  sans-serif;

--ds-font-mono:
  "SFMono-Regular",
  Consolas,
  "Liberation Mono",
  monospace;

--ds-font-display: var(--ds-font-sans);
```

Do not require an external font download for templates to function correctly.

System fallbacks must remain usable.

---

# 18. TYPOGRAPHY SCALE

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

Recommended scale:

```css
--ds-text-xs: 12px;
--ds-text-sm: 13px;
--ds-text-md: 14px;
--ds-text-lg: 16px;
--ds-text-xl: 18px;
--ds-text-2xl: 22px;
--ds-text-3xl: 28px;
--ds-text-4xl: 36px;
--ds-text-5xl: 44px;
```

Use larger sizes only when hierarchy requires them.

Normal product interfaces should remain compact.

---

# 19. FONT WEIGHTS

Define:

```css
--ds-weight-regular
--ds-weight-medium
--ds-weight-semibold
--ds-weight-bold
```

Recommended:

```css
--ds-weight-regular: 400;
--ds-weight-medium: 500;
--ds-weight-semibold: 600;
--ds-weight-bold: 700;
```

Do not make every heading bold.

---

# 20. LINE HEIGHT

Define:

```css
--ds-leading-tight
--ds-leading-snug
--ds-leading-normal
--ds-leading-relaxed
```

Recommended:

```css
--ds-leading-tight: 1.15;
--ds-leading-snug: 1.3;
--ds-leading-normal: 1.5;
--ds-leading-relaxed: 1.65;
```

Use tighter values for headings and relaxed values for long-form content.

---

# 21. LETTER SPACING

Define:

```css
--ds-tracking-tight
--ds-tracking-normal
--ds-tracking-wide
```

Use restrained tracking.

Do not rely on uppercase text plus large letter spacing as the primary hierarchy mechanism.

---

# 22. SPACING SYSTEM

Define:

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

Recommended:

```css
--ds-space-1: 4px;
--ds-space-2: 8px;
--ds-space-3: 12px;
--ds-space-4: 16px;
--ds-space-5: 20px;
--ds-space-6: 24px;
--ds-space-8: 32px;
--ds-space-10: 40px;
--ds-space-12: 48px;
--ds-space-16: 64px;
--ds-space-20: 80px;
--ds-space-24: 96px;
--ds-space-32: 128px;
```

Prefer these tokens over arbitrary values.

---

# 23. COMPONENT SPACING

Define:

```css
--ds-component-padding-xs
--ds-component-padding-sm
--ds-component-padding-md
--ds-component-padding-lg
```

Use these consistently across:

```text
buttons
cards
inputs
lists
navigation
tables
panels
dropdowns
dialogs
```

---

# 24. PAGE AND CONTENT WIDTH

Define:

```css
--ds-container-xs
--ds-container-sm
--ds-container-md
--ds-container-lg
--ds-container-xl
--ds-container-wide

--ds-content-reading
--ds-content-default
--ds-content-wide
```

Recommended principles:

```text
reading content → narrow
documentation   → readable
dashboards      → wide
tables          → expandable
marketing       → controlled
```

Never allow long-form text to become unnecessarily wide.

---

# 25. PAGE PADDING

Define:

```css
--ds-page-padding-mobile
--ds-page-padding-tablet
--ds-page-padding-desktop
```

Recommended starting values:

```css
--ds-page-padding-mobile: 16px;
--ds-page-padding-tablet: 24px;
--ds-page-padding-desktop: 32px;
```

Templates may increase these values when their layout requires it.

---

# 26. SECTION SPACING

Define:

```css
--ds-section-gap-sm
--ds-section-gap-md
--ds-section-gap-lg
--ds-section-gap-xl
```

Whitespace must establish hierarchy.

Do not create huge empty sections simply to make the UI appear premium.

---

# 27. GRID TOKENS

Define:

```css
--ds-grid-gap-xs
--ds-grid-gap-sm
--ds-grid-gap-md
--ds-grid-gap-lg
--ds-grid-gap-xl
```

Grid density should be chosen according to the template.

---

# 28. RADIUS SYSTEM

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

Recommended values:

```css
--ds-radius-none: 0;
--ds-radius-xs: 2px;
--ds-radius-sm: 4px;
--ds-radius-md: 6px;
--ds-radius-lg: 8px;
--ds-radius-xl: 10px;
--ds-radius-full: 999px;
```

Default DevSnips templates should favor:

```text
none
xs
sm
md
```

Large radius values are intentional exceptions.

Full rounding is mainly for:

```text
avatars
badges
tags
status pills
special controls
```

Do not round everything.

---

# 29. SHADOW SYSTEM

Define:

```css
--ds-shadow-none
--ds-shadow-xs
--ds-shadow-sm
--ds-shadow-md
--ds-shadow-lg
```

Recommended:

```css
--ds-shadow-none: none;
--ds-shadow-xs: 0 1px 2px rgb(0 0 0 / 0.04);
--ds-shadow-sm: 0 2px 6px rgb(0 0 0 / 0.06);
--ds-shadow-md: 0 6px 18px rgb(0 0 0 / 0.08);
--ds-shadow-lg: 0 12px 32px rgb(0 0 0 / 0.10);
```

Most components should use:

```text
none
xs
```

Use stronger shadows only for temporary overlays such as:

```text
dropdowns
dialogs
floating panels
```

Never use:

```text
neon shadows
colored shadows
glows
massive shadows
```

---

# 30. BUTTON TOKENS

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

Primary buttons should generally be:

```text
black
white text
small radius
thin or no visible outer border
subtle hover state
```

Secondary buttons should generally be:

```text
white
dark text
1px border
subtle hover surface
```

Buttons must support:

```text
hover
active
focus
disabled
loading
```

---

# 31. INPUT TOKENS

Define:

```css
--ds-input-height-sm
--ds-input-height-md
--ds-input-height-lg

--ds-input-padding-x
--ds-input-padding-y

--ds-input-radius
```

Inputs should be:

```text
white or subtle gray surface
1px border
clear focus state
comfortable text size
minimal decoration
```

Support:

```text
default
focus
error
success
disabled
readonly
```

Avoid heavy inner shadows and glowing focus effects.

---

# 32. CARD TOKENS

Define:

```css
--ds-card-padding
--ds-card-radius
--ds-card-border
--ds-card-shadow
```

Cards are optional.

Do not turn every section into a card.

Use a card when it improves:

```text
grouping
scannability
hierarchy
interaction
```

A section that can exist cleanly without a container should generally remain unboxed.

---

# 33. NAVIGATION TOKENS

Define:

```css
--ds-nav-height
--ds-nav-item-height
--ds-nav-gap
--ds-nav-padding-x
--ds-nav-padding-y
```

Navigation should feel lightweight.

Prefer:

```text
clear alignment
small typography
thin separators
subtle active state
minimal background treatment
```

Support:

```text
hover
active
selected
focus
collapsed
mobile
```

---

# 34. TABLE TOKENS

Define:

```css
--ds-table-cell-padding-x
--ds-table-cell-padding-y
--ds-table-row-height
--ds-table-header-height
```

Tables should prioritize:

```text
scanability
alignment
density
hierarchy
```

Use light row dividers rather than boxed cells wherever possible.

---

# 35. BADGE TOKENS

Define:

```css
--ds-badge-height
--ds-badge-padding-x
--ds-badge-padding-y
--ds-badge-radius
```

Badges communicate:

```text
status
category
priority
state
```

Keep them small and restrained.

Do not use badges purely as decoration.

---

# 36. ICON TOKENS

Define:

```css
--ds-icon-xs
--ds-icon-sm
--ds-icon-md
--ds-icon-lg
--ds-icon-xl
```

Icons must:

```text
align with text
remain lightweight
use consistent sizing
support meaning
```

Avoid oversized decorative icons.

Icons should not visually dominate the interface.

---

# 37. RESPONSIVE SYSTEM

Define:

```css
--ds-breakpoint-sm
--ds-breakpoint-md
--ds-breakpoint-lg
--ds-breakpoint-xl
```

Breakpoints represent meaningful layout changes, not simply device labels.

Responsive design should transform composition where necessary.

Examples:

```text
sidebar → drawer
multi-column grid → reduced grid
large toolbar → grouped controls
wide table → compact representation
large header → compact header
secondary content → collapsible section
```

---

# 38. MOBILE DESIGN

Every template must remain intentionally usable on:

```text
large desktop
desktop
laptop
tablet
mobile
small mobile
```

Mobile must:

```text
avoid horizontal overflow
maintain readable typography
preserve usable controls
prevent clipping
handle long labels
handle tables
handle code
handle dialogs
handle navigation
handle filters
```

Never simply shrink the desktop layout.

---

# 39. MOTION

Define:

```css
--ds-duration-fast
--ds-duration-normal
--ds-duration-slow

--ds-ease-standard
--ds-ease-emphasized
```

Recommended direction:

```text
fast   → 100–150ms
normal → 150–200ms
slow   → 200–300ms
```

Use motion for:

```text
dropdowns
drawers
dialogs
navigation
state changes
subtle feedback
```

Do not use animation for decoration.

Respect:

```css
@media (prefers-reduced-motion: reduce)
```

---

# 40. Z-INDEX

Define:

```css
--ds-z-base
--ds-z-dropdown
--ds-z-sticky
--ds-z-overlay
--ds-z-modal
--ds-z-toast
```

Use predictable stacking.

Avoid arbitrary extreme z-index values.

---

# 41. LIGHT MODE

Light mode is the default DevSnips experience.

Use primarily:

```text
white
off-white
soft gray
charcoal
black
```

with controlled semantic accents.

Hierarchy should come from:

```text
spacing
typography
border contrast
surface contrast
```

not from decorative backgrounds.

---

# 42. DARK MODE

Every template should support a simple dark-mode toggle.

Dark mode should feel like the same design system inverted.

Recommended values:

```css
--ds-bg-canvas: #0a0a0a;
--ds-bg-surface: #111111;
--ds-bg-surface-subtle: #171717;
--ds-bg-surface-raised: #1b1b1b;

--ds-text-primary: #f5f5f5;
--ds-text-secondary: #c8c8c8;
--ds-text-muted: #909090;
--ds-text-disabled: #5f5f5f;
--ds-text-inverse: #111111;

--ds-border-subtle: #1a1a1a;
--ds-border-default: #272727;
--ds-border-strong: #363636;
--ds-border-focus: #ffffff;

--ds-action-primary: #f5f5f5;
--ds-action-primary-hover: #ffffff;
--ds-action-primary-active: #e5e5e5;
```

Do NOT turn dark mode into:

```text
black + neon purple
black + glowing gradients
black + glassmorphism
```

Dark mode should remain calm, clean, and readable.

---

# 43. BLACK TOGGLE

The theme toggle should be visually minimal.

Preferred characteristics:

```text
small
compact
black/white
bordered
simple icon
clear focus state
```

Avoid oversized switch components or decorative sun/moon animations.

The toggle should feel like part of the interface rather than a feature showcase.

---

# 44. ACCESSIBILITY

All tokens must support accessible interfaces.

Consider:

```text
contrast
keyboard navigation
visible focus states
disabled states
selected states
hover states
dark-mode contrast
touch targets
reduced motion
```

Do not use color as the only indicator of state.

Subtle design must never reduce usability.

---

# 45. DATA-DENSE INTERFACES

The token system must work for:

```text
SaaS dashboards
documentation
job boards
finance interfaces
CRM
developer tools
project management
analytics
e-commerce
```

Density should be controlled with:

```text
typography
spacing
grouping
borders
hierarchy
```

not clutter.

---

# 46. TEMPLATE-SPECIFIC TOKENS

Individual templates may define:

```css
--template-accent
--template-sidebar-width
--template-content-width
--template-reading-width
--template-card-radius
--template-density
--template-header-height
```

Template-specific tokens extend the shared system.

They must NOT redefine the entire global visual language.

---

# 47. TEMPLATE PERSONALITY

The shared tokens establish the foundation, while templates establish personality.

## Documentation

```text
editorial
technical
compact
typography-driven
highly readable
```

## Job Board

```text
structured
dense
content-focused
scannable
filter-heavy
```

## SaaS Dashboard

```text
analytical
operational
data-focused
structured
```

## Developer Portfolio

```text
personal
technical
expressive
minimal
```

## Agency

```text
visual
polished
portfolio-oriented
editorial
```

Every template must still feel recognizably DevSnips.

---

# 48. CONTENT RULES

Templates must use realistic content.

Avoid excessive placeholder content such as:

```text
Lorem ipsum
Card title
Description here
John Doe
12345
```

Use realistic:

```text
names
dates
titles
metrics
categories
statuses
descriptions
technical values
navigation labels
examples
```

Content is part of visual quality because it demonstrates real spacing, hierarchy, and density.

---

# 49. COMPONENT PHILOSOPHY

Components should be visually quiet and structurally strong.

Prefer:

```text
1px borders
subtle surfaces
small radii
compact typography
clear alignment
short transitions
```

over:

```text
gradients
glows
large shadows
giant radius
heavy decoration
```

Components should look refined even without color.

---

# 50. DOCUMENTATION-STYLE INTERFACES

Documentation templates should especially prioritize:

```text
readable content width
sticky navigation where useful
thin dividers
small navigation typography
strong heading hierarchy
compact metadata
clear code blocks
quiet active states
```

The interface should feel editorial and technical rather than like a marketing landing page.

---

# 51. LIGHTWEIGHT IMPLEMENTATION

The token system is framework-independent.

Primary target:

```text
HTML
CSS
Vanilla JavaScript
```

Keep implementation lightweight.

Prefer:

```text
CSS custom properties
native CSS
system fonts
small JavaScript
minimal dependencies
```

Avoid introducing dependencies only to implement simple visual behavior.

Individual templates may use lightweight tools such as Pico CSS when appropriate, but the design tokens remain the source of truth.

---

# 52. CSS CUSTOM PROPERTY REQUIREMENT

The final implementation must expose the shared design system through CSS custom properties.

Example:

```css
:root {
  --ds-bg-canvas: #ffffff;
  --ds-text-primary: #111111;
  --ds-border-default: #e5e5e5;
  --ds-radius-sm: 4px;
  --ds-space-4: 16px;
}

[data-theme="dark"] {
  --ds-bg-canvas: #0a0a0a;
  --ds-text-primary: #f5f5f5;
  --ds-border-default: #272727;
}
```

Components should consume semantic variables instead of hardcoded visual values whenever practical.

---

# 53. PREVIEW.HTML CONVENTION

Every individual template folder MUST contain exactly one:

```text
preview.html
```

Example:

```text
Vanilla/
└── Templates/
    ├── design-tokens.md
    ├── SaaS Dashboard/
    │   └── preview.html
    ├── Documentation Site/
    │   └── preview.html
    └── Job Board/
        └── preview.html
```

`preview.html` is the canonical preview displayed by DevSnips.

It must:

```text
be fully responsive
use the actual template design
use realistic content
use the real CSS/JS
work without a backend
use relative paths
load when opened directly
contain no broken interactions
contain no JavaScript errors
```

Do NOT create:

```text
desktop-preview.html
tablet-preview.html
mobile-preview.html
```

There must be exactly one `preview.html` per template.

---

# 54. TEMPLATE STRUCTURE

Root structure:

```text
DevSnips/
└── Vanilla/
    └── Templates/
        ├── design-tokens.md
        ├── SaaS Dashboard/
        │   ├── preview.html
        │   └── ...
        ├── Documentation Site/
        │   ├── preview.html
        │   └── ...
        └── ...
```

Do NOT create:

```text
_templates/
_shared/
design-system/
system/
Vanilla/Templates/shared/
Vanilla/Templates/_shared/
```

---

# 55. IMPLEMENTATION EXPECTATION

This file defines the shared visual system.

Do NOT turn this task into a complete component library.

Do NOT create:

```text
React
Vue
Next.js
Tailwind
Bootstrap
backend infrastructure
```

The specification must remain framework-independent.

---

# 56. VALIDATION

Validate the design system against at least:

```text
SaaS Dashboard
Documentation
Job Board
Developer Portfolio
Agency Website
```

The system must be able to support:

```text
light mode
dark mode
desktop
tablet
mobile
dense tables
long-form content
forms
navigation
cards
dashboards
documentation
status states
```

without forcing every template into the same layout.

---

# 57. FINAL VISUAL STANDARD

DevSnips Vanilla should communicate:

> Professional interfaces designed with intention.

The visual quality should come from:

```text
typography
spacing
hierarchy
alignment
realistic content
subtle borders
neutral surfaces
controlled color
responsive behavior
accessibility
consistency
```

Not from:

```text
glow
neon
excessive gradients
excessive rounding
decorative noise
generic AI aesthetics
giant marketing sections
artificial content
heavy effects
```

The default visual benchmark is:

```text
minimal
light
black-first
editorial
technical
refined
responsive
lightweight
```

The interface should look polished even when every decorative effect is removed.

---

# 58. FINAL FILE

Create and maintain this specification at exactly:

```text
Vanilla/Templates/design-tokens.md
```

This file is the single visual reference for all future DevSnips Vanilla templates.

Do not move it.

Do not duplicate it.

Do not create a shared folder.

Do not create a new template as part of this task.

The output of this task is:

```text
Vanilla/Templates/design-tokens.md
```
