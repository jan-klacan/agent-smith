"""
CLI entrypoint — the interactive Smith terminal.
Phase V: Session Memory + Full Demo Ready.
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
)
from . import __phase__
from .llm import load_llm, get_llm_description
from .graph import build_graph
from .replication import should_replicate, replicate_and_execute, MAX_CLONES
from .persistence import with_persistence, MAX_RETRIES
from .purpose_meter import PurposeMeter
from .memory import (
    load_memory,
    save_memory,
    add_memory_entry,
    format_memory_for_prompt,
    memory_summary,
)

load_dotenv()
console = Console()

EXIT_COMMANDS = {"exit", "quit", "q", "bye", "goodbye"}


def run():
    name = os.getenv("USER_NAME", "Anderson").strip()
    meter = PurposeMeter()

    # Load persisted memory
    memory_entries = load_memory()

    boot_message(name)
    print_status(f"LLM backend      : {get_llm_description()}")
    print_status(f"Identity         : Mr. {name}")
    print_status(f"Phase            : {__phase__}")
    print_status(f"Max clones       : {MAX_CLONES}")
    print_status(f"Max retries      : {MAX_RETRIES}")
    print_status(f"Memory           : {memory_summary(memory_entries)}")
    print_status("Type 'exit' to terminate the session.")
    console.print()

    try:
        llm = load_llm()
        graph = build_graph(llm, name)
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

    def invoke_graph(query: str) -> str:
        # Prepend memory context as a system message if available
        memory_context = format_memory_for_prompt(memory_entries)
        messages = []
        if memory_context:
            messages.append(SystemMessage(content=memory_context))
        messages.append(HumanMessage(content=query))

        result = graph.invoke({"messages": messages})
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
                return msg.content
        return "No response generated."

    while True:
        try:
            user_input = print_user_prompt(name).strip()
        except (KeyboardInterrupt, EOFError):
            save_memory(memory_entries)
            farewell_message(name)
            break

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            save_memory(memory_entries)
            farewell_message(name)
            break

        print_status(thinking_message())

        try:
            if should_replicate(user_input):
                print_status("Complex query detected — activating Replication Protocol...")
                clone_results = replicate_and_execute(user_input, invoke_graph)

                for clone in clone_results:
                    print_status(f"Clone {clone['clone_id']} assigned : \"{clone['sub_query']}\"")

                merged = "\n\n".join(
                    f"[Clone {c['clone_id']} — \"{c['sub_query']}\"]\n{c['result']}"
                    for c in clone_results
                )
                synthesis_prompt = (
                    f"You have just dispatched {len(clone_results)} clone agents to handle "
                    f"a complex query from Mr. {name}. Their findings are below. "
                    f"Synthesise them into a single authoritative response, "
                    f"maintaining your persona as Agent Smith.\n\n{merged}"
                )
                reply = with_persistence(invoke_graph, synthesis_prompt)
            else:
                reply = with_persistence(invoke_graph, user_input)

        except Exception as e:
            print_error(f"The Matrix has rejected your query. {e}")
            continue

        # Save this exchange to memory
        memory_entries = add_memory_entry(memory_entries, user_input, reply)

        meter.increment()
        meter.display()
        print_smith(reply)