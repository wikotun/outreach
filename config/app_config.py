"""Application configuration settings.

This module defines the application configuration using Pydantic settings,
loading values from environment variables and .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Application configuration loaded from environment variables.

    Configuration values are loaded from environment variables or a .env file.
    All fields are required unless a default is specified.

    Attributes:
        database_url: Full database connection URL.
        secret_key: Secret key for JWT token signing.
        algorithm: Algorithm used for JWT encoding (e.g., HS256).
        access_token_expire_minutes: Token expiration time in minutes.
        db_username: Database username for connection.
        db_password: Database password for connection.
        host: Host address for the API server.
        port: Port number for the API server.
        log_level: Logging level (e.g., info, debug, warning).
    """

    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_username: str
    db_password: str
    host: str
    port: int
    log_level: str

    model_config = SettingsConfigDict(env_file=".env")


# Singleton instance
settings = AppConfig()
