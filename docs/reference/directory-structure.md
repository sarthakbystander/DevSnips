# Directory structure

The authoritative repository layout, with each path's role. Canonical vs generated is marked; see [Architecture](../introduction/architecture.md) for the reasoning.

```text
DevSnips/
├── library/                          CANONICAL — all UI resources
│   ├── React/
│   │   ├── Components/<Family>/<variant>/
│   │   ├── Sections/<Family>/<direction>/
│   │   ├── Templates/<template>/     (Vite/TS projects)
│   │   ├── DESIGN_TOKENS.md          token docs (non-resource)
│   │   └── index.html                gallery page (non-resource)
│   ├── Tailwind/
│   │   ├── Components/<Family>/<variant>/          (2-level; Buttons uses 3-level groups)
│   │   ├── Sections/<Category>/<style>/            (single-concept)
│   │   ├── Sections/<Category>/<section>/<style>/  (multi-concept)
│   │   ├── Templates/<template>/
│   │   ├── Components/STYLE_TOKENS.md
│   │   └── index.html
│   └── Vanilla/
│       ├── Components/<Family>/<variant>/          (incl. legacy Navigation sub-families)
│       ├── Sections/<Family>/<variant>/            (neo-brutalist sections)
│       ├── Templates/<template>/                   (code under pages/)
│       ├── Components/tokens.css + DESIGN_TOKENS.md
│       └── Sections/sections-index.html, sections-showcase.html
│
├── snippets-index.json               GENERATED — the machine-readable registry
├── index.html                        root tech landing page
│
├── cli/                              the npm package `devsnips`
│   ├── package.json                  name devsnips, bin → src/index.js, node >=18
│   ├── src/index.js                  entry + command dispatch
│   ├── src/commands/add.js           `add` implementation
│   ├── src/commands/init.js          `init` implementation
│   ├── src/registry/resolver.js      registry fetch + path resolution
│   ├── src/install/downloader.js     file selection + download
│   ├── src/install/writer.js         destination + safe writes
│   ├── src/devsnips/{config,agents,context}.js   project context
│   ├── src/utils/{paths,errors}.js   path safety + error formatting
│   └── test/*.test.js                node:assert suites (no framework)
│
├── agents/
│   ├── skills/devsnips/
│   │   ├── SKILL.md                  published agent skill (v1.0.1)
│   │   ├── references/               cli_reference.md, registry_schema.md,
│   │   │                             accessibility_responsive_checklist.md, schemas.md
│   │   └── eval-viewer/              eval tooling (generate_review.py, viewer.html)
│   └── resources/                    repository-side deep agent docs
│       ├── architecture.md, resources.md, cli.md, indexing.md,
│       ├── qa.md, workflows.md, conventions.md
│       ├── frameworks/{react,tailwind,vanilla}.md
│       └── indexes/*.json            GENERATED — specialized indexes
│
├── scripts/
│   ├── tooling/validators/           validate.py, deep_check.py
│   ├── tooling/indexing/             rebuild_index.py, build_resource_indexes.py,
│   │                                 validate_indexes.py, update_index.py (legacy)
│   ├── tooling/generators/           gen_site.py (website), Tailwind section builders
│   ├── tooling/utilities/            one-off migration/repair scripts
│   └── qa/resources/                 qa_vanilla.py + Playwright harnesses
│
├── website/                          GENERATED — published static site
│   ├── index.html                    home page
│   ├── <Tech>/<Type>/…/index.html    resource detail pages (mirrors)
│   ├── llms.txt · llms-full.txt      LLM-oriented inventory digests
│   ├── search-index.json             flat per-resource search records
│   ├── sitemap.xml · robots.txt      crawlability
│   └── docs/, cli/, contributing/ …  site documentation pages
│
├── docs/                             contributor + platform documentation (this tree)
│   └── …                             see docs/index.md for the map
│
├── devsnips/                         CLI init-output artifact in this checkout (config.json, AGENTS.md)
├── integrations/                     reserved, currently empty
├── reports/                          audit reports
└── .github/PULL_REQUEST_TEMPLATE.md  PR template (no CI workflows exist)
```

## Rules that follow from this layout

- Resource content exists **only** under `library/`. Tooling under `scripts/` must never be a resource; content must never live under `scripts/`.
- `cli/` is self-contained and must not depend on repository-relative paths.
- `website/**` paths are output, never resource locations. A resource's on-disk location is always `library/<registry path>`.
- Forbidden directory names under any technology: `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, `Tools/`.
- There is no root `package.json`; CLI commands run from `cli/` (or via `npx devsnips`).

## Addressing a resource

| Want | Use |
|---|---|
| Install | registry path: `npx devsnips add React/Components/Buttons/split-button` |
| Read on disk | `library/React/Components/Buttons/split-button/` |
| Registry entry | `snippets-index.json` → family `React/Components/Buttons/` → variant |
| Website page | `https://devsnips.dev/React/Components/Buttons/split-button/index.html` |
