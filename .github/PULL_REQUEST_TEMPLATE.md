# DevSnips Pull Request

## Summary

<!-- What changed and why. Include the affected technology (React / Tailwind / Vanilla)
     and content type (Components / Sections / Templates) when relevant. -->

## Change type

- [ ] Library content (new / modified / removed resource under `library/`)
- [ ] Tooling (`scripts/`)
- [ ] CLI (`cli/`)
- [ ] Agent docs / indexes (`agents/`, `snippets-index.json`)
- [ ] Human docs (`docs/`, `README.md`)
- [ ] Website (`website/` — regenerated artifacts only)

## Validation

Run the gates that apply to your change (see `agents/resources/qa.md`):

```bash
# Always:
python scripts/tooling/validators/validate.py

# When per-tech required-file sets are in play:
python scripts/tooling/validators/deep_check.py

# When Markdown changed, or files it references were moved/renamed:
python scripts/tooling/validators/check_md_links.py
python scripts/tooling/validators/check_agent_doc_paths.py

# When library/ content or resource metadata changed — regenerate, then verify:
python scripts/tooling/indexing/rebuild_index.py
python scripts/tooling/indexing/validate_indexes.py

# When cli/ changed:
npm test   # run from cli/
```

Checklist:

- [ ] `validate.py` exits 0 and prints `VALIDATION PASSED`.
- [ ] `rebuild_index.py` was run if any resource was added, removed, renamed, or moved;
      it printed `Validation: OK (indexed content matches disk exactly)` and **never**
      `NOT writing index due to validation problems`.
- [ ] `deep_check.py` passes if required-file sets were touched.
- [ ] `check_md_links.py` and `check_agent_doc_paths.py` pass if Markdown changed or
      referenced files were moved/renamed.
- [ ] No generated file was hand-edited (`snippets-index.json` and
      `agents/resources/indexes/*.json` are script outputs — regenerate, don't patch).
- [ ] For visual/interactive changes: the relevant harness under
      `scripts/qa/resources/` was run; zero console errors and no horizontal overflow
      at mobile width. React harnesses expect a static server rooted at `library/`
      on :8765 (e.g. `python3 -m http.server 8765 --directory library`).
- [ ] `snippets-index.json` regenerated when `library/` content changed.

## Notes

<!-- Known limitations, pre-existing issues observed (report them; do not fix unrelated
     issues silently), screenshots / preview links for visual changes. -->
