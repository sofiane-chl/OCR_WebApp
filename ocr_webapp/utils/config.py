"""Application configuration via environment variables (pydantic-settings)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # App
    app_name: str = "OCR WebApp"
    debug: bool = False
    log_level: str = "INFO"

    # API
    api_prefix: str = "/api/v1"
    allowed_origins: list[str] = ["*"]

    # OCR
    tesseract_lang: str = "eng"
    max_upload_size_mb: int = 10


# Singleton — import this everywhere
settings = Settings()
