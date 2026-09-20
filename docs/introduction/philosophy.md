# Philosophy

DevSnips' architecture follows from a small set of principles. Each principle below is implemented in the repository; the mechanism is named so the principle can be verified rather than taken on faith.

## 1. Agent-first, human-compatible

AI coding agents are the primary consumers. Every operation an agent needs — discovery, evaluation, installation, verification — has a non-interactive, machine-readable interface:

- Discovery reads JSON (`snippets-index.json`, the specialized indexes, `search-index.json`).
- Installation runs one command (`npx devsnips add <path>`) with no prompts.
- Verification is file-based: expected paths, expected files, expected content.

This does not exclude humans. `code.html` and `code.tsx` are readable and copy-paste ready, and the website renders the same registry for browsing. But whenever a design decision trades interactive convenience against predictability, predictability wins. The CLI deliberately has no interactive prompts, no wizards, and no flags that change behavior silently.

## 2. Structured resources with a fixed file contract

A resource is a folder whose required files are determined by its technology and type, and enforced by validators (`scripts/tooling/validators/validate.py`, `scripts/tooling/validators/deep_check.py`). The contract is small and stable:

- Implementation file(s): `code.html`, or `code.tsx` (+ `code.jsx` parity for React components).
- `preview.html` — a runnable demonstration; never installed.
- `metadata.json` — required on every leaf; the registry input.
- `README.md` — variant documentation (required for component variants and templates).
- `AGENTS.md` — required for every template.

A fixed contract is what makes everything else possible: the indexer can build a complete file manifest, the CLI can decide exactly what to install, and an agent can know what it will find inside an installed folder without opening it first.

## 3. Explicit metadata over inferred behavior

Metadata is infrastructure, not decoration. `metadata.json` records what the implementation actually provides — `responsive`, `darkMode`, `accessibility`, `dependencies`, `features` — and contributors are required not to claim behavior the code does not implement. Downstream consumers (index, website, agents) treat metadata as the description of record.

One deliberate consequence: metadata schemas are **per-technology, not universal**. Each technology's records follow the shape of its siblings, reflecting how the collection evolved, and the indexer tolerates field differences across technologies. Do not invent keys; copy a sibling's shape.

## 4. One canonical identity per resource

A resource's identity is its filesystem path relative to its technology — the **registry path**, e.g. `React/Components/Buttons/solid-button`. Three address forms describe the same resource, and the mapping between them is deterministic:

- **Registry path** (tech-first, used by the CLI and every index): `React/Components/Buttons/solid-button/`
- **Filesystem path** (on disk): `library/React/Components/Buttons/solid-button/`
- **Family + variant** (inside the registry): tech `React` → category `Components` → family `Buttons` → variant `solid-button`

The folder name is the canonical slug. `slug`, `name`, and `id` in `metadata.json` are descriptive; the path is authoritative. This is why renaming or moving a resource is a structural event that requires regenerating the registry and checking every consumer, and why IDs must stay stable once published.

## 5. A single machine-readable registry

Every queryable fact about the inventory lives in `snippets-index.json`. It is generated from the filesystem by `scripts/tooling/indexing/rebuild_index.py` and is the single object that the CLI, the website, the validators, and the specialized indexes all derive from. One registry means one place to update and one place to trust — and one place that can drift, which is why a two-way index↔disk consistency check runs in the primary validator.

Counts in the registry are recomputed on every regeneration. Documentation is deliberately forbidden from quoting inventory counts because they drift; read them from the current registry.

## 6. Generated artifacts are never hand-edited

`snippets-index.json`, `agents/resources/indexes/*.json`, and the `website/` mirrors are generated. Hand-editing them creates a second source of truth. The generators preserve curated fields (family descriptions, tags, search terms) across regenerations, so there is no reason to patch the output. Regeneration is also defensive: `rebuild_index.py` refuses to write when its cross-validation finds disk↔index disagreement, so a broken state is reported rather than committed.

## 7. Compatibility over cleverness

Resources favor what works without a build step or lock-in:

- **Vanilla** components are self-contained HTML fragments with inline CSS/JS, referencing `--ds-*` design tokens *with fallbacks* so they render correctly standalone and re-theme together when the shared token sheet (`library/Vanilla/Components/tokens.css`) is present.
- **Tailwind** `code.html` files are copy-paste snippets with no `<html>`, no `<!DOCTYPE>`, and no CDN script — they drop into any page that already loads Tailwind.
- **React** components are TypeScript-first with a JavaScript parity build; templates are complete Vite projects, but templates are not required for everyday use.

Conventional dependencies are limited to Tailwind (via CDN), Google Fonts, and Pico CSS, plus the React template toolchain (React, React Router, Framer Motion). Adding new runtime dependencies to the ecosystem is out of convention.

## 8. Accessibility and responsiveness are the quality bar, not metadata fields

Keyboard operability, visible focus, reduced-motion support, native semantics first (ARIA only to supplement), and no horizontal overflow at mobile widths are enforced by convention and — for Vanilla components — by a machine-checked quality bar (`scripts/qa/resources/qa_vanilla.py`). "Responsive" means usable at mobile widths, not pixel-identical across breakpoints.

## 9. The host project keeps its architecture

An installed resource is a starting point, not a framework. The CLI writes only into `./devsnips/` and never touches the rest of the project; adaptation guidance (in the skill and in the generated project `AGENTS.md`) instructs agents to adapt the resource to the project's existing patterns rather than restructure the project around the resource. Reusing the project's existing tokens, utilities, and components takes precedence over preserving the resource's exact styling.

## 10. Report what happened, not what should have happened

Verification rules apply to the tooling as much as to agents: the CLI exits non-zero with a specific error class on failure and records an installation only after files are on disk; the index generator refuses to write on validation failure; the validator exits non-zero with per-path messages. Agents consuming DevSnips are held to the same contract — an install may not be reported as successful until the destination directory and files have been confirmed.

