# DevSnips Repository Audit & Validation Execution Plan

## Overview
This document outlines the complete audit, validation, and regeneration workflow to ensure all DevSnips components, sections, and templates meet the production-ready spec.

## Architecture
```
Vanilla/     → Components/ + Sections/ + Templates/
Tailwind/    → Components/ + Sections/ + Templates/
React/       → Components/ + Sections/ + Templates/
```

Each technology has three first-class content types, each content type is organized by family, and each family contains one or more variants.

## New Scripts Created

### 1. `scripts/deep_check.py`
**Purpose:** Deep-check script enforcing required file sets per tech for Components and Sections.

**Requirements by Tech:**
- **Tailwind Components/Sections:** `code.html`, `preview.html`, `metadata.json`, `README.md`
- **React Components/Sections:** `code.tsx`, `preview.html`, `metadata.json`, `README.md` (+ `code.jsx` parity for Components)
- **Vanilla Components/Sections:** `metadata.json` (code files vary by design)
- **All Templates:** `AGENTS.md` (template-specific instructions for AI agents), `preview.html` or `pages/*`, `metadata.json`, `README.md`

**Run:**
```bash
python3 scripts/deep_check.py
```

### 2. `scripts/_gen_react_sections_readme.py`
**Purpose:** Generate missing README.md files for React Sections.

**Features:**
- Scans `React/Sections/` for variant folders
- Generates README.md with template structure matching metadata
- Supports `--check` mode to validate without generation

**Run:**
```bash
# Generate all missing README.md files
python3 scripts/_gen_react_sections_readme.py

# Check mode (validation only)
python3 scripts/_gen_react_sections_readme.py --check
```

### 3. `scripts/_gen_tailwind_sections_readme.py`
**Purpose:** Generate missing README.md files for Tailwind Sections.

**Features:**
- Scans `Tailwind/Sections/` for variant folders
- Generates README.md with template structure matching metadata
- Supports `--check` mode to validate without generation

**Run:**
```bash
# Generate all missing README.md files
python3 scripts/_gen_tailwind_sections_readme.py

# Check mode (validation only)
python3 scripts/_gen_tailwind_sections_readme.py --check
```

## Execution Workflow

### Phase 1: Audit Current State
1. Run deep_check.py to identify missing files:
   ```bash
   python3 scripts/deep_check.py
   ```
2. Review any errors or warnings
3. Note gaps in required file sets

### Phase 2: Generate Missing README Files
1. Generate React Sections README files:
   ```bash
   python3 scripts/_gen_react_sections_readme.py
   ```
2. Generate Tailwind Sections README files:
   ```bash
   python3 scripts/_gen_tailwind_sections_readme.py
   ```
3. Verify generation output

### Phase 3: Update QA Scripts
The QA scripts (_qa_react_*.py) have been updated to enforce the 5-file shape for React sections:
- `code.tsx` (primary source)
- `code.jsx` (parity file for components, validation checks existence)
- `preview.html` (preview)
- `metadata.json` (metadata)
- `README.md` (documentation)

QA scripts also validate:
- README.md is not empty
- code.jsx exists for components (warning if missing)
- All metadata fields are valid

### Phase 4: Rebuild Index
1. Run index rebuild:
   ```bash
   python3 -m _gen.rebuild_index
   ```
2. The rebuild script will:
   - Scan all content-type trees on disk
   - Preserve curated family-level data from previous index
   - Detect all new leaves (components, sections, templates)
   - Cross-validate: every indexed variant must exist on disk
   - Recompute stats and per-tech breakdown
   - Output validation results

### Phase 5: Full Validation
Run the complete validation suite:
```bash
python3 scripts/validate.py
```

This runs:
1. Architecture checks
2. Metadata validity checks
3. Index vs. disk cross-checks
4. Template AGENTS.md checks
5. Vanilla quality-bar scan

### Phase 6: Verification Checklist

- [ ] `scripts/deep_check.py` passes with no errors
- [ ] `scripts/_gen_react_sections_readme.py --check` passes
- [ ] `scripts/_gen_tailwind_sections_readme.py --check` passes
- [ ] `python3 -m _gen.rebuild_index` completes with no validation problems
- [ ] `python3 scripts/validate.py` passes
- [ ] All generated README.md files are non-empty and descriptive
- [ ] snippets-index.json is updated with latest content
- [ ] Index stats reflect all families and variants

## Key Validation Rules

### Architecture
- ✅ Only Components/, Sections/, Templates/ directories allowed per tech
- ✅ No standalone Utilities/, Resources/, Snippets/, Pages/, Tools/ directories
- ✅ React/Sections/ is first-class content type (not forbidden)

### Content Leaves
- ✅ Every component/section leaf must have metadata.json
- ✅ No orphaned metadata.json (metadata without expected sibling files)
- ✅ No duplicate IDs (pre-existing duplicates preserved per rule #9)

### Index Consistency
- ✅ Every indexed variant path exists on disk
- ✅ Every on-disk leaf is indexed
- ✅ No duplicate variant paths in index
- ✅ No stale Sections/Utilities/Resources path references

### Metadata
- ✅ Every entry carries valid `type` (component/section/template)
- ✅ Type matches content-type bucket location
- ✅ All required files present per tech

### Templates
- ✅ Every template ships AGENTS.md with agent instructions
- ✅ AGENTS.md is not empty
- ✅ Templates have preview.html or pages/* structure

## Expected Outcomes

After successful execution:

1. **File Inventory:**
   - ~56 React Sections README.md files (generated)
   - ~50 Tailwind Sections README.md files (generated)
   - All Components and Sections have complete file sets per tech

2. **Index Updates:**
   - snippets-index.json regenerated with latest content
   - Stats updated: families, variants, styles per tech
   - Variant file manifests updated

3. **Validation Passes:**
   - deep_check.py: ✅ PASSED
   - validate.py: ✅ PASSED
   - rebuild_index.py validation: ✅ PASSED

4. **PR Ready:**
   - All changes committed to branch
   - PR template includes execution details
   - Ready for review and merge

## Troubleshooting

### If deep_check.py fails:
- Check error messages for missing files
- Verify file paths match tech-specific requirements
- Use `ls -la` to inspect actual directory contents

### If index rebuild fails:
- Ensure all leaves have valid metadata.json
- Check for duplicate family paths
- Verify all indexed variants exist on disk

### If validate.py fails:
- Run individual check functions to isolate issues
- Review qa_vanilla.py output for quality-bar failures
- Verify no stale path references in index

## Related Files

- `scripts/validate.py` - Main validation entry point
- `_gen/rebuild_index.py` - Index rebuild script
- `scripts/qa_vanilla.py` - Vanilla quality-bar scanner
- `scripts/_qa_react_*.py` - React QA scripts (12 per section family)
- `snippets-index.json` - Generated index (source of truth for public API)

## Notes

- All generators support `--check` mode for CI/CD validation
- Pre-existing duplicate IDs are preserved (rule #9)
- Hand-curated family-level descriptions preserved from previous index
- Variant-level curated data (tags, features, styles) carried forward
