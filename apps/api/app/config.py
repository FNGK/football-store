from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://amp:amp@localhost:5432/amp"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    cors_origins: str = "http://localhost:3000"
    allowed_hosts: str = "localhost,127.0.0.1"

    rate_limit_per_minute: int = 120

    bootstrap_admin_email: str = ""
    bootstrap_admin_password: str = ""
    bootstrap_tenant_name: str = "Default Organization"

    openai_api_key: str = ""
    agents_enabled: bool = True

    bigquery_project_id: str = ""
    bigquery_dataset: str = ""

    firecracker_socket_path: str = "/var/run/firecracker.sock"

    sentry_dsn: str = ""

    @field_validator("debug", mode="before")
    @classmethod
    def default_debug(cls, v: object, info) -> bool:
        if v is not None and v != "":
            return bool(v)
        env = info.data.get("environment", "development")
        return env == "development"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
