# DevSnips — Validation and QA

Every verification layer in the repository, what it checks, where it lives, and what an agent
must run after a change. There is **no CI** in this repository (`.github/` contains only
`PULL_REQUEST_TEMPLATE.md`), so these checks run only when someone runs them.

## The gate you must always run

```bash
python scripts/tooling/validators/validate.py
```

Implementation: `scripts/tooling/validators/validate.py`. Prints
`VALIDATION PASSED - architecture, metadata, and index all consistent.` and exits `0` on
success; prints `VALIDATION FAILED - N problem(s):` and exits `1` otherwise. It resolves the
repo root from its own file location (`parents[3]`), so the working directory does not matter.

A second, more granular checker exists:

```bash
python scripts/tooling/validators/deep_check.py
```

Implementation: `scripts/tooling/validators/deep_check.py`. It is a standalone, stricter
file-set checker that runs alongside `validate.py` (it is **not** invoked by `validate.py`'s
`main()`). It enforces per-tech file sets and is stricter about
`README.md` and `code.jsx` in places where `validate.py` is not.

## Validation layers

| Layer | Enforcing file | What it covers |
|---|---|---|
| Architecture | `scripts/tooling/validators/validate.py` (`check_architecture`) | Allowed/forbidden dirs per tech. |
| Metadata validity | `scripts/tooling/validators/validate.py` (`check_metadata_validity`) | JSON parse, `type` value + bucket match, required files per tech. |
| Index ↔ disk consistency | `scripts/tooling/validators/validate.py` (`check_index_vs_disk`) | Two-way coverage, duplicate paths, stale paths. |
| Template `AGENTS.md` | `scripts/tooling/validators/validate.py` (`check_template_agents`) and `scripts/tooling/indexing/rebuild_index.py` (`validate`) | Existence + non-empty. |
| Per-tech file sets | `scripts/tooling/validators/deep_check.py` | Required/optional files per tech + type. |
| Vanilla quality bar | `scripts/qa/resources/qa_vanilla.py` (invoked by `validate.py`) | a11y/animation/dark-mode per Vanilla component. |
| Index regeneration safety | `scripts/tooling/indexing/rebuild_index.py` (`validate`) | Refuses to write on mismatch. |
| CLI behavior | `cli/test/*.test.js` | Path/file/context behaviors. |
| Browser QA (React) | `scripts/qa/resources/_qa_react_*.py` | Runtime, layout, theme, a11y per family. |
| Browser QA (templates) | `scripts/qa/resources/_qa_template.py` | Overflow, console errors, interactions. |
| Nav page QA | `scripts/qa/resources/test_tailwind_nav.py`, `test_react_nav.py` | Browse-page behavior. |

## Structure checks

`check_architecture()` in `scripts/tooling/validators/validate.py`:

- each of `library/Vanilla`, `library/Tailwind`, `library/React` may contain only
  `Components`, `Sections`, `Templates` (`ALLOWED_DIRS`);
- `Utilities`, `Resources`, `Snippets`, `Pages`, `Tools` are forbidden under every tech.

`is_leaf()` (in that file, and separately in `deep_check.py` and `rebuild_index.py`) defines
what counts as a resource — see `agents/resources/resources.md` §3 for the deliberate
difference between the indexer's predicate and the validators' predicate.

## Resource (file-set) checks

`check_metadata_validity()` in `validate.py`:

- Tailwind `Components/` and `Sections/` leaves must have `code.html` **and** `preview.html`;
- Tailwind `Components/` leaves must additionally have a non-empty `README.md`;
- React `Components/` and `Sections/` leaves must have `code.tsx` **and** `preview.html`;
- invalid JSON in any `metadata.json` is a failure.

`deep_check.py` `check_component_section_files()` adds:

- Tailwind Components: `code.html`, `preview.html`, `README.md`;
- Tailwind Sections: `code.html`, `preview.html` (README optional, non-empty if present);
## Indexing checks

