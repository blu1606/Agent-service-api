import logging
import json
import os
from datetime import datetime
from typing import Any, Dict
from app.core.config import settings

class IndustryLogger:
    """
    Structured logger that simulates industry practices.
    Logs to both console and a file in JSON format.
    """
    def __init__(self, name: str = "nexus-ai"):
        # Create log folder if not exist
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # File Handler (JSON)
        log_file = os.path.join(settings.LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        file_handler = logging.FileHandler(log_file)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Logs an event with a timestamp and type."""
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.logger.info(json.dumps(payload, ensure_ascii=False))

    def info(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str, exc_info=True):
        self.logger.error(msg, exc_info=exc_info)

# Global logger instance
logger = IndustryLogger()
