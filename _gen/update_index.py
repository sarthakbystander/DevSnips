"""Update snippets-index.json with the 165 Tailwind section-style components (11 families x 15 variants)."""
import json
from pathlib import Path
from .styles import STYLE_NAMES
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
INDEX = ROOT / "snippets-index.json"

CATEGORY_DESCRIPTIONS = {
    "Testimonials": "Customer testimonial layouts with ratings, avatars, and quotes for social proof.",
    "FAQ": "Frequently-asked-question sections with accordions, search, and categorized layouts.",
    "Contact": "Contact sections with forms, office locations, support channels, and team directories.",
    "Footer": "Site footers with multi-column links, newsletters, social, and legal rows.",
    "Navbar": "Navigation bars — transparent, sticky, mega menu, dashboard, glass, and floating styles.",
    "Stats": "Stats and metrics sections — KPI cards, dashboards, counters, and progress bars.",
    "Team": "Team sections — grids, founders, hierarchy, circular, and detailed profile cards.",
    "Blog": "Blog sections — featured articles, magazine, bento, editorial, and news layouts.",
    "Logos": "Logo clouds and brand walls — infinite scroll, grids, partners, and trusted-by rows.",
    "Newsletter": "Newsletter subscribe CTAs — centered, split, glass, gradient, and bento styles.",
    "404": "404 error pages — minimal, funny, terminal, space, retro, and gradient themes.",
}

BUILDERS = [
    ("Testimonials", "testimonials", testimonials),
    ("FAQ", "faq", faq),
    ("Contact", "contact", contact),
    ("Footer", "footer", footer),
    ("Navbar", "navbar", navbar),
    ("Stats", "stats", stats),
    ("Team", "team", team),
    ("Blog", "blog", blog),
    ("Logos", "logos", logos),
    ("Newsletter", "newsletter", newsletter),
    ("404", "404", error_page),
]

CATEGORY_STYLES = [
    "neo-brutalism", "edge-glassmorphism", "vercel", "minimal", "apple-inspired",
    "bento-grid", "editorial", "dark-premium", "startup-landing", "futuristic",
    "gradient-mesh", "soft-ui", "cyber", "monochrome", "elegant-luxury",
]


def style_for(cat_index, concept_index):
    offset = (cat_index * 4) % 15
    return CATEGORY_STYLES[(concept_index + offset) % 15]


def update_index():
    data = json.loads(INDEX.read_text(encoding="utf-8"))

    # Remove any pre-existing families we may have added in a prior run, to keep idempotent.
    existing_paths = {f["path"] for f in data["families"]}
    new_family_paths = set()
    for ci, (cat, slug, _) in enumerate(BUILDERS):
        new_family_paths.add("Tailwind/Components/%s/" % cat)
    data["families"] = [f for f in data["families"] if f["path"] not in new_family_paths]

    # Also clean technologies[].families list entries we may have added.
    family_names_to_add = []
    families_to_add = []
    for ci, (cat, slug, builder) in enumerate(BUILDERS):
        variants = []
        for n in range(15):
            style_key = style_for(ci, n)
            result = builder(style_key, n)
            sec_path = "Tailwind/Components/%s/%s/" % (cat, style_key)
            variants.append({
                "name": "%s — %s" % (result["section_name"], STYLE_NAMES[style_key]),
                "path": sec_path,
                "description": result["desc"],
                "styles": [style_key],
                "features": result["features"],
                "tags": result["tags"],
                "files": ["code.html", "preview.html", "metadata.json", "README.md"],
            })
        fam_path = "Tailwind/Components/%s/" % cat
        family = {
            "name": "%s (Tailwind)" % cat,
            "path": fam_path,
            "tech": "Tailwind CSS",
            "category": "Components",
            "subcategory": slug,
            "description": CATEGORY_DESCRIPTIONS[cat],
            "variantsCount": 15,
            "variants": variants,
            "tags": sorted(set().union(*[set(v["tags"]) for v in variants]) - {slug}),
            "searchTerms": [slug, cat.lower(), "tailwind", "section"],
        }
        families_to_add.append(family)
        family_names_to_add.append(family["name"])

    data["families"].extend(families_to_add)

    # Register under technologies -> Tailwind CSS families list (idempotent).
    for t in data["technologies"]:
        if t["name"] == "Tailwind CSS":
            fams = t.setdefault("families", [])
            for name in family_names_to_add:
                if name not in fams:
                    fams.append(name)

    # Recompute stats.
    total_families = len(data["families"])
    total_variants = sum(f.get("variantsCount", 0) for f in data["families"])
    data["stats"]["totalFamilies"] = total_families
    data["stats"]["totalVariants"] = total_variants
    # Keep technologies list reflecting the two main techs.
    tech_names = sorted({f.get("tech", "") for f in data["families"] if f.get("tech")})
    data["stats"]["technologies"] = tech_names

    # Update lastUpdated timestamp if present.
    from datetime import datetime, timezone
    data["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    INDEX.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return total_families, total_variants


if __name__ == "__main__":
    f, v = update_index()
    print("Updated index: totalFamilies=%d totalVariants=%d" % (f, v))
