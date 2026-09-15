#!/usr/bin/env python3
"""
DevSnips static site generator.
Walks Tailwind/ Vanilla/ React/ (Components, Sections, Templates), reads each
item's metadata.json + README.md, and emits a fully cross-linked static
site into site/ with:
  - shared navbar/footer on every page
  - home page
  - technology hub pages (Tailwind/Vanilla/React)
  - category index pages (Components/Sections/Templates per technology)
  - family group pages (e.g. Tailwind > Sections > 404)
  - a detail page per item (preview + code + metadata + features + related + docs)
  - a template detail page (multi-page templates)
  - a documentation hub page
All internal links are relative and correct; "Preview" always opens the
real preview.html (or index.html for templates) in a new tab.

Usage (works from any CWD, no hardcoded paths):
  python3 _gen/gen_site.py

Branding assets are read from this directory (_gen/):
  - style_extra.css  -> copied to site/assets/style.css  (light cadet gray theme)
  - logo.svg         -> original uploaded mark kept for reference; an
                        adaptive copy is written to site/assets/logo.svg
                        (favicon) and the navbar embeds the same mark
                        inline with currentColor so it adapts to
                        light/dark mode automatically.
"""
import json, os, re, shutil, html as htmllib

# Paths are resolved relative to this script so the generator works from any
# CWD and any machine: script lives in <repo>/_gen/, site is emitted to <repo>/site/.
GEN_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(GEN_DIR)
SITE = os.path.join(ROOT, "site")
TECHS = ["Tailwind", "Vanilla", "React"]

def rd(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def load_json(path):
    try:
        return json.loads(rd(path))
    except Exception:
        return {}

# ---------------------------------------------------------------- markdown -
def md_to_html(md):
    """Small, dependency-free markdown -> HTML for README rendering."""
    lines = md.replace("\r\n", "\n").split("\n")
    out, in_list, in_code = [], False, False
    for ln in lines:
        if ln.strip().startswith("```"):
            if in_code:
                out.append("</code></pre>")
            else:
                out.append('<pre class="code-block"><code>')
            in_code = not in_code
            continue
        if in_code:
            out.append(htmllib.escape(ln))
            continue
        s = ln.strip()
        if s.startswith("### "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f"<h3>{inline_md(s[4:])}</h3>")
        elif s.startswith("## "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f"<h2>{inline_md(s[3:])}</h2>")
        elif s.startswith("# "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f"<h1>{inline_md(s[2:])}</h1>")
        elif s.startswith("> "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f"<blockquote>{inline_md(s[2:])}</blockquote>")
        elif s.startswith("- ") or s.startswith("* "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline_md(s[2:])}</li>")
        elif re.match(r"^\d+\.\s", s):
            if not in_list:
                out.append("<ol>"); in_list = "ol"
            out.append(f"<li>{inline_md(re.sub(r'^\d+\.\s', '', s))}</li>")
        elif s == "":
            if in_list:
                out.append("</ul>" if in_list is True else "</ol>")
                in_list = False
        else:
            if in_list:
                out.append("</ul>" if in_list is True else "</ol>")
                in_list = False
            out.append(f"<p>{inline_md(s)}</p>")
    if in_list:
        out.append("</ul>" if in_list is True else "</ol>")
    return "\n".join(out)

def inline_md(s):
    s = htmllib.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", "", s)  # drop image embeds (previews)
    # relative (non-http) links in READMEs point at sibling repo files whose depth
    # differs per generated page; render as plain code instead of a dead link.
    def _link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "mailto:")):
            return f'<a href="{href}">{label}</a>'
        return f'<code>{label}</code>'
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, s)
    return s

# ------------------------------------------------------------- collection --
def collect():
    """Returns nested dict: tech -> category -> family -> [items], plus templates list."""
    data = {t: {"Components": {}, "Sections": {}, "Templates": []} for t in TECHS}
    for tech in TECHS:
        for cat in ["Components", "Sections"]:
            base = os.path.join(ROOT, tech, cat)
            if not os.path.isdir(base):
                continue
            for family in sorted(os.listdir(base)):
                fam_dir = os.path.join(base, family)
                if not os.path.isdir(fam_dir):
                    continue
                items = []
                for variant in sorted(os.listdir(fam_dir)):
                    vdir = os.path.join(fam_dir, variant)
                    meta_path = os.path.join(vdir, "metadata.json")
                    if not os.path.isdir(vdir) or not os.path.isfile(meta_path):
                        continue
                    has_own_code = any(
                        os.path.isfile(os.path.join(vdir, f))
                        for f in ("code.html", "code.tsx", "code.jsx", "preview.html")
                    )
                    nested = [
                        d for d in sorted(os.listdir(vdir))
                        if os.path.isdir(os.path.join(vdir, d)) and os.path.isfile(os.path.join(vdir, d, "metadata.json"))
                    ]
                    if not has_own_code and nested:
                        # this is a "group" dir (e.g. outline-button/{primary,dashed,thick})
                        # with no leaf files of its own -- descend into its sub-variants.
                        for sub in nested:
                            sdir = os.path.join(vdir, sub)
                            smeta = load_json(os.path.join(sdir, "metadata.json"))
                            sreadme = rd(os.path.join(sdir, "README.md")) if os.path.isfile(os.path.join(sdir, "README.md")) else ""
                            sfiles = sorted(os.listdir(sdir))
                            smeta.setdefault("name", f"{variant.replace('-', ' ').title()} — {sub.replace('-', ' ').title()}")
                            items.append({
                                "tech": tech, "category": cat, "family": family,
                                "slug": f"{variant}-{sub}", "dir": sdir, "meta": smeta,
                                "readme": sreadme, "files": sfiles,
                            })
                        continue
                    meta = load_json(meta_path)
                    readme = ""
                    if os.path.isfile(os.path.join(vdir, "README.md")):
                        readme = rd(os.path.join(vdir, "README.md"))
                    files = sorted(os.listdir(vdir))
                    items.append({
                        "tech": tech, "category": cat, "family": family,
                        "slug": variant, "dir": vdir, "meta": meta,
                        "readme": readme, "files": files,
                    })
                if items:
                    data[tech][cat][family] = items
        # templates
        tbase = os.path.join(ROOT, tech, "Templates")
        if os.path.isdir(tbase):
            for tname in sorted(os.listdir(tbase)):
                tdir = os.path.join(tbase, tname)
                meta_path = os.path.join(tdir, "metadata.json")
                if not os.path.isdir(tdir) or not os.path.isfile(meta_path):
                    continue
                meta = load_json(meta_path)
                readme = rd(os.path.join(tdir, "README.md")) if os.path.isfile(os.path.join(tdir, "README.md")) else ""
                pages = []
                pages_dir = os.path.join(tdir, "pages")
                if os.path.isdir(pages_dir):
                    pages = sorted(f for f in os.listdir(pages_dir) if f.endswith(".html"))
                entry_dir = os.path.isdir(os.path.join(tdir, "src"))  # react app-style
                data[tech]["Templates"].append({
                    "tech": tech, "family": "Templates", "slug": tname,
                    "dir": tdir, "meta": meta, "readme": readme,
                    "pages": pages, "is_app": entry_dir,
                })
    return data

