"""Configuration for MCPress MCP server."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    supabase_url: str
    supabase_key: str

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not supabase_key:
            raise ValueError("SUPABASE_KEY environment variable is required")

        return cls(
            supabase_url=supabase_url,
            supabase_key=supabase_key,
        )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings.from_env()
