"""Rebuild snippets-index.json to match the migrated filesystem.

Architecture after migration:
    Vanilla/  -> Components/ + Templates/
    Tailwind/ -> Components/ + Templates/
    React/    -> Components/ + Templates/  (currently empty)

This script:
  1. Loads the existing index to preserve hand-curated family-level
     description / tags / searchTerms and variant-level fields.
  2. Rewrites every family/variant path from the old Sections/ location to
     Components/ and flips category Sections -> Components.
  3. Removes families under the deleted Utilities/ and Resources/ trees.
  4. Merges the former Vanilla/Sections/Navigation family into the existing
     Vanilla/Components/Navigation family.
  5. Cross-validates: every indexed variant must exist on disk, and every
     valid on-disk leaf must be indexed. Reports mismatches.
  6. Recomputes stats and technologies[].families from the final family set.

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
# Build the new index, preserving curated data from the old index
# ---------------------------------------------------------------------------
def build_index():
    """Rebuild the index by transforming existing family paths and re-scanning
    the disk for leaves. Family granularity is preserved from the old index
    (per AGENTS.md contract): the index regenerator matches on normalized path.
    """
    old = json.loads(INDEX.read_text(encoding="utf-8"))
    old_by_path = {norm(f["path"]): f for f in old.get("families", [])}

    # 1. Transform each old family: Sections/ -> Components/, drop deleted
    #    Utilities/Resources trees, flip category Sections -> Components.
    transformed = []  # list of (new_path_str, old_family_dict)
    for fam in old.get("families", []):
        op = fam["path"]
        # Skip deleted content collections entirely.
        if "/Utilities/" in op or "/Resources/" in op:
            continue
        if op.startswith("Vanilla/Utilities/") or op.startswith("Vanilla/Resources/"):
            continue
        np_ = op.replace("/Sections/", "/Components/")
        # Verify the transformed path exists on disk.
        if not (ROOT / np_.rstrip("/")).exists():
            continue
        new_cat = "Components" if fam.get("category") == "Sections" else fam.get("category", "Components")
        transformed.append((np_, fam, new_cat))

    # 2. Merge the former Vanilla/Sections/Navigation family into the existing
    #    Vanilla/Components/Navigation family (both now share the same path).
    merged = {}
    order = []
    for np_, fam, new_cat in transformed:
        if np_ in merged:
            # Merge: append the old family's variant disk-leaves.
            base = merged[np_]
            base["_extra_old"] = base.get("_extra_old", [])
            base["_extra_old"].append(fam)
        else:
            merged[np_] = {"fam": fam, "category": new_cat, "_extra_old": []}
            order.append(np_)

    new_families = []
    for np_ in order:
        entry = merged[np_]
        fam = entry["fam"]
        new_cat = entry["category"]
        tech = fam["tech"]
        family_dir = ROOT / np_.rstrip("/")
        is_template = (new_cat == "Templates")
        if is_template:
            leaves = _template_leaves(family_dir, tech)
        else:
            leaves = _leaves_in_family_dir(family_dir, tech)
        leaves = sorted(leaves, key=lambda lm: lm[0].name.lower())

        # Build curated variant lookup across the primary family + any merged
        # source families (e.g. the former Sections/Navigation).
        old_variants_by_path = {}
        for src in [fam] + entry["_extra_old"]:
            for v in src.get("variants", []):
                vp = v["path"].replace("/Sections/", "/Components/")
                old_variants_by_path[norm(vp)] = v

        variants = []
        for leaf, meta in leaves:
            leaf_rel = str(leaf).replace(str(ROOT) + "/", "") + "/"
            ov = old_variants_by_path.get(norm(leaf_rel), {})
            v = {
                "name": meta.get("name") or ov.get("name") or leaf.name,
                "path": leaf_rel,
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
            v["files"] = sorted(p.name for p in leaf.iterdir() if p.is_file())
            variants.append(v)

        family = {
            "name": fam.get("name") or family_dir.name,
            "path": np_,
            "tech": tech,
            "category": new_cat,
            "description": fam.get("description", ""),
            "variantsCount": len(variants),
            "variants": variants,
        }
        if fam.get("subcategory"):
            family["subcategory"] = fam["subcategory"]
        if fam.get("tags"):
            family["tags"] = fam["tags"]
        else:
            all_tags = set()
            for v in variants:
                all_tags.update(v.get("tags", []))
            family["tags"] = sorted(all_tags)
        if fam.get("searchTerms"):
            family["searchTerms"] = fam["searchTerms"]
        new_families.append(family)

    # 4. Discovery pass: add any on-disk family not already in the index.
    indexed_paths = {norm(f["path"]) for f in new_families}
    # Templates: a top-level Templates/<name>/ with its own metadata.json and no
    # child metadata-bearing folder is a single-variant template family.
    for tech, root_dir in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        tdir = ROOT / root_dir / "Templates"
        if not tdir.exists():
            continue
        for top in sorted(tdir.iterdir()):
            if not top.is_dir():
                continue
            rel = str(top).replace(str(ROOT) + "/", "")
            if norm(rel) in indexed_paths:
                continue
            meta = _read_meta(top / "metadata.json")
            if meta is None:
                continue
            leaf_rel = rel + "/"
            v = {
                "name": meta.get("name") or top.name,
                "path": leaf_rel,
                "description": meta.get("description", ""),
            }
            if meta.get("tags"):
                v["tags"] = meta["tags"]
            if meta.get("features"):
                v["features"] = meta["features"]
            style = meta.get("style")
            if style:
                v["styles"] = style if isinstance(style, list) else [style]
            v["files"] = sorted(p.name for p in top.iterdir() if p.is_file())
            family = {
                "name": meta.get("name") or top.name,
                "path": leaf_rel,
                "tech": tech,
                "category": "Templates",
                "description": meta.get("description", ""),
                "variantsCount": 1,
                "variants": [v],
            }
            family["tags"] = meta.get("tags", [])
            new_families.append(family)
            indexed_paths.add(norm(rel))

    # Components: any top-level Components/<name>/ folder with on-disk leaves
    # that is not yet indexed becomes its own family (one family per folder).
    for tech, root_dir in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        comp = ROOT / root_dir / "Components"
        if not comp.exists():
            continue
        for top in sorted(comp.iterdir()):
            if not top.is_dir():
                continue
            rel = str(top).replace(str(ROOT) + "/", "")
            # Covered if a family path equals rel or starts with rel/
            if norm(rel) in indexed_paths or any(
                    norm(p).startswith(norm(rel) + "/") for p in indexed_paths):
                continue
            leaves = _leaves_in_family_dir(top, tech)
            if not leaves:
                continue
            leaves = sorted(leaves, key=lambda lm: lm[0].name.lower())
            variants = []
            for leaf, meta in leaves:
                leaf_rel = str(leaf).replace(str(ROOT) + "/", "") + "/"
                v = {
                    "name": meta.get("name") or leaf.name,
                    "path": leaf_rel,
                    "description": meta.get("description", ""),
                }
                if meta.get("tags"):
                    v["tags"] = meta["tags"]
                if meta.get("features"):
                    v["features"] = meta["features"]
                style = meta.get("style")
                if style:
                    v["styles"] = style if isinstance(style, list) else [style]
                v["files"] = sorted(p.name for p in leaf.iterdir() if p.is_file())
                variants.append(v)
            all_tags = set()
            for v in variants:
                all_tags.update(v.get("tags", []))
            family = {
                "name": top.name,
                "path": rel + "/",
                "tech": tech,
                "category": "Components",
                "description": "",
                "variantsCount": len(variants),
                "variants": variants,
                "tags": sorted(all_tags),
            }
            new_families.append(family)
            indexed_paths.add(norm(rel))

    # 5. Technologies list.
    techs = []
    for name, path in ((TAILWIND, "Tailwind/"), (VANILLA, "Vanilla/")):
        fam_names = [f["name"] for f in new_families if f["tech"] == name]
        techs.append({"name": name, "path": path, "status": "active",
                      "families": fam_names})

    total_families = len(new_families)
    total_variants = sum(f["variantsCount"] for f in new_families)
    total_styles = sum(len(v.get("styles", [])) or 1
                       for f in new_families for v in f["variants"])

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
        root_dir = "Tailwind" if tech == TAILWIND else "Vanilla"
        for v in f["variants"]:
            vpath = ROOT / v["path"].rstrip("/")
            mpath = vpath / "metadata.json"
            if not mpath.exists():
                problems.append(f"Indexed variant missing on disk: {v['path']}")
                continue
            # For Tailwind, require code.html + preview.html unless it's a template.
            if f["category"] == "Components" and tech == TAILWIND:
                if not (vpath / "code.html").exists():
                    problems.append(
                        f"Tailwind component missing code.html: {v['path']}")
                if not (vpath / "preview.html").exists():
                    problems.append(
                        f"Tailwind component missing preview.html: {v['path']}")

    # 2. Every disk leaf under Components/ must be indexed.
    indexed = {norm(v["path"]) for f in families for v in f["variants"]}
    for tech, root_dir in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        comp = ROOT / root_dir / "Components"
        for leaf, meta in list_leaves_under(comp, tech):
            leaf_rel = str(leaf).replace(str(ROOT) + "/", "") + "/"
            if norm(leaf_rel) not in indexed:
                problems.append(f"On-disk leaf NOT indexed: {leaf_rel}")

    # 3. Templates: every template folder with metadata.json indexed.
    for tech, root_dir in ((TAILWIND, "Tailwind"), (VANILLA, "Vanilla")):
        tdir = ROOT / root_dir / "Templates"
        if not tdir.exists():
            continue
        for top in tdir.iterdir():
            if not top.is_dir():
                continue
            for leaf, meta in list_leaves_under(top, tech):
                leaf_rel = str(leaf).replace(str(ROOT) + "/", "") + "/"
                if norm(leaf_rel) not in indexed:
                    problems.append(f"On-disk template leaf NOT indexed: {leaf_rel}")

    # 4. No duplicate paths / duplicate family paths.
    fam_paths = [f["path"] for f in families]
    dup = {p for p in fam_paths if fam_paths.count(p) > 1}
    for d in dup:
        problems.append(f"Duplicate family path: {d}")

    # 5. No stale Sections/Utilities/Resources references.
    for f in families:
        if "/Sections/" in f["path"] or "/Utilities/" in f["path"] or "/Resources/" in f["path"]:
            problems.append(f"Stale path in family: {f['path']}")
        for v in f["variants"]:
            if "/Sections/" in v["path"] or "/Utilities/" in v["path"] or "/Resources/" in v["path"]:
                problems.append(f"Stale path in variant: {v['path']}")

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
