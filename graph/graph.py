from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import planner, execute_tool, observe, should_continue, policy_check, human_approval

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("execute_tool", execute_tool)
    graph.add_node("observe", observe)
    graph.add_node("policy_check", policy_check)
    graph.add_node("human_approval", human_approval)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "policy_check")
    graph.add_edge("policy_check", "human_approval")
    graph.add_edge("human_approval", "execute_tool")
    graph.add_edge("execute_tool", "observe")

    graph.add_conditional_edges(
        "observe",
        should_continue,
        {
            "continue": "policy_check",
            "end": END
        }
    )

    return graph.compile()
