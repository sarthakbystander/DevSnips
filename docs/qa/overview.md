# QA — overview

CI (`.github/workflows/ci.yml`) covers the static gates — structure/metadata validation, index drift, index validation, documentation link/path checks, and the CLI tests. The browser QA layers are still locally-run gates. This page maps every layer, where it lives, and how to run it. For the fix procedure and the per-change command matrix see [Validation](../contributing/validation.md); this page is the structural map of the QA *surface*.

```text
scripts/qa/
  resources/
    qa_vanilla.py          Vanilla quality-bar scanner (static)
    test_react_nav.py      React gallery nav (Playwright)
    test_tailwind_nav.py   Tailwind gallery nav (Playwright)
    _qa_react_*.py         per-family React browser harnesses (Playwright)
    _qa_template.py        generic multi-page template harness (Playwright)
```

## The layers at a glance

| Layer | Tool | Where it lives | Required for |
|---|---|---|---|
| Repository validator | `validators/validate.py` | `scripts/tooling/validators/` | every push |
| File-set checker | `validators/deep_check.py` | `scripts/tooling/validators/` | file-set changes |
| Markdown link checker | `validators/check_md_links.py` | `scripts/tooling/validators/` | Markdown edits / file moves |
| Agent-doc path checker | `validators/check_agent_doc_paths.py` | `scripts/tooling/validators/` | agent-facing docs (`agents/resources/`, `library/**/AGENTS.md`, MCP) |
| Python tooling tests | `scripts/tooling/tests/` (`unittest`) | `scripts/tooling/tests/` | validator/indexer changes |
| Master index drift | `indexing/rebuild_index.py --check` | `scripts/tooling/indexing/` | every push |
| Specialized index validation | `indexing/validate_indexes.py` | `scripts/tooling/indexing/` | index changes |
| Vanilla quality bar | `qa_vanilla.py` | `scripts/qa/resources/` | Vanilla component changes |
| React browser QA | `_qa_react_*.py` | `scripts/qa/resources/` | visual/interactive React changes |
| Template browser QA | `_qa_template.py` | `scripts/qa/resources/` | template changes |
| Nav/gallery QA | `test_react_nav.py`, `test_tailwind_nav.py` | `scripts/qa/resources/` | gallery page changes |
| CLI behavior | `cli/test/*.test.js` | `cli/test/` | CLI changes |

## Static scanner: `qa_vanilla.py`

Pure-Python (no node/npm), safe for CI. Measures every Vanilla component against a documented quality bar and prints an actionable report; exits `1` when any **required** check fails for an interactive component, `0` otherwise.

Checks per component `.html`:

| Code | Check | Required? |
|---|---|---|
| R1 doctype | full `<!DOCTYPE html>` document, or a clearly marked snippet fragment (both acceptable; flagged for the record) | no (warn) |
| R2 lang | `<html lang>` set when a DOCTYPE is present | when a DOCTYPE is present |
| R3 viewport | viewport meta set when a DOCTYPE is present | when a DOCTYPE is present |
| A1 reduced-motion | animations guarded by `prefers-reduced-motion` | when the file animates |
| A2 aria/role | interactive components use role/aria-* semantics (native semantic elements satisfy this) | interactive families |
| A3 focus-visible | `:focus-visible` (or a focus-visible ring) present | interactive families |
| A4 keyboard | interactive controls are `<button>`/`<a>` or carry `tabindex`/`role="button"` | interactive families that wire JS interaction |
| A5 semantic | uses semantic landmarks (`main`/`nav`/`section`/`header`/…) | no (warn) |

The script also computes dark-mode support (`prefers-color-scheme`), but that is currently an
informational value, not an emitted pass/fail check.

**"Interactive" families** (where A1–A4 are *required*): Modals, Dropdowns, Tabs, Accordions, Navigation, Tooltips, Buttons, Forms, Loaders. Purely visual families (Cards, Hero, Marketing, Testimonials, Stats, …) still need reduced-motion when they animate, but not ARIA/keyboard. A failure in a required check is what fails the gate.

