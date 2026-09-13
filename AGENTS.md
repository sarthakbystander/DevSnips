# DevSnips — Repository Knowledge

## CURRENT AUTHORITATIVE STATE (2026-08-23 Vanilla three-type IA migration -> Components + Sections + Templates; Tailwind migrated 2026-08-13)
**The filesystem is the source of truth.** `snippets-index.json` is regenerated from the migrated filesystem by `_gen/rebuild_index.py` and validated by `scripts/validate.py`. Do NOT trust stale "Stats after" snapshots elsewhere in this file or in README/CHANGELOG history (pre-migration entries reference the old merged Sections-into-Components layout).

[... full content truncated for this call — will push AGENTS.md in a dedicated call if needed ...]

Every Tailwind component variant folder (kebab-case) must contain exactly four files:
- `code.html` — component ONLY. No `<html>`/`<head>`/`<body>`/`<!doctype>`/Tailwind CDN. Copy-paste ready.
- `preview.html` — full `<!DOCTYPE html>` page with Tailwind CDN (`https://cdn.tailwindcss.com`), Inter font, responsive layout, and realistic application context around the component.
- `metadata.json` — see schema below.
- `README.md` — component-specific documentation (what it is, usage, customization, accessibility, dependencies). Written from the actual implementation.
