# Suna Studio Template

A production-ready, single-page **React + TypeScript AI music studio** that generates
**real songs** through [Suna AI's public Hugging Face Space](https://huggingface.co/spaces/johanjomet/suna-ai-studio)
via `@gradio/client`. The page is a prompt-first composer over a soft lavender dashboard,
with a Spotify-style dark player that plays, seeks, and downloads the Space's actual audio.

There is **no mock generation** in this template. Every track is rendered by the live
Space; every state (idle → connecting → composing → ready/unavailable) reflects the real
request, and the honest messages say exactly that.

## Highlights

- **Real generation** — `Client.connect("johanjomet/suna-ai-studio")` + `client.submit("/generate_suna_track", …)`.
- **Prompt-first composer** — Simple and Custom modes, idea chips, ⌘/Ctrl + ↵ submit, 500-char budget.
- **Six artist presets** — Indila Chanson, Matushka Folk-Pop, Power Ballad, Arena Rock, Afro-Latin Pop, Slap House — each stored with the Space's exact API values and its default songbook.
- **Editable lyrics** — the Custom mode exposes the same lyric sheet the Space edits; untouched songbooks follow preset changes just like the Space's UI.
- **Synthesis engine** — Turbo (8 steps) / High-Fidelity SFT (16 steps); **length** 24–68 s.
- **Sing-to-Masterpiece** — optional vocal clip (drop or browse, 25 MB) with a 0.30–1.20 vocal/band mix.
- **Honest states** — a real elapsed timer while the Space renders. Suna's queue exposes no progress percentage, and the UI says so instead of faking one. Space errors (quota, capacity, render failure) surface verbatim.
- **Session library** — tracks live in the tab only; rename, remove, clear, copy prompt.
- **Dark player bar** — near-violet bottom bar with play/pause, seek, ±10 s, volume, mute, MediaSession metadata; a full-screen mobile player sheet + session drawer.
- **Telemetry & lyrics** — the Space's studio telemetry and the word-aligned sung-lyric sheet are kept with each track.
- **Downloads** — prefer the 48 kHz 16-bit WAV master, fall back to the 320 kbps MP3.

## Design direction

**Soft lavender studio** — a calm instrument panel around a serious dark player:

- **Type:** Plus Jakarta Sans (UI, 400–800) + Fraunces (display).
- **Palette:** paper `#F6F4FA`, ink `#211D31`, violet accent `#6F52D9`, night player `#151220`, soft cream `#F5F1FF`.
- **Composition:** rounded 26px cards on a paper canvas, a sidebar + top bar shell, a featured track card that grows out of the composer, and the fixed near-violet player at the bottom. No glassmorphism, no neon, no decorative clutter.

The visual system lives entirely in `tailwind.config.ts` (colors, fonts), `src/index.css`
(tokens, range styling, dialog/drawer rules), and the presentational components — it does
not depend on the shared DevSnips `--ds-*` tokens.

## Structure

```text
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
    ├── lib/
    │   ├── suna.ts            # Gradio API adapter: presets, generate, probe, download
    │   ├── types.ts           # Track, SunaGenerateInput, generation + error types
    │   ├── palettes.ts        # artwork palettes
    │   ├── format.ts          # time/bytes helpers + titleFromPrompt
    │   ├── clipboard.ts       # copy helper
    │   └── focus.ts           # focus/keyboard helpers
    ├── studio/
    │   └── StudioProvider.tsx # audio element, generation lifecycle, session state
    └── components/
        ├── Composer.tsx       # Simple/Custom prompt-first composer
        ├── GenerationPanel.tsx# honest generation status card
        ├── TrackCard.tsx      # featured + compact track cards
        ├── NowPlaying.tsx     # expanded current-track panel
        ├── PlayerBar.tsx      # dark bottom player
        ├── PlayerSheet.tsx    # mobile full-screen player dialog
        ├── Sidebar.tsx        # session tracklist (desktop + drawer content)
        ├── TopBar.tsx         # brand + availability status
        ├── MobileDrawer.tsx   # mobile session drawer
        ├── SunaMark.tsx       # brand mark (SVG)
        ├── TrackArtwork.tsx   # generated per-track artwork
        ├── Slider.tsx         # accessible range styling
        └── Icon.tsx           # inline icon set
```

## Setup & run

Requires Node.js + npm. From the template root:

```bash
npm install
npm run dev        # Vite dev server — open the printed URL (usually http://localhost:5173)
```

Production build + local preview:

```bash
npm run build      # tsc type-check + Vite production build → dist/
npm run preview    # serve the built app
```

**Static preview:** `preview.html` at the template root is a self-contained static
prototype of the studio shell (Tailwind CDN + the real palette, composer, and dark player
chrome). It **cannot** generate audio — generation is intentionally disabled in the
preview, and the preview says so. Only the installed app talks to the Space.

## The Suna API contract

Everything lives in `src/lib/suna.ts`. Verified against
`https://johanjomet-suna-ai-studio.hf.space/gradio_api/info` + the Space's source (2026-10):

- `POST /gradio_api/call/v2/generate_suna_track`
- params (in order): `user_prompt` (str) · `artist_preset` (exact enum string) ·
  `custom_lyrics` (str, empty = the preset's songbook) · `duration_sec` (24–68 slider,
  server clips 20–68) · `speed_mode` (Turbo | High-Fidelity SFT enum string) ·
  `uploaded_vocal` (optional fingerprint/file) · `vocal_mix` (0.30–1.20, step 0.05)
- returns `[mp3 FileData, wav FileData, telemetry string, lyricSheet string]`;
  render errors return `[null, null, "⚠️ …", lyrics]`.
- `GET …/gradio_api/info` is used as the availability probe (`/generate_suna_track` must
  exist in `named_endpoints`).

The audio file URLs are Space-hosted `…/gradio_api/file=/tmp/gradio/…` links; they expire
with the Space's temp storage, which is why the library is session-only and downloads are
encouraged.

**Know the external limits.** The Space runs on ZeroGPU with an anonymous run quota; when
the quota is spent for your connection the queue may close with no events — the template
says so honestly and asks you to retry later. Streaming the returned audio from the page
works because the Space sends CORS headers (verified).

## Customization

- **Palette & fonts:** defined once in `tailwind.config.ts` + the token block at the top of `src/index.css`.
- **Presets:** `SUNA_PRESETS` in `src/lib/suna.ts` — ids, labels, palettes, and the default songbook the composer autofills. Keep the `apiValue` strings byte-exact.
- **Engine modes:** `SUNA_QUALITY_MODES`, same byte-exact rule.
- **Copy/ideas:** the `IDEAS` array in `src/components/Composer.tsx` and the shell copy in `src/App.tsx`.
- **Host change:** if you fork/deploy the Space, change the constants at the top of `src/lib/suna.ts` (`SUNA_SPACE_ID`, `SUNA_HOST`).

## Accessibility

- Landmark structure (`header`, `main`, `aside`, `footer`, `form`), single `h1`.
- All controls labeled: sliders (`aria-label`, `aria-valuetext`), toggles (`aria-pressed`/radio groups), player buttons with explicit names.
- Generation status card uses `role="status"`; toasts use a polite live region.
- Player sheet is a native `<dialog>` with focus on close control and Escape to dismiss; the drawer behaves the same.
- Global `:focus-visible` rings; `prefers-reduced-motion` disables floating/idle animations (verified in `src/index.css`).

## Browser support

Modern evergreen browsers. Playback uses native `HTMLAudioElement` with MediaSession;
generation requires WebSockets/SSE for the Gradio queue stream.
