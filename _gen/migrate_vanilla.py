"""Phase 0 migration for the Vanilla library (deterministic, re-runnable).

Cleans up the structural/Schema inconsistencies identified in the Vanilla audit:

  A. Resolve duplicate collision pairs (a `snippet-NN-<name>` folder sitting
     next to a clean-named sibling that is the same concept).
       - True duplicates: delete the lesser stub, rename the richer
         `snippet-NN-<name>` -> `<name>` (overwriting the stub's slot).
       - Distinct variants: rename the `snippet-NN-<name>` to a distinct name
         and keep both.
       - Empty stub (no .html): delete the `snippet-NN-*` folder, keep the
         clean sibling.
  B. Rename all remaining `snippet-NN-<name>` folders to `<name>` (kebab),
     renaming the inner `<old>.html` to `<new>.html` too.
  C. Flatten `Vanilla/Components/Forms/<Subfamily>/<variant>/` to
     `Vanilla/Components/Forms/<variant>/` (matches every other family's
     2-level layout).
  D. Unify every legacy `metadata.json` to the rich schema used by the
     migrated sections (add slug/component/family/variant/framework/language/
     features/related/darkMode/accessibility), deriving `responsive`,
     `darkMode` and `accessibility` HONESTLY by scanning the component HTML.
     Strip `Snippet NN ` boilerplate from `name`/`description`, and remove the
     clearly-irrelevant `table` tag from non-Tables families.

The script is safe to dry-run:  DRY_RUN=1 python3 -m _gen.migrate_vanilla
It only writes when run without DRY_RUN. After it runs, regenerate the index:
    python3 -m _gen.rebuild_index && python3 scripts/validate.py
"""
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMP = ROOT / "Vanilla" / "Components"

SNIPPET_RE = re.compile(r"^snippet-(\d+)-(.+)$")

# ---------------------------------------------------------------------------
# Collision resolution map.
# Each entry: (snippet_folder_rel, action, dest_name)
#   action = "replace"  : delete the clean-named sibling, rename snippet -> dest
#   action = "distinct"  : rename snippet -> dest (distinct), keep sibling
#   action = "drop"      : delete the snippet folder entirely (no .html), keep sibling
# ---------------------------------------------------------------------------
COLLISIONS = [
    # True duplicates: keep the rich version under the clean name.
    ("Forms/Contact/snippet-13-contact-form", "replace", "contact-form"),
    ("Forms/Other/snippet-16-file-upload-input", "replace", "file-upload-input"),
    ("Modals/snippet-08-toast-notification", "replace", "toast-notification"),
    # Empty stub (no .html): drop it, keep clean sibling.
    ("Display/snippet-03-sticky-footer", "drop", "sticky-footer"),
    # Distinct variant: auto-hide-on-scroll vs simple position:sticky.
    ("Navigation/Navbar/snippet-02-sticky-header", "distinct", "auto-hide-sticky-header"),
]

# Tags that are noise on non-Tables components (a button tagged "table" is wrong).
NOISE_TAGS = {"table"}


def log(*a):
    print(*a)


# ---------------------------------------------------------------------------
# Step A + B: collision resolution and snippet-NN renames
# ---------------------------------------------------------------------------
def html_file_in(folder: Path):
    for f in folder.iterdir():
        if f.is_file() and f.suffix == ".html":
            return f
    return None


def rename_variant_folder(src: Path, dest_name: str, dry: bool):
    """Rename a variant folder + its inner <old>.html to the canonical
    `code.html` and rewrite metadata id/slug/name accordingly."""
    dest = src.parent / dest_name
    # In a "replace" collision the sibling stub is deleted first (only logged
    # during a dry run, so it still physically exists) — allow the rename to
    # proceed in dry mode without a false "target exists" error.
    if dest.exists() and not dry:
        raise RuntimeError(f"rename target exists: {dest}")
    log(f"  RENAME {src.relative_to(ROOT)} -> {dest_name}/")
    if dry:
        return
    shutil.move(str(src), str(dest))
    # rename inner html to the canonical component source filename
    old_html = html_file_in(dest)
    if old_html and old_html.name != "code.html":
        new_html = dest / "code.html"
        old_html.rename(new_html)
        log(f"          {old_html.name} -> {new_html.name}")
    # rewrite metadata id/slug/name to drop snippet-NN prefix
    mf = dest / "metadata.json"
    if mf.exists():
        m = json.loads(mf.read_text(encoding="utf-8"))
        old_id = m.get("id", "")
        if old_id.startswith("snippet-"):
            # snippet-NN-<name>-001 -> <dest_name>-001
            m["id"] = f"{dest_name}-001" if old_id.endswith("-001") else dest_name
        m["slug"] = dest_name
        nm = m.get("name", "")
        m["name"] = re.sub(r"^Snippet\s+\d+\s+", "", nm).strip()
        mf.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")


