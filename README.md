# 🚀 DevSnips – Component Library

Reusable frontend components organized as design system families.

## Structure

```
├── Tailwind/
│   ├── Components/            # 12 families, 310 variants
│   │   ├── Accordions/        # 15 variants
│   │   ├── Buttons/           # 58 variants (15 styles, each with sub-variants)
│   │   ├── Cards/             # 40 variants
│   │   ├── Dropdowns/         # 30 variants
│   │   ├── Input/             # 49 variants
│   │   ├── Modals/            # 30 variants
│   │   ├── Navigation/        # 35 variants
│   │   ├── Progress/          # 6 variants
│   │   ├── Tables/            # 20 variants
│   │   ├── Tabs/              # 15 variants
│   │   ├── Toasts/            # 6 variants
│   │   └── Tooltips/          # 6 variants
│   ├── Pages/                 # (reserved)
│   ├── Sections/              # 216 variants (15-style categories, multi-concept, SaaS)
│   ├── Templates/             # 8 full-site templates (3 multipage, 5 single-page)
│   └── Utilities/             # (reserved)
├── Vanilla/
│   ├── Components/            # 19 families, 232 variants
│   │   ├── Accordions/        # 5 variants
│   │   ├── Alerts/            # 2 variants
│   │   ├── Avatars/           # 1 variant
│   │   ├── Badges/            # 2 variants
│   │   ├── Buttons/           # 14 variants
│   │   ├── Cards/             # 15 variants
│   │   ├── Display/           # 7 variants
│   │   ├── Dropdowns/        # 1 variant
│   │   ├── Forms/             # 38 variants (Contact, Login, Newsletter, Other, Register, Search)
│   │   ├── Loaders/           # 8 variants
│   │   ├── Marketing/        # 6 variants (FAQ, Hero, Pricing, Testimonials)
│   │   ├── Media/             # 17 variants
│   │   ├── Modals/            # 12 variants
│   │   ├── Navigation/       # 24 variants (Breadcrumb, Menu, Navbar, Other, Pagination, Sidebar)
│   │   ├── Other/            # 65 variants
│   │   ├── Ratings/          # 3 variants
│   │   ├── Tables/           # 4 variants
│   │   ├── Tabs/             # 5 variants
│   │   └── Tooltips/        # 3 variants
│   ├── Sections/              # Neo-Brutalist website sections (16 families, 65 variants)
│   ├── Templates/             # 14 templates (Landing-Pages, Standalone, +11 themed)
│   ├── Tools/                # (reserved)
│   ├── Utilities/             # 76 utility snippets (Animations, Clipboard, Layout, Scrollbar, Theming, Typography)
│   └── Resources/             # 67 JS helper snippets (Helpers, LocalStorage)
├── snippets-index.json        # Component family index (114 families, 988 variants)
└── README.md
```

## Quick Start

1. Browse `Tailwind/Components/` for ready-to-use Tailwind components
2. Check `Vanilla/Components/` for HTML/CSS patterns
3. Copy, customize, and ship

## Component Families

### Tailwind (Production-Ready)

