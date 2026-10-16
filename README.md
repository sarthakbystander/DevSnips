# DevSnips

**The UI library built for AI coding agents — and the humans who use them.**

Production-ready **components**, **sections**, and full **multi-page templates** for Vanilla HTML/CSS/JS, Tailwind CSS, and React. Free, open source, and designed so both developers and AI agents can discover, install, and adapt UI without starting from a blank file.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/sarthakbystander/DevSnips/actions/workflows/ci.yml/badge.svg)](https://github.com/sarthakbystander/DevSnips/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/sarthakbystander/DevSnips?style=social)](https://github.com/sarthakbystander/DevSnips/stargazers)
[![Variants](https://img.shields.io/badge/variants-1000%2B-brightgreen)](https://github.com/sarthakbystander/DevSnips)
[![npm](https://img.shields.io/npm/v/devsnips)](https://www.npmjs.com/package/devsnips)

---

## Why DevSnips?

Most UI libraries give you components. DevSnips gives you a **structured, machine-readable UI resource system** that works equally well for humans and AI coding agents.

| | |
|---|---|
| **1000+ production-ready variants** | Components, sections, and full templates across three stacks |
| **Agent-first design** | Machine-readable registry, MCP server, and official agent skill |
| **Source you own** | CLI installs real source files into your project — no black-box packages |
| **Consistent engineering** | Design tokens, accessibility-conscious markup, responsive by default |
| **MIT licensed** | Free for personal and commercial use |

From a single button to a complete AI SaaS platform, dashboard, agency site, or conference website — copy, adapt, and ship.

---

## Quick Start

### Install any resource with the CLI

```bash
npx devsnips add <path>
```

**Examples**

```bash
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
npx devsnips add React/Components/Buttons/solid-button
npx devsnips add Vanilla/Components/Buttons/split-button
```

Resources land in `./devsnips/<tech>/<category>/<family>/<variant>/` as plain source files you control.

Requires Node.js 18+. Full CLI docs → [`cli/README.md`](cli/README.md)

---

## What's Inside

### Components
Reusable UI elements and interaction patterns (buttons, inputs, forms, cards, navigation, modals, dropdowns, tables, tooltips, and more).

### Sections
Complete page regions ready to drop in: heroes, features, pricing, testimonials, contact, footers, AI product sections, dashboard blocks, and more.

### Templates
Full multi-page starting points. Featured examples:

- [AI SaaS Platform](library/Tailwind/Templates/ai-saas-platform/preview.html)
- [Northstar Vanilla Dashboard](library/Vanilla/Templates/saas-dashboard/preview.html)
- [Stratum](library/Tailwind/Templates/stratum/preview.html)
- [Northline Atelier](library/Tailwind/Templates/northline-atelier/preview.html)
- [Baseline Conference](library/Tailwind/Templates/baseline-conference/pages/index.html)

### Supported stacks

| Stack | What you get |
|-------|--------------|
| **Tailwind CSS** | Components · Sections · Templates |
| **React** | Components · Sections · Templates |
| **Vanilla** | HTML · CSS · JavaScript |

Browse:
- [Tailwind library](library/Tailwind/index.html)
- [React library](library/React/index.html)
- [Vanilla library](library/Vanilla/Sections/sections-index.html)

---

## Built for AI Coding Agents

DevSnips is deliberately structured so agents can discover, evaluate, install, adapt, and verify UI resources reliably:

- **Live registry** — [`snippets-index.json`](https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json) is the authoritative, machine-readable inventory
- **Official agent skill** — drop-in instructions for agents that use DevSnips
- **MCP integration** — expose the library to MCP-compatible clients
- **AGENTS.md** — clear entry point for agents working on this repository or in consumer projects

See the [agent documentation](docs/agents/overview.md) and [MCP overview](docs/mcp/overview.md).

---

## Documentation

Start with the [documentation index](docs/index.md) — it routes by role:

| You are… | Start here |
|----------|------------|
| An AI coding agent integrating DevSnips | [Introduction](docs/introduction/what-is-devsnips.md) → [Agent overview](docs/agents/overview.md) → [CLI](docs/cli/overview.md) |
| A developer evaluating the library | [What is DevSnips](docs/introduction/what-is-devsnips.md) → [Architecture](docs/introduction/architecture.md) → [Resources](docs/resources/overview.md) |
| A contributor adding a resource | [Resource model](docs/resources/overview.md) → [Creating resources](docs/contributing/creating-resources.md) → [Validation](docs/contributing/validation.md) |
| Connecting via MCP | [DevSnips MCP](docs/mcp/overview.md) |

Key references: [CLI reference](docs/reference/cli-reference.md) · [Registry schema](docs/machine-readable/registry.md) · [Contributing guide](docs/CONTRIBUTING.md) · [`AGENTS.md`](AGENTS.md)

---

## Design Philosophy

- Reusable design tokens
- Consistent spacing & typography
- Responsive layouts by default
- Neutral-first foundations with controlled visual variation
- Accessibility-conscious interfaces
- Source that is easy for humans and agents to read and adapt

**Different designs. Consistent engineering.**

---

## Use Cases

AI SaaS products · Dashboards & admin panels · Business & agency sites · Developer tools · Landing pages · Portfolios · Conference & event sites · Product marketing sites · Personal projects

---

## Contributing

Contributions are welcome — new variants, fixes, documentation, and tooling improvements.

1. Fork the repository
2. Create a feature branch
3. Follow the [resource model](docs/resources/overview.md) and [validation](docs/contributing/validation.md) rules
4. Open a pull request

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full guide.

---

## License

MIT © [Sarthak Bystander](https://github.com/sarthakbystander)

Free for personal and commercial use.

---

## Star the repo

If DevSnips saves you time (or helps your AI agent ship better UI), a star helps others discover it.

[![Star this repo](https://img.shields.io/github/stars/sarthakbystander/DevSnips?style=for-the-badge&logo=github)](https://github.com/sarthakbystander/DevSnips)
