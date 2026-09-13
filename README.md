# DevSnips

**The largest free & open-source UI library for web developers**

Reusable **Tailwind CSS**, **Vanilla HTML/CSS/JS**, and **React** components, sections, and full multi-page templates — including production-ready AI SaaS platforms.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/sarthakbystander/DevSnips?style=social)](https://github.com/sarthakbystander/DevSnips/stargazers)
[![Variants](https://img.shields.io/badge/variants-1000%2B-brightgreen)](https://github.com/sarthakbystander/DevSnips)
[![Templates](https://img.shields.io/badge/templates-19-orange)](https://github.com/sarthakbystander/DevSnips)
[![npm](https://img.shields.io/npm/v/devsnips)](https://www.npmjs.com/package/devsnips)

---

## Why DevSnips?

DevSnips is a free, open-source UI library built for developers who want production-ready interfaces without starting every project from an empty file.

- **1000+ UI variants**
- **15+ visual styles**
- **Tailwind CSS, React, and Vanilla**
- **Full multi-page templates**
- **Reusable components and sections**
- **Design-token driven interfaces**
- **MIT licensed**
- **CLI for installing source directly into your project**

From individual buttons and forms to complete AI SaaS platforms, dashboards, agencies, portfolios, and conference websites.

---

## What's Included?

### Components

Reusable UI components for common interface patterns.

- Buttons
- Inputs
- Forms
- Cards
- Navigation
- Modals
- Dropdowns
- Breadcrumbs
- Checkboxes
- Radios
- And more

### Sections

Complete page sections ready to drop into your projects.

- Hero sections
- Features
- Pricing
- Testimonials
- Contact
- Footers
- AI product sections
- Dashboard sections
- And more

### Templates

Complete multi-page websites built from composed sections and components.

Featured templates include:

- [AI SaaS Platform](Tailwind/Templates/ai-saas-platform/preview.html)
- [Northstar Vanilla Dashboard](Vanilla/Templates/SaaS%20Dashboard/)
- [Stratum](Tailwind/Templates/stratum/preview.html)
- [Northline Atelier](Tailwind/Templates/northline-atelier/preview.html)
- [Baseline Conference](Tailwind/Templates/baseline-conference/pages/index.html)

---

## Supported Technologies

| Technology | Library |
| --- | --- |
| Tailwind CSS | Components, sections & templates |
| React | Components, sections & templates |
| Vanilla | HTML, CSS & JavaScript |

Browse the libraries:

- [Tailwind](Tailwind/index.html)
- [React](React/index.html)
- [Vanilla](Vanilla/Sections/sections-index.html)

---

## DevSnips CLI

DevSnips now includes an official CLI for installing components, sections, and templates directly into your project.

### Install with npx

```bash
npx devsnips add <path>
```

### Examples

```bash
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
```

```bash
npx devsnips add React/Components/Buttons/solid-button
```

```bash
npx devsnips add Vanilla/Components/Buttons/split-button
```

The CLI fetches the requested source directly from DevSnips and installs it into:

```text
./devsnips/<technology>/<category>/<family>/<variant>/
```

For example:

```bash
npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
```

becomes:

```text
./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/
```

### CLI commands

```bash
npx devsnips --help
npx devsnips --version
```

Node.js 18 or newer is required.

Read the full [CLI documentation](cli/README.md).

---

## Quick Start

### Option 1: Use the CLI

Install what you need directly into your project:

```bash
npx devsnips add <path>
```

### Option 2: Clone the repository

```bash
git clone https://github.com/sarthakbystander/DevSnips.git
cd DevSnips
```

To browse the library locally:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/
```

---

## Design System

DevSnips follows a consistent design philosophy across its component library.

The system is built around:

* Reusable design tokens
* Consistent spacing
* Structured typography
* Responsive layouts
* Neutral-first foundations
* Controlled visual variation
* Accessibility-conscious interfaces
* Developer-friendly source code

The goal is simple: **different designs, consistent engineering.**

---

## Built For

DevSnips can be used for:

* AI SaaS products
* Dashboards
* Admin panels
* Business websites
* Agency websites
* Developer tools
* Landing pages
* Portfolios
* Conferences and events
* Product websites
* Personal projects

---

## Repository Structure

```text
DevSnips/
├── React/
├── Tailwind/
├── Vanilla/
├── cli/
├── docs/
├── scripts/
├── snippets-index.json
├── CHANGELOG.md
├── LICENSE
└── README.md
```

The `snippets-index.json` registry provides the structured index of available library content.

---

## Open Source

DevSnips is completely free and open source under the **MIT License**.

Use it in personal projects, commercial products, experiments, and anything else the MIT license permits.

Contributions, improvements, bug fixes, and new components are welcome.

---

## Links

* [GitHub Repository](https://github.com/sarthakbystander/DevSnips)
* [DevSnips CLI on npm](https://www.npmjs.com/package/devsnips)
* [Tailwind Library](Tailwind/index.html)
* [React Library](React/index.html)
* [Vanilla Library](Vanilla/Sections/sections-index.html)
* [Changelog](CHANGELOG.md)
* [License](LICENSE)

---

## License

MIT © Sarthak Bystander
