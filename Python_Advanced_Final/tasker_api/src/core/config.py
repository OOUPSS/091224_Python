import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "My Custom API"
    APP_VERSION: str = "1.0.0"
    
    APP_DB_URL: str
    APP_SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    REDIS_HOST: str = "redis_cache"
    REDIS_PORT: int = 6380

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()