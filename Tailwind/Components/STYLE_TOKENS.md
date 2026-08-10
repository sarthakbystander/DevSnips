# Tailwind/Components — Style Tokens (shared reference)

This file is the canonical design-token reference for every `Tailwind/Components/<category>/<section>/<style>/` variant (formerly under `Tailwind/Sections/`). All three styles must remain visually distinct and reuse the tokens below so the library stays cohesive across sections.

## Shared conventions (ALL styles)

- **3 files per variant folder**: `code.html` (snippet only — no `<!DOCTYPE>`, no `<html>`/`<head>`/`<body>`, no Tailwind CDN), `preview.html` (full `<!DOCTYPE html>` page + Tailwind CDN `https://cdn.tailwindcss.com` + app-context shell), `metadata.json`.
- `code.html` header comment (optional, per CONTRIBUTING.md):
  ```html
  <!--
  Snippet Name: <Name> — <Style>
  Description: <one line>
  Author: DevSnips Contributors
  Usage Example: <short>
  -->
  ```
- 2-space indentation. Semantic HTML. Accessibility: `aria-*`, keyboard, `focus-visible:ring`.
- JS pattern: scope with `document.currentScript.closest('[data-<scope>]')` so the snippet works in isolation.
- `metadata.json` keys: `name, slug, category, subcategory, section, style, description, framework, language, tags, features, responsive, dependencies`. `slug` = `<section>-<style>`.

## Style 1 — neo-brutalism
- **Fonts**: Archivo (500–900) display + JetBrains Mono labels. Load in preview: `https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700;800&display=swap`. Helper classes: `.font-archivo { font-family:'Archivo',sans-serif }`, `.font-mono { font-family:'JetBrains Mono',monospace }`.
- **Surfaces**: `bg-white` / `bg-[#FFFDF5]` cream. Hard `border-2 border-black`. Offset shadows `shadow-[8px_8px_0_0_#000]` (large), `shadow-[4px_4px_0_0_#000]` / `shadow-[3px_3px_0_0_#000]` / `shadow-[2px_2px_0_0_#000]` (small).
- **Accent colors** (flat, bright): `#FFE600` yellow, `#FF4FA3` pink, `#00E676` green, `#00C2FF` cyan.
- **Corners**: `rounded-none` or none; minimal radius.
- **Hover**: press-down: `transition-transform duration-100 hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[1px_1px_0_0_#000]` (shadow shrinks).
- **Labels**: uppercase, `font-mono text-[11px] font-bold tracking-wider`.
- **Body bg**: `bg-[#FFFDF5] text-black`. Optional grid bg: `.nb-grid-bg { background-image: linear-gradient(#000 1px,transparent 1px), linear-gradient(90deg,#000 1px,transparent 1px); background-size:28px 28px; }` used at low opacity behind titles.
- **scope attr**: `data-chat="nb"` / `data-<thing>="nb"`.

## Style 2 — vercel
- **Fonts**: Geist (300–700) + Geist Mono. Load in preview: `https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap`. Helpers: `.font-g { font-family:'Geist',sans-serif }`, `.vc-mono { font-family:'Geist Mono',ui-monospace,monospace }`.
- **Surfaces**: `bg-[#0a0a0a]` panel on `bg-[#050505]` body. Borders `border-white/10`, hairlines `border-white/[0.07]`. Panel shadow `shadow-[0_0_0_1px_rgba(255,255,255,0.02),0_20px_60px_-20px_rgba(0,0,0,0.9)]`. Rounded `rounded-[14px]` / `rounded-lg` / `rounded-full`.
- **Accent**: a single teal `#50e3c2` glowing dot: `.vc-dot { display:inline-block; height:6px; width:6px; border-radius:9999px; background:#50e3c2; box-shadow:0 0 8px #50e3c2; }`. White primary buttons `bg-white text-black`.
- **Text**: white/white-75/white-50/white-35 hierarchy.
- **Backdrop**: subtle conic/radial glow `.vc-grid-bg` (44px grid, masked) behind titles; panel radial glow `[background:radial-gradient(60%_60%_at_50%_0%,rgba(255,255,255,0.10),transparent_70%)]`.
- **Hover**: subtle `hover:bg-white/[0.06] hover:text-white` / `hover:border-white/20`.
- **code chip**: `.vc-code { font-family:'Geist Mono',monospace; font-size:12px; background:rgba(255,255,255,0.06); padding:1px 5px; border-radius:4px; color:rgba(255,255,255,0.9) }`.
- **scope attr**: `data-<thing>="vc"`.

## Style 3 — sharp-glassmorphism
- **Fonts**: Sora (400–700) + JetBrains Mono. Load in preview: `https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap`. Helpers: `.font-sora { font-family:'Sora',sans-serif }`, `.sg-mono { font-family:'JetBrains Mono',ui-monospace,monospace }`.
- **Glass**: `border border-white/20 bg-white/10 backdrop-blur-2xl` (panels), `bg-white/10 backdrop-blur-md` (bubbles), `bg-white/20 backdrop-blur` (icons). Rounded `rounded-2xl`/`rounded-xl`/`rounded-full`.
- **Gradient mesh body**: `.sg-mesh { background: radial-gradient(at 18% 18%, rgba(236,72,153,0.55) 0px, transparent 50%), radial-gradient(at 82% 12%, rgba(99,102,241,0.55) 0px, transparent 50%), radial-gradient(at 75% 78%, rgba(34,211,238,0.45) 0px, transparent 50%), radial-gradient(at 22% 82%, rgba(168,85,247,0.5) 0px, transparent 50%), #0b0a1f; background-size:180% 180%; animation: sg-pan 18s ease-in-out infinite alternate; } @keyframes sg-pan { 0%{background-position:0% 0%} 100%{background-position:100% 100%} }`.
- **Accents**: gradient `bg-gradient-to-r from-fuchsia-500 to-indigo-500` for primary buttons; cyan glow dot `.sg-dot { height:6px;width:6px;border-radius:9999px;background:#6ee7ff;box-shadow:0 0 8px #6ee7ff }`. `.sg-glow { box-shadow:0 0 0 1px rgba(255,255,255,0.08), 0 4px 20px -4px rgba(168,85,247,0.5) }` on icon chips.
- **Highlight edge**: top 1px gradient line `bg-gradient-to-r from-transparent via-white/50 to-transparent`.
- **code chip**: `.sg-code { font-family:'JetBrains Mono',monospace; font-size:12px; background:rgba(255,255,255,0.14); padding:1px 5px; border-radius:4px; color:#fff }`.
- **scope attr**: `data-<thing>="sg"`.
- NOTE: glass needs a colored backdrop behind the panel to read — always sit it on `.sg-mesh` (preview) or instruct the user the parent must provide a colored bg.

## metadata.json template (fill per variant)
```json
{
  "name": "<Section Title> — <Style>",
  "slug": "<section-slug>-<style>",
  "category": "Sections",
  "subcategory": "<category-slug>",
  "section": "<section-slug>",
  "style": "<style>",
  "description": "...",
  "framework": "Tailwind CSS",
  "language": "HTML",
  "tags": ["..."],
  "features": ["..."],
  "responsive": true,
  "dependencies": ["Tailwind CSS (CDN)", "Google Fonts: <fonts>"]
}
```
