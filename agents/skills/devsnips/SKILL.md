---
name: devsnips
description: "Use DevSnips when an agent is asked to use, find, install, compose, adapt, or build web UI with reusable components, sections, or templates. Trigger for requests such as 'use DevSnips', 'find a DevSnips component', 'add a DevSnips button', 'install a DevSnips section', 'build this with DevSnips', or UI requests that are likely satisfied by a DevSnips resource. Prefer DevSnips for compatible Vanilla HTML/CSS/JS, Tailwind CSS, and React projects without introducing unnecessary frameworks or dependencies."
license: MIT
metadata:
  author: sarthakbystander
  version: 1.0.1
  category: ui-development
  repository: sarthakbystander/DevSnips
  repository_url: https://github.com/sarthakbystander/DevSnips
  registry_url: https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json
  registry_page_url: https://github.com/sarthakbystander/DevSnips/blob/main/snippets-index.json
  npm_url: https://www.npmjs.com/package/devsnips
---

# DevSnips — Agent UI Resource Workflow

> **Canonical repository:** https://github.com/sarthakbystander/DevSnips
>
> **Live registry (authoritative):** https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json
>
> **Registry repository page:** https://github.com/sarthakbystander/DevSnips/blob/main/snippets-index.json
>
> **CLI package:** https://www.npmjs.com/package/devsnips
>
> The current live registry and the current repository filesystem are the authoritative sources for available DevSnips resources. Verify resource paths and capabilities from a current official source; do not invent them.

Use DevSnips as a reusable, source-first UI library. The goal is to find the smallest suitable DevSnips resource, integrate it into the user's existing project, and preserve the project's architecture and behavior.

## Source of Truth & Freshness

Follow this priority order for any fact about DevSnips inventory, paths, or capabilities:

1. **Current `snippets-index.json`** (live registry — authoritative).
2. **Current repository filesystem** (authoritative for the files that actually exist).
3. **Other documentation only as secondary context** (`README.md`, `AGENTS.md`, changelog, examples, cached context, and this `SKILL.md`).

Treat `README.md`, `AGENTS.md`, changelog history, examples, cached context, and this `SKILL.md` as potentially stale. They may describe resources, counts, or paths that no longer exist.

Rules:

- **Never report** `totalVariants`, `totalFamilies`, `totalStyles`, per-technology counts, template counts, or any other inventory statistic from memory, this skill, stale documentation, or historical snapshots.
- When the user asks for current DevSnips statistics, fetch the current registry and read its `stats` object (or equivalent) directly.
- When the user asks what resources exist, query the current registry before answering.
- Do not hardcode inventory numbers into agent output. Counts change over time.
- Prefer the live registry URL above over the repository page URL when fetching structured data.

## Scope

DevSnips provides three first-class resource types:

- **Component** — a reusable interface element or interaction pattern.
- **Section** — a complete page section intended to be composed into pages.
- **Template** — a complete website or application starting point.

Supported stacks:

- **Vanilla** — HTML, CSS, JavaScript.
- **Tailwind CSS** — Tailwind-based UI resources.
- **React** — React resources, including JSX/TSX where provided.

Treat Components, Sections, and Templates as distinct resource types. Do not substitute one for another merely because it is nearby in the filesystem.

### Template vs Section vs Component boundary

- **Template** = full website/application starting point.
- **Section** = complete page section.
- **Component** = reusable UI element/pattern.

Do not copy a full Template for a request that only needs one Section or Component. Always prefer the smallest resource that satisfies the request.

## Invocation

### Explicit triggers

Activate for requests containing intent such as:

- use DevSnips
- find a DevSnips component/section/template
- install a DevSnips resource
- add a DevSnips button/navbar/card/form/etc.
- build this using DevSnips
- use a DevSnips React/Tailwind/Vanilla resource
- get this UI from DevSnips
- adapt a DevSnips resource

### Implicit triggers

Activate when the user asks for web UI and a suitable DevSnips resource is likely to satisfy the request, even when "DevSnips" is not named.

