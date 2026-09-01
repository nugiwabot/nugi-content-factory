import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env file.
    Follows 12-factor application methodology.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    # Core Application Settings
    APP_ENV: str = Field(default="development", description="Environment: development, testing, production")
    APP_NAME: str = Field(default="Nugi Content Factory", description="Application display name")
    APP_VERSION: str = Field(default="0.1.0", description="SemVer Application Version")
    DEBUG: bool = Field(default=True, description="Enable debug mode")

    # API Server Settings
    HOST: str = Field(default="127.0.0.1", description="Host to bind server")
    PORT: int = Field(default=8000, description="Port to listen on")
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    # Database Settings (SQLite default, PostgreSQL compatible)
    DATABASE_URL: str = Field(
        default="sqlite:///./nugi_content_factory.db",
        description="Database connection URL"
    )

    # Storage Settings
    STORAGE_PROVIDER: str = Field(default="local", description="Storage provider type: local, s3, etc.")
    STORAGE_BASE_DIR: str = Field(
        default="./storage/assets",
        description="Filesystem directory for local asset persistence"
    )

    # AI Provider Settings
    LLM_PROVIDER: str = Field(default="mock", description="Active LLM provider: mock, openai, anthropic")
    IMAGE_PROVIDER: str = Field(default="mock", description="Active Image provider: mock, flux")

    # API Keys & Endpoints (Loaded safely, never hardcoded)
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key for live LLM")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API Key for live LLM")
    FLUX_API_KEY: Optional[str] = Field(default=None, description="Flux / BFL API Key for image generation")
    FLUX_MODEL: str = Field(default="flux-1.1-pro", description="Flux model identifier: flux-1.1-pro, flux-dev, flux-schnell")
    FLUX_BASE_URL: str = Field(default="https://api.bfl.ml/v1", description="Flux API Gateway Base URL")

    # Rendering Engine Parameters
    DEFAULT_IMAGE_WIDTH: int = Field(default=1080, description="Default canvas width in pixels")
    DEFAULT_IMAGE_HEIGHT: int = Field(default=1080, description="Default canvas height in pixels")
    DEFAULT_FONT_FAMILY: str = Field(default="sans-serif", description="Default font family")

    @property
    def cors_origins(self) -> List[str]:
        """Parsed list of allowed CORS origins."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def is_testing(self) -> bool:
        return self.APP_ENV.lower() == "testing"

    @property
    def storage_path(self) -> Path:
        """Resolved Path object for storage directory."""
        path = Path(self.STORAGE_BASE_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
