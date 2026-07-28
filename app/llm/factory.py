from app.config import settings
from app.llm.base import LLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.llm.lmstudio_provider import LMStudioProvider
from app.llm.claude_provider import ClaudeProvider


def get_provider() -> LLMProvider:
    provider = settings.provider.lower()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "lmstudio":
        return LMStudioProvider()
    if provider == "claude":
        return ClaudeProvider()
    raise ValueError(f"Unsupported provider: {provider}")


def list_supported_providers() -> list[str]:
    return ["openai", "lmstudio", "claude"]