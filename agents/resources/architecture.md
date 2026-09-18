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
| `website/` | Published static site — a *derived* copy of the resource tree. |
| `docs/` | Contributor-facing specs (`COMPONENT_STRUCTURE.md`, `CONTRIBUTING.md`). |
| `integrations/mcp/` | Reserved; currently empty. |
| `.github/` | Only `PULL_REQUEST_TEMPLATE.md`. **There is no CI workflow in this repository.** |
| `devsnips/` | CLI `init` output artifact (`AGENTS.md` + `config.json`); untracked. |
| `index.html` | Root tech landing page; links into `library/`. |
| `fix_validate.py` | Untracked one-off migration patch script at the repo root. |

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
| `scripts/tooling/indexing/update_index.py` | Legacy generator for the Tailwind 15-style section families; see "Known stale references". |
| `scripts/tooling/generators/` | Section generators (`generate.py`, `gen_site.py`, `builders_*.py`, `styles.py`) and README generators. |
| `scripts/tooling/utilities/` | One-off migration/repair scripts (`migrate_tokens.py`, `fix_quality_bar.py`, …). |
| `scripts/qa/resources/qa_vanilla.py` | Vanilla quality-bar + token-conformance scanner. |
| `scripts/qa/resources/_qa_react_*.py` | Per-family Playwright harnesses. |
| `scripts/qa/resources/_qa_template.py` | Vanilla template overflow/interaction harness. |
| `scripts/qa/resources/test_tailwind_nav.py`, `test_react_nav.py` | Nav/index page harnesses. |

**No test runner, CI, or `package.json` exists at the repository root.** Python files under
`scripts/` are plain scripts; the only `package.json` is `cli/package.json`.

See `agents/resources/qa.md` and `agents/resources/indexing.md`.

## `website/`

The published static site. It mirrors the resource tree for rendering.

- Pages: `website/index.html`, `website/docs/index.html`, `website/docs/cli/index.html`,
  `website/docs/agents/index.html`, `website/docs/structure/index.html`, …
- Resource mirrors: `website/<React|Tailwind|Vanilla>/<Components|Sections|Templates>/...`
- Machine-readable: `website/llms.txt`, `website/llms-full.txt`, `website/search-index.json`
- `website/assets/style.css`, `website/robots.txt`, `website/sitemap.xml`

`website/` is a **derived publishing artifact**, not the canonical source. Do not treat
`website/...` paths as resource locations — the canonical resource is always under `library/`.

## `agents/`

| Path | Role |
|---|---|
| `agents/skills/devsnips/SKILL.md` | The agent skill: discover, install, adapt, verify DevSnips resources. |
| `agents/skills/devsnips/references/` | `cli_reference.md`, `registry_schema.md`, `accessibility_responsive_checklist.md`, `schemas.md`. |
| `agents/skills/devsnips/eval-viewer/` | Eval viewer tooling (`generate_review.py`, `viewer.html`). |
| `agents/resources/` | **This doc set** — repository-side (maintainer/agent) resource documentation. |
| `agents/examples/`, `agents/prompts/`, `agents/providers/` | Present but currently empty. |

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
   +--> website/ (llms.txt, search-index.json, mirrors)
```

Templates carry their own per-template `AGENTS.md` (see `resources.md`) — a *resource-level*
file, distinct from the root `AGENTS.md` and from `agents/resources/`.

## Boundaries

- **`library/` is content.** Do not put tooling there (only token/README/gallery docs).
- **`scripts/` is tooling.** Tooling must not be a resource; content must not live under `scripts/`.
- **`cli/` is distribution.** It is a self-contained npm package (`cli/package.json` `files`)
  and must not depend on repository-relative paths.
- **`website/` is output.** Regenerate; don't hand-edit resource mirrors.
- **No CI.** Validation is enforced only when a human/agent runs it manually; the process
  artifacts are `docs/PULL_REQUEST_TEMPLATE.md` and `.github/PULL_REQUEST_TEMPLATE.md`.

## Known stale references (documented, deliberately not silently changed)

1. Root `README.md` links `Tailwind/Templates/…`, `React/index.html`, `Tailwind/index.html`,
   and `Vanilla/Templates/SaaS%20Dashboard/` — none exist at those paths.
2. `scripts/tooling/indexing/update_index.py` writes `library/`-prefixed paths and uses
   package-relative imports, so it disagrees with the current index format produced by
   `rebuild_index.py`. Treat it as legacy.
3. `scripts/tooling/validators/validate.py`'s duplicate-ID check only prints a NOTE for
   pre-existing duplicates; it does not fail the run.
4. `agents/skills/devsnips/references/schemas.md` references eval files (`scripts/run_eval.py`,
   `agents/analyzer.md`, `agents/grader.md`, …) that do not exist in this repository.

(The former items about the root `AGENTS.md` layout, the `docs/` validator commands, and the
QA harnesses' static-server convention were resolved and removed from this list.)

## Deeper reading

- Resources: `agents/resources/resources.md` · Frameworks: `agents/resources/frameworks/react.md`, `tailwind.md`, `vanilla.md`
- CLI: `agents/resources/cli.md` · Indexing: `agents/resources/indexing.md` · QA: `agents/resources/qa.md`
- Workflows: `agents/resources/workflows.md` · Conventions: `agents/resources/conventions.md`
