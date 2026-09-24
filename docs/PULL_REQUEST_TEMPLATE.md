## 🚀 Pull Request Summary

### What does this PR change?
<!-- Describe the snippet(s) or documentation updates in 2-4 bullets. -->

### Related issue
Closes #<issue-number> (if applicable)

## ✅ PR Checklist

- [ ] My snippet(s) include the standard comment header.
- [ ] I followed project formatting and code style rules.
- [ ] For templates, I added/updated the template-specific `AGENTS.md` agent instructions.
- [ ] I reviewed snippet accessibility (semantic HTML + ARIA where needed).
- [ ] I tested in multiple browsers.
- [ ] I updated `snippets-index.json` for added/removed snippets.
- [ ] I added/updated documentation where necessary.

## 🧪 Validation

The authoritative template is [`.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/sarthakbystander/DevSnips/blob/main/.github/PULL_REQUEST_TEMPLATE.md). Run the gates that apply to your change:

```bash
# Always:
python scripts/tooling/validators/validate.py

# When library/ content or resource metadata changed:
python scripts/tooling/indexing/rebuild_index.py
python scripts/tooling/indexing/validate_indexes.py

# When Markdown changed or referenced files moved:
python scripts/tooling/validators/check_md_links.py
python scripts/tooling/validators/check_agent_doc_paths.py

# When cli/ changed:
cd cli && npm test
```

- [ ] `validate.py` prints `VALIDATION PASSED` (exit 0).
- [ ] `snippets-index.json` regenerated when `library/` content changed.
- [ ] Relevant checks above pass.

## 📸 Screenshots / Preview

<!-- Optional for visual changes: include screenshots or a demo link. -->
