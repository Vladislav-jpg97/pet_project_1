import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        extra="ignore",
    )
    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    # Redis
    redis_url: str

    # Celery
    celery_broker_url: str
    celery_result_backend: str

    # Security & JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 300

    # General
    base_url: str = "http://localhost:8001"

settings = Settings()