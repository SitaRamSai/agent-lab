from llm.local_model import get_llm
from tools.task_tools import create_task_tool, list_tasks_tool
from langchain_core.messages import AIMessage
from graph.state import AgentState

llm = get_llm()
tools = [create_task_tool, list_tasks_tool]
llm_with_tools = llm.bind_tools(tools)

def planner(state: AgentState) -> AgentState:
    response = llm_with_tools.invoke(state["messages"])

    new_queue = state.get("pending_tool_calls", [])

    if response.tool_calls:
        new_queue = new_queue + response.tool_calls

    return {
        "messages": state["messages"] + [response],
        "pending_tool_calls": new_queue,
        "tool_result": None
    }


def execute_tool(state: AgentState) -> AgentState:
    if not state["pending_tool_calls"]:
        return state

    call = state["pending_tool_calls"].pop(0)  # ← POP ONE

    if call["name"] == "create_task_tool":
        result = create_task_tool.invoke(call["args"])
    elif call["name"] == "list_tasks_tool":
        result = list_tasks_tool.invoke(call["args"])
    else:
        result = {"error": "Unknown tool"}

    return {
        "messages": state["messages"],
        "pending_tool_calls": state["pending_tool_calls"],
        "tool_result": result
    }


from langchain_core.messages import AIMessage

def observe(state: AgentState) -> AgentState:
    """
    Feed the tool result back to the LLM as context.
    """
    if state["tool_result"] is None:
        return state

    observation = AIMessage(
        content=f"Tool result: {state['tool_result']}"
    )

    return {
        "messages": state["messages"] + [observation],
        "tool_result": None
    }


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]

    # If the LLM did not request a tool, we are done
    if not last_message.tool_calls:
        return "end"

    return "continue"

from policy.policy import check_policy

def policy_check(state: AgentState) -> AgentState:
    if not state["pending_tool_calls"]:
        return state

    next_call = state["pending_tool_calls"][0]

    if not check_policy(next_call):
        raise Exception(f"Policy denied tool: {next_call['name']}")

    return state

from approval.approval import request_approval

def human_approval(state: AgentState) -> AgentState:
    if not state["pending_tool_calls"]:
        return state

    next_call = state["pending_tool_calls"][0]

    approved = request_approval(next_call)
    if not approved:
        raise Exception("Human rejected the action")

    return state
