from langgraph.graph import StateGraph, START, END
from app.agents.state import State
from app.agents.nodes import make_reasoning_node, make_tool_node


def should_continue(state: State):
    last_message = state["messages"][-1]

    if not last_message.tool_calls:
        return END
    return "tools"

def build_react_graph(llm, tools:list): 
    reasoning_node = make_reasoning_node(llm)
    tool_node = make_tool_node(tools)
        
    workflow = StateGraph(State)

    workflow.add_node("reasoning", reasoning_node)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "reasoning")
    workflow.add_conditional_edges("reasoning", should_continue, {"tools": "tools", END:END })
    workflow.add_edge("tools", "reasoning")

    return workflow.compile()
