"""Reflector — post-answer critique of tool usage and confidence."""

from __future__ import annotations

from typing import Any

import config
from llm_client import chat_completion

REFLECTOR_SYSTEM = """You are a quality reviewer for an airline operations agent.
After the agent answered a question using tools, reflect on:
- Which tools were used and whether they were sufficient
- Any missing information that would improve the answer
- Confidence level (high/medium/low) with brief justification
Keep the reflection to 4-6 sentences."""


def reflect(
    user_question: str,
    answer: str,
    tool_call_log: list[dict[str, Any]],
    *,
    demo: bool = False,
) -> dict[str, str]:
    """Generate a separate LLM reflection on the agent run."""
    if demo or config.DEMO_MODE:
        return _demo_reflection(tool_call_log)

    tool_summary = _summarize_tools(tool_call_log)
    messages = [
        {"role": "system", "content": REFLECTOR_SYSTEM},
        {
            "role": "user",
            "content": (
                f"Question: {user_question}\n\n"
                f"Tools used:\n{tool_summary}\n\n"
                f"Final answer:\n{answer}\n\n"
                "Provide your reflection."
            ),
        },
    ]
    response = chat_completion(messages, tools=None, temperature=0.4)
    text = (response.content or "").strip()
    return {"reflection": text}


def _summarize_tools(tool_call_log: list[dict[str, Any]]) -> str:
    if not tool_call_log:
        return "(none)"
    lines = []
    for entry in tool_call_log:
        status = entry.get("result", {}).get("status", "unknown")
        lines.append(
            f"- {entry.get('tool')}({entry.get('arguments')}) -> status={status}"
        )
    return "\n".join(lines)


def _demo_reflection(tool_call_log: list[dict[str, Any]]) -> dict[str, str]:
    tools_used = [e["tool"] for e in tool_call_log]
    return {
        "reflection": (
            f"The agent invoked {len(tool_call_log)} tools ({', '.join(tools_used)}), "
            "covering flight status, weather, and maintenance - appropriate for a delay "
            "assessment. Gate availability was not checked, which could matter if a "
            "gate change is needed. Confidence: medium - weather and existing delay "
            "data support the conclusion, but live ATC/ATC flow data was unavailable."
        )
    }
