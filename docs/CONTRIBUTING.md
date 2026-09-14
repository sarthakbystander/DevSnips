# Contributing to DevSnips

Thanks for contributing to DevSnips. The goal is to keep the library useful at scale, so contributions should be easy to discover, copy, review, and maintain.

## Before you start

Read these files first:

- `README.md` for the current repository structure and content counts.
- `COMPONENT_STRUCTURE.md` for folder, file, metadata, and naming rules.
- `AGENTS.md` for repository-specific automation and maintainer guidance.

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

## Tailwind component and section structure

A standard Tailwind component or section variant contains:

```text
<variant>/
├── code.html
├── preview.html
├── metadata.json
└── README.md
```

`code.html` must contain the focused copy-paste implementation. Keep demo-only wrappers and unrelated page content out of it.

`preview.html` is a complete standalone demonstration. It may contain Tailwind CDN setup, demo data, page framing, and scripts needed only for the preview.

`metadata.json` must contain the structured information required by the repository schema, including a valid `type` for Tailwind content.

`README.md` provides component-specific documentation: what the variant is, when to use it, how to install/customize it, accessibility notes, responsive behavior, and dependencies. Write it from the actual implementation in `code.html` rather than generic marketing text.

Tailwind `type` values are:

- `component`
- `section`
- `template`

The value must agree with the directory in which the metadata lives.

## Vanilla structure

Vanilla component variants use a single self-contained source file named `code.html` (inline `<style>` + `<script>`):

```text
<variant>/
├── code.html
├── README.md
└── metadata.json
```

The directory name is the canonical component id/slug; the primary component source file is always `code.html`. Do not introduce a second file convention for a new family without a clear repository-level reason.

Templates may have multiple HTML, CSS, JS, and documentation files because they represent complete experiences rather than isolated snippets.

## Template structure

Every template under `Tailwind/Templates/`, `React/Templates/`, or `Vanilla/Templates/` must contain an `AGENTS.md` at its root:

```text
<template>/
├── AGENTS.md          # template-specific AI agent instructions (required)
├── metadata.json
├── preview.html
├── README.md
└── pages/ or src/    # actual template source
```

`AGENTS.md` is DevSnips agent metadata/instructions — it is NOT template source code. It should explain what the template is, its structure, design system, how an agent should safely modify it, what NOT to change unnecessarily,and the quality bar to re-check. The validator enforces this structurally (`scripts/validate.py` fails when a template is missing it; `_gen/rebuild_index.py` refuses to write an index for a template that lacks it), so a new template contribution that omits `AGENTS.md` will not validate.

## Quality requirements

Every contribution should aim for production-ready output, not merely a visual screenshot.

Use semantic HTML where appropriate. Interactive controls should be keyboard accessible and have visible focus states. Use ARIA only when native HTML semantics are insufficient.

Respect reduced-motion preferences for meaningful animations. Avoid unnecessary JavaScript and external dependencies. Keep third-party dependencies explicit and minimal.

Components should work at common viewport sizes without horizontal overflow. Text should remain readable and controls should remain usable on touch devices.

Keep code focused. A component should demonstrate one clear pattern instead of becoming a miniature application unless it is intentionally a template or section.

## Naming

Use kebab-case for filesystem slugs:

```text
multi-step-form
pricing-comparison
animated-accordion
```

Use readable Title Case for display names in metadata.

Keep IDs stable. Do not change an existing ID merely to make it look nicer. New content should use a unique ID that will not collide with another entry.

## Metadata

Metadata is part of the library's infrastructure, not decoration. Keep names, descriptions, categories, tags, search terms, and related entries accurate.

Do not claim accessibility, responsiveness, browser support, or features that the implementation does not actually provide.

When adding a new family, make sure the family and its variants can be represented cleanly in `snippets-index.json`.

## Index and validation

After adding, moving, renaming, or deleting content, regenerate the index:

```bash
python3 -m _gen.rebuild_index
```

Then run:

```bash
python3 scripts/validate.py
```

Do not submit a pull request with a stale index or broken validation output.

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
- [ ] `python3 scripts/validate.py` passes.
- [ ] I documented any known limitations in the pull request.

## Maintainer principle

When in doubt, prefer the smallest change that preserves the repository's existing architecture and makes the content easier to discover, reuse, and maintain.
