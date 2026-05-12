from langchain_core.messages import SystemMessage
from app.agents.state import State
from app.agents.prompts.reasoning_prompt import SYSTEM_PROMPT

def make_reasoning_node(llm):
    """Factory: inject LLM -> return node function"""
    
    def call_model(state: State):
        # Kết hợp System Prompt với lịch sử hội thoại
        messages = [SYSTEM_PROMPT] + state["messages"]
        response = llm.invoke(messages)

        return {
            "messages": [response]
        }
    
    return call_model