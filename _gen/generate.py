"""Main generator: writes all 165 section-style component folders and updates the index."""
import json
import os
from pathlib import Path

from .styles import TOKENS, STYLE_NAMES
from .helpers import ic, ICONS, logo_svg
from .builders_testimonials import testimonials
from .builders_faq import faq
from .builders_contact import contact
from .builders_footer import footer
from .builders_navbar import navbar
from .builders_stats import stats
from .builders_team import team
from .builders_blog import blog
from .builders_logos import logos
from .builders_newsletter import newsletter
from .builders_404 import error_page

ROOT = Path(__file__).resolve().parent.parent
# Generated section-style content lives under Tailwind/Sections/ — Sections are a
# first-class content type alongside Components/ and Templates/ in the Tailwind IA.
SECTIONS = ROOT / "Tailwind" / "Sections"

BUILDERS = [
    ("Testimonials", testimonials),
    ("FAQ", faq),
    ("Contact", contact),
    ("Footer", footer),
    ("Navbar", navbar),
    ("Stats", stats),
    ("Team", team),
    ("Blog", blog),
    ("Logos", logos),
    ("Newsletter", newsletter),
    ("404", error_page),
]

# Fixed style rotation per category for even distribution + uniqueness.
# Each category maps concept-index -> style.
CATEGORY_STYLES = [
    "neo-brutalism", "edge-glassmorphism", "vercel", "minimal", "apple-inspired",
    "bento-grid", "editorial", "dark-premium", "startup-landing", "futuristic",
    "gradient-mesh", "soft-ui", "cyber", "monochrome", "elegant-luxury",
]


def style_for(cat_index, concept_index):
    """Rotate styles so distribution is even and each category spans a wide range."""
    offset = (cat_index * 4) % 15
    return CATEGORY_STYLES[(concept_index + offset) % 15]


def preview_shell(builder_result, style, cat, n):
    b = TOKENS[style]
    font_url = b["font_url"]
    # CSS helper classes per style
    head_css = b["head_css"]
    # Body background: if style has decor (fixed bg), apply via body class; otherwise use body_class
    decor = b.get("decor", "")
    body_bg = b["body_class"]
    title = "%s — %s | DevSnips" % (builder_result["section_name"], STYLE_NAMES[style])
    snippet_comment = (
        "<!--\nSnippet Name: %s — %s\nDescription: %s\nAuthor: DevSnips Contributors\n"
        "Usage Example: Drop this %s section into any page using Tailwind CSS.\n-->"
    ) % (builder_result["section_name"], STYLE_NAMES[style], builder_result["desc"], cat.lower())
    # For navbar/footer the section element differs; builder_result["code"] already includes it.
    code = snippet_comment + "\n" + builder_result["code"]
    # Add the style's decor inside body for preview
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%s</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="%s" rel="stylesheet">
  <style>%s</style>
</head>
<body class="min-h-screen %s antialiased">
%s
  %s
</body>
</html>""" % (title, font_url, head_css, body_bg, decor, code)


def code_snippet(builder_result, style):
    snippet_comment = (
        "<!--\nSnippet Name: %s — %s\nDescription: %s\nAuthor: DevSnips Contributors\n"
        "Usage Example: Drop this snippet into any Tailwind CSS page.\n-->"
    ) % (builder_result["section_name"], STYLE_NAMES[style], builder_result["desc"])
    return snippet_comment + "\n" + builder_result["code"]


def metadata(builder_result, style, cat, n, style_key):
    b = TOKENS[style]
    cat_slug = cat.lower().replace(" ", "-")
    slug = "%s-%s" % (cat_slug, style_key)
    return {
        "id": slug,
        "slug": slug,
        "name": "%s — %s" % (builder_result["section_name"], STYLE_NAMES[style]),
        "technology": "tailwind",
        "type": "section",
        "category": "Sections",
        "subcategory": cat.lower(),
        "section": builder_result["section_name"],
        "style": style_key,
        "description": builder_result["desc"],
        "framework": "Tailwind CSS",
        "language": "HTML",
        "tags": builder_result["tags"],
        "features": builder_result["features"],
        "responsive": True,
        "darkMode": style in ("vercel", "dark-premium", "edge-glassmorphism", "bento-grid", "futuristic", "cyber", "gradient-mesh", "elegant-luxury"),
        "accessibility": True,
        "browserSupport": ["Chrome", "Firefox", "Safari", "Edge"],
        "dependencies": ["Tailwind CSS (CDN)", "Google Fonts"],
    }


def readme(builder_result, style, cat, n):
    style_key = style
    md = """# %s — %s

> %s

![Preview](./preview.html)

## Features

%s

## Responsive support

- Mobile-first layout
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px)
- Stacks gracefully on small screens, expands on large viewports

## Browser support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Usage

1. Copy the markup from `code.html` into your Tailwind CSS project.
2. Include the corresponding Google Fonts in your document `<head>` if the style requires them.
3. The snippet is self-contained and copy-paste ready — no build step or JavaScript required.

## Design language

**%s** — part of the DevSnips Tailwind Sections library. Every section is
original, accessible, and production-ready.

## Files

- `preview.html` — full standalone preview page (Tailwind CDN + fonts)
- `code.html` — copy-paste snippet only (no `<head>` / CDN)
- `metadata.json` — structured metadata
- `README.md` — this file
""" % (
        builder_result["section_name"], STYLE_NAMES[style], builder_result["desc"],
        "\n".join("- " + f for f in builder_result["features"]),
        STYLE_NAMES[style],
    )
    return md


def generate(dry_run=False):
    written = []
    index_entries = []  # (cat, n, style_key, builder_result, path)
    for ci, (cat, builder) in enumerate(BUILDERS):
        cat_dir = SECTIONS / cat
        if not dry_run:
            cat_dir.mkdir(parents=True, exist_ok=True)
        for n in range(15):
            style_key = style_for(ci, n)
            result = builder(style_key, n)
            sec_dir = cat_dir / style_key
            if not dry_run:
                sec_dir.mkdir(parents=True, exist_ok=True)
                (sec_dir / "preview.html").write_text(preview_shell(result, style_key, cat, n), encoding="utf-8")
                (sec_dir / "code.html").write_text(code_snippet(result, style_key), encoding="utf-8")
                (sec_dir / "metadata.json").write_text(json.dumps(metadata(result, style_key, cat, n, style_key), indent=2), encoding="utf-8")
                (sec_dir / "README.md").write_text(readme(result, style_key, cat, n), encoding="utf-8")
            written.append((cat, n, style_key, str(sec_dir)))
            index_entries.append((cat, n, style_key, result, sec_dir))
    return written, index_entries


if __name__ == "__main__":
    w, idx = generate(dry_run=False)
    print("Wrote", len(w), "sections")
    # quick count check
    from collections import Counter
    c = Counter(x[2] for x in w)
    print("Style distribution:", dict(c))
    c2 = Counter(x[0] for x in w)
    print("Per category:", dict(c2))
