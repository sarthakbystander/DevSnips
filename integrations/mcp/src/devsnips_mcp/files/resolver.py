"""Path/file resolution and safety for resource retrieval.

Two independent gates protect every fetch (implementation_plan.md §17):

1. Syntax gate — ids and filenames must match strict patterns (no `..`, no
   backslashes, no absolute paths, no URL-encoded separators, bounded length).
2. Registry allowlist — the id must exist in the loaded registry, and the
   filename must be a member of that variant's manifest plus the documented
   doc set. A traversal string can therefore never reach a fetch.
"""
from __future__ import annotations

import re

from ..errors import FILE_NOT_FOUND, INVALID_ARGUMENT, PATH_REJECTED, RESOURCE_NOT_FOUND, DevSnipsError
from ..models import Registry, Variant
from ..registry.provider import library_rel_path

_ID_RE = re.compile(r"^(react|tailwind|vanilla)/[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+){0,6}$", re.IGNORECASE)
_FILE_RE = re.compile(r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+){0,6}$")
MAX_ID_LENGTH = 200
MAX_FILE_LENGTH = 200

# Docs that may be fetched even when explicitly requested beyond the manifest.
# preview.html and metadata.json are retrievable ONLY by explicit request and
# never bundled implicitly (the CLI never installs them either).
DOCS = ("README.md", "AGENTS.md")

_TECH_CANONICAL = {"react": "React", "tailwind": "Tailwind", "vanilla": "Vanilla"}


def canonicalize_id(raw_id: str) -> str:
    if not isinstance(raw_id, str):
        raise DevSnipsError(INVALID_ARGUMENT, "id must be a string", {})
    candidate = raw_id.strip().replace("\\", "/").rstrip("/")
    if not candidate:
        raise DevSnipsError(INVALID_ARGUMENT, "id must not be empty", {})
    if len(candidate) > MAX_ID_LENGTH:
        raise DevSnipsError(INVALID_ARGUMENT, "id is too long", {"max_length": MAX_ID_LENGTH})
    match = _ID_RE.match(candidate)
    if ".." in candidate or match is None:
        raise DevSnipsError(
            PATH_REJECTED,
            "id is not a canonical DevSnips registry id",
            {
                "attempted": raw_id,
                "expected_shape": "<Technology>/<Type>/<Family>/<variant>[/style]",
                "example": "Tailwind/Components/Accordions/basic-accordion",
            },
        )
    # Normalize the technology segment to its canonical on-disk capitalization
    # (registry ids are always `React/…`, `Tailwind/…`, `Vanilla/…`).
    first, _, rest = candidate.partition("/")
    candidate = f"{_TECH_CANONICAL[first.lower()]}/{rest}"
    return candidate


def resolve_variant(registry: Registry, raw_id: str) -> Variant:
    canonical = canonicalize_id(raw_id)
    variant = registry.resolve(canonical)
    if variant is None:
        raise DevSnipsError(
            RESOURCE_NOT_FOUND,
            f"resource not found in the registry: {canonical}",
            {
                "suggestions": suggest_ids(registry, canonical),
                "registry": {"last_updated": registry.last_updated,
                             "variant_count": len(registry.by_id)},
                "hint": "call search_resources to discover valid ids",
            },
        )
    return variant


def suggest_ids(registry: Registry, raw_id: str, limit: int = 5) -> list[str]:
    import difflib

    normalized = raw_id.lower()
    prefix = [vid for vid in registry.by_id
              if vid.lower().startswith(normalized) or normalized.startswith(vid.lower())]
    close = difflib.get_close_matches(normalized, [vid.lower() for vid in registry.by_id],
                                      n=limit * 2, cutoff=0.5)
    lower_to_id = {vid.lower(): vid for vid in registry.by_id}
    ordered: list[str] = []
    for candidate in sorted(prefix, key=len) + [lower_to_id[c] for c in close]:
        if candidate not in ordered:
            ordered.append(candidate)
        if len(ordered) >= limit:
            break
    return ordered


def resolve_file(variant: Variant, raw_name: str) -> str:
    if not isinstance(raw_name, str):
        raise DevSnipsError(INVALID_ARGUMENT, "file must be a string", {})
    candidate = raw_name.strip().replace("\\", "/")
    candidate = candidate.removeprefix("./")
    if not candidate or len(candidate) > MAX_FILE_LENGTH:
        raise DevSnipsError(PATH_REJECTED, "file name is empty or too long",
                            {"attempted": raw_name, "max_length": MAX_FILE_LENGTH})
    if ".." in candidate or candidate.startswith("/") or not _FILE_RE.match(candidate):
        raise DevSnipsError(
            PATH_REJECTED,
            "file name rejected by the safety gate",
            {"attempted": raw_name, "rule": "repo-relative allowlisted path only"},
        )
    allowed = set(variant.files) | set(DOCS) | {"metadata.json"}
    if candidate not in allowed:
        matching = [name for name in allowed if name.lower() == candidate.lower()]
        if matching:
            return matching[0]  # case-insensitive match to the manifest spelling
        raise DevSnipsError(
            PATH_REJECTED,
            "file is not part of this resource",
            {
                "attempted": raw_name,
                "allowed_files": sorted(allowed)[:25],
                "note": "only files listed in the registry manifest (plus README/AGENTS/metadata) are retrievable",
            },
        )
    return candidate


def rel_repo_path(variant: Variant, filename: str) -> str:
    return library_rel_path(variant.path, filename)


def find_not_found_error(exc: DevSnipsError) -> bool:
    return exc.code == FILE_NOT_FOUND
