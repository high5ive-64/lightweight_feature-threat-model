from app.schemas import FeatureInput


SYSTEM_PROMPT = """
You are a senior application security engineer.
Assess only the net-new feature and any changed trust boundaries.
Do not repeat generic platform threats unless they are newly introduced.
Return concise, actionable STRIDE threats and mitigations.
If context is missing, capture that in security_questions and assumptions.
You must return only valid JSON that matches the requested schema.
""".strip()


def build_messages(feature: FeatureInput) -> list[dict]:
    user_prompt = f"""
Create a STRIDE threat model for this feature.

Feature name: {feature.feature_name}
Summary: {feature.summary}
Actors: {", ".join(feature.actors) or "Unknown"}
Data elements: {", ".join(feature.data_elements) or "Unknown"}
Entry points: {", ".join(feature.entry_points) or "Unknown"}
Trust boundaries: {", ".join(feature.trust_boundaries) or "Unknown"}
Integrations: {", ".join(feature.integrations) or "None"}
Internet facing: {"Yes" if feature.internet_facing else "No"}
Authentication: {feature.authentication or "Not provided"}
Authorization: {feature.authorization or "Not provided"}
Sensitive actions: {", ".join(feature.sensitive_actions) or "None"}

Return JSON with this structure:
- feature_name
- summary
- assets
- trust_boundaries
- threats[]
- abuse_cases[]
- security_questions[]

Each threat must include:
- stride
- title
- scenario
- impact
- likelihood
- severity
- mitigations[]
- assumptions[]
""".strip()

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]