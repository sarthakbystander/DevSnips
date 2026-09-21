# Tooling — overview

This page is the map of `scripts/tooling/`. Four families: **validators** (guardrails), **indexing** (the registry), **site generators** (the website), **utilities** (one-off migrations and quality fixes). For end-to-end procedures see [QA](../qa/overview.md); for the high-level registry pipeline see [Machine-readable overview](../machine-readable/overview.md).

Never hand-edit generated output: `snippets-index.json`, `agents/resources/indexes/*.json`, or `website/**`. Re-run the script that made it.

```text
scripts/tooling/
  validators/       guardrails that the library must clear
  indexing/         the machine-readable registry and the per-type indexes
  generators/       the static website (site generation + Tailwind section builders)
  utilities/        one-off migrations and automated quality-bar fixes
```

The canonical run order:

```text
  library/
    -> validators/validate.py           architecture, metadata, index<->disk
    -> indexing/rebuild_index.py        master registry
    -> indexing/build_resource_indexes.py per-type indexes
    -> indexing/validate_indexes.py      per-type indexes match
    -> generators/gen_site.py            website
    -> utilities/*.py                    migrations / quality fixes
```

| Family | What it guards / produces | Run when |
|---|---|---|
| **validators** | repository integrity: architecture, metadata, index<->disk consistency, template `AGENTS.md`, file-set sanctions, Vanilla quality bar | before every push (minimum: `validate.py`) |
| **indexing** | `snippets-index.json` + per-type indexes | leaves added/removed/renamed/moved; metadata changes |
| **site generators** | `website/` + search index, `llms.txt`, `llms-full.txt`, `sitemap.xml` | content/metadata changes that should appear on the site |
| **utilities** | deterministic migrations + quality fixes | when invited for a specific cleanup |

## Validators

Validators run as standalone scripts; no CI wraps them. The minimum bar before any push is `validate.py`; everything else is scope-dependent.

| Path | What it checks |
|---|---|
| `validators/validate.py` | architecture (only `Components`/`Sections`/`Templates` under each tech; no `Utilities`/`Resources`/`Snippets`/`Pages`/`Tools`), metadata validity (`type` present and matching its folder bucket; required files per tech), two-way index↔disk consistency, template `AGENTS.md` existence + non-empty, Vanilla quality bar (via `qa_vanilla.py`), duplicate IDs (collected as a NOTE, not a failure — deliberate) |
| `validators/deep_check.py` | per-tech required vs optional files: React Components need `code.tsx` + `preview.html` + `README.md`; React Sections need `code.tsx` + `preview.html`; a missing React `code.jsx` is a **warning** only; any Section with an empty `README.md` is a failure |

Key behavior:

- `validate.py` resolves the repo root from its own file location (CWD-independent), invokes `qa_vanilla.py` as a subprocess, and prints `VALIDATION PASSED` or `VALIDATION FAILED - N problem(s):` (exit 0 / 1).
- `deep_check.py` is **not** invoked by `validate.py`; run it alongside for file-set changes.

## Indexing

The indexing family produces the machine-readable registry and the three per-type specialized indexes — the spine of the system. See [Machine-readable overview](../machine-readable/overview.md) for the pipeline; this page is the script-level map.

| Path | Command | What it does |
|---|---|---|
| `indexing/rebuild_index.py` | `python scripts/tooling/indexing/rebuild_index.py` | re-scans disk, preserves curated family-level fields, cross-validates, recomputes stats, **refuses to write on mismatch** (prints `NOT writing index due to validation problems`) |
| `indexing/build_resource_indexes.py` | `python scripts/tooling/indexing/build_resource_indexes.py` | regenerates `components-index.json`, `sections-index.json`, `templates-index.json` from the same in-memory family set; only emits fields backed by real data |
| `indexing/validate_indexes.py` | `python scripts/tooling/indexing/validate_indexes.py` | fails loudly on schema/order/stale/missing-file/install-mirror count mismatches and JSON parse errors |

### How they relate

- `build_resource_indexes.py` **imports** `rebuild_index.py` for the scanner, curated-data preservation, and `validate()` — the filesystem scanner is never duplicated.
- `validate_indexes.py` **imports** `rebuild_index.py` for `disk_leaf_ids()` — so the validator can never drift from the generator's leaf-detection logic.
- `indexing/update_index.py` is **legacy / do not use** — it writes `library/`-prefixed paths and disagrees with the current format.

### The `files` manifest

`rebuild_index.py` builds each variant's `files` manifest from what is actually on disk: direct files (`code.html`, `code.tsx`, `metadata.json`, `preview.html`, `README.md`, `AGENTS.md`, …), plus `pages/*` (one level) for Tailwind/Vanilla templates, plus `src/*`, `components/*`, `data/*`, `sections/*`, `styles/*` (one level) for React templates. Files nested deeper than one level are **not** listed. This manifest is exactly what the CLI installs, so an incomplete manifest = incomplete install.

### Leaf detection

