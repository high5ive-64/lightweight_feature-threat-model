from app.llm.factory import get_provider
from app.schemas import FeatureInput, ThreatModelResponse


class ThreatModelService:
    def __init__(self) -> None:
        self.provider = get_provider()

    def generate(self, feature: FeatureInput) -> ThreatModelResponse:
        return self.provider.generate_threat_model(feature)