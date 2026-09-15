# Audit & Validate Repository Structure

## 🎯 Objective
Enforce consistent required file sets across all Components, Sections, and Templates for each technology (Tailwind, Vanilla, React). Ensure the index matches disk state exactly and all validation checks pass.

## 📋 Changes Made

### New Scripts Created

#### 1. `scripts/deep_check.py`
- **Purpose:** Deep-check enforcing required file sets per tech for Components and Sections
- **Checks:**
  - Tailwind Components/Sections: `code.html`, `preview.html`, `metadata.json`, `README.md`
  - React Components/Sections: `code.tsx`, `preview.html`, `metadata.json`, `README.md` + `code.jsx` parity
  - Vanilla Components/Sections: `metadata.json` (code files vary)
  - All Templates: `AGENTS.md`, `preview.html` or `pages/*`, `metadata.json`, `README.md`

#### 2. `scripts/_gen_react_sections_readme.py`
- **Purpose:** Generate missing README.md files for React Sections
- **Output:** ~56 README.md files with template structure from metadata
- **Supports:** `--check` mode for CI/CD validation

#### 3. `scripts/_gen_tailwind_sections_readme.py`
- **Purpose:** Generate missing README.md files for Tailwind Sections
- **Output:** ~50 README.md files with template structure from metadata
- **Supports:** `--check` mode for CI/CD validation

### Documentation Added

- **`AUDIT_EXECUTION_PLAN.md`** - Complete execution workflow, validation rules, and troubleshooting guide

## ✅ Validation Checklist

Before merging, run the following commands to verify all checks pass:

### Phase 1: Deep Check
```bash
python3 scripts/deep_check.py
```
**Expected:** ✅ DEEP CHECK PASSED - all required file sets present

### Phase 2: Generate Missing README Files
```bash
# React Sections
python3 scripts/_gen_react_sections_readme.py

# Tailwind Sections
python3 scripts/_gen_tailwind_sections_readme.py
```
**Expected:** Successfully generated ~106 README.md files (56 React + 50 Tailwind)

### Phase 3: Rebuild Index
```bash
python3 -m _gen.rebuild_index
```
**Expected:** 
- Validation: OK (indexed content matches disk exactly)
- All families, variants, and styles accounted for
- stats updated correctly

### Phase 4: Full Validation
```bash
python3 scripts/validate.py
```
**Expected:** ✅ VALIDATION PASSED - architecture, metadata, and index all consistent

## 🔍 What Gets Validated

### Architecture
- ✅ Only `Components/`, `Sections/`, `Templates/` directories per tech
- ✅ No forbidden `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, `Tools/` directories
- ✅ React/Sections/ is first-class content type

### Content Integrity
- ✅ Every component/section leaf has complete required file set per tech
- ✅ No orphaned metadata.json without sibling files
- ✅ All metadata.json files are valid JSON

### Index Consistency
- ✅ Every indexed variant path exists on disk with metadata.json
- ✅ Every on-disk leaf is indexed
- ✅ No duplicate variant paths
- ✅ No stale /Utilities/ or /Resources/ path references

### Metadata Quality
- ✅ Every entry has valid `type` field (component/section/template)
- ✅ Type matches content-type bucket location
- ✅ No invalid metadata entries

### Template Requirements
- ✅ Every template directory has AGENTS.md with agent instructions
- ✅ AGENTS.md is not empty
- ✅ Templates have preview.html or pages/* structure

## 📊 Expected Metrics After Merge

```
Deep Check:        1 script (core validation)
README Generators: 2 scripts (~106 files to generate)
QA Scripts:        12 React section scripts (updated for 5-file shape)
Total Families:    116
Total Variants:    1018
Total Styles:      1854
```

## 🔗 Related Documentation

- [`AUDIT_EXECUTION_PLAN.md`](./AUDIT_EXECUTION_PLAN.md) - Full execution workflow and troubleshooting
- [`scripts/validate.py`](./scripts/validate.py) - Main validation entry point
- [`_gen/rebuild_index.py`](./_gen/rebuild_index.py) - Index rebuild logic
- [`scripts/deep_check.py`](./scripts/deep_check.py) - Deep check implementation

## 🚀 Deployment Notes

### Manual Execution Required
1. Run `python3 scripts/_gen_react_sections_readme.py` to generate React Section READMEs
2. Run `python3 scripts/_gen_tailwind_sections_readme.py` to generate Tailwind Section READMEs
3. Run `python3 -m _gen.rebuild_index` to regenerate the index
4. Run `python3 scripts/validate.py` to confirm all checks pass
5. Commit the generated files and updated index

### CI/CD Integration
All generators support `--check` mode for automated validation:
- `python3 scripts/_gen_react_sections_readme.py --check`
- `python3 scripts/_gen_tailwind_sections_readme.py --check`
- `python3 scripts/validate.py` (exit code 1 on failure)
- `python3 scripts/deep_check.py` (exit code 1 on failure)

## 📝 Commit Structure

After generation, expect commits for:
1. Generated README.md files for React Sections (~56)
2. Generated README.md files for Tailwind Sections (~50)
3. Updated `snippets-index.json` with latest content
4. Any required file fixes identified by deep_check.py

## ⚠️ Important Notes

- Pre-existing duplicate IDs are preserved (per rule #9 of migration spec)
- Hand-curated family-level descriptions are carried forward from previous index
- Variant-level curated data (tags, features, styles) preserved via path matching
- All generators are idempotent (safe to run multiple times)

## 🎓 Testing Locally

To verify everything works before merge:

```bash
# Full validation pipeline
python3 scripts/deep_check.py && \
python3 scripts/_gen_react_sections_readme.py --check && \
python3 scripts/_gen_tailwind_sections_readme.py --check && \
python3 -m _gen.rebuild_index && \
python3 scripts/validate.py
```

If all commands exit with code 0, the PR is ready to merge.

---

**Branch:** `chore/audit-and-validate-repo-structure`
**Type:** Chore (infrastructure)
**Size:** 3 new scripts + 1 documentation file
**Impact:** Establishes validation foundation for production-ready component library
