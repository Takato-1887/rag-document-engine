"""
Centralized configuration management for the RAG Document Engine.

Loads and validates all environment-driven settings using pydantic-settings.
Import `settings` anywhere in the codebase instead of calling os.environ
directly — this guarantees every config value is validated once, at
startup, rather than failing deep inside a pipeline at runtime.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class EmbeddingDevice(StrEnum):
    CUDA = "cuda"
    CPU = "cpu"


class LLMProvider(StrEnum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Settings(BaseSettings):
    """
    Application-wide settings, sourced from environment variables / .env file.

    Field names map 1:1 to .env keys (case-insensitive). Any missing
    required value will raise a ValidationError at import time —
    fail fast, fail loud, fail before the pipeline even starts.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_env: AppEnv = AppEnv.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO

    # --- Embedding / Model settings ---
    embedding_model_name: str = "BAAI/bge-small-en-v1.5"
    embedding_device: EmbeddingDevice = EmbeddingDevice.CUDA
    embedding_batch_size: int = Field(default=32, gt=0, le=512)

    # --- LLM settings ---
    llm_provider: LLMProvider = LLMProvider.OLLAMA
    llm_model_name: str = "llama3.1:8b"
    llm_base_url: str = "http://localhost:11434"

    # --- Vector store ---
    vector_store_path: Path = Path("./data/vector_store")
    chunk_size: int = Field(default=512, gt=0)
    chunk_overlap: int = Field(default=64, ge=0)

    # --- API keys (optional — only required if provider needs them) ---
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    @field_validator("chunk_overlap")
    @classmethod
    def overlap_must_be_smaller_than_chunk(cls, v: int, info: ValidationInfo) -> int:
        chunk_size = info.data.get("chunk_size")
        if chunk_size is not None and v >= chunk_size:
            raise ValueError(
                f"chunk_overlap ({v}) must be smaller than chunk_size ({chunk_size})"
            )
        return v

    @field_validator("vector_store_path")
    @classmethod
    def ensure_vector_store_dir_exists(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v

    def validate_provider_requirements(self) -> None:
        """
        Cross-field validation that can't be expressed as a single-field
        validator: if a cloud LLM provider is selected, its API key must
        be present. Call this explicitly at app startup (not on every
        import) so unit tests can construct partial Settings freely.
        """
        if self.llm_provider == LLMProvider.OPENAI and not self.openai_api_key:
            raise ValueError("LLM_PROVIDER=openai requires OPENAI_API_KEY to be set")
        if self.llm_provider == LLMProvider.ANTHROPIC and not self.anthropic_api_key:
            raise ValueError(
                "LLM_PROVIDER=anthropic requires ANTHROPIC_API_KEY to be set"
            )


settings = Settings()
