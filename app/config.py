"""
Master configuration for Feature Threat Model.

Edit this file to set all variables for the application.
You can also override via environment variables or .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


ProviderType = Literal["openai", "lmstudio", "claude"]


class Settings(BaseSettings):
    # App settings
    app_name: str = "Feature Threat Model API"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # Provider selection: "openai", "lmstudio", or "claude"
    provider: ProviderType = "openai"

    # OpenAI settings
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str | None = None  # Optional custom base URL

    # LM Studio settings
    lmstudio_base_url: str = "http://127.0.0.1:1234/v1"
    lmstudio_api_key: str = "lm-studio"
    lmstudio_model: str = "local-model"

    # Claude settings
    claude_api_key: str | None = None
    claude_model: str = "claude-sonnet-4-20250514"

    # Threat model generation settings
    max_retries: int = 2
    default_severity: str = "Medium"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


# Create a singleton instance
settings = Settings()


if __name__ == "__main__":
    # Print current config for debugging
    import json
    print("Current configuration:")
    print(json.dumps(settings.model_dump(), indent=2, default=str))