from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = Field(default="development")
    openai_api_key: str | None = Field(default=None)
    openai_model: str = Field(default="gpt-4o-mini")
    redis_url: str | None = Field(default=None)
    database_url: str | None = Field(default=None)
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

