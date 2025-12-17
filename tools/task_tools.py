from langchain_core.tools import tool
from tools.task_store import create_task, list_tasks

@tool
def create_task_tool(title: str) -> dict:
    """Create a new task with the given title."""
    return create_task(title)

@tool
def list_tasks_tool() -> list:
    """List all existing tasks."""
    return list_tasks()

