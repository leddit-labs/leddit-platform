from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Search Service"

    rabbitmq_host: str
    rabbitmq_port: int = 5672
    rabbitmq_user: str
    rabbitmq_pass: str

    elasticsearch_url: str = "http://elasticsearch:9200"
    elasticsearch_post_index: str = "leddit-posts"
    elasticsearch_community_index: str = "leddit-communities"

    redis_url: str = "redis://redis:6379/0"
    cache_enabled: bool = True
    cache_ttl_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

