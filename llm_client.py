"""Thin MODEL-compatible LLM client — works with Ollama or cloud providers."""

from __future__ import annotations

import json
from typing import Any

from MODEL import MODEL

import config


def get_client() -> MODEL:
    """Build an MODEL client from config."""
    api_key = config.require_api_key()
    kwargs: dict[str, Any] = {"api_key": api_key}
    if config.MODEL_BASE_URL:
        kwargs["base_url"] = config.MODEL_BASE_URL
    return MODEL(**kwargs)


def chat_completion(
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: str | dict[str, Any] | None = "auto",
    temperature: float = 0.2,
) -> Any:
    """Send a chat completion request and return the response message."""
    client = get_client()
    kwargs: dict[str, Any] = {
        "model": config.MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
    }
    if tools is not None:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message


def message_to_dict(message: Any) -> dict[str, Any]:
    """Convert an SDK message object to a plain dict for conversation history."""
    payload: dict[str, Any] = {"role": message.role, "content": message.content}
    if message.tool_calls:
        payload["tool_calls"] = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in message.tool_calls
        ]
    return payload


def parse_tool_arguments(raw: str) -> dict[str, Any]:
    """Parse JSON tool arguments safely."""
    try:
        return json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
