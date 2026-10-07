import os
from dataclasses import dataclass
from functools import lru_cache
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = "Asia/Kolkata"


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    app_timezone: str
    cors_origins: list[str]
    log_level: str

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.app_timezone)


def _csv_env(name: str, default: str) -> list[str]:
    raw_value = os.getenv(name, default)
    return [value.strip() for value in raw_value.split(",") if value.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "TODO List Voice Note API"),
        app_env=os.getenv("APP_ENV", "development"),
        app_timezone=os.getenv("APP_TIMEZONE", DEFAULT_TIMEZONE),
        cors_origins=_csv_env(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
