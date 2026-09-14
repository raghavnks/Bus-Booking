from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "BusBooking Business Services"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "local"

    POSTGRES_HOST: str = "192.168.29.225"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "busbooking"
    POSTGRES_USER: str = "busbooking"
    POSTGRES_PASSWORD: str = ""

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    @property
    def database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
