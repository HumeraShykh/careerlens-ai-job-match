from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or .env files."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    careerlens_env: str = "development"
    careerlens_host: str = "0.0.0.0"
    careerlens_port: int = 8000
    careerlens_cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5174,http://127.0.0.1:5174,"
        "http://localhost:5175,http://127.0.0.1:5175"
    )
    database_url: str = "postgresql+psycopg://careerlens:careerlens_dev@localhost:5432/careerlens"
    database_enabled: bool = True
    max_upload_mb: int = 5

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.careerlens_cors_origins.split(",") if item.strip()]

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
