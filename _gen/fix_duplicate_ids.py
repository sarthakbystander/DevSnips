"""Fix duplicate metadata IDs by family-namespacing the colliding ones.

A public registry / CLI needs globally-unique IDs. Two slugs legitimately
recur across different families (e.g. a `dark-mode-toggle` in `Display` and in
`Other`; a `contact-form` in `Forms` and in `Contact`). The slug stays the
same (it equals the folder name within its family) but the ID becomes
family-namespaced so it is globally unique.

Only IDs that appear in >1 metadata.json are rewritten. The rewrite is:
    <slug>-NNN  ->  <family>-<slug>-NNN
so `dark-mode-toggle-001` under family `display` becomes
`display-dark-mode-toggle-001`. Non-colliding IDs are left untouched (preserve
existing stable IDs).

Run:  python3 -m _gen.fix_duplicate_ids
Then: python3 -m _gen.rebuild_index && python3 scripts/validate.py
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    by_id = defaultdict(list)
    for mf in (ROOT / "Vanilla").rglob("metadata.json"):
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            continue
        mid = m.get("id")
        if mid:
            by_id[mid].append((mf, m))

    dups = {mid: locs for mid, locs in by_id.items() if len(locs) > 1}
    if not dups:
        print("No duplicate IDs. Nothing to do.")
        return

    changed = 0
    for mid, locs in sorted(dups.items()):
        print(f"Resolving duplicate id '{mid}' ({len(locs)} files):")
        for mf, m in locs:
            family = m.get("family") or mf.parent.parent.name
            slug = m.get("slug") or mf.parent.name
            # numeric suffix from the old id (e.g. '-001'); default to '-001'
            suffix = ""
            if mid.endswith(tuple(f"-{n:03d}" for n in range(1000))):
                suffix = mid[-4:]
            new_id = f"{family}-{slug}{suffix}"
            if new_id == m.get("id"):
                continue
            old = m["id"]
            m["id"] = new_id
            mf.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
            print(f"  {mf.relative_to(ROOT)}: {old} -> {new_id}")
            changed += 1
    print(f"\nRewrote {changed} duplicate ID(s) (family-namespaced).")


if __name__ == "__main__":
    main()
