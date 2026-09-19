"""SearchEngine — deterministic field-weighted search over the registry.

Pipeline per search:
  1. normalize filters (technology aliases; enum validation)
  2. filter candidates
  3. rank by weighted token score with exact-id / type-intent adjustments
  4. tie-break: score desc → exact name match → shorter id → id ascending
  5. mode escalation: exact (all tokens) → partial (≥⌈n/2⌉ tokens) → fuzzy
     (difflib ratio ≥ 0.75 vs name/id, max 5)

Two identical calls against the same registry state return byte-identical
ordered ids. No randomness, no wall-clock inputs, no embeddings.
"""
from __future__ import annotations

import difflib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from ..errors import INVALID_ARGUMENT, DevSnipsError
from ..models import Registry, Variant
from .scoring import EXACT_ID_BONUS, TYPE_INTENT_BONUS, TYPE_INTENT_PENALTY, WEIGHTS
from .tokenizer import detect_type_intent, normalize, tokenize

VALID_TYPES = ("component", "section", "template")
VALID_CATEGORIES = ("components", "sections", "templates")
FUZZY_CUTOFF = 0.75
FUZZY_MAX = 5
MAX_LIMIT = 50
DEFAULT_LIMIT = 10

# Alias → set of canonical technology display names (mirrors the alias spirit
# of cli/src/utils/paths.js TECH_SLUG_MAP; display names come from the index).
TECH_ALIASES: dict[str, frozenset] = {
    "react": frozenset({"React"}),
    "tailwind": frozenset({"Tailwind CSS"}),
    "tailwindcss": frozenset({"Tailwind CSS"}),
    "tailwindcsscss": frozenset({"Tailwind CSS"}),
    "tailwind-css": frozenset({"Tailwind CSS"}),
    "vanilla": frozenset({"Vanilla HTML/CSS/JS"}),
    "html": frozenset({"Vanilla HTML/CSS/JS"}),
    "css": frozenset({"Vanilla HTML/CSS/JS"}),
    "js": frozenset({"Vanilla HTML/CSS/JS"}),
    "javascript": frozenset({"Vanilla HTML/CSS/JS"}),
}


@dataclass
class _Record:
    variant: Variant
    name_tokens: frozenset
    path_tokens: frozenset
    family_tokens: frozenset
    family_terms: tuple[str, ...]
    tags: frozenset
    styles: frozenset
    features: frozenset
    description_tokens: frozenset
    family_tags: frozenset
    tech: str
    tech_tokens: frozenset
    category: str
    type: str
    name_lower: str
    path_lower: str


