"""
LangGraph ReAct agent graph — the core of Agent Smith's intelligence.
Defines the state graph with tool-calling loop.
"""


from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from .tools import get_weather, calculate, search_web, get_news, convert_currency
from .persona import get_system_prompt


TOOLS = [get_weather, calculate, search_web, get_news, convert_currency]


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_graph(llm, name: str):
    """
    Build and compile the LangGraph ReAct agent graph.
    Returns a compiled graph ready for invocation.
    """
    llm_with_tools = llm.bind_tools(TOOLS)
    tool_node = ToolNode(TOOLS)
    system_prompt = get_system_prompt(name)

    def agent_node(state: AgentState) -> AgentState:
        messages = state["messages"]
        # Always ensure system prompt is first
        has_system = any(isinstance(m, SystemMessage) for m in messages)
        if not has_system:
            messages = [SystemMessage(content=system_prompt)] + list(messages)
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()