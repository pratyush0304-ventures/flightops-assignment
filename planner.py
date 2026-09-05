"""Planner — generates Goal and Plan before tool execution."""

from __future__ import annotations

from typing import Any

import config
from llm_client import chat_completion

PLANNER_SYSTEM = """You are a flight operations planning assistant.
Given a user question, produce:
1. GOAL: one sentence describing what must be determined.
2. PLAN: numbered steps listing which tools or data sources to use and why.
Do not answer the question yet — only plan."""


def generate_plan(user_question: str, *, demo: bool = False) -> dict[str, str]:
    """Call the LLM to produce a goal and plan for the user's question."""
    if demo or config.DEMO_MODE:
        return _demo_plan(user_question)

    messages = [
        {"role": "system", "content": PLANNER_SYSTEM},
        {
            "role": "user",
            "content": (
                f"Question: {user_question}\n\n"
                "Available tools: get_flight_status, search_passenger, "
                "maintenance_history, find_available_gate, get_weather, "
                "lookup_aircraft, get_departure_airport.\n"
                "Format your response as:\nGOAL: ...\nPLAN:\n1. ...\n2. ..."
            ),
        },
    ]
    response = chat_completion(messages, tools=None, temperature=0.3)
    text = (response.content or "").strip()
    goal, plan = _parse_goal_plan(text)
    return {"goal": goal, "plan": plan, "raw": text}


def _parse_goal_plan(text: str) -> tuple[str, str]:
    goal = ""
    plan = ""
    if "GOAL:" in text.upper():
        parts = text.split("PLAN:", 1) if "PLAN:" in text.upper() else text.split("Plan:", 1)
        goal_part = parts[0]
        goal = goal_part.split(":", 1)[-1].strip() if ":" in goal_part else goal_part.strip()
        if len(parts) > 1:
            plan = parts[1].strip()
    else:
        goal = text.split("\n", 1)[0].strip()
        plan = text
    return goal or "Determine operational answer for the user question.", plan or text


def _demo_plan(user_question: str) -> dict[str, str]:
    return {
        "goal": f"Assess operational status related to: {user_question}",
        "plan": (
            "1. Call get_flight_status for the referenced flight to check delays and aircraft.\n"
            "2. Call get_weather for the departure airport to evaluate external risk.\n"
            "3. Call maintenance_history for the assigned tail number to rule out technical holds.\n"
            "4. Synthesize findings into an on-time likelihood assessment."
        ),
        "raw": "(demo plan)",
    }
