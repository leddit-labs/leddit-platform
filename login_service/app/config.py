from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/login_db"
    
    JWT_SECRET_KEY: str = "this_is_a_secret_key_for_jwt"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    REDIS_URL: str = "redis://localhost:6379/0"

    BCRYPT_ROUNDS: int = 12

    class Config:
        env_file = ".env"

settings = Settings()