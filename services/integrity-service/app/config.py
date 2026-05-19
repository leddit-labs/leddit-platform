from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int = 5672
    rabbitmq_user: str
    rabbitmq_pass: str

    deepseek_api_key: str
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-v4-flash"

    model_config = {"env_file": ".env"}

settings = Settings()
