# Conventions

The naming, file, JSON, and code conventions actually used in this repository, with what enforces them.

## Directory naming

| Level | Convention | Enforced by |
|---|---|---|
| Technology dirs | Capitalized: `React`, `Tailwind`, `Vanilla` | `validate.py` (`TECH_DIRS`, `ALLOWED_DIRS`) |
| Content-type dirs | Capitalized, exactly `Components`, `Sections`, `Templates` | `validate.py` (`ALLOWED_DIRS`) |
| Families | Capitalized: `Buttons`, `Hero`, `Logo-Cloud`. Existing exceptions to follow when joining them: `AI-Product`, `App-UI`, `Premium-Visual`, `SaaS`, `404` (Tailwind sections) | Convention |
| Variants | kebab-case, lowercase: `solid-button`, `basic-accordion`, `hero-minimal` | Convention |
| Forbidden | `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, `Tools/` under any tech | `validate.py` (`check_architecture`) |

## File naming

Inside a leaf, file names are fixed lowercase constants: `code.html`, `code.tsx`, `code.jsx`, `preview.html`, `metadata.json`, `README.md`, `AGENTS.md`. Template support directories (`pages/`, `assets/`, `css/`, `js/`, `src/`) and React toolchain config files follow their own established names — do not rename them.

## Display names and IDs

- Display `name`: human-readable Title Case — `Solid Button`, `Minimal Hero`.
- Tailwind generated sections: `"Modern Blog — Minimal"` (em dash + style).
- React sections: `"<Family> — <Direction>"`.
- `id`: kebab-case, often zero-padded (`split-button-001`, `hero-minimal-001`).
- **IDs are stable.** Never change an existing ID to make it look nicer. New content must not collide with an existing ID (duplicates are a validator NOTE, not a license).
- Avoid generic variants: `new`, `test`, `final`, `version-2`.

## JSON conventions

- Booleans are real JSON booleans, never `"true"`/`"false"` strings.
- `tags` are lowercase search words; `features` are short capability phrases; `searchTerms` are longer user-intent phrases.
- `type` is lowercase (`component`/`section`/`template`); `category` is Capitalized (`Components`/`Sections`/`Templates`). Never conflate them.
- Registry paths carry a trailing slash; `files[]` entries are bare file names or one-level prefixed paths with no leading directory.
- Metadata schemas are per-framework — copy a sibling; never invent keys.

## Code conventions

- **Tailwind** `code.html`: snippet only — no DOCTYPE/head/body/CDN. 2-space indent, semantic HTML, scoped vanilla JS (`document.currentScript.closest('[data-…="…"]')` pattern), reduced-motion-safe animations. `preview.html` is a full page with the CDN.
- **Vanilla components**: self-contained fragments, inline style+script, `--ds-*` tokens with fallbacks. **Vanilla sections**: full standalone pages (`<body class="nb">`, own token set).
- **React**: TSX-first, no `any`, no inline `style=`, `code.jsx` kept in exact parity with `code.tsx`, `motion-reduce:transition-none` guards, `focus-visible` rings.
- **Accessibility** is part of the quality bar everywhere: native semantics first, ARIA only to supplement, keyboard operability, visible focus, reduced-motion support, no color-only state.
- **Responsive** means usable at mobile widths without horizontal overflow, not pixel-identical across breakpoints.

## Markdown and documentation

- Repository docs are GitHub-flavored Markdown with `#` titles. Docs in `docs/` (maintainer specs) use SCREAMING_CASE filenames; token/reference docs use the same form (`DESIGN_TOKENS.md`, `STYLE_TOKENS.md`).
- Do not quote inventory counts in documentation — read `snippets-index.json`.
- Do not add comment banners to generated files — they are overwritten.

## Tooling and tests

- Python tooling lives under `scripts/` grouped by role: `tooling/validators/`, `tooling/indexing/`, `tooling/generators/`, `tooling/utilities/`, `qa/resources/`. Module docstrings name their own run command; scripts resolve the repo root from their own path.
- CLI tests are plain `node:assert` scripts (`cli/test/<module>.test.js`) using `os.tmpdir()` sandboxes, chained in `cli/package.json` `scripts.test`. No test framework.
- One-off migration/repair scripts belong in `scripts/tooling/utilities/`. Untracked ad-hoc patches at the repo root are not a convention.

## Git conventions

- Branches are prefixed: `feat/your-component`, `chore/…`.
- Commit messages use conventional prefixes: `feat:`, `chore:`.
- Keep commits focused; do not mix a repository-wide refactor into a resource contribution.
- Pull requests use the PR template and must report the validation commands run.
- `.gitignore` is currently empty — build artifacts and CLI output (`devsnips/`) are not ignored. Do not assume an ignore rule exists.

## Generated files — never hand-edit

`snippets-index.json` (`rebuild_index.py`), `agents/resources/indexes/*.json` (`build_resource_indexes.py`), `website/**` (`gen_site.py`), `devsnips/config.json` (CLI). `devsnips/AGENTS.md` is CLI-created once and user-owned thereafter.
