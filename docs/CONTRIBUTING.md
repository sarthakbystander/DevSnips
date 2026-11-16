# Contributing to DevSnips

Thanks for contributing to DevSnips. The goal is to keep the library useful at scale, so contributions should be easy to discover, copy, review, and maintain.

This file is the authoritative summary of the contributor rules. The step-by-step walkthrough of the same rules, organized around the full workflow, lives in [`docs/contributing/`](contributing/overview.md); naming conventions are specified in [`docs/reference/conventions.md`](reference/conventions.md). Do not duplicate their detail here — link to it.

## Before you start

Read these files first:

- `README.md` for the current repository structure and content counts.
- `COMPONENT_STRUCTURE.md` for folder, file, metadata, and naming rules.
- `AGENTS.md` for repository-specific automation and maintainer guidance.
- [`docs/contributing/overview.md`](contributing/overview.md) for the end-to-end contribution pipeline.

Do not edit `snippets-index.json` by hand unless a maintainer specifically asks you to. It is generated from repository content.

## Where content belongs

Use the technology and content type that matches what you are adding:

```text
Tailwind/
├── Components/<family>/<variant>/
├── Sections/<family>/<variant>/
└── Templates/<template>/

Vanilla/
├── Components/<family>/<variant>/
└── Templates/<template>/

React/
├── Components/<family>/<variant>/
├── Sections/<family>/<variant>/
└── Templates/<template>/
```

Do not create standalone `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` collections.

## Choosing a content type

Use a **component** when the contribution represents one focused UI pattern.

Use a **section** when it is a larger composition that normally occupies part of a page, such as a hero, pricing area, testimonial block, or footer. Tailwind sections belong in `Tailwind/Sections/`.

Use a **template** when the contribution represents a complete page or substantial page experience. Templates may contain multiple pages and supporting files.

## Structure requirements (summary)

The exact per-technology file contract is specified in [`agents/resources/resources.md`](../agents/resources/resources.md) §4 and walked through step by step in [`docs/contributing/creating-resources.md`](contributing/creating-resources.md). The invariants:

- Each variant follows its technology's required file set (Tailwind components: `code.html`, `preview.html`, `metadata.json`, `README.md`; Vanilla components: a single self-contained `code.html`; templates always include an `AGENTS.md` at the template root).
- `code.html` / `code.tsx` is the focused copy-paste implementation — demo-only wrappers and unrelated page content stay out of it.
- `preview.html` is a complete standalone demonstration and may contain CDN setup, demo data, and page framing.
- `metadata.json` `type` must agree with the directory it lives in (`component` / `section` / `template`).
- Templates must carry an `AGENTS.md` explaining structure, design system, safe modification guidance, and the quality bar. Both `validate.py` and `rebuild_index.py` enforce this.

## Quality requirements

Every contribution should aim for production-ready output, not merely a visual screenshot.

Use semantic HTML where appropriate. Interactive controls should be keyboard accessible and have visible focus states. Use ARIA only when native HTML semantics are insufficient.

Respect reduced-motion preferences for meaningful animations. Avoid unnecessary JavaScript and external dependencies. Keep third-party dependencies explicit and minimal.

Components should work at common viewport sizes without horizontal overflow. Text should remain readable and controls should remain usable on touch devices.

Keep code focused. A component should demonstrate one clear pattern instead of becoming a miniature application unless it is intentionally a template or section.

## Naming and metadata (summary)

Naming rules live in [`docs/reference/conventions.md`](reference/conventions.md); the metadata procedure and its tooling-enforced rules live in [`docs/contributing/metadata.md`](contributing/metadata.md). The invariants:

- Kebab-case for filesystem slugs; readable Title Case for display names in metadata.
- Keep IDs stable. Do not change an existing ID merely to make it look nicer. New content should use a unique ID that will not collide with another entry.
- Metadata is part of the library's infrastructure, not decoration. Keep names, descriptions, categories, tags, search terms, and related entries accurate.
- Do not claim accessibility, responsiveness, browser support, or features that the implementation does not actually provide.
- When adding a new family, make sure the family and its variants can be represented cleanly in `snippets-index.json`.

## Index and validation

After adding, moving, renaming, or deleting content, regenerate the index:

```bash
python scripts/tooling/indexing/rebuild_index.py
```

Then run:

```bash
python scripts/tooling/validators/validate.py
```

Do not submit a pull request with a stale index or broken validation output. The full command matrix, layer-by-layer checks, and common failure classes are in [`docs/contributing/validation.md`](contributing/validation.md).

If a validator exposes a pre-existing issue that your change does not introduce, mention it clearly in the pull request instead of silently changing unrelated content.

## Git workflow

A typical contribution looks like:

```bash
git checkout -b feat/your-component
git add .
git commit -m "feat: add your component"
```

Keep commits focused. Avoid mixing an unrelated repository-wide refactor into a component contribution.

## Pull requests

Explain what changed and why. Include the affected technology and content type when useful.

For visual changes, include screenshots or a preview link when possible.

Mention validation commands you ran and any known limitations.

## Contributor checklist

- [ ] I placed the content in the correct technology and content type.
- [ ] I used kebab-case for new filesystem slugs.
- [ ] I added the required files for the content type (including README.md for Tailwind component variants).
- [ ] Metadata accurately describes the implementation.
- [ ] Interactive behavior is keyboard accessible.
- [ ] Focus states are visible where applicable.
- [ ] Motion respects `prefers-reduced-motion` where applicable.
- [ ] The component works at mobile and desktop widths.
- [ ] I avoided unnecessary dependencies.
- [ ] I regenerated `snippets-index.json` when content changed.
- [ ] I added the `AGENTS.md` template-specific agent-instructions file when adding or editing a template.
- [ ] `python scripts/tooling/validators/validate.py` passes.
- [ ] `python scripts/tooling/validators/check_md_links.py` passes if Markdown changed or referenced files moved.
- [ ] I documented any known limitations in the pull request.

## Maintainer principle

When in doubt, prefer the smallest change that preserves the repository's existing architecture and makes the content easier to discover, reuse, and maintain.
