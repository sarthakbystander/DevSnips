# DevSnips Component Structure Specification

## Problem

Currently, DevSnips treats **categories** as single components. For example:
- `Buttons/buttons-actions.html` contains 10+ unrelated components
- `Gradient/Button-Gradient.html` contains all gradient button variants in one file

This makes components:
- Unsearchable (can't link directly to "Gradient Pill Button")
- Hard to navigate (500+ line files)
- Not SEO-friendly (no pages for specific components)

## Architecture

DevSnips organizes content under each technology (`Tailwind/`, `Vanilla/`, `React/`)
into content types. **Tailwind** has three first-class content types;
**Vanilla** and **React** use two:

```
Tailwind/
├── Components/   # reusable UI building blocks
├── Sections/     # larger reusable page sections (compositions of components)
└── Templates/    # complete website / page templates

<Vanilla|React>/
├── Components/   # reusable UI building blocks (and former sections, merged)
└── Templates/    # complete website / page templates
```

There are no standalone `Utilities/` or `Resources/` collections. In Tailwind,
`Sections/` is a first-class type (distinct from `Components/`); in Vanilla/React
the former sections are merged into `Components/`.

Every Tailwind item declares its content type via a lowercase `type` field in
`metadata.json` and in `snippets-index.json`:

| `type` | Category | What it is |
|--------|----------|------------|
| `component` | Components | One focused interface pattern (Button, Card, Modal…). |
| `section` | Sections | A larger composition occupying part of a page (Hero, Pricing, FAQ…). |
| `template` | Templates | A complete page or substantial page experience (SaaS, Agency…). |

## Desired Structure

Each **variant** becomes its own:
1. Searchable page
2. Folder in the filesystem
3. Indexable by search engines

### Component Folder Structure

```
<Technology>/Components/
└── {Component Name}/
    ├── {Variant-01}/
    │   ├── preview.html        # Interactive preview (Tailwind) / <slug>.html (Vanilla)
    │   ├── code.html          # Copy-paste ready code (Tailwind)
    │   ├── README.md          # Variant-specific documentation (optional)
    │   └── metadata.json      # Variant metadata
    ├── {Variant-02}/
    ├── {Variant-03}/
    └── metadata.json          # (optional) family/grouping metadata
```

### Example: Gradient Button

```
Buttons/
└── Gradient Button/
    ├── linear/
    │   ├── preview.html
    │   ├── code.html
    │   └── metadata.json
    ├── multi-stop/
    │   ├── preview.html
    │   └── ...
    ├── directional/
    ├── pill/
    ├── shadow/
    ├── dark-background/
    ├── README.md
    └── metadata.json
```

### File Types

| File | Purpose |
|------|---------|
| `preview.html` | Interactive preview with all states |
| `code.html` | Clean, copy-paste ready code |
| `README.md` | Usage notes, accessibility, tips |
| `metadata.json` | SEO, tags, related components |

## Metadata Schema

```json
{
  "name": "Gradient Button - Linear",
  "component": "Gradient Button",
  "variant": "Linear",
  "description": "Two-color horizontal gradient button",
  "category": "Components",
  "subcategory": "Buttons",
  "tech": ["Tailwind CSS", "HTML"],
  "tags": ["gradient", "button", "linear", "blue"],
  "searchTerms": ["gradient button", "linear gradient", "blue button"],
  "related": ["gradient-multi-stop", "gradient-pill"],
  "accessibility": {
    "focus": "Visible focus ring included",
    "aria": "Use disabled attribute for disabled state",
    "touch": "44x44px minimum touch target"
  }
}
```

## Benefits

1. **Search**: Users find "Tailwind Gradient Pill Button" directly
2. **SEO**: Each variant has its own URL and meta tags
3. **Scalability**: Add unlimited variants to any component
4. **Contributions**: Contributors add single variants, not entire categories
5. **Counts**: "Gradient Button (8 variants)" vs "1 component"

## Migration

1. Split monolithic files into individual variant folders
2. Create metadata.json for each variant
3. Update parent index.json to reference variant paths
4. Update snippets-index.json for global search

## Naming Conventions

- Folder names: kebab-case (`gradient-button`, `pill-button`)
- Variants: kebab-case (`linear`, `multi-stop`, `dark-background`)
- Display names: Title Case (`Gradient Button`)
- Tags: lowercase, hyphenated (`gradient-button`, `cta`)
