try:
    from pydantic_settings import BaseSettings
except Exception:
    from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings centralized here. Can be overridden by env vars."""

    DEFAULT_MODEL: str = 'gemma3:4b'
    USE_GPU: bool = True

    PORT: int = 8000

    # JWT / Auth settings
    JWT_SECRET: str = "SUPER-SECRET-KEY" # TODO change
    ACCESS_TOKEN_EXPIRE_HOURS: int = 60


settings = Settings()