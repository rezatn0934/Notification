from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE_NUMBER: int

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EMAIL_HOST: str
    EMAIL_USE_TLS: bool
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def load_settings():
    return Settings()


settings = load_settings()
