from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )

    database_url: str
    rabbitmq_url: str

    grpc_port: int = 50051


@lru_cache()
def get_settings() -> Settings:
    return Settings()