def resolve_collisions(dry: bool):
    log("\n=== Step A: resolve collision pairs ===")
    for rel, action, dest in COLLISIONS:
        snip = COMP / rel
        if not snip.exists():
            log(f"  SKIP {rel} (already migrated)")
            continue
        if action == "drop":
            log(f"  DROP   {rel} (empty stub, keep clean sibling {dest})")
            if not dry:
                shutil.rmtree(snip)
        elif action == "replace":
            sibling = snip.parent / dest
            if sibling.exists():
                log(f"  DELETE sibling stub {sibling.relative_to(ROOT)}")
                if not dry:
                    shutil.rmtree(sibling)
            rename_variant_folder(snip, dest, dry)
        elif action == "distinct":
            rename_variant_folder(snip, dest, dry)


def rename_remaining_snippets(dry: bool):
    log("\n=== Step B: rename remaining snippet-NN-* folders ===")
    targets = []
    for p in sorted(COMP.rglob("metadata.json")):
        leaf = p.parent
        m = SNIPPET_RE.match(leaf.name)
        if m:
            targets.append((leaf, m.group(2)))
    for leaf, dest_name in targets:
        rename_variant_folder(leaf, dest_name, dry)


# ---------------------------------------------------------------------------
# Step C: flatten Forms subcategories
# ---------------------------------------------------------------------------
def flatten_forms(dry: bool):
    log("\n=== Step C: flatten Forms/<Subfamily>/<variant> -> Forms/<variant> ===")
    forms = COMP / "Forms"
    if not forms.exists():
        return
    subfamilies = [d for d in sorted(forms.iterdir())
                   if d.is_dir() and any(c.is_dir() for c in d.iterdir())]
    for sub in subfamilies:
        for variant in sorted(sub.iterdir()):
            if not variant.is_dir():
                continue
            dest = forms / variant.name
            if dest.exists():
                raise RuntimeError(
                    f"flatten collision: {dest} already exists "
                    f"(from {variant})")
            log(f"  MOVE {variant.relative_to(ROOT)} -> Forms/{variant.name}/")
            if not dry:
                shutil.move(str(variant), str(dest))
        # remove the now-empty subfamily folder
        remaining = [c for c in sub.iterdir() if not c.name.startswith(".")]
        if not remaining:
            log(f"  RMDIR {sub.relative_to(ROOT)} (empty)")
            if not dry:
                sub.rmdir()


# ---------------------------------------------------------------------------
# Step D: unify legacy metadata to rich schema (honest flags via HTML scan)
# ---------------------------------------------------------------------------
def scan_html(folder: Path, all_files: bool = False):
    """Return (responsive, dark_mode, accessibility_features) from the HTML.

    By default scans the first .html in the folder (a single-variant component).
    With all_files=True (templates), scans every .html in the folder and ORs
    the signals.
    """
    responsive = False
    dark = False
    a11y = []
    htmls = []
    for f in folder.iterdir():
        if f.is_file() and f.suffix == ".html":
            htmls.append(f)
            if not all_files:
                break
    for html in htmls:
        if not html.exists():
            continue
        txt = html.read_text(encoding="utf-8", errors="ignore")
        low = txt.lower()
        if re.search(r"@media[^{]*(min|max)-width", low):
            responsive = True
        if "prefers-color-scheme" in low:
            dark = True
        if "prefers-reduced-motion" in low:
            a11y.append("reduced-motion")
        if re.search(r"\b(role|aria-)\b", low):
            a11y.append("ARIA")
        if re.search(r"tabindex|:focus-visible|focus-visible", low):
            a11y.append("focus-visible")
        sem = re.search(
            r"<(main|nav|section|article|header|footer|aside|figure|figcaption)\b",
            low)
        if sem:
            a11y.append("semantic HTML")
        if "keyboard nav" not in a11y and re.search(
                r"role=[\"']?button|tabindex", low):
            a11y.append("keyboard nav")
    return responsive, dark, a11y


