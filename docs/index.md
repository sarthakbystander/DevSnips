# DevSnips Documentation

DevSnips is an agent-first UI resource library: a structured collection of UI resources — Components, Sections, and Templates in React, Tailwind CSS, and Vanilla HTML/CSS/JS — that AI coding agents can discover, evaluate, install, adapt, and verify through machine-readable interfaces.

Start here based on what you are doing:

| You are… | Read |
|---|---|
| An AI coding agent integrating DevSnips into a project | [Introduction](introduction/what-is-devsnips.md) → [Agent overview](agents/overview.md) → [CLI](cli/overview.md) |
| A developer evaluating DevSnips | [What is DevSnips](introduction/what-is-devsnips.md) → [Architecture](introduction/architecture.md) → [Resources](resources/overview.md) |
| A contributor adding a resource | [Resource model](resources/overview.md) → [Creating resources](contributing/creating-resources.md) → [Validation](contributing/validation.md) |
| An integrator consuming the registry programmatically | [Machine-readable overview](machine-readable/overview.md) → [Registry schema](machine-readable/registry.md) |
| An AI coding agent (or developer) connecting DevSnips to an MCP client | [DevSnips MCP](mcp/overview.md) |
| New to DevSnips and want a guided path | [Tutorials](tutorials/getting-started.md) |
| Theming a project or adapting a resource | [Theming](theming.md) |
| Running or extending the repository tooling | [Tooling](tooling/overview.md) → [QA](qa/overview.md) |
| Looking up a definition, path, or command | [Reference](reference/terminology.md) → [FAQ](faq.md) |

## Documentation map

```text
docs/
├── introduction/        What DevSnips is, why it exists, how the pieces fit together
│   ├── what-is-devsnips.md
│   ├── philosophy.md
│   └── architecture.md
├── agents/              The agent lifecycle: discovery → selection → install → adapt → verify
│   ├── overview.md
│   ├── discovery.md
│   ├── resource-selection.md
│   ├── installation.md
│   ├── adaptation.md
│   └── validation.md
├── resources/           The resource model: types, technologies, file contracts
│   ├── overview.md
│   ├── components.md
│   ├── sections.md
│   ├── templates.md
│   ├── technologies.md
│   └── resource-structure.md
├── cli/                 The `devsnips` CLI: add, init, project context, troubleshooting
│   ├── overview.md
│   ├── add.md
│   ├── init.md
│   ├── configuration.md
│   └── troubleshooting.md
├── machine-readable/    The registry, metadata, and derived machine-readable surfaces
│   ├── overview.md
│   ├── registry.md
│   ├── metadata.md
│   └── schemas.md
├── mcp/                 The devsnips-mcp server: install, configure, connect, use
│   └── overview.md
├── tooling/             scripts/tooling/: validators, indexing, site generators, utilities
│   └── overview.md
├── qa/                  The QA surface: validators, quality bars, browser harnesses
│   └── overview.md
├── tutorials/           Step-by-step walkthroughs
│   ├── getting-started.md
│   ├── install-and-customize.md
│   ├── build-a-landing-page.md
│   └── author-a-resource.md
├── contributing/        How to add resources: structure, metadata, agent files, validation
│   ├── overview.md
│   ├── creating-resources.md
│   ├── metadata.md
│   ├── agent-files.md
│   └── validation.md
├── reference/           Terminology, directory structure, CLI reference, conventions
│   ├── terminology.md
│   ├── directory-structure.md
│   ├── cli-reference.md
│   └── conventions.md
├── theming.md           Design tokens and the --ds-* contract per technology
└── faq.md
```

## Canonical sources inside this repository

These documentation pages explain the system. The following are the authoritative sources; when this documentation and one of them disagree, the source wins:

1. `library/` and each resource's `metadata.json` — what actually exists.
2. `snippets-index.json` — the generated machine-readable registry. Never quote resource counts from documentation; read them from the registry.
3. `AGENTS.md` (repository root) — the entry point for AI agents working *on this repository*.

## Related entry points

- `AGENTS.md` — agent-facing repository context (maintenance and modification tasks).
- `agents/resources/*.md` — repository-side deep reference for agents modifying DevSnips itself.
- `agents/skills/devsnips/SKILL.md` — the operational skill for agents *consuming* DevSnips.
- `docs/COMPONENT_STRUCTURE.md`, `docs/CONTRIBUTING.md` — maintainer-facing structure specs.
- `website/llms.txt`, `website/llms-full.txt`, `website/search-index.json` — website discovery surfaces.
