"""Direct tool testing — Part 3 smoke tests without LLM."""

from __future__ import annotations

import json

from tools import (
    find_available_gate,
    get_departure_airport,
    get_flight_status,
    get_weather,
    lookup_aircraft,
    maintenance_history,
    search_passenger,
)


def _print_result(label: str, result: dict) -> None:
    print(f"\n=== {label} ===")
    print(json.dumps(result, indent=2, default=str))


def run_tool_tests() -> None:
    """Exercise every tool function with representative inputs."""
    print("FlightOps Tool Smoke Tests (Part 3)")
    print("=" * 50)

    _print_result("get_flight_status(AI203)", get_flight_status("AI203"))
    _print_result("get_flight_status(UNKNOWN)", get_flight_status("ZZ999"))

    _print_result("search_passenger(Priya)", search_passenger("Priya"))
    _print_result("search_passenger(Nobody)", search_passenger("Nobody Here"))

    _print_result("maintenance_history(VT-EXA)", maintenance_history("VT-EXA"))
    _print_result("maintenance_history(VT-XXX)", maintenance_history("VT-XXX"))

    _print_result("find_available_gate(T3)", find_available_gate("T3"))
    _print_result("find_available_gate(T9)", find_available_gate("T9"))

    _print_result("get_weather(DEL)", get_weather("DEL"))
    _print_result("get_weather(XXX) [should fail]", get_weather("XXX"))

    _print_result("lookup_aircraft(A320)", lookup_aircraft("A320"))
    _print_result("lookup_aircraft(A380)", lookup_aircraft("A380"))

    _print_result("get_departure_airport(AI203)", get_departure_airport("AI203"))

    print("\n" + "=" * 50)
    print("All tool smoke tests completed.")


if __name__ == "__main__":
    run_tool_tests()