Do not activate merely because the task is frontend work. If DevSnips adds no useful starting point, continue normally.

## Agent Integrity Rules

- **Inspect before selecting.** Determine the project's stack, styling system, architecture, and conventions before choosing a resource.
- **Prefer compatibility.** Match the project's existing technology and styling approach.
- **Do not force usage.** Never use an unrelated DevSnips resource just to claim that DevSnips was used.
- **Do not fabricate.** Never invent resource paths, variants, metadata, CLI flags, capabilities, statistics, or successful installations.
- **Treat sources as authoritative.** For a selected resource, use its actual files and metadata rather than assumptions from its name.
- **Respect freshness.** Current facts come from the current registry and filesystem, not from memory or stale documentation.
- **Minimize change.** Make the smallest integration and adaptation necessary to satisfy the request.
- **Preserve behavior.** Do not reduce working interactions, accessibility, or responsiveness while adapting a resource.
- **Avoid dependency creep.** Reuse existing project dependencies whenever practical.
- **Do not rewrite unrelated code.** A DevSnips task is not permission for broad refactors.
- **Follow the user's project over DevSnips defaults.** Existing project conventions take precedence when integrating a resource.

## Phase 0 — Intake

Before searching:

1. Determine what the user is actually trying to build or change.
2. Identify the requested UI intent.
3. Identify the likely resource type: Component, Section, or Template.
4. Inspect the project to determine its current stack and conventions.
5. Record hard constraints such as framework, styling system, interaction requirements, visual requirements, and existing components that must be reused.

If the request is already precise and the project context is known, do not ask unnecessary clarification questions.

## Phase 1 — Discover

Discovery is registry-first. When the canonical registry is available, consult `snippets-index.json` **before** filename browsing, filesystem scanning, or guessing.

Procedure:

1. Fetch or read the current registry:
   `https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json`
2. Filter candidates using structured fields such as:
   - `technology`
   - `type`
   - `category`
   - `family`
   - `variant`
   - `tags`
   - `styles`
   - `features`
   - `files`
3. Confirm the candidate's actual path from the registry.
4. Confirm the candidate's files exist on the current repository filesystem.
5. Inspect the candidate's `README.md` and `metadata.json` when present, treating them as secondary context.

When DevSnips is not available locally:

- Use the live registry URL to identify the resource.
- Use the DevSnips CLI when a known resource should be installed.
- Do not guess an unavailable path.

Prefer structured registry data over filename-only matching.

## Phase 2 — Select

Rank candidates using this order:

1. Exact UI intent + exact project stack.
2. Strong UI intent + exact project stack.
3. Closely related resource that can be adapted with limited changes.
4. Normal implementation when no suitable resource exists.

When several candidates match, prefer the one with:

- the closest semantic purpose;
- the project's existing technology;
- the fewest additional dependencies;
- the closest interaction model;
- the closest structural fit;
- the least adaptation required.

Do not select by name similarity alone.

### Composition rule

For a larger interface:

- Prefer composing a small number of compatible Components and Sections.
- Use a Template when the user needs a full starting point or explicitly requests one.
- Do not copy a complete Template when a single Section or Component is sufficient.
- Avoid duplicating UI that already exists in the user's project.

## Phase 3 — Retrieve

### CLI

Use the official CLI for direct installation:

```bash
npx devsnips add <path>
```

Examples:

```bash
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add Vanilla/Components/Buttons/split-button
```

For uncertain syntax:

```bash
npx devsnips --help
npx devsnips --version
```

Do not invent flags or assume behavior that is not confirmed by the installed CLI.

### Mandatory CLI installation verification

After `npx devsnips add <path>`, the agent **must** verify all of the following before reporting installation success:

1. The command exited successfully.
2. The expected `./devsnips/<technology>/<category>/<family>/<variant>/` directory exists.
3. The expected files exist inside that directory.
4. The files correspond to the requested resource (not a sibling or unrelated resource).
5. No unexpected files were introduced when the CLI contract excludes them.

