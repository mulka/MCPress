"""MCPress MCP Server - Main entry point."""

from fastmcp import FastMCP

from mcpress.tools import register_tools

# Create the MCP server
mcp = FastMCP("MCPress")

# Register all tools
register_tools(mcp)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
