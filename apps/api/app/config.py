from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://amp:amp@localhost:5432/amp"
    bigquery_project_id: str = ""
    bigquery_dataset: str = ""
    firecracker_socket_path: str = "/var/run/firecracker.sock"
    openai_api_key: str = ""
    default_tenant_id: str = "demo-tenant"


settings = Settings()
