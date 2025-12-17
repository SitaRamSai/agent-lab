def request_approval(tool_call: dict) -> bool:
    print(f"\nAPPROVAL REQUIRED for tool: {tool_call['name']}")
    print(f"Arguments: {tool_call['args']}")
    choice = input("Approve? (y/n): ").lower()
    return choice == "y"
