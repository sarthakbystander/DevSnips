# Resource structure

The exact file contract inside a resource. "Required" means a failure in `scripts/tooling/validators/deep_check.py` and/or `scripts/tooling/validators/validate.py`. "Optional" means allowed and sometimes present.

## Fixed file names

File names inside a leaf are fixed lowercase constants:

| File | Meaning | Installed by CLI? |
|---|---|---|
| `code.html` | Tailwind/Vanilla implementation (snippet or self-contained page) | Yes |
| `code.tsx` | React primary implementation | Yes |
| `code.jsx` | React JavaScript parity build (components only) | Yes |
| `preview.html` | Runnable demo | **Never** |
| `metadata.json` | Registry record | **Never** |
| `README.md` | Variant documentation | When present |
| `AGENTS.md` | Template-level agent instructions | When present |

Template support directories: `pages/` (Tailwind, Vanilla), `assets/` (Tailwind, Vanilla), `css/`, `js/` (Vanilla saas-dashboard), and `src/` with `components/`, `data/`, `pages/`, `sections/`, `styles/` (React). React template config files follow the toolchain's own conventions (`index.html`, `package.json`, `tsconfig.json`, `tailwind.config.ts`, `postcss.config.js`, `.gitignore`) — do not rename them.

## Required files per tech + type

### React — `library/React/{Components,Sections,Templates}/`

| Type | Required | Optional / notable |
|---|---|---|
| Component | `code.tsx`, `preview.html`, `metadata.json`, `README.md` | `code.jsx` parity build (missing → warning, not error, in `deep_check.py`) |
| Section | `code.tsx`, `preview.html`, `metadata.json` | **No `README.md`, no `code.jsx`** |
| Template | `preview.html`, `metadata.json`, `AGENTS.md` | Full Vite/TS project: `index.html`, `package.json`, configs, `src/**`, `README.md` |

Example: `library/React/Components/Buttons/split-button/`

### Tailwind — `library/Tailwind/{Components,Sections,Templates}/`

| Type | Required | Optional / notable |
|---|---|---|
| Component | `code.html`, `preview.html`, `metadata.json`, `README.md` | 3-level layout allowed (Buttons groups) |
| Section | `code.html`, `preview.html`, `metadata.json` | `README.md` optional but non-empty when present |
| Template | `preview.html`, `metadata.json`, `AGENTS.md` | `README.md`, `pages/**`, `assets/**` |

Examples: `library/Tailwind/Components/Accordions/basic-accordion/` (2-level), `library/Tailwind/Components/Buttons/basic-button/primary/` (3-level), `library/Tailwind/Sections/Blog/minimal/` (2-level), `library/Tailwind/Sections/AI-Product/model-comparison/vercel/` (3-level), `library/Tailwind/Templates/meridian/`.

### Vanilla — `library/Vanilla/{Components,Sections,Templates}/`

| Type | Required | Optional / notable |
|---|---|---|
| Component | `metadata.json` | `code.html`, `README.md` are the universal convention but not machine-enforced |
| Section | `metadata.json` | `code.html`, `README.md` (non-empty when present) |
| Template | `metadata.json`, `AGENTS.md`, `preview.html` **or** non-empty `pages/`, plus `README.md` | modular `pages/{code.html,style.css,script.js}`, `css/`, `js/`, `assets/` |

Examples: `library/Vanilla/Components/Buttons/split-button/`, `library/Vanilla/Sections/Hero/hero-minimal/`, `library/Vanilla/Templates/agency/`, `library/Vanilla/Templates/saas-dashboard/`.

## What each file is for

- **Implementation (`code.*`)** — the production-ready artifact. A consumer integrates this; everything else is context.
- **`preview.html`** — a standalone demonstration page. It may include CDNs, demo data, and framing that must never leak into the implementation file. Browsers and QA harnesses open this file.
- **`metadata.json`** — the structured record consumed by the index generator. Its `type` must match the folder bucket. See [Metadata](../machine-readable/metadata.md).
- **`README.md`** — variant documentation: what it is, when to use it, how to customize it, accessibility and responsive notes, dependencies. Written from the actual implementation, not generic prose.
- **`AGENTS.md`** — template-level instructions for agents working with that template. Required for every template.

## Supporting and generated content

- **Token docs and galleries inside `library/`** are non-resource files that live at family or technology level (`DESIGN_TOKENS.md`, `STYLE_TOKENS.md`, `tokens.css`, gallery `index.html` pages). They are not leaves and are not indexed as resources.
- **The `files` manifest** in the registry is generated from disk (direct files plus one level inside `pages/`, and for React templates `src/`, `components/`, `data/`, `sections/`, `styles/`). Files deeper than one level are not listed — keep important files within one level of those directories.

## Notes

- There are deliberately **no per-resource README requirements beyond the contract above**, and no additional documentation files are part of the architecture. Keep resource-level documentation in `README.md` and, for templates, `AGENTS.md`.
- The folder name is the identity. Never rename a leaf to "improve" naming — see [Conventions](../reference/conventions.md).
