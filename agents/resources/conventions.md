# DevSnips — Conventions

The naming, file, JSON, and code conventions actually used in this repository. Each entry notes
where the convention is demonstrated and, where applicable, what enforces it.

## Directory naming

- **Technology dirs** are Capitalized: `library/React/`, `library/Tailwind/`, `library/Vanilla/`.
  Enforced: `scripts/tooling/validators/validate.py` (`TECH_DIRS`, `ALLOWED_DIRS`).
- **Content-type dirs** are Capitalized and exactly `Components`, `Sections`, `Templates`.
  Enforced: `ALLOWED_DIRS` in `scripts/tooling/validators/validate.py`.
- **Families** are Capitalized: `Buttons`, `Accordions`, `Hero`, `Testimonials`, `Logo-Cloud`.
  Exceptions that exist today: Tailwind section families use hyphen/initialism forms —
  `AI-Product`, `App-UI`, `Premium-Visual`, `SaaS`, `404`. Follow the family you are joining.
- **Variants** are kebab-case and lowercase: `solid-button`, `basic-accordion`, `hero-minimal`,
  `dark-premium`, `neo-brutalist`.
- Never create `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` under a tech.
  Enforced: `check_architecture()` in `scripts/tooling/validators/validate.py`.

## File naming

Inside a leaf, file names are fixed lowercase constants:

| File | Meaning |
|---|---|
| `code.html` | Tailwind/Vanilla implementation (snippet / self-contained) |
| `code.tsx` | React primary implementation |
| `code.jsx` | React JavaScript parity build (components only) |
| `preview.html` | Runnable demo — never installed |
| `metadata.json` | Required registry record |
| `README.md` | Variant documentation |
| `AGENTS.md` | Template-level agent instructions |

Template support directories, observed: `pages/` (Tailwind, Vanilla), `assets/` (Tailwind,
Vanilla), `css/` and `js/` (`library/Vanilla/Templates/saas-dashboard/`), and `src/` with
`components/`, `data/`, `pages/`, `sections/`, `styles/`
(`library/React/Templates/spray-art-school/`).

React template project config files follow the toolchain's own conventions: `index.html`,
`package.json`, `package-lock.json`, `postcss.config.js`, `tailwind.config.ts`, `tsconfig.json`,
`.gitignore`. Do not rename these.

## Resource naming (display names)

- The filesystem slug / folder name is the canonical identity. Where `slug` exists in
  `metadata.json` it should match the folder name.
- Display `name` is human-readable Title Case: `Solid Button`, `Basic Accordion`,
  `Minimal Hero`, `Meridian Incident Command Platform`.
- Tailwind generated sections use an em dash with the style name:
  `"Modern Blog — Minimal"`, `"Premium SaaS 404 — Apple Inspired"`.
- React sections use `"<Family> — <Direction>"`: `"Hero — Minimal"`, `"CTA — Bento"`.
- Avoid generic variants such as `new`, `test`, `final`, `version-2`
  (`docs/COMPONENT_STRUCTURE.md`, "Naming conventions").

## IDs and slugs

- `id` values are kebab-case, often suffixed with a zero-padded index: `solid-button-react-001`,
  `split-button-001`, `hero-minimal-001`, `blog-minimal`, `agency-001`.
- **Keep IDs stable.** `docs/CONTRIBUTING.md`: "Keep IDs stable. Do not change an existing ID
  merely to make it look nicer."
- Duplicate IDs are reported as an informational NOTE by
  `scripts/tooling/validators/validate.py`, not a failure; new content must not add collisions.

## Markdown conventions

- Repository docs are GitHub-flavored Markdown with `#` titles.
- Doc files in `docs/` are SCREAMING_CASE (`COMPONENT_STRUCTURE.md`, `CONTRIBUTING.md`,
  `PULL_REQUEST_TEMPLATE.md`, `VANILLA_CURATION_REPORT.md`); token/reference docs use the same
  form (`DESIGN_TOKENS.md`, `STYLE_TOKENS.md`) or lowercase
  (`library/Vanilla/Templates/design-tokens.md`).
- Variant `README.md` files cover: what the variant is, when to use it, how to install/customize
  it, accessibility notes, responsive behavior, dependencies (`docs/CONTRIBUTING.md`).
- Template `AGENTS.md` files use a consistent section shape: what the template is, design
  system, file layout, how to adapt it, and guardrails. See
  `library/Tailwind/Templates/meridian/AGENTS.md` and
  `library/React/Templates/spray-art-school/AGENTS.md`.
- The optional `code.html` snippet header comment is
  `Snippet Name / Description / Author: DevSnips Contributors / Usage Example`
  (`docs/CONTRIBUTING.md`, `library/Tailwind/Components/STYLE_TOKENS.md`).

## JSON conventions

- All JSON is 2-space indented UTF-8. CLI-written JSON (`devsnips/config.json`) is 2-space
  indented **with** a trailing newline (`cli/src/devsnips/config.js` `writeConfig`).
