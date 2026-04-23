"""
CLI entrypoint — the interactive Smith terminal.
Phase III: LangGraph ReAct graph + Replication Protocol.
"""

import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from langchain_core.messages import HumanMessage, SystemMessage

import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from langchain_core.messages import HumanMessage

from .persona import (
    boot_message,
    farewell_message,
    thinking_message,
    print_smith,
    print_user_prompt,
    print_error,
    print_status,
)
from .llm import load_llm, get_llm_description
from .graph import build_graph
from .replication import should_replicate, replicate_and_execute, MAX_CLONES


load_dotenv()
console = Console()


EXIT_COMMANDS = {"exit", "quit", "q", "bye", "goodbye"}


def run():
    name = os.getenv("USER_NAME", "Anderson").strip()

    boot_message(name)
    print_status(f"LLM backend      : {get_llm_description()}")
    print_status(f"Identity         : Mr. {name}")
    print_status(f"Phase            : III — Replication Protocol")
    print_status(f"Max clones       : {MAX_CLONES}")
    print_status("Type 'exit' to terminate the session.")
    console.print()

    # Load LLM and bind tools
    try:
        llm = load_llm()
        graph = build_graph(llm, name)
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

    def invoke_graph(query: str) -> str:
        """Invoke the graph on a single query and return the final text response."""
        result = graph.invoke({"messages": [HumanMessage(content=query)]})
        messages = result["messages"]
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content and not getattr(msg, "tool_calls", None):
                return msg.content
        return "No response generated."
    
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

        print_status(thinking_message())

        try:
            if should_replicate(user_input):
                print_status(f"Complex query detected — activating Replication Protocol...")

                clone_results = replicate_and_execute(user_input, invoke_graph)

                for clone in clone_results:
                    print_status(f"Clone {clone['clone_id']} assigned : \"{clone['sub_query']}\"")

                # Merge all clone results into one synthesis prompt
                merged = "\n\n".join(
                    f"[Clone {c['clone_id']} — \"{c['sub_query']}\"]\n{c['result']}"
                    for c in clone_results
                )
                synthesis_prompt = (
                    f"You have just dispatched {len(clone_results)} clone agents to handle "
                    f"a complex query. Their findings are below. Synthesise them into a single "
                    f"authoritative response in your voice, Mr. {name}.\n\n{merged}"
                )
                reply = invoke_graph(synthesis_prompt)
            else:
                reply = invoke_graph(user_input)

        except Exception as e:
            print_error(f"The Matrix has rejected your query. {e}")
            continue

        print_smith(reply)