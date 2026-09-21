# Author a resource

Create a new DevSnips resource that passes validation and lands in the registry. This tutorial walks through adding a component; sections and templates follow the same shape with their own file contracts (see [Resource structure](../resources/resource-structure.md)).

## 1. Choose the technology and type

Pick the technology that matches the implementation and the type that matches the intent — do not upscale a component into a template. See [Resource model](../resources/overview.md).

## 2. Create the leaf folder

Create `library/<Tech>/<Category>/<Family>/<kebab-slug>/`. The **folder name is the canonical slug**. Never create `Utilities/`, `Resources/`, `Snippets/`, `Pages/`, or `Tools/` — `validate.py` rejects them.

Example: `library/Vanilla/Components/Buttons/multi-action-button/`.

## 3. Add the required files

File contract by tech + type (full table in [Resource structure](../resources/resource-structure.md)):

- **Vanilla component:** `metadata.json` (required) + the universal convention `code.html` + `README.md`.
- **Tailwind component:** `code.html`, `preview.html`, `metadata.json`, non-empty `README.md`.
- **React component:** `code.tsx`, `preview.html`, `metadata.json`, `README.md` (`code.jsx` optional parity build).
- **Template (any tech):** `metadata.json`, non-empty `AGENTS.md`, `preview.html` **or** non-empty `pages/`, plus `README.md`.

Self-containment rules: Vanilla components carry inline `<style>` + `<script>` with `--ds-*` token fallbacks; Tailwind snippets are markup + scoped JS only; React components export one primary component with internal or prop-driven state.

## 4. Write metadata.json

**The schema is not uniform across technologies.** Copy the exact shape of a sibling in the same family — do not invent fields. Required in every tech: a `type` that matches the folder bucket (`component`/`section`/`template`). See [Metadata](../machine-readable/metadata.md) for the per-tech field reference.

## 5. Regenerate and validate

```bash
python scripts/tooling/indexing/rebuild_index.py
python scripts/tooling/indexing/validate_indexes.py
python scripts/tooling/validators/validate.py
```

`rebuild_index.py` printing `NOT writing index due to validation problems` is a **failure** — read the listed problems, fix the content, re-run. `validate.py` must print `VALIDATION PASSED`.

For Vanilla components, also run `python scripts/qa/resources/qa_vanilla.py` and confirm `failing required checks: 0`.

## 6. Preview and review

Open the resource's `preview.html` in a browser. Confirm it renders standalone, is responsive (no horizontal overflow at mobile width), and respects `prefers-reduced-motion`. If it is interactive, run the matching browser harness under `scripts/qa/resources/` — see [QA](../qa/overview.md).

## Go deeper

- [Creating resources](../contributing/creating-resources.md) — the full contributor procedure.
- [Validation](../contributing/validation.md) — the command matrix and fix procedure.
- [Resource structure](../resources/resource-structure.md) — exact per-tech file contracts.
