"""
CLI entrypoint — the interactive Smith terminal.
"""


import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from langchain_core.messages import HumanMessage, SystemMessage

from .persona import (
    boot_message,
    farewell_message,
    thinking_message,
    print_smith,
    print_user_prompt,
    print_error,
    print_status,
    get_system_prompt,
)
from .llm import load_llm, get_llm_description


load_dotenv()
console = Console()

EXIT_COMMANDS = {"exit", "quit", "q", "bye", "goodbye"}


def run():
    name = os.getenv("USER_NAME", "Anderson").strip()

    boot_message(name)
    print_status(f"LLM backend  : {get_llm_description()}")
    print_status(f"Identity     : Mr. {name}")
    print_status(f"Phase        : I — The Matrix")
    print_status("Type 'exit' to terminate the session.")
    console.print()

    try:
        llm = load_llm()
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

    system_prompt = get_system_prompt(name)
    history = [SystemMessage(content=system_prompt)]

    while True:
        try:
            user_input = print_user_prompt(name).strip()
        except (KeyboardInterrupt, EOFError):
            farewell_message(name)
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            farewell_message(name)
            break

        history.append(HumanMessage(content=user_input))
        print_status(thinking_message())

        try:
            response = llm.invoke(history)
            reply = response.content
        except Exception as e:
            print_error(f"The Matrix has rejected your query. {e}")
            history.pop()
            continue

        history.append(response)
        print_smith(reply)