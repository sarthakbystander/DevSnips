# PromptShelf starter

A lightweight static prompt-sharing starter built directly from DevSnips UI patterns.

## DevSnips resources used

- `Tailwind/Components/Buttons/basic-button/primary`
- `Tailwind/Components/Buttons/outline-button/primary`
- `Tailwind/Components/Cards/blog-card` as the content-card reference

The starter intentionally keeps the first version framework-free and data-driven. Prompt records currently live in `index.html`; the next step can move them into Markdown or JSON and generate one static page per prompt.

## Run locally

From the repository root:

```bash
python3 -m http.server 8080
```

Then open `/prompt-site/`.
