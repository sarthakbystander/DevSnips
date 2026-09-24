# DevSnips — Repository Architecture

Scope: how the repository is laid out, which files are canonical vs generated, and which
subsystem owns which responsibility. This file is the map; the other `agents/resources/*.md`
files are the detail.

## Source-of-truth hierarchy

1. **`snippets-index.json`** (repo root) — the live machine-readable registry. Paths in it are
   **tech-first** (`Tailwind/Components/Buttons/basic-button/primary/`), i.e. without the
   `library/` prefix that exists on disk.
2. **The filesystem under `library/`** — authoritative for which files actually exist and
   what they contain.
3. **Everything else** (`README.md`, root `AGENTS.md`, `CHANGELOG.md`, `docs/*`) — secondary
   context that may be stale. Several of these still describe a pre-`library/` layout; see
   "Known stale references" below.

Never quote inventory counts (`totalFamilies`, `totalVariants`, `stats.*`) from documentation.
Read them from the current `snippets-index.json`.

## Top-level map

| Path | Role |
|---|---|
| `library/` | Canonical UI resources (the product). |
| `snippets-index.json` | Generated registry of every resource. |
| `cli/` | Published npm CLI (`devsnips`) that installs resources into a user project. |
| `agents/` | Agent-facing layer: skills (`agents/skills/devsnips/`) and this resource doc set. |
| `scripts/` | Repository tooling: validators, indexing, generators, utilities, QA harnesses. |
| `docs/` | Contributor + platform documentation (start at `docs/index.md`). |
| `integrations/mcp/` | Read-only MCP server (`devsnips-mcp`) exposing the library to AI agents; see `agents/resources/mcp.md`. |
| `reports/` | Engineering audits and investigations. |
| `.github/workflows/` | CI — runs the validators and the CLI tests on every push and pull request. |
| `index.html` | Root tech landing page; links into `library/`. |

Two paths are generated and uncommitted rather than checked in: `website/` (the
derived static site) is produced by `scripts/tooling/generators/gen_site.py`, and
`devsnips/` is created in a *user* project by `npx devsnips init`. Neither exists
in a clean checkout.

## `library/`

Canonical resource collection. Every technology has the same three content types.

Location: `library/`

Structure:

```text
library/<Technology>/<Components|Sections|Templates>/...
  Technology ∈ {React, Tailwind, Vanilla}
```

Enforcing code:

- `scripts/tooling/validators/validate.py` — `ALLOWED_DIRS` restricts each tech dir to
  `{Components, Sections, Templates}` and rejects `Utilities/`, `Resources/`, `Snippets/`,
  `Pages/`, `Tools/` anywhere under a tech.
- `scripts/tooling/indexing/rebuild_index.py` — `TAILWIND_TREES` / `VANILLA_TREES` /
  `REACT_TREES` define the three trees per tech; `is_leaf()` decides what counts as a resource.

Design-token references that live inside `library/`:

- `library/React/DESIGN_TOKENS.md`
- `library/React/Sections/DESIGN_TOKENS.md`
- `library/Tailwind/Components/STYLE_TOKENS.md`
- `library/Vanilla/Components/DESIGN_TOKENS.md`
- `library/Vanilla/Templates/design-tokens.md`

Browse pages that also live under `library/`:

- `library/Tailwind/index.html`, `library/React/index.html`
- `library/Vanilla/Sections/sections-index.html`, `library/Vanilla/Sections/sections-showcase.html`

For the resource model itself see `agents/resources/resources.md`.

## `cli/`

Node.js CLI published to npm as `devsnips` (see `cli/package.json`; the version lives there).

Location: `cli/` — entry point `cli/src/index.js`, tests `cli/test/*.test.js`.

It never reads the local `library/` tree. It resolves a path against the **remote**
`snippets-index.json` on GitHub `main` and downloads files from `raw.githubusercontent.com`
(`cli/src/registry/resolver.js`, `cli/src/install/downloader.js`).
## `scripts/`