def clean_description(desc: str):
    if not desc:
        return desc
    d = re.sub(r"^Snippet\s+\d+\s+", "", desc).strip()
    for boilerplate in (
        " with responsive design with animations and hover interactions.",
        " with animations and hover interactions.",
        " with responsive design with animations.",
        " with animations.",
    ):
        if d.endswith(boilerplate):
            d = d[: -len(boilerplate)]
            break
    if d and not d.endswith("."):
        d += "."
    return d


def unify_metadata(dry: bool):
    log("\n=== Step D: unify legacy metadata to rich schema ===")
    RICH_KEYS = {"features", "related", "darkMode", "accessibility"}
    migrated = 0
    refresh = os.environ.get("REFRESH") == "1"
    for mf in sorted(COMP.rglob("metadata.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        if not refresh and RICH_KEYS.issubset(m.keys()):
            continue  # already rich
        leaf = mf.parent
        slug = leaf.name
        family_dir = leaf.parent
        family = family_dir.name.lower()
        # component = singular-ish family noun
        comp = family[:-1] if family.endswith("s") and family != "other" else family
        responsive, dark, a11y = scan_html(leaf)

        m["slug"] = slug
        m["component"] = comp
        m["family"] = family
        m["variant"] = slug
        m["framework"] = "Vanilla HTML/CSS/JS"
        m["language"] = "HTML"
        m["responsive"] = responsive
        m["darkMode"] = dark
        m["accessibility"] = a11y
        m["related"] = m.get("related", [])
        # features: honest capabilities, deduped
        feats = []
        if responsive:
            feats.append("responsive")
        if dark:
            feats.append("light/dark")
        feats.extend(a11y)
        m["features"] = list(dict.fromkeys(feats))
        # tags: drop irrelevant "table" on non-Tables families, dedupe
        tags = m.get("tags", [])
        if family != "tables" and "table" in tags:
            tags = [t for t in tags if t != "table"]
        m["tags"] = list(dict.fromkeys(tags))
        # name/description: strip Snippet NN boilerplate
        nm = m.get("name", "")
        m["name"] = re.sub(r"^Snippet\s+\d+\s+", "", nm).strip() or nm
        m["description"] = clean_description(m.get("description", ""))

        log(f"  UNIFY {leaf.relative_to(ROOT)}  "
            f"(resp={responsive} dark={dark} a11y={len(a11y)})")
        if not dry:
            mf.write_text(
                json.dumps(m, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8")
        migrated += 1
    log(f"  migrated {migrated} legacy metadata files")


def clean_templates(dry: bool):
    log("\n=== Step E: clean Vanilla Templates metadata (boilerplate + honest flags) ===")
    tdir = ROOT / "Vanilla" / "Templates"
    if not tdir.exists():
        return
    cleaned = 0
    for mf in sorted(tdir.rglob("metadata.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        if m.get("category") != "templates":
            continue
        leaf = mf.parent
        responsive, dark, a11y = scan_html(leaf, all_files=True)
        m["responsive"] = responsive
        m["darkMode"] = dark
        m["accessibility"] = a11y
        # features: honest template capabilities
        feats = []
        if responsive:
            feats.append("responsive")
        if dark:
            feats.append("light/dark")
        feats.extend(a11y)
        m["features"] = list(dict.fromkeys(feats))
        # description boilerplate cleanup
        m["description"] = clean_description(m.get("description", ""))
        log(f"  CLEAN {leaf.relative_to(ROOT)}  "
            f"(resp={responsive} dark={dark} a11y={len(a11y)})")
        if not dry:
            mf.write_text(
                json.dumps(m, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8")
        cleaned += 1
    log(f"  cleaned {cleaned} template metadata files")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    dry = os.environ.get("DRY_RUN") == "1"
    log("DevSnips Phase 0 — Vanilla migration"
        + ("  [DRY RUN — no writes]" if dry else "  [LIVE]"))
    resolve_collisions(dry)
    rename_remaining_snippets(dry)
    flatten_forms(dry)
    unify_metadata(dry)
    clean_templates(dry)
    log("\nDone. Next: python3 -m _gen.fix_duplicate_ids && "
        "python3 -m _gen.rebuild_index && python3 scripts/validate.py")


if __name__ == "__main__":
    main()
