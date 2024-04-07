from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: SecretStr
    postgres_port: int = 5432
    postgres_db: str
    postgres_host: str = "localhost"
    debug: bool = False
    # FastAPI settings
    uvicorn_port: int = 5001
    uvicorn_log_level: str = "info"

    model_config = SettingsConfigDict()


service_settings = Settings()