```bash
python3 scripts/qa/resources/qa_vanilla.py            # report + exit code
python3 scripts/qa/resources/qa_vanilla.py --json     # machine-readable report
```

It scans `library/Vanilla/Components` and `library/Vanilla/Sections`. It runs **inside** `validate.py`, so a required-check failure fails overall validation. Related autofix: `scripts/tooling/utilities/fix_quality_bar.py`.

## Browser harnesses (Playwright)

Per-family Playwright scripts under `scripts/qa/resources/`. Playwright is **not** declared in any manifest in this repository — install it in your environment before running these.

| Harness | Scope | Invocation |
|---|---|---|
| `_qa_react_*.py` | one React component/section family | serve `library/` on `:8765` (`python3 -m http.server 8765 --directory library`), then e.g. `python3 scripts/qa/resources/_qa_react_button.py split-button` |
| `_qa_template.py` | a multi-page template (Tailwind/Vanilla too) | `python3 scripts/qa/resources/_qa_template.py <path-to-preview.html>` (loads it over `file://`) |
| `test_react_nav.py` | the React gallery/browse page | serve `library/` on `:12000`, then `python3 scripts/qa/resources/test_react_nav.py` |
| `test_tailwind_nav.py` | the Tailwind gallery/browse page | serve `library/` on `:12000`, then `python3 scripts/qa/resources/test_tailwind_nav.py` |

The React and nav harnesses navigate to `http://localhost:<port>/<Tech>/...`, so the document root must be `library/` (the index paths are tech-first, without the `library/` prefix). `_qa_template.py` instead opens the preview over `file://` and needs no server.

### How the React harnesses work

Each `_qa_react_*.py` loads the family's `preview.html` from a static server you run on `:8765` (document root `library/`), drives a real browser, and asserts:

- **runtime** — the component mounts with no console errors;
- **layout** — no horizontal overflow at mobile widths;
- **theme** — dark/light switching where applicable;
- **accessibility** — focus, keyboard, ARIA on interactive controls.

Harnesses exist for most — not all — families. Check the directory before assuming one exists; do not invent a harness name.

### Reading the output

A harness prints `PASS`/`FAIL` per check and per viewport. `FAIL` lines name the resource and the failing check (e.g. `reduced-motion`, `focus-visible`, horizontal overflow). Treat any `FAIL` as a defect in the resource — fix the content, not the harness.

## CLI behavior tests

`cli/test/*.test.js` (run with `npm test` from `cli/`) cover path handling, file selection, config/context behavior, and `init`. They use `node:assert` + `os.tmpdir()` sandboxes — no framework, no network. See [CLI](../cli/overview.md#tests).

## The minimal per-change QA sequence

```text
1. rebuild_index.py        (if leaves added/removed/renamed or metadata changed)
2. validate.py             (must print VALIDATION PASSED, exit 0 — includes the file-set layer)
3. deep_check.py           (optional focused file-set report)
4. check_md_links.py       (Markdown edits / file moves)
5. check_agent_doc_paths.py (agents/resources + library AGENTS.md edits)
6. validate_indexes.py     (index regeneration)
7. scripts/tooling/tests   (validator/indexer changes)
8. qa_vanilla.py           (Vanilla changes)
9. cd cli; npm test        (cli/ changes)
10. relevant browser harness(visual/interactive changes)
11. report exact commands + observed results

Steps 1-9 run in CI (plus the tooling-test suite); run them locally first so a push does not fail.
```

`rebuild_index.py` printing `NOT writing index due to validation problems` is a **failure**, not a no-op.

## Go deeper

This page is the human-facing QA map. The implementation-anchored reference (per-check code locations, the interactive-family list, the exact harness invocation contracts) is maintained for agents in [`agents/resources/qa.md`](https://github.com/sarthakbystander/DevSnips/blob/main/agents/resources/qa.md).

## Related

- [Validation](../contributing/validation.md) — the command matrix and the fix procedure.
- [Tooling](../tooling/overview.md) — the validators/indexing/generators/utilities these gates call into.
