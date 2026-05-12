from langchain_core.messages import ToolMessage
import json
from app.tools.search_tool import search_tool 
from app.agents.state import State

TOOL_MAP = {
    "search_tool": search_tool 
}

def call_tools(state: State): 
    last_message = state["messages"][-1]
    outputs = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]

        if tool_name in TOOL_MAP:
            content = TOOL_MAP[tool_name].invoke(args)
        else:
            content = f"Error: Tool '{tool_name}' not found. Available tools: {list{TOOL_MAP.keys()}}"

            outputs.append(
                ToolMessage(
                    content=content, 
                    name=tool_name,
                    tool_call_id=tool_call["id"]
                )
            )
        
    return {
        "messages": outputs 
    }