import os
import sys
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Modular Application Configuration for Nugi Content Factory.
    Decoupled Model Provider Architecture (LLM, Image, Storage).
    Handles Desktop packaging paths and %LOCALAPPDATA% persistence.
    """
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
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
        default="http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:8000,http://localhost:8000",
        description="Comma-separated list of allowed CORS origins"
    )

    # Database Settings
    DATABASE_URL: str = Field(
        default="sqlite:///./nugi_content_factory.db",
        description="Database connection URL"
    )

    # Storage Settings
    STORAGE_PROVIDER: str = Field(default="local", description="Storage provider type: local")
    STORAGE_BASE_DIR: str = Field(
        default="./storage/assets",
        description="Filesystem directory for local asset persistence"
    )

    # =========================================================================
    # 1. LLM PROVIDER CONFIGURATION
    # =========================================================================
    LLM_PROVIDER: str = Field(default="mock", description="Active LLM provider: mock, openrouter, openai, anthropic, google, custom")
    LLM_API_KEY: Optional[str] = Field(default=None, description="Generic LLM API Key")
    LLM_BASE_URL: Optional[str] = Field(default=None, description="Generic LLM Base URL")
    LLM_MODEL: Optional[str] = Field(default=None, description="Generic LLM Model Name")

    # OpenRouter Specific
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, description="OpenRouter API Key")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="OpenRouter Gateway Base URL")
    OPENROUTER_MODEL: str = Field(default="google/gemini-2.5-flash-lite", description="OpenRouter Model Identifier")

    # OpenAI Specific / Compatible
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key")
    OPENAI_BASE_URL: str = Field(default="https://api.openai.com/v1", description="OpenAI Base URL")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", description="OpenAI Model Identifier")

    # Anthropic Specific
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API Key")
    ANTHROPIC_BASE_URL: str = Field(default="https://api.anthropic.com/v1", description="Anthropic Base URL")
    ANTHROPIC_MODEL: str = Field(default="claude-3-5-sonnet-20241022", description="Anthropic Model Identifier")

    # Google Direct Specific
    GOOGLE_API_KEY: Optional[str] = Field(default=None, description="Google Gemini Direct API Key")
    GOOGLE_MODEL: str = Field(default="gemini-1.5-flash", description="Google Model Identifier")

    # =========================================================================
    # 2. IMAGE PROVIDER CONFIGURATION
    # =========================================================================
    IMAGE_PROVIDER: str = Field(default="mock", description="Active Image provider: mock, flux, openrouter, openai, custom")
    IMAGE_API_KEY: Optional[str] = Field(default=None, description="Generic Image Provider API Key")
    IMAGE_BASE_URL: Optional[str] = Field(default=None, description="Generic Image Provider Endpoint URL")
    IMAGE_ENDPOINT: Optional[str] = Field(default=None, description="Alias for Image Provider Endpoint")
    IMAGE_MODEL: Optional[str] = Field(default=None, description="Generic Image Model Name")

    # Flux / Black Forest Labs Specific
    FLUX_API_KEY: Optional[str] = Field(default=None, description="Flux / BFL API Key")
    FLUX_MODEL: str = Field(default="flux-2-klein-9b", description="Flux Model: flux-2-klein-9b, flux-1.1-pro, flux-dev, flux-schnell")
    FLUX_BASE_URL: str = Field(default="https://api.bfl.ai/v1", description="Flux API Gateway Base URL")

    # Knowledge Source (read-only path to the business knowledge repository)
    KNOWLEDGE_SOURCE_PATH: Optional[str] = Field(
        default=None,
        description="Filesystem path to the business knowledge repo (freelance-nugi-software-engineer). Auto-detected as sibling when unset."
    )

    # Canvas & Rendering System Defaults
    DEFAULT_IMAGE_WIDTH: int = Field(default=1080, description="Default canvas width in pixels")
    DEFAULT_IMAGE_HEIGHT: int = Field(default=1350, description="Default canvas height in pixels")
    DEFAULT_FONT_FAMILY: str = Field(default="sans-serif", description="Default font family")

    @property
    def cors_origins(self) -> List[str]:
        """Parsed list of allowed CORS origins."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def is_testing(self) -> bool:
        return self.APP_ENV.lower() == "testing"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production" or getattr(sys, "frozen", False)

    @property
    def knowledge_source_dir(self) -> Optional[Path]:
        """
        Resolves the read-only business knowledge repository directory.
        Priority:
        1. Explicit KNOWLEDGE_SOURCE_PATH (if it is a valid directory).
        2. The merged in-repo folder `<repo>/nugi-business` (single-repo layout).
        3. Legacy sibling folder `../freelance-nugi-software-engineer`.
        """
        if self.KNOWLEDGE_SOURCE_PATH:
            p = Path(self.KNOWLEDGE_SOURCE_PATH).expanduser()
            if p.is_dir():
                return p.resolve()

        repo_root = Path(__file__).resolve().parents[3]
        merged = repo_root / "nugi-business"
        if merged.is_dir():
            return merged.resolve()

        sibling = repo_root.parent / "freelance-nugi-software-engineer"
        if sibling.is_dir():
            return sibling.resolve()
        return None

    @property
    def user_data_dir(self) -> Path:
        """
        Returns the persistent per-user data directory (%LOCALAPPDATA%/Nugi Content Factory).
        Survives application updates and binary reinstalls.
        """
        if self.is_production:
            base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or "~/.nugi_content_factory"
            p = Path(base).expanduser() / "Nugi Content Factory"
        else:
            p = Path(".").resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def config_dir(self) -> Path:
        p = self.user_data_dir / "config"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def storage_path(self) -> Path:
        """Resolved Path object for storage directory."""
        if self.is_production:
            p = self.user_data_dir / "storage" / "assets"
        else:
            p = Path(self.STORAGE_BASE_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def logs_dir(self) -> Path:
        p = self.user_data_dir / "logs"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def effective_database_url(self) -> str:
        """Resolved Database URL."""
        if self.is_production:
            db_path = self.user_data_dir / "nugi_content_factory.db"
            return f"sqlite:///{db_path.as_posix()}"
        return self.DATABASE_URL

    def load_persistent_settings(self) -> None:
        """Loads user settings from persistent JSON file if available."""
        if self.is_testing:
            # Tests must never inherit real provider credentials from the local machine.
            return
        settings_file = self.config_dir / "provider_settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                llm = data.get("llm", {})
                if llm.get("provider"):
                    self.LLM_PROVIDER = llm["provider"]
                if llm.get("base_url"):
                    self.LLM_BASE_URL = llm["base_url"]
                    if self.LLM_PROVIDER == "openrouter":
                        self.OPENROUTER_BASE_URL = llm["base_url"]
                    elif self.LLM_PROVIDER == "openai":
                        self.OPENAI_BASE_URL = llm["base_url"]
                    elif self.LLM_PROVIDER == "anthropic":
                        self.ANTHROPIC_BASE_URL = llm["base_url"]
                if llm.get("api_key"):
                    self.LLM_API_KEY = llm["api_key"]
                    if self.LLM_PROVIDER == "openrouter":
                        self.OPENROUTER_API_KEY = llm["api_key"]
                    elif self.LLM_PROVIDER == "openai":
                        self.OPENAI_API_KEY = llm["api_key"]
                if llm.get("model"):
                    self.LLM_MODEL = llm["model"]
                    if self.LLM_PROVIDER == "openrouter":
                        self.OPENROUTER_MODEL = llm["model"]
                    elif self.LLM_PROVIDER == "openai":
                        self.OPENAI_MODEL = llm["model"]
                    elif self.LLM_PROVIDER == "anthropic":
                        self.ANTHROPIC_MODEL = llm["model"]
                    elif self.LLM_PROVIDER == "google":
                        self.GOOGLE_MODEL = llm["model"]

                img = data.get("image", {})
                if img.get("provider"):
                    self.IMAGE_PROVIDER = img["provider"]
                if img.get("endpoint_url"):
                    self.IMAGE_BASE_URL = img["endpoint_url"]
                    self.FLUX_BASE_URL = img["endpoint_url"]
                if img.get("api_key"):
                    self.IMAGE_API_KEY = img["api_key"]
                    self.FLUX_API_KEY = img["api_key"]
                if img.get("model"):
                    self.IMAGE_MODEL = img["model"]
                    self.FLUX_MODEL = img["model"]

            except Exception:
                pass

    def save_persistent_settings(self, data: Dict[str, Any]) -> None:
        """Saves user provider settings persistently to disk."""
        if self.is_testing:
            return
        settings_file = self.config_dir / "provider_settings.json"
        try:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass


settings = Settings()
# Initialize persistent settings if exists
settings.load_persistent_settings()
