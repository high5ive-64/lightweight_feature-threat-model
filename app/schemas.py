from typing import Literal
from pydantic import BaseModel, Field


Severity = Literal["Low", "Medium", "High"]
StrideCategory = Literal[
    "Spoofing",
    "Tampering",
    "Repudiation",
    "Information Disclosure",
    "Denial of Service",
    "Elevation of Privilege",
]


class FeatureInput(BaseModel):
    feature_name: str = Field(..., examples=["Support ticket attachments"])
    summary: str
    actors: list[str] = Field(default_factory=list)
    data_elements: list[str] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)
    trust_boundaries: list[str] = Field(default_factory=list)
    integrations: list[str] = Field(default_factory=list)
    internet_facing: bool = True
    authentication: str | None = None
    authorization: str | None = None
    sensitive_actions: list[str] = Field(default_factory=list)


class ThreatItem(BaseModel):
    stride: StrideCategory
    title: str
    scenario: str
    impact: str
    likelihood: Severity
    severity: Severity
    mitigations: list[str]
    assumptions: list[str] = Field(default_factory=list)


class ThreatModelResponse(BaseModel):
    feature_name: str
    summary: str
    assets: list[str]
    trust_boundaries: list[str]
    threats: list[ThreatItem]
    abuse_cases: list[str]
    security_questions: list[str]