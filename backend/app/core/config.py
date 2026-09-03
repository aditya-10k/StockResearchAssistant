from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "StockResearchAssistant"
    APP_VER: str = "1.0.0"
    DEBUG: bool = False
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "qwen/qwen3.8-27b"
    LLM_PROVIDER: Literal["gemini", "groq"] = "gemini"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/stock_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
