"""Field weights for deterministic ranking (implementation_plan.md §12.2).

Weights were chosen so that identity (id/name) outranks curated intent
(searchTerms/tags/styles), which outranks prose (description). Any change here
must be re-snapshotted in tests/test_search.py — the ordering contract is
byte-identical determinism.
"""
from __future__ import annotations

WEIGHTS = {
    "id": 12,               # exact token in the canonical id/path
    "name": 8,              # token in display name
    "name_phrase": 10,      # whole query as a phrase in the display name
    "family_search_terms": 7,
    "tags": 6,
    "styles": 5,
    "family_name": 5,
    "family_name_phrase": 6,
    "category_type": 4,
    "features": 4,
    "family_tags": 4,
    "description": 3,
    "tech": 2,
}

EXACT_ID_BONUS = 40        # query equals the canonical id (pinned to rank 1)
TYPE_INTENT_BONUS = 6      # query's type word matches the variant type
TYPE_INTENT_PENALTY = 0.5  # multiplier when the type word contradicts the type
FAMILY_FILTER = "family"   # sentinel: family filter contributes no score weight
