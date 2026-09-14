# DevSnips Vanilla Design Tokens — "Swiss"

The canonical design-token system for DevSnips Vanilla components. Source of truth: `tokens.css` (this file documents it). The aesthetic is **neo-minimal Swiss** — neutral surfaces, hairline borders, restrained elevation, a single accent, system typography, generous space. Industry-standard scale aligned to Tailwind (so tokens feel familiar) and WCAG AA contrast on all text.

## How components opt in

Every migrated component references tokens as `var(--ds-<token>)` **with the original value as a fallback**, e.g. `border-radius: var(--ds-radius-md, 8px)`. This means:

- **Standalone**: a component is copy-paste ready and renders correctly even without `tokens.css` loaded (the fallback applies).
- **Cohesive**: include `tokens.css` once in a project and *every* component speaks the same visual language and upgrades together — re-theme by editing one file.
- **Safe migration**: the fallback preserves the original look, so migrating 200+ components cannot visually break them.

`tokens.css` lives at `Vanilla/Components/tokens.css` and is a single `:root` block + a `prefers-color-scheme: dark` override.

---

## Color — neutrals (stone ramp)

| Token | Light | Dark | Use |
|---|---|---|---|
| `--ds-bg` | `#ffffff` | `#0a0a0a` | page background |
| `--ds-surface` | `#ffffff` | `#111111` | card / panel |
| `--ds-surface-2` | `#f7f7f7` | `#171717` | raised panel |
| `--ds-surface-3` | `#ededed` | `#1f1f1f` | inset / muted panel |
| `--ds-foreground` | `#0a0a0a` | `#fafafa` | primary text |
| `--ds-muted` | `#525252` | `#a3a3a3` | secondary text |
| `--ds-subtle` | `#a3a3a3` | `#737373` | tertiary / placeholder |
| `--ds-border` | `#e5e5e5` | `#262626` | hairline 1px rule |
| `--ds-border-strong` | `#d4d4d4` | `#404040` | emphasis rule |

## Color — accent (single)

| Token | Light | Dark | Use |
|---|---|---|---|
| `--ds-accent` | `#2563eb` (blue-600) | `#3b82f6` | primary action |
| `--ds-accent-hover` | `#1d4ed8` | `#60a5fa` | hover |
| `--ds-accent-fg` | `#ffffff` | `#ffffff` | text on accent |
| `--ds-accent-soft` | `#eff6ff` | `#172554` | accent tint surface |

## Color — semantic status (WCAG AA on light)

| Token | Light | Dark | Use |
|---|---|---|---|
| `--ds-success` / `--ds-success-soft` | `#16a34a` / `#f0fdf4` | `#22c55e` / `#052e16` | success |
| `--ds-warning` / `--ds-warning-soft` | `#d97706` / `#fffbeb` | `#f59e0b` / `#422006` | warning (amber-600 for AA) |
| `--ds-danger` / `--ds-danger-soft` | `#dc2626` / `#fef2f2` | `#ef4444` / `#450a0a` | danger |
| `--ds-info` / `--ds-info-soft` | `#2563eb` / `#eff6ff` | `#3b82f6` / `#172554` | info |

## Typography

| Token | Value | Use |
|---|---|---|
| `--ds-font-sans` | system stack (Segoe UI, Roboto, Inter…) | body — no web-font dependency, Swiss "no ornamentation" |
| `--ds-font-mono` | ui-monospace, SF Mono, JetBrains Mono… | code / metadata |
| `--ds-text-xs`→`--ds-text-4xl` | `0.75rem`→`2.25rem` | size ramp |
| `--ds-leading-tight/normal/relaxed` | `1.25`/`1.5`/`1.625` | line-height |
| `--ds-weight-normal/medium/semibold/bold` | `400`/`500`/`600`/`700` | weight ramp |

## Spacing scale (base-4, Tailwind-aligned)

| Token | rem | px | |
|---|---|---|---|
| `--ds-space-0` | 0 | 0 | |
| `--ds-space-px` | 1px | 1 | |
| `--ds-space-0-5` | 0.125rem | 2 | |
| `--ds-space-1` | 0.25rem | 4 | |
| `--ds-space-1-5` | 0.375rem | 6 | |
| `--ds-space-2` | 0.5rem | 8 | |
| `--ds-space-3` | 0.75rem | 12 | |
| `--ds-space-4` | 1rem | 16 | |
| `--ds-space-5` | 1.25rem | 20 | |
| `--ds-space-6` | 1.5rem | 24 | |
| `--ds-space-8` | 2rem | 32 | |
| `--ds-space-10` | 2.5rem | 40 | |
| `--ds-space-12` | 3rem | 48 | |
| `--ds-space-16` | 4rem | 64 | |

## Radius scale

| Token | Value |
|---|---|
| `--ds-radius-none` | `0` |
| `--ds-radius-sm` | `0.25rem` (4px) |
| `--ds-radius-md` | `0.5rem` (8px) |
| `--ds-radius-lg` | `0.75rem` (12px) |
| `--ds-radius-xl` | `1rem` (16px) |
| `--ds-radius-2xl` | `1.5rem` (24px) |
| `--ds-radius-full` | `9999px` |

## Shadow scale (restrained)

Swiss minimal = subtle elevation, never the brutalist offset shadow.

| Token | Value |
|---|---|
| `--ds-shadow-none` | `none` |
| `--ds-shadow-sm` | `0 1px 2px 0 rgba(0,0,0,0.05)` |
| `--ds-shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -2px rgba(0,0,0,0.05)` |
| `--ds-shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.05)` |
| `--ds-shadow-focus` | `0 0 0 2px var(--ds-accent-soft), 0 0 0 4px var(--ds-accent)` |

## Motion

| Token | Value |
|---|---|
| `--ds-duration-fast` | `120ms` |
| `--ds-duration-normal` | `200ms` |
| `--ds-duration-slow` | `300ms` |
| `--ds-ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `--ds-ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` |

## Layout

| Token | Value | Use |
|---|---|---|
| `--ds-ring` | `0 0 0 2px var(--ds-accent)` | focus ring |
| `--ds-container` | `1200px` | max content width |
| `--ds-gutter` | `1rem` | container side padding |

---

## Migration rule (value → token)

Components are migrated deterministically by `_gen/migrate_tokens.py`. Each raw value is replaced with a `var(--ds-*, <original>)` reference so nothing changes visually until `tokens.css` is themed:

| Raw value (examples) | Token |
|---|---|
| `#ffffff`, `#fff`, `#fafafa`, `#f5f5f5`, `#f8f9fa` | `--ds-surface` / `--ds-bg` |
| `#0a0a0a`, `#000`, `#333`, `#151515` | `--ds-foreground` |
| `#525252`, `#666`, `#555` | `--ds-muted` |
| `#ddd`, `#ccc`, `#e5e5e5` | `--ds-border` |
| `#2563eb`, `#4a90e2`, `#4f46e5`, `#6366f1`, `#007bff` | `--ds-accent` |
| `#4caf50` | `--ds-success` |
| `#f44336` | `--ds-danger` |
| `Arial, sans-serif` | `--ds-font-sans` |
| `4px` / `8px` / `12px` (radius) | `--ds-radius-sm` / `md` / `lg` |
| `0 2px 5px rgba(0,0,0,0.1)` (shadow) | `--ds-shadow-md` |

Adoption is measured by `scripts/qa_vanilla.py --tokens` (counts `var(--ds-*)` vs raw values per component).
