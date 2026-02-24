from enum import Enum

from pydantic import computed_field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    APP_NAME: str = "ReportApi"
    APP_DESCRIPTION: str | None = None
    APP_VERSION: str | None = None
    LICENSE_NAME: str | None = None
    CONTACT_NAME: str | None = None
    CONTACT_EMAIL: str | None = None


class EnvironmentOption(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

class CORSSettings(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = EnvironmentOption.LOCAL

class FileLoggerSettings(BaseSettings):
    FILE_LOG_MAX_BYTES: int = 10 * 1024 * 1024
    FILE_LOG_BACKUP_COUNT: int = 3
    FILE_LOG_FORMAT_JSON: bool = True
    FILE_LOG_LEVEL: str = "INFO"

    # Include request ID, path, method, client host, and status code in the file log
    FILE_LOG_INCLUDE_REQUEST_ID: bool = True
    FILE_LOG_INCLUDE_PATH: bool = True
    FILE_LOG_INCLUDE_METHOD: bool = True
    FILE_LOG_INCLUDE_CLIENT_HOST: bool = True
    FILE_LOG_INCLUDE_STATUS_CODE: bool = True

class ConsoleLoggerSettings(BaseSettings):
    CONSOLE_LOG_LEVEL: str = "INFO"
    CONSOLE_LOG_FORMAT_JSON: bool = False

    # Include request ID, path, method, client host, and status code in the console log
    CONSOLE_LOG_INCLUDE_REQUEST_ID: bool = False
    CONSOLE_LOG_INCLUDE_PATH: bool = False
    CONSOLE_LOG_INCLUDE_METHOD: bool = False
    CONSOLE_LOG_INCLUDE_CLIENT_HOST: bool = False
    CONSOLE_LOG_INCLUDE_STATUS_CODE: bool = False

class DatabaseSettings(BaseSettings):
    pass

class DBAPostgresSettings(DatabaseSettings):
    DBAPOSTGRES_USER: str = "postgres"
    DBAPOSTGRES_PASSWORD: str = "postgres"
    DBAPOSTGRES_SERVER: str = "localhost"
    DBAPOSTGRES_PORT: int = 5432
    DBAPOSTGRES_DB: str = "postgres"
    DBAPOSTGRES_SYNC_PREFIX: str = "postgresql://"
    DBAPOSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"
    DBAPOSTGRES_URL: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DBAPOSTGRES_URI(self) -> str:
        credentials = f"{self.DBAPOSTGRES_USER}:{self.DBAPOSTGRES_PASSWORD}"
        location = f"{self.DBAPOSTGRES_SERVER}:{self.DBAPOSTGRES_PORT}/{self.DBAPOSTGRES_DB}"
        return f"{credentials}@{location}"

class SQLFileSettings(BaseSettings):
    BASE_FILE:str = "src/app/sql/"


class RateLimitSettings(BaseSettings):
    pass

class SlowapiSettings(RateLimitSettings):
    GLOBAL_GENERIC_LIMIT: int = 60

class Settings(
    AppSettings,
    EnvironmentSettings,
    FileLoggerSettings,
    ConsoleLoggerSettings,
    DBAPostgresSettings,
    SQLFileSettings,
    SlowapiSettings,
    CORSSettings,
):
    class Config:
        env_file = None

settings = Settings()
