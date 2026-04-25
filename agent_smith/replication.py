"""
Replication Protocol — clone detection and parallel execution.
Smith spawns clone agents for complex multi-part queries.
Maximum clones is capped by MAX_CLONES (default: 3, minimum: 1).
"""

import os
import re
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv


load_dotenv()


def _normalise_max_clones(value) -> int:
    """Return a safe clone count with a minimum of 1."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 1
    return max(1, parsed)


MAX_CLONES = _normalise_max_clones(os.getenv("MAX_CLONES", 3))


SPLIT_PATTERN = re.compile(
    r"\s*(?:,\s*and\b|\band\b|\balso\b|\bas\s+well\s+as\b|\bplus\b|\badditionally\b|\bboth\b)\s*",
    re.IGNORECASE,
)

# Tool keywords used to count how many distinct tool needs exist
TOOL_KEYWORDS = {
    "get_weather": ["weather", "temperature", "forecast", "humidity", "climate"],
    "calculate": ["calculate", "compute", "multiply", "divide", "add", "subtract", "plus", "minus", "squared"],
    "search_web": ["search", "find", "look up", "information about", "tell me about"],
    "get_news": ["news", "headlines", "latest", "recent", "current events"],
}


def detect_required_tools(query: str) -> list[str]:
    """
    Detect which tools a query likely needs based on keywords.
    Returns a list of tool names.
    """
    query_lower = query.lower()
    required = []
    for tool_name, keywords in TOOL_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            required.append(tool_name)
    return required


def should_replicate(query: str) -> bool:
    """
    Determine if a query is complex enough to warrant cloning.
    Returns True if 2+ distinct tools are needed.
    """
    required_tools = detect_required_tools(query)
    return len(required_tools) >= 2


def decompose_query(query: str) -> list[str]:
    """
    Decompose a multi-part query into sub-queries.
    Each sub-query targets a single tool need.
    Capped at MAX_CLONES.
    """
    max_clones = _normalise_max_clones(MAX_CLONES)

    # Split case-insensitively across common conjunctions.
    parts = [p.strip() for p in SPLIT_PATTERN.split(query) if p.strip()]
    sub_queries = parts if parts else [query]

    # Cap at MAX_CLONES
    if len(sub_queries) > max_clones:
        sub_queries = sub_queries[:max_clones]

    return sub_queries


def run_clone(clone_id: int, sub_query: str, graph_fn) -> dict:
    """
    Execute a single clone agent on a sub-query.
    Retries once on empty result.
    """
    result = graph_fn(sub_query)

    # Retry once if result looks empty
    if not result or result == "No response generated.":
        result = graph_fn(sub_query)

    return {
        "clone_id": clone_id,
        "sub_query": sub_query,
        "result": result,
    }


def replicate_and_execute(query: str, graph_fn) -> list[dict]:
    """
    Spawn clone agents in parallel and collect their results.
    Each clone runs graph_fn on its assigned sub-query.
    """
    max_clones = _normalise_max_clones(MAX_CLONES)
    sub_queries = decompose_query(query)
    clone_count = min(len(sub_queries), max_clones)
    sub_queries = sub_queries[:clone_count]

    results = []
    with ThreadPoolExecutor(max_workers=clone_count) as executor:
        futures = [
            executor.submit(run_clone, i + 1, sq, graph_fn)
            for i, sq in enumerate(sub_queries)
        ]
        for future in futures:
            results.append(future.result())

    return results