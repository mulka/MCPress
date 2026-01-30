"""Article tools for MCPress MCP server."""

from typing import Any

from fastmcp import FastMCP
from supabase import create_client

from mcpress.config import get_settings


def get_supabase_client():
    """Get a Supabase client instance."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def register_tools(mcp: FastMCP) -> None:
    """Register all article tools with the MCP server."""

    @mcp.tool
    def search_articles(query: str, limit: int = 10) -> list[dict[str, Any]]:
        """
        Search news articles by semantic similarity.

        Uses embedding-based vector search to find articles matching the query.

        Args:
            query: The search query text
            limit: Maximum number of articles to return (default: 10)

        Returns:
            List of matching articles with title, summary, author, and metadata
        """
        client = get_supabase_client()

        # Call the Supabase RPC function for vector similarity search
        # This assumes a function named 'search_articles' exists in Supabase
        # that takes a query embedding and returns matching articles
        result = client.rpc(
            "search_articles",
            {"query_text": query, "match_limit": limit},
        ).execute()

        return result.data if result.data else []

    @mcp.tool
    def get_article(article_id: str) -> dict[str, Any] | None:
        """
        Get a specific article by its ID.

        Args:
            article_id: The unique identifier of the article

        Returns:
            The article data including full content, or None if not found
        """
        client = get_supabase_client()

        result = (
            client.table("articles")
            .select("*")
            .eq("id", article_id)
            .single()
            .execute()
        )

        return result.data

    @mcp.tool
    def list_articles(
        category: str | None = None,
        media_source: str | None = None,
        author: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        List articles with optional filters.

        Args:
            category: Filter by article category (e.g., "politics", "technology")
            media_source: Filter by media organization name
            author: Filter by author name
            limit: Maximum number of articles to return (default: 20)
            offset: Number of articles to skip for pagination (default: 0)

        Returns:
            List of articles matching the filters, ordered by publish date (newest first)
        """
        client = get_supabase_client()

        query = client.table("articles").select(
            "id, title, summary, author, category, media_source, published_at, url"
        )

        if category:
            query = query.eq("category", category)
        if media_source:
            query = query.eq("media_source", media_source)
        if author:
            query = query.eq("author", author)

        result = (
            query.order("published_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )

        return result.data if result.data else []
