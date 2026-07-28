import json
from anthropic import Anthropic
from pydantic import ValidationError
from app.config import settings
from app.llm.base import LLMProvider
from app.prompting import build_messages
from app.schemas import FeatureInput, ThreatModelResponse


class ClaudeProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.claude_api_key:
            raise ValueError("CLAUDE_API_KEY is required for provider=claude")
        self.client = Anthropic(api_key=settings.claude_api_key)
        self.model = settings.claude_model

    def generate_threat_model(self, feature: FeatureInput) -> ThreatModelResponse:
        messages = build_messages(feature)
        retries = settings.max_retries
        last_error = None

        # Extract system prompt
        system_prompt = ""
        user_content = ""
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            elif msg["role"] == "user":
                user_content = msg["content"]

        for attempt in range(retries + 1):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_content}],
                )

                raw_text = response.content[0].text

                # Try to parse JSON from response
                # Claude may wrap in markdown code blocks
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json").split("```").strip()[1]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()

                data = json.loads(raw_text)
                return ThreatModelResponse.model_validate(data)

            except (json.JSONDecodeError, ValidationError, IndexError, KeyError) as exc:
                last_error = exc
                if attempt < retries:
                    user_content += "\n\nYour previous response was invalid. Return only valid JSON matching the exact schema with all required fields. Do not include markdown code blocks."

        raise ValueError(f"Claude output failed validation after retries: {last_error}")