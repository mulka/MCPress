---
name: FastMCP 3 Setup
overview: Set up a basic FastMCP 3 project structure in mcp-server/ with placeholder tools for searching and accessing news articles from Supabase.
todos:
  - id: pyproject
    content: Create pyproject.toml with FastMCP 3 and Supabase dependencies
    status: completed
  - id: config
    content: Create config.py and .env.example for Supabase configuration
    status: completed
  - id: server
    content: Create main server.py with FastMCP initialization
    status: completed
  - id: tools
    content: Create article tools (search_articles, get_article, list_articles)
    status: completed
  - id: readme
    content: Create README with setup and usage instructions
    status: completed
---

# FastMCP 3 MCP Server Setup

## Project Structure

```
mcp-server/
├── pyproject.toml          # Dependencies and project config
├── .env.example            # Environment variables template
├── README.md               # Setup and usage instructions
└── src/
    └── mcpress/
        ├── __init__.py
        ├── server.py       # Main FastMCP server
        ├── config.py       # Configuration/settings
        └── tools/
            ├── __init__.py
            └── articles.py # Article search tools
```

## Dependencies

- `fastmcp>=3.0.0b1` - MCP server framework
- `supabase` - Database client
- `python-dotenv` - Environment variable loading

## MCP Server Components

### Tools (in `tools/articles.py`)

Based on the requirements, the server will expose these tools:

1. **search_articles** - Search articles by keywords using embedding similarity
2. **get_article** - Retrieve a specific article by ID
3. **list_articles** - List articles with filters (category, date range, media source)

### Example Tool Structure

```python
from fastmcp import FastMCP

mcp = FastMCP("MCPress")

@mcp.tool
def search_articles(query: str, limit: int = 10) -> list[dict]:
    """Search news articles by semantic similarity."""
    # Will connect to Supabase for vector search
    pass

@mcp.tool
def get_article(article_id: str) -> dict:
    """Get a specific article by ID."""
    pass

@mcp.tool
def list_articles(
    category: str | None = None,
    media_source: str | None = None,
    limit: int = 20
) -> list[dict]:
    """List articles with optional filters."""
    pass
```

## Configuration

Environment variables needed:

- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase service role key

## Running the Server

```bash
cd mcp-server
pip install -e .
python -m mcpress.server
```