import time
from typing import Dict, Any, List
from app.core.observability.logger import logger

class PerformanceTracker:
    """
    Tracking industry-standard metrics for LLMs.
    """
    def __init__(self):
        self.session_metrics = []

    def track_request(self, provider: str, model: str, usage: Dict[str, int], latency_ms: int):
        """
        Logs a single request metric to our telemetry.
        """
        metric = {
            "provider": provider,
            "model": model,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "latency_ms": latency_ms,
            "cost_estimate": self._calculate_cost(model, usage) # Mock cost calculation
        }
        self.session_metrics.append(metric)
        logger.log_event("LLM_METRIC", metric)

    def _calculate_cost(self, model: str, usage: Dict[str, int]) -> float:
        """
        Calculates estimated cost based on model-specific pricing (USD per 1M tokens).
        """
        pricing = {
            "gemini-3-flash-preview": {"input": 0.10, "output": 0.40},
            "gemini-2.5-flash":       {"input": 0.075, "output": 0.30},
            "gemini-1.5-pro":         {"input": 1.25, "output": 5.00},
            "gpt-4o":                 {"input": 2.50, "output": 10.00},
            "gpt-4o-mini":            {"input": 0.15, "output": 0.60},
        }

        model_price = pricing.get(model, {"input": 0.01, "output": 0.01}) #fallback

        prompt_cost = (usage.get("prompt_tokens", 0) / 1_000_000) * model_price["input"]
        completion_cost = (usage.get("completion_tokens", 0) / 1_000_000) * model_price["output"]

        return round(prompt_cost + completion_cost, 8)

# Global tracker instance
tracker = PerformanceTracker()
