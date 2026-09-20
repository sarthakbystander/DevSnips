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
   - **VERIFIED:** There is currently no automated GitHub Actions workflow file (`.github/workflows/`) enforcing validation on push/PR. Developers must run validation and indexing scripts manually.

## Recommendations

1. **Launch-Critical:** Add a basic GitHub Actions CI workflow to automate running `python scripts/tooling/validators/validate.py` and `python scripts/tooling/indexing/validate_indexes.py` on pull requests and pushes.
2. **Post-Launch:** Consolidate standalone supplementary checkers like `deep_check.py` into `validate.py` or archive them alongside historical migration utilities.
