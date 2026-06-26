from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    analyzer_provider: Literal["heuristic", "openai"] = "heuristic"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.4-mini"


@lru_cache
def get_settings() -> Settings:
    return Settings()

