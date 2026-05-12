from app.agents.base import BaseAgent
from app.agents.graphs import build_react_graph
from langchain_core.messages import HumanMessage
from app.core.observability import logger, tracker
import time

class ReActAgent(BaseAgent):
    def build_graph(self):
        return build_react_graph(self.llm, self.tools)
    
    async def stream(self, input_text: str, thread_id: str = None):
        start_time = time.time() 
        inputs = {"messages": [HumanMessage(content=input_text)]}

        logger.log_event("AGENT_START", {"input": input_text, "thread_id": thread_id})
        final_message = None

        config = {
            "configurable": {
                "thread_id": thread_id
            } if thread_id else {}
        }

        async for chunk in self.graph.astream(inputs, config=config, stream_mode="updates"):
            if "reasoning" in chunk: 
                final_message = chunk["reasoning"]["messages"][-1]
            yield chunk 
        
        latency_ms = int((time.time() - start_time) * 1000)
        if final_message and hasattr(final_message, 'usage_metadata'):
            usage = final_message.usage_metadata
            tracker.track_request(
                provider=self.provider,
                model=self.model_name, 
                usage=usage,
                latency_ms=latency_ms
            )
        
        logger.log_event("AGENT_END", {"latency": latency_ms})