# AGENTS.md — Suna Studio

Guidance for an AI agent adapting this template. Read this before editing.

## What this template is

A single-page **React + TypeScript AI music studio** that generates **real songs** through
Suna AI's public Hugging Face Space (`johanjomet/suna-ai-studio`) via `@gradio/client`.
It ships the full Vite project. Every track is rendered by the live Space — the template
contains no mock generation, no fake audio URLs, and no fabricated progress states.

## Design system

**Soft lavender studio** — Plus Jakarta Sans (UI) + Fraunces (display); palette paper
`#F6F4FA`, ink `#211D31`, violet accent `#6F52D9`, night player `#151220`, soft cream
`#F5F1FF`. Rounded prompt-first composer cards on a paper canvas, a sidebar + top-bar
shell, a featured track card, and a fixed near-violet Spotify-style player at the bottom.
No glassmorphism, no neon, no gradient-built decoration. The visual system lives entirely
in `tailwind.config.ts` (colors, fonts), the token block at the top of `src/index.css`,
and the presentational components — it does not depend on the shared DevSnips `--ds-*`
tokens.

## File layout

```
suna-ai-studio/
├── index.html                 # Vite entry (theme-color, root mount)
├── package.json               # React 18, @gradio/client 2, Vite 5
├── vite.config.ts
├── tailwind.config.ts         # lavender/white color system, fonts, animations
├── postcss.config.js
├── tsconfig.json              # strict TypeScript
└── src/
    ├── main.tsx               # StrictMode + StudioProvider mount
    ├── App.tsx                # shell: TopBar, Sidebar, composer, session feed, footer
    ├── index.css              # CSS tokens, range styling, dialog/drawer rules
    ├── lib/                   # suna.ts (Gradio adapter), types.ts, palettes.ts,
    │                            format.ts, clipboard.ts, focus.ts
    ├── studio/
    │   └── StudioProvider.tsx # audio element, generation lifecycle, session state
    └── components/            # Composer, GenerationPanel, TrackCard, NowPlaying,
                                 PlayerBar, PlayerSheet, Sidebar, TopBar, MobileDrawer,
                                 SunaMark, TrackArtwork, Slider, Icon
```

## The external API (do not invent values)

`src/lib/suna.ts` is the single adapter. The contract was verified against the Space's
`/gradio_api/info` and its source (2026-10):

- endpoint `POST /gradio_api/call/v2/generate_suna_track`
- params in order: `user_prompt` · `artist_preset` · `custom_lyrics` · `duration_sec`
  (Space slider 24–68, step 4) · `speed_mode` · `uploaded_vocal` (optional) ·
  `vocal_mix` (0.30–1.20, step 0.05, default 0.88)
- returns `[mp3 FileData, wav FileData, telemetry string, lyricSheet string]`;
  render errors return `[null, null, "⚠️ …", lyrics]`
- `artist_preset` and `speed_mode` take **byte-exact enum strings** (emoji included) —
  they live in `SUNA_PRESETS` and `SUNA_QUALITY_MODES` and must never be paraphrased.
- availability probe: `GET /gradio_api/info` must contain `/generate_suna_track`
  in `named_endpoints`.

Known external limits to preserve in copy: ZeroGPU anonymous run quota (the queue may
close with zero events when the quota is spent — surface that honestly), Space-hosted
temp file URLs that expire with the session (hence session-only tracks), and no progress
percentage from Suna (show a real elapsed timer, never a fake bar).

## How to adapt it

1. **Re-theme:** colors and fonts are defined once in `tailwind.config.ts` + the token block in `src/index.css`; swapping the palette re-colors every surface consistently.
2. **Copy and ideas:** edit the `IDEAS` array in `src/components/Composer.tsx` and the shell copy in `src/App.tsx`.
3. **Presets/engines:** edit `SUNA_PRESETS` / `SUNA_QUALITY_MODES` in `src/lib/suna.ts`, keeping the `apiValue` strings byte-exact and the preset `lyrics` matching the Space's songbooks.
4. **Different Space host:** change the constants at the top of `src/lib/suna.ts` (and re-verify the endpoint shape against that Space's `/gradio_api/info`).
5. **Run:** `npm install` → `npm run dev`; `npm run build` (strict `tsc` + Vite → `dist/`).

## Do not

- Do not mock generation, hardcode audio URLs, or fake progress percentages, timers, or telemetry strings — every visible state must come from a real request or an honest absence.
- Do not paraphrase the Gradio enum values, endpoint name, or parameter names.
- Do not persist tracks, prompts, or audio to local storage or a backend — the session lives in the tab only.
- Do not remove the honest quota/capacity messaging, the `role="status"` generation card, labeled sliders, or the focus-managed player sheet/drawer.
- Do not hand-edit generated DevSnips indexes; regenerate them with the repository's indexing scripts after structural changes.

## Quality bar

Semantics (`header`, `main`, `aside`, `footer`, `form`), single `h1`, all sliders/buttons
labeled with `aria-label` + `aria-valuetext`, toggles via `aria-pressed`/radio groups,
`role="status"` generation card, polite toast live region, native `<dialog>` surfaces with
Escape-to-close and known-focus close buttons, global `:focus-visible` rings,
`prefers-reduced-motion` handling, and no horizontal overflow down to 390px. Run
`npm run build` (strict `tsc` type-check) and `python3 scripts/tooling/validators/validate.py`
after changes.
