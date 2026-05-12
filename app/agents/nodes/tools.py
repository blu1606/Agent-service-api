from langchain_core.messages import ToolMessage
import json
from app.agents.state import State

def make_tool_node(tools: list):
    tools_map = {t.name: t for t in tools}

    def call_tools(state: State): 
        last_message = state["messages"][-1]
        outputs = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            args = tool_call["args"]

            if tool_name in tools_map:
                content = tools_map[tool_name].invoke(args)
            else:
                content = f"Error: Tool '{tool_name}' not found. Available tools: {list(tools_map.keys())}"

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
    
    return call_tools