from typing import Any
from pydantic import BaseModel, Field


class ClearWeights(BaseModel):
    cost: float = 0.15
    latency: float = 0.15
    efficacy: float = 0.35
    assurance: float = 0.20
    reliability: float = 0.15


class EvalCase(BaseModel):
    id: str
    input: Any
    expected: Any | None = None
    policies: list[str] = Field(default_factory=list)
    max_latency_ms: int | None = None
    max_cost_usd: float | None = None


class EvalSpec(BaseModel):
    name: str
    metric: str = "exact_match"
    threshold: float = 0.8
    reliability_runs: int = 1
    weights: ClearWeights = Field(default_factory=ClearWeights)
    cases: list[EvalCase]


class TraceEvent(BaseModel):
    name: str
    event_type: str = "step"
    latency_ms: int = 0
    cost_usd: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class Prediction(BaseModel):
    output: Any
    latency_ms: int = 0
    cost_usd: float = 0.0
    policy_violations: list[str] = Field(default_factory=list)
    trace: list[TraceEvent] = Field(default_factory=list)


class ClearScore(BaseModel):
    cost: float
    latency: float
    efficacy: float
    assurance: float
    reliability: float
    composite: float


class EvalResult(BaseModel):
    case_id: str
    score: float
    passed: bool
    clear: ClearScore
    latency_ms: int = 0
    cost_usd: float = 0.0
    policy_violations: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)


class EvalRun(BaseModel):
    benchmark: str
    average_score: float
    pass_rate: float
    clear: ClearScore
    verdict: str
    results: list[EvalResult]
