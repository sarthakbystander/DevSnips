# Pull request template

The canonical template lives at
[`../.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md);
GitHub loads it automatically when a pull request is opened. Use that file
rather than duplicating it here.

In short, run the gates that apply to your change:

```bash
# Always:
python scripts/tooling/validators/validate.py        # must print VALIDATION PASSED

# When library/ content or resource metadata changed:
python scripts/tooling/indexing/rebuild_index.py
python scripts/tooling/indexing/validate_indexes.py

# When Markdown changed or referenced files moved:
python scripts/tooling/validators/check_md_links.py
python scripts/tooling/validators/check_agent_doc_paths.py

# When cli/ changed:
cd cli && npm test
```

See [`contributing/overview.md`](contributing/overview.md) for the contributor
checklist and [`contributing/validation.md`](contributing/validation.md) for
what each gate covers.
