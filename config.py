"""Configuration for FlightOps assignment — loads settings from environment."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root if present (user copies from .env.example)
load_dotenv(Path(__file__).parent / ".env")

# Defaults target local Ollama (MODEL-compatible API at localhost:11434).
MODEL_USED: str | None = os.getenv("MODEL_USED", "ollama")
MODEL_NAME: str = os.getenv("MODEL_NAME", "qwen3.5:4b")
MODEL_BASE_URL: str | None = os.getenv("MODEL_BASE_URL", "http://localhost:11434/v1")

# Demo mode runs without a live LLM when explicitly disabled (empty API key + --demo).
DEMO_MODE: bool = os.getenv("MODEL_USED", "ollama") == ""

MAX_TOOL_ITERATIONS: int = int(os.getenv("MAX_TOOL_ITERATIONS", "8"))


def require_api_key() -> str:
    """Return API key for the configured LLM endpoint."""
    if MODEL_USED:
        return MODEL_USED
    raise RuntimeError(
        "MODEL_USED is not set. For local Ollama use MODEL_USED=ollama, "
        "or run in demo mode with --demo."
    )
