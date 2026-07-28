import json
import re
from openai import OpenAI
from pydantic import ValidationError
from app.config import settings
from app.llm.base import LLMProvider
from app.prompting import build_messages
from app.schemas import FeatureInput, ThreatModelResponse


def extract_json_object(text: str) -> str:
    # If the model wraps JSON in markdown code fences, extract it
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if match:
        return match.group(1)
    # Otherwise, try to find a top-level {...} block
    start = text.find("{")
    if start == -1:
        return text
    depth = 0
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return text[start:]


class LMStudioProvider(LLMProvider):
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.lmstudio_api_key,
            base_url=settings.lmstudio_base_url,
        )
        self.model = settings.lmstudio_model

    def generate_threat_model(self, feature: FeatureInput) -> ThreatModelResponse:
        messages = build_messages(feature)
        retries = settings.max_retries
        last_error = None

        for attempt in range(retries + 1):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,
            )

            raw_text = (response.choices[0].message.content or "").strip()
            if not raw_text:
                last_error = ValueError("LM Studio returned empty response")
                messages.append({
                    "role": "system",
                    "content": "Return only valid JSON matching the schema. Do not include any commentary."
                })
                continue

            # Try to extract a JSON object from the text
            candidate = extract_json_object(raw_text)

            try:
                data = json.loads(candidate)
                return ThreatModelResponse.model_validate(data)
            except (json.JSONDecodeError, ValidationError) as exc:
                last_error = exc
                # Append a stronger system instruction for retry
                messages.append({
                    "role": "system",
                    "content": "Your previous answer was not valid JSON. Return ONLY a JSON object that matches the required schema. No markdown, no explanation."
                })

        raise ValueError(f"LM Studio output failed validation after retries: {last_error}")