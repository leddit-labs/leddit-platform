from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str

    database_url: str
    rabbitmq_url: str

    grpc_port: int = 50051

    user_id_header: str = "X-User-Id"

    model_config = {"env_file": ".env"}


settings = Settings()
