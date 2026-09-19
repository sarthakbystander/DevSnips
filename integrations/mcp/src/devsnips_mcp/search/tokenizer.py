"""Deterministic tokenizer shared by indexing and queries.

Rules (mirrored identically on query and corpus — see implementation_plan.md §12):
- Unicode NFKC, lowercase, non-alphanumerics (including the corpus's mojibake
  em-dash sequences) collapse to spaces.
- Tokens shorter than 2 characters and a small stopword set are dropped.
- Light stemming: a single trailing "s" is stripped when the stem keeps at
  least 4 characters (buttons→button; sass stays sass). Applied symmetrically,
  so behavior is deterministic and reproducible.
"""
from __future__ import annotations

import re
import unicodedata

_SPLIT_RE = re.compile(r"[^0-9a-z]+")

STOPWORDS = frozenset({
    "a", "an", "the", "for", "with", "using", "and", "or", "of", "to", "in",
    "on", "at", "by", "my", "our", "your", "this", "that", "is", "are", "be",
    "it", "its", "as", "from", "into",
})

# Words in a query that express a resource-type intent. Detection only adds a
# bonus/penalty in ranking; it never overrides an explicit `type` filter.
TYPE_WORDS = {
    "component": "component", "components": "component",
    "section": "section", "sections": "section",
    "template": "template", "templates": "template",
}


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text or "").casefold()


def stem(token: str) -> str:
    if len(token) >= 5 and token.endswith("s"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    normalized = normalize(text)
    tokens: list[str] = []
    seen = set()
    for raw in _SPLIT_RE.split(normalized):
        if len(raw) < 2 or raw in STOPWORDS:
            continue
        token = stem(raw)
        if token and token not in seen:
            seen.add(token)
            tokens.append(token)
    return tokens


def detect_type_intent(tokens: list[str]) -> str | None:
    """Return the type implied by unstemmed type words in a token stream."""
    for token in tokens:
        raw = token
        if raw in TYPE_WORDS:
            return TYPE_WORDS[raw]
        # tokens are stemmed; a stripped plural may hide the original word
        if raw + "s" in TYPE_WORDS:
            return TYPE_WORDS[raw + "s"]
    return None
