# Contributing — creating resources

The complete procedure for adding a resource. Goal → steps → result.

**Goal:** a new leaf under `library/` that passes validation and appears correctly in the registry.

**Prerequisites:** you have read [Resource structure](../resources/resource-structure.md) and [Metadata](metadata.md), and you know the resource's technology, type, and family.

## Step 1 — Classify the resource

| If the contribution is… | Type | Directory |
|---|---|---|
| One focused UI pattern | component | `library/<Tech>/Components/<Family>/<slug>/` |
| A page-level composition | section | `library/<Tech>/Sections/<Family>/<slug>/` |
| A complete page or site | template | `library/<Tech>/Templates/<slug>/` |

Do not upscale or downscale. If it could be either, present both options in the PR discussion rather than guessing.

## Step 2 — Pick or create the family

- Prefer joining an existing family; inspect its sibling leaves for house style.
- New family names are Capitalized (`Buttons`, `Hero`, `Logo-Cloud`). Follow the family you are joining — Tailwind section families use hyphen/initialism forms (`AI-Product`, `SaaS`, `404`).
- For a new generated-style Tailwind or Vanilla section family, the display name comes from `SECTION_FAMILY_NAMES` / `VANILLA_SECTION_FAMILY_NAMES` in `scripts/tooling/indexing/rebuild_index.py` — add a mapping there if the derived name is poor.

## Step 3 — Create the folder with the exact file set

Kebab-case, lowercase slug. Required files per tech + type (full table in [Resource structure](../resources/resource-structure.md)):

| Tech + type | Create |
|---|---|
| React component | `code.tsx`, `code.jsx`, `preview.html`, `metadata.json`, `README.md` |
| React section | `code.tsx`, `preview.html`, `metadata.json` |
| React template | full Vite/TS project + `preview.html`, `metadata.json`, `AGENTS.md`, `README.md` |
| Tailwind component | `code.html`, `preview.html`, `metadata.json`, `README.md` |
| Tailwind section | `code.html`, `preview.html`, `metadata.json` (README optional, non-empty if present) |
| Tailwind template | pages + root `preview.html`, `metadata.json`, `AGENTS.md` |
| Vanilla component | `code.html`, `metadata.json`, `README.md` |
| Vanilla section | `code.html`, `metadata.json`, `README.md` |
| Vanilla template | `pages/` code + root `metadata.json`, `README.md`, `AGENTS.md`, `preview.html` |

## Step 4 — Implement

Technology-specific requirements:

- **Tailwind** — `code.html` is copy-paste ready: markup only, no `<html>`/`<head>`/`<body>`/`<!DOCTYPE>`/CDN script. 2-space indentation, semantic HTML, scoped vanilla JS for interactivity, reduced-motion-safe animations. `preview.html` is a full page loading the Tailwind CDN + Inter font.
- **Vanilla components** — `code.html` is self-contained: inline `<style>` + `<script>`, `--ds-*` tokens with fallbacks, reduced-motion guards, `:focus-visible` rings, native semantics (or full role+keyboard handling).
- **Vanilla sections** — `code.html` is a full standalone page with `<body class="nb">` and the section token vocabulary.
- **React components** — TSX-first, no `any`, no inline `style=`, token consumption via Tailwind arbitrary values; keep `code.jsx` in exact parity with `code.tsx`.
- **React sections** — one exported component with all content as overridable props; follow the four-direction architecture and read `library/React/Sections/DESIGN_TOKENS.md` first.
- **All** — accessibility is part of the quality bar (keyboard, focus, ARIA only to supplement, reduced motion); responsive means no horizontal overflow at mobile widths.

## Step 5 — Write metadata

Copy the sibling's `metadata.json` shape (same family, same type), adjust every field, and set `type` to match the folder bucket. See [Metadata](metadata.md).

## Step 6 — Write README.md (when required)

Write it from the actual implementation: what the variant is, when to use it, how to install/customize it, accessibility notes, responsive behavior, dependencies. Not marketing prose.

## Step 7 — Write AGENTS.md (templates only)

Required at the template root. What it should cover: [Agent files](agent-files.md).

## Step 8 — Regenerate the registry and validate

```bash
python scripts/tooling/indexing/rebuild_index.py
python scripts/tooling/validators/deep_check.py
python scripts/tooling/validators/validate.py
```

Check the registry entry that was created: correct family name, `variantsCount`, `type`, and the variant's `files[]` manifest (this manifest drives CLI installs).

## Step 9 — QA (per scope)

- Vanilla components: `python scripts/qa/resources/qa_vanilla.py --only-failures` — must report zero failing required checks.
- Visual/interactive changes: run the relevant Playwright harness under `scripts/qa/resources/` (check it exists first; not every family has one).
- CLI changes: `cd cli && npm test`.

## Step 10 — Pull request

Branch `feat/…`, conventional commit, focused diff. Include screenshots or a preview link for visual changes, the exact validation commands run, and known limitations. Checklist: [Contributing overview](overview.md).

## Result

The resource is indexed, browsable on the website (after site regeneration), installable via `npx devsnips add <path>`, and covered by the validators. Anything less means a step was skipped — the validator output will say which.
