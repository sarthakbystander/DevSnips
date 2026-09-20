# Contributing — metadata

Metadata is part of the library's infrastructure, not decoration. This page covers authoring `metadata.json` for a new or modified resource. Field-level reference: [Metadata](../machine-readable/metadata.md).

## The one rule that governs everything

**Copy a sibling, then tell the truth.** The schema is per-technology and per-type; the fastest correct metadata is the sibling leaf's file with every field adjusted to your resource. Inventing keys or claiming unimplemented behavior breaks consumers.

## Procedure

1. Open the `metadata.json` of a sibling leaf in the same family and type.
2. Copy it into your leaf.
3. Update every field:
   - `type` must match the folder bucket (`component` / `section` / `template`).
   - `slug` should equal your folder name where the schema has `slug`.
   - `name` is human-readable Title Case (`Solid Button`, `Minimal Hero`).
   - `description` describes what this variant actually is and is for.
   - `tags` — lowercase search words.
   - `searchTerms` — user-intent phrases (where the schema has them).
   - `features` — short phrases for capabilities the code actually implements.
   - `responsive`, `darkMode`, `accessibility` — only what is true.
   - `dependencies` — runtime requirements (Tailwind via CDN, Google Fonts, …).
   - `related` — sibling slugs that serve as alternatives.
   - `id` — kebab-case, unique, often zero-padded (`<slug>-001`). Never collide with an existing ID; never change an existing ID elsewhere.
4. Booleans as real booleans. No placeholder values.

## Rules enforced by tooling

| Rule | Enforced by |
|---|---|
| Valid JSON on every leaf | `validate.py` (failure) |
| `type` present, lowercase vocabulary, matches folder bucket | `validate.py` (failure) |
| Required files per tech + type alongside the metadata | `validate.py`, `deep_check.py` |
| Duplicate IDs | `validate.py` NOTE only — but new collisions are not acceptable |

## What metadata flows into the registry

On regeneration, the index builder reads `name`, `description`, `tags`, `features`, and `style`/`styles` from your metadata (falling back to the previous index for anything absent). Everything else stays resource-local. Consequences:

- Good metadata here is what makes the resource discoverable by tags and features.
- Deleting a curated field from metadata does not necessarily remove it from the registry — check the entry after regenerating.

## Naming rules

- Filesystem slug: kebab-case lowercase (`multi-step-form`, `pricing-comparison`).
- Display name: Title Case (`Pricing Comparison`).
- Tailwind generated sections: `"Modern Blog — Minimal"` (em dash + style).
- React sections: `"<Family> — <Direction>"` (`"Hero — Minimal"`).
- Avoid generic variants: `new`, `test`, `final`, `version-2`.

## Modifying existing metadata

- Changing content in place does not change identity; keep the folder name and slug.
- Keep IDs stable. Do not rename an ID merely to make it look nicer.
- After any change: `python scripts/tooling/indexing/rebuild_index.py`, then `python scripts/tooling/validators/validate.py`.