| Family | Variants | Styles |
|--------|----------|---------|
| **Accordions** | 15 | Basic, Animated, Bordered, Dark, FAQ, Glass, Icon, Minimal, Multi-Open, Nested, Pricing-FAQ, Settings, Sidebar, Single-Open, Timeline |
| **Buttons** | 58 | Basic (Primary/Secondary/Neutral/Sizes/Full-Width), Ghost (Primary/Colors/Dark/Sizes/Icon), Outline (Primary/Colors/Dashed/Pill/Dark), Filled (Primary/Soft/Rounded/Dark/Sizes/Muted), Glass, Neumorphism, Gradient (Linear/Multi-Stop/Directional/Pill/Shadow/Dark), Animated (Shine/Scale/Arrow/Icon), Icon (Basic/Rounded/Dark), Split (Dropdown/Icon), Loading (Spinner/Progress), Social (GitHub/Facebook/Google), Floating Action (Standard/Group/Extended), 3D (Basic/Colored), Minimal (Border/Underline) |
| **Cards** | 40 | Profile, Pricing, Product, Blog, Team, Testimonial, Feature, Dashboard-Stat, Analytics, KPI, Statistics, Notification, Event, Music, Video, Weather, Social-Post, NFT, Checkout, Order, Chat, File, Job, Course, Timeline, Glass, Minimal, Corporate, SaaS, Gradient, and more |
| **Dropdowns** | 30 | Action, Animated, Avatar, Basic, Checkbox, Click, Command, Context, Date-Filter, Divider, Filter, Floating, Hover, Icon, Language, Mega, Mobile, Multi-Level, Multi-Select, Notification, Profile, Quick-Actions, Radio, Searchable-Select, Select, Sidebar, Sort, Status, Theme, User-Account |
| **Input** | 49 | Animated-Focus, Character-Count, Chat-Input, Checkbox-Styled, Color-Picker, Corporate, Credit-Card, Currency-Input, CVV, Dark-Mode, Date-Picker, Disabled-Readonly, Email-Input, Expiration-Date, File-Upload, Filled, Floating-Label, Glassmorphism, Gradient-Border, Icon-Both/Left/Right, Markdown-Editor, Mention-Input, Modern-SaaS, Neumorphism, Number-Stepper, OTP-6-Digit, Outlined, Password-Toggle, Phone-Input, Radio-Styled, Range-Slider, Rich-Text-Editor, Rounded-Pill, Search-Bar/Autocomplete/Filters, Sharp-Corner, Split-Input, Tag-Input, Textarea, Toggle-Switch, Underline, URL-Input, Validation-States, With-Helper/Prefix/Suffix |
| **Modals** | 30 | Basic, Confirmation, Delete, Success, Error, Warning, Login, Signup, Forgot-Password, Reset-Password, Payment, Checkout, Share, Image-Preview, Video, Form, Settings, Drawer, Bottom-Sheet, Slide-Over, Fullscreen, Loading, Command-Palette, Notification, Multi-Step, OTP, Feedback, Subscription, Cookie-Consent, Update-Available |
| **Navigation** | 35 | Admin-Sidebar, Basic-Navbar, Blog, Bottom, Breadcrumb, Category, Centered, Collapsible-Sidebar, Corporate, Dashboard-Sidebar, Dock, Documentation, Ecommerce, Floating, Glass, Gradient, Hamburger, Horizontal, Icon, Mega, Mini-Sidebar, Mobile, Multi-Level, Offcanvas, Pagination, Profile, SaaS, Search, Settings, Split, Step, Sticky, Tab, Transparent, Vertical |
| **Progress** | 6 | Linear-Bar (determinate/indeterminate), Circular-Spinner (4 sizes), Skeleton-Loader (card/list), Segmented-Stepper (checkout), Step-Progress (timeline), Upload-Progress (multi-file) |
| **Tables** | 20 | Analytics, Basic, Bordered, Compact, Expandable, File-Manager, Filterable, Hover, Invoice, Leaderboard, Order-Management, Paginated, Pricing-Comparison, Product-Inventory, Responsive, Searchable, Selectable, Sortable, Striped, User-Management |
| **Tabs** | 15 | Multiple tab variants |
| **Toasts** | 6 | Basic, Status (Success/Error/Warning/Info), Action (Undo), Stacked, Persistent (progress bar), Minimal (pill) |
| **Tooltips** | 6 | Basic (top+arrow), Directional (top/right/bottom/left), Rich (title+description), Delayed (600ms), Icon (icon-button a11y), Status (success/warning/error/info themed) |

### Vanilla

**Components (19 families, 232 variants):** Accordions (5), Alerts (2), Avatars (1), Badges (2), Buttons (14), Cards (15), Display (7), Dropdowns (1), Forms (38 — Contact, Login, Newsletter, Other, Register, Search), Loaders (8), Marketing (6 — FAQ, Hero, Pricing, Testimonials), Media (17), Modals (12), Navigation (24 — Breadcrumb, Menu, Navbar, Other, Pagination, Sidebar), Other (65), Ratings (3), Tables (4), Tabs (5), Tooltips (3).

**Templates (14):** Landing-Pages (one-page-scrolling), Standalone (404-not-found-page, Coming-Soon), ai-tool-launch, blog-landing-pages, event-conference, freelancer-portfolio, html5-boilerplate, micro-saas-product, nft-web3-project, portfolio-site, product-launch, startup-template, template-element.

**Utilities (76 snippets):** Animations (33), Layout (22), Typography (10), Theming (7), Clipboard (3), Scrollbar (1). Pure CSS/JS patterns for layout, animation, theming, and typography.

**Resources (67 JS snippets):** Helpers (65 reusable JS functions) and LocalStorage (2 wrappers).

**Sections (Neo-Brutalist, 16 families, 65 variants):** Hero (10), Navigation (4), Features (5), Logos (3), Statistics (3), Products (6), Pricing (4), Testimonials (4), Team (3), Process (4), Content (4), Gallery (3), FAQ (2), CTA (4), Contact (3), Footer (3). See `Vanilla/Sections/README.md` and browse `Vanilla/Sections/index.html`.

### Tailwind Sections & Templates

**Sections (216 variants):** 11 categories × 15 design styles (404, Blog, Contact, FAQ, Footer, Logos, Navbar, Newsletter, Stats, Team, Testimonials); multi-concept sections (ai-product, app-ui, developer, marketing, premium-visual × 3 styles each); and 16 SaaS sections. See `Tailwind/Sections/`.

**Templates (8):** ai-saas-platform (multipage), baseline-conference (multipage), northline-atelier (multipage), krat-adventure (single-page), meridian (single-page), stratum (single-page), vesper (single-page), quiet-place (single-page). See `Tailwind/Templates/`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
