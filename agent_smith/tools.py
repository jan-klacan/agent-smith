"""
LangChain tool definitions.
Each tool calls the local mock server at localhost:8000.
"""

from .anomaly import detect_anomaly
import httpx
from langchain_core.tools import tool

BASE_URL = "http://localhost:8000"


def _get(endpoint: str, params: dict = None) -> dict:
    """Make a GET request to the mock server."""
    try:
        response = httpx.get(f"{BASE_URL}{endpoint}", params=params, timeout=5.0)
        response.raise_for_status()
        return response.json()
    except httpx.ConnectError:
        return {"error": "Mock server is offline. Start it with: uvicorn mock_server.server:app --port 8000"}
    except httpx.HTTPStatusError as e:
        return {"error": e.response.json().get("detail", str(e))}
    

@tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city. Available cities: Amsterdam, London, New York, Tokyo, Paris, Sydney, Berlin, Dubai."""
    return _get(f"/weather/{city}")

@tool
def calculate(expression: str) -> dict:
    """Evaluate a mathematical expression. Supports +, -, *, /, **, %. Example: '(10 + 5) * 2'"""
    return _get("/calculate", params={"expr": expression})

@tool
def search_web(query: str) -> dict:
    """Search the web for a topic. Available topics: python, ai, matrix."""
    return _get("/search", params={"q": query})

@tool
def get_news(topic: str = "default") -> dict:
    """Get recent news headlines for a topic. Available topics: technology, science, world."""
    return _get("/news", params={"topic": topic})

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert an amount between currencies. Supported: USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, SEK, NOK."""
    return _get("/currency", params={
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
    })


TOOLS = [get_weather, calculate, search_web, get_news, convert_currency, detect_anomaly]