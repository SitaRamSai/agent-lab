DENY_LIST = {"delete_task_tool"}

def check_policy(tool_call: dict) -> bool:
    return tool_call["name"] not in DENY_LIST
