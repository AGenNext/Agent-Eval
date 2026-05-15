from typing import Any
from pydantic import BaseModel, Field

class EvalCase(BaseModel):
    id: str
    input: Any
    expected: Any | None = None

class EvalSpec(BaseModel):
    name: str
    metric: str = "exact_match"
    threshold: float = 0.8
    cases: list[EvalCase]

class EvalResult(BaseModel):
    case_id: str
    score: float
    passed: bool
    details: dict[str, Any] = Field(default_factory=dict)

class EvalRun(BaseModel):
    benchmark: str
    average_score: float
    pass_rate: float
    verdict: str
    results: list[EvalResult]
