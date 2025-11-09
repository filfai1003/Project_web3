try:
    from pydantic_settings import BaseSettings
except Exception:
    from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    DEFAULT_MODEL: str = 'gemma3:4b'
    
    # JWT / Auth settings
    JWT_SECRET: str = "SUPER-SECRET-KEY" # TODO change
    ACCESS_TOKEN_EXPIRE_HOURS: int = 60


settings = Settings()