## Code conventions

- **Indentation:** 2 spaces for HTML, CSS, TS/TSX, JS. The Python tooling is 4-space PEP 8.
- **HTML:** semantic elements, headings in order, ARIA only to supplement native semantics.
- **Tailwind:** Tailwind utilities only; inline `<style>` only for pure-CSS animation helpers.
  Scope JS with `document.currentScript.closest('[data-<scope>]')` so a snippet works in
  isolation (`library/Tailwind/Components/STYLE_TOKENS.md`).
- **Vanilla:** `code.html` is self-contained (inline `<style>` + `<script>`). The shared `--ds-*`
  token vocabulary is documented in `library/Vanilla/Components/DESIGN_TOKENS.md`; the
  neo-brutalist sections deliberately use their own `--bg`/`--surface`/`--radius` set instead.
- **React:** TypeScript-first. `code.tsx` is primary, `code.jsx` is the parity build. Section
  variants intentionally ship `code.tsx` only.
- **No extra frameworks:** no React/Vue/Alpine/Bootstrap/jQuery in Tailwind or Vanilla content
  (`docs/COMPONENT_STRUCTURE.md`). React content obviously uses React. Only the dependencies
  already present in real metadata are conventional (`agents/resources/resources.md` §7).
- Accessibility is part of the bar: keyboard operability, visible focus, reduced-motion support,
  and no color-only state. Vanilla is machine-checked by
  `scripts/qa/resources/qa_vanilla.py`.

## Generated files

- `snippets-index.json` — generated by `scripts/tooling/indexing/rebuild_index.py`. Never
  hand-edit.
- `website/**` — published output (mirrors, `llms.txt`, `search-index.json`).
- `devsnips/config.json` — CLI-managed; may be rewritten by the CLI, never by hand.
- `devsnips/AGENTS.md` — user-owned; the CLI creates it once and never overwrites it
  (`cli/src/devsnips/agents.js`).

## Comments

- Python tooling uses module docstrings explaining what the file does, usually including the run
  command (e.g. the header of `scripts/tooling/indexing/rebuild_index.py`).
- Non-obvious decisions carry an inline comment explaining *why* (e.g. the Windows path note in
  `rebuild_index.py` `rel_path()`, the leaf-predicate rationale in
  `scripts/tooling/validators/validate.py`).
- Do not add comment banners to generated files — they are overwritten.

## Tests

- CLI tests are plain `node:assert` scripts named `<module>.test.js` under `cli/test/`, using a
  `check(name, fn)` helper and `os.tmpdir()` sandboxes, chained in `cli/package.json`
  `scripts.test`. No test framework.
- Python QA scripts live under `scripts/qa/resources/`, run directly (`python <script>`), and
  exit non-zero on failure. No pytest.
- There is no repository-root test runner — see `agents/resources/qa.md`.

## Scripts

- Repository tooling lives under `scripts/`, grouped by role: `tooling/validators/`,
  `tooling/indexing/`, `tooling/generators/`, `tooling/utilities/`, `qa/resources/`.
- Python module docstrings name their own run command. Prefer
  `python scripts/<group>/<name>.py` from the repository root — the scripts resolve `ROOT` from
  their own file path, so the working directory does not matter.
- One-off migration/repair scripts belong in `scripts/tooling/utilities/`. Untracked ad-hoc
  patches at the repo root (`fix_validate.py`) are not a convention — do not add more.

## Git conventions (from repository evidence)

- Branch naming observed in the current git state is prefixed (`chore/complete-library-path-integration`),
  matching `docs/CONTRIBUTING.md`'s `feat/your-component` example.
- Commit messages use conventional prefixes: `feat:`, `chore:`
  (`docs/CONTRIBUTING.md`: `git commit -m "feat: add your component"`).
- Keep commits focused; do not mix a repository-wide refactor into a resource contribution
  (`docs/CONTRIBUTING.md`, "Git workflow").
- `.gitignore` is currently empty, so build artifacts and CLI output (`devsnips/`) are not
  ignored. Note this rather than assuming an ignore rule exists.
- Pull requests use `docs/PULL_REQUEST_TEMPLATE.md` / `.github/PULL_REQUEST_TEMPLATE.md` and must
  report the validation commands run (`docs/CONTRIBUTING.md`, contributor checklist).
- Booleans are real JSON booleans (`true`/`false`), not strings.
- `tags` are lowercase search words; `features` are short human-readable phrases; `searchTerms`
  are longer user-intent phrases.
- `type` is lowercase (`component`/`section`/`template`); `category` is Capitalized
  (`Components`/`Sections`/`Templates`). Do not conflate them.
- Registry paths carry a **trailing slash** in `snippets-index.json`; `files[]` entries are bare
  file names (or one-level `pages/...` / `src/...` paths) with no leading directory.
- Metadata schemas are **per-framework**, not universal — copy a sibling
  (`agents/resources/resources.md` §5). Do not invent keys.