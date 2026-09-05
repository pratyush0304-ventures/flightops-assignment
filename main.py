"""FlightOps Assignment 04 — entry point orchestrating plan → agent → reflection."""

from __future__ import annotations

import argparse
import sys
import textwrap

import config
from agent import run_agent, run_agent_demo
from planner import generate_plan
from reflector import reflect

BANNER = """
+--------------------------------------------------------------+
|        Assignment 04: FlightOps Tool Calling & Agents        |
+--------------------------------------------------------------+
"""

EXAMPLE_QUERIES = [
    "Is AI203 likely to depart on time?",
    "Find passenger Priya Sharma and her flight status.",
    "What maintenance was done on VT-EXA?",
    "Is there an available gate at T3?",
    "What's the weather at DEL and BOM?",
    "I usually work Terminal 2, remember that.",
    "Find me an open gate.",
]


def _section(title: str, body: str) -> None:
    width = 62
    print(f"\n{'-' * width}")
    print(f"  {title}")
    print(f"{'-' * width}")
    wrapped = textwrap.fill(body, width=width, subsequent_indent="  ")
    print(f"  {wrapped}")


def run_pipeline(question: str, *, demo: bool = False) -> None:
    """Execute the full plan → agent → reflect pipeline."""
    use_demo = demo or config.DEMO_MODE

    if use_demo and not demo and config.DEMO_MODE:
        print("\n  Note: No LLM configured — running in demo mode.")
        print("  Start Ollama and pull qwen3.5:4b, or set MODEL_* in .env.\n")
    elif not use_demo:
        print(f"\n  Model: {config.MODEL_NAME} @ {config.MODEL_BASE_URL}\n")

    # --- Plan ---
    if use_demo:
        plan = generate_plan(question, demo=True)
    else:
        try:
            plan = generate_plan(question)
        except Exception as exc:
            print(f"\n  Planner error: {exc}")
            print("  Falling back to demo mode.\n")
            use_demo = True
            plan = generate_plan(question, demo=True)

    _section("GOAL", plan["goal"])
    _section("PLAN", plan["plan"])

    # --- Agent ---
    print(f"\n{'-' * 62}")
    print("  AGENT (tool execution loop)")
    print(f"{'-' * 62}")

    if use_demo:
        agent_result = run_agent_demo(question)
    else:
        try:
            agent_result = run_agent(question)
        except Exception as exc:
            print(f"\n  Agent error: {exc}")
            print("  Falling back to demo agent.\n")
            agent_result = run_agent_demo(question)

    _section("ANSWER", agent_result["answer"])

    # --- Reflection ---
    reflection = reflect(
        question, agent_result["answer"], agent_result["tool_call_log"], demo=use_demo
    )
    _section("REFLECTION", reflection["reflection"])

    tool_count = len(agent_result["tool_call_log"])
    print(f"\n  Tools invoked: {tool_count}")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FlightOps AI agent with tool calling (Assignment 04)."
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="Is AI203 likely to depart on time?",
        help="Natural language operations question",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Force demo mode without calling the LLM API",
    )
    parser.add_argument(
        "--test-tools",
        action="store_true",
        help="Run Part 3 tool smoke tests only (app.py)",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Print example prompts and exit",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print(BANNER)

    if args.examples:
        print("Example prompts:")
        for i, q in enumerate(EXAMPLE_QUERIES, 1):
            print(f"  {i}. {q}")
        print("\nRun: python main.py \"<your question>\"")
        return

    if args.test_tools:
        from app import run_tool_tests

        run_tool_tests()
        return

    try:
        run_pipeline(args.query, demo=args.demo)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)


if __name__ == "__main__":
    main()
