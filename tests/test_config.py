"""
Unit tests for src/config.py — validates that Settings correctly
enforces the invariants that matter for the RAG pipeline (chunk
overlap/size relationship, provider/API-key requirements).
"""

import pytest
from pydantic import ValidationError

from src.config import LLMProvider, Settings


def test_settings_load_with_defaults():
    """Settings should load successfully using .env / defaults."""
    settings = Settings()
    assert settings.chunk_size > 0
    assert settings.chunk_overlap < settings.chunk_size


def test_chunk_overlap_must_be_smaller_than_chunk_size():
    """chunk_overlap >= chunk_size should fail validation."""
    with pytest.raises(ValidationError):
        Settings(chunk_size=100, chunk_overlap=100)


def test_chunk_overlap_equal_to_chunk_size_fails():
    """Boundary case: equal values are also invalid, not just greater."""
    with pytest.raises(ValidationError):
        Settings(chunk_size=200, chunk_overlap=200)


def test_openai_provider_requires_api_key():
    """Selecting openai as provider without a key should fail
    when validate_provider_requirements() is explicitly called."""
    settings = Settings(llm_provider=LLMProvider.OPENAI, openai_api_key=None)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        settings.validate_provider_requirements()


def test_anthropic_provider_requires_api_key():
    settings = Settings(llm_provider=LLMProvider.ANTHROPIC, anthropic_api_key=None)
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
        settings.validate_provider_requirements()


def test_ollama_provider_does_not_require_api_key():
    """Local provider (ollama) should validate fine with no keys set."""
    settings = Settings(llm_provider=LLMProvider.OLLAMA)
    settings.validate_provider_requirements()  # should not raise