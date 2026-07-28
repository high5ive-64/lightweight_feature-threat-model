from abc import ABC, abstractmethod
from app.schemas import FeatureInput, ThreatModelResponse


class LLMProvider(ABC):
    @abstractmethod
    def generate_threat_model(self, feature: FeatureInput) -> ThreatModelResponse:
        raise NotImplementedError