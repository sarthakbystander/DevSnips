# Agent discovery

Discovery is how an agent finds DevSnips and its inventory. DevSnips exposes several structured surfaces; all of them derive from the same registry, so an agent can pick whichever is cheapest to reach.

## Discoverable surfaces

| Surface | What it contains | Best for |
|---|---|---|
| `snippets-index.json` (registry) | Every family and variant: tech, type, category, paths, descriptions, tags, features, styles, file manifests, counts. | The authoritative inventory query. |
| `agents/resources/indexes/components-index.json` | Components only, with `id` and a ready-to-run `install` command per variant. | Answering "find/install a component…" without scanning the full registry. |
| `agents/resources/indexes/sections-index.json` | Sections only, same shape. | Section-scoped queries. |
| `agents/resources/indexes/templates-index.json` | Templates only, same shape. | Template-scoped queries. |
| `website/llms.txt` | Every resource as a Markdown link list, grouped by technology and category. | A compact, human/LLM-readable inventory with URLs. |
| `website/llms-full.txt` | The same list with descriptions and tags inline per entry. | Evaluating resources without fetching the registry. |
| `website/search-index.json` | Flat array of per-resource records (`id`, `type`, `technology`, `category`, `family`, `slug`, `name`, `description`, `tags`, `features`, `related`, `url`). | Client-side search integration. |
| `website/sitemap.xml` | All resource page URLs. | URL enumeration. |

Registry URLs (also recorded in the skill's frontmatter):

```text
https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json
https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/agents/resources/indexes/components-index.json
https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/agents/resources/indexes/sections-index.json
https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/agents/resources/indexes/templates-index.json
```

Prefer the raw URL over the GitHub web page URL when fetching structured data.

## How an agent is expected to discover DevSnips

1. **Via the agent skill.** If the host agent supports skills, the `devsnips` skill declares its triggers in its frontmatter description ("use DevSnips", "add a DevSnips button", or UI requests likely satisfied by a DevSnips resource). Installing the skill is the intended integration path.
2. **Via repository context.** A project that uses DevSnips contains `devsnips/AGENTS.md` (created by the CLI) telling agents that resources are installed under `devsnips/`, and `devsnips/config.json` listing what is already installed. An agent entering such a project reads these before touching UI.
3. **Via web search / website.** The website is fully indexed (sitemap, robots allow-all) and carries LLM-oriented digests. An agent that lands on `devsnips.dev` should follow the pointers to the registry rather than scraping pages.

## Querying the registry

Work type-first, then technology, then semantics:

```text
Pick the index by type (components / sections / templates)
    → filter families on tech   (exact strings: "React", "Tailwind CSS", "Vanilla HTML/CSS/JS")
    → filter families on path   (e.g. contains "Components/Buttons")
    → match intent against family name + tags + variant description/tags/features/styles
    → read the variant's files manifest to know what will be installed
```

Typical queries answerable from the indexes alone:

- "Find React button components" → components index, `tech == "React"`, family path containing `Components/Buttons`.
- "Find Tailwind pricing sections" → sections index, `tech == "Tailwind CSS"`, family path containing `Sections/Pricing`.
- "What does the split button contain?" → the variant's `files` array; deeper structure lives at `library/<path>` on disk.
- "Give me the install command" → the entry's `install` field (specialized indexes only).

## Rules

- Match against `tags`, `searchTerms`, and `features`, not only names. Some intents (e.g. "hamburger menu") surface only through tags on a differently named family (e.g. Navigation).
- Filter by the host project's actual stack, inspected first — do not default to Tailwind.
- Registry entries are snapshots. If an entry disagrees with the disk, the disk wins; regenerate and re-validate rather than patching the JSON.
- Answer inventory questions only from a registry fetched in the current session. Counts change.
