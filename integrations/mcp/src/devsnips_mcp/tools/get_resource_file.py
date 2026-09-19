"""`get_resource_file` â€” one allowlisted source/doc file from a resource."""

from typing import Any

from ..errors import DevSnipsError
from ..files.resolver import rel_repo_path, resolve_file, resolve_variant
from . import get_context, run_guarded


def register(mcp: Any) -> None:
    @mcp.tool()
    async def get_resource_file(
        id: str,
        file: str,
        maxBytes: int | None = None,
        truncate: bool = True,
    ) -> str:
        """Retrieve one file from a DevSnips resource (source, page, README, AGENTS.md).

        Only files listed in the resource's registry manifest (plus README.md /
        AGENTS.md / metadata.json when present) are retrievable â€” arbitrary paths
        are rejected. `preview.html` is a demo page and is never bundled implicitly;
        request it explicitly if you really want it.

        Templates: fetch page by page (e.g. file="pages/pricing.html"), or install
        the whole template with the CLI command from `get_resource(id).install`.

        Args:
            id: canonical registry id (see search_resources / get_resource).
            file: manifest file name, e.g. "code.tsx", "code.html", "pages/index.html".
            maxBytes: byte cap for this call (default: server setting, 512 KiB).
            truncate: when true (default), oversized files are returned truncated;
                      when false, a file_too_large error is returned instead.
        """
        def run():
            app = get_context()
            registry, provenance = app.registry_with_provenance()
            variant = resolve_variant(registry, id)
            filename = resolve_file(variant, file)
            rel = rel_repo_path(variant, filename)
            cap = maxBytes if maxBytes is not None else app.settings.max_file_bytes
            if cap is not None and cap < 1:
                return {"error": {"code": "invalid_argument",
                                  "message": "maxBytes must be >= 1", "details": {}}}
            data, info = app.read_resource_bytes(rel, max_bytes=cap)
            if info.get("truncated") and not truncate:
                from ..errors import FILE_TOO_LARGE
                raise DevSnipsError(
                    FILE_TOO_LARGE,
                    f"file exceeds the byte cap: {filename}",
                    {"bytes_returned": len(data), "limit": cap, "truncated_available": True})
            try:
                text = data.decode("utf-8")
                lossless = True
            except UnicodeDecodeError:
                text = data.decode("utf-8", errors="replace")
                lossless = False
            return {
                "id": variant.id,
                "file": filename,
                "content": text,
                "bytes": len(data),
                "truncated": bool(info.get("truncated")),
                "encoding_lossless": lossless,
                "cached": bool(info.get("cached")),
                "stale": bool(info.get("stale")),
                "source": {"origin": info.get("origin", ""), "ref": provenance["ref"],
                           "repo_path": rel},
                "install": variant.install or None,
                "registry": provenance,
            }

        return run_guarded("get_resource_file", run)
