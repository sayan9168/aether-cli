"""Configuration management for Aether CLI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env from current working directory or project root
load_dotenv()
load_dotenv(Path.cwd() / ".env")

CONFIG_DIR = Path.home() / ".aether"
SESSIONS_DIR = CONFIG_DIR / "sessions"


def ensure_dirs() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


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
                "You have access to tools for reading/writing files, searching code, and running shell commands. "
                "Be concise, accurate, and practical. When suggesting code changes, show clear diffs or full files. "
                "Always prioritize safety: never run destructive commands without clear user intent. "
                "You work on Windows, Linux, macOS and Termux."
            ),
        )
    )

    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    xai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("XAI_API_KEY"))
    google_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("GOOGLE_API_KEY"))
    deepseek_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY"))

    def has_any_key(self) -> bool:
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
    ensure_dirs()
    return Settings()


def save_session(name: str, messages: list) -> str:
    """Save conversation to ~/.aether/sessions/<name>.json"""
    ensure_dirs()
    path = SESSIONS_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    return str(path)


def load_session(name: str) -> list | None:
    """Load conversation from ~/.aether/sessions/<name>.json"""
    path = SESSIONS_DIR / f"{name}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_sessions() -> list[str]:
    ensure_dirs()
    return sorted([p.stem for p in SESSIONS_DIR.glob("*.json")])
