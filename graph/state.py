from typing import List, Optional, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    pending_tool_calls: List[dict]
    tool_result: Optional[object]
