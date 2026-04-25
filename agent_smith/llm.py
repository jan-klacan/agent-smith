"""
LLM loader — Ollama first, Gemini when OLLAMA_MODEL is not set.
"""


import os
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel


load_dotenv()


def load_llm() -> BaseChatModel:
    """Select backend by config priority: OLLAMA_MODEL, then GEMINI_API_KEY."""
    ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

    if ollama_model:
        return _load_ollama(ollama_model)
    if gemini_key:
        return _load_gemini(gemini_key)
    return _load_ollama("qwen2.5")


def _load_ollama(model: str) -> BaseChatModel:
    try:
        from langchain_ollama import ChatOllama
        return ChatOllama(model=model, temperature=0.3)
    except ImportError:
        raise RuntimeError(
            "langchain-ollama is not installed. Run: pip install langchain-ollama"
        )


def _load_gemini(api_key: str) -> BaseChatModel:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            google_api_key=api_key,
            temperature=0.3,
        )
    except ImportError:
        raise RuntimeError(
            "langchain-google-genai is not installed. Run: pip install langchain-google-genai"
        )


def get_llm_description() -> str:
    ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

    if ollama_model:
        return f"Ollama ({ollama_model}) — local, zero cost"
    if gemini_key:
        return "Gemini 2.0 Flash Lite — selected when OLLAMA_MODEL is empty"
    return "Ollama (qwen2.5) — local, zero cost [default]"