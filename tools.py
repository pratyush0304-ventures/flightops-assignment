"""Plain Python tool functions for FlightOps — no agent frameworks."""

from __future__ import annotations

from typing import Any

from data import AIRCRAFT, AIRCRAFT_TYPES, FLIGHTS, GATES, MAINTENANCE, PASSENGERS, WEATHER


def _error(message: str, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"status": "error", "message": message}
    payload.update(extra)
    return payload


def _success(**payload: Any) -> dict[str, Any]:
    return {"status": "ok", **payload}


def get_flight_status(flight_number: str) -> dict[str, Any]:
    """Return status and schedule details for a flight."""
    try:
        key = flight_number.strip().upper()
        flight = FLIGHTS.get(key)
        if not flight:
            return _error(f"Flight {flight_number} not found")
        return _success(flight=flight)
    except Exception as exc:  # noqa: BLE001 — structured tool errors
        return _error(f"Failed to retrieve flight status: {exc}")


def search_passenger(name: str) -> dict[str, Any]:
    """Search passengers by partial name match."""
    try:
        query = name.strip().lower()
        if not query:
            return _error("Passenger name is required")
        matches = [p for p in PASSENGERS if query in p["name"].lower()]
        if not matches:
            return _error(f"No passenger found matching '{name}'")
        return _success(passengers=matches, count=len(matches))
    except Exception as exc:
        return _error(f"Passenger search failed: {exc}")


def maintenance_history(tail_number: str) -> dict[str, Any]:
    """Return maintenance records for an aircraft tail number."""
    try:
        key = tail_number.strip().upper()
        records = MAINTENANCE.get(key)
        if records is None:
            return _error(f"No maintenance history for tail {tail_number}")
        aircraft = AIRCRAFT.get(key, {})
        return _success(tail_number=key, aircraft=aircraft, records=records)
    except Exception as exc:
        return _error(f"Maintenance lookup failed: {exc}")


def find_available_gate(terminal: str) -> dict[str, Any]:
    """Find the first available gate in a terminal."""
    try:
        key = terminal.strip().upper()
        gates = GATES.get(key)
        if gates is None:
            return _error(f"Terminal {terminal} not found")
        available = [g for g in gates if g["status"] == "Available"]
        if not available:
            return _error(f"No available gates in {key}", terminal=key, gates=gates)
        return _success(terminal=key, available_gates=available, recommended=available[0])
    except Exception as exc:
        return _error(f"Gate search failed: {exc}")


def get_weather(airport: str) -> dict[str, Any]:
    """Return current weather for an airport. XXX triggers service failure."""
    try:
        key = airport.strip().upper()
        if key in {"XXX", "UNAVAILABLE"}:
            return {"status": "error", "message": "Weather service unavailable"}
        weather = WEATHER.get(key)
        if not weather:
            return _error(f"Weather data not available for airport {airport}")
        return _success(weather=weather)
    except Exception as exc:
        return _error(f"Weather lookup failed: {exc}")


def lookup_aircraft(aircraft_type: str) -> dict[str, Any]:
    """Look up specifications for an aircraft type (e.g., A320)."""
    try:
        key = aircraft_type.strip().upper()
        specs = AIRCRAFT_TYPES.get(key)
        if not specs:
            return _error(f"Aircraft type {aircraft_type} not found")
        fleet = [a for a in AIRCRAFT.values() if a["type"] == key]
        return _success(type=key, specifications=specs, fleet=fleet)
    except Exception as exc:
        return _error(f"Aircraft lookup failed: {exc}")


def get_departure_airport(flight_number: str) -> dict[str, Any]:
    """Return departure airport code for a flight."""
    try:
        key = flight_number.strip().upper()
        flight = FLIGHTS.get(key)
        if not flight:
            return _error(f"Flight {flight_number} not found")
        return _success(
            flight_number=key,
            departure_airport=flight["origin"],
            destination_airport=flight["destination"],
        )
    except Exception as exc:
        return _error(f"Departure airport lookup failed: {exc}")


# Registry used by agent for dynamic dispatch
TOOL_REGISTRY: dict[str, Any] = {
    "get_flight_status": get_flight_status,
    "search_passenger": search_passenger,
    "maintenance_history": maintenance_history,
    "find_available_gate": find_available_gate,
    "get_weather": get_weather,
    "lookup_aircraft": lookup_aircraft,
    "get_departure_airport": get_departure_airport,
}


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute a tool by name with JSON arguments."""
    func = TOOL_REGISTRY.get(name)
    if func is None:
        return _error(f"Unknown tool: {name}")
    try:
        return func(**arguments)
    except TypeError as exc:
        return _error(f"Invalid arguments for {name}: {exc}")
    except Exception as exc:
        return _error(f"Tool {name} raised an exception: {exc}")