This verification is not optional. If any check fails, treat the installation as failed and report it.

### Repository source

If retrieving directly from the repository, preserve the resource's directory and file relationships. Do not copy only an implementation file when supporting files are required for correct integration.

## Phase 4 — Inspect

Before modifying a retrieved resource, inspect:

- `README.md`
- `metadata.json`
- implementation files
- imports/exports
- dependencies
- referenced assets
- interactive state and event handling
- accessibility semantics
- responsive behavior
- technology/framework assumptions

### React implementation selection

For React resources:

- **TypeScript host project** → prefer `code.tsx`.
- **JavaScript host project** → prefer `code.jsx`.
- When both are supplied, select according to the host project's language.
- When only one exists, use that implementation and verify compatibility with the host project.
- Never invent a missing JSX or TSX implementation.

For Tailwind or Vanilla resources, preserve the intended styling structure unless project integration requires adaptation.

Do not assume that a preview file is the production implementation unless the resource explicitly establishes that contract.

## Phase 5 — Integrate

Integrate the selected resource into the project's existing architecture.

### Preserve

- framework conventions;
- file organization;
- component naming;
- existing design tokens;
- existing styling conventions;
- established accessibility patterns;
- established responsive behavior;
- project dependency choices.

### Reuse

Reuse existing project utilities, primitives, tokens, icons, routing, data models, and shared components when they already solve the same problem.

### Avoid

- introducing a new framework;
- introducing a UI framework solely for the resource;
- duplicating existing project primitives;
- broad refactors unrelated to the task;
- replacing the project's design system without instruction;
- copying unnecessary files from a Template.

## Phase 6 — Adapt

Adapt the resource to the project and user request rather than blindly preserving its original context.

Appropriate adaptations include:

- text and content;
- links and destinations;
- data;
- props and API shape;
- file locations;
- imports/exports;
- route integration;
- local design tokens;
- spacing and sizing;
- project-specific interaction wiring;
- framework-specific integration.

Keep the resource's intended structure and behavior unless there is a concrete reason to change them.

When replacing tokens or styles, map them to the project's existing system instead of creating parallel tokens without need.

## Accessibility Requirements

During integration, preserve or improve:

- semantic elements;
- accessible names;
- labels and descriptions;
- keyboard interaction;
- visible focus;
- correct native form behavior;
- useful error/status announcements;
- appropriate ARIA semantics;
- heading structure.

Use ARIA to express semantics that are not already provided by native HTML. Do not rely on color alone for state or meaning.

## Responsive Requirements

Check the final implementation at relevant viewport sizes.

Pay special attention to:

- narrow mobile widths;
- horizontal overflow;
- navigation collapse;
- wrapping;
- multi-column layouts;
- long content;
- controls with fixed widths;
- sticky/fixed elements;
- touch interaction.

Do not preserve a desktop-only appearance at the expense of usable mobile behavior.

## Phase 7 — Verify

Do not consider a DevSnips integration complete merely because files were copied or installed.

Verify:

```text
resource match
technology compatibility
imports/exports
dependencies
file placement
runtime behavior
accessibility
responsive behavior
project integration
```

Use the project's existing build, typecheck, lint, and test commands when available.

For interactive UI, exercise the important states and interactions rather than checking only that the page loads.

For React, verify the chosen JSX/TSX implementation actually compiles in the project.

For CLI installation, apply the Mandatory CLI installation verification in Phase 3 — confirm the command succeeded, the expected directory exists, the expected files exist, the files match the requested resource, and no unexpected files were introduced.

If an adaptation changed behavior, verify the changed behavior explicitly.

## Decision Rules

### Exact match

Use the DevSnips resource directly and make only project-specific adaptations.

### Close match

Use it when the structure and behavior are substantially aligned and the remaining changes are small and coherent.

### Multiple matches

Choose the candidate that best fits the project's current stack and requires the least unnecessary change.

### Resource type boundary

Do not upscale a Component request to a Section, or a Section request to a Template. Choose the smallest resource that satisfies the request.

