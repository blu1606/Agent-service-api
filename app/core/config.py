from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from pathlib import Path

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LLMProvider(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    GROQ = "groq" # ← Thêm Groq

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nexus AI"
    APP_END: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False

    DEFAULT_PROVIDER: LLMProvider = LLMProvider.GOOGLE
    DEFAULT_MODEL:str = "gemini-2.5-flash"
    TEMPERATURE:float = 1.0

    LOG_DIR: Path = Path("logs")
    LOG_LEVEL: str = "INFO"

    GOOGLE_API_KEY: str
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = "" # ← Thêm Groq API Key

    ALLOWED_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

settings = Settings()
