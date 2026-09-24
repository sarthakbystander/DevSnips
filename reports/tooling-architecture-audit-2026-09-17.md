# Tooling and Script Architecture Audit

- **Date:** 2026-09-17
- **Scope:** `scripts/` directory, indexing system, validation harnesses, and tooling generators.
- **Objective:** Map the existing automation architecture, evaluate script redundancy, identify gaps, and determine launch readiness.

## Files Inspected

- `scripts/tooling/validators/validate.py`
- `scripts/tooling/validators/deep_check.py`
- `scripts/tooling/indexing/rebuild_index.py`
- `scripts/tooling/indexing/build_resource_indexes.py`
- `scripts/tooling/indexing/validate_indexes.py`
- `scripts/qa/resources/qa_vanilla.py`
- All active generator scripts under `scripts/tooling/generators/` and utility scripts under `scripts/tooling/utilities/`.

## Findings & Status Verification

1. **Active vs. Historical Scripts:**
   - **VERIFIED:** Core active tooling (`rebuild_index.py`, `build_resource_indexes.py`, `validate_indexes.py`, `validate.py`, `qa_vanilla.py`) forms the complete pipeline for indexing, validation, and QA.
   - **VERIFIED:** Scripts under `scripts/tooling/utilities/` (e.g., `fix_duplicate_ids.py`, `migrate_vanilla.py`) are historical one-off migration utilities and are not part of the active CI/development loop.

2. **Validation Architecture:**
   - **VERIFIED:** `scripts/tooling/validators/validate.py` serves as the primary comprehensive validator entrypoint, covering architecture, metadata correctness, file contracts, index synchronization, and invoking the Vanilla QA scanner.
   - **VERIFIED:** `deep_check.py` provides supplementary checks but overlaps in scope with `validate.py`.

3. **Indexing System:**
   - **VERIFIED:** `rebuild_index.py` builds the master `snippets-index.json` by scanning `library/`, which is then consumed by `build_resource_indexes.py` to generate AI-agent sub-indexes under `agents/resources/indexes/`.

4. **CI / Automation:**
   - **SUPERSEDED (2026-09-24):** No GitHub Actions workflow existed at audit time. `.github/workflows/ci.yml` now enforces validation and indexing on push/PR; see Follow-up status below.

## Recommendations

1. **Launch-Critical:** Add a basic GitHub Actions CI workflow to automate running `python scripts/tooling/validators/validate.py` and `python scripts/tooling/indexing/validate_indexes.py` on pull requests and pushes.
2. **Post-Launch:** Consolidate standalone supplementary checkers like `deep_check.py` into `validate.py` or archive them alongside historical migration utilities.

## Follow-up status (2026-09-24)

1. **Done.** `.github/workflows/ci.yml` runs `validate.py`, the Python tooling unit tests
   (`scripts/tooling/tests/`), `rebuild_index.py --check`, `validate_indexes.py`,
   `check_md_links.py`, `check_agent_doc_paths.py`, and `cli` `npm test` on every push to
   `main` and every pull request.
2. **Done.** `deep_check.py`'s `collect()` is merged into `validate.py`'s `main()` via
   `_run_deep_check()`, so a `validate.py` pass covers the strict file-set layer; the script
   remains runnable standalone for a focused report. The duplicate-ID policy was also scoped:
   collisions within one technology/type/subcategory fail, while cross-technology id echoes are
   informational NOTES (the registry keys on the tech-first path).
