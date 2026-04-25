"""
Session Memory.
Persists conversation summaries across sessions.
"""


import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


MEMORY_DIR = Path(os.getenv("MEMORY_DIR", "memory"))
MAX_MEMORY_ENTRIES = int(os.getenv("MAX_MEMORY_ENTRIES", 20))


def _ensure_memory_dir() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _memory_file() -> Path:
    return MEMORY_DIR / "smith_memory.json"


def load_memory() -> list[dict]:
    """
    Load persisted memory entries from disk.
    Returns a list of past conversation entries.
    """
    _ensure_memory_dir()
    path = _memory_file()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_memory(entries: list[dict]) -> None:
    """
    Persist memory entries to disk, trimmed to MAX_MEMORY_ENTRIES.
    """
    _ensure_memory_dir()
    trimmed = entries[-MAX_MEMORY_ENTRIES:]
    with open(_memory_file(), "w", encoding="utf-8") as f:
        json.dump(trimmed, f, indent=2, ensure_ascii=False)


def add_memory_entry(entries: list[dict], user: str, assistant: str) -> list[dict]:
    """
    Append a new exchange to the memory list and return the updated list.
    """
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user": user,
        "assistant": assistant[:300],  # cap length
    }
    return entries + [entry]


def format_memory_for_prompt(entries: list[dict]) -> str:
    """
    Format the last 5 memory entries as context for the LLM prompt.
    Returns an empty string if there are no entries.
    """
    if not entries:
        return ""
    recent = entries[-5:]
    lines = ["[Previous session context — Smith remembers:]"]
    for e in recent:
        lines.append(f"  User    : {e['user']}")
        lines.append(f"  Smith   : {e['assistant']}")
        lines.append("")
    return "\n".join(lines)


def memory_summary(entries: list[dict]) -> str:
    """
    Return a one-line summary of the memory state for the boot message.
    """
    if not entries:
        return "No prior sessions detected."
    last = entries[-1]
    ts = last.get("timestamp", "unknown time")
    return f"{len(entries)} exchange(s) on record. Last contact: {ts}."