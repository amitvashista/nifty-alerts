
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # App
    env: str = Field(default="dev")
    tz: str = Field(default="Asia/Kolkata")
    log_level: str = Field(default="INFO")

    # Notifications
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    # Broker placeholders
    broker: str | None = None
    zerodha_api_key: str | None = None
    zerodha_api_secret: str | None = None
    zerodha_access_token: str | None = None

    # Optional infra
    postgres_dsn: str | None = None
    redis_url: str | None = None

    class Config:
        env_file = "config/.env"

settings = Settings()