| Tech | What makes a leaf |
|---|---|
| Tailwind | `metadata.json` + no child `metadata.json` folder + both `code.html` **and** `preview.html` |
| React | `metadata.json` + no child `metadata.json` folder + (`code.tsx` **or** `preview.html`) |
| Vanilla | `metadata.json` + no child `metadata.json` folder |

The indexer is strict for Tailwind (both files) and loose for React (either file); the validators are stricter in the opposite direction so a variant missing one of the pair is flagged by the required-files check rather than reclassified as a non-leaf.

## Site generators

The site-generator family emits the static `website/`. It is fully self-contained Python (no Node, no build step for the generator itself).

| Path | Role |
|---|---|
| `generators/gen_site.py` | main site generator — walks `library/Tailwind/`, `library/Vanilla/`, `library/React/` (Components/Sections/Templates), reads each item's `metadata.json` + `README.md`, emits a fully cross-linked static site into `website/` |
| `generators/generate.py` | Tailwind **section** builder — writes all 165 Tailwind/Sections section folders (`code.html`, `preview.html`, `metadata.json`, `README.md`), one of 15 styles per category |
| `generators/styles.py` | the 15 style systems (tokens, fonts, helper classes, dark-mode membership) used by the section builders |
| `generators/layout.py` + `helpers.py` | shared layout helpers: containers, navbar/footer, logo/svg handling |
| `generators/builders_*.py` (11 files) | per-category section builders: testimonials, faq, contact, footer, navbar, stats, team, blog, logos, newsletter, 404 |

### What `gen_site.py` emits

Per resource: a detail page (preview + code + metadata + features + related + docs); templates get a multi-page-aware detail page. Cross-cutting: technology hub pages, category index pages (Components/Sections/Templates per tech), family group pages, a home page, a documentation hub, and shared navbar/footer on every page. It also emits the index surfaces — `website/search-index.json`, `llms.txt`, `llms-full.txt`, `sitemap.xml` — and brand assets (`assets/style.css`, `assets/logo.svg`). All internal links are relative; "Preview" opens the real `preview.html` (or `index.html` for templates) in a new tab.

Regenerate after any content/metadata change that should appear on the site:

```bash
python scripts/tooling/generators/gen_site.py
```

The website is a **derived output** — never hand-edit `website/` mirrors; see [Architecture](../introduction/architecture.md).

## Utilities

Utilities are deterministic, re-runnable migration/quality-fix scripts. They write files — run them deliberately, then follow with `rebuild_index.py` + `validate.py` (and `validate_indexes.py` if the index changed).

| Path | What it fixes |
|---|---|
| `utilities/fix_duplicate_ids.py` | family-namespaces colliding IDs: `<slug>-NNN` → `<family>-<slug>-NNN`. Non-colliding IDs are left untouched (preserve stable IDs). Run before `rebuild_index.py` when duplicates are reported. |
| `utilities/fix_quality_bar.py` | Injects the two universally-safe Vanilla quality fixes: a `prefers-reduced-motion` guard when a component animates without one, and a `:focus-visible` ring when absent. Idempotent (marker-guarded). `DRY_RUN=1` to preview. |
| `utilities/fix_self_contained_css.py` | Copies a Tailwind section's `preview.html` `<style>` helper CSS into its `code.html` so the snippet is self-contained. Idempotent (marker-guarded); does not touch `preview.html`. |
| `utilities/migrate_tokens.py` | Replaces hardcoded values in legacy Vanilla component HTML with `var(--ds-*, <original>)` so they render identically until `tokens.css` is themed. `DRY_RUN=1` to report. |
| `utilities/migrate_vanilla.py` | Phase-0 Vanilla migration: resolves collision pairs, renames `snippet-NN-<name>` folders to clean names, flattens `Forms/<Subfamily>/<variant>/`, unifies legacy `metadata.json` to the rich schema with honestly-derived `responsive`/`darkMode`/`accessibility`. |

Shared conventions: all resolve the repo root relative to their own file (CWD-independent); all are deterministic/re-runnable; all print what they did on stdout; all should be followed by `rebuild_index.py` (then `validate_indexes.py`) and `validate.py`.

## When to run which

| Situation | Run |
|---|---|
| Before every push | `validators/validate.py` |
| File-set changes (missing README, etc.) | `deep_check.py` |
| New/removed/renamed leaf or metadata change | `rebuild_index.py` → `validate_indexes.py` → (optionally) `gen_site.py` |
| Duplicate IDs reported | `fix_duplicate_ids.py` → `rebuild_index.py` → `validate_indexes.py` → `validate.py` |
| Vanilla quality-bar failures | `fix_quality_bar.py` (DRY_RUN first) → re-run `qa_vanilla.py` → `validate.py` |
| Site needs to reflect content changes | `gen_site.py` |

## Go deeper

This page is the human-facing tooling map. The implementation-anchored per-script reference (exact check functions, the full leaf-detection contract, the 15-style system) is maintained for agents in the scripts themselves and `agents/resources/workflows.md`.
