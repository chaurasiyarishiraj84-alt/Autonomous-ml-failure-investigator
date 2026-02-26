from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Application
    app_name: str = Field(default="Autonomous ML Failure Investigator")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    # Security (safe default for dev)
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")

    # Logging
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Loaded once per process.
    """
    return Settings()

