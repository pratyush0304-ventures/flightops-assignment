"""JSON-schema style tool declarations for MODEL function calling."""

from __future__ import annotations

from typing import Any

# --- Two versions of get_flight_status description (lazy vs careful) ---

LAZY_GET_FLIGHT_STATUS_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "get_flight_status",
        "description": "Get flight info.",
        "parameters": {
            "type": "object",
            "properties": {
                "flight_number": {
                    "type": "string",
                    "description": "Flight number",
                }
            },
            "required": ["flight_number"],
        },
    },
}

CAREFUL_GET_FLIGHT_STATUS_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "get_flight_status",
        "description": (
            "Retrieve live operational status for a commercial flight including "
            "scheduled/actual times, gate, terminal, assigned aircraft tail number, "
            "current delay minutes, and delay reason. Use when the user asks whether "
            "a flight is on time, delayed, boarding, or departed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "flight_number": {
                    "type": "string",
                    "description": (
                        "IATA-style flight number such as AI203. Case-insensitive."
                    ),
                }
            },
            "required": ["flight_number"],
        },
    },
}

# Default uses the careful schema
GET_FLIGHT_STATUS_SCHEMA = CAREFUL_GET_FLIGHT_STATUS_SCHEMA

SEARCH_PASSENGER_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "search_passenger",
        "description": (
            "Search the passenger manifest by partial or full name. Returns PNR, "
            "seat, check-in/boarding status, and associated flight."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Passenger name or substring to match.",
                }
            },
            "required": ["name"],
        },
    },
}

MAINTENANCE_HISTORY_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "maintenance_history",
        "description": (
            "Fetch maintenance records and aircraft metadata for a tail number. "
            "Use to assess airworthiness or recent technical issues affecting departure."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "tail_number": {
                    "type": "string",
                    "description": "Aircraft registration / tail number, e.g. VT-EXA.",
                }
            },
            "required": ["tail_number"],
        },
    },
}

FIND_AVAILABLE_GATE_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "find_available_gate",
        "description": (
            "List available gates at a terminal. Useful when reassigning flights "
            "or checking gate capacity."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "terminal": {
                    "type": "string",
                    "description": "Terminal identifier such as T2 or T3.",
                }
            },
            "required": ["terminal"],
        },
    },
}

GET_WEATHER_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "Get current weather and operational impact for an airport IATA code. "
            "Call for origin/destination when assessing delay risk."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "airport": {
                    "type": "string",
                    "description": "Three-letter airport code, e.g. DEL or BOM.",
                }
            },
            "required": ["airport"],
        },
    },
}

LOOKUP_AIRCRAFT_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "lookup_aircraft",
        "description": (
            "Look up fleet specifications and active aircraft for a type code "
            "such as A320 or B737."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "aircraft_type": {
                    "type": "string",
                    "description": "Aircraft type designator, e.g. A320.",
                }
            },
            "required": ["aircraft_type"],
        },
    },
}

GET_DEPARTURE_AIRPORT_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "get_departure_airport",
        "description": (
            "Resolve origin and destination airport codes for a given flight number."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "flight_number": {
                    "type": "string",
                    "description": "Flight number such as AI203.",
                }
            },
            "required": ["flight_number"],
        },
    },
}

# All tool schemas exported for the agent (careful flight status by default)
TOOL_SCHEMAS: list[dict[str, Any]] = [
    GET_FLIGHT_STATUS_SCHEMA,
    SEARCH_PASSENGER_SCHEMA,
    MAINTENANCE_HISTORY_SCHEMA,
    FIND_AVAILABLE_GATE_SCHEMA,
    GET_WEATHER_SCHEMA,
    LOOKUP_AIRCRAFT_SCHEMA,
    GET_DEPARTURE_AIRPORT_SCHEMA,
]

LAZY_TOOL_SCHEMAS: list[dict[str, Any]] = [
    LAZY_GET_FLIGHT_STATUS_SCHEMA,
    SEARCH_PASSENGER_SCHEMA,
    MAINTENANCE_HISTORY_SCHEMA,
    FIND_AVAILABLE_GATE_SCHEMA,
    GET_WEATHER_SCHEMA,
    LOOKUP_AIRCRAFT_SCHEMA,
    GET_DEPARTURE_AIRPORT_SCHEMA,
]

CAREFUL_TOOL_SCHEMAS: list[dict[str, Any]] = TOOL_SCHEMAS
