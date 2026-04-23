"""
Mock API server — FastAPI application.
Provides 5 tool endpoints. Zero external API calls.
Run with: uvicorn mock_server.server:app --port 8000
"""

import ast
import operator
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .data import WEATHER_DATA, NEWS_DATA, SEARCH_DATA, CURRENCY_RATES

app = FastAPI(
    title="Agent Smith — Mock Tool Server",
    description="Simulated tool backends. No external APIs. No cost.",
    version="0.2.0",
)

# ── Safe calculator ───────────────────────────────────────────────

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def safe_eval(expr: str) -> float:
    """Safely evaluate a mathematical expression without using eval()."""
    try:
        tree = ast.parse(expr.strip(), mode="eval")
    except SyntaxError:
        raise ValueError(f"Invalid expression: {expr}")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](_eval(node.operand))
        else:
            raise ValueError(f"Unsupported operation in expression: {expr}")

    return _eval(tree)


# ── Endpoints ─────────────────────────────────────────────────────

@app.get("/weather/{city}")
def get_weather(city: str):
    key = city.lower().strip()
    data = WEATHER_DATA.get(key)
    if not data:
        available = list(WEATHER_DATA.keys())
        raise HTTPException(
            status_code=404,
            detail=f"No weather data for '{city}'. Available cities: {available}"
        )
    return JSONResponse(content=data)


@app.get("/calculate")
def calculate(expr: str):
    try:
        result = safe_eval(expr)
        return JSONResponse(content={"expression": expr, "result": result})
    except (ValueError, ZeroDivisionError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/search")
def search_web(q: str):
    key = q.lower().strip()
    results = SEARCH_DATA.get(key, SEARCH_DATA["default"])
    return JSONResponse(content={"query": q, "results": results})


@app.get("/news")
def get_news(topic: str = "default"):
    key = topic.lower().strip()
    headlines = NEWS_DATA.get(key, NEWS_DATA["default"])
    return JSONResponse(content={"topic": topic, "headlines": headlines})


@app.get("/currency")
def convert_currency(amount: float, from_currency: str, to_currency: str):
    src = from_currency.upper().strip()
    dst = to_currency.upper().strip()

    if src not in CURRENCY_RATES:
        raise HTTPException(status_code=400, detail=f"Unknown currency: {src}")
    if dst not in CURRENCY_RATES:
        raise HTTPException(status_code=400, detail=f"Unknown currency: {dst}")

    in_usd = amount / CURRENCY_RATES[src]
    converted = in_usd * CURRENCY_RATES[dst]

    return JSONResponse(content={
        "amount": amount,
        "from": src,
        "to": dst,
        "result": round(converted, 2),
        "rate": round(CURRENCY_RATES[dst] / CURRENCY_RATES[src], 6),
    })


@app.get("/health")
def health():
    return {"status": "online", "server": "Agent Smith Mock Tool Server"}