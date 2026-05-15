import yaml
from .models import EvalSpec, EvalResult, EvalRun
from .scorers import SCORERS


def load_spec(path: str) -> EvalSpec:
    with open(path, 'r') as f:
        return EvalSpec.model_validate(yaml.safe_load(f))


def run_eval(spec: EvalSpec, predict):
    scorer = SCORERS[spec.metric]
    results = []
    for case in spec.cases:
        actual = predict(case.input)
        score = scorer(case.expected, actual)
        results.append(EvalResult(case_id=case.id, score=score, passed=score >= spec.threshold))

    avg = sum(r.score for r in results) / len(results)
    pass_rate = sum(r.passed for r in results) / len(results)
    verdict = 'approved' if avg >= spec.threshold else 'blocked'
    return EvalRun(
        benchmark=spec.name,
        average_score=avg,
        pass_rate=pass_rate,
        verdict=verdict,
        results=results,
    )
