"""Rebuild snippets-index.json to match the migrated filesystem.

Architecture after migration:
    Vanilla/  -> Components/ + Templates/
    Tailwind/ -> Components/ + Sections/ + Templates/
    React/    -> Components/ + Templates/  (currently empty)

Tailwind has three first-class content types (Components / Sections /
Templates); Vanilla and React keep the two-type layout. Every Tailwind entry
carries a lowercase `type` field (component / section / template) for search
and filtering, and a Capitalized `category` bucket.

This script:
  1. Loads the existing index to preserve hand-curated family-level
     description / tags / searchTerms and variant-level fields.
  2. Re-scans the disk for leaves under each content-type tree and rebuilds
     every family/variant path + category + type from the on-disk location.
  3. Cross-validates: every indexed variant must exist on disk, and every
     valid on-disk leaf must be indexed. Reports mismatches.
  4. Recomputes stats and technologies[].families from the final family set.

Run:  python3 -m _gen.rebuild_index
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "snippets-index.json"

VANILLA = "Vanilla HTML/CSS/JS"
TAILWIND = "Tailwind CSS"


# ---------------------------------------------------------------------------
# Filesystem leaf detection
# ---------------------------------------------------------------------------
def _read_meta(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _has_child_meta(folder: Path) -> bool:
    """True if any direct sub-folder of `folder` contains a metadata.json."""
    for child in folder.iterdir():
        if child.is_dir() and (child / "metadata.json").exists():
            return True
    return False


def is_leaf(folder: Path, tech: str) -> bool:
    """A leaf content item.

    Tailwind leaf: a folder containing code.html + preview.html + metadata.json
    whose direct children do NOT include another metadata.json-bearing folder.
    Vanilla leaf: a folder containing metadata.json whose direct children do
    NOT include another metadata.json-bearing folder.
    """
    if not (folder / "metadata.json").exists():
        return False
    if _has_child_meta(folder):
        return False
    if tech == TAILWIND:
        # Tailwind content folders ship code.html + preview.html (+ metadata).
        # The Buttons 3-level grouping folders have metadata.json but no
        # code.html/preview.html, so they are correctly excluded as non-leaves.
        return (folder / "code.html").exists() and (folder / "preview.html").exists()
    return True


def list_leaves_under(folder: Path, tech: str):
    """Yield (leaf_path_rel, metadata) for every leaf under `folder`."""
    if not folder.exists():
        return
    for p in folder.rglob("metadata.json"):
        leaf = p.parent
        if is_leaf(leaf, tech):
            yield leaf, _read_meta(p)


def norm(p: str) -> str:
    """Normalize a path string for matching: strip trailing slash."""
    return p.rstrip("/").replace("\\", "/")


def _leaves_in_family_dir(family_dir: Path, tech: str):
    """Return [(leaf_path, metadata)] for every leaf under `family_dir`."""
    out = []
    for leaf, meta in list_leaves_under(family_dir, tech):
        out.append((leaf, meta))
    return out


def _template_leaves(family_dir: Path, tech: str):
    """Return [(leaf_path, metadata)] for a template family folder.

    A template family folder may itself carry metadata.json (single-page) or
    contain sub-template leaf folders (e.g. Standalone with 2 templates).
    """
    if (family_dir / "metadata.json").exists() and not _has_child_meta(family_dir):
        return [(family_dir, _read_meta(family_dir / "metadata.json"))]
    out = []
    for leaf, meta in list_leaves_under(family_dir, tech):
        out.append((leaf, meta))
    return out


# ---------------------------------------------------------------------------
# Content-type trees per technology
# ---------------------------------------------------------------------------
# (Capitalized bucket, lowercase type, is_template) for each content tree.
# Tailwind has three first-class types; Vanilla/React have two.
TAILWIND_TREES = [
    ("Components", "component", False),
    ("Sections", "section", False),
    ("Templates", "template", True),
]
VANILLA_TREES = [
    ("Components", "component", False),
    ("Templates", "template", True),
]


def _trees_for(tech):
    return TAILWIND_TREES if tech == TAILWIND else VANILLA_TREES


# Curated family-level display names + descriptions for generated Tailwind
# section categories (these families have no family-level metadata on disk, so
# without this the family name would fall back to a per-variant name like
# "Accordion FAQ — Apple Inspired"). Values mirror the pre-migration index.
SECTION_FAMILY_NAMES = {
    "404": "404 (Tailwind)",
    "Blog": "Blog (Tailwind)",
    "Contact": "Contact (Tailwind)",
    "FAQ": "FAQ (Tailwind)",
    "Footer": "Footer (Tailwind)",
    "Logos": "Logos (Tailwind)",
    "Navbar": "Navbar (Tailwind)",
    "Newsletter": "Newsletter (Tailwind)",
    "Stats": "Stats (Tailwind)",
    "Team": "Team (Tailwind)",
    "Testimonials": "Testimonials (Tailwind)",
    "ai-product": "AI Product (Tailwind)",
    "app-ui": "App UI (Tailwind)",
    "developer": "Developer (Tailwind)",
    "marketing": "Marketing (Tailwind)",
    "premium-visual": "Premium Visual (Tailwind)",
    "saas": "SaaS (Tailwind)",
}

SECTION_FAMILY_DESCRIPTIONS = {
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
    "ai-product": "AI product sections — chat interfaces, model comparison, prompt libraries, and agent workflows.",
    "app-ui": "App UI sections — dashboard overviews and kanban boards for in-product surfaces.",
    "developer": "Developer sections — code playgrounds and command palettes for dev-tool surfaces.",
    "marketing": "Marketing sections — feature grids and hero landings for top-of-funnel pages.",
    "premium-visual": "Premium visual sections — aurora hero and other high-impact, animation-forward headers.",
    "saas": "SaaS sections — heroes, pricing, testimonials, metrics, CTAs, and footers for SaaS sites.",
}


# ---------------------------------------------------------------------------
# Build the new index, preserving curated data from the old index
# ---------------------------------------------------------------------------
def build_index():
    """Rebuild the index by scanning each content-type tree on disk.

    Family granularity follows the on-disk layout (one family per top-level
    folder under a content tree, except for the multi-concept section categories
    where each <category>/<section>/ folder is its own family). Hand-curated
    family-level description / tags / searchTerms and variant-level fields from
    the previous index are preserved by matching on normalized path.
    """
    old = json.loads(INDEX.read_text(encoding="utf-8"))
    old_fam_by_path = {norm(f["path"]): f for f in old.get("families", [])}
    # Variant-level curated data from the old index (matched by normalized path).
    old_var_by_path = {}
    for f in old.get("families", []):
        for v in f.get("variants", []):
            old_var_by_path[norm(v["path"])] = (f, v)

    def lookup_old_fam(fam_path):
        """Match curated family data by path, including the pre-move
        Components/ location for section families that were moved to Sections/."""
        if norm(fam_path) in old_fam_by_path:
            return old_fam_by_path[norm(fam_path)]
        if fam_path.startswith("Tailwind/Sections/"):
            pre = fam_path.replace("Tailwind/Sections/", "Tailwind/Components/", 1)
            return old_fam_by_path.get(norm(pre), {})
        return {}

    new_families = []

    def make_variant(leaf, meta, type_val, leaf_rel):
        ov_fam, ov = old_var_by_path.get(norm(leaf_rel), (None, {}))
        if not ov and leaf_rel.startswith("Tailwind/Sections/"):
            pre = leaf_rel.replace("Tailwind/Sections/", "Tailwind/Components/", 1)
            ov_fam, ov = old_var_by_path.get(norm(pre), (None, {}))
        v = {
            "name": meta.get("name") or ov.get("name") or leaf.name,
            "path": leaf_rel,
            "type": type_val,
            "description": meta.get("description") or ov.get("description", ""),
        }
        if meta.get("tags"):
            v["tags"] = meta["tags"]
        elif ov.get("tags"):
            v["tags"] = ov["tags"]
        if meta.get("features"):
            v["features"] = meta["features"]
        elif ov.get("features"):
            v["features"] = ov["features"]
        style = meta.get("style")
        if style:
            v["styles"] = style if isinstance(style, list) else [style]
        elif ov.get("styles"):
            v["styles"] = ov["styles"]
        # Build the file manifest. Vanilla templates keep their code files in a
        # `pages/` sub-folder (so the root holds only preview.html +
        # metadata.json + README.md); include those one level deep, prefixed
        # `pages/`. Tailwind leaves keep their flat code.html/preview.html.
        files = sorted(p.name for p in leaf.iterdir() if p.is_file())
        pages_dir = leaf / "pages"
        if pages_dir.is_dir():
            files += sorted("pages/" + p.name
                            for p in pages_dir.iterdir() if p.is_file())
        v["files"] = files
        return v

    def add_family(family_dir, tech, category, type_val, is_template):
        """Index a single family directory (one family per call)."""
        if is_template:
            leaves = _template_leaves(family_dir, tech)
        else:
            leaves = _leaves_in_family_dir(family_dir, tech)
        if not leaves:
            return
        leaves = sorted(leaves, key=lambda lm: lm[0].name.lower())
        rel = str(family_dir).replace(str(ROOT) + "/", "")
        fam_path = rel + "/"
        old_fam = lookup_old_fam(fam_path)

        variants = []
        for leaf, meta in leaves:
            leaf_rel = str(leaf).replace(str(ROOT) + "/", "") + "/"
            variants.append(make_variant(leaf, meta, type_val, leaf_rel))

        # Family display name resolution order:
        #   1. curated section-family name (generated section categories have
        #      no family-level metadata, so this wins over a variant-derived
        #      name that may already be in the previous index)
        #   2. curated name from the previous index (path-matched)
        #   3. the first variant's metadata "section" concept (stable across styles)
        #   4. the first variant's metadata name
        #   5. the folder name (title-cased)
        name = SECTION_FAMILY_NAMES.get(family_dir.name) if category == "Sections" else None
        if not name:
            name = old_fam.get("name")
        if not name:
            first_meta = leaves[0][1] or {}
            raw = first_meta.get("name") or family_dir.name
            looks_like_variant = ("—" in raw) or (
                "-" in raw and family_dir.name.lower() not in raw.lower())
            if looks_like_variant:
                name = first_meta.get("section") or family_dir.name
            else:
                name = raw
            if not name:
                name = family_dir.name.replace("-", " ").replace("_", " ").title()
        description = old_fam.get("description", "")
        if not description and category == "Sections":
            description = SECTION_FAMILY_DESCRIPTIONS.get(family_dir.name, "")

        family = {
            "name": name,
            "path": fam_path,
            "tech": tech,
            "type": type_val,
            "category": category,
            "description": description,
            "variantsCount": len(variants),
            "variants": variants,
        }
        if old_fam.get("subcategory"):
            family["subcategory"] = old_fam["subcategory"]
        elif leaves and leaves[0][1] and leaves[0][1].get("subcategory"):
            family["subcategory"] = leaves[0][1]["subcategory"]
        if old_fam.get("tags"):
            family["tags"] = old_fam["tags"]
        else:
            all_tags = set()
            for v in variants:
                all_tags.update(v.get("tags", []))
            family["tags"] = sorted(all_tags)
        if old_fam.get("searchTerms"):
            family["searchTerms"] = old_fam["searchTerms"]
        new_families.append(family)

    # Scan every technology's content-type trees.
    for tech, root_dir in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        for category, type_val, is_template in _trees_for(tech):
            tree = ROOT / root_dir / category
            if not tree.exists():
                continue
            for top in sorted(tree.iterdir()):
                if not top.is_dir():
                    continue
                if is_template:
                    # Each top-level template folder is one family.
                    add_family(top, tech, category, type_val, is_template=True)
                else:
                    # Components/Sections: a top-level folder is a family
                    # UNLESS it is a multi-concept section category
                    # (<category>/<section>/<style>/), in which case each
                    # <section> sub-folder is its own family.
                    sub_families = [
                        c for c in top.iterdir()
                        if c.is_dir() and _leaves_in_family_dir(c, tech)
                    ]
                    if sub_families and not _leaves_in_family_dir(top, tech):
                        for sub in sorted(sub_families):
                            add_family(sub, tech, category, type_val, is_template=False)
                    else:
                        add_family(top, tech, category, type_val, is_template=False)

    # Technologies list.
    techs = []
    for name, path in ((TAILWIND, "Tailwind/"), (VANILLA, "Vanilla/")):
        fam_names = [f["name"] for f in new_families if f["tech"] == name]
        techs.append({"name": name, "path": path, "status": "active",
                      "families": fam_names})

    total_families = len(new_families)
    total_variants = sum(f["variantsCount"] for f in new_families)
    total_styles = sum(len(v.get("styles", [])) or 1
                       for f in new_families for v in f["variants"])

    # Per-type counts for the Tailwind landing/navigation UI.
    tw_by_type = {"component": 0, "section": 0, "template": 0}
    for f in new_families:
        if f["tech"] == TAILWIND:
            tw_by_type[f["type"]] = tw_by_type.get(f["type"], 0) + f["variantsCount"]

    data = {
        "version": old.get("version", "2.0"),
        "lastUpdated": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).strftime("%Y-%m-%d"),
        "description": old.get("description", "DevSnips component library index."),
        "stats": {
            "totalFamilies": total_families,
            "totalVariants": total_variants,
            "totalSubVariants": 0,
            "totalStyles": total_styles,
            "technologies": [t["name"] for t in techs],
            "tailwindByType": tw_by_type,
        },
        "families": new_families,
        "technologies": techs,
        "contributionGuidelines": old.get("contributionGuidelines", {}),
    }
    return data, new_families


def validate(data, families):
    """Cross-check: indexed variants == disk leaves. Return list of problems."""
    problems = []

    # 1. Every indexed variant path must exist on disk.
    for f in families:
        tech = f["tech"]
        for v in f["variants"]:
            vpath = ROOT / v["path"].rstrip("/")
            mpath = vpath / "metadata.json"
            if not mpath.exists():
                problems.append(f"Indexed variant missing on disk: {v['path']}")
                continue
            # Tailwind components + sections require code.html + preview.html.
            # Tailwind templates ship preview.html only.
            if tech == TAILWIND and f["category"] in ("Components", "Sections"):
                bucket = f["category"].lower()
                if not (vpath / "code.html").exists():
                    problems.append(
                        f"Tailwind {bucket} missing code.html: {v['path']}")
                if not (vpath / "preview.html").exists():
                    problems.append(
                        f"Tailwind {bucket} missing preview.html: {v['path']}")

    # 2. Every disk leaf under each content tree must be indexed.
    indexed = {norm(v["path"]) for f in families for v in f["variants"]}
    for tech, root_dir in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        for category, _type, _is_template in _trees_for(tech):
            tree = ROOT / root_dir / category
            if not tree.exists():
                continue
            for leaf, meta in list_leaves_under(tree, tech):
                leaf_rel = str(leaf).replace(str(ROOT) + "/", "") + "/"
                if norm(leaf_rel) not in indexed:
                    problems.append(f"On-disk leaf NOT indexed: {leaf_rel}")

    # 3. No duplicate family paths.
    fam_paths = [f["path"] for f in families]
    dup = {p for p in fam_paths if fam_paths.count(p) > 1}
    for d in dup:
        problems.append(f"Duplicate family path: {d}")

    # 4. No stale Utilities/Resources references; /Sections/ is only valid under
    #    Tailwind/Sections/.
    for f in families:
        for token in ("/Utilities/", "/Resources/"):
            if token in f["path"]:
                problems.append(f"Stale path in family: {f['path']}")
        if "/Sections/" in f["path"] and not f["path"].startswith("Tailwind/Sections/"):
            problems.append(f"Stale path in family: {f['path']}")
        for v in f["variants"]:
            for token in ("/Utilities/", "/Resources/"):
                if token in v["path"]:
                    problems.append(f"Stale path in variant: {v['path']}")
            if "/Sections/" in v["path"] and not v["path"].startswith("Tailwind/Sections/"):
                problems.append(f"Stale path in variant: {v['path']}")

    # 5. Every Tailwind entry must carry a valid type.
    for f in families:
        if f["tech"] != TAILWIND:
            continue
        if f.get("type") not in ("component", "section", "template"):
            problems.append(f"Tailwind family missing/invalid type: {f['path']}")
        for v in f["variants"]:
            if v.get("type") not in ("component", "section", "template"):
                problems.append(f"Tailwind variant missing/invalid type: {v['path']}")

    return problems


if __name__ == "__main__":
    data, families = build_index()
    problems = validate(data, families)
    if problems:
        print("VALIDATION PROBLEMS (%d):" % len(problems))
        for p in problems:
            print("  -", p)
    else:
        print("Validation: OK (indexed content matches disk exactly)")
    print("Families: %d | Variants: %d | Styles: %d" % (
        data["stats"]["totalFamilies"],
        data["stats"]["totalVariants"],
        data["stats"]["totalStyles"]))
    # Per-tech breakdown
    for tech in (TAILWIND, VANILLA):
        tfams = [f for f in families if f["tech"] == tech]
        tv = sum(f["variantsCount"] for f in tfams)
        print(f"  {tech}: {len(tfams)} families, {tv} variants")
    if not problems:
        INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                         encoding="utf-8")
        print("Wrote snippets-index.json")
    else:
        print("NOT writing index due to validation problems.")
