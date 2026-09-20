# Contributing — validation and QA

There is **no CI** in this repository (`.github/` contains only the PR template). Every check runs only when a human or agent runs it. A pull request must state which commands were run and what they printed.

## The command matrix

| Scope | Command | Passing condition |
|---|---|---|
| Always (minimum bar) | `python scripts/tooling/validators/validate.py` | Prints `VALIDATION PASSED - architecture, metadata, and index all consistent.`, exit 0 |
| File-set changes | `python scripts/tooling/validators/deep_check.py` | No failures reported |
| Any content added/removed/renamed | `python scripts/tooling/indexing/rebuild_index.py` | Prints `Wrote snippets-index.json` — not `NOT writing index due to validation problems` |
| After index regeneration | `python scripts/tooling/indexing/validate_indexes.py` | Exit 0 (indexes match the repository) |
| Vanilla component changes | `python scripts/qa/resources/qa_vanilla.py --only-failures` | `failing required checks: 0` |
| CLI changes | `cd cli && npm test` | All suites pass |
| Visual/interactive changes | Relevant Playwright harness under `scripts/qa/resources/` | No console errors, no horizontal overflow at mobile width |

Python scripts resolve the repository root from their own file location, so the working directory does not matter. Playwright is not declared in any manifest — install it in your environment before running browser harnesses.

## What `validate.py` checks

| Layer | Covers |
|---|---|
| Architecture | Each tech dir may contain only `Components`, `Sections`, `Templates`; `Utilities`/`Resources`/`Snippets`/`Pages`/`Tools` are forbidden anywhere under a tech |
| Metadata validity | JSON parses; `type` present, lowercase vocabulary, matches folder bucket; required files per tech (Tailwind Comp/Sec: `code.html` + `preview.html`; Tailwind components: non-empty `README.md`; React Comp/Sec: `code.tsx` + `preview.html`) |
| Index ↔ disk | Two-way coverage, duplicate paths, stale paths |
| Template `AGENTS.md` | Exists and non-empty for every template |
| Vanilla quality bar | `qa_vanilla.py` runs inside `validate.py`; a required-check failure fails validation |
| Duplicate IDs | Reported as a NOTE, not a failure (deliberate, so pre-existing IDs are preserved). Do not "fix" duplicates as a side effect |

`deep_check.py` is a standalone, stricter file-set checker (per-tech required/optional files; React section README absence is fine, empty README anywhere is a failure; missing React `code.jsx` is a warning only).

## What `qa_vanilla.py` checks

Per Vanilla component: accessibility and interaction semantics (keyboard operability, focus visibility, ARIA on custom widgets), reduced-motion guards on animations, dark-mode support. Flags: `--only-failures`, `--json`, and advisory `--tokens` (`--ds-*` adoption vs raw hex; always exits 0). It scans the Components tree; Sections/Templates are governed by their own specs.

## Browser QA harnesses

Per-family Playwright scripts under `scripts/qa/resources/`: `_qa_react_*.py` (component/section families), `_qa_template.py` (generic template harness, works for Tailwind/Vanilla templates too), `test_tailwind_nav.py` / `test_react_nav.py` (gallery pages). React harnesses serve `preview.html` at `http://localhost:8765` and are invoked per slug, e.g.:

```bash
python3 scripts/qa/resources/_qa_react_button.py split-button
```

Harnesses exist for most — not all — families. Check the directory before assuming one exists.

## Common failure classes and fixes

| Message | Meaning | Fix |
|---|---|---|
| `VALIDATION FAILED - N problem(s):` | Any of the layers above | Read the listed paths; fix the content, not the validator |
| `type=section outside Sections/` | Resource moved without updating metadata `type` | Update that leaf's `metadata.json` |
| `Tailwind component missing README.md` | Missing or empty README | Add/complete it |
| `Architecture: unexpected dir` | New top-level dir under a tech tree | Remove it or justify a schema change |
| `Template … is missing AGENTS.md` | New template without agent instructions | Add a non-empty one |
| `FAIL <path> <check>` (reduced-motion/focus-visible/…) | Vanilla quality bar | Fix the component |
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
2. validate.py             (must print VALIDATION PASSED, exit 0)
3. deep_check.py           (file-set changes)
4. qa_vanilla.py           (Vanilla changes)
5. cd cli; npm test        (cli/ changes)
6. relevant browser harness(visual/interactive changes)
7. Report exact commands + observed results — not a general claim of success
```
