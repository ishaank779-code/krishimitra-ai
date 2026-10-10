from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://krishi:krishi123@localhost:3306/krishimitra"
    SECRET_KEY: str = "krishimitra-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    APP_NAME: str = "KrishiMitra AI"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
