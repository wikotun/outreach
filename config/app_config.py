from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_username: str
    db_password: str
    host: str
    port: int
    log_level: str

    class Config:
        env_file = ".env"

    # Singleton instance
settings = AppConfig()
