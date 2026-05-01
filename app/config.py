from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    DB_NAME: str = "trade_parser"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()