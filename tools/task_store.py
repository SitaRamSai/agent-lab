# Simple in-memory task store (local-only)
TASKS = {}
NEXT_ID = 1

def create_task(title: str) -> dict:
    global NEXT_ID
    task_id = NEXT_ID
    TASKS[task_id] = {"id": task_id, "title": title}
    NEXT_ID += 1
    return TASKS[task_id]

def list_tasks() -> list:
    return list(TASKS.values())
