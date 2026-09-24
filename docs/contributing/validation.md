# Contributing — validation and QA

CI (`.github/workflows/ci.yml`) runs the always-on gates on every push and pull request. The browser QA layers are still manual, so a pull request must state which commands were run and what they printed.

## The command matrix

| Scope | Command | Passing condition |
|---|---|---|
| Always (minimum bar) | `python scripts/tooling/validators/validate.py` | Prints `VALIDATION PASSED - architecture, metadata, and index all consistent.`, exit 0 |
| File-set changes | `python scripts/tooling/validators/deep_check.py` | No failures reported (also covered by `validate.py`) |
| Any content added/removed/renamed | `python scripts/tooling/indexing/rebuild_index.py` | Prints `Wrote snippets-index.json` — not `NOT writing index due to validation problems` |
| Index drift check (what CI runs) | `python scripts/tooling/indexing/rebuild_index.py --check` | Prints `Index is up to date (--check).`; does not write |
| After index regeneration | `python scripts/tooling/indexing/validate_indexes.py` | Exit 0 (indexes match the repository) |
| Markdown edits / file moves | `python scripts/tooling/validators/check_md_links.py` | `OK: all relative Markdown links resolve` |
| Agent-facing docs edits | `python scripts/tooling/validators/check_agent_doc_paths.py` | `OK: all path references in scanned agent docs resolve` |
| Validator/indexer changes | `python -m unittest discover -s scripts/tooling/tests -t scripts/tooling/tests` | All tests pass |
| Vanilla component changes | `python scripts/qa/resources/qa_vanilla.py --only-failures` | `failing required checks: 0` |
| CLI changes | `cd cli && npm test` | All suites pass |
| Visual/interactive changes | Relevant Playwright harness under `scripts/qa/resources/` | No console errors, no horizontal overflow at mobile width |

Python scripts resolve the repository root from their own file location, so the working directory does not matter. Playwright is not declared in any manifest — install it in your environment before running browser harnesses.

## The full validation layers

Every verification layer, what it checks, and where it lives:

| Layer | Enforcing file | What it covers |
|---|---|---|
| Architecture | `validate.py` (`check_architecture`) | Allowed/forbidden dirs per tech |
| Metadata validity | `validate.py` (`check_metadata_validity`) | JSON parse, `type` value + bucket match, required files per tech |
| Index ↔ disk consistency | `validate.py` (`check_index_vs_disk`) | Two-way coverage, duplicate paths, stale paths |
| Template `AGENTS.md` | `validate.py` (`check_template_agents`) + `rebuild_index.py` (`validate`) | Existence + non-empty |
| Per-tech file sets | `deep_check.py` (merged into `validate.py`) | Required/optional files per tech + type |
| Markdown links | `check_md_links.py` | Relative links in every `*.md` resolve, and `file.md#fragment` anchors match a real heading slug |
| Agent doc paths | `check_agent_doc_paths.py` | Path-like backticked refs in agent-facing docs (`agents/resources/*.md`, `library/**/AGENTS.md`, MCP) resolve |
| Python tooling tests | `scripts/tooling/tests/` (`unittest`) | Unit tests for the validators and indexer ordering/leaf detection |
| Vanilla quality bar | `qa_vanilla.py` (invoked by `validate.py`) | a11y/animation/dark-mode per Vanilla component |
| Index regeneration safety | `rebuild_index.py` (`validate`) | Refuses to write on mismatch |
| CLI behavior | `cli/test/*.test.js` | Path/file/context behaviors |
| Browser QA (React) | `scripts/qa/resources/_qa_react_*.py` | Runtime, layout, theme, a11y per family |
| Browser QA (templates) | `scripts/qa/resources/_qa_template.py` | Overflow, console errors, interactions |
| Nav page QA | `scripts/qa/resources/test_tailwind_nav.py`, `test_react_nav.py` | Browse-page behavior |

## Structure checks

`check_architecture()` (in `validate.py`):

- each of `library/Vanilla`, `library/Tailwind`, `library/React` may contain only `Components`, `Sections`, `Templates` (`ALLOWED_DIRS`);
- `Utilities`, `Resources`, `Snippets`, `Pages`, `Tools` are forbidden under every tech.

The `is_leaf()` predicate (in `validate.py`, `deep_check.py`, and `rebuild_index.py`) defines what counts as a resource — see [Resource model](../resources/overview.md) for the deliberate difference between the indexer's predicate and the validators' predicate.

## Resource (file-set) checks

`check_metadata_validity()` in `validate.py`:

- Tailwind `Components/` and `Sections/` leaves must have `code.html` **and** `preview.html`;
- Tailwind `Components/` leaves must additionally have a non-empty `README.md`;
- React `Components/` and `Sections/` leaves must have `code.tsx` **and** `preview.html`;
- invalid JSON in any `metadata.json` is a failure.

