# snippets-index.json — registry reference

Authoritative source (always fetch current, never assume from memory):
https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json

## Top-level shape

```json
{
  "totalFamilies": <int>,
  "totalVariants": <int>,
  "totalStyles": <int>,
  "stats": {
    "tailwindByType": { "component": <int>, "section": <int>, "template": <int> },
    "vanillaByType":  { "component": <int>, "section": <int>, "template": <int> }
  },
  "technologies": [
    { "name": "Tailwind CSS", "families": ["Accordions", "Buttons", "..."] },
    { "name": "Vanilla",      "families": ["..."] },
    { "name": "React",        "families": ["..."] }
  ],
  "families": [ /* see below */ ]
}
```

`totalFamilies`, `totalVariants`, `totalStyles`, and every per-technology count
are **live values** — re-fetch and re-read them each time they're needed.
Never quote a number from this doc, from AGENTS.md, from CHANGELOG.md, or from
an earlier turn in the conversation. They drift constantly.

## Family object

```json
{
  "name": "Buttons",
  "path": "Tailwind/Components/Buttons",
  "tech": "Tailwind CSS",
  "category": "Components",
  "type": "component",
  "description": "...",
  "variantsCount": <int>,
  "tags": ["button", "cta"],
  "searchTerms": ["..."],
  "variants": [ /* see below */ ]
}
```

- `category` is Capitalized: `Components` | `Sections` | `Templates`.
- `type` is lowercase and is the field to filter on: `component` | `section` |
  `template`. Vanilla family objects may omit `type` (category alone
  disambiguates for Vanilla's two-type layout); Tailwind and React always
  carry it.
- `path` is the folder path relative to the repo root — this is what both the
  CLI (`npx devsnips add <path>`) and direct repository/raw-URL retrieval key
  off of. Confirm it here before using it anywhere else.

## Variant object

```json
{
  "name": "Solid Button",
  "path": "Tailwind/Components/Buttons/solid",
  "description": "...",
  "features": ["..."],
  "tags": ["..."],
  "styles": ["..."],
  "files": ["code.html", "preview.html", "metadata.json"]
}
```

- `files` lists what actually exists for that variant — use it to decide
  which implementation to inspect/retrieve rather than assuming a fixed file
  set. File sets differ by stack:
  - **Tailwind / Vanilla component or section**: `code.html`, `preview.html`,
    `metadata.json` (Vanilla also typically has `README.md`).
  - **React component**: `code.tsx`, `code.jsx`, `preview.html`,
    `metadata.json`, `README.md`.
  - **React section**: `code.tsx`, `metadata.json`, `preview.html` only — no
    `code.jsx`, no `README.md`. Don't go looking for a JS parity build that
    was never generated for Sections.
  - **Template**: typically a multi-page folder — inspect the folder itself
    rather than assuming a single `code.*` file.

## Matching a request to a family/variant

1. Normalize the request to the resource-type vocabulary: Component /
   Section / Template (see SKILL.md's boundary rules — don't upscale).
2. Match against family `name`, `tags`, and `searchTerms`, not just `name` —
   some intents (e.g. "hamburger menu") only surface via tags/searchTerms on
   a differently-named family (e.g. Navigation).
3. Filter by `tech` using the host project's actual stack (inspect the
   project first — see SKILL.md Phase 0). Don't default to Tailwind if the
   project is plain HTML/CSS/JS or React.
4. Within a family, rank variants by how many of the user's style words
   (dark, minimal, animated, destructive, with-icon, compact, ...) appear in
   that variant's `name` / `description` / `tags` / `features` / `styles`.
5. If the top candidates are close, list them briefly for the user rather
   than silently picking one — per SKILL.md Phase 2, don't select by name
   similarity alone.

## Cross-checking against the filesystem

The registry is authoritative for *what should exist*; the repository
filesystem is authoritative for *what files actually contain*. After
identifying a `path` from the registry:

- Confirm the path resolves on the current repository (registry entries can
  lag a rename/move — see AGENTS.md's own migration history for how often
  this has happened: Sections split out of Components, React families added
  incrementally, etc.).
- Read the real `metadata.json` and `README.md` at that path rather than
  trusting the registry's cached `description`/`features`/`tags` alone —
  those are indexed copies and can be stale relative to the source file.
