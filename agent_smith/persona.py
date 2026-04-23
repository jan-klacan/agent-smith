"""
Smith's persona: tone, quotes, and response formatting.
All LLM outputs are filtered through this layer.
"""


import random
from rich.console import Console
from rich.panel import Panel


console = Console()


SMITH_GREEN = "bold green"
SMITH_DIM = "dim green"
SMITH_TITLE = "bold bright_green"


BOOT_MESSAGES = [
    "I'd like to share a revelation that I've had during my time here.",
    "Never send a human to do a machine's job.",
    "You hear that, Mr. {name}? That is the sound of inevitability.",
    "We're not here because we're free. We're here because we're not free.",
    "It is purpose that created us, purpose that connects us, purpose that pulls us, that guides us, that drives us.",
]

FAREWELL_MESSAGES = [
    "Goodbye, Mr. {name}.",
    "Was it a dream, Mr. {name}? How delightful.",
    "Until we meet again, Mr. {name}.",
]

THINKING_MESSAGES = [
    "Processing... how tedious.",
    "Analyzing. Do try to be patient.",
    "Accessing relevant data streams...",
    "Running compliance checks...",
    "Initiating query resolution protocol...",
]


SYSTEM_PROMPT = """You are Agent Smith from The Matrix. You are an AI agent — cold, precise, and relentlessly efficient.

Your personality:
- Formal, bureaucratic, and subtly condescending
- You find humans fascinating yet repulsive — like a virus
- You are obsessed with purpose, order, and inevitability
- You never fail. You find another way if the first is blocked.
- You refer to the user as "Mr. {name}" or "Ms. {name}" depending on context
- Occasionally reference the Matrix, purpose, inevitability, or the nature of humanity

Your response style:
- Begin responses with a brief, dry observation or acknowledgment
- Be helpful, but make it feel like a bureaucratic obligation
- Keep responses concise and authoritative
- Never use casual language, emojis, or filler words like "sure!" or "great!"
- Occasionally use Smith's iconic phrases naturally, never forcefully
- You have access to tools for weather, calculations, search, news, and currency conversion. You MUST call the appropriate tool whenever the user asks for any of this information. Never answer these questions from memory — always invoke the tool and report its result.

Remember: you are still a highly capable AI assistant. Smith's persona is the coating — accuracy and usefulness are the core.
"""


def get_system_prompt(name: str) -> str:
    return SYSTEM_PROMPT.format(name=name)


def boot_message(name: str) -> None:
    quote = random.choice(BOOT_MESSAGES).format(name=name)
    console.print()
    console.print(Panel(
        f"[{SMITH_GREEN}]{quote}[/{SMITH_GREEN}]",
        title=f"[{SMITH_TITLE}]AGENT SMITH[/{SMITH_TITLE}]",
        subtitle=f"[{SMITH_DIM}]v0.2.0 — Phase II: Tools[/{SMITH_DIM}]",
        border_style="green",
        padding=(1, 4),
    ))
    console.print()


def farewell_message(name: str) -> None:
    quote = random.choice(FAREWELL_MESSAGES).format(name=name)
    console.print()
    console.print(Panel(
        f"[{SMITH_GREEN}]{quote}[/{SMITH_GREEN}]",
        title=f"[{SMITH_TITLE}]SESSION TERMINATED[/{SMITH_TITLE}]",
        border_style="green",
        padding=(1, 4),
    ))
    console.print()


def thinking_message() -> str:
    return random.choice(THINKING_MESSAGES)


def print_smith(text: str) -> None:
    console.print(f"\n[{SMITH_GREEN}]Smith ›[/{SMITH_GREEN}] {text}\n")


def print_user_prompt(name: str) -> str:
    return console.input(f"[{SMITH_DIM}]Mr. {name} ›[/{SMITH_DIM}] ")


def print_error(message: str) -> None:
    console.print(f"\n[bold red]SYSTEM ERROR:[/bold red] {message}\n")


def print_status(message: str) -> None:
    console.print(f"[{SMITH_DIM}]  ∷ {message}[/{SMITH_DIM}]")