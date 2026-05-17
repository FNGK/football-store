"""LangGraph orchestration with tenant-namespaced checkpoints."""

from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from amp_shared.guardrails import BudgetGuardrails


class MarketingState(TypedDict):
    tenant_id: str
    messages: Annotated[list, add_messages]
    brief: str
    safe_mode: bool
    guardrails: dict


def checkpoint_thread_id(tenant_id: str, thread_id: str) -> str:
    if thread_id.startswith(f"{tenant_id}:"):
        return thread_id
    return f"{tenant_id}:{thread_id}"


def intake_node(state: MarketingState) -> MarketingState:
    guard = BudgetGuardrails()
    guard.reserve_step()
    brief = (
        "Scoped strategy brief: validate business goals, market research, "
        "and performance targets for build agents."
    )
    return {**state, "brief": brief, "guardrails": {"mode": guard.mode.value}}


def safe_mode_gate(state: MarketingState) -> str:
    return "end" if state.get("safe_mode") else "build"


def build_graph() -> StateGraph:
    graph = StateGraph(MarketingState)
    graph.add_node("intake", intake_node)
    graph.add_conditional_edges("intake", safe_mode_gate, {"build": END, "end": END})
    graph.set_entry_point("intake")
    return graph


def compile_orchestrator():
    return build_graph().compile()