Implementation: `scripts/tooling/indexing/rebuild_index.py` `validate()` and
`scripts/tooling/validators/validate.py` `check_index_vs_disk()`.

The full list of problems each reports is in `agents/resources/indexing.md` under
"Validation of the index".

## Vanilla quality bar

Implementation: `scripts/qa/resources/qa_vanilla.py` (standalone CLI; also invoked by
`validate.py` through `_run_qa()` with `--only-failures`).

Scans `library/Vanilla/Components/**` and `library/Vanilla/Sections/**` (`COMP` / `SECTIONS` /
`SCAN_ROOTS`), one check per component `.html`. Required-vs-advisory is decided by `checks()`:

| Check | Required when | Fails when |
|---|---|---|
| `doctype` | never (warn only) | — |
| `lang` | the file has a DOCTYPE | `<html lang>` missing |
| `viewport` | the file has a DOCTYPE | viewport meta missing |
| `reduced-motion` | the file animates (`transition:`/`animation:`/`@keyframes`) | no `prefers-reduced-motion` |
| `aria/role` | family is in `INTERACTIVE` | no `role`/`aria-*`, no native interactive element, no content semantics |
| `focus-visible` | family is in `INTERACTIVE` | no `:focus-visible` |
| `keyboard` | family is `INTERACTIVE` **and** the file wires interaction (`onclick`, click listeners, `role="button"`, div-with-onclick) | no `<button>/<a>/<input>/<select>/<textarea>/<summary>`, no `role="button"`, no `tabindex`, no `<dialog>` |
| `semantic` | never (warn only) | — |

`INTERACTIVE` = `modals, dropdowns, tabs, accordions, navigation, tooltips, buttons, forms,
loaders`. `VISUAL_ANIM` families get reduced-motion but not ARIA/keyboard requirements. Exit
code is `1` if **any** required check fails.

`python scripts/qa/resources/qa_vanilla.py --tokens` runs an advisory `--ds-*` token-conformance
report and **always exits 0**. The neo-brutalist sections keep their own `--bg`/`--surface`
system and are counted separately. See `agents/resources/frameworks/vanilla.md`.

## Browser QA (Playwright)

React harnesses: `scripts/qa/resources/_qa_react_*.py`. Python + Playwright; not wired into any
runner.

- They read source files from `ROOT / "library/React/..."` (e.g. `_qa_react_accordion.py`,
  `_qa_react_textareas.py`).
- Their `BASE` URLs are inconsistent about the `library/` prefix — e.g. `_qa_react_button.py`
  uses `f"{BASE}/React/Components/Buttons/{slug}/preview.html"` with
  `BASE = "http://localhost:8765"`, while the same file reads from `library/React/...`. For
  those URLs to resolve, **serve the repository with the document root set to `library/`**.
- Typical assertions: page/console errors, horizontal overflow at 375/768/1280, `data-theme`
  token flip, `focus-visible` outline, disabled opacity, reduced-motion, ARIA/role wiring, and
  each family's keyboard model.

Other harnesses:

- `scripts/qa/resources/_qa_template.py <path-to-preview.html>` — `file://` based; widths
  `320, 375, 768, 1024, 1280, 1920`; console/page errors; per-template interaction checks
  (`dp_checks` for `developer-portfolio`, `pl_checks` for `product-launch`, `ec_checks` for
  `event-conference`).
- `scripts/qa/resources/test_tailwind_nav.py`, `test_react_nav.py` — browse-page harnesses
  (`BASE = "http://localhost:12000"`).

## Expected verification flow

1. `python scripts/tooling/indexing/rebuild_index.py` — only if content was added, removed,
   renamed, or moved.
2. `python scripts/tooling/validators/validate.py`
3. `python scripts/tooling/validators/deep_check.py` — when file-set rules are in play.
4. `cd cli; npm test` — only if `cli/` changed.
5. The relevant browser harness — when the change is visual/interactive.
6. `python scripts/qa/resources/qa_vanilla.py` — when Vanilla content changed.

