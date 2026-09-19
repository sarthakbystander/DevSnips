"""`get_resource` â€” metadata, docs and the file manifest for one resource."""

from typing import Any

from ..errors import FILE_NOT_FOUND, DevSnipsError
from ..files.resolver import rel_repo_path, resolve_variant
from ..registry.provider import library_rel_path
from . import get_context, run_guarded

VALID_INCLUDE = ("metadata", "readme", "agents", "files", "family")


def _fetch_doc(app, variant, filename: str, max_bytes: int | None) -> dict[str, Any]:
    rel = rel_repo_path(variant, filename)
    try:
        text, info = app.read_resource_text(rel, max_bytes=max_bytes)
    except DevSnipsError as exc:
        if exc.code == FILE_NOT_FOUND:
            return {"content": None, "error": "file_not_found",
                    "manifest_stale": True, "details": exc.details}
        raise
    return {"content": text, "bytes": len(text.encode("utf-8")),
            "truncated": bool(info.get("truncated")), "cached": bool(info.get("cached")),
            "stale": bool(info.get("stale")), "source": info.get("origin", "")}


def register(mcp: Any) -> None:
    @mcp.tool()
    async def get_resource(
        id: str,
        include: list[str] | None = None,
        maxBytes: int | None = None,
    ) -> str:
        """Get the descriptive package for one DevSnips resource: metadata, README,
        the template's AGENTS.md (templates ship one), and the file manifest â€”
        without pulling source code into context.

        Use `search_resources` first to find the canonical `id`.
        For template file trees, `files_complete` tells you whether the manifest
        is the whole tree (true for local checkouts; GitHub raw cannot enumerate,
        and some React template manifests list only one level of `src/**`).

        Args:
            id: canonical registry id, e.g. "Tailwind/Components/Accordions/basic-accordion".
            include: subset of metadata, readme, agents, files, family (default: metadata+readme+files;
                     templates automatically add agents when AGENTS.md exists).
            maxBytes: per-document byte cap for README/AGENTS content.
        """
        def run():
            app = get_context()
            registry, provenance = app.registry_with_provenance()
            variant = resolve_variant(registry, id)

            requested = [item for item in (include or ["metadata", "readme", "files"])
                         if item in VALID_INCLUDE]
            if variant.type == "template" and "AGENTS.md" in variant.files \
                    and include is None and "agents" not in requested:
                requested.append("agents")

            payload: dict[str, Any] = {
                "id": variant.id, "name": variant.name, "type": variant.type,
                "tech": variant.tech, "category": variant.category,
                "family": variant.family, "path": variant.path,
                "description": variant.description, "tags": list(variant.tags),
                "features": list(variant.features), "styles": list(variant.styles),
                "files": list(variant.files),
                "install": variant.install or None,
                "installable": variant.installable,
            }

            if "family" in requested:
                for family in registry.families:
                    if family.path.rstrip("/").lower() == variant.path.rstrip("/").lower() \
                            or variant.id.startswith(family.path.rstrip("/") + "/"):
                        payload["family_context"] = {
                            "name": family.name, "path": family.path,
                            "description": family.description,
                            "tags": list(family.tags),
                            "search_terms": list(family.search_terms),
                            "variants_count": family.variants_count,
                        }
                        break

            docs: dict[str, Any] = {}
            if "readme" in requested and "README.md" in variant.files:
                docs["README.md"] = _fetch_doc(app, variant, "README.md", maxBytes)
            if "agents" in requested and "AGENTS.md" in variant.files:
                docs["AGENTS.md"] = _fetch_doc(app, variant, "AGENTS.md", maxBytes)
            if docs:
                payload["docs"] = docs

            if "files" in requested:
                payload["files_base_url"] = app.provider.describe().origin
                listing = app.provider.list_files(library_rel_path(variant.path, ""))
                if listing is None:
                    payload["files_complete"] = None
                    payload["files_note"] = (
                        "the remote provider cannot enumerate directories; 'files' is the "
                        "registry manifest, which may be incomplete for some templates "
                        "(e.g. React templates list only one level of src/**). Use a local "
                        "checkout (DEVSNIPS_MCP_SOURCE=local) for the complete tree.")
                else:
                    on_disk = sorted(listing)
                    payload["files_complete"] = set(on_disk) == set(variant.files)
                    payload["files_on_disk"] = on_disk

            payload["registry"] = provenance
            return payload

        return run_guarded("get_resource", run)
