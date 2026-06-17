from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://bou_sentinel:sentinel_pass_2024@postgres:5432/bou_sentinel"
    DATABASE_URL_SYNC: str = "postgresql://bou_sentinel:sentinel_pass_2024@postgres:5432/bou_sentinel"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # API
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: str = '["http://localhost:3000"]'

    # External APIs
    OPENEXCHANGERATES_APP_ID: str = "demo"
    OPENWEATHERMAP_API_KEY: str = "demo"

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def cors_origin_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)


settings = Settings()