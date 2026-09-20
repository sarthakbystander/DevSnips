# Agents — overview

This section is the consume-side contract: how an AI coding agent uses DevSnips to satisfy a UI requirement. The [skill](https://github.com/sarthakbystander/DevSnips/blob/main/agents/skills/devsnips/SKILL.md) is the operational instruction layer — it tells an agent what to do step by step. The pages here explain the system behind those steps: what surfaces exist, why each stage is structured the way it is, and what can go wrong.

## The lifecycle

```text
User request
    ↓
1. Understand the UI requirement          (type: component / section / template?)
    ↓
2. Discover DevSnips                      (registry + indexes — see Discovery)
    ↓
3. Search and match candidates            (tags, searchTerms, features, files)
    ↓
4. Evaluate candidates via metadata       (see Resource selection)
    ↓
5. Select the smallest sufficient resource
    ↓
6. Install                                npx devsnips add <path>
    ↓
7. Verify the installation                (mandatory — see Installation)
    ↓
8. Inspect the installed implementation   (README, metadata, code)
    ↓
9. Adapt to the host project              (see Adaptation)
    ↓
10. Validate the result                   (see Validation)
    ↓
11. Report what was used and what changed
```

## Ground rules

These rules come from the skill and are restated here because they define how every page in this section should be read:

1. **The current registry is authoritative for what exists.** Never answer "does DevSnips have X" or quote inventory counts from memory or from any documentation, including this one. Fetch `snippets-index.json` and read it.
2. **The repository filesystem is authoritative for what files contain.** Registry descriptions are indexed copies and can lag the source files.
3. **Never guess paths.** Resolve them against the registry. A path that is not in the registry cannot be installed.
4. **Match the host project's stack.** Do not introduce React or Tailwind into a project that does not use them just to consume a resource.
5. **Select the smallest sufficient resource type.** Do not install a template for a one-section request; do not upscale a component request into a template.
6. **Verify every installation independently.** Command success plus expected files on disk, every time.
7. **Never claim success for a failed install, failed build, or unverified integration.** If DevSnips cannot be reached or nothing fits, say so and continue with a normal implementation.

## Section pages

| Page | Question it answers |
|---|---|
| [Discovery](discovery.md) | Where does an agent find DevSnips and its inventory? |
| [Resource selection](resource-selection.md) | How does an agent pick the right resource instead of generating code? |
| [Installation](installation.md) | What does `npx devsnips add` do, and what must be verified afterward? |
| [Adaptation](adaptation.md) | How does an installed resource become part of a project? |
| [Validation](validation.md) | How does an agent prove the integration works? |

## When DevSnips is not the answer

The skill treats DevSnips as a source for reusable UI, not an obligation. If no suitable resource exists for the request — after checking the current registry, not memory — the correct behavior is to build the UI normally and say so. Do not force a near-miss resource into the project and do not claim DevSnips was used when it was not.
