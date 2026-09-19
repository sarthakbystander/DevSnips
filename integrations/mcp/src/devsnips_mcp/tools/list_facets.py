"""`list_facets` â€” orientation over the registry (technologies/types/families)."""

from typing import Any

from ..errors import INVALID_ARGUMENT, DevSnipsError
from ..search.engine import TECH_ALIASES
from . import get_context, run_guarded

VALID_FACETS = ("all", "technologies", "types", "categories", "families")
MAX_VARIANTS_LISTED = 500


def register(mcp: Any) -> None:
    @mcp.tool()
    async def list_facets(
        facet: str = "all",
        technology: str | None = None,
        includeVariants: bool = False,
    ) -> str:
        """List what exists in the DevSnips library: technologies, types, categories,
        and families with live counts â€” read from the current registry, never
        hardcoded, so the answer is always current inventory (including any
        technology or type added after this server was written).

        Args:
            facet: all | technologies | types | categories | families.
            technology: scope the families facet to one technology (aliases accepted).
            includeVariants: for the families facet, also list variant ids (capped at 500).
        """
        def run():
            app = get_context()
            registry, provenance = app.registry_with_provenance()
            facet_value = (facet or "all").lower()
            if facet_value not in VALID_FACETS:
                raise DevSnipsError(INVALID_ARGUMENT,
                                    f"facet must be one of {', '.join(VALID_FACETS)}",
                                    {"received": facet})
            payload: dict[str, Any] = {
                "schema": {"version": registry.schema_version,
                           "supported": provenance.get("schema_version") in ("2.0",),
                           "warnings": list(registry.warnings)},
                "stats": registry.stats,
                "registry": provenance,
            }
            want = set(VALID_FACETS) if facet_value == "all" else {facet_value}

            if "types" in want or "categories" in want:
                type_counts: dict[str, int] = {}
                category_counts: dict[str, int] = {}
                for family in registry.families:
                    if family.type:
                        type_counts[family.type] = type_counts.get(family.type, 0) + family.variants_count
                    if family.category:
                        category_counts[family.category] = category_counts.get(family.category, 0) + family.variants_count
                if "types" in want:
                    payload["types"] = [{"type": key, "count": value}
                                        for key, value in sorted(type_counts.items())]
                if "categories" in want:
                    payload["categories"] = [{"category": key, "count": value}
                                             for key, value in sorted(category_counts.items())]

            if "technologies" in want:
                tech_counts: dict[str, dict[str, int]] = {}
                for family in registry.families:
                    bucket = tech_counts.setdefault(family.tech, {"families": 0, "resources": 0})
                    bucket["families"] += 1
                    bucket["resources"] += family.variants_count
                alias_map: dict[str, Any] = {}
                for name in sorted(tech_counts):
                    aliases = sorted(a for a, names in TECH_ALIASES.items() if name in names)
                    alias_map[name] = aliases
                payload["technologies"] = [
                    {"name": name,
                     "aliases": alias_map.get(name, []),
                     "families": tech_counts[name]["families"],
                     "resources": tech_counts[name]["resources"],
                     "declared": next((t.get("families") for t in registry.technologies
                                       if t.get("name") == name), None)}
                    for name in sorted(tech_counts)]

            if "families" in want:
                needle = (technology or "").strip().lower()
                families = []
                for family in registry.families:
                    if needle and needle not in family.tech.lower() \
                            and not any(needle in alias for alias in TECH_ALIASES
                                        if family.tech in TECH_ALIASES[alias]):
                        continue
                    entry: dict[str, Any] = {
                        "name": family.name, "path": family.path, "tech": family.tech,
                        "type": family.type, "category": family.category,
                        "variants_count": family.variants_count,
                    }
                    if includeVariants:
                        entry["variant_ids"] = [v.id for v in family.variants[:MAX_VARIANTS_LISTED]]
                    families.append(entry)
                families.sort(key=lambda item: item["path"].lower())
                payload["families"] = families
            return payload

        return run_guarded("list_facets", run)