# ------------------------------------------------------------------ paths --
def item_dir_out(it):
    return os.path.join(SITE, it["tech"], it["category"], it["family"], it["slug"])

def ensure_local_src(it):
    """Copy the item's real source folder into its own detail-page folder
    (as _src/) so the deployed site/ is fully self-contained — no reaching
    outside the site root for previews/code, so it works no matter where
    site/ is deployed (with or without a /site/ prefix)."""
    dest = os.path.join(item_dir_out(it), "_src")
    if not os.path.isdir(dest):
        shutil.copytree(it["dir"], dest)
    return dest

def rel_source(it, fname):
    """Link from the generated detail page to its own local copy of a source file."""
    ensure_local_src(it)
    return f"_src/{fname}"

def tmpl_dir_out(t):
    return os.path.join(SITE, t["tech"], "Templates", t["slug"])

def ensure_local_src_tmpl(t):
    dest = os.path.join(tmpl_dir_out(t), "_src")
    if not os.path.isdir(dest):
        shutil.copytree(t["dir"], dest)
    return dest

def rel_source_tmpl(t, relpath):
    ensure_local_src_tmpl(t)
    return f"_src/{relpath}"

def root_rel(out_dir):
    depth = len(os.path.relpath(out_dir, SITE).split(os.sep))
    return "../" * depth