class SearchEngine:
    def __init__(self, registry: Registry):
        self._registry = registry
        self._records: list[_Record] = []
        for family in registry.families:
            fam_tokens = frozenset(tokenize(family.name))
            fam_tags = frozenset(normalize(t) for t in family.tags)
            fam_terms = tuple(sorted(normalize(t) for t in family.search_terms))
            for variant in family.variants:
                self._records.append(self._build_record(variant, fam_tokens, fam_tags, fam_terms))

    # ----------------------------------------------------------- indexing ---
    @staticmethod
    def _build_record(variant: Variant, fam_tokens: frozenset, fam_tags: frozenset,
                      fam_terms: tuple[str, ...]) -> _Record:
        return _Record(
            variant=variant,
            name_tokens=frozenset(tokenize(variant.name)),
            path_tokens=frozenset(tokenize(variant.id.replace("/", " "))),
            family_tokens=fam_tokens,
            family_terms=fam_terms,
            tags=frozenset(normalize(t) for t in variant.tags),
            styles=frozenset(normalize(s) for s in variant.styles),
            features=frozenset(tokenize(" ".join(variant.features))),
            description_tokens=frozenset(tokenize(variant.description)),
            family_tags=fam_tags,
            tech=variant.tech,
            tech_tokens=frozenset(tokenize(variant.tech.replace("/", " "))),
            category=normalize(variant.category),
            type=variant.type,
            name_lower=normalize(variant.name),
            path_lower=normalize(variant.id),
        )

    # ------------------------------------------------------------- search ---
    def search(
        self,
        query: str | None = None,
        technology: str | None = None,
        type: str | None = None,
        category: str | None = None,
        family: str | None = None,
        tags: Sequence[str] | None = None,
        tags_mode: str = "all",
        styles: Sequence[str] | None = None,
        features: Sequence[str] | None = None,
        installable_only: bool = False,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit, offset = self._validate_paging(limit, offset)
        tags_mode = (tags_mode or "all").lower()
        if tags_mode not in ("all", "any"):
            raise DevSnipsError(INVALID_ARGUMENT, "tagsMode must be 'all' or 'any'",
                                {"received": tags_mode})
        wanted_types = self._normalize_type(type)
        wanted_category = self._normalize_category(category)
        tech_names = self._normalize_technology(technology)

        candidates = [r for r in self._records if self._passes(
            r, tech_names, wanted_types, wanted_category, family, tags, tags_mode,
            styles, features, installable_only)]
        total_matches = len(candidates)

        query_tokens = tokenize(query or "")
        if query_tokens:
            ranked = self._rank(candidates, query_tokens)
            mode = "exact"
            if not ranked:
                mode = "partial"
                ranked = self._rank(candidates, query_tokens, partial=True)
            if not ranked:
                mode = "fuzzy"
                ranked = self._fuzzy(candidates, normalize(query or ""))
        else:
            mode = "filtered"
            ranked = [(0.0, set(), r) for r in candidates]

        page = ranked[offset:offset + limit]
        items = [self._to_item(score, matched, record) for score, matched, record in page]
        return {
            "mode": mode,
            "items": items,
            "total_matches": total_matches,
            "truncated": (offset > 0) or (offset + len(page) < len(ranked)),
            "query": {"tokens": query_tokens, "offset": offset, "limit": limit},
        }

    # --------------------------------------------------------- validation ---
    @staticmethod
    def _validate_paging(limit: int, offset: int) -> tuple[int, int]:
        try:
            limit = DEFAULT_LIMIT if limit is None else int(limit)
            offset = 0 if offset is None else int(offset)
        except (TypeError, ValueError):
            raise DevSnipsError(INVALID_ARGUMENT, "limit/offset must be integers", {})
        if limit < 1 or limit > MAX_LIMIT:
            raise DevSnipsError(INVALID_ARGUMENT, f"limit must be between 1 and {MAX_LIMIT}",
                                {"received": limit})
        if offset < 0:
            raise DevSnipsError(INVALID_ARGUMENT, "offset must be >= 0", {"received": offset})
        return limit, offset

    @staticmethod
    def _normalize_type(type_value: str | None) -> str | None:
        if type_value is None:
            return None
        value = normalize(type_value).rstrip("s")
        if value not in VALID_TYPES:
            raise DevSnipsError(INVALID_ARGUMENT, "type must be component, section, or template",
                                {"received": type_value})
        return value

    @staticmethod
    def _normalize_category(category: str | None) -> str | None:
        if category is None:
            return None
        value = normalize(category)
        if value not in VALID_CATEGORIES:
            raise DevSnipsError(INVALID_ARGUMENT, "category must be Components, Sections, or Templates",
                                {"received": category})
        return value

    @staticmethod
    def _normalize_technology(technology: str | None) -> frozenset | None:
        if technology is None:
            return None
        value = normalize(technology).replace(" ", "").replace("/", "").replace("-", "")
        if value in TECH_ALIASES:
            return TECH_ALIASES[value]
        # Unknown technology: pass through as a display-name match (index-driven,
        # never hardcoded — future technologies work without MCP changes).
        return frozenset({technology.strip()})

    # ----------------------------------------------------------- filtering ---
    @staticmethod
    def _passes(record: _Record, tech_names: frozenset | None, wanted_type: str | None,
                wanted_category: str | None, family: str | None,
                tags: Sequence[str] | None, tags_mode: str,
                styles: Sequence[str] | None, features: Sequence[str] | None,
                installable_only: bool) -> bool:
        if tech_names is not None and record.tech not in tech_names:
            return False
        if wanted_type is not None and record.type != wanted_type:
            return False
        if wanted_category is not None and record.category != wanted_category:
            return False
        if family and normalize(family).strip() not in record.variant.path.lower():
            return False
        if tags:
            wanted = {normalize(t) for t in tags if normalize(t)}
            if tags_mode == "all" and not wanted.issubset(record.tags):
                return False
            if tags_mode == "any" and not record.tags.intersection(wanted):
                return False
        if styles:
            wanted = {normalize(s) for s in styles if normalize(s)}
            if not wanted.issubset(record.styles):
                return False
        if features:
            wanted = {normalize(f) for f in features if normalize(f)}
            if not wanted.issubset(record.features):
                return False
        return not (installable_only and not record.variant.installable)

    # ------------------------------------------------------------- ranking ---
    def _rank(self, candidates: list[_Record], query_tokens: list[str],
              partial: bool = False) -> list[tuple[float, set, _Record]]:
        intent = detect_type_intent(query_tokens)
        scored: list[tuple[float, set, _Record]] = []
        for record in candidates:
            score, matched, token_hits = self._score(record, query_tokens, intent)
            if partial:
                needed = max(1, (len(query_tokens) + 1) // 2)
                if token_hits < needed:
                    continue
            elif token_hits < len(query_tokens):
                continue
            scored.append((score, matched, record))
        scored.sort(key=self._tie_break)
        return scored

    def _score(self, record: _Record, query_tokens: list[str],
               intent: str | None) -> tuple[float, set, int]:
        score = 0.0
        matched: set = set()
        token_hits = 0
        query_lower = normalize(" ".join(query_tokens))
        for token in query_tokens:
            best_field: str | None = None
            best_weight = 0
            if token in record.path_tokens:
                best_field, best_weight = "id", WEIGHTS["id"]
            if token in record.name_tokens and WEIGHTS["name"] > best_weight:
                best_field, best_weight = "name", WEIGHTS["name"]
            if token in record.family_tokens and WEIGHTS["family_name"] > best_weight:
                best_field, best_weight = "family", WEIGHTS["family_name"]
            if (record.family_terms and token in record.family_terms
                    and WEIGHTS["family_search_terms"] > best_weight):
                best_field, best_weight = "family_search_terms", WEIGHTS["family_search_terms"]
            if token in record.tags and WEIGHTS["tags"] > best_weight:
                best_field, best_weight = "tags", WEIGHTS["tags"]
            if token in record.styles and WEIGHTS["styles"] > best_weight:
                best_field, best_weight = "styles", WEIGHTS["styles"]
            if (token in record.category or token == record.type) \
                    and WEIGHTS["category_type"] > best_weight:
                best_field, best_weight = "category_type", WEIGHTS["category_type"]
            if token in record.features and WEIGHTS["features"] > best_weight:
                best_field, best_weight = "features", WEIGHTS["features"]
            if token in record.family_tags and WEIGHTS["family_tags"] > best_weight:
                best_field, best_weight = "family_tags", WEIGHTS["family_tags"]
            if token in record.description_tokens and WEIGHTS["description"] > best_weight:
                best_field, best_weight = "description", WEIGHTS["description"]
            if token in record.tech_tokens and WEIGHTS["tech"] > best_weight:
                best_field, best_weight = "tech", WEIGHTS["tech"]
            if best_field is not None:
                score += best_weight
                matched.add(best_field)
                token_hits += 1
        if query_lower and query_lower in record.name_lower:
            score += WEIGHTS["name_phrase"]
            matched.add("name_phrase")
        if record.family_terms and any(query_lower in term for term in record.family_terms):
            score += WEIGHTS["family_name_phrase"]
            matched.add("family_search_terms")
        if query_lower == record.path_lower:
            score += EXACT_ID_BONUS
        if intent is not None:
            if record.type == intent:
                score += TYPE_INTENT_BONUS
            else:
                score *= TYPE_INTENT_PENALTY
        return score, matched, token_hits

    @staticmethod
    def _tie_break(entry: tuple[float, set, _Record]) -> tuple:
        score, _matched, record = entry
        exact_name = record.name_lower == record.path_lower.rsplit("/", 1)[-1]
        return (-score, 0 if exact_name else 1, len(record.variant.id), record.variant.id)

    def _fuzzy(self, candidates: list[_Record], query: str) -> list[tuple[float, set, _Record]]:
        fuzzy: list[tuple[float, set, _Record]] = []
        for record in candidates:
            ratio = max(difflib.SequenceMatcher(None, query, record.name_lower).ratio(),
                        difflib.SequenceMatcher(None, query, record.path_lower).ratio())
            if ratio >= FUZZY_CUTOFF:
                fuzzy.append((ratio, {"fuzzy"}, record))
        fuzzy.sort(key=lambda entry: (-entry[0], len(entry[2].variant.id), entry[2].variant.id))
        return fuzzy[:FUZZY_MAX]

    # -------------------------------------------------------------- output ---
    def _to_item(self, score: float, matched: set, record: _Record) -> dict[str, Any]:
        variant = record.variant
        return {
            "id": variant.id,
            "name": variant.name,
            "type": variant.type,
            "tech": variant.tech,
            "category": variant.category,
            "family": variant.family,
            "path": variant.path,
            "description": variant.description,
            "tags": list(variant.tags),
            "features": list(variant.features),
            "styles": list(variant.styles),
            "files": list(variant.files),
            "install": variant.install or None,
            "score": round(float(score), 3),
            "matched_fields": sorted(matched),
        }
