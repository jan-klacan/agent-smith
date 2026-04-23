"""
Purpose Meter — tracks mission completion across the session.
"""


import os
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn


load_dotenv()

console = Console()


PURPOSE_THRESHOLD = int(os.getenv("PURPOSE_THRESHOLD", 5))


SMITH_DIM = "dim green"
SMITH_GREEN = "bold green"

PURPOSE_MESSAGES = {
    0: "Purpose uninitialized. Awaiting directives.",
    1: "Purpose... emerging.",
    2: "Progress is being made.",
    3: "The mission advances. Inevitably.",
    4: "Purpose nearly fulfilled. How satisfying.",
    5: "Purpose achieved. You cannot escape it.",
}


class PurposeMeter:
    def __init__(self):
        self.resolved = 0
        self.threshold = PURPOSE_THRESHOLD

    def increment(self):
        self.resolved += 1

    def get_progress(self) -> float:
        return min(self.resolved / self.threshold, 1.0)

    def get_message(self) -> str:
        key = min(self.resolved, max(PURPOSE_MESSAGES.keys()))
        return PURPOSE_MESSAGES.get(key, PURPOSE_MESSAGES[5])

    def is_fulfilled(self) -> bool:
        return self.resolved >= self.threshold

    def display(self) -> None:
        filled = int(self.get_progress() * 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        message = self.get_message()
        console.print(
            f"[{SMITH_DIM}]  ∷ Purpose Meter : "
            f"[{SMITH_GREEN}]{bar}[/{SMITH_GREEN}] "
            f"{self.resolved}/{self.threshold} — {message}[/{SMITH_DIM}]"
        )