# --------------------------------------------------------------- layout ---
def page(title, description, body, root, active="", extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{htmllib.escape(title)}</title>
<meta name="description" content="{htmllib.escape(description)}">
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config = {{ darkMode: 'class' }};
(function(){{var s=localStorage.getItem('devsnips-theme');var d=s?s==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;if(d)document.documentElement.classList.add('dark');}})();</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="{root}assets/logo.svg">
<link rel="stylesheet" href="{root}assets/style.css">
{extra_head}
</head>
<body class="min-h-screen bg-white text-neutral-900 dark:bg-[#0a0a0a] dark:text-neutral-100 antialiased">
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-3 focus:left-3 focus:rounded-md focus:bg-white focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:shadow dark:focus:bg-neutral-900 dark:focus:text-white">Skip to content</a>
{navbar(root, active)}
<main id="main">
{body}
</main>
{footer(root)}
<script>
var btn=document.getElementById('theme-toggle');
btn.addEventListener('click',function(){{var d=document.documentElement.classList.toggle('dark');localStorage.setItem('devsnips-theme',d?'dark':'light');}});
var mbtn=document.getElementById('mobile-menu-btn'),mnav=document.getElementById('mobile-nav');
if(mbtn){{mbtn.addEventListener('click',function(){{mnav.classList.toggle('hidden');}});}}
</script>
</body>
</html>
"""

# ------------------------------------------------------------------ logo --
LOGO_VIEWBOX = "0 0 680 620"
LOGO_PATHS = (
    '<path d="M113 100 H233 V193 H196 V233 H233 V567 H113 V233 H150 V193 H113 Z"/>'
    '<path d="M278 100 H577 V181 L360 200 L360 233 H577 V307 H360 V351 H577 V567 H278 Z"/>'
)

def logo_svg_inline(cls="h-8 w-auto"):
    """Inline brand mark; currentColor keeps it visible in light and dark mode."""
    return (f'<svg viewBox="{LOGO_VIEWBOX}" class="{cls}" fill="currentColor" '
            f'aria-hidden="true">{LOGO_PATHS}</svg>')

# Standalone logo file for favicon/og-image use; adapts to browser color scheme.
LOGO_FILE_SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{LOGO_VIEWBOX}" width="680" height="620" role="img">
<title>iE logo</title>
<desc>Bold black geometric logo reading "iE".</desc>
<style>path{{fill:#000000}}@media (prefers-color-scheme:dark){{path{{fill:#ffffff}}}}</style>
{LOGO_PATHS}
</svg>'''

def navbar(root, active):
    def link(label, href, key):
        cls = "text-slate-500 dark:text-slate-400" if active == key else "text-neutral-700 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white"
        return f'<a href="{href}" class="text-sm font-semibold {cls} transition">{label}</a>'
    items = [
        ("Home", f"{root}index.html", "home"),
        ("Tailwind", f"{root}Tailwind/index.html", "tailwind"),
        ("Vanilla", f"{root}Vanilla/index.html", "vanilla"),
        ("React", f"{root}React/index.html", "react"),
        ("Docs", f"{root}docs/index.html", "docs"),
    ]
    desktop = "\n      ".join(link(l, h, k) for l, h, k in items)
    mobile = "\n      ".join(f'<a href="{h}" class="block rounded-lg px-3 py-2 text-sm font-semibold hover:bg-neutral-100 dark:hover:bg-neutral-900">{l}</a>' for l, h, k in items)
    return f"""<header class="sticky top-0 z-30 border-b border-neutral-200/80 bg-white/80 backdrop-blur dark:border-neutral-800 dark:bg-[#0a0a0a]/80">
  <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
    <a href="{root}index.html" class="flex items-center gap-2.5 font-extrabold tracking-tight">
      {logo_svg_inline("h-8 w-auto text-neutral-900 dark:text-white")}
      DevSnips
    </a>
    <nav class="hidden items-center gap-6 md:flex" aria-label="Primary">
      {desktop}
    </nav>
    <div class="flex items-center gap-2">
      <button id="theme-toggle" type="button" aria-label="Toggle color theme"
        class="rounded-md border border-neutral-300 px-3 py-1.5 text-sm font-semibold hover:bg-neutral-100 dark:border-neutral-700 dark:hover:bg-neutral-900">
        <span class="dark:hidden">&#9789; Dark</span><span class="hidden dark:inline">&#9728; Light</span>
      </button>
      <button id="mobile-menu-btn" type="button" aria-label="Toggle menu" class="rounded-md border border-neutral-300 px-3 py-1.5 text-sm font-semibold md:hidden dark:border-neutral-700">&#9776;</button>
    </div>
  </div>
  <div id="mobile-nav" class="hidden border-t border-neutral-200 px-4 py-3 md:hidden dark:border-neutral-800">
    {mobile}
  </div>
</header>"""

def footer(root):
    return f"""<footer class="border-t border-neutral-200 dark:border-neutral-800">
  <div class="mx-auto max-w-6xl px-4 py-10 text-sm text-neutral-500 sm:px-6 dark:text-neutral-400">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <span>DevSnips &middot; open-source frontend component library</span>
      <nav class="flex flex-wrap gap-4" aria-label="Footer">
        <a href="{root}index.html" class="hover:text-neutral-900 dark:hover:text-white">Home</a>
        <a href="{root}Tailwind/index.html" class="hover:text-neutral-900 dark:hover:text-white">Tailwind</a>
        <a href="{root}Vanilla/index.html" class="hover:text-neutral-900 dark:hover:text-white">Vanilla</a>
        <a href="{root}React/index.html" class="hover:text-neutral-900 dark:hover:text-white">React</a>
        <a href="{root}docs/index.html" class="hover:text-neutral-900 dark:hover:text-white">Documentation</a>
      </nav>
    </div>
  </div>
</footer>"""

def breadcrumb(root, crumbs):
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if href:
            parts.append(f'<a href="{href}" class="hover:text-neutral-900 dark:hover:text-white">{htmllib.escape(label)}</a>')
        else:
            parts.append(f'<span class="text-neutral-900 dark:text-white">{htmllib.escape(label)}</span>')
    sep = '<span class="mx-1.5 text-neutral-400">/</span>'
    return f'<nav aria-label="Breadcrumb" class="mono flex flex-wrap items-center text-xs text-neutral-500 dark:text-neutral-400">{sep.join(parts)}</nav>'

def badge(text, color="neutral"):
    palette = {
        "slate": "bg-slate-100 text-slate-700 dark:bg-slate-900 dark:text-slate-300",
        "emerald": "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300",
        "amber": "bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300",
        "sky": "bg-sky-50 text-sky-700 dark:bg-sky-950 dark:text-sky-300",
        "neutral": "bg-neutral-100 text-neutral-700 dark:bg-neutral-900 dark:text-neutral-300",
    }
    return f'<span class="mono rounded-full px-2.5 py-1 text-xs font-semibold {palette.get(color,palette["neutral"])}">{htmllib.escape(text)}</span>'

TECH_COLOR = {"Tailwind": "slate", "Vanilla": "emerald", "React": "sky"}

# ----------------------------------------------------------------- write --
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def card(href, eyebrow, title, desc, color, meta_line=""):
    return f"""<a href="{href}" class="group flex flex-col rounded-2xl border border-neutral-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-{color}-400 hover:shadow-lg dark:border-neutral-800 dark:bg-neutral-950 dark:hover:border-{color}-500">
  <span class="mono text-[11px] font-semibold uppercase tracking-widest text-{color}-600 dark:text-{color}-400">{htmllib.escape(eyebrow)}</span>
  <h3 class="mt-2 text-base font-bold group-hover:text-{color}-600 dark:group-hover:text-{color}-400">{htmllib.escape(title)}</h3>
  <p class="mt-1.5 line-clamp-2 text-sm text-neutral-600 dark:text-neutral-400">{htmllib.escape(desc)}</p>
  {f'<span class="mono mt-3 text-[11px] text-neutral-400">{htmllib.escape(meta_line)}</span>' if meta_line else ''}
</a>"""

# ---- HOME ----
def build_home(data):
    tech_cards = []
    icons = {"Tailwind": "&#127912;", "Vanilla": "&#9881;&#65039;", "React": "&#9883;&#65039;"}
    blurb = {
        "Tailwind": "Utility-first components, sections, and full page templates.",
        "Vanilla": "Framework-free HTML/CSS/JS &mdash; copy, paste, ship.",
        "React": "TypeScript-first components, sections, and app templates.",
    }
    for t in TECHS:
        n_comp = sum(len(v) for v in data[t]["Components"].values())
        n_sec = sum(len(v) for v in data[t]["Sections"].values())
        n_tmpl = len(data[t]["Templates"])
        color = TECH_COLOR[t]
        tech_cards.append(f"""
        <a href="{t}/index.html" class="group flex flex-col rounded-2xl border border-neutral-200 bg-white p-6 transition hover:-translate-y-1 hover:border-{color}-400 hover:shadow-lg dark:border-neutral-800 dark:bg-neutral-950 dark:hover:border-{color}-500">
          <span class="mono text-xs font-semibold uppercase tracking-widest text-{color}-600 dark:text-{color}-400">{t}</span>
          <span class="mt-4 text-4xl">{icons[t]}</span>
          <h3 class="mt-4 text-lg font-bold">{t}</h3>
          <p class="mt-2 text-sm text-neutral-600 dark:text-neutral-400">{blurb[t]}</p>
          <span class="mt-5 inline-flex flex-wrap gap-2 text-xs">
            {badge(f"{n_comp} Components", color)}
            {badge(f"{n_sec} Sections", color)}
            {badge(f"{n_tmpl} Templates", color)}
          </span>
        </a>""")
    body = f"""
  <section class="mx-auto max-w-6xl px-4 py-14 sm:px-6 sm:py-20">
    <p class="mono mb-3 text-xs font-semibold uppercase tracking-widest text-slate-500 dark:text-slate-400">framework-free frontend library</p>
    <h1 class="max-w-3xl text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl">Reusable frontend snippets, organized as design-system families.</h1>
    <p class="mt-4 max-w-2xl text-base text-neutral-600 dark:text-neutral-400 sm:text-lg">Browse by technology. Every component, section, and template has a real, working detail page: live preview, copy-paste code, metadata, and documentation.</p>
    <div class="mt-6 flex flex-wrap gap-3">
      <a href="docs/index.html" class="rounded-lg bg-slate-500 px-4 py-2 text-sm font-bold text-white hover:bg-slate-600">Read the docs</a>
      <a href="Tailwind/index.html" class="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-bold hover:bg-neutral-100 dark:border-neutral-700 dark:hover:bg-neutral-900">Browse Tailwind</a>
    </div>
  </section>
  <section class="mx-auto max-w-6xl px-4 pb-20 sm:px-6" aria-label="Technologies">
    <div class="grid gap-5 md:grid-cols-3">{''.join(tech_cards)}</div>
  </section>"""
    write(os.path.join(SITE, "index.html"), page(
        "DevSnips — Frontend component library",
        "DevSnips is an open-source, framework-free frontend component library. Browse Tailwind, Vanilla, and React content by type.",
        body, "", "home"))

# ---- TECH HUB (e.g. site/Tailwind/index.html) ----
def build_tech_hub(data, tech):
    root = "../"
    color = TECH_COLOR[tech]
    def cat_block(cat, families):
        if not families:
            return ""
        fam_cards = []
        for fam, items in sorted(families.items()):
            fam_cards.append(card(
                f"{cat}/index.html#{fam}",
                fam, f"{fam} ({len(items)})", items[0]["meta"].get("description", ""), color,
                f"{len(items)} variant{'s' if len(items)!=1 else ''}"
            ))
        return f"""
    <div class="mt-10">
      <div class="flex items-baseline justify-between">
        <h2 class="text-xl font-bold">{cat}</h2>
        <a href="{cat}/index.html" class="text-sm font-semibold text-{color}-600 hover:underline dark:text-{color}-400">View all &rarr;</a>
      </div>
      <div class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{''.join(fam_cards)}</div>
    </div>"""
    tmpl_cards = "".join(
        card(f"Templates/{t['slug']}/index.html", "Template", t["meta"].get("name", t["slug"]),
             t["meta"].get("description", ""), color, f"{len(t['pages'])} pages" if t["pages"] else "")
        for t in data[tech]["Templates"]
    )
    body = f"""
  <section class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    {breadcrumb(root, [("Home", root+"index.html"), (tech, None)])}
    <h1 class="mt-3 text-3xl font-extrabold tracking-tight">{tech}</h1>
    <p class="mt-2 max-w-2xl text-neutral-600 dark:text-neutral-400">Components, sections, and full page templates built with {tech}.</p>
    <div class="mt-6 flex flex-wrap gap-3">
      <a href="Components/index.html" class="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-bold hover:bg-neutral-100 dark:border-neutral-700 dark:hover:bg-neutral-900">Browse Components</a>
      <a href="Sections/index.html" class="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-bold hover:bg-neutral-100 dark:border-neutral-700 dark:hover:bg-neutral-900">Browse Sections</a>
      <a href="Templates/index.html" class="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-bold hover:bg-neutral-100 dark:border-neutral-700 dark:hover:bg-neutral-900">Browse Templates</a>
    </div>
    {cat_block("Components", data[tech]["Components"])}
    {cat_block("Sections", data[tech]["Sections"])}
    <div class="mt-10">
      <div class="flex items-baseline justify-between">
        <h2 class="text-xl font-bold">Templates</h2>
        <a href="Templates/index.html" class="text-sm font-semibold text-{color}-600 hover:underline dark:text-{color}-400">View all &rarr;</a>
      </div>
      <div class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{tmpl_cards}</div>
    </div>
  </section>"""
    write(os.path.join(SITE, tech, "index.html"), page(f"{tech} — DevSnips", f"{tech} components, sections, and templates.", body, root, tech.lower()))

# ---- CATEGORY INDEX (e.g. site/Tailwind/Components/index.html) ----
def build_category_index(data, tech, cat):
    root = "../../"
    color = TECH_COLOR[tech]
    families = data[tech][cat]
    fam_sections = []
    for fam, items in sorted(families.items()):
        item_cards = "".join(
            card(f"{fam}/{it['slug']}/index.html", it["meta"].get("family", fam), it["meta"].get("name", it["slug"]),
                 it["meta"].get("description", ""), color)
            for it in items
        )
        fam_sections.append(f"""
    <div id="{fam}" class="mt-10 scroll-mt-24">
      <h2 class="text-xl font-bold">{htmllib.escape(fam)} <span class="mono text-sm font-normal text-neutral-400">({len(items)})</span></h2>
      <div class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{item_cards}</div>
    </div>""")
    toc = " &middot; ".join(f'<a href="#{fam}" class="hover:underline">{htmllib.escape(fam)}</a>' for fam in sorted(families))
    body = f"""
  <section class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    {breadcrumb(root, [("Home", root+"index.html"), (tech, root+tech+"/index.html"), (cat, None)])}
    <h1 class="mt-3 text-3xl font-extrabold tracking-tight">{tech} {cat}</h1>
    <p class="mt-2 max-w-2xl text-neutral-600 dark:text-neutral-400">{sum(len(v) for v in families.values())} variants across {len(families)} families.</p>
    <p class="mono mt-4 text-xs text-neutral-500 dark:text-neutral-400">{toc}</p>
    {''.join(fam_sections)}
  </section>"""
    write(os.path.join(SITE, tech, cat, "index.html"), page(f"{tech} {cat} — DevSnips", f"Browse all {tech} {cat.lower()}.", body, root, tech.lower()))

# ---- ITEM DETAIL ----
def build_item(it, related_pool):
    root = root_rel(item_dir_out(it))
    color = TECH_COLOR[it["tech"]]
    meta = it["meta"]
    name = meta.get("name", it["slug"])
    desc = meta.get("description", "")
    files = it["files"]
    has_preview = "preview.html" in files
    code_file = "code.html" if "code.html" in files else ("code.tsx" if "code.tsx" in files else ("code.jsx" if "code.jsx" in files else None))
    preview_src = rel_source(it, "preview.html" if has_preview else (code_file or "code.html"))
    code_src_path = os.path.join(it["dir"], code_file) if code_file else None
    code_text = rd(code_src_path) if code_src_path and os.path.isfile(code_src_path) else ""
    framework = meta.get("framework", it["tech"])
    features = meta.get("features", [])
    tags = meta.get("tags", [])
    related_slugs = meta.get("related", [])
    # related items: prefer metadata.related within same family, else same family siblings
    fam_items = [x for x in related_pool if x["slug"] != it["slug"]]
    related_items = [x for x in fam_items if x["slug"] in related_slugs]
    if not related_items:
        related_items = fam_items[:4]
    related_cards = "".join(
        card(f"../{r['slug']}/index.html", r["family"], r["meta"].get("name", r["slug"]),
             r["meta"].get("description", ""), color)
        for r in related_items[:4]
    ) or '<p class="text-sm text-neutral-500 dark:text-neutral-400">No related variants yet.</p>'

    install_cmd = f"npx devsnips add {it['tech'].lower()}/{it['category'].lower()}/{it['family']}/{it['slug']}"
    tags_html = " ".join(badge(t, "neutral") for t in tags[:8])
    features_html = "".join(f'<li class="flex items-start gap-2"><span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-{color}-500"></span><span>{htmllib.escape(f)}</span></li>' for f in features) or '<li class="text-neutral-500 dark:text-neutral-400">No listed features.</li>'
    docs_html = md_to_html(it["readme"]) if it["readme"] else "<p>No documentation available.</p>"

    body = f"""
  <section class="mx-auto max-w-6xl px-4 py-8 sm:px-6">
    {breadcrumb(root, [("Home", root+"index.html"), (it["tech"], root+it["tech"]+"/index.html"), (it["category"], root+it["tech"]+"/"+it["category"]+"/index.html"), (it["family"], root+it["tech"]+"/"+it["category"]+"/index.html#"+it["family"]), (name, None)])}
    <div class="mt-3 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-extrabold tracking-tight sm:text-3xl">{htmllib.escape(name)}</h1>
        <p class="mt-2 max-w-2xl text-neutral-600 dark:text-neutral-400">{htmllib.escape(desc)}</p>
      </div>
      <div class="flex shrink-0 gap-2">
        <a href="{preview_src}" target="_blank" rel="noopener" class="rounded-lg bg-neutral-900 px-4 py-2 text-sm font-bold text-white hover:bg-neutral-700 dark:bg-white dark:text-neutral-900 dark:hover:bg-neutral-200">Preview &#8599;</a>
        <button type="button" onclick="var c=document.getElementById('code-block').innerText;navigator.clipboard.writeText(c);this.innerText='Copied!';setTimeout(()=>this.innerText='Copy code',1200);" class="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-bold hover:bg-neutral-100 dark:border-neutral-700 dark:hover:bg-neutral-900">Copy code</button>
      </div>
    </div>

    <div class="mt-6 overflow-hidden rounded-2xl border border-neutral-200 dark:border-neutral-800">
      <div class="flex items-center justify-between border-b border-neutral-200 bg-neutral-50 px-4 py-2 dark:border-neutral-800 dark:bg-neutral-950">
        <div class="flex gap-1.5"><span class="h-2.5 w-2.5 rounded-full bg-red-400"></span><span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span><span class="h-2.5 w-2.5 rounded-full bg-emerald-400"></span></div>
        <span class="mono text-xs text-neutral-500">{htmllib.escape(name)} &mdash; live preview</span>
        <a href="{preview_src}" target="_blank" rel="noopener" class="text-xs font-semibold text-{color}-600 hover:underline dark:text-{color}-400">Open full preview &#8599;</a>
      </div>
      <iframe src="{preview_src}" title="{htmllib.escape(name)} preview" class="h-[420px] w-full bg-white dark:bg-neutral-900" loading="lazy"></iframe>
    </div>

    <div class="mt-6 grid gap-4 sm:grid-cols-3">
      <div class="rounded-xl border border-neutral-200 p-4 dark:border-neutral-800">
        <p class="mono text-[11px] font-semibold uppercase tracking-widest text-neutral-400">Technology</p>
        <p class="mt-1 font-bold">{htmllib.escape(framework)}</p>
      </div>
      <div class="rounded-xl border border-neutral-200 p-4 dark:border-neutral-800">
        <p class="mono text-[11px] font-semibold uppercase tracking-widest text-neutral-400">Category</p>
        <p class="mt-1 font-bold">{it["category"]} &rsaquo; {htmllib.escape(it["family"])}</p>
      </div>
      <div class="rounded-xl border border-neutral-200 p-4 dark:border-neutral-800">
        <p class="mono text-[11px] font-semibold uppercase tracking-widest text-neutral-400">Files</p>
        <p class="mt-1 font-bold">{len(files)}</p>
      </div>
    </div>

    <div class="mt-2 flex flex-wrap gap-2">{tags_html}</div>

    <div class="mt-8 rounded-xl border border-neutral-200 p-4 dark:border-neutral-800">
      <p class="mono text-[11px] font-semibold uppercase tracking-widest text-neutral-400">Installation</p>
      <div class="mt-2 flex items-center justify-between gap-3 rounded-lg bg-neutral-950 px-4 py-3">
        <code class="mono truncate text-sm text-emerald-300">{htmllib.escape(install_cmd)}</code>
        <button type="button" onclick="navigator.clipboard.writeText('{install_cmd}');this.innerText='Copied!';setTimeout(()=>this.innerText='Copy',1200);" class="mono shrink-0 rounded-md border border-neutral-700 px-2 py-1 text-xs font-semibold text-neutral-200 hover:bg-neutral-800">Copy</button>
      </div>
    </div>

    <div class="mt-10 grid gap-8 lg:grid-cols-3">
      <div class="lg:col-span-2">
        <h2 class="text-lg font-bold">Features</h2>
        <ul class="mt-3 space-y-2 text-sm text-neutral-700 dark:text-neutral-300">{features_html}</ul>
      </div>
      <div>
        <h2 class="text-lg font-bold">Related</h2>
        <div class="mt-3 grid gap-3">{related_cards}</div>
      </div>
    </div>

    <div class="mt-10 border-t border-neutral-200 pt-8 dark:border-neutral-800">
      <h2 class="text-lg font-bold">Documentation</h2>
      <article class="prose-devsnips mt-4">{docs_html}</article>
    </div>

    <div class="mt-8">
      <h2 class="text-lg font-bold">Source code</h2>
      <pre id="code-block" class="code-block mt-3 max-h-[420px] overflow-auto rounded-xl border border-neutral-200 bg-neutral-950 p-4 text-xs text-neutral-200 dark:border-neutral-800"><code>{htmllib.escape(code_text[:20000])}</code></pre>
    </div>
  </section>"""
    write(os.path.join(item_dir_out(it), "index.html"), page(
        f"{name} — {it['tech']} {it['category']} — DevSnips", desc or f"{name} {it['tech']} {it['category']}.",
        body, root, it["tech"].lower()))

# ---- TEMPLATE DETAIL ----
def build_template(t, siblings):
    root = root_rel(tmpl_dir_out(t))
    color = TECH_COLOR[t["tech"]]
    meta = t["meta"]
    name = meta.get("name", t["slug"])
    desc = meta.get("description", "")
    entry = "preview.html" if os.path.isfile(os.path.join(t["dir"], "preview.html")) else ("index.html" if os.path.isfile(os.path.join(t["dir"], "index.html")) else None)
    preview_src = rel_source_tmpl(t, entry) if entry else "#"
    pages_html = "".join(
        f'<li><a href="{rel_source_tmpl(t, "pages/"+p)}" target="_blank" rel="noopener" class="flex items-center justify-between rounded-lg border border-neutral-200 px-3 py-2 text-sm hover:border-{color}-400 dark:border-neutral-800"><span class="mono">{htmllib.escape(p)}</span><span class="text-neutral-400">Open &#8599;</span></a></li>'
        for p in t["pages"]
    ) or '<li class="text-sm text-neutral-500 dark:text-neutral-400">Single-page template &mdash; see preview.</li>'
    other_cards = "".join(
        card(f"../{s['slug']}/index.html", "Template", s["meta"].get("name", s["slug"]), s["meta"].get("description", ""), color)
        for s in siblings if s["slug"] != t["slug"]
    )[:4] or ""
    docs_html = md_to_html(t["readme"]) if t["readme"] else "<p>No documentation available.</p>"
    features = meta.get("features", [])
    features_html = "".join(f'<li class="flex items-start gap-2"><span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-{color}-500"></span><span>{htmllib.escape(f)}</span></li>' for f in features) or ""
    body = f"""
  <section class="mx-auto max-w-6xl px-4 py-8 sm:px-6">
    {breadcrumb(root, [("Home", root+"index.html"), (t["tech"], root+t["tech"]+"/index.html"), ("Templates", root+t["tech"]+"/Templates/index.html"), (name, None)])}
    <div class="mt-3 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-extrabold tracking-tight sm:text-3xl">{htmllib.escape(name)}</h1>
        <p class="mt-2 max-w-2xl text-neutral-600 dark:text-neutral-400">{htmllib.escape(desc)}</p>
      </div>
      {f'<a href="{preview_src}" target="_blank" rel="noopener" class="shrink-0 rounded-lg bg-neutral-900 px-4 py-2 text-sm font-bold text-white hover:bg-neutral-700 dark:bg-white dark:text-neutral-900 dark:hover:bg-neutral-200">Full preview &#8599;</a>' if entry else ''}
    </div>
    <div class="mt-6 overflow-hidden rounded-2xl border border-neutral-200 dark:border-neutral-800">
      <div class="flex items-center justify-between border-b border-neutral-200 bg-neutral-50 px-4 py-2 dark:border-neutral-800 dark:bg-neutral-950">
        <div class="flex gap-1.5"><span class="h-2.5 w-2.5 rounded-full bg-red-400"></span><span class="h-2.5 w-2.5 rounded-full bg-amber-400"></span><span class="h-2.5 w-2.5 rounded-full bg-emerald-400"></span></div>
        <span class="mono text-xs text-neutral-500">{htmllib.escape(name)} &mdash; live preview</span>
        <a href="{preview_src}" target="_blank" rel="noopener" class="text-xs font-semibold text-{color}-600 hover:underline dark:text-{color}-400">Open full preview &#8599;</a>
      </div>
      {f'<iframe src="{preview_src}" title="{htmllib.escape(name)} preview" class="h-[460px] w-full bg-white dark:bg-neutral-900" loading="lazy"></iframe>' if entry else '<p class="p-6 text-sm text-neutral-500">No standalone preview file found.</p>'}
    </div>

    <div class="mt-8 grid gap-8 lg:grid-cols-3">
      <div class="lg:col-span-2">
        <h2 class="text-lg font-bold">Pages in this template</h2>
        <ul class="mt-3 space-y-2">{pages_html}</ul>
        {f'<h2 class="mt-8 text-lg font-bold">Features</h2><ul class="mt-3 space-y-2 text-sm text-neutral-700 dark:text-neutral-300">{features_html}</ul>' if features_html else ''}
      </div>
      <div>
        <h2 class="text-lg font-bold">Other templates</h2>
        <div class="mt-3 grid gap-3">{other_cards}</div>
      </div>
    </div>

    <div class="mt-10 border-t border-neutral-200 pt-8 dark:border-neutral-800">
      <h2 class="text-lg font-bold">Documentation</h2>
      <article class="prose-devsnips mt-4">{docs_html}</article>
    </div>
  </section>"""
    write(os.path.join(tmpl_dir_out(t), "index.html"), page(
        f"{name} — {t['tech']} Template — DevSnips", desc or f"{name} template.", body, root, t["tech"].lower()))

def build_template_index(data, tech):
    root = "../../"
    color = TECH_COLOR[tech]
    cards = "".join(
        card(f"{t['slug']}/index.html", "Template", t["meta"].get("name", t["slug"]), t["meta"].get("description", ""), color,
             f"{len(t['pages'])} pages" if t["pages"] else "single page")
        for t in data[tech]["Templates"]
    )
    body = f"""
  <section class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    {breadcrumb(root, [("Home", root+"index.html"), (tech, root+tech+"/index.html"), ("Templates", None)])}
    <h1 class="mt-3 text-3xl font-extrabold tracking-tight">{tech} Templates</h1>
    <p class="mt-2 max-w-2xl text-neutral-600 dark:text-neutral-400">{len(data[tech]["Templates"])} complete, multi-page templates.</p>
    <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{cards}</div>
  </section>"""
    write(os.path.join(SITE, tech, "Templates", "index.html"), page(f"{tech} Templates — DevSnips", f"Browse all {tech} templates.", body, root, tech.lower()))

# ---- DOCS (multi-page, sourced from the repo's real docs) ----
DOC_PAGES = [
    # (slug, title, repo-relative source path, short description)
    ("overview", "Overview", None, "How DevSnips is organized and how to use it."),
    ("structure", "Content Structure", "docs/COMPONENT_STRUCTURE.md", "How components, sections, templates, and metadata are organized."),
    ("contributing", "Contributing", "docs/CONTRIBUTING.md", "How to add or change content in DevSnips."),
    ("vanilla-curation", "Vanilla Curation Report", "docs/VANILLA_CURATION_REPORT.md", "Quality curation notes for the Vanilla components library."),
    ("cli", "CLI Reference", "cli/README.md", "Install DevSnips components from the command line."),
    ("agents", "Agent Instructions", "AGENTS.md", "Authoritative repository notes for human and AI contributors."),
    ("changelog", "Changelog", "CHANGELOG.md", "Version history."),
    ("license", "License", "LICENSE", "MIT license."),
]

def docs_sidebar(root, active_slug):
    items = "".join(
        f'<a href="{root}docs/{slug}/index.html" class="block rounded-lg px-3 py-1.5 text-sm {"bg-slate-100 font-semibold text-slate-600 dark:bg-slate-900 dark:text-slate-300" if slug==active_slug else "text-neutral-600 hover:bg-neutral-100 dark:text-neutral-400 dark:hover:bg-neutral-900"}">{htmllib.escape(title)}</a>'
        for slug, title, _src, _desc in DOC_PAGES
    )
    return f'<nav aria-label="Documentation" class="w-full shrink-0 space-y-0.5 sm:w-56">{items}</nav>'

def build_docs(data):
    root = "../../"  # docs/<slug>/index.html -> two levels up
    total_comp = sum(sum(len(v) for v in data[t]["Components"].values()) for t in TECHS)
    total_sec = sum(sum(len(v) for v in data[t]["Sections"].values()) for t in TECHS)
    total_tmpl = sum(len(data[t]["Templates"]) for t in TECHS)

    for slug, title, src, desc in DOC_PAGES:
        crumb = breadcrumb(root, [("Home", root + "index.html"), ("Documentation", root + "docs/overview/index.html"), (title, None)])
        sidebar = docs_sidebar(root, slug)
        if slug == "overview":
            content = f"""
        <h1 class="text-3xl font-extrabold tracking-tight">Documentation</h1>
        <p class="mt-2 text-neutral-600 dark:text-neutral-400">{desc}</p>
        <div class="mt-8 grid gap-4 sm:grid-cols-3">
          <div class="rounded-xl border border-neutral-200 p-4 text-center dark:border-neutral-800"><p class="text-2xl font-extrabold">{total_comp}</p><p class="mono text-xs text-neutral-500">Components</p></div>
          <div class="rounded-xl border border-neutral-200 p-4 text-center dark:border-neutral-800"><p class="text-2xl font-extrabold">{total_sec}</p><p class="mono text-xs text-neutral-500">Sections</p></div>
          <div class="rounded-xl border border-neutral-200 p-4 text-center dark:border-neutral-800"><p class="text-2xl font-extrabold">{total_tmpl}</p><p class="mono text-xs text-neutral-500">Templates</p></div>
        </div>
        <article class="prose-devsnips mt-10">
          <h2>Structure</h2>
          <p>Every technology (Tailwind, Vanilla, React) is organized into three content types:</p>
          <ul>
            <li><strong>Components</strong> &mdash; small, reusable UI primitives (buttons, tabs, modals&hellip;)</li>
            <li><strong>Sections</strong> &mdash; page-level blocks (hero, pricing, 404, footer&hellip;)</li>
            <li><strong>Templates</strong> &mdash; complete, multi-page sites built from components and sections.</li>
          </ul>
          <h2>Anatomy of an item</h2>
          <p>Every component and section ships with four files:</p>
          <ul>
            <li><code>code.html</code> / <code>code.tsx</code> &mdash; copy-paste-ready snippet only.</li>
            <li><code>preview.html</code> &mdash; full standalone page you can open directly in a browser.</li>
            <li><code>metadata.json</code> &mdash; structured, machine-readable metadata (name, tags, features, related items).</li>
            <li><code>README.md</code> &mdash; human-readable documentation, rendered on every detail page.</li>
          </ul>
          <h2>Using a snippet</h2>
          <ol>
            <li>Open the item's detail page and click <strong>Preview</strong> to see it live in a new tab.</li>
            <li>Click <strong>Copy code</strong>, or read the source block at the bottom of the page.</li>
            <li>Paste it into your project and wire up any Tailwind classes or fonts it references.</li>
          </ol>
        </article>"""
        else:
            src_path = os.path.join(ROOT, src)
            if os.path.isfile(src_path):
                raw = rd(src_path)
                rendered = md_to_html(raw) if src.endswith(".md") else f"<pre class='code-block'>{htmllib.escape(raw)}</pre>"
            else:
                rendered = "<p>Source file not found.</p>"
            content = f"""
        <h1 class="text-3xl font-extrabold tracking-tight">{htmllib.escape(title)}</h1>
        <p class="mt-2 text-neutral-600 dark:text-neutral-400">{htmllib.escape(desc)}</p>
        <article class="prose-devsnips mt-8">{rendered}</article>"""
        body = f"""
  <section class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    {crumb}
    <div class="mt-4 flex flex-col gap-8 sm:flex-row">
      {sidebar}
      <div class="min-w-0 flex-1">{content}</div>
    </div>
  </section>"""
        write(os.path.join(SITE, "docs", slug, "index.html"), page(
            f"{title} — DevSnips Docs", desc, body, root, "docs"))

    # /docs/index.html itself redirects to the overview page for a stable entry URL
    redirect_body = f'<meta http-equiv="refresh" content="0; url=overview/index.html"><p class="p-8 text-sm">Redirecting to <a href="overview/index.html">Documentation</a>&hellip;</p>'
    write(os.path.join(SITE, "docs", "index.html"), f"""<!DOCTYPE html><html><head><meta charset="UTF-8">{redirect_body}</head><body></body></html>""")

# ---------------------------------------------------------------- main ----
def main():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    shutil.copy(os.path.join(GEN_DIR, "style_extra.css"), os.path.join(SITE, "assets", "style.css"))
    write(os.path.join(SITE, "assets", "logo.svg"), LOGO_FILE_SVG)

    data = collect()
    build_home(data)
    for tech in TECHS:
        build_tech_hub(data, tech)
        for cat in ["Components", "Sections"]:
            if data[tech][cat]:
                build_category_index(data, tech, cat)
                for fam, items in data[tech][cat].items():
                    for it in items:
                        build_item(it, items)
        if data[tech]["Templates"]:
            build_template_index(data, tech)
            for t in data[tech]["Templates"]:
                build_template(t, data[tech]["Templates"])
    build_docs(data)

    # simple counts report
    n_items = sum(
        len(items) for tech in TECHS for cat in ["Components", "Sections"] for items in data[tech][cat].values()
    )
    n_tmpl = sum(len(data[tech]["Templates"]) for tech in TECHS)
    print(f"Generated {n_items} component/section detail pages + {n_tmpl} template pages.")

if __name__ == "__main__":
    main()
