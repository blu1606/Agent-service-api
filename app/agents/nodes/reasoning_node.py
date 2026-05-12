from app.agents.state import State
from app.core.llm_factory import LLMFactory
from app.tools.search_tool import search_tool 

def call_model(state: State):
    model = LLMFactory.get_provider(
        provider="gemini",
        temperature=1.0,
        model="gemini-2.5-flash"
    )

    model.bind_tools([search_tool])

    response = model.invoke(state["messages"])

    return {
        "messages": [response]
    }