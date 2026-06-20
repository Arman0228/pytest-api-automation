from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


BASE_URLS = {
    Environment.DEV: "https://playground.learnqa.ru/api_dev",
    Environment.PROD: "https://playground.learnqa.ru/api",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Environment = Environment.DEV

    def get_base_url(self) -> str:
        return BASE_URLS[self.env]


settings = Settings()
