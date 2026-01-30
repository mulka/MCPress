"""Article tools for MCPress MCP server."""

from typing import Any

from fastmcp import FastMCP
from supabase import create_client

from mcpress.config import get_settings


def get_supabase_client():
    """Get a Supabase client instance."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_key)


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
        # Vector search is not yet implemented.
        # To enable, add OpenAI embedding support and create a Supabase RPC function
        # for cosine similarity search against the article_embeddings table.
        return []

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
            .select(
                "id, url, title, author, published_date, content, summary, keywords, "
                "category_id, organization_id, image_url, created_at, updated_at, "
                "categories(name), organizations(name)"
            )
            .eq("id", article_id)
            .single()
            .execute()
        )

        if not result.data:
            return None

        article = result.data

        # Flatten the nested category and organization objects
        flattened = {
            "id": article["id"],
            "url": article["url"],
            "title": article["title"],
            "author": article["author"],
            "published_date": article["published_date"],
            "content": article["content"],
            "summary": article["summary"],
            "keywords": article["keywords"],
            "category_id": article["category_id"],
            "organization_id": article["organization_id"],
            "image_url": article["image_url"],
            "created_at": article["created_at"],
            "updated_at": article["updated_at"],
        }
        # Include category and organization names if available
        if article.get("categories") and article["categories"].get("name"):
            flattened["category"] = article["categories"]["name"]
        if article.get("organizations") and article["organizations"].get("name"):
            flattened["media_source"] = article["organizations"]["name"]

        return flattened

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

        # Build the query with proper column names from the schema
        query = client.table("articles").select(
            "id, url, title, author, published_date, content, summary, keywords, "
            "category_id, organization_id, image_url, created_at, updated_at, "
            "categories(name), organizations(name)"
        )

        # First resolve category name to category_id if filtering by category
        category_id = None
        if category:
            cat_result = (
                client.table("categories")
                .select("id")
                .eq("name", category)
                .single()
                .execute()
            )
            if cat_result.data:
                category_id = cat_result.data["id"]
            else:
                # No matching category found, return empty list
                return []

        # First resolve organization name to organization_id if filtering by media_source
        organization_id = None
        if media_source:
            org_result = (
                client.table("organizations")
                .select("id")
                .eq("name", media_source)
                .single()
                .execute()
            )
            if org_result.data:
                organization_id = org_result.data["id"]
            else:
                # No matching organization found, return empty list
                return []

        # Apply filters
        if category_id:
            query = query.eq("category_id", category_id)
        if organization_id:
            query = query.eq("organization_id", organization_id)
        if author:
            query = query.eq("author", author)

        result = (
            query.order("published_date", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )

        if not result.data:
            return []

        # Flatten the nested category and organization objects
        articles = []
        for article in result.data:
            flattened = {
                "id": article["id"],
                "url": article["url"],
                "title": article["title"],
                "author": article["author"],
                "published_date": article["published_date"],
                "content": article["content"],
                "summary": article["summary"],
                "keywords": article["keywords"],
                "category_id": article["category_id"],
                "organization_id": article["organization_id"],
                "image_url": article["image_url"],
                "created_at": article["created_at"],
                "updated_at": article["updated_at"],
            }
            # Include category and organization names if available
            if article.get("categories") and article["categories"].get("name"):
                flattened["category"] = article["categories"]["name"]
            if article.get("organizations") and article["organizations"].get("name"):
                flattened["media_source"] = article["organizations"]["name"]
            articles.append(flattened)

        return articles
