---
name: Update MCP server to match Supabase schema
overview: Update mcp-server code to align with the Supabase schema in supabase/migrations/001_create_schema.sql
todos:
  - id: update-list-articles
    content: Update list_articles function with correct column names and joins
    status: completed
  - id: update-get-article
    content: Update get_article function with joined category/organization data
    status: completed
  - id: stub-search-articles
    content: Keep search_articles as a stub (vector search to be implemented later)
    status: completed
---

## Summary

The mcp-server code needs significant updates to match the Supabase schema. The current code uses incorrect column names and table relationships that don't match the schema.

## Key Discrepancies

1. **articles table columns**: Current code uses `category`, `media_source`, `published_at` but schema uses `category_id`, `organization_id`, `published_date`
2. **Relationships**: Articles reference categories/organizations via foreign keys, not by name
3. **Vector search**: The RPC function `search_articles` doesn't exist in the schema - will keep as stub for now

## Changes Required

### 1. Update `list_articles` function ([mcp-server/src/mcpress/tools/articles.py](mcp-server/src/mcpress/tools/articles.py))

- Change select columns to match schema: `id, url, title, author, published_date, content, summary, keywords, category_id, organization_id, image_url, created_at, updated_at`
- Add proper joins for filtering:
- Filter by `category` (name) → join with categories table on category_id
- Filter by `media_source` (organization name) → join with organizations table on organization_id
- Update sort column from `published_at` to `published_date`
- Include category/organization names in response via inner join

### 2. Update `get_article` function ([mcp-server/src/mcpress/tools/articles.py](mcp-server/src/mcpress/tools/articles.py))

- Current implementation is mostly correct with `select("*")`
- Add optional: Include category_name and organization_name via join or separate query

### 3. Keep `search_articles` as a stub ([mcp-server/src/mcpress/tools/articles.py](mcp-server/src/mcpress/tools/articles.py))

The current implementation calls a non-existent RPC function. For now:

- Return an empty list or a clear message that vector search needs to be configured
- The full vector search implementation can be added later

## Implementation Order

1. Update `list_articles` with correct column names and joins
2. Update `get_article` with optional joined data
3. Keep `search_articles` as a stub (vector search deferred)