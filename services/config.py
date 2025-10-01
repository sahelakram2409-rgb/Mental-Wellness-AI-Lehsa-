import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Mental Wellness API")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    # AI provider configuration (mock by default; swap later)
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "mock")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "mock-model")

    # Optional API key (not required for mock)
    API_KEY: str | None = os.getenv("API_KEY")


settings = Settings()
