"""Generate the master index + the specialized type indexes from disk.

Run:  python scripts/tooling/indexing/build_resource_indexes.py

This is the one-command entry point for the whole index system. It REUSES the
scanner, curated-data preservation and cross-validation of
`rebuild_index.py` (imported — the filesystem scanner is never duplicated),
then:

  1. Rebuilds snippets-index.json (master index, unchanged schema).
  2. Derives three specialized indexes from the SAME in-memory family data:
       agents/resources/indexes/components-index.json
       agents/resources/indexes/sections-index.json
       agents/resources/indexes/templates-index.json

Deterministic output: families and variants are sorted by path, keys are in a
fixed order, no timestamps, no absolute or machine-specific paths. Two runs
over the same repository state produce byte-identical specialized indexes.

Paths follow the master-index convention: tech-first, WITHOUT the `library/`
prefix. The on-disk location of every entry is `library/<path>`.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rebuild_index as rb  # noqa: E402  (same directory)

ROOT = rb.ROOT
MASTER = rb.INDEX
OUT_DIR = ROOT / "agents" / "resources" / "indexes"

# Source extensions the CLI installs (cli/src/install/downloader.js
# getSourceFiles). metadata.json / preview.html are never installed.
SOURCE_EXTS = {".html", ".jsx", ".tsx", ".js", ".ts", ".css"}
NEVER_INSTALL = {"metadata.json", "preview.html"}
DOCS_INSTALL = {"README.md", "AGENTS.md"}


def is_installable(files):
    """Mirror cli/src/install/downloader.js getSourceFiles: the CLI errors
    with 'No source files found' when NOTHING passes its filter, so an
    install command is only derived when at least one file passes."""
    for f in files:
        if f in NEVER_INSTALL:
            continue
        if f in DOCS_INSTALL:
            return True
        dot = f.rfind(".")
        if dot != -1 and f[dot:] in SOURCE_EXTS:
            return True
    return False


def make_variant_entry(variant):
    """Specialized-index variant entry. Only fields backed by real data are
    emitted — empty optional fields are omitted entirely (e.g. 52 of the 56
    React section metadata.json files carry no `description`; those entries
    simply have no description key rather than an empty string)."""
    path = variant["path"].rstrip("/")
    entry = {
        "id": path,  # canonical CLI-resolvable id (npx devsnips add <id>)
        "name": variant.get("name", ""),
        "type": variant["type"],
        "path": variant["path"],  # trailing-slash form, matches master index
    }
    description = variant.get("description", "")
    if description:
        entry["description"] = description
    files = variant.get("files", [])
    if files:
        entry["files"] = files
    for key in ("tags", "features", "styles"):
        val = variant.get(key)
        if val:
            entry[key] = val
    if is_installable(files):
        entry["install"] = "npx devsnips add " + path
    return entry


def make_family_entry(family):
    entry = {
        "name": family["name"],
        "path": family["path"],
        "tech": family["tech"],
        "type": family["type"],
        "category": family["category"],
        "variantsCount": family["variantsCount"],
        # Deterministic ordering: sort variants by full path (case-insensitive).
        # The master index's leaf-name order is inherited from rebuild_index
        # (sorted by leaf NAME, where ties fall back to rglob discovery order),
        # so re-sorting here makes specialized-index output stable across
        # machines and filesystems. Also sorted() on a copy never mutates the
        # master's in-memory families.
        "variants": [make_variant_entry(v) for v in
                     sorted(family["variants"],
                            key=lambda v: v["path"].lower())],
    }
    if family.get("subcategory"):
        entry["subcategory"] = family["subcategory"]
    if family.get("tags"):
        entry["tags"] = family["tags"]
    if family.get("searchTerms"):
        entry["searchTerms"] = family["searchTerms"]
    return entry


TYPE_META = {
    "component": {
        "file": "components-index.json",
        "description": "Reusable UI building blocks (components) across all "
                       "technologies. Generated from library/<Tech>/Components/.",
    },
    "section": {
        "file": "sections-index.json",
        "description": "Composable page sections (heroes, features, pricing, "
                       "footers...) across all technologies. Generated from "
                       "library/<Tech>/Sections/.",
    },
    "template": {
        "file": "templates-index.json",
        "description": "Full website/page templates across all technologies. "
                       "Generated from library/<Tech>/Templates/.",
    },
}


def build_specialized(families, type_val):
    """Build one specialized index dict from the in-memory family set."""
    sel = [f for f in families if f["type"] == type_val]
    sel.sort(key=lambda f: f["path"].lower())
    by_tech = {}
    installable = 0
    resources = 0
    for fam in sel:
        by_tech[fam["tech"]] = by_tech.get(fam["tech"], 0) + fam["variantsCount"]
        for v in fam["variants"]:
            resources += 1
            if is_installable(v.get("files", [])):
                installable += 1
    return {
        "version": "1.0",
        "type": type_val,
        "description": TYPE_META[type_val]["description"],
        "generatedBy": "scripts/tooling/indexing/build_resource_indexes.py",
        "masterIndex": "snippets-index.json",
        "pathConvention": (
            "Paths are tech-first WITHOUT the `library/` prefix "
            "(matching snippets-index.json). The on-disk location of every "
            "entry is `library/<path>`. Install an entry with "
            "`npx devsnips add <id>` when it carries an `install` field."
        ),
        "stats": {
            "families": len(sel),
            "resources": resources,
            "installable": installable,
            "byTechnology": {k: by_tech[k] for k in sorted(by_tech)},
        },
        "families": [make_family_entry(f) for f in sel],
    }


def main():
    data, families = rb.build_index()
    problems = rb.validate(data, families)
    if problems:
        print("VALIDATION PROBLEMS (%d):" % len(problems))
        for p in problems:
            print("  -", p)
        print("NOT writing any index due to validation problems.")
        sys.exit(1)

    # 1. Master index (schema unchanged, mirrors rebuild_index.py output).
    MASTER.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    print("Wrote snippets-index.json (%d families, %d variants)" % (
        data["stats"]["totalFamilies"], data["stats"]["totalVariants"]))

    # 2. Specialized indexes, derived from the same in-memory families.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for type_val, meta in TYPE_META.items():
        payload = build_specialized(families, type_val)
        out = OUT_DIR / meta["file"]
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                       encoding="utf-8")
        print("Wrote %s (%d families, %d resources)" % (
            out.relative_to(ROOT).as_posix(),
            payload["stats"]["families"], payload["stats"]["resources"]))

    # 3. Coverage audit (nothing is silently skipped: rebuild_index's
    #    validate() already guarantees indexed == disk, so any resource that
    #    could not be indexed would have surfaced as a validation problem).
    print("")
    print("Coverage by technology x type:")
    for tech in (rb.TAILWIND, rb.VANILLA, rb.REACT):
        counts = {}
        for f in families:
            if f["tech"] == tech:
                counts[f["type"]] = counts.get(f["type"], 0) + f["variantsCount"]
        print("  %-18s components=%-4d sections=%-4d templates=%d" % (
            tech, counts.get("component", 0), counts.get("section", 0),
            counts.get("template", 0)))


if __name__ == "__main__":
    main()
