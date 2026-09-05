"""FlightOps agent — multi-tool function calling loop."""

from __future__ import annotations

import json
from typing import Any

import config
from llm_client import chat_completion, message_to_dict, parse_tool_arguments
from schemas import TOOL_SCHEMAS
from tools import execute_tool

SYSTEM_PROMPT = """You are FlightOps, an airline operations assistant.
Use the provided tools to gather facts before answering.
Combine flight status, weather, maintenance, and gate data when assessing delays.
If a tool returns status "error", explain the limitation and continue with available data.
Be concise and operational in tone."""


def run_agent(
    user_question: str,
    *,
    tool_schemas: list[dict[str, Any]] | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    """
    Run the full function-calling lifecycle until the model returns a final answer.

    Returns dict with answer, tool_call_log, and raw messages.
    """
    schemas = tool_schemas or TOOL_SCHEMAS
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]
    audtl: list[dict[str, Any]] = []  #tool call audit log
    iterations = 0

    while iterations < config.MAX_TOOL_ITERATIONS:
        iterations += 1
        response = chat_completion(messages, tools=schemas)
        assistant_msg = message_to_dict(response)
        messages.append(assistant_msg)

        tool_calls = getattr(response, "tool_calls", None)
        if not tool_calls:
            answer = response.content or ""
            if verbose:
                _print_tool_log(audtl)
            return {
                "answer": answer.strip(),
                "tool_call_log": audtl,
                "messages": messages,
            }

        for tool_call in tool_calls:
            name = tool_call.function.name
            args = parse_tool_arguments(tool_call.function.arguments)
            result = execute_tool(name, args)
            entry = {
                "step": len(audtl) + 1,
                "tool": name,
                "arguments": args,
                "result": result,
            }
            audtl.append(entry)
            if verbose:
                print(f"  [Tool {entry['step']}] {name}({json.dumps(args)})")
                print(f"           -> {json.dumps(result, default=str)[:200]}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, default=str),
                }
            )

    if verbose:
        _print_tool_log(audtl)
    return {
        "answer": "Maximum tool iterations reached without a final answer.",
        "tool_call_log": audtl,
        "messages": messages,
    }


def _print_tool_log(audtl: list[dict[str, Any]]) -> None:
    if not audtl:
        print("  (no tools called)")
        return
    print("\n  Tool call sequence:")
    for entry in audtl:
        print(f"    {entry['step']}. {entry['tool']} {entry['arguments']}")


def run_agent_demo(user_question: str) -> dict[str, Any]:
    """Deterministic demo path when no API key is configured."""
    print("  [Demo mode] Simulating multi-tool agent run without LLM.")
    steps = [
        ("get_flight_status", {"flight_number": "AI203"}),
        ("get_weather", {"airport": "DEL"}),
        ("maintenance_history", {"tail_number": "VT-EXA"}),
    ]
    audtl: list[dict[str, Any]] = []
    for name, args in steps:
        result = execute_tool(name, args)
        audtl.append({"step": len(audtl) + 1, "tool": name, "arguments": args, "result": result})
        print(f"  [Tool {len(audtl)}] {name}({json.dumps(args)})")

    flight = audtl[0]["result"].get("flight", {})
    weather = audtl[1]["result"].get("weather", {})
    delay = flight.get("delay_minutes", 0)
    answer = (
        f"AI203 is currently {flight.get('status', 'unknown')} with a {delay}-minute delay "
        f"({flight.get('delay_reason', 'no reason given')}). "
        f"DEL weather: {weather.get('condition', 'unknown')} - {weather.get('impact', '')}. "
        f"Recent maintenance on {flight.get('aircraft_tail')} was completed, but combined "
        f"weather and existing delay suggest on-time departure is unlikely without further recovery."
    )
    _print_tool_log(audtl)
    return {"answer": answer, "tool_call_log": audtl, "messages": []}
