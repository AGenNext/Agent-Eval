from .models import ClearScore, ClearWeights


def bounded_inverse(value: float, target: float | None) -> float:
    if target is None or target <= 0:
        return 1.0
    return min(1.0, target / max(value, 1e-9))


def compute_clear_score(*, efficacy: float, latency_ms: int, cost_usd: float,
                        policy_violations: int, reliability: float,
                        max_latency_ms: int | None = None,
                        max_cost_usd: float | None = None,
                        weights: ClearWeights | None = None) -> ClearScore:
    weights = weights or ClearWeights()
    cost = bounded_inverse(cost_usd, max_cost_usd)
    latency = bounded_inverse(latency_ms, max_latency_ms)
    assurance = 1.0 if policy_violations == 0 else max(0.0, 1.0 - 0.25 * policy_violations)
    composite = (
        weights.cost * cost +
        weights.latency * latency +
        weights.efficacy * efficacy +
        weights.assurance * assurance +
        weights.reliability * reliability
    )
    return ClearScore(
        cost=cost,
        latency=latency,
        efficacy=efficacy,
        assurance=assurance,
        reliability=reliability,
        composite=composite,
    )
