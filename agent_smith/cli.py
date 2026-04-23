"""
CLI entrypoint — the interactive Smith terminal.
Phase II: tools are now bound to the LLM.
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
from .tools import get_weather, calculate, search_web, get_news, convert_currency


load_dotenv()
console = Console()


EXIT_COMMANDS = {"exit", "quit", "q", "bye", "goodbye"}

TOOLS = [get_weather, calculate, search_web, get_news, convert_currency]


def run():
    name = os.getenv("USER_NAME", "Anderson").strip()

    boot_message(name)
    print_status(f"LLM backend  : {get_llm_description()}")
    print_status(f"Identity     : Mr. {name}")
    print_status(f"Phase        : II — Tools")
    print_status(f"Tools loaded : {', '.join(t.name for t in TOOLS)}")
    print_status("Type 'exit' to terminate the session.")
    console.print()

    # Load LLM and bind tools
    try:
        llm = load_llm()
        llm_with_tools = llm.bind_tools(TOOLS)
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
            response = llm_with_tools.invoke(history)

            # Handle tool calls if the LLM requested any
            if response.tool_calls:
                for tc in response.tool_calls:
                    print_status(f"Invoking tool  : {tc['name']}({tc['args']})")

                history.append(response)

                # Execute each tool and add results to history
                from langchain_core.messages import ToolMessage
                for tc in response.tool_calls:
                    tool_map = {t.name: t for t in TOOLS}
                    tool_fn = tool_map.get(tc["name"])
                    if tool_fn:
                        tool_result = tool_fn.invoke(tc["args"])
                        history.append(ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tc["id"],
                        ))

                # Ask LLM to summarise tool results in Smith's voice
                print_status(thinking_message())
                final_response = llm_with_tools.invoke(history)
                reply = final_response.content
                history.append(final_response)
            else:
                reply = response.content
                history.append(response)

        except Exception as e:
            print_error(f"The Matrix has rejected your query. {e}")
            history.pop()
            continue

        print_smith(reply)