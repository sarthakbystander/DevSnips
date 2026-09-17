"""Validate the DevSnips index system against the repository.

Run:  python scripts/tooling/indexing/validate_indexes.py

Fails loudly (exit 1) on ANY problem. Cross-checks:

  snippets-index.json (master)
    - valid JSON with a families array
    - every variant path exists on disk with a metadata.json

  agents/resources/indexes/components-index.json   (type: component)
  agents/resources/indexes/sections-index.json     (type: section)
  agents/resources/indexes/templates-index.json    (type: template)
    - schema: required keys, correct `type`, masterIndex, generatedBy
    - unique ids + unique paths within and ACROSS the three indexes
    - ids are tech-first and match their path
    - every family/variant path exists on disk
    - every listed file exists inside its resource folder
    - `install` present iff the CLI would install the resource
      (mirrors cli/src/install/downloader.js getSourceFiles) and well-formed
    - deterministic ordering (families + variants sorted by path)
    - stats block consistent with the actual payload contents

  Orphans / staleness
    - every valid on-disk leaf appears in exactly the right specialized index
      (leaf detection reuses scripts/tooling/indexing/rebuild_index.py, so the
      validator can never drift from the generator's scanner)

  Master <-> specialized consistency
    - same variant path sets per type
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rebuild_index as rb  # noqa: E402  (same directory)

ROOT = rb.ROOT
MASTER = ROOT / "snippets-index.json"
IDX_DIR = ROOT / "agents" / "resources" / "indexes"
SPECIALIZED = {
    "component": IDX_DIR / "components-index.json",
    "section": IDX_DIR / "sections-index.json",
    "template": IDX_DIR / "templates-index.json",
}
# tech display name -> on-disk top-level directory name
TREE_ROOTS = {
    rb.TAILWIND: "Tailwind",
    rb.VANILLA: "Vanilla",
    rb.REACT: "React",
}
SOURCE_EXTS = {".html", ".jsx", ".tsx", ".js", ".ts", ".css"}
NEVER_INSTALL = {"metadata.json", "preview.html"}
DOCS_INSTALL = {"README.md", "AGENTS.md"}

problems = []


def fail(msg):
    problems.append(msg)


def load_json(path):
    if not path.exists():
        fail(f"Missing index file: {path.relative_to(ROOT).as_posix()}")
        return None
    try:
        import json
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"Invalid JSON in {path.relative_to(ROOT).as_posix()}: {e}")
        return None


def cli_would_install(files):
    """Mirror cli/src/install/downloader.js getSourceFiles: the CLI errors with
    'No source files found' only when NOTHING passes its filter."""
    for f in files:
        if f in NEVER_INSTALL:
            continue
        if f in DOCS_INSTALL:
            return True
        dot = f.rfind(".")
        if dot != -1 and f[dot:] in SOURCE_EXTS:
            return True
    return False


def disk_leaf_ids(tech, type_bucket):
    """On-disk leaf ids for one content tree, in index convention
    (tech-first, no `library/` prefix).

    Discovery MUST mirror the master generator's driver loop
    (rebuild_index.py main loop): each top-level directory under the tree is
    a family — Templates go through rb._template_leaves (a template family
    root with metadata.json and no child metadata IS the leaf, even though it
    fails is_leaf's component-style file tests: Tailwind template roots ship
    pages/ rather than a root code.html/preview.html), while Components/
    Sections use the generic recursive scanner.
    """
    tree = ROOT / "library" / TREE_ROOTS[tech] / type_bucket
    out = {}
    if not tree.exists():
        return out
    is_template = type_bucket == "Templates"
    for top in sorted(tree.iterdir()):
        if not top.is_dir():
            continue
        if is_template:
            leaves = rb._template_leaves(top, tech)
        else:
            leaves = rb.list_leaves_under(top, tech)
        for leaf, _meta in leaves:
            out[rb.rel_path(leaf)] = leaf
    return out


def fam_variant_map(payload, expected_type):
    """{(family_path, variant_path): entry} for one specialized payload."""
    if not isinstance(payload, dict) or not isinstance(payload.get("families"), list):
        fail("Payload has no families array")
        return {}
    if payload.get("type") != expected_type:
        fail("Wrong type in %s: %r (expected %r)" % (
            expected_type + "-index.json", payload.get("type"), expected_type))
    for key in ("version", "generatedBy", "masterIndex", "stats", "families"):
        if key not in payload:
            fail("Missing top-level key %r in %s" % (
                key, expected_type + "-index.json"))
    if payload.get("masterIndex") != "snippets-index.json":
        fail("masterIndex should be snippets-index.json in %s" % (
            expected_type + "-index.json"))
    out = {}
    for fam in payload.get("families", []):
        if fam.get("type") != expected_type:
            fail("Family %s has wrong type %r in %s" % (
                fam.get("path"), fam.get("type"),
                expected_type + "-index.json"))
        # expected_type is the lowercase enum ("component"); the family
        # `category` is the Capitalized bucket ("Components"/"Sections"/
        # "Templates") — same convention as snippets-index.json.
        if fam.get("category") != expected_type.capitalize() + "s":
            fail("Family %s has wrong category %r in %s" % (
                fam.get("path"), fam.get("category"),
                expected_type + "-index.json"))
        if fam.get("tech") not in TREE_ROOTS:
            fail("Family %s has invalid tech %r" % (
                fam.get("path"), fam.get("tech")))
        fpath = fam.get("path", "")
        fvariants = fam.get("variants")
        if not isinstance(fvariants, list):
            fail("Family %s has no variants array" % fpath)
            fvariants = []
        if fam.get("variantsCount") != len(fvariants):
            fail("variantsCount (%r) != len(variants) (%d) for family %s" % (
                fam.get("variantsCount"), len(fvariants), fpath))
        prev_names = []
        for v in fvariants:
            vpath = v.get("path", "")
            keypair = (fpath, vpath)
            if keypair in out:
                fail("Duplicate variant path in %s: %s" % (
                    expected_type + "-index.json", vpath))
            out[keypair] = v
            # id must equal the tech-first path without trailing slash
            vid = v.get("id", "")
            if vid != vpath.rstrip("/"):
                fail("id %r != path-without-slash %r (variant %s)" % (
                    vid, vpath.rstrip("/"), vpath))
            if v.get("type") != expected_type:
                fail("Variant %s has wrong type %r" % (vpath, v.get("type")))

            # disk existence: library/<tech-first path>
            leaf = ROOT / "library" / vpath.rstrip("/")
            if not (leaf / "metadata.json").exists():
                fail("Variant path missing on disk: %s" % vpath)
            else:
                # every listed file must exist inside the resource folder
                pages = {"pages", "src", "components", "data",
                         "sections", "styles"}
                for fname in v.get("files", []):
                    if "/" in fname:
                        top = fname.split("/", 1)[0]
                        if top not in pages:
                            fail("File %r listed with unsupported sub-dir "
                                 "in %s" % (fname, vpath))
                            continue
                    if not (leaf / fname).exists():
                        fail("Listed file missing on disk: %s (%s)" % (
                            fname, vpath))
                # install field: present iff the CLI would install
                has_install = "install" in v
                would = cli_would_install(v.get("files", []))
                if has_install and not would:
                    fail("install present but CLI would NOT install: %s"
                         % vpath)
                if would and not has_install:
                    fail("CLI would install but no install field: %s" % vpath)
                if has_install:
                    expected = "npx devsnips add " + vpath.rstrip("/")
                    if v["install"] != expected:
                        fail("install command %r != expected %r (%s)" % (
                            v["install"], expected, vpath))
            # tags/features/styles must be lists when present
            for k in ("tags", "features", "styles"):
                if k in v and not isinstance(v[k], list):
                    fail("Field %r is not a list in variant %s" % (k, vpath))
            prev_names.append(vpath)
        if prev_names != sorted(prev_names, key=str.lower):
            fail("Variants not sorted by path (case-insensitive) in "
                 "family %s" % fpath)

    # families sorted by path (case-insensitive)
    fpaths = [f.get("path", "") for f in payload.get("families", [])]
    if fpaths != sorted(fpaths, key=str.lower):
        fail("Families not sorted by path (case-insensitive) in %s" % (
            expected_type + "-index.json"))
    # stats cross-check
    st = payload.get("stats", {})
    fams = payload.get("families", [])
    if st.get("families") != len(fams):
        fail("stats.families (%r) != actual (%d)" % (
            st.get("families"), len(fams)))
    res = sum(len(f.get("variants", [])) for f in fams)
    if st.get("resources") != res:
        fail("stats.resources (%r) != actual (%d)" % (
            st.get("resources"), res))
    inst = sum(1 for f in fams for v in f.get("variants", [])
               if "install" in v)
    if st.get("installable") != inst:
        fail("stats.installable (%r) != actual (%d)" % (
            st.get("installable"), inst))
    by_tech = {}
    for f in fams:
        by_tech[f.get("tech")] = by_tech.get(
            f.get("tech"), 0) + len(f.get("variants", []))
    if st.get("byTechnology") != by_tech:
        fail("stats.byTechnology mismatch in %s: %r vs %r" % (
            expected_type + "-index.json",
            st.get("byTechnology"), by_tech))
    return out


def main():
    # --- Master index ---
    master = load_json(MASTER)
    master_paths = set()
    if master is not None:
        if not isinstance(master.get("families"), list):
            fail("Master index has no families array")
        else:
            for fam in master["families"]:
                for v in fam.get("variants", []):
                    p = v.get("path", "").rstrip("/")
                    master_paths.add(p)
                    leaf = ROOT / "library" / p
                    if not (leaf / "metadata.json").exists():
                        fail("Master variant missing on disk: %s" % p)
            st = master.get("stats", {})
            if st.get("totalVariants") != len(master_paths):
                fail("Master stats.totalVariants (%r) != actual (%d)" % (
                    st.get("totalVariants"), len(master_paths)))

    # --- Specialized indexes ---
    per_type = {}
    for type_val, idx_path in SPECIALIZED.items():
        payload = load_json(idx_path)
        if payload is None:
            continue
        per_type[type_val] = fam_variant_map(payload, type_val)

    # --- Cross-index duplicates ---
    seen = {}
    for type_val, kv in per_type.items():
        for (fpath, vpath) in kv:
            vkey = vpath.rstrip("/")
            if vkey in seen:
                fail("Variant path in multiple indexes: %s (%s then %s)" % (
                    vpath, seen[vkey], type_val))
            else:
                seen[vkey] = type_val

    # --- Orphans: every valid disk leaf must be in the right index ---
    # A specialized index holds all three technologies, so the key set must be
    # filtered per tech (by family-path prefix) before comparing with one
    # tech's disk tree — otherwise entries from the other techs would be
    # falsely reported as stale.
    for tech in (rb.TAILWIND, rb.VANILLA, rb.REACT):
        tech_dir = TREE_ROOTS[tech]
        for bucket, type_val in (("Components", "component"),
                                 ("Sections", "section"),
                                 ("Templates", "template")):
            disk = disk_leaf_ids(tech, bucket)
            idx_keys = {vp.rstrip("/") for (fp, vp) in
                        per_type.get(type_val, {})
                        if fp.split("/", 1)[0] == tech_dir}
            for leaf_id in disk:
                if leaf_id not in idx_keys:
                    fail("On-disk leaf NOT in %s: %s" % (
                        SPECIALIZED[type_val].name, leaf_id))
            for leaf_id in idx_keys:
                if leaf_id not in disk:
                    fail("Stale entry in %s (not on disk): %s" % (
                        SPECIALIZED[type_val].name, leaf_id))

    # --- Master <-> specialized consistency ---
    for type_val, kv in per_type.items():
        idx_keys = {vp.rstrip("/") for (fp, vp) in kv}
        missing = idx_keys - master_paths
        if missing:
            fail("%d %s entries missing from master index, e.g. %s" % (
                len(missing), type_val, sorted(missing)[0]))
        # Master may legitimately hold extra family-level rows? No: every
        # master variant must belong to exactly one specialized index.
        extra = master_paths - set(seen.keys())
        if extra:
            fail("%d master variants not in any specialized index, e.g. %s"
                 % (len(extra), sorted(extra)[0]))

    if problems:
        print("INDEX VALIDATION FAILED (%d problems):" % len(problems))
        for p in problems:
            print("  -", p)
        sys.exit(1)
    total = sum(len(kv) for kv in per_type.values())
    print("Index validation: OK")
    print("  Master: %d variants" % len(master_paths))
    for type_val in ("component", "section", "template"):
        n = len(per_type.get(type_val, {}))
        print("  %-10s %d resources" % (type_val, n))
    print("  Total: %d resources across all specialized indexes" % total)


if __name__ == "__main__":
    main()
