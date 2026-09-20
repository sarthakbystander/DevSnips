# Technologies

DevSnips supports exactly three technologies. They are named `React`, `Tailwind`, and `Vanilla` on disk (Capitalized directory names), and appear in the registry as `React`, `Tailwind CSS`, and `Vanilla HTML/CSS/JS`. Use the registry strings when filtering; use the disk names when writing paths.

| Disk name | Registry `tech` string | Destination slug (CLI) |
|---|---|---|
| `React` | `React` | `react` |
| `Tailwind` | `Tailwind CSS` | `tailwind` |
| `Vanilla` | `Vanilla HTML/CSS/JS` | `vanilla` |

All three technologies carry all three resource types (`Components`, `Sections`, `Templates`).

## React

**What it means.** TypeScript-first React implementations styled with Tailwind utilities. Components are drop-in source files, not npm packages; templates are complete Vite projects.

**Implementation files.**

- Components: `code.tsx` (primary, TypeScript) + `code.jsx` (JavaScript parity build — same API, classes, and behavior with TS syntax stripped) + `preview.html`.
- Sections: `code.tsx` only (+ `preview.html`). No parity build, no README.
- Templates: a full Vite + TypeScript + Tailwind project.

**Conventions.** No `any`; no inline `style=` in `code.tsx`/`code.jsx`; native semantics with ARIA wiring and `focus-visible` rings; `motion-reduce:transition-none` guards; `--ds-*` tokens consumed via Tailwind arbitrary values (e.g. `bg-[var(--ds-color-primary)]`). `preview.html` is fully self-contained (Tailwind CDN + React 18 UMD + Babel standalone, inline token block with a persisted no-flash dark toggle).

**Limitations.** Sections ship `code.tsx` only — do not expect or invent a `code.jsx`. There is no in-repo generator that re-emits React files; committed files are canonical. The section and component metadata disagree on `technology` casing (`"React"` vs `"react"`); the indexer tolerates this.

## Tailwind CSS

**What it means.** Copy-paste Tailwind markup. `code.html` contains component markup only — no `<html>`, `<head>`, `<body>`, `<!DOCTYPE>`, or CDN script.

**Implementation files.**

- Components and Sections: `code.html` + `preview.html` (+ `metadata.json`, and `README.md` for components; sections carry it optionally).
- Templates: multi-page or single-page static sites under `pages/`.

**Conventions.** `preview.html` is a full `<!DOCTYPE html>` page loading the Tailwind CDN and the Inter font, with a realistic application shell. Interactivity uses scoped vanilla JS with the `document.currentScript.closest('[data-<thing>="<style>"]')` pattern so snippets work standalone. Pure-CSS animations must be reduced-motion safe. Section families use a shared style system (`neo-brutalism`, `vercel`, `sharp-glassmorphism`) documented in `library/Tailwind/Components/STYLE_TOKENS.md`.

**Limitations.** Running the full section generator regenerates *all* section folders and can overwrite hand-patched variants — prefer editing committed `code.html` directly. Never add a CDN script or DOCTYPE to `code.html`.

## Vanilla (HTML/CSS/JS)

**What it means.** Zero-dependency HTML/CSS/JS. The registry names the technology `Vanilla HTML/CSS/JS` — use that exact string when filtering.

**Implementation files.**

- Components: `code.html` — a self-contained fragment (inline `<style>` + inline `<script>`, no DOCTYPE wrapper by accepted convention) + `metadata.json` + `README.md`.
- Sections: `code.html` — a **full standalone page** (`<!DOCTYPE html>`, `<body class="nb">`, own token vocabulary) + `metadata.json` + `README.md`.
- Templates: root `metadata.json` + `README.md` + `AGENTS.md` + `preview.html`, all code under `pages/`.

**Conventions.** Components reference `var(--ds-<token>, <fallback>)` so they render standalone and re-theme together via `library/Vanilla/Components/tokens.css`. Sections use their own neo-brutalist token set. Machine-enforced quality bar on components: `prefers-reduced-motion` guards, `:focus-visible` rings, ARIA/roles on custom widgets, native element semantics (or full `role="button"` + Enter/Space handling).

**Limitations.** No `preview.html` at component/section level (only templates have it), so Vanilla resources are verified through the gallery pages and `qa_vanilla.py` rather than per-variant previews.

## Token documentation

| Document | Scope |
|---|---|
| `library/React/DESIGN_TOKENS.md` | React root `--ds-*` token spec. |
| `library/React/Sections/DESIGN_TOKENS.md` | React section directions (Minimal, Dark Premium, Bento, Neo-Brutalist). |
| `library/Tailwind/Components/STYLE_TOKENS.md` | Tailwind section style token palettes. |
| `library/Vanilla/Components/DESIGN_TOKENS.md` + `tokens.css` | The Swiss neo-minimal `--ds-*` system (canonical token source). |
| `library/Vanilla/Templates/design-tokens.md` | Vanilla template token spec. |

Do not introduce a second token vocabulary into an existing family without a documented reason.

## Adding a technology

Adding a fourth technology is a structural change: new top-level directory, scanner trees in `scripts/tooling/indexing/rebuild_index.py` (`*_TREES`), `ALLOWED_DIRS`/tech slug handling in the validators and the CLI, and registry schema review. It is not a folder copy. See [Contributing overview](../contributing/overview.md).
