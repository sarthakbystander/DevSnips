# Contributing — overview

This section is the end-to-end contributor guide for adding UI resources to DevSnips. The maintainer-facing specs (`docs/CONTRIBUTING.md`, `docs/COMPONENT_STRUCTURE.md`) remain authoritative for detail; these pages organize the same rules around the full workflow and explain the reasoning.

## The contribution pipeline

```text
Idea
 ↓
Classify            component / section / template — and which technology
 ↓
Correct structure   folder + required files per tech + type
 ↓
Implementation      code.* (production-ready, self-contained)
 ↓
Metadata            metadata.json copied from a sibling schema
 ↓
Preview             preview.html (required by contract; Vanilla components excluded)
 ↓
Agent context       AGENTS.md for templates; README.md per contract
 ↓
Validation          regenerate registry → validators → QA
 ↓
Pull request        report the validation commands run
```

## Before you start

1. Read [Resource structure](../resources/resource-structure.md) — the file contract is the rule you cannot negotiate.
2. Read [Metadata](../machine-readable/metadata.md) — copy the sibling schema; never invent keys.
3. Pick the family you are joining and inspect a sibling leaf end to end (files, metadata, README style, code conventions). The sibling is the house style.

## The non-negotiables

- **Correct technology + type directory.** `library/<Tech>/<Type>/...`. Never create `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` under a technology — validators reject them.
- **Exact file contract** for the tech + type (see [Creating resources](creating-resources.md)).
- **Honest metadata.** Never claim behavior the implementation does not provide.
- **Stable identity.** Kebab-case folder name; never rename existing resources to "improve" naming; never reuse an existing ID.
- **Accessibility and responsiveness.** Keyboard operability, visible focus, reduced-motion support, no horizontal overflow at mobile widths.
- **Generated files are never hand-edited.** After content changes, regenerate `snippets-index.json`; never patch it.
- **Run the validators** and report the exact commands and results in the pull request.

## Pages in this section

| Page | Content |
|---|---|
| [Creating resources](creating-resources.md) | The step-by-step procedure per resource type, with naming rules. |
| [Metadata](metadata.md) | How to author `metadata.json` for a new resource. |
| [Agent files](agent-files.md) | `AGENTS.md` files — which ones exist, what goes in them. |
| [Validation](validation.md) | What to run, expected output, common failures, how to fix them. |

## Git and pull requests

```bash
git checkout -b feat/your-component
git add .
git commit -m "feat: add your component"
```

- Branch names are prefixed (`feat/…`, `chore/…`); commit messages use conventional prefixes (`feat:`, `chore:`).
- Keep commits focused — do not mix a repository-wide refactor into a resource contribution.
- Pull requests use `.github/PULL_REQUEST_TEMPLATE.md` / `docs/PULL_REQUEST_TEMPLATE.md` and must report the validation commands run and their observed results, plus any known limitations.
- CI runs the static gates (validator, index drift, index validation, doc links, CLI tests) on every push and pull request. Run them locally first; a PR with stale registry output will fail CI.

## When in doubt

Prefer the smallest change that preserves the repository's existing architecture and makes the content easier to discover, reuse, and maintain. If a validator exposes a pre-existing issue your change does not introduce, mention it in the PR rather than silently changing unrelated content.
