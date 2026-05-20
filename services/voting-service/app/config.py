from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str

    database_write_url: str
    database_read_url: str

    rabbitmq_host: str
    rabbitmq_port: int = 5672

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
