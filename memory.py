# Roll number: evernorth-aai-817080
"""Disk-backed fact store for SkyVault. Survives a process restart."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MEMORY_FILE = Path(__file__).parent / "skyvault_memory.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _norm_key(key: str) -> str:
    return " ".join(key.strip().lower().split())


def _load() -> dict[str, Any]:
    if not MEMORY_FILE.exists():
        return {"facts": {}}
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {"facts": {}}
    if not isinstance(data, dict) or "facts" not in data:
        return {"facts": {}}
    return data


def _save(store: dict[str, Any]) -> None:
    with MEMORY_FILE.open("w", encoding="utf-8") as fh:
        json.dump(store, fh, indent=2)


def remember(key: str, value: str, source: str) -> dict[str, Any]:
    """
    Persist a fact. Same key with a different value overwrites the old one
    (last-write-wins). The previous value is kept only as an audit field,
    never as a second live fact.
    """
    key = (key or "").strip()
    value = "" if value is None else str(value).strip()
    source = (source or "unknown").strip() or "unknown"
    if not key:
        return {"status": "error", "message": "Memory key is required"}
    if not value:
        return {"status": "error", "message": "Memory value is required"}

    nk = _norm_key(key)
    store = _load()
    facts = store.setdefault("facts", {})
    existing = facts.get(nk)

    conflict = False
    previous = None
    if existing is not None:
        old_val = str(existing.get("value", ""))
        if old_val != value:
            conflict = True
            previous = old_val

    record: dict[str, Any] = {
        "key": nk,
        "value": value,
        "source": source,
        "updated_at": _now(),
    }
    if previous is not None:
        record["previous_value"] = previous

    facts[nk] = record
    _save(store)

    out: dict[str, Any] = {
        "status": "ok",
        "key": nk,
        "value": value,
        "source": source,
        "conflict": conflict,
        "action": "overwritten" if conflict else ("updated" if existing else "stored"),
    }
    if previous is not None:
        out["previous_value"] = previous
    return out


def recall(query: str) -> dict[str, Any]:
    """Look up facts whose key or value contains the query string."""
    q = (query or "").strip().lower()
    if not q:
        return {"status": "error", "message": "Recall query is required"}

    facts = _load().get("facts", {})
    hits = []
    for rec in facts.values():
        key = str(rec.get("key", ""))
        val = str(rec.get("value", ""))
        if q in key.lower() or q in val.lower():
            hits.append(
                {
                    "key": key,
                    "value": val,
                    "source": rec.get("source"),
                    "updated_at": rec.get("updated_at"),
                }
            )

    if not hits:
        return {"status": "ok", "matches": [], "count": 0, "message": f"Nothing in memory for '{query}'"}
    return {"status": "ok", "matches": hits, "count": len(hits)}


def working_context() -> str:
    """Short dump of every stored fact for the system prompt (MemGPT-style)."""
    facts = _load().get("facts", {})
    if not facts:
        return ""
    lines = []
    for rec in facts.values():
        line = f"- {rec.get('key')}: {rec.get('value')} (source: {rec.get('source', 'unknown')})"
        if rec.get("previous_value"):
            line += f" [replaced {rec['previous_value']}]"
        lines.append(line)
    return "Known facts from earlier sessions:\n" + "\n".join(lines)
