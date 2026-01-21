"""
Configuration management for Phase 2 Authentication System.
Handles environment variables and settings.
"""

from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/todo_app_dev"

    # Authentication
    BETTER_AUTH_SECRET: str = "your-secret-key-here-minimum-32-characters-long"

    # Application
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"

    # CORS (comma-separated string from env, or list)
    CORS_ORIGINS: list[str] = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS_ORIGINS from comma-separated string or list."""
        if v is None or v == "":
            return ["http://localhost:3000", "http://localhost:8000"]
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # JWT
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 604800  # 7 days
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 2592000  # 30 days
    ALGORITHM: str = "HS256"

    # API
    API_PREFIX: str = "/api"
    API_TITLE: str = "Todo App Authentication API"
    API_VERSION: str = "0.1.0"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        # Don't parse JSON for list fields - use custom validator
        env_parse_none_str="",
    )

    def validate_settings(self) -> None:
        """Validate critical settings."""
        if len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters long")


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings instance from environment variables
    """
    settings = Settings()
    settings.validate_settings()
    return settings
