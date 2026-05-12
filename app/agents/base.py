from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Optional
from app.core.observability import logger, tracker

class BaseAgent(ABC):
    def __init__(self, llm, provider: str, model_name: str, tools: list = None):
        self.llm = llm
        self.provider = provider
        self.model_name = model_name
        self.tools = tools or []
        self._graph = None # Lazy loading
        logger.log_event("AGENT_INITIALIZED", {"model_name": model_name, "tools":  [t.name for t in self.tools]})

    @property
    def graph(self):
        """Getter cho graph, tự động build nếu chưa có."""
        if self._graph is None:
            self._graph = self.build_graph()
        return self._graph

    @abstractmethod
    def build_graph(self):
        """Mọi Agent con BẮT BUỘC phải tự vẽ sơ đồ graph của mình ở đây."""
        pass

    @abstractmethod
    async def stream(self, input_text: str, thread_id: str = None) -> AsyncGenerator:
        """Phương thức chính để giao tiếp với Agent."""
        pass