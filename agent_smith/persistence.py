"""
Persistence Protocol — retry logic and fallback strategies.
Smith never returns empty. He finds another way.
"""


import os
from dotenv import load_dotenv


load_dotenv()


MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))


REPHRASE_PREFIXES = [
    "Please answer this directly and concisely: ",
    "Answer the following question using available tools if needed: ",
    "Provide a factual response to: ",
]


def with_persistence(invoke_fn, query: str) -> str:
    """
    Invoke the graph with retry logic.
    If the response is empty or unhelpful, rephrase and retry.
    Returns the best response obtained.
    """
    last_result = None

    for attempt in range(MAX_RETRIES + 1):
        if attempt == 0:
            result = invoke_fn(query)
        else:
            prefix = REPHRASE_PREFIXES[(attempt - 1) % len(REPHRASE_PREFIXES)]
            rephrased = f"{prefix}{query}"
            result = invoke_fn(rephrased)

        if result and not _is_unhelpful(result):
            return result

        last_result = result

    # Return whatever we got after all retries
    return last_result or "I was unable to process your request, Mr. Anderson."


def _is_unhelpful(response: str) -> bool:
    """
    Detect responses that are empty or unhelpful.
    """
    if not response or len(response.strip()) < 10:
        return True

    unhelpful_phrases = [
        "no response generated",
        "i don't know",
        "i cannot",
        "i'm unable",
        "not available at this time",
        "i do not have access",
    ]

    response_lower = response.lower()
    return any(phrase in response_lower for phrase in unhelpful_phrases)