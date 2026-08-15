# DevSnips Content Structure Specification

This document defines how DevSnips organizes components, sections, templates, variants, and metadata. The structure is designed so every useful piece of content can be addressed independently by the repository, indexer, and future website.

## Design goals

DevSnips treats individual variants as first-class content. A variant should be:

- independently discoverable
- independently indexable
- easy to copy and reuse
- understandable without opening unrelated files
- stable enough to receive a permanent URL later

A family groups related variants. A content type describes the size and purpose of the content.

## Repository architecture

```text
DevSnips/
├── Tailwind/
│   ├── Components/
│   ├── Sections/
│   └── Templates/
├── Vanilla/
│   ├── Components/
│   └── Templates/
└── React/
    ├── Components/
    └── Templates/
```

### Tailwind

Tailwind has three first-class content types:

| Directory | `type` | Purpose |
|---|---|---|
| `Components/` | `component` | One focused reusable UI pattern. |
| `Sections/` | `section` | A larger page-section composition. |
| `Templates/` | `template` | A complete page or substantial page experience. |

### Vanilla and React

Vanilla and React use `Components/` and `Templates/`. Vanilla's former standalone section collection has been merged into `Components/`.

React is currently reserved for future content. Its structure should follow this specification when React content is introduced.

### Forbidden content collections

Do not create technology-level `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` collections. If something is a reusable UI pattern, it should have an appropriate component, section, or template classification. Repository tooling belongs under `_gen/` or `scripts/`.

## Family and variant model

A **family** is a group of related UI patterns, such as `Buttons`, `Cards`, `Navigation`, or `Pricing`.

A **variant** is one concrete implementation inside a family, such as `primary-button`, `icon-button`, or `pricing-comparison`.

The preferred structure is:

```text
<Technology>/<ContentType>/<Family>/<variant>/
```

For example:

```text
Tailwind/Components/Buttons/primary-button/
├── code.html
├── preview.html
└── metadata.json
```

Vanilla components use a single self-contained source file:

```text
Vanilla/Components/Buttons/3d-button-effect/
├── component.html
├── README.md
└── metadata.json
```

The directory name is the canonical component id/slug. The single primary component source file is always named `component.html` (inline `<style>` + `<script>`, copy-paste self-contained).

Templates are different because they may contain multiple pages and supporting files:

```text
Tailwind/Templates/<template-slug>/
├── metadata.json
├── preview.html
├── README.md
└── pages/
    ├── index.html
    └── ...
```

The exact internal template structure may vary when the template requires it. Do not force a multi-page template into the component three-file convention.

## Standard files

| File | Required for | Purpose |
|---|---|---|
| `code.html` | Tailwind components/sections | Clean copy-paste implementation. |
| `preview.html` | Tailwind components/sections | Standalone visual preview and demonstration. |
| `component.html` | Vanilla components | Self-contained single primary component source file (inline CSS + JS). |
| `metadata.json` | Indexed variants | Structured identity, classification, search, and feature data. |
| `README.md` | When useful / template-specific | Human-readable usage or implementation notes. |

`preview.html` is a demonstration environment. It may contain CDN imports, demo content, page framing, and preview-only JavaScript. `code.html` should not inherit unnecessary preview scaffolding.

## Metadata principles

Metadata is consumed by repository tooling and the future DevSnips website. It should be accurate, deterministic, and consistent with the filesystem.

A Tailwind variant must declare its content type:

```json
{
  "id": "primary-button-001",
  "name": "Primary Button",
  "description": "A primary call-to-action button with a clear focus state.",
  "type": "component",
  "category": "components",
  "subcategory": "buttons",
  "tags": ["button", "primary", "cta"],
  "responsive": true
}
```

The exact metadata schema used by the repository may contain additional fields. When adding fields, keep their meaning consistent across entries rather than creating one-off names.

### Required consistency rules

- `type` must match the directory for Tailwind content.
- IDs should be globally unique.
- Names and descriptions should describe the actual implementation.
- Categories and subcategories should agree with the family structure.
- Tags should be lowercase and useful for search.
- Boolean fields should use actual JSON booleans, not strings.
- Do not claim support for behavior that the code does not implement.

## Naming conventions

Filesystem names and IDs should use kebab-case:

```text
pricing-comparison
animated-accordion
multi-step-form
```

Display names should be human-readable:

```text
Pricing Comparison
Animated Accordion
Multi-Step Form
```

Avoid generic variants such as `new`, `test`, `final`, or `version-2`.

## Accessibility expectations

Accessibility is part of the component quality bar.

Prefer native HTML semantics over custom ARIA. Interactive controls should be keyboard operable, have visible focus states, and expose an understandable accessible name.

Use `aria-*` attributes when they add semantics that native HTML cannot provide. Do not add ARIA merely to make metadata or a validator look complete.

Animations should respect `prefers-reduced-motion` when motion conveys meaningful movement or transition effects.

## Responsive expectations

Components should remain usable across common mobile and desktop widths. Avoid fixed widths that cause horizontal overflow and make interactive targets difficult to use on touch screens.

A responsive component does not need to look identical at every viewport. It needs to preserve its hierarchy, readability, and usability.

## Design tokens

When a family uses shared design tokens, keep token definitions consistent within that family and avoid unnecessary duplication.

Tailwind's section-style component work has a dedicated token reference at:

```text
Tailwind/Components/STYLE_TOKENS.md
```

Do not silently introduce a second token vocabulary for an existing family unless there is a documented reason.

## Indexing model

`snippets-index.json` is generated from repository content and provides the global machine-readable index.

The index contains family and variant records, technology information, content types, paths, descriptions, tags, features, and aggregate statistics.

After adding, moving, renaming, or deleting content, regenerate it with:

```bash
python3 -m _gen.rebuild_index
```

Then validate the repository:

```bash
python3 scripts/validate.py
```

The validator checks architecture, metadata, index-to-disk consistency, stale paths, duplicate variant paths, and content coverage.

## Migration and refactoring rules

When moving existing content:

1. Preserve existing IDs unless there is a documented reason to change them.
2. Update metadata to match the new location and content type.
3. Regenerate the index.
4. Run validation.
5. Search for stale paths and references.
6. Update documentation and the changelog when the repository architecture changes.

Do not perform a large migration by changing folders alone. The index and metadata are part of the same data model.

## Why this structure exists

This model allows DevSnips to grow without turning every category into a large monolithic file. Each variant can eventually have its own website page, search result, metadata, preview, analytics, and canonical URL while families still provide useful organization for humans.
