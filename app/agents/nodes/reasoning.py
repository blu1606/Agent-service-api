from app.agents.state import State

def make_reasoning_node(llm):
    """Factory: inject LLM -> return node function"""

    def call_model(state: State):

        response = llm.invoke(state["messages"])

        return {
            "messages": [response]
        }
    
    return call_model