## Common failure classes

| Symptom | Likely cause | Inspect |
|---|---|---|
| `On-disk content leaf not indexed` | New leaf added but index not regenerated | `scripts/tooling/indexing/rebuild_index.py` |
| `Index variant missing on disk` | Leaf deleted/renamed without regenerating | same |
| `type=section outside Sections/` | Resource moved without updating `metadata.json` `type` | that leaf's `metadata.json` |
| `Tailwind component missing README.md` | Missing or empty README | `scripts/tooling/validators/deep_check.py` |
| `Architecture: unexpected dir` | New top-level dir under a tech tree | `ALLOWED_DIRS` in `validate.py` |
| `Template ... is missing AGENTS.md` | New template without a resource-level `AGENTS.md` | `validate.py`, `rebuild_index.py` |
| `FAIL <path> reduced-motion/focus-visible/...` | Vanilla quality bar | `scripts/qa/resources/qa_vanilla.py` |
| `NOT writing index due to validation problems` | Disk and index disagree | the printed problem list |
| `npm test` failure in `cli/` | File-selection or context behavior regressed | the specific `cli/test/*.test.js` |

## What an agent must verify after a change

- Ran `rebuild_index.py` if any leaf was added, removed, renamed, or moved.
- Ran `validate.py` and it passed (exit `0`).
- For file-set changes, ran `deep_check.py`.
- For `cli/` changes, ran `npm test` in `cli/`.
- For Vanilla content, ran `qa_vanilla.py` and confirmed `failing required checks: 0`.
- For visual/interactive changes, ran the relevant harness and checked console errors and
  horizontal overflow at mobile width.
- Read the actual output. `rebuild_index.py` printing "NOT writing index due to validation
  problems" is a failure, not a no-op.
Playwright is not declared in any manifest in this repository; install it in your environment
before running these.

## CLI checks

Implementation: `cli/test/`, run via `npm test` from `cli/` (see `cli/package.json`).

- `cli/test/downloader.test.js` — exactly which files install; asserts `metadata.json` and
  `preview.html` are excluded and `README.md`/`AGENTS.md`/source extensions are included,
  including a realistic nested template file list.
- `cli/test/config.test.js` — config structure, atomic write, malformed-JSON rejection,
  installation recording and de-duplication, field preservation.
- `cli/test/agents.test.js` — `AGENTS.md` created when missing, **never** overwritten.
- `cli/test/context.test.js` — orchestration: full initialization, preservation of custom files,
  safe failure on malformed config, recording only after install, no `.tmp` leftovers.
- `cli/test/init.test.js` — end-to-end `init` via `execSync`, including idempotency and
  malformed-config failure.
- React Components: `code.tsx`, `preview.html`, `README.md`;
- React Sections: `code.tsx`, `preview.html`;
- React component missing `code.jsx` → **warning** only (printed, does not fail);
- Vanilla Components/Sections: `metadata.json`;
- any Section with an empty `README.md` → failure.

`deep_check.py` `check_template_files()` requires per template root: a non-empty `AGENTS.md`
(all techs); Tailwind and React templates also need `preview.html`; Vanilla templates need
`preview.html` **or** a non-empty `pages/`, plus `README.md`.

## Metadata checks

Implementation: `scripts/tooling/validators/validate.py`

- `type` must be present and one of `component` / `section` / `template`;
- `type` must match the folder bucket, via explicit cross-checks
  (`type=component outside Components/`, `type=section outside Sections/`,
  `type=template outside Templates/`).
- Duplicate IDs are collected and reported as a **NOTE**, not a failure — the code states this
  is deliberate so pre-existing IDs are preserved. Do not "fix" duplicates as a side effect of
  an unrelated change; report them.

Per-technology metadata key sets are enumerated in `agents/resources/resources.md` §5.