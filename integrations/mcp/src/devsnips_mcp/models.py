"""Data models for the DevSnips registry (snippets-index.json).

Parsing is defensive by design: a malformed family/variant record is skipped
(with a warning) rather than failing the whole registry load. Unknown fields
are ignored. Nothing here trusts registry content beyond what tools need.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .index.schema import derive_id, install_command, is_installable, schema_supported


@dataclass(frozen=True)
class Variant:
    id: str
    name: str
    type: str
    path: str
    tech: str
    category: str
    family: str
    description: str = ""
    tags: tuple[str, ...] = ()
    features: tuple[str, ...] = ()
    styles: tuple[str, ...] = ()
    files: tuple[str, ...] = ()
    installable: bool = False
    install: str = ""


@dataclass(frozen=True)
class Family:
    name: str
    path: str
    tech: str
    type: str
    category: str
    description: str = ""
    tags: tuple[str, ...] = ()
    search_terms: tuple[str, ...] = ()
    subcategory: str = ""
    variants: tuple[Variant, ...] = ()
    variants_count: int = 0


@dataclass
class Registry:
    schema_version: str
    last_updated: str
    stats: dict[str, Any]
    technologies: tuple[dict[str, Any], ...]
    families: tuple[Family, ...]
    by_id: dict[str, Variant] = field(default_factory=dict)
    by_id_ci: dict[str, str] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    def resolve(self, resource_id: str) -> Variant | None:
        canonical = self.by_id_ci.get(resource_id.strip().rstrip("/").lower())
        if canonical is None:
            return None
        return self.by_id.get(canonical)


def _str(value: Any, default: str = "") -> str:
    return value if isinstance(value, str) else default


def _str_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def _variant_from(raw: Any, family: dict[str, Any], warnings: list[str]) -> Variant | None:
    if not isinstance(raw, dict):
        return None
    path = _str(raw.get("path"))
    if not path:
        return None
    resource_id = _str(raw.get("id")) or derive_id(path)
    files = _str_tuple(raw.get("files"))
    installable = is_installable(files)
    return Variant(
        id=resource_id,
        name=_str(raw.get("name")) or resource_id.rsplit("/", 1)[-1],
        type=_str(raw.get("type"), _str(family.get("type"))),
        path=path,
        tech=_str(family.get("tech")),
        category=_str(family.get("category")),
        family=_str(family.get("name")),
        description=_str(raw.get("description")),
        tags=_str_tuple(raw.get("tags")),
        features=_str_tuple(raw.get("features")),
        styles=_str_tuple(raw.get("styles")),
        files=files,
        installable=installable,
        install=install_command(resource_id) if installable else "",
    )


def parse_registry(data: dict[str, Any]) -> Registry:
    """Parse + normalize a registry payload. Malformed records are skipped."""
    if not isinstance(data, dict):
        raise ValueError("registry payload is not a JSON object")  # noqa: TRY004 — loader maps ValueError→REGISTRY_INVALID
    families_raw = data.get("families")
    if not isinstance(families_raw, list):
        raise ValueError("registry is missing a families array")  # noqa: TRY004 — loader maps ValueError→REGISTRY_INVALID

    warnings: list[str] = []
    families: list[Family] = []
    by_id: dict[str, Variant] = {}
    by_id_ci: dict[str, str] = {}

    for index, raw_family in enumerate(families_raw):
        if not isinstance(raw_family, dict):
            warnings.append(f"families[{index}] is not an object; skipped")
            continue
        path = _str(raw_family.get("path"))
        if not path:
            warnings.append(f"families[{index}] has no path; skipped")
            continue
        variants_raw = raw_family.get("variants")
        variants: list[Variant] = []
        if isinstance(variants_raw, list):
            for raw_variant in variants_raw:
                variant = _variant_from(raw_variant, raw_family, warnings)
                if variant is None:
                    warnings.append(f"{path}: malformed variant skipped")
                    continue
                if variant.id in by_id:
                    warnings.append(f"duplicate id ignored: {variant.id}")
                    continue
                by_id[variant.id] = variant
                by_id_ci[variant.id.lower()] = variant.id
                variants.append(variant)
        declared_count = raw_family.get("variantsCount")
        variants_count = declared_count if isinstance(declared_count, int) else len(variants)
        families.append(Family(
            name=_str(raw_family.get("name")) or path.rstrip("/").rsplit("/", 1)[-1],
            path=path,
            tech=_str(raw_family.get("tech")),
            type=_str(raw_family.get("type")),
            category=_str(raw_family.get("category")),
            description=_str(raw_family.get("description")),
            tags=_str_tuple(raw_family.get("tags")),
            search_terms=_str_tuple(raw_family.get("searchTerms")),
            subcategory=_str(raw_family.get("subcategory")),
            variants=tuple(variants),
            variants_count=variants_count,
        ))

    version = data.get("version")
    if not schema_supported(version):
        warnings.append(f"unsupported registry schema version: {version!r}")
    stats_raw = data.get("stats")
    technologies_raw = data.get("technologies")
    return Registry(
        schema_version=_str(version),
        last_updated=_str(data.get("lastUpdated")),
        stats=stats_raw if isinstance(stats_raw, dict) else {},
        technologies=tuple(t for t in technologies_raw if isinstance(t, dict)) if isinstance(technologies_raw, list) else (),
        families=tuple(families),
        by_id=by_id,
        by_id_ci=by_id_ci,
        warnings=tuple(warnings),
    )