| Path | Role |
|---|---|
| `scripts/tooling/validators/validate.py` | The repository gate: architecture, metadata, index↔disk, template `AGENTS.md`, plus the Vanilla quality bar. |
| `scripts/tooling/validators/deep_check.py` | Per-tech required-file-set checker; the detailed file-set rules behind `validate.py`. |
| `scripts/tooling/indexing/rebuild_index.py` | Authoritative regenerator for `snippets-index.json`. |
| `scripts/tooling/generators/` | Section generators (`generate.py`, `gen_site.py`, `builders_*.py`, `styles.py`) and README generators. |
| `scripts/tooling/utilities/` | One-off migration/repair scripts (`migrate_tokens.py`, `fix_quality_bar.py`, …). |
| `scripts/qa/resources/qa_vanilla.py` | Vanilla quality-bar + token-conformance scanner. |
| `scripts/qa/resources/_qa_react_*.py` | Per-family Playwright harnesses. |
| `scripts/qa/resources/_qa_template.py` | Vanilla template overflow/interaction harness. |
| `scripts/qa/resources/test_tailwind_nav.py`, `test_react_nav.py` | Nav/index page harnesses. |

**There is no test runner or `package.json` at the repository root.** Python files under
`scripts/` are plain scripts; the only `package.json` is `cli/package.json`. CI is driven by
`.github/workflows/ci.yml`, which invokes those scripts plus `npm test` in `cli/`.

See `agents/resources/qa.md` and `agents/resources/indexing.md`.

## `website/` (generated, not committed)

The published static site, produced by `scripts/tooling/generators/gen_site.py`. It is a
**derived publishing artifact** and is not present in a clean checkout.

- Pages: `website/index.html`, `website/docs/index.html`, `website/docs/cli/index.html`, …
- Resource mirrors: `website/<React|Tailwind|Vanilla>/<Components|Sections|Templates>/...`
- Machine-readable: `website/llms.txt`, `website/llms-full.txt`, `website/search-index.json`

Do not treat `website/...` paths as resource locations — the canonical resource is always
under `library/`. Regenerate; never hand-edit.

## `agents/`

| Path | Role |
|---|---|
| `agents/skills/devsnips/SKILL.md` | The agent skill: discover, install, adapt, verify DevSnips resources. |
| `agents/skills/devsnips/references/` | `cli_reference.md`, `registry_schema.md`, `accessibility_responsive_checklist.md`. |
| `agents/resources/` | **This doc set** — repository-side (maintainer/agent) resource documentation. |

Relationship: `SKILL.md` documents *consuming* DevSnips (find → install → integrate).
`agents/resources/` documents *the repository itself* (where things live, what is enforced,
what to run). Do not duplicate consume-side guidance here.

## Data flow

```text
library/**                    canonical files authored/edited by contributors
   |
   |  scripts/tooling/indexing/rebuild_index.py     (scans disk, preserves curated fields)
   v
snippets-index.json           generated registry, tech-first paths
   |
   +--> scripts/tooling/validators/validate.py       requires index <-> disk agreement
   +--> cli/src/registry/resolver.js                 fetches it from GitHub main
   +--> website/ (generated by gen_site.py: llms.txt, search-index.json, mirrors)
```

Templates carry their own per-template `AGENTS.md` (see `resources.md`) — a *resource-level*
file, distinct from the root `AGENTS.md` and from `agents/resources/`.

## Boundaries

- **`library/` is content.** Do not put tooling there (only token/README/gallery docs).
- **`scripts/` is tooling.** Tooling must not be a resource; content must not live under `scripts/`.
- **`cli/` is distribution.** It is a self-contained npm package (`cli/package.json` `files`)
  and must not depend on repository-relative paths.
- **`website/` is output.** Regenerate; don't hand-edit resource mirrors.
- **CI enforces the validators.** `.github/workflows/ci.yml` runs `validate.py`,
  the Python tooling unit tests, `rebuild_index.py --check`, `validate_indexes.py`, the
  Markdown/agent-doc link and path checks, and `cli` `npm test` on every push and pull
  request. The process artifacts remain
  `docs/PULL_REQUEST_TEMPLATE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.

## Known gaps

This section is currently empty: the previously tracked items — the root `README.md` links,
the root `AGENTS.md` layout, the `docs/` validator commands, the QA harnesses' static-server
convention, the absence of CI, the legacy `update_index.py`, the unscoped duplicate-ID policy,
and the orphaned eval-tooling references — have all been resolved.

## Deeper reading

- Resources: `agents/resources/resources.md` · Frameworks: `agents/resources/frameworks/react.md`, `tailwind.md`, `vanilla.md`
- CLI: `agents/resources/cli.md` · Indexing: `agents/resources/indexing.md` · QA: `agents/resources/qa.md`
- Workflows: `agents/resources/workflows.md` · Conventions: `agents/resources/conventions.md`
