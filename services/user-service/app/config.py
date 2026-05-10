from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://leddit:leddit@localhost:5432/leddit"
    keycloak_url: str = "http://localhost:8080"
    keycloak_realm: str = "leddit"
    keycloak_client_id: str = "leddit-api"
    keycloak_client_secret: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()