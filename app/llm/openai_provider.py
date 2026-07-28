from openai import OpenAI
from app.config import settings
from app.llm.base import LLMProvider
from app.prompting import build_messages
from app.schemas import FeatureInput, ThreatModelResponse


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for provider=openai")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate_threat_model(self, feature: FeatureInput) -> ThreatModelResponse:
        response = self.client.responses.parse(
            model=self.model,
            input=build_messages(feature),
            text_format=ThreatModelResponse,
        )
        if not response.output_parsed:
            raise ValueError("Model did not return a parsable structured response")
        return response.output_parsed