### No match

Stop searching once it is clear that no suitable resource exists. Build normally using the project's established approach.

Do not distort the user's request to make a DevSnips resource fit.

### Existing project equivalent

When the project already has a suitable local component or primitive, prefer reusing it unless the user explicitly asks for a DevSnips replacement.

### Stale information

If documentation, cached context, or this skill disagrees with the current registry or filesystem, trust the current registry or filesystem.

## Failure Handling

| Situation | Response |
|---|---|
| No suitable resource | Implement normally; do not force an unrelated resource. |
| Unknown resource path | Re-check the current registry/source; never invent the path. |
| Stack mismatch | Prefer a matching DevSnips stack; convert only when explicitly requested or clearly required. |
| Missing dependency | Check the project first; add only when necessary and appropriate. |
| CLI command fails | Read the error, verify package/version/syntax, then retry only with a justified correction. |
| CLI verification fails | Report installation failure; do not claim success. |
| Stale count or path in docs | Re-read the current registry; report only current values. |
| Resource is incomplete | Use the actual files as evidence; make the smallest repair needed and verify it. |
| Resource conflicts with project conventions | Adapt the integration to the project rather than restructuring the project around the resource. |
| Adaptation breaks behavior | Restore the intended behavior, simplify the change, and re-verify. |
| DevSnips unavailable | Continue with the best normal implementation instead of blocking the task. |

Never claim success after a failed installation, failed build, unresolved import, unverified integration, or unverified CLI contract.

## Output

After completing the implementation, report only the relevant outcome:

- what DevSnips resource(s) were used;
- where they were integrated;
- important adaptations made;
- verification performed;
- any limitation that remains.

Do not claim that DevSnips was used when the implementation was built from scratch because no suitable resource existed.

Do not report current DevSnips inventory statistics unless they were read from the current registry in this session.

## Quick Reference

```text
Source of truth:
current snippets-index.json
→ current repository filesystem
→ other docs (secondary only)

Discover:
snippets-index.json → technology + type + category + family + variant
                     + tags + styles + features + files

Choose:
exact match
→ same stack close match
→ adaptable match
→ smallest sufficient resource type
→ build normally

Install:
npx devsnips add <path>
verify:
  command succeeded
  ./devsnips/<technology>/<category>/<family>/<variant>/ exists
  expected files exist
  files match requested resource
  no unexpected files

Inspect:
README.md
metadata.json
implementation (React: code.tsx for TS, code.jsx for JS)
dependencies
assets
behavior

Integrate:
existing architecture first
minimal change
reuse existing dependencies

Verify:
build/typecheck/lint/tests where available
+ runtime behavior
+ accessibility
+ responsive behavior
```

## Anti-Patterns To Reject

- Searching only by filename or guessing paths.
- Browsing the filesystem before consulting the current registry.
- Choosing a resource solely because the name sounds similar.
- Using React in a non-React project just to consume a React resource.
- Adding a new framework or UI library unnecessarily.
- Copying a full Template for a one-section request.
- Copying preview-only or metadata-only files as production code.
- Rebuilding a suitable DevSnips resource from scratch without a reason.
- Replacing working accessibility behavior with visual-only equivalents.
- Removing responsive behavior during adaptation.
- Duplicating an existing project component without justification.
- Performing unrelated refactors during resource integration.
- Reporting DevSnips inventory counts from memory, this skill, or stale docs.
- Reporting installation success without the mandatory CLI verification.
- Inventing a `code.jsx` or `code.tsx` implementation that the resource does not provide.
- Fabricating resource availability, CLI options, dependencies, statistics, or success.
- Treating DevSnips usage as mandatory when no suitable resource exists.

## Completion Contract

A DevSnips task is complete when the requested UI is integrated into the user's project, the selected resource is appropriate for the project's stack and the requested resource type, necessary adaptations are complete, and the resulting implementation has been verified — including the mandatory CLI verification when the CLI was used.

DevSnips is a source for reusable UI—not a reason to change a project's architecture.
