"""Mock FlightOps data dictionaries for tool-backed retrieval."""

FLIGHTS: dict[str, dict] = {
    "AI203": {
        "flight_number": "AI203",
        "origin": "DEL",
        "destination": "BOM",
        "scheduled_departure": "2026-08-20T14:30:00+05:30",
        "scheduled_arrival": "2026-08-20T16:45:00+05:30",
        "status": "Boarding",
        "gate": "G12",
        "terminal": "T3",
        "aircraft_tail": "VT-EXA",
        "aircraft_type": "A320",
        "delay_minutes": 25,
        "delay_reason": "Late inbound aircraft and minor maintenance check",
    },
    "AI101": {
        "flight_number": "AI101",
        "origin": "DEL",
        "destination": "BLR",
        "scheduled_departure": "2026-08-20T09:00:00+05:30",
        "scheduled_arrival": "2026-08-20T11:30:00+05:30",
        "status": "Departed",
        "gate": "G08",
        "terminal": "T3",
        "aircraft_tail": "VT-EXB",
        "aircraft_type": "B737",
        "delay_minutes": 0,
        "delay_reason": None,
    },
    "AI450": {
        "flight_number": "AI450",
        "origin": "BOM",
        "destination": "GOI",
        "scheduled_departure": "2026-08-20T18:00:00+05:30",
        "scheduled_arrival": "2026-08-20T19:15:00+05:30",
        "status": "Scheduled",
        "gate": None,
        "terminal": "T2",
        "aircraft_tail": "VT-EXC",
        "aircraft_type": "A320",
        "delay_minutes": 0,
        "delay_reason": None,
    },
}

AIRCRAFT: dict[str, dict] = {
    "VT-EXA": {
        "tail_number": "VT-EXA",
        "type": "A320",
        "manufacturer": "Airbus",
        "seats": 180,
        "status": "Active",
        "last_inspection": "2026-08-18",
        "notes": "Minor hydraulic leak addressed during pre-flight check",
    },
    "VT-EXB": {
        "tail_number": "VT-EXB",
        "type": "B737",
        "manufacturer": "Boeing",
        "seats": 162,
        "status": "Active",
        "last_inspection": "2026-08-15",
        "notes": "No open items",
    },
    "VT-EXC": {
        "tail_number": "VT-EXC",
        "type": "A320",
        "manufacturer": "Airbus",
        "seats": 180,
        "status": "Active",
        "last_inspection": "2026-08-19",
        "notes": "Ready for next rotation",
    },
}

AIRCRAFT_TYPES: dict[str, dict] = {
    "A320": {
        "type": "A320",
        "manufacturer": "Airbus",
        "typical_seats": 180,
        "range_km": 6100,
        "cruise_speed_kmh": 828,
    },
    "B737": {
        "type": "B737",
        "manufacturer": "Boeing",
        "typical_seats": 162,
        "range_km": 5765,
        "cruise_speed_kmh": 842,
    },
}

PASSENGERS: list[dict] = [
    {
        "name": "Priya Sharma",
        "pnr": "ABC123",
        "flight_number": "AI203",
        "seat": "12A",
        "status": "Checked In",
        "baggage_count": 1,
    },
    {
        "name": "Rahul Mehta",
        "pnr": "DEF456",
        "flight_number": "AI203",
        "seat": "14C",
        "status": "Boarded",
        "baggage_count": 2,
    },
    {
        "name": "Anita Desai",
        "pnr": "GHI789",
        "flight_number": "AI101",
        "seat": "8F",
        "status": "Departed",
        "baggage_count": 1,
    },
]

MAINTENANCE: dict[str, list[dict]] = {
    "VT-EXA": [
        {
            "date": "2026-08-20",
            "type": "A-Check follow-up",
            "description": "Hydraulic line inspection after overnight alert",
            "status": "Completed",
            "technician": "M. Kapoor",
        },
        {
            "date": "2026-08-10",
            "type": "Scheduled",
            "description": "Routine A320 line maintenance",
            "status": "Completed",
            "technician": "S. Iyer",
        },
    ],
    "VT-EXB": [
        {
            "date": "2026-08-05",
            "type": "Scheduled",
            "description": "Engine borescope inspection",
            "status": "Completed",
            "technician": "L. Singh",
        },
    ],
    "VT-EXC": [
        {
            "date": "2026-08-19",
            "type": "Scheduled",
            "description": "Pre-rotation walkaround and avionics test",
            "status": "Completed",
            "technician": "P. Nair",
        },
    ],
}

WEATHER: dict[str, dict] = {
    "DEL": {
        "airport": "DEL",
        "condition": "Thunderstorms",
        "visibility_km": 3.5,
        "wind_kmh": 28,
        "temp_c": 31,
        "impact": "Moderate departure delays possible",
    },
    "BOM": {
        "airport": "BOM",
        "condition": "Partly Cloudy",
        "visibility_km": 8.0,
        "wind_kmh": 14,
        "temp_c": 29,
        "impact": "Minimal impact expected",
    },
    "BLR": {
        "airport": "BLR",
        "condition": "Clear",
        "visibility_km": 10.0,
        "wind_kmh": 10,
        "temp_c": 26,
        "impact": "No impact expected",
    },
}

GATES: dict[str, list[dict]] = {
    "T2": [
        {"gate": "G01", "status": "Occupied", "flight": "AI450"},
        {"gate": "G02", "status": "Available", "flight": None},
        {"gate": "G03", "status": "Maintenance", "flight": None},
    ],
    "T3": [
        {"gate": "G08", "status": "Occupied", "flight": "AI101"},
        {"gate": "G12", "status": "Occupied", "flight": "AI203"},
        {"gate": "G15", "status": "Available", "flight": None},
        {"gate": "G16", "status": "Available", "flight": None},
    ],
}
