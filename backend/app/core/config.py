from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings centralized here. Can be overridden by env vars."""

    DEFAULT_MODEL: str = "Llama-2-3B"
    TIMEOUT_SECONDS: int = 30

    # TODO Replace with proper CORS settings
    CORS_ORIGINS: List[str] = ["*"]

    PORT: int = 8000


settings = Settings()