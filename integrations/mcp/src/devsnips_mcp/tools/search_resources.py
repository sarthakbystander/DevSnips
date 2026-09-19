"""`search_resources` â€” deterministic discovery over the DevSnips registry."""

from typing import Any

from . import get_context, run_guarded


def register(mcp: Any) -> None:
    @mcp.tool()
    async def search_resources(
        query: str | None = None,
        technology: str | None = None,
        type: str | None = None,
        category: str | None = None,
        family: str | None = None,
        tags: list[str] | None = None,
        tagsMode: str = "all",
        styles: list[str] | None = None,
        features: list[str] | None = None,
        installableOnly: bool = False,
        limit: int = 10,
        offset: int = 0,
    ) -> str:
        """Search the DevSnips UI library (components, sections, templates).

        Deterministic keyword search over names, ids, family names, curated
        searchTerms, tags, styles, features and descriptions. Provide a natural
        language query, structured filters, or both. Results are ranked with a
        fixed weighting and deterministic tie-breaking, so the same query
        against the same registry always returns the same order.

        Examples:
          search_resources(query="responsive SaaS pricing section", technology="React")
          search_resources(query="dark dashboard sidebar", type="component")
          search_resources(technology="Tailwind CSS", type="section", family="Pricing")

        Args:
            query: free-text query (stopwords and plurals are normalized).
            technology: filter â€” React, Tailwind (CSS), Vanilla (HTML/CSS/JS); aliases accepted.
            type: filter â€” component | section | template.
            category: filter â€” Components | Sections | Templates.
            family: substring filter on the family path (e.g. "Buttons", "AI-Product").
            tags: tag filter; combined per tagsMode.
            tagsMode: "all" (default, AND) or "any" (OR) for the tags filter.
            styles: style filter (all listed styles must be present).
            features: feature filter (all listed features must be present).
            installableOnly: only resources the DevSnips CLI can install.
            limit: page size, 1-50 (default 10).
            offset: zero-based page offset.
        """
        def run():
            app = get_context()
            registry, provenance = app.registry_with_provenance()
            result = app.engine(registry).search(
                query=query, technology=technology, type=type, category=category,
                family=family, tags=tags, tags_mode=(tagsMode or "all"),
                styles=styles, features=features,
                installable_only=bool(installableOnly), limit=limit, offset=offset)
            result["registry"] = provenance
            return result

        return run_guarded("search_resources", run)