`deep_check.py` is a standalone, stricter file-set checker whose `collect()` is merged into `validate.py`'s `main()` (so a `validate.py` pass includes it; it is still runnable on its own for a focused report). It enforces per-tech file sets and is stricter about `README.md` and `code.jsx` in places where `validate.py` is not: React Components need `code.tsx`, `preview.html`, `README.md`; React Sections need `code.tsx`, `preview.html`; a missing React `code.jsx` is a **warning** only; any Section with an empty `README.md` is a failure. `check_template_files()` requires a non-empty `AGENTS.md` for every template, plus `preview.html` (Tailwind/React) or `preview.html` **or** non-empty `pages/` (Vanilla), plus `README.md` (Vanilla).

## Metadata checks

- `type` must be present and one of `component` / `section` / `template`;
- `type` must match the folder bucket via explicit cross-checks (`type=component outside Components/`, etc.);
- Duplicate IDs are collected per technology/type/subcategory. A collision within one technology, content type, and subcategory fails (two leaves in the same collection cannot share an id). Ids echoed across technologies (Tailwind and React `team-minimal`, etc.) are expected id-parity reported as a **NOTE**, because the registry keys on the tech-first *path*.

## What `qa_vanilla.py` checks

Per Vanilla component `.html` under both the Components and Sections trees: accessibility and interaction semantics (keyboard operability, focus visibility, ARIA on custom widgets), reduced-motion guards on animations. Dark-mode support is computed but not yet an emitted pass/fail check. Flags: `--only-failures`, `--json`, and advisory `--tokens` (`--ds-*` adoption vs raw hex; always exits 0). It runs **inside** `validate.py`, so a required-check failure fails overall validation.

## Browser QA harnesses

Per-family Playwright scripts under `scripts/qa/resources/`:

- `_qa_react_*.py` — React component/section families. Serve the repo with document root `library/` on `:8765` (`python3 -m http.server 8765 --directory library`), then invoke per slug:
  ```bash
  python3 scripts/qa/resources/_qa_react_button.py split-button
  ```
- `_qa_template.py` — generic template harness (works for Tailwind/Vanilla templates too); takes a `preview.html` path and loads it over `file://` (no server needed).
- `test_tailwind_nav.py` / `test_react_nav.py` — the gallery/browse pages; serve `library/` on `:12000` first.

Harnesses exist for most — not all — families. Check the directory before assuming one exists.

## Common failure classes and fixes

| Message | Meaning | Fix |
|---|---|---|
| `VALIDATION FAILED - N problem(s):` | Any of the layers above | Read the listed paths; fix the content, not the validator |
| `indexed variant missing on disk` / `on-disk leaf not indexed` | Leaf added/renamed without regenerating | Run `rebuild_index.py` |
| `type=section outside Sections/` | Resource moved without updating metadata `type` | Update that leaf's `metadata.json` |
| `Tailwind component missing README.md` | Missing or empty README | Add/complete it |
| `Architecture: unexpected dir` | New top-level dir under a tech tree | Remove it or justify a schema change |
| `Template … is missing AGENTS.md` | New template without agent instructions | Add a non-empty one |
| `FAIL <path> <check>` (reduced-motion/focus-visible/…) | Vanilla quality bar | Fix the component |
| `Duplicate id within one technology/type` | Two leaves in the same tech/type/subcategory share an `id` | Give one a unique `id`/`slug`; cross-tech echoes are only a NOTE |
| `NOT writing index due to validation problems` | Disk and registry disagree | Fix the listed problems, re-run — this is a failure, not a no-op |
| `npm test` failure in `cli/` | CLI behavior regressed | Read the failing suite (`cli/test/*.test.js`) |

## The fix procedure

```text
1. Run the failing command and read the raw error text.
2. Locate the producing code:
   validate.py messages            → scripts/tooling/validators/validate.py
   "NOT writing index …"           → scripts/tooling/indexing/rebuild_index.py
   CLI error text                  → cli/src/utils/errors.js
   quality-bar FAIL lines          → scripts/qa/resources/qa_vanilla.py
3. Inspect the offending artifact.
4. Fix the cause — never silence a validator to make a change pass.
5. Re-run the full command matrix for your scope before reporting success.
```

If a failure is pre-existing and unrelated to your change, report it in the PR instead of fixing unrelated content.

## Standard verification sequence after a change

```text
1. rebuild_index.py        (only if leaves were added/removed/renamed or metadata changed)
2. validate.py             (must print VALIDATION PASSED, exit 0 — includes the file-set layer)
3. deep_check.py           (optional focused file-set report)
4. scripts/tooling/tests   (validator/indexer changes)
5. qa_vanilla.py           (Vanilla changes)
6. cd cli; npm test        (cli/ changes)
7. relevant browser harness (visual/interactive changes)
8. Report exact commands + observed results — not a general claim of success
```

## Go deeper

This page is the human-facing QA reference. The implementation-anchored reference (the exact check functions, the deliberate duplicate-ID policy, and the per-harness invocation contracts) is maintained for agents in [`agents/resources/qa.md`](https://github.com/sarthakbystander/DevSnips/blob/main/agents/resources/qa.md).

