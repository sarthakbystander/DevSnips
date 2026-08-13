# DevSnips

**DevSnips is an open-source frontend UI library of reusable components, page sections, and templates.**

The repository is organized for two things: making individual UI pieces easy to discover and keeping the source library maintainable as it grows.

## What is in the repository?

DevSnips currently contains **89 families and 852 indexed variants** across Tailwind CSS and Vanilla HTML/CSS/JS. The index is generated from the repository filesystem and is intended to stay in sync with the source content.

| Technology | Components | Sections | Templates | Total |
|---|---:|---:|---:|---:|
| Tailwind CSS | 321 | 201 | 9 | 531 |
| Vanilla HTML/CSS/JS | 297 | — | 24 | 321 |
| **Total** | **618** | **201** | **33** | **852** |

React directories exist as reserved structure for future content and are not included in the current index totals.

## Repository structure

```text
DevSnips/
├── Tailwind/
│   ├── Components/       # focused, reusable UI building blocks
│   ├── Sections/         # larger page-section compositions
│   └── Templates/        # complete page/site experiences
├── Vanilla/
│   ├── Components/       # reusable HTML/CSS/JS components
│   └── Templates/        # complete page/site experiences
├── React/
│   ├── Components/       # reserved for future React content
│   └── Templates/        # reserved for future React content
├── _gen/                 # generation and index tooling
├── scripts/              # validation and quality checks
├── snippets-index.json   # generated global content index
├── COMPONENT_STRUCTURE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

There are no standalone `Utilities/`, `Resources/`, or `Snippets/` content collections. Content belongs to a technology and an explicit content type.

## Content types

Tailwind has three first-class content types:

- **Components**: one focused interface pattern such as a button, card, modal, table, or accordion.
- **Sections**: larger compositions such as heroes, pricing sections, testimonials, FAQs, and footers.
- **Templates**: complete pages or substantial page experiences such as SaaS, agency, conference, or store sites.

Vanilla currently uses `Components/` and `Templates/`. Former standalone Vanilla sections were consolidated into Components.

Every indexed Tailwind variant has a `type` value of `component`, `section`, or `template` in its metadata and index entry.

## Tailwind CSS

### Components

321 variants across 13 families:

| Family | Variants |
|---|---:|
| Accordions | 15 |
| Buttons | 54 |
| Cards | 40 |
| Dropdowns | 30 |
| Input | 49 |
| Modals | 30 |
| Navbar | 15 |
| Navigation | 35 |
| Progress | 6 |
| Tables | 20 |
| Tabs | 15 |
| Toasts | 6 |
| Tooltips | 6 |

### Sections

201 variants across 16 families. The collection includes common marketing and product sections such as Hero, Pricing, Testimonials, FAQ, Logos, Stats, Team, Footer, SaaS sections, AI product sections, developer sections, app UI, and premium visual sections.

### Templates

9 templates:

- `ai-saas-platform`
- `baseline-conference`
- `devsnips-store`
- `northline-atelier`
- `krat-adventure`
- `meridian`
- `stratum`
- `vesper`
- `quiet-place`

See `Tailwind/Components/STYLE_TOKENS.md` for the shared style-token reference used by the section-style component work.

## Vanilla HTML/CSS/JS

Vanilla contains 297 component variants across 34 families plus 24 templates.

The component library includes common UI families such as Buttons, Cards, Forms, Navigation, Modals, Media, Marketing, Tables, Tabs, Accordions, Loaders, Hero, Pricing, Testimonials, and more.

Former Neo-Brutalist Vanilla sections live under `Vanilla/Components/` rather than a separate Sections collection.

## How an individual entry is organized

A Tailwind component or section normally looks like this:

```text
Tailwind/Components/<family>/<variant>/
├── code.html
├── preview.html
└── metadata.json
```

`code.html` is the copy-paste version. `preview.html` is the standalone visual preview. `metadata.json` provides structured information used by indexing, search, and the site.

Templates may use a larger internal structure because they represent complete page experiences.

Vanilla entries use their own documented file convention. See `COMPONENT_STRUCTURE.md` for the full specification.

## Using DevSnips

You can browse the repository directly, copy an individual snippet, or consume the generated `snippets-index.json` for tooling and site generation.

For Tailwind variants, copy the contents of `code.html` into a Tailwind project. `preview.html` is intended for viewing the component in context and may include CDN or demo-specific setup that should not be copied into production blindly.

## Validation and indexing

The repository includes automated checks for architecture, metadata, index consistency, stale paths, duplicate variant paths, and content coverage.

Run the main validation command from the repository root:

```bash
python3 scripts/validate.py
```

Regenerate the global index from the filesystem with:

```bash
python3 -m _gen.rebuild_index
```

If you change content, regenerate the index and run validation before opening a pull request.

## Contributing

Contributions are welcome. New entries should be focused, accessible, responsive, documented through metadata, and placed in the correct technology/content-type directory.

Read `CONTRIBUTING.md` before creating a new component or template.

## Documentation

- `CONTRIBUTING.md` — contribution workflow, quality expectations, and checklist.
- `COMPONENT_STRUCTURE.md` — repository architecture, naming rules, file conventions, and metadata model.
- `CHANGELOG.md` — chronological record of repository changes.
- `PULL_REQUEST_TEMPLATE.md` — pull request review checklist.
- `AGENTS.md` — repository guidance for automated coding agents and maintainers.

## License

See `LICENSE` for the project's license terms.
