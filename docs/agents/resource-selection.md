# Agent resource selection

Selection is the stage where an agent decides *which* DevSnips resource — if any — to use. The goal is to find the smallest suitable resource that matches the host project's stack, and to prefer reuse over regenerating code.

## Step 1 — Normalize the request into the resource vocabulary

Classify the request as one of the three types:

| Request shape | Type |
|---|---|
| "a button / accordion / modal / dropdown…" | component |
| "a hero / pricing block / footer / testimonials area…" | section |
| "a dashboard / landing page / full site…" | template |

Types are not interchangeable:

- Do not upscale — do not install a full template when one section answers the request.
- Do not downscale-by-substitution — do not merge a section into a component or treat a section as "just markup".
- If the request is genuinely between two types (e.g. "a pricing block that becomes a page"), present the closest candidates of each type to the user instead of silently choosing.

## Step 2 — Match the host project's stack

Inspect the project before searching: framework, styling system, existing dependencies. Then filter candidates to the matching technology:

| Project stack | Technology filter |
|---|---|
| Plain HTML/CSS/JS | `Vanilla HTML/CSS/JS` |
| Tailwind CSS | `Tailwind CSS` |
| React (with or without TypeScript) | `React` |

Anti-patterns to reject: using React in a non-React project to consume a React resource; adding a framework or UI library just to install a resource; defaulting to Tailwind when the project is vanilla.

## Step 3 — Match semantics, not names

Within the chosen type and technology, match the request against:

- family `name` and `tags` (registry),
- variant `description`, `tags`, `features`, and `styles`.

Rank variants by how many of the user's intent words (dark, minimal, animated, destructive, compact, with-icon, …) appear in those fields. Never choose a resource solely because its name sounds similar.

## Step 4 — Apply the selection ladder

When multiple candidates fit, resolve in this order:

```text
1. Exact match in the project's stack
2. Close match in the project's stack (minor adaptation expected)
3. Adaptable match in another stack (only if the user agrees — costs a rewrite)
4. Smallest sufficient resource type
5. No suitable resource → build normally and say so
```

If the top candidates are close, list them briefly for the user rather than silently picking one.

## Step 5 — Read the metadata before committing

Before installing, confirm from the variant record:

- `files` — what will actually be installed. If a resource lacks the implementation form you expect (e.g. no `code.jsx` on a React section — sections ship `code.tsx` only), adapt your plan now, not after installation.
- `description` / `features` — that the variant's behavior matches the request (single-open vs multi-open accordion, for example).
- `install` (specialized indexes) — the exact command to run.

Registry copies of descriptions can lag the source files. For high-stakes selections, read the resource's `metadata.json` and `README.md` at `library/<path>` directly.

## Step 6 — Confirm identifiers

The only identifier the CLI accepts is the registry path. Case-insensitive matching is supported by the resolver, but the canonical form is the registry's own path spelling. Do not invent IDs, and do not abbreviate paths (e.g. `Tailwind/Components/Buttons/basic-button` when the variant is `basic-button/primary`).

## When not to select anything

Reject the reuse path when:

- the registry (fetched this session) has no suitable family or variant;
- the only candidates require a technology the project does not use;
- the request is trivial enough that writing it directly is smaller than adapting a resource;
- adaptation would require replacing working project behavior.

In these cases build the UI normally and report that no DevSnips resource was used. Never rebuild a suitable DevSnips resource from scratch without a reason, and never force DevSnips usage when nothing fits.
