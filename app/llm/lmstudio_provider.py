import json
from openai import OpenAI
from pydantic import ValidationError
from app.config import settings
from app.llm.base import LLMProvider
from app.prompting import build_messages
from app.schemas import FeatureInput, ThreatModelResponse


class LMStudioProvider(LLMProvider):
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.lmstudio_api_key,
            base_url=settings.lmstudio_base_url,
        )
        self.model = settings.lmstudio_model

    def generate_threat_model(self, feature: FeatureInput) -> ThreatModelResponse:
        messages = build_messages(feature)
        retries = 2
        last_error = None

        for _ in range(retries + 1):
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                text={"format": {"type": "json_object"}},
            )

            raw_text = getattr(response, "output_text", None)
            if not raw_text:
                chunks = []
                for item in getattr(response, "output", []):
                    if getattr(item, "type", None) != "message":
                        continue
                    for content in getattr(item, "content", []):
                        if getattr(content, "type", None) == "output_text":
                            chunks.append(content.text)
                raw_text = "".join(chunks)

            if not raw_text:
                last_error = ValueError("LM Studio returned no text output")
                messages.append({
                    "role": "system",
                    "content": "Return only valid JSON matching the schema. Do not include markdown fences or commentary."
                })
                continue

            try:
                data = json.loads(raw_text)
                return ThreatModelResponse.model_validate(data)
            except (json.JSONDecodeError, ValidationError) as exc:
                last_error = exc
                messages.append({
                    "role": "system",
                    "content": "Your previous answer was invalid. Return only valid JSON matching the exact schema with all required fields."
                })

        raise ValueError(f"LM Studio output failed validation after retries: {last_error}")