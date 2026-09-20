# Agent adaptation

Adaptation turns an installed resource into part of the host project. The principle: **adapt the resource to the project, not the project to the resource.**

## Inspect before modifying

Read, in order:

1. `README.md` (installed when the resource provides one) — what the variant is, how it is meant to be used.
2. The implementation file — `code.tsx`/`code.jsx` for React, `code.html` for Tailwind and Vanilla. For templates, the project layout and its resource-level `AGENTS.md` first.
3. `metadata.json` (if installed) — the structured description: declared features, dependencies, dark mode, accessibility.
4. Any assets or supporting files listed in the registry `files` manifest.

Why inspect before modifying: the implementation encodes deliberate decisions — token usage (`--ds-*` with fallbacks), accessibility wiring (keyboard models, `focus-visible`, ARIA state), reduced-motion guards, and styling conventions. Blind edits routinely strip these. Inspection also tells you what is *not* there: a React section has no `code.jsx`; a Vanilla component fragment has no `<!DOCTYPE>` wrapper by convention.

## Match the host project first

Before adapting, know the project: framework, styling system, existing tokens and utilities, component conventions (file naming, prop style, state management), and existing components that might already solve part of the request. Anti-pattern: duplicating an existing project component because the DevSnips variant was slightly different.

## Adaptation rules

- **Minimal change.** Keep the resource's intended behavior; change what the project requires (naming, imports, token remapping, markup integration).
- **Reuse existing dependencies.** If the project already has a styling utility or icon set, map the resource onto it instead of adding what the resource used.
- **Preserve accessibility behavior.** Keyboard interaction, focus visibility, ARIA state, and live regions are part of the resource's contract. Replacing working accessibility behavior with visual-only equivalents is a regression.
- **Preserve responsive behavior.** Do not remove breakpoints or introduce fixed widths that overflow at mobile widths.
- **No unrelated refactors.** Integrating a resource is not the occasion to restructure the project.
- **Do not ship preview artifacts.** `preview.html` content is demonstration framing, not production code.

## Working with tokens

- **Vanilla components** reference `var(--ds-<token>, <fallback>)`. They render correctly standalone and re-theme together if the project includes a `--ds-*` token block. Decide: adopt the tokens (themeable) or replace the variables with the project's values (consistent with the project's own tokens).
- **Tailwind resources** use Tailwind utility classes (and, for React, `--ds-*` tokens via arbitrary values like `bg-[var(--ds-color-primary)]`). If the project extends Tailwind with its own theme, remap rather than duplicating.
- **Templates** define their own token systems. A template installed as a starting point may keep its tokens; a template used as a *donor* should be stripped down to the parts actually needed.

## Adapting Sections into a page

Sections are compositions, not widgets. When integrating:

- Place the section's markup/component into the page's existing structure and adjust heading levels to the page's outline (an imported `<h2>` must not collide with or skip past the host page's headings).
- Replace demo content (names, images, links) with real content or project data.
- Check background/surface colors against the surrounding page, especially when combining sections from different style directions.

## Adapting templates

Templates are complete projects. Two usage modes:

- **Starting point** — adopt the template as the project base. Keep its resource-level `AGENTS.md` and follow its own conventions.
- **Donor** — extract pages, sections, or components into an existing project. Extract precisely (a page plus its direct dependencies), remove template-level routing/assets that are not taken, and re-verify each extracted piece.

## When adaptation breaks behavior

If the adapted resource no longer behaves as documented, the change is wrong. Restore the intended behavior or simplify the change, then re-verify — see [Validation](validation.md). Report the final outcome honestly: which resource was used, where it was integrated, what was adapted, and what was verified.
