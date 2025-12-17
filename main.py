# from llm.local_model import get_llm
# from tools.task_tools import create_task_tool, list_tasks_tool
# from langchain_core.messages import HumanMessage

# def main():
#     llm = get_llm()
#     tools = [create_task_tool, list_tasks_tool]

#     llm_with_tools = llm.bind_tools(tools)

#     user_input = "List all tasks"

#     response = llm_with_tools.invoke(
#         [HumanMessage(content=user_input)]
#     )

#     print("\nRAW LLM RESPONSE:\n")
#     print(response)

#     if response.tool_calls:
#         print("\nTOOL CALLS DETECTED:\n")
#         for call in response.tool_calls:
#             print(call)

#             if call["name"] == "create_task_tool":
#                 result = create_task_tool.invoke(call["args"])
#                 print("\nTOOL RESULT:\n", result)

# if __name__ == "__main__":
#     main()



from langchain_core.messages import HumanMessage
from graph.graph import build_graph

def main():
    graph = build_graph()

    initial_state = {
        "messages": [
            HumanMessage(
                content="Create two tasks called Buy milk and Buy bread and then list all tasks"
            )
        ],
        "tool_result": None
    }

    result = graph.invoke(initial_state)

    print("\nFINAL STATE:\n")
    print(result)

if __name__ == "__main__":
    main()
