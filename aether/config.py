"""Configuration management for Aether CLI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env from current working directory or project root
load_dotenv()
load_dotenv(Path.cwd() / ".env")


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    model: str = Field(
        default_factory=lambda: os.getenv("AETHER_MODEL", "openai/gpt-4o")
    )
    max_tokens: int = Field(
        default_factory=lambda: int(os.getenv("AETHER_MAX_TOKENS", "4096"))
    )
    temperature: float = Field(
        default_factory=lambda: float(os.getenv("AETHER_TEMPERATURE", "0.2"))
    )
    system_prompt: str = Field(
        default_factory=lambda: os.getenv(
            "AETHER_SYSTEM_PROMPT",
            (
                "You are Aether, an expert AI coding assistant running inside a terminal. "
                "You help developers write, understand, refactor, and debug code. "
                "You have access to tools for reading/writing files and running shell commands. "
                "Be concise, accurate, and practical. When suggesting code changes, show clear diffs or full files. "
                "Always prioritize safety: never run destructive commands without clear user intent."
            ),
        )
    )

    # API keys (LiteLLM reads them from environment automatically)
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    xai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("XAI_API_KEY"))
    google_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("GOOGLE_API_KEY"))
    deepseek_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY"))

    def has_any_key(self) -> bool:
        """Return True if at least one API key is configured."""
        return any(
            [
                self.openai_api_key,
                self.anthropic_api_key,
                self.xai_api_key,
                self.google_api_key,
                self.deepseek_api_key,
            ]
        )


def get_settings() -> Settings:
    """Return a Settings instance."""
    return Settings()
