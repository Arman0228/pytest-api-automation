from config.settings import settings


class Environment:
    """Backward-compatible wrapper around pydantic settings."""

    DEV = "DEV"
    PROD = "PROD"

    URLS = {
        DEV: "https://playground.learnqa.ru/api_dev",
        PROD: "https://playground.learnqa.ru/api",
    }

    def __init__(self) -> None:
        self.env = settings.env.value

    def get_base_url(self) -> str:
        return settings.get_base_url()


ENV_OBJECT = Environment()
