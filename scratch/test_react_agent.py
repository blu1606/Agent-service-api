import asyncio
from langchain_core.messages import AIMessage # ← Thêm dòng này
from app.core.llm_factory import LLMFactory
from app.tools.search_tool import search_tool
from app.agents.graphs import build_react_graph
from app.utils.graph_visualizer import save_graph_as_png
from app.agents.react_agent import ReActAgent

async def main():
    # init LLM and tool
    provider = "groq"
    model_name = "llama-3.3-70b-versatile"

    llm = LLMFactory.get_provider(
        provider=provider, 
        model=model_name, 
        temperature=0.0
    ).bind_tools([search_tool])

    agent = ReActAgent(llm=llm, provider=provider, model_name=model_name, tools=[search_tool])
    print("--- 🤖 Agent đang suy nghĩ... ---")
    async for chunk in agent.stream("Faker là ai?", thread_id="session_1"):
        # Ở đây em chỉ việc in chunk ra theo ý muốn
        print(chunk)


    
if __name__ == "__main__":
    asyncio.run(main())