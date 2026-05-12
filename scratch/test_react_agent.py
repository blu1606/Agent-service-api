import asyncio
from langchain_core.messages import AIMessage # ← Thêm dòng này
from app.core.llm_factory import LLMFactory
from app.tools.search_tool import search_tool
from app.agents.graphs import build_react_graph
from app.utils.graph_visualizer import save_graph_as_png

async def main():
    # init LLM and tool
    llm = LLMFactory.get_provider(
        provider="groq", # ← Đổi sang Groq
        model="llama-3.3-70b-versatile", # ← Model mạnh của Groq
        temperature=0.0
    ).bind_tools([search_tool])

    # compile agent graph
    app = build_react_graph(llm, [search_tool])
    
    save_graph_as_png(app)

    inputs = {"messages": [("user", "Hãy dùng search_tool để tìm xem Faker là ai?")]}
    print("--- 🤖 Agent đang suy nghĩ... ---")
    async for chunk in app.astream(inputs, stream_mode="values"):
        last_msg = chunk["messages"][-1]
        last_msg.pretty_print()

    for message in chunk['messages']:
        if isinstance(message, AIMessage):
            if message.content:
                print(f"🤖 Suy nghĩ: {message.content}") # ← In phần suy nghĩ
            if message.tool_calls:
                print(f"🛠️ Gọi tool: {message.tool_calls[0]['name']}")

    
if __name__ == "__main__":
    asyncio.